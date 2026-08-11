"""版付きconfigとlockから開発用venvを機械構築・検証する。"""

import argparse
import dataclasses
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path


_CONFIG_FIELDS = {
    "environment_id",
    "environment_version",
    "base_python",
    "venv_path",
    "venv_python",
    "python",
    "pytest",
    "required_imports",
    "lock",
    "toolchain_command",
    "install_command",
}


class DevelopmentEnvironmentError(Exception):
    """再現可能な開発環境を構築または検証できない。"""


@dataclasses.dataclass(frozen=True)
class DevelopmentEnvironmentResult:
    status: str
    python_version: str
    pytest_version: str = "not_verified"


from tools.common.digests import sha256_hex as _sha256


def _version(value):
    match = re.search(r"([0-9]+(?:\.[0-9]+)+)", value)
    if match is None:
        raise DevelopmentEnvironmentError("version_unreadable")
    return match.group(1)


def _version_tuple(value):
    return tuple(int(part) for part in _version(value).split("."))


def _in_range(actual, minimum, maximum):
    width = max(len(actual), len(minimum), len(maximum))
    normalized = lambda item: item + (0,) * (width - len(item))
    return normalized(minimum) <= normalized(actual) < normalized(maximum)


def _project_path(project_root, relative_path):
    root = Path(project_root).resolve()
    path = Path(relative_path)
    if path.is_absolute() or not path.parts:
        raise DevelopmentEnvironmentError("project_path_invalid")
    resolved = Path(os.path.abspath(str(root / path)))
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise DevelopmentEnvironmentError("project_path_invalid") from error
    return resolved


def load_config(path):
    try:
        config = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise DevelopmentEnvironmentError("environment_config_invalid") from error
    if set(config) != _CONFIG_FIELDS:
        raise DevelopmentEnvironmentError("environment_config_invalid")
    if (
        config["environment_id"] != "RC3-DEVELOPMENT-VENV"
        or config["environment_version"] != 1
        or config["venv_path"] != ".venv"
        or config["venv_python"] != ".venv/bin/python3"
        or config["toolchain_command"][0] != config["venv_python"]
        or config["install_command"][0] != config["venv_python"]
    ):
        raise DevelopmentEnvironmentError("environment_config_invalid")
    return config


def _run(run, command, *, project_root, failure):
    result = run(
        list(command),
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise DevelopmentEnvironmentError(failure)
    return result


def _validate_lock(config, project_root):
    lock = _project_path(project_root, config["lock"]["path"])
    try:
        content = lock.read_bytes()
    except OSError as error:
        raise DevelopmentEnvironmentError("dependency_lock_missing") from error
    if _sha256(content) != config["lock"]["sha256"]:
        raise DevelopmentEnvironmentError("dependency_lock_digest_mismatch")


def _declared_project_scripts(project_root):
    path = _project_path(project_root, "pyproject.toml")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise DevelopmentEnvironmentError("project_scripts_invalid") from error
    section = None
    distribution = None
    scripts = {}
    section_pattern = re.compile(r"\[([A-Za-z0-9_.-]+)\]")
    assignment_pattern = re.compile(
        r'([A-Za-z0-9_.-]+)\s*=\s*"([^"]+)"\s*(?:#.*)?'
    )
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        section_match = section_pattern.fullmatch(stripped)
        if section_match is not None:
            section = section_match.group(1)
            continue
        if section not in {"project", "project.scripts"}:
            continue
        assignment = assignment_pattern.fullmatch(stripped)
        if assignment is None:
            if section == "project.scripts":
                raise DevelopmentEnvironmentError("project_scripts_invalid")
            continue
        name, value = assignment.groups()
        if section == "project" and name == "name":
            if distribution is not None:
                raise DevelopmentEnvironmentError("project_scripts_invalid")
            distribution = value
        elif section == "project.scripts":
            if name in scripts:
                raise DevelopmentEnvironmentError("project_scripts_invalid")
            scripts[name] = value
    if distribution is None or not scripts:
        raise DevelopmentEnvironmentError("project_scripts_invalid")
    return distribution, scripts


def _installed_project_scripts(config, project_root, distribution, run):
    script = (
        "import importlib.metadata as m,json; "
        f"d=m.distribution({distribution!r}); "
        "print(json.dumps(sorted((e.name,e.value) for e in d.entry_points "
        "if e.group==\"console_scripts\")))"
    )
    result = _run(
        run,
        (config["venv_python"], "-c", script),
        project_root=project_root,
        failure="project_scripts_unavailable",
    )
    try:
        pairs = json.loads(result.stdout)
        if (
            not isinstance(pairs, list)
            or any(
                not isinstance(pair, list)
                or len(pair) != 2
                or not all(isinstance(value, str) for value in pair)
                for pair in pairs
            )
        ):
            raise ValueError
        installed = dict(pairs)
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        raise DevelopmentEnvironmentError("project_scripts_unavailable") from error
    if len(installed) != len(pairs):
        raise DevelopmentEnvironmentError("project_scripts_unavailable")
    return installed


def verify_environment(*, config, project_root, run=subprocess.run):
    root = Path(project_root).resolve()
    python = _project_path(root, config["venv_python"])
    if not python.is_file():
        raise DevelopmentEnvironmentError("venv_python_missing")
    python_result = _run(
        run,
        (config["venv_python"], "--version"),
        project_root=root,
        failure="venv_python_unavailable",
    )
    python_version = _version(python_result.stdout or python_result.stderr)
    if not _in_range(
        _version_tuple(python_version),
        _version_tuple(config["python"]["minimum_version"]),
        _version_tuple(config["python"]["maximum_exclusive_version"]),
    ):
        raise DevelopmentEnvironmentError("venv_python_version_out_of_range")
    pytest_result = _run(
        run,
        (config["venv_python"], "-m", "pytest", "--version"),
        project_root=root,
        failure="pytest_unavailable",
    )
    pytest_version = _version(pytest_result.stdout or pytest_result.stderr)
    if pytest_version != config["pytest"]["exact_version"]:
        raise DevelopmentEnvironmentError("pytest_version_mismatch")
    for package, expected in config["required_imports"].items():
        script = (
            "import importlib.metadata as m; "
            f"print(m.version({package!r}))"
        )
        result = _run(
            run,
            (config["venv_python"], "-c", script),
            project_root=root,
            failure=f"required_import_unavailable:{package}",
        )
        if result.stdout.strip() != expected:
            raise DevelopmentEnvironmentError(
                f"required_import_version_mismatch:{package}"
            )
    distribution, declared_scripts = _declared_project_scripts(root)
    installed_scripts = _installed_project_scripts(
        config,
        root,
        distribution,
        run,
    )
    if installed_scripts != declared_scripts:
        raise DevelopmentEnvironmentError("project_scripts_mismatch")
    return DevelopmentEnvironmentResult(
        status="verified",
        python_version=python_version,
        pytest_version=pytest_version,
    )


def bootstrap_environment(
    *,
    config,
    project_root,
    locate=shutil.which,
    run=subprocess.run,
    verify=True,
):
    root = Path(project_root).resolve()
    _validate_lock(config, root)
    base = config["base_python"]
    if locate(base) is None:
        raise DevelopmentEnvironmentError("base_python_missing")
    base_result = _run(
        run,
        (base, "--version"),
        project_root=root,
        failure="base_python_unavailable",
    )
    base_version = _version(base_result.stdout or base_result.stderr)
    if not _in_range(
        _version_tuple(base_version),
        _version_tuple(config["python"]["minimum_version"]),
        _version_tuple(config["python"]["maximum_exclusive_version"]),
    ):
        raise DevelopmentEnvironmentError(
            "base_python_version_out_of_range"
        )
    venv = _project_path(root, config["venv_path"])
    venv_python = _project_path(root, config["venv_python"])
    status = "updated"
    if not venv.exists():
        _run(
            run,
            (base, "-m", "venv", config["venv_path"]),
            project_root=root,
            failure="venv_creation_failed",
        )
        status = "created"
    if not venv_python.is_file():
        raise DevelopmentEnvironmentError("venv_python_missing")
    _run(
        run,
        tuple(config["toolchain_command"]),
        project_root=root,
        failure="toolchain_install_failed",
    )
    _run(
        run,
        tuple(config["install_command"]),
        project_root=root,
        failure="locked_install_failed",
    )
    if verify:
        checked = verify_environment(
            config=config,
            project_root=root,
            run=run,
        )
        return dataclasses.replace(checked, status=status)
    return DevelopmentEnvironmentResult(
        status=status,
        python_version=base_version,
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="config/development-environment.json",
    )
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args(argv)
    root = Path(args.project_root).resolve()
    config = load_config(root / args.config)
    result = bootstrap_environment(config=config, project_root=root)
    print(json.dumps(dataclasses.asdict(result), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
