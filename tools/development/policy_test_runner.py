"""版付きrepository policyだけから公式Testを実行しreceiptを作る。

receiptの`test_summary`は、pytestのmachine API（report object）から数えた構造化集計である。
実行結果の出力文字列から件数を取り出すことはしない。集計の各fieldの意味は
`tools/development/pytest_summary.py`のdocstringを正本とする。
"""

import argparse
import dataclasses
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from tools.development import pytest_summary


class TestRunnerPolicyError(Exception):
    """Test runner policyが不正である。"""


class TestEnvironmentUnavailable(Exception):
    """設定されたTest環境を利用できない。"""


@dataclasses.dataclass(frozen=True)
class TestExecution:
    status: str
    exit_code: int
    receipt_path: str


def _canonical_digest(value):
    return hashlib.sha256(
        json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def _version_tuple(value):
    match = re.search(r"([0-9]+(?:\.[0-9]+)+)", value)
    if match is None:
        raise TestEnvironmentUnavailable(
            "test_environment_unavailable: version_unreadable"
        )
    return tuple(int(part) for part in match.group(1).split("."))


def _version_text(value):
    match = re.search(r"([0-9]+(?:\.[0-9]+)+)", value)
    if match is None:
        raise TestEnvironmentUnavailable(
            "test_environment_unavailable: version_unreadable"
        )
    return match.group(1)


def _version_in_range(actual, minimum, maximum_exclusive):
    width = max(len(actual), len(minimum), len(maximum_exclusive))
    normalized = lambda value: value + (0,) * (width - len(value))
    return (
        normalized(actual) >= normalized(minimum)
        and normalized(actual) < normalized(maximum_exclusive)
    )


def load_config(path):
    path = Path(path)
    try:
        config = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise TestRunnerPolicyError(
            f"cannot load Test runner policy: {path}"
        ) from error
    required = {
        "runner_id",
        "runner_version",
        "python",
        "pytest",
        "suites",
        "fallback",
        "receipt_required",
    }
    if set(config) != required:
        raise TestRunnerPolicyError(
            "Test runner policy fields are incomplete or unknown"
        )
    if (
        config["runner_id"] != "RC3-DEVELOPMENT-TEST-RUNNER"
        or config["runner_version"] < 1
        or config["fallback"] != "forbidden"
        or config["receipt_required"] is not True
    ):
        raise TestRunnerPolicyError(
            "Test runner policy identity or safety boundary is invalid"
        )
    for suite, command in config["suites"].items():
        if (
            not suite
            or not isinstance(command, list)
            or not command
            or any(not isinstance(part, str) or not part for part in command)
            or command[0] != config["python"]["command"]
        ):
            raise TestRunnerPolicyError(
                "Test suite command must use the configured Python"
            )
    return config


def command_for(config, suite):
    try:
        return tuple(config["suites"][suite])
    except KeyError as error:
        raise TestRunnerPolicyError(
            f"unknown Test suite: {suite}"
        ) from error


def _check_version(label, output, policy):
    actual = _version_tuple(output)
    minimum = _version_tuple(policy["minimum_version"])
    maximum = _version_tuple(policy["maximum_exclusive_version"])
    if not _version_in_range(actual, minimum, maximum):
        raise TestEnvironmentUnavailable(
            f"test_environment_unavailable: {label}_version_out_of_range"
        )
    return _version_text(output)


def _source_state_digest(project_root, *, excluded_paths=()):
    ignored = {".git", ".pytest_cache", ".venv", "__pycache__"}
    excluded = {
        Path(path).resolve()
        for path in excluded_paths
    }
    digest = hashlib.sha256()
    paths = sorted(
        path
        for path in project_root.rglob("*")
        if path.is_file()
        and path.resolve() not in excluded
        and not ignored.intersection(path.relative_to(project_root).parts)
        and not any(
            part.endswith(".egg-info")
            for part in path.relative_to(project_root).parts
        )
    )
    for path in paths:
        relative = path.relative_to(project_root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def _run_checked(run, command, *, project_root, failure):
    result = run(
        list(command),
        cwd=project_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise TestEnvironmentUnavailable(
            f"test_environment_unavailable: {failure}"
        )
    return result


def _write_receipt(path, receipt):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content)
    temporary.replace(path)


def execute(
    *,
    config,
    project_root,
    suite,
    receipt_path,
    locate=shutil.which,
    run=subprocess.run,
):
    project_root = Path(project_root).resolve()
    command = command_for(config, suite)
    python_command = config["python"]["command"]
    if locate(python_command) is None:
        raise TestEnvironmentUnavailable(
            "test_environment_unavailable: configured_python_missing"
        )

    python_result = _run_checked(
        run,
        (python_command, "--version"),
        project_root=project_root,
        failure="python_preflight_failed",
    )
    python_output = python_result.stdout or python_result.stderr
    python_version = _check_version(
        "python",
        python_output,
        config["python"],
    )
    pytest_result = _run_checked(
        run,
        (python_command, "-m", "pytest", "--version"),
        project_root=project_root,
        failure="pytest_preflight_failed",
    )
    pytest_output = pytest_result.stdout or pytest_result.stderr
    pytest_version = _check_version(
        "pytest",
        pytest_output,
        config["pytest"],
    )
    if receipt_path is None and config["receipt_required"]:
        raise TestRunnerPolicyError(
            "official Test execution requires a receipt path"
        )

    receipt_output = Path(receipt_path)
    if not receipt_output.is_absolute():
        receipt_output = project_root / receipt_output

    # 集計の受け渡しfileはreceiptの隣に置き、読み終えたら消す。source state digestからは除く。
    summary_output = receipt_output.with_name(receipt_output.name + ".summary.json")
    source_state_digest = _source_state_digest(
        project_root,
        excluded_paths=(receipt_output, summary_output),
    )
    try:
        test_result = run(
            list(command),
            cwd=project_root,
            capture_output=True,
            text=True,
            env=dict(
                os.environ,
                **{pytest_summary.SUMMARY_ENVIRONMENT_VARIABLE: str(summary_output)},
            ),
        )
        try:
            test_summary = pytest_summary.read_summary(summary_output)
        except pytest_summary.TestSummaryError as error:
            raise TestRunnerPolicyError(str(error)) from error
    finally:
        if summary_output.exists():
            summary_output.unlink()

    status = "passed" if test_result.returncode == 0 else "failed"
    if status == "passed" and (test_summary["failed"] or test_summary["errors"]):
        raise TestRunnerPolicyError(
            "test_summary_inconsistent: passed status with failed or errored tests"
        )
    receipt = {
        "receipt_kind": "policy_test_verification_run",
        "runner_id": config["runner_id"],
        "runner_version": config["runner_version"],
        "recorded_at": datetime.datetime.now(
            datetime.timezone.utc
        ).astimezone().isoformat(timespec="seconds"),
        "suite": suite,
        "command": " ".join(command),
        "configured_python": python_command,
        "resolved_python": locate(python_command),
        "python_version": python_version,
        "pytest_version": pytest_version,
        "fallback_used": False,
        "config_digest": _canonical_digest(config),
        "source_state_digest": source_state_digest,
        "status": status,
        "exit_code": test_result.returncode,
        "test_summary": test_summary,
        "stdout": test_result.stdout,
        "stderr": test_result.stderr,
    }
    _write_receipt(receipt_output, receipt)
    return TestExecution(
        status=status,
        exit_code=test_result.returncode,
        receipt_path=str(receipt_output),
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        default="config/development-test-runner.json",
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--suite", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args(argv)
    project_root = Path(args.project_root).resolve()
    config = load_config(project_root / args.config)
    result = execute(
        config=config,
        project_root=project_root,
        suite=args.suite,
        receipt_path=Path(args.receipt),
    )
    print(json.dumps(dataclasses.asdict(result), sort_keys=True))
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
