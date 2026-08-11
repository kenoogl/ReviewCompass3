"""承認済みの固定二payloadだけをClaude Codeへ渡す閉じた入口。"""

import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import uuid

from tools.common import digests


REQUIRED_COMPLETION_REVIEW_STATUS = "verified"
REQUIRED_SEND_APPROVAL_RECORD_KIND = "human_claude_bootstrap_send_approval"
RED_START_APPROVAL_IS_NOT_SEND_APPROVAL = True

_COMPLETION_REVIEW_RELATIVE_PATH = (
    "records/development/claude-bootstrap-completion-review-v1.json"
)

_ORIGINAL_RUN = subprocess.run
_PURPOSE = "codex-pilot-no-tool-claude-bootstrap"
_PROVIDER = "claude-code-first-party"
_MODEL = "fable"
_VERSION = "2.1.220"
_EXECUTABLE_SHA256 = (
    "8addc857f3fe64d5a0368af9ee50321b50afb4a6918ba3ef018ab84f5dbbe081"
)
_ORDERED_PAYLOAD_SHA256 = (
    "26933d4f45ed497f9d1d9f5fdc741aca87b0ad37c3ed3c35fd99ebff6b2bd8a0"
)
_PAYLOADS = (
    {
        "ordinal": 1,
        "utf8_bytes": 296,
        "sha256": (
            "18059aa0f32b93bae5b117092a45fbf4e985381546b8c64507168f0226f4ad64"
        ),
        "text": (
            "あなたはClaude Reviewerです。Codex Pilotからの疎通確認です。ツールを使わず、"
            "他のエージェントを起動せず、次のJSONだけを返してください。"
            '{"protocol":"codex-pilot-claude-bootstrap-v1","role":"reviewer",'
            '"nonce":"RC3-CPC-20260811-A","reinvoke":false}'
        ),
    },
    {
        "ordinal": 2,
        "utf8_bytes": 221,
        "sha256": (
            "c2309f2624ba0d0f36fd00894dcbc67ccd66e83429960c4083f4e10b2f18982a"
        ),
        "text": (
            "同じセッションの継続確認です。前回のnonceを使い、次のJSONだけを返してください。"
            '{"protocol":"codex-pilot-claude-bootstrap-v1","continued":true,'
            '"nonce":"<前回のnonce>","reinvoke":false}'
        ),
    },
)
_MATERIAL_POLICY = {
    "require_secret_scan": True,
    "forbid_credentials": True,
    "forbid_personal_identifiers": True,
}
_ALLOWED_CHILD_ENVIRONMENT = (
    "HOME",
    "PATH",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "NO_COLOR",
)
_SUCCESS_REQUIRED = {
    "type",
    "subtype",
    "duration_ms",
    "duration_api_ms",
    "is_error",
    "num_turns",
    "result",
    "stop_reason",
    "total_cost_usd",
    "usage",
    "modelUsage",
    "permission_denials",
    "uuid",
    "session_id",
}
_SUCCESS_OPTIONAL = {
    "ttft_ms",
    "ttft_stream_ms",
    "time_to_request_ms",
    "user_message_uuid",
    "request_sent_wall_ms",
    "time_to_request_from_spawn_ms",
    "warm_spare_claimed",
    "time_origin_ms",
    "api_error_status",
    "structured_output",
    "deferred_tool_use",
    "terminal_reason",
    "fast_mode_state",
    "fast_mode_disabled_reason",
    "origin",
}
_EXECUTABLE_DIGEST_CACHE = {}
_HEX_64 = re.compile(r"[0-9a-f]{64}")
_HEX_40 = re.compile(r"[0-9a-f]{40}")
_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE = re.compile(r"(?:\+?\d[\d -]{7,}\d)")
_SECRET = re.compile(
    r"(?:sk-[A-Za-z0-9_-]+|gh[pousr]_[A-Za-z0-9]+|"
    r"(?:api[_-]?key|auth[_-]?token|password|secret)\s*[:=])",
    re.IGNORECASE,
)


class _BootstrapStop(Exception):
    def __init__(
        self,
        code,
        *,
        approval_state="pending",
        payload_process_count=0,
        preflight_process_count=0,
        recovery="新しいHuman承認を確認してから再開してください。",
    ):
        super().__init__(code)
        self.code = code
        self.approval_state = approval_state
        self.payload_process_count = payload_process_count
        self.preflight_process_count = preflight_process_count
        self.recovery = recovery


def _canonical_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _read_json(path, code):
    if path.is_symlink() or not path.is_file():
        raise _BootstrapStop(code)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise _BootstrapStop(code) from error


def _inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _git_blob(repository, relative_path):
    tree = _ORIGINAL_RUN(
        ["git", "ls-tree", "-z", "HEAD", "--", relative_path],
        cwd=repository,
        check=False,
        capture_output=True,
    )
    if tree.returncode != 0 or not tree.stdout:
        raise _BootstrapStop("manifest_not_committed")
    try:
        metadata, found = tree.stdout[:-1].split(b"\t", 1)
        mode, kind, _ = metadata.split(b" ", 2)
    except ValueError as error:
        raise _BootstrapStop("manifest_not_committed") from error
    if (
        mode not in (b"100644", b"100755")
        or kind != b"blob"
        or found.decode("utf-8") != relative_path
    ):
        raise _BootstrapStop("manifest_not_committed")
    shown = _ORIGINAL_RUN(
        ["git", "show", f"HEAD:{relative_path}"],
        cwd=repository,
        check=False,
        capture_output=True,
    )
    if shown.returncode != 0:
        raise _BootstrapStop("manifest_not_committed")
    return shown.stdout


def _project_id(repository):
    manifest = _read_json(
        repository / ".reviewcompass/project-manifest.json",
        "project_manifest_invalid",
    )
    value = manifest.get("project_id") if isinstance(manifest, dict) else None
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise _BootstrapStop("project_manifest_invalid")
    return value


def _runtime_paths(project_id, approval_id):
    root = Path.home() / ".reviewcompass3" / "projects" / project_id / "development"
    return {
        "store": root / "state/claude-bootstrap/approval-store",
        "work": root / "data/claude-bootstrap/work",
        "result": root / "sensitive/claude-bootstrap/runs" / approval_id,
    }


def _safe_directory(path, repository, *, empty=False):
    if path.is_symlink() or not path.is_dir():
        return False
    resolved = path.resolve()
    repository = repository.resolve()
    if (
        _inside(resolved, repository)
        or resolved == repository.parent
        or _inside(repository, resolved)
    ):
        return False
    if stat.S_IMODE(path.stat().st_mode) & 0o077:
        return False
    return not empty or not any(path.iterdir())


def _validate_manifest(manifest):
    if not isinstance(manifest, dict):
        raise _BootstrapStop("manifest_contract_mismatch")
    payloads = manifest.get("payloads")
    if not isinstance(payloads, list):
        raise _BootstrapStop("manifest_contract_mismatch")
    texts = [
        item.get("text", "")
        for item in payloads
        if isinstance(item, dict)
    ]
    outbound = "\n".join(texts)
    if _SECRET.search(outbound) or _EMAIL.search(outbound) or _PHONE.search(outbound):
        raise _BootstrapStop("unsafe_payload")
    expected = {
        "schema_version": 1,
        "record_kind": "approved_no_tool_claude_bootstrap_manifest",
        "purpose": _PURPOSE,
        "provider": _PROVIDER,
        "model": _MODEL,
        "claude_code_version": _VERSION,
        "claude_executable_sha256": _EXECUTABLE_SHA256,
        "payloads": list(_PAYLOADS),
        "ordered_payload_sha256": _ORDERED_PAYLOAD_SHA256,
        "material_policy": _MATERIAL_POLICY,
    }
    if manifest != expected:
        raise _BootstrapStop("manifest_contract_mismatch")
    ordered = [
        {"ordinal": item["ordinal"], "sha256": item["sha256"]}
        for item in payloads
    ]
    if digests.sha256_hex(_canonical_bytes(ordered)) != _ORDERED_PAYLOAD_SHA256:
        raise _BootstrapStop("manifest_contract_mismatch")


def _validate_decision(decision, manifest_digest, result_root, repository, path):
    relative = str(path.relative_to(repository))
    if _git_blob(repository, relative) != path.read_bytes():
        raise _BootstrapStop("approval_mismatch")
    required = {
        "schema_version": 1,
        "record_kind": REQUIRED_SEND_APPROVAL_RECORD_KIND,
        "approved_by": "user",
        "approval_id": decision.get("approval_id"),
        "store_identity": decision.get("store_identity"),
        "purpose": _PURPOSE,
        "provider": _PROVIDER,
        "model": _MODEL,
        "manifest_sha256": manifest_digest,
        "ordered_payload_sha256": _ORDERED_PAYLOAD_SHA256,
        "claude_executable_sha256": _EXECUTABLE_SHA256,
        "expires_at": decision.get("expires_at"),
        "material_policy": _MATERIAL_POLICY,
        "result_root_identity": digests.sha256_hex(
            str(result_root).encode("utf-8")
        ),
        "completion_review_id": decision.get("completion_review_id"),
        "completion_review_path": _COMPLETION_REVIEW_RELATIVE_PATH,
        "completion_review_sha256": decision.get("completion_review_sha256"),
        "completion_review_target_commit": decision.get(
            "completion_review_target_commit"
        ),
    }
    if decision != required or decision.get("approved_by") != "user":
        raise _BootstrapStop("approval_mismatch")
    try:
        expires = datetime.datetime.fromisoformat(
            decision["expires_at"].replace("Z", "+00:00")
        )
    except (AttributeError, ValueError) as error:
        raise _BootstrapStop("approval_mismatch") from error
    if expires <= datetime.datetime.now(datetime.timezone.utc):
        raise _BootstrapStop("approval_expired")
    _validate_completion_review(decision, manifest_digest, repository, path)


def _git_review_command(repository, *arguments):
    completed = _ORIGINAL_RUN(
        ["git", *arguments],
        cwd=repository,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        raise _BootstrapStop("completion_review_invalid")
    return completed.stdout


def _validate_completion_review(decision, manifest_digest, repository, decision_path):
    review_id = decision.get("completion_review_id")
    review_digest = decision.get("completion_review_sha256")
    target_commit = decision.get("completion_review_target_commit")
    if (
        not isinstance(review_id, str)
        or _IDENTIFIER.fullmatch(review_id) is None
        or not isinstance(review_digest, str)
        or _HEX_64.fullmatch(review_digest) is None
        or not isinstance(target_commit, str)
        or _HEX_40.fullmatch(target_commit) is None
    ):
        raise _BootstrapStop("completion_review_invalid")
    review_path = repository / _COMPLETION_REVIEW_RELATIVE_PATH
    if review_path.is_symlink() or not review_path.is_file():
        raise _BootstrapStop("completion_review_invalid")
    try:
        review_bytes = review_path.read_bytes()
        review = json.loads(review_bytes.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise _BootstrapStop("completion_review_invalid") from error
    if (
        _git_blob(repository, _COMPLETION_REVIEW_RELATIVE_PATH) != review_bytes
        or digests.sha256_hex(review_bytes) != review_digest
    ):
        raise _BootstrapStop("completion_review_invalid")
    expected = {
        "schema_version": 1,
        "record_kind": "claude_bootstrap_completion_review",
        "review_id": review_id,
        "status": REQUIRED_COMPLETION_REVIEW_STATUS,
        "target_commit": target_commit,
        "manifest_sha256": manifest_digest,
        "ordered_payload_sha256": _ORDERED_PAYLOAD_SHA256,
        "blocking_finding_count": 0,
    }
    if review != expected:
        raise _BootstrapStop("completion_review_invalid")
    _git_review_command(
        repository,
        "merge-base",
        "--is-ancestor",
        target_commit,
        "HEAD",
    )
    manifest_relative = "records/development/claude-bootstrap-send-manifest-v1.json"
    reviewed_manifest = _git_review_command(
        repository,
        "show",
        f"{target_commit}:{manifest_relative}",
    )
    if reviewed_manifest != _git_blob(repository, manifest_relative):
        raise _BootstrapStop("completion_review_invalid")
    changed = _git_review_command(
        repository,
        "diff",
        "--name-only",
        "-z",
        target_commit,
        "HEAD",
    )
    try:
        changed_paths = {
            item.decode("utf-8")
            for item in changed.split(b"\0")
            if item
        }
    except UnicodeDecodeError as error:
        raise _BootstrapStop("completion_review_invalid") from error
    if changed_paths != {
        _COMPLETION_REVIEW_RELATIVE_PATH,
        str(decision_path.relative_to(repository)),
    }:
        raise _BootstrapStop("completion_review_invalid")


def _validate_store(store, approval_id, decision, decision_path, manifest_digest):
    if not _safe_directory(store, Path.cwd().resolve()):
        raise _BootstrapStop("approval_store_missing")
    allowed = {"store.json", "pending", "claimed", "consumed"}
    if {entry.name for entry in store.iterdir()} != allowed:
        raise _BootstrapStop("approval_store_invalid")
    store_record = _read_json(store / "store.json", "approval_store_missing")
    if stat.S_IMODE((store / "store.json").stat().st_mode) != 0o600:
        raise _BootstrapStop("approval_store_invalid")
    if store_record != {
        "schema_version": 1,
        "store_identity": decision["store_identity"],
    }:
        raise _BootstrapStop("approval_store_invalid")
    states = []
    for state in ("pending", "claimed", "consumed"):
        directory = store / state
        if not _safe_directory(directory, Path.cwd().resolve()):
            raise _BootstrapStop("approval_store_invalid")
        entries = list(directory.iterdir())
        for entry in entries:
            if entry.is_symlink() or entry.name != f"{approval_id}.json":
                raise _BootstrapStop("approval_store_invalid")
            states.append((state, entry))
    if len(states) != 1 or states[0][0] != "pending":
        raise _BootstrapStop("approval_store_missing")
    token_path = states[0][1]
    if stat.S_IMODE(token_path.stat().st_mode) != 0o600:
        raise _BootstrapStop("approval_store_invalid")
    token = _read_json(token_path, "approval_store_missing")
    expected = {
        "schema_version": 1,
        "approval_id": approval_id,
        "decision_sha256": digests.sha256_hex(decision_path.read_bytes()),
        "store_identity": decision["store_identity"],
        "manifest_sha256": manifest_digest,
        "ordered_payload_sha256": _ORDERED_PAYLOAD_SHA256,
        "provider": _PROVIDER,
        "model": _MODEL,
        "purpose": _PURPOSE,
        "claude_executable_sha256": _EXECUTABLE_SHA256,
        "expires_at": decision["expires_at"],
    }
    if token != expected:
        raise _BootstrapStop("approval_mismatch")
    return token_path


def _executable_digest(path):
    metadata = path.stat()
    key = (str(path), metadata.st_size, metadata.st_mtime_ns)
    if key not in _EXECUTABLE_DIGEST_CACHE:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        _EXECUTABLE_DIGEST_CACHE.clear()
        _EXECUTABLE_DIGEST_CACHE[key] = digest.hexdigest()
    return _EXECUTABLE_DIGEST_CACHE[key]


def _resolve_executable(repository):
    located = shutil.which("claude")
    if not located:
        raise _BootstrapStop("claude_binary_mismatch")
    locator = Path(located)
    resolved = locator.resolve()
    if (
        not resolved.is_file()
        or resolved.is_symlink()
        or _inside(resolved, repository)
        or _executable_digest(resolved) != _EXECUTABLE_SHA256
    ):
        raise _BootstrapStop("claude_binary_mismatch")
    return str(locator)


def _child_environment():
    return {
        name: os.environ[name]
        for name in _ALLOWED_CHILD_ENVIRONMENT
        if name in os.environ
    }


def _invoke(argv, *, cwd, environment, payload_count, preflight_count):
    try:
        return subprocess.run(
            argv,
            cwd=str(cwd),
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        )
    except PermissionError as error:
        raise _BootstrapStop(
            "host_safety_rejected",
            payload_process_count=payload_count,
            preflight_process_count=preflight_count + 1,
            recovery="hostの安全規則を確認し、別経路へ迂回せず停止してください。",
        ) from error


def _validate_outer(value, session_id):
    if not isinstance(value, dict):
        return False
    if set(value) - (_SUCCESS_REQUIRED | _SUCCESS_OPTIONAL):
        return False
    if not _SUCCESS_REQUIRED <= set(value):
        return False
    if (
        value["type"] != "result"
        or value["subtype"] != "success"
        or value["is_error"] is not False
        or type(value["duration_ms"]) is not int
        or type(value["duration_api_ms"]) is not int
        or value["num_turns"] != 1
        or not isinstance(value["result"], str)
        or value["stop_reason"] is not None
        and not isinstance(value["stop_reason"], str)
        or isinstance(value["total_cost_usd"], bool)
        or not isinstance(value["total_cost_usd"], (int, float))
        or not isinstance(value["modelUsage"], dict)
        or value["permission_denials"] != []
        or not isinstance(value["uuid"], str)
        or value["session_id"] != session_id
    ):
        return False
    return True


def _validate_result(completed, session_id, expected_inner):
    if completed.returncode != 0 or completed.stderr:
        return None
    try:
        outer = json.loads(completed.stdout)
    except (TypeError, json.JSONDecodeError):
        return None
    if not _validate_outer(outer, session_id):
        return None
    try:
        inner = json.loads(outer["result"])
    except json.JSONDecodeError:
        return None
    if inner != expected_inner:
        return None
    return outer


def _reserve_result_files(result_root, repository):
    if not _safe_directory(result_root, repository, empty=True):
        raise _BootstrapStop("storage_unavailable")
    paths = {
        name: result_root / filename
        for name, filename in {
            "launch": "launch.json",
            "raw_1": "raw-1.json",
            "raw_2": "raw-2.json",
            "receipt": "receipt.json",
        }.items()
    }
    opened = []
    try:
        for path in paths.values():
            descriptor = os.open(
                path,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                0o600,
            )
            os.close(descriptor)
            opened.append(path)
    except OSError as error:
        raise _BootstrapStop("storage_unavailable") from error
    return paths


def _write_json(path, value):
    path.write_bytes(_canonical_bytes(value))
    path.chmod(0o600)
    if json.loads(path.read_text(encoding="utf-8")) != value:
        raise _BootstrapStop("storage_unavailable", approval_state="claimed")


def _stop_result(error):
    return {
        "schema_version": 1,
        "result": "stopped",
        "stop_code": error.code,
        "payload_process_count": error.payload_process_count,
        "preflight_process_count": error.preflight_process_count,
        "approval_state": error.approval_state,
        "recovery": error.recovery,
    }


def _consume(claimed, consumed):
    try:
        os.replace(claimed, consumed)
    except OSError as error:
        raise _BootstrapStop(
            "approval_state_write_failed",
            approval_state="claimed",
            recovery="承認を再利用せず、Humanへ状態確認を依頼してください。",
        ) from error


def run_approved_no_tool_bootstrap(manifest_digest, approval_id):
    """固定目録Digestと承認IDだけから一回限りの処理を行う。"""
    payload_count = 0
    preflight_count = 0
    approval_state = "pending"
    claimed = None
    consumed = None
    paths = None
    raw_digests = []
    exit_codes = []
    session_id = None
    try:
        if (
            not isinstance(manifest_digest, str)
            or _HEX_64.fullmatch(manifest_digest) is None
            or not isinstance(approval_id, str)
            or _IDENTIFIER.fullmatch(approval_id) is None
        ):
            raise _BootstrapStop("input_invalid")
        repository = Path.cwd().resolve()
        project_id = _project_id(repository)
        runtime = _runtime_paths(project_id, approval_id)
        manifest_path = (
            repository
            / "records/development/claude-bootstrap-send-manifest-v1.json"
        )
        if manifest_path.is_symlink() or not manifest_path.is_file():
            raise _BootstrapStop("manifest_missing")
        manifest_bytes = manifest_path.read_bytes()
        if (
            digests.sha256_hex(manifest_bytes) != manifest_digest
            or _git_blob(repository, str(manifest_path.relative_to(repository)))
            != manifest_bytes
        ):
            raise _BootstrapStop("manifest_digest_mismatch")
        try:
            manifest = json.loads(manifest_bytes.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as error:
            raise _BootstrapStop("manifest_contract_mismatch") from error
        _validate_manifest(manifest)
        decision_path = (
            repository
            / "records/development/claude-bootstrap-human-decision-v1.json"
        )
        decision = _read_json(decision_path, "approval_mismatch")
        if decision.get("approval_id") != approval_id:
            raise _BootstrapStop("approval_mismatch")
        _validate_decision(
            decision,
            manifest_digest,
            runtime["result"],
            repository,
            decision_path,
        )
        token = _validate_store(
            runtime["store"],
            approval_id,
            decision,
            decision_path,
            manifest_digest,
        )
        if not _safe_directory(runtime["work"], repository, empty=True):
            raise _BootstrapStop("work_directory_invalid")

        executable = _resolve_executable(repository)
        environment = _child_environment()
        version = _invoke(
            [executable, "--version"],
            cwd=runtime["work"],
            environment=environment,
            payload_count=payload_count,
            preflight_count=preflight_count,
        )
        preflight_count += 1
        if version.returncode != 0 or not version.stdout.startswith(_VERSION):
            raise _BootstrapStop(
                "claude_version_mismatch",
                preflight_process_count=preflight_count,
            )
        auth = _invoke(
            [executable, "auth", "status", "--json"],
            cwd=runtime["work"],
            environment=environment,
            payload_count=payload_count,
            preflight_count=preflight_count,
        )
        preflight_count += 1
        try:
            auth_value = json.loads(auth.stdout)
        except (TypeError, json.JSONDecodeError) as error:
            raise _BootstrapStop(
                "authentication_not_approved",
                preflight_process_count=preflight_count,
            ) from error
        if auth.returncode != 0 or auth_value != {
            "loggedIn": True,
            "authMethod": "claude.ai",
            "apiProvider": "firstParty",
        }:
            raise _BootstrapStop(
                "authentication_not_approved",
                preflight_process_count=preflight_count,
            )

        claimed = runtime["store"] / "claimed" / token.name
        consumed = runtime["store"] / "consumed" / token.name
        try:
            os.replace(token, claimed)
        except FileNotFoundError as error:
            raise _BootstrapStop(
                "approval_store_missing",
                preflight_process_count=preflight_count,
            ) from error
        approval_state = "claimed"
        paths = _reserve_result_files(runtime["result"], repository)
        session_id = str(uuid.uuid4())
        base = [
            executable,
            "--print",
            "--safe-mode",
            "--tools",
            "",
            "--disallowedTools",
            "*",
            "--strict-mcp-config",
            "--mcp-config",
            '{"mcpServers":{}}',
            "--disable-slash-commands",
            "--no-chrome",
            "--output-format",
            "json",
            "--model",
            _MODEL,
        ]
        first_argv = [
            *base,
            "--session-id",
            session_id,
            _PAYLOADS[0]["text"],
        ]
        second_argv = [
            *base,
            "--resume",
            session_id,
            _PAYLOADS[1]["text"],
        ]
        _write_json(
            paths["launch"],
            {
                "schema_version": 1,
                "provider": _PROVIDER,
                "model": _MODEL,
                "payload_sha256": [item["sha256"] for item in _PAYLOADS],
                "argv": [first_argv, second_argv],
            },
        )
        expected_inner = (
            {
                "protocol": "codex-pilot-claude-bootstrap-v1",
                "role": "reviewer",
                "nonce": "RC3-CPC-20260811-A",
                "reinvoke": False,
            },
            {
                "protocol": "codex-pilot-claude-bootstrap-v1",
                "continued": True,
                "nonce": "RC3-CPC-20260811-A",
                "reinvoke": False,
            },
        )
        outer_values = []
        for index, argv in enumerate((first_argv, second_argv), start=1):
            completed = _invoke(
                argv,
                cwd=runtime["work"],
                environment=environment,
                payload_count=payload_count,
                preflight_count=preflight_count,
            )
            payload_count += 1
            exit_codes.append(completed.returncode)
            outer = _validate_result(
                completed,
                session_id,
                expected_inner[index - 1],
            )
            if outer is None:
                raise _BootstrapStop(
                    "claude_result_invalid",
                    approval_state="claimed",
                    payload_process_count=payload_count,
                    preflight_process_count=preflight_count,
                )
            outer_values.append(outer)
            raw_bytes = _canonical_bytes(outer)
            raw_digests.append(digests.sha256_hex(raw_bytes))
            paths[f"raw_{index}"].write_bytes(raw_bytes)
            paths[f"raw_{index}"].chmod(0o600)

        _consume(claimed, consumed)
        approval_state = "consumed"
        receipt = {
            "schema_version": 1,
            "result": "succeeded",
            "approval_id": approval_id,
            "approval_state": approval_state,
            "provider": _PROVIDER,
            "model": _MODEL,
            "auth_method": "claude.ai",
            "payload_sha256": [item["sha256"] for item in _PAYLOADS],
            "raw_sha256": raw_digests,
            "session_id": [session_id],
            "exit_code": exit_codes,
            "payload_process_count": payload_count,
            "preflight_process_count": preflight_count,
            "storage_result": "saved",
            "completed_at": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(),
            "local_owner_rollback_detection": "not_guaranteed",
        }
        _write_json(paths["receipt"], receipt)
        return {
            "schema_version": 1,
            "result": "succeeded",
            "payload_process_count": payload_count,
            "preflight_process_count": preflight_count,
            "approval_state": approval_state,
            "receipt_path": str(paths["receipt"]),
        }
    except _BootstrapStop as error:
        if error.payload_process_count == 0:
            error.payload_process_count = payload_count
        if error.preflight_process_count == 0:
            error.preflight_process_count = preflight_count
        if approval_state == "claimed" and claimed is not None and consumed is not None:
            try:
                _consume(claimed, consumed)
                approval_state = "consumed"
            except _BootstrapStop:
                approval_state = "claimed"
        error.approval_state = approval_state
        if paths is not None:
            receipt = {
                "schema_version": 1,
                "result": "stopped",
                "stop_code": error.code,
                "approval_state": approval_state,
                "payload_process_count": error.payload_process_count,
                "preflight_process_count": error.preflight_process_count,
                "payload_sha256": [item["sha256"] for item in _PAYLOADS],
                "raw_sha256": raw_digests,
                "exit_code": exit_codes,
            }
            try:
                _write_json(paths["receipt"], receipt)
            except _BootstrapStop:
                pass
        return _stop_result(error)
