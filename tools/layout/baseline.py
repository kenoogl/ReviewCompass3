"""Work 1A用のLayout Baseline読込・配置境界検証。"""

import dataclasses
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


class LayoutError(Exception):
    """固定Layoutを安全に解決または検証できない。"""


LOGICAL_ROOTS = {
    "code_root",
    "config_root",
    "project_root",
    "data_root",
    "state_root",
    "log_root",
    "cache_root",
    "sensitive_root",
    "evaluation_root",
}
EXTERNAL_ROOTS = LOGICAL_ROOTS - {"project_root"}
WRITABLE_RUNTIME_ROOTS = {
    "data_root",
    "state_root",
    "log_root",
    "cache_root",
    "sensitive_root",
    "evaluation_root",
}
ARTIFACT_ROOTS_V1 = {
    "contracts",
    "design_decisions",
    "policies",
    "requirement_maps",
    "reuse",
    "verified_artifacts",
}
ARTIFACT_ROOTS_BY_VERSION = {
    1: ARTIFACT_ROOTS_V1,
    2: ARTIFACT_ROOTS_V1 | {"workflow"},
}
BINDING_FIELDS = {
    "binding_id",
    "captured_at",
    "checkout_id",
    "project_id",
    "project_manifest_digest",
    "repository_root",
    "schema_version",
    "validation",
}
ENVIRONMENT_ROLES = {"stable", "development"}
ENVIRONMENT_VARIABLES = {
    name: f"REVIEWCOMPASS3_{name.upper()}"
    for name in EXTERNAL_ROOTS
}
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_WINDOWS_ABSOLUTE = re.compile(r"^[A-Za-z]:[\\/]")
_TEXT_ABSOLUTE = re.compile(
    r"(?<![A-Za-z0-9._-])(?:/[A-Za-z0-9._-]+){2,}"
)


@dataclasses.dataclass(frozen=True)
class LayoutResolution:
    environment_role: str
    roots: dict


@dataclasses.dataclass(frozen=True)
class ProjectBinding:
    binding_id: str
    project_id: str
    checkout_id: str
    repository_root: Path
    captured_at: str
    project_manifest_digest: str
    resolved_document_links: tuple

    def to_dict(self):
        return {
            "binding_id": self.binding_id,
            "captured_at": self.captured_at,
            "checkout_id": self.checkout_id,
            "project_id": self.project_id,
            "project_manifest_digest": self.project_manifest_digest,
            "repository_root": str(self.repository_root),
            "schema_version": 1,
            "validation": "passed",
        }


def _load_json(path, message):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LayoutError(message) from error


def _inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _overlaps(left, right):
    return _inside(left, right) or _inside(right, left)


def _safe_relative(value, *, field):
    if not isinstance(value, str):
        raise LayoutError(f"{field} must be a project-relative path")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or not pure.parts
        or any(part in ("", ".", "..") for part in pure.parts)
        or "\\" in value
    ):
        raise LayoutError(f"{field} must not escape project_root")
    return pure


def load_layout_baseline(record_path):
    path = Path(record_path)
    if not path.is_absolute() or not path.is_file():
        raise LayoutError("Layout Baseline Record must be an existing absolute path")
    record = _load_json(path, "Cannot load Layout Baseline Record")
    required = {
        "record_id",
        "schema_version",
        "layout_version",
        "status",
        "logical_roots",
        "resolution_precedence",
        "environment_variables",
        "git_boundary",
        "relative_path_policy",
        "project_manifest",
        "project_binding",
        "environment_isolation",
        "migration_policy",
        "verification",
    }
    if not isinstance(record, dict):
        raise LayoutError("Layout Baseline Record has unknown or missing keys")
    version = (record.get("schema_version"), record.get("layout_version"))
    if version == (1, 1):
        expected = required
    elif version == (2, 2):
        expected = required | {
            "deployment_package_policy",
            "project_artifact_policy",
        }
    else:
        raise LayoutError("Unsupported Layout Baseline version")
    if set(record) != expected:
        raise LayoutError("Layout Baseline Record has unknown or missing keys")
    if set(record["logical_roots"]) != LOGICAL_ROOTS:
        raise LayoutError("Layout Baseline logical roots are incomplete")
    if record["environment_variables"] != ENVIRONMENT_VARIABLES:
        raise LayoutError("Layout Baseline environment allowlist is invalid")
    if record["git_boundary"] != {
        "managed_root": "project_root",
        "external_roots": sorted(EXTERNAL_ROOTS),
    }:
        raise LayoutError("Layout Baseline Git boundary is invalid")
    if version == (2, 2):
        if record["project_artifact_policy"] != {
            "canonical_root_name": "workflow",
            "canonical_project_artifact_move": "prohibited",
            "record_relation_identity": [
                "id",
                "version",
                "digest",
                "relation_kind",
            ],
            "classification_change": "rebuild_projection",
            "semantic_data_migration": "exceptional_human_approved",
        }:
            raise LayoutError("Layout Baseline Project Artifact policy is invalid")
        if record["deployment_package_policy"] != {
            "source_selection": "manifest_allowlist",
            "deployment_package_replaceable": True,
            "runtime_projection_rebuildable": True,
            "project_artifact_update_requires_runtime_reinstall": False,
            "prohibited_project_paths": [
                ".reviewcompass/project-manifest.json",
                ".reviewcompass/workflow",
            ],
        }:
            raise LayoutError("Layout Baseline deployment package policy is invalid")
    return record


def _absolute_path(value, *, name):
    path = Path(value)
    if not path.is_absolute():
        raise LayoutError(f"{name} must be an absolute path")
    return path.resolve()


def resolve_layout(
    baseline,
    *,
    environment_role,
    project_root,
    defaults,
    environment=None,
    user_settings=None,
    overrides=None,
):
    if environment_role not in ENVIRONMENT_ROLES:
        raise LayoutError("Unknown environment role")
    project = _absolute_path(project_root, name="project_root")
    if not project.is_dir():
        raise LayoutError("project_root must be an existing directory")
    default_values = dict(defaults)
    environment_values = {} if environment is None else dict(environment)
    setting_values = {} if user_settings is None else dict(user_settings)
    override_values = {} if overrides is None else dict(overrides)
    for source in (default_values, setting_values, override_values):
        if set(source) - EXTERNAL_ROOTS:
            raise LayoutError("Unknown logical root setting")
    if set(default_values) != EXTERNAL_ROOTS:
        raise LayoutError("OS standard defaults must define every external root")

    roots = {"project_root": project}
    for name in sorted(EXTERNAL_ROOTS):
        environment_name = baseline["environment_variables"][name]
        value = override_values.get(name)
        if value is None:
            value = setting_values.get(name)
        if value is None:
            value = environment_values.get(environment_name)
        if value is None:
            value = default_values[name]
        roots[name] = _absolute_path(value, name=name)

    for name in EXTERNAL_ROOTS:
        if _overlaps(roots[name], project):
            raise LayoutError(f"{name} must be outside project_root")
    for left_name in EXTERNAL_ROOTS:
        for right_name in EXTERNAL_ROOTS:
            if left_name >= right_name:
                continue
            if _overlaps(roots[left_name], roots[right_name]):
                raise LayoutError("External logical roots must not overlap")
    return LayoutResolution(
        environment_role=environment_role,
        roots=roots,
    )


def validate_environment_isolation(stable, development):
    if {
        stable.environment_role,
        development.environment_role,
    } != ENVIRONMENT_ROLES:
        raise LayoutError("Both stable and development layouts are required")
    if stable.roots["project_root"] != development.roots["project_root"]:
        raise LayoutError("Stable and development must bind the same project")
    for stable_name in EXTERNAL_ROOTS:
        for development_name in EXTERNAL_ROOTS:
            if _overlaps(
                stable.roots[stable_name],
                development.roots[development_name],
            ):
                raise LayoutError("Stable and development roots overlap")


def validate_write_target(resolution, target):
    path = _absolute_path(target, name="write target")
    if resolution.environment_role == "development" and _inside(
        path,
        resolution.roots["project_root"],
    ):
        return path
    if any(
        _inside(path, resolution.roots[name])
        for name in WRITABLE_RUNTIME_ROOTS
    ):
        return path
    raise LayoutError("cross-environment or unmanaged write target")


def _load_project_manifest(project_root):
    path = project_root / ".reviewcompass" / "project-manifest.json"
    manifest = _load_json(path, "Cannot load Project Manifest")
    expected = {
        "artifact_roots",
        "document_links",
        "project_id",
        "schema_version",
    }
    if not isinstance(manifest, dict) or set(manifest) != expected:
        raise LayoutError("Project Manifest has unknown or missing keys")
    artifact_roots = ARTIFACT_ROOTS_BY_VERSION.get(manifest["schema_version"])
    if artifact_roots is None:
        raise LayoutError("Unsupported Project Manifest version")
    if _IDENTIFIER.fullmatch(manifest.get("project_id", "")) is None:
        raise LayoutError("Project Manifest project identity is invalid")
    if (
        not isinstance(manifest["artifact_roots"], dict)
        or set(manifest["artifact_roots"]) != artifact_roots
    ):
        raise LayoutError("Project Manifest artifact roots are incomplete")
    if not isinstance(manifest["document_links"], list):
        raise LayoutError("Project Manifest document links are invalid")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return manifest, digest


def snapshot_project_artifacts(project_root, artifact_root_name):
    root = _absolute_path(project_root, name="project_root")
    if not root.is_dir():
        raise LayoutError("project_root must be an existing directory")
    manifest, _digest = _load_project_manifest(root)
    if artifact_root_name not in manifest["artifact_roots"]:
        raise LayoutError("Project Manifest artifact root is unknown")
    artifact_root = _resolve_project_path(
        root,
        manifest["artifact_roots"][artifact_root_name],
        field=f"artifact_roots.{artifact_root_name}",
        must_be_file=False,
    )
    snapshot = {}
    for path in sorted(item for item in artifact_root.rglob("*") if item.is_file()):
        resolved = path.resolve()
        if path.is_symlink() or not _inside(resolved, artifact_root):
            raise LayoutError("Project Artifact must remain inside its root")
        relative = path.relative_to(root).as_posix()
        snapshot[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def validate_project_artifact_append_only(before, after):
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise LayoutError("Project Artifact snapshots must be mappings")
    changed = [
        path
        for path, digest in before.items()
        if after.get(path) != digest
    ]
    if changed:
        raise LayoutError(
            "Canonical Project Artifact was removed or rewritten: "
            + ", ".join(sorted(changed))
        )
    return True


def validate_deployment_package_layout(package_root, baseline):
    root = _absolute_path(package_root, name="deployment package root")
    if not root.is_dir():
        raise LayoutError("deployment package root must be an existing directory")
    policy = baseline.get("deployment_package_policy")
    if not isinstance(policy, dict):
        raise LayoutError("Deployment package policy is required")
    for value in policy.get("prohibited_project_paths", []):
        relative = _safe_relative(value, field="prohibited_project_paths")
        target = root.joinpath(*relative.parts)
        if target.exists() or target.is_symlink():
            raise LayoutError(
                "Deployment package contains a prohibited Project Artifact path"
            )
    return True


def _resolve_project_path(project_root, value, *, field, must_be_file):
    relative = _safe_relative(value, field=field)
    resolved = project_root.joinpath(*relative.parts).resolve()
    if not _inside(resolved, project_root):
        raise LayoutError(f"{field} must not escape project_root")
    exists = resolved.is_file() if must_be_file else resolved.is_dir()
    if not exists:
        raise LayoutError(f"{field} does not resolve")
    return resolved


def validate_project_layout(
    project_root,
    *,
    binding_id,
    checkout_id,
    captured_at,
):
    root = _absolute_path(project_root, name="project_root")
    if not root.is_dir():
        raise LayoutError("project_root must be an existing directory")
    for identity in (binding_id, checkout_id):
        if _IDENTIFIER.fullmatch(identity or "") is None:
            raise LayoutError("Project Binding identity is invalid")
    manifest, digest = _load_project_manifest(root)
    for name, value in manifest["artifact_roots"].items():
        _resolve_project_path(
            root,
            value,
            field=f"artifact_roots.{name}",
            must_be_file=False,
        )
    links = tuple(
        _resolve_project_path(
            root,
            value,
            field="document_links",
            must_be_file=True,
        )
        for value in manifest["document_links"]
    )
    return ProjectBinding(
        binding_id=binding_id,
        project_id=manifest["project_id"],
        checkout_id=checkout_id,
        repository_root=root,
        captured_at=captured_at,
        project_manifest_digest=digest,
        resolved_document_links=links,
    )


def validate_project_binding(project_root, binding):
    root = _absolute_path(project_root, name="project_root")
    manifest, digest = _load_project_manifest(root)
    if not isinstance(binding, dict) or set(binding) != BINDING_FIELDS:
        raise LayoutError("Project Binding has unknown or missing keys")
    repository_value = binding["repository_root"]
    if (
        not isinstance(repository_value, str)
        or not Path(repository_value).is_absolute()
    ):
        raise LayoutError("Project Binding repository root must be absolute")
    if binding.get("project_id") != manifest["project_id"]:
        raise LayoutError("Project Binding project identity mismatch")
    if binding.get("project_manifest_digest") != digest:
        raise LayoutError("Project Binding manifest identity mismatch")
    if Path(repository_value).resolve() != root:
        raise LayoutError("Project Binding repository root mismatch")
    return True


def _string_absolute(value):
    return (
        value.startswith("/")
        or _WINDOWS_ABSOLUTE.match(value) is not None
    )


def _json_absolute_values(value, prefix="$"):
    findings = []
    if isinstance(value, dict):
        for key, item in value.items():
            findings.extend(
                _json_absolute_values(item, f"{prefix}.{key}")
            )
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(
                _json_absolute_values(item, f"{prefix}[{index}]")
            )
    elif isinstance(value, str) and _string_absolute(value):
        findings.append(f"{prefix}={value}")
    return findings


def find_terminal_absolute_paths(managed_root):
    root = Path(managed_root).resolve()
    findings = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as error:
            raise LayoutError("Cannot inspect managed artifact") from error
        if path.suffix == ".json":
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as error:
                raise LayoutError("Cannot inspect managed JSON artifact") from error
            findings.extend(
                f"{relative}:{finding}"
                for finding in _json_absolute_values(payload)
            )
        else:
            findings.extend(
                f"{relative}:{match.group(0)}"
                for match in _TEXT_ABSOLUTE.finditer(text)
            )
    return tuple(findings)


def validate_layout_migration(baseline, migration):
    required = baseline["migration_policy"]["required_fields"]
    missing = [name for name in required if name not in migration]
    if missing:
        raise LayoutError(
            "Layout migration is missing " + ", ".join(missing)
        )
    if migration["from_version"] >= migration["to_version"]:
        raise LayoutError("Layout migration version must increase")
    if not set(migration["affected_roots"]).issubset(LOGICAL_ROOTS):
        raise LayoutError("Layout migration has unknown roots")
    if migration["link_check"] != "passed":
        raise LayoutError("Layout migration link check must pass")
    if migration["dry_run"] != "passed":
        raise LayoutError("Layout migration dry run must pass")
    if not migration["rollback"]:
        raise LayoutError("Layout migration rollback is required")
    return True
