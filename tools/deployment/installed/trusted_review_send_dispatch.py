"""管理者設置の既存送信入口へClaude疎通を固定接続する振り分け処理。"""

import hashlib
import importlib
import json
from pathlib import Path
import re
import sys


CLAUDE_CAPABILITY = {
    "model": "claude-fable-5",
    "purpose": "codex-pilot-no-tool-claude-bootstrap",
    "topology": "same_session_two_payload",
}
PINNED_WORKSPACE_FILES = {
    "tools/development/claude_bootstrap.py": (
        "14f352afb54353ccac45d84db2ce2a02c7c8a97204c0712651a5bd6218bc4133"
    ),
    "tools/common/__init__.py": (
        "fdb99f627d54b0661d5b3d3f487c2a3e0266df9ac97ea642529c39e6b17774cd"
    ),
    "tools/common/digests.py": (
        "fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7"
    ),
    "tools/common/errors.py": (
        "1d2fefcc075080138f3ab9a8b19775e0ff0fb333e811d6918a06c6730236c4c0"
    ),
}
_HEX_64 = re.compile(r"[0-9a-f]{64}")
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def with_claude_capability(base):
    value = json.loads(json.dumps(base))
    if (
        not isinstance(value, dict)
        or value.get("status") != "capabilities"
        or value.get("schema_version") != "trusted-review-send-v1"
        or not isinstance(value.get("roles"), dict)
    ):
        raise ValueError("base trusted capabilities invalid")
    if "claude_session_bootstrap" in value["roles"]:
        raise ValueError("base trusted Claude capability conflicts")
    value["roles"]["claude_session_bootstrap"] = dict(CLAUDE_CAPABILITY)
    return value


def _validate_workspace(workspace_root):
    root = Path(workspace_root)
    if not root.is_absolute() or root.is_symlink() or not root.is_dir():
        raise ValueError("trusted workspace invalid")
    root = root.resolve()
    manifest = root / ".reviewcompass/project-manifest.json"
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError("trusted workspace invalid")
    try:
        project = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError("trusted workspace invalid") from error
    if not isinstance(project, dict) or project.get("project_id") != "reviewcompass3":
        raise ValueError("trusted workspace invalid")
    for relative, expected_digest in PINNED_WORKSPACE_FILES.items():
        path = root / relative
        if (
            path.is_symlink()
            or not path.is_file()
            or _sha256(path) != expected_digest
        ):
            raise ValueError("trusted workspace source mismatch")
    return root


def _load_bootstrap(workspace_root):
    root = _validate_workspace(workspace_root)
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    module = importlib.import_module("tools.development.claude_bootstrap")
    expected = root / "tools/development/claude_bootstrap.py"
    if Path(module.__file__).resolve() != expected:
        raise ValueError("trusted workspace import mismatch")
    return module


def _blocked():
    print(
        json.dumps(
            {
                "schema_version": 1,
                "result": "stopped",
                "stop_code": "trusted_transport_unavailable",
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 2


def main(argv, *, base_main, base_capabilities):
    arguments = list(argv)
    if arguments == ["--capabilities"]:
        try:
            value = with_claude_capability(base_capabilities())
        except (TypeError, ValueError, json.JSONDecodeError):
            return _blocked()
        print(json.dumps(value, separators=(",", ":"), sort_keys=True))
        return 0
    if not arguments or arguments[0] != "claude-bootstrap":
        return base_main(arguments)
    if (
        len(arguments) != 7
        or arguments[1] != "--workspace-root"
        or arguments[3] != "--manifest-digest"
        or arguments[5] != "--approval-id"
        or _HEX_64.fullmatch(arguments[4]) is None
        or _IDENTIFIER.fullmatch(arguments[6]) is None
    ):
        return _blocked()
    try:
        bootstrap = _load_bootstrap(arguments[2])
        result = bootstrap.run_approved_no_tool_bootstrap(
            arguments[4],
            arguments[6],
        )
    except (ImportError, OSError, TypeError, ValueError):
        return _blocked()
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    if result.get("result") == "succeeded":
        return 0
    if result.get("result") == "stopped":
        return 2
    return 1
