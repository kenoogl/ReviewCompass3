"""管理者設置の既存送信入口へClaude疎通を固定接続する振り分け処理。"""

import json
import os
from pathlib import Path
import re

from tools.development import claude_bootstrap


CLAUDE_CAPABILITY = {
    "model": "claude-fable-5",
    "purpose": "codex-pilot-no-tool-claude-bootstrap",
    "topology": "same_session_two_payload",
}
CLAUDE_IMPLEMENTATION_CAPABILITY = {
    "model": "from-approved-launch",
    "purpose": "claude_implementation_executor",
    "topology": "same_session_test_then_implementation",
}
_HEX_64 = re.compile(r"[0-9a-f]{64}")
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def with_claude_capability(base):
    value = json.loads(json.dumps(base))
    if (
        not isinstance(value, dict)
        or value.get("status") != "capabilities"
        or value.get("schema_version") != "trusted-review-send-v1"
        or not isinstance(value.get("roles"), dict)
    ):
        raise ValueError("base trusted capabilities invalid")
    if (
        "claude_session_bootstrap" in value["roles"]
        or "claude_implementation_executor" in value["roles"]
    ):
        raise ValueError("base trusted Claude capability conflicts")
    value["roles"]["claude_session_bootstrap"] = dict(CLAUDE_CAPABILITY)
    value["roles"]["claude_implementation_executor"] = dict(
        CLAUDE_IMPLEMENTATION_CAPABILITY
    )
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
    return root


def _load_bootstrap(workspace_root):
    root = _validate_workspace(workspace_root)
    os.chdir(root)
    return claude_bootstrap


def _load_implementation(workspace_root):
    root = _validate_workspace(workspace_root)
    os.chdir(root)
    from tools.development import claude_implementation_route

    return claude_implementation_route


def _load_executor(workspace_root):
    root = _validate_workspace(workspace_root)
    os.chdir(root)
    from tools.development import claude_implementation_executor

    return claude_implementation_executor


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
    if arguments and arguments[0] == "claude-implementation-execute":
        if (
            len(arguments) != 17
            or arguments[1] != "--workspace-root"
            or arguments[3] != "--repository"
            or arguments[5] != "--private-root"
            or arguments[7] != "--run-id"
            or arguments[9] != "--turn"
            or arguments[11] != "--approval-id"
            or arguments[13] != "--manifest-path"
            or arguments[15] != "--manifest-sha256"
            or any(
                not Path(arguments[index]).is_absolute()
                for index in (2, 4, 6, 14)
            )
            or _IDENTIFIER.fullmatch(arguments[8]) is None
            or arguments[10] not in ("test", "implementation")
            or _IDENTIFIER.fullmatch(arguments[12]) is None
            or _HEX_64.fullmatch(arguments[16]) is None
        ):
            return _blocked()
        try:
            executor = _load_executor(arguments[2])
            result = executor.execute_turn(
                Path(arguments[4]),
                Path(arguments[6]),
                arguments[8],
                arguments[10],
                arguments[12],
                Path(arguments[14]),
                arguments[16],
            )
        except Exception:
            return _blocked()
        print(
            json.dumps(
                result,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
        )
        return 0
    if arguments and arguments[0] == "claude-implementation-record":
        if (
            len(arguments) != 15
            or arguments[1] != "--workspace-root"
            or arguments[3] != "--repository"
            or arguments[5] != "--private-root"
            or arguments[7] != "--run-id"
            or arguments[9] != "--turn"
            or arguments[11] != "--launch-record"
            or arguments[13] != "--raw-file"
            or any(
                not Path(arguments[index]).is_absolute()
                for index in (2, 4, 6, 12, 14)
            )
            or _IDENTIFIER.fullmatch(arguments[8]) is None
            or arguments[10] not in ("test", "implementation")
        ):
            return _blocked()
        try:
            implementation = _load_implementation(arguments[2])
            result = implementation.record_turn(
                Path(arguments[4]),
                Path(arguments[6]),
                arguments[8],
                arguments[10],
                Path(arguments[12]),
                Path(arguments[14]),
            )
        except Exception:
            return _blocked()
        print(
            json.dumps(
                result,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
        )
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
