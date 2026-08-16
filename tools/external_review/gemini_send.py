"""外部レビュアAPIへの一回送信の核（契約008 v5）。

送信指示一件を検査し、commit済みfile由来のpayloadを機械構成して、
選択providerへ一回だけHTTPS送信し、未加工応答を保存し、台帳を着地させる。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import datetime
import hashlib
import json
import os
import re
import stat
import urllib.error
import urllib.request

from tools.session_logs.redaction import default_pattern_rules
from tools.session_logs.redaction import find_high_entropy


_GENERAL_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_SHA256_VALUE = re.compile(r"[0-9a-f]{64}\Z")
_ORDER_SIZE_LIMIT = 262144
_PAYLOAD_LIMIT = 2097152
_RESPONSE_LIMIT = 16777216
_ATTEMPT_LIMIT = 100
_TIMEOUT_SECONDS = 300
_LEDGER_RELATIVE = (".reviewcompass", "egress-ledger")
_ALLOWED_PREFIXES = ("docs/", "records/", "tools/", "tests/", "config/")
_ALLOWED_ROOT_FILES = ("AGENTS.md", "TODO_NEXT_SESSION.md", "pyproject.toml")
_DENIED_PREFIXES = ("records/requirements/", ".git/")
_PREAMBLE = (
    "あなたは独立したレビュアです。以下の資料を読み、資料内の依頼記述に"
    "従って判定を返してください。判定には根拠を付けてください。"
)
_ORDER_MEMBERS = frozenset(
    (
        "schema_version",
        "order_identifier",
        "human_approved",
        "destination_provider",
        "destination_model",
        "pilot_provider",
        "purpose",
        "repository_root",
        "source_files",
    )
)
_PROVIDERS = {
    "gemini-api": {
        "host": "generativelanguage.googleapis.com",
        "model_rule": re.compile(r"gemini-[a-z0-9.-]+\Z"),
        "key_variable": "GEMINI_API_KEY",
    },
    "openai-api": {
        "host": "api.openai.com",
        "model_rule": re.compile(r"(?:gpt-|o)[a-z0-9.-]+\Z"),
        "key_variable": "OPENAI_API_KEY",
    },
    "anthropic-api": {
        "host": "api.anthropic.com",
        "model_rule": re.compile(r"claude-[a-z0-9.-]+\Z"),
        "key_variable": "ANTHROPIC_API_KEY",
    },
}


class SendStop(Exception):
    """送信指示を安全に実行できないため処理を停止する。"""

    def __init__(self, reason, source, *, after_attempt=False):
        super().__init__(reason)
        self.reason = reason
        self.source = source
        self.after_attempt = after_attempt


class _DuplicateMember(ValueError):
    """復号後のJSON項目名が重複している。"""


def canonical_json_bytes(value):
    """値を内容識別値用の正準JSON bytesへ変換する。"""

    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha256(value):
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _environment_value(name):
    return os.environ.get(name)


def _has_only_unicode_scalar_values(value):
    return not any(0xD800 <= ord(character) <= 0xDFFF for character in value)


def _absolute_path_parts(value, reason, source):
    if (
        not isinstance(value, str)
        or not value.startswith("/")
        or "\x00" in value
        or not _has_only_unicode_scalar_values(value)
    ):
        raise SendStop(reason, source)
    if value == "/":
        return ()
    parts = value.split("/")[1:]
    if not parts or any(part in ("", ".", "..") for part in parts):
        raise SendStop(reason, source)
    return tuple(parts)


def _read_regular_file(path_value, source, size_limit):
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    if not no_follow:
        raise SendStop("unreadable_input", source)
    descriptor = None
    open_failed = False
    try:
        descriptor = os.open(path_value, os.O_RDONLY | no_follow)
    except OSError:
        open_failed = True
    if open_failed:
        raise SendStop("unreadable_input", source)
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            raise SendStop("unreadable_input", source)
        if details.st_size > size_limit:
            raise SendStop("size_limit_exceeded", source)
        chunks = []
        remaining = size_limit + 1
        while remaining:
            chunk = os.read(descriptor, remaining)
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > size_limit:
            raise SendStop("size_limit_exceeded", source)
        after = os.fstat(descriptor)
    except SendStop:
        raise
    except OSError:
        raise SendStop("unreadable_input", source)
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
    before_identity = (
        details.st_mode,
        details.st_size,
        details.st_dev,
        details.st_ino,
        details.st_mtime_ns,
        details.st_ctime_ns,
    )
    after_identity = (
        after.st_mode,
        after.st_size,
        after.st_dev,
        after.st_ino,
        after.st_mtime_ns,
        after.st_ctime_ns,
    )
    if before_identity != after_identity or len(data) != details.st_size:
        raise SendStop("unreadable_input", source)
    return data


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise _DuplicateMember
        value[key] = item
    return value


def _decode_order(raw):
    source = "order"
    decode_failed = False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        decode_failed = True
    if decode_failed:
        raise SendStop("invalid_utf8", source)
    schema_failed = False
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, ValueError, RecursionError):
        schema_failed = True
    if schema_failed:
        raise SendStop("invalid_schema", source)
    return value


def _is_excluded(path, text, provider_name):
    if (
        len(path) == 3
        and path[0] == "source_files"
        and isinstance(path[1], int)
        and path[2] == "sha256"
        and _SHA256_VALUE.fullmatch(text) is not None
    ):
        return True
    if len(path) == 1 and path[0] in ("destination_provider", "pilot_provider"):
        return text in _PROVIDERS
    if len(path) == 1 and path[0] == "destination_model":
        definition = _PROVIDERS.get(provider_name)
        return (
            definition is not None
            and definition["model_rule"].fullmatch(text) is not None
        )
    return False


def _iter_strings(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str):
                yield key, None
            yield from _iter_strings(item, path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _iter_strings(item, path + (index,))
    elif isinstance(value, str):
        yield value, path


def _scan_text(text, source):
    rules = default_pattern_rules()
    if any(re.search(rule.pattern, text) for rule in rules):
        raise SendStop("sensitive_data_remaining", source)
    if find_high_entropy(text):
        raise SendStop("sensitive_data_remaining", source)


def _scan_order(value):
    provider_name = value.get("destination_provider") if isinstance(value, dict) else None
    for text, path in _iter_strings(value):
        if path is not None and _is_excluded(path, text, provider_name):
            continue
        _scan_text(text, "order")


def _validate_relative_path(value, source):
    if (
        not isinstance(value, str)
        or not value
        or value.startswith("/")
        or "\x00" in value
        or not _has_only_unicode_scalar_values(value)
    ):
        raise SendStop("source_file_rejected", source)
    parts = value.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise SendStop("source_file_rejected", source)
    allowed = value in _ALLOWED_ROOT_FILES or any(
        value.startswith(prefix) for prefix in _ALLOWED_PREFIXES
    )
    denied = any(value.startswith(prefix) for prefix in _DENIED_PREFIXES)
    if not allowed or denied:
        raise SendStop("source_file_rejected", source)
    return value


def _validate_order(value):
    source = "order"
    if not isinstance(value, dict) or set(value) != _ORDER_MEMBERS:
        raise SendStop("invalid_schema", source)
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise SendStop("invalid_schema", source)
    identifier = value["order_identifier"]
    if (
        not isinstance(identifier, str)
        or _GENERAL_IDENTIFIER.fullmatch(identifier) is None
    ):
        raise SendStop("invalid_schema", source)
    if value["human_approved"] is not True:
        raise SendStop("invalid_schema", source)
    provider_name = value["destination_provider"]
    if provider_name not in _PROVIDERS:
        raise SendStop("invalid_schema", source)
    definition = _PROVIDERS[provider_name]
    model = value["destination_model"]
    if not isinstance(model, str) or definition["model_rule"].fullmatch(model) is None:
        raise SendStop("invalid_schema", source)
    pilot = value["pilot_provider"]
    if pilot not in _PROVIDERS:
        raise SendStop("invalid_schema", source)
    if pilot == provider_name:
        raise SendStop("reviewer_not_independent", source)
    purpose = value["purpose"]
    if (
        not isinstance(purpose, str)
        or not 1 <= len(purpose) <= 500
        or "\x00" in purpose
        or not _has_only_unicode_scalar_values(purpose)
    ):
        raise SendStop("invalid_schema", source)
    _absolute_path_parts(value["repository_root"], "invalid_schema", source)
    source_files = value["source_files"]
    if not isinstance(source_files, list) or not 1 <= len(source_files) <= 64:
        raise SendStop("invalid_schema", source)
    for item in source_files:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise SendStop("invalid_schema", source)
        digest = item["sha256"]
        if not isinstance(digest, str) or _SHA256_VALUE.fullmatch(digest) is None:
            raise SendStop("invalid_schema", source)
        _validate_relative_path(item["path"], "source_file")
    return value


def _ledger_root(repository_root):
    return "/".join((repository_root.rstrip("/"),) + _LEDGER_RELATIVE)


def _exists(path_value):
    try:
        os.lstat(path_value)
    except OSError:
        return False
    return True


def _is_directory(path_value):
    try:
        details = os.lstat(path_value)
    except OSError:
        return False
    return stat.S_ISDIR(details.st_mode)


def _record_names(identifier):
    return (
        f"{identifier}--attempt-v1.json",
        f"{identifier}--response-v1.raw",
        f"{identifier}--result-v1.json",
    )


def _check_ledger(value):
    repository_root = value["repository_root"]
    if not _exists(f"{repository_root.rstrip('/')}/.git"):
        raise SendStop("invalid_repository_root", "order")
    ledger = _ledger_root(repository_root)
    if not _is_directory(ledger):
        raise SendStop("invalid_output_root", "ledger")
    identifier = value["order_identifier"]
    attempt_name, response_name, result_name = _record_names(identifier)
    if _exists(f"{ledger}/{attempt_name}"):
        raise SendStop("duplicate_order", "ledger")
    for name in (response_name, result_name):
        if _exists(f"{ledger}/{name}"):
            raise SendStop("invalid_output_root", "ledger")
    for name in (attempt_name, response_name, result_name):
        if _exists(f"{ledger}/{name}.partial"):
            raise SendStop("invalid_output_root", "ledger")
    listing_failed = False
    try:
        entries = os.listdir(ledger)
    except OSError:
        listing_failed = True
    if listing_failed:
        raise SendStop("invalid_output_root", "ledger")
    attempts = sum(1 for name in entries if name.endswith("--attempt-v1.json"))
    if attempts >= _ATTEMPT_LIMIT:
        raise SendStop("limit_exceeded", "ledger")
    return ledger


def _build_payload(value):
    repository_root = value["repository_root"].rstrip("/")
    sections = [_PREAMBLE]
    for item in value["source_files"]:
        relative = item["path"]
        declared = item["sha256"]
        data = _read_regular_file(
            f"{repository_root}/{relative}",
            "source_file",
            _PAYLOAD_LIMIT,
        )
        if hashlib.sha256(data).hexdigest() != declared:
            raise SendStop("source_file_rejected", "source_file")
        decode_failed = False
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            decode_failed = True
        if decode_failed:
            raise SendStop("source_file_rejected", "source_file")
        _scan_text(text, "source_file")
        sections.append(f"----- FILE: {relative} (sha256={declared}) -----")
        sections.append(text)
    payload_text = "\n".join(sections)
    payload_bytes = payload_text.encode("utf-8")
    if len(payload_bytes) > _PAYLOAD_LIMIT:
        raise SendStop("limit_exceeded", "order")
    return payload_text, payload_bytes


def _request_for(value, payload_text, key):
    provider_name = value["destination_provider"]
    model = value["destination_model"]
    host = _PROVIDERS[provider_name]["host"]
    if provider_name == "gemini-api":
        url = f"https://{host}/v1beta/models/{model}:generateContent"
        headers = {"x-goog-api-key": key, "Content-Type": "application/json"}
        body = {"contents": [{"parts": [{"text": payload_text}]}]}
    elif provider_name == "openai-api":
        url = f"https://{host}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": model,
            "messages": [{"role": "user", "content": payload_text}],
        }
    else:
        url = f"https://{host}/v1/messages"
        headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        body = {
            "model": model,
            "max_tokens": 8192,
            "messages": [{"role": "user", "content": payload_text}],
        }
    return url, headers, canonical_json_bytes(body)


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None


def _build_opener():
    return urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        _NoRedirect(),
    )


def _send_request(url, headers, body, timeout):
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    opener = _build_opener()
    try:
        with opener.open(request, timeout=timeout) as response:
            status = response.status
            data = response.read(_RESPONSE_LIMIT + 1)
    except urllib.error.HTTPError as error:
        status = error.code
        data = error.read(_RESPONSE_LIMIT + 1)
    return status, data


def _publish(record_bytes, final_path):
    partial_path = f"{final_path}.partial"
    no_follow = getattr(os, "O_NOFOLLOW", 0)
    creation_failed = False
    descriptor = None
    try:
        descriptor = os.open(
            partial_path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | no_follow,
            0o600,
        )
    except OSError:
        creation_failed = True
    if creation_failed:
        raise SendStop("record_write_failed", "ledger", after_attempt=True)
    write_failed = False
    try:
        written = os.write(descriptor, record_bytes)
        if written != len(record_bytes):
            write_failed = True
    except OSError:
        write_failed = True
    finally:
        try:
            os.close(descriptor)
        except OSError:
            write_failed = True
    if not write_failed:
        try:
            verify_descriptor = os.open(partial_path, os.O_RDONLY | no_follow)
            try:
                chunks = []
                remaining = len(record_bytes) + 1
                while remaining:
                    chunk = os.read(verify_descriptor, remaining)
                    if not chunk:
                        break
                    chunks.append(chunk)
                    remaining -= len(chunk)
                if b"".join(chunks) != record_bytes:
                    write_failed = True
            finally:
                os.close(verify_descriptor)
        except OSError:
            write_failed = True
    if write_failed:
        try:
            os.unlink(partial_path)
        except OSError:
            pass
        raise SendStop("record_write_failed", "ledger", after_attempt=True)
    publish_failed = False
    try:
        os.link(partial_path, final_path)
    except OSError:
        publish_failed = True
    if publish_failed:
        try:
            os.unlink(partial_path)
        except OSError:
            pass
        raise SendStop("record_write_failed", "ledger", after_attempt=True)
    cleanup_failed = False
    try:
        os.unlink(partial_path)
    except OSError:
        cleanup_failed = True
    if cleanup_failed:
        raise SendStop("partial_cleanup_failed", "ledger", after_attempt=True)


def run_send_order(order_path):
    """送信指示fileを検査し、一回送信・保存・台帳着地を行う。"""

    _absolute_path_parts(order_path, "invalid_path", "arguments")
    raw = _read_regular_file(order_path, "order", _ORDER_SIZE_LIMIT)
    decoded = _decode_order(raw)
    _scan_order(decoded)
    value = _validate_order(decoded)
    ledger = _check_ledger(value)
    key_variable = _PROVIDERS[value["destination_provider"]]["key_variable"]
    key = _environment_value(key_variable)
    if not isinstance(key, str) or not key:
        raise SendStop("missing_credentials", "credentials")
    payload_text, payload_bytes = _build_payload(value)
    payload_sha256 = hashlib.sha256(payload_bytes).hexdigest()
    order_sha256 = _sha256(value)
    identifier = value["order_identifier"]
    attempt_name, response_name, result_name = _record_names(identifier)

    attempt = {
        "status": "attempt_recorded",
        "schema_version": 1,
        "order": {"identifier": identifier, "sha256": order_sha256},
        "destination_provider": value["destination_provider"],
        "destination_model": value["destination_model"],
        "pilot_provider": value["pilot_provider"],
        "purpose": value["purpose"],
        "source_files": [dict(item) for item in value["source_files"]],
        "payload_sha256": payload_sha256,
        "payload_bytes": len(payload_bytes),
        "attempted_at": _now_utc(),
        "external_send_approved": True,
    }
    attempt["record_sha256"] = _sha256(attempt)
    _publish(canonical_json_bytes(attempt) + b"\n", f"{ledger}/{attempt_name}")

    url, headers, body = _request_for(value, payload_text, key)
    try:
        status, data = _send_request(url, headers, body, _TIMEOUT_SECONDS)
    except SendStop:
        raise
    except Exception:
        raise SendStop("network_failure", "network", after_attempt=True)
    if not isinstance(data, bytes):
        raise SendStop("network_failure", "network", after_attempt=True)
    if len(data) > _RESPONSE_LIMIT:
        raise SendStop("response_size_exceeded", "network", after_attempt=True)

    _publish(data, f"{ledger}/{response_name}")
    if status != 200:
        raise SendStop("http_error", "network", after_attempt=True)

    result = {
        "status": "response_stored",
        "schema_version": 1,
        "order": {"identifier": identifier, "sha256": order_sha256},
        "http_status": status,
        "payload_sha256": payload_sha256,
        "response_sha256": hashlib.sha256(data).hexdigest(),
        "response_bytes": len(data),
        "completed_at": _now_utc(),
        "external_send_approved": True,
    }
    result["record_sha256"] = _sha256(result)
    result_bytes = canonical_json_bytes(result) + b"\n"
    _publish(result_bytes, f"{ledger}/{result_name}")
    return result_bytes
