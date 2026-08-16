"""外部レビュア一回送信に関する製品試験。通信は全て模擬する。"""

import hashlib
import importlib
import io
import json
import os
import shutil
import tempfile
from pathlib import Path

import pytest


_AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"
_LEDGER_RELATIVE = ".reviewcompass/egress-ledger"


def _core():
    return importlib.import_module("tools.egress.gemini_send")


def _entry():
    return importlib.import_module("tools.egress.gemini_send_entry")


def _canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


@pytest.fixture()
def repo_root():
    created = Path(tempfile.mkdtemp(prefix="g20-", dir="/private/tmp"))
    (created / ".git").mkdir()
    (created / _LEDGER_RELATIVE).mkdir(parents=True)
    (created / "docs").mkdir()
    try:
        yield created
    finally:
        shutil.rmtree(created, ignore_errors=True)


def _write_source(repo_root, relative_path, text):
    target = repo_root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = text.encode("utf-8")
    target.write_bytes(payload)
    return relative_path, hashlib.sha256(payload).hexdigest()


def _order(repo_root, sources, **overrides):
    value = {
        "schema_version": 1,
        "order_identifier": "ORD-G20-001",
        "human_approved": True,
        "destination_provider": "gemini-api",
        "destination_model": "gemini-2.5-pro",
        "pilot_provider": "anthropic-api",
        "purpose": "契約候補の独立確認の依頼",
        "repository_root": str(repo_root),
        "source_files": [
            {"path": path, "sha256": digest} for path, digest in sources
        ],
    }
    value.update(overrides)
    return value


def _write_order(repo_root, order, name="order.json"):
    order_path = repo_root / name
    order_path.write_bytes(json.dumps(order, ensure_ascii=False).encode("utf-8"))
    return order_path


class _FakeResponse:
    def __init__(self, status=200, body=b'{"candidates":[{"text":"ok"}]}'):
        self.status = status
        self.body = body


def _install_transport(monkeypatch, responses):
    core = _core()
    calls = []

    def fake_send(url, headers, body, timeout):
        calls.append(
            {
                "url": url,
                "headers": dict(headers),
                "body": body,
                "timeout": timeout,
            }
        )
        outcome = responses[min(len(calls) - 1, len(responses) - 1)]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome.status, outcome.body

    monkeypatch.setattr(core, "_send_request", fake_send)
    return calls


def _run(order_path):
    buffer = io.BytesIO()
    code = _entry().main(["send", "--order", str(order_path)], output=buffer)
    return code, buffer.getvalue()


def _prepare(repo_root, monkeypatch, *, key="fake-test-key-not-real"):
    sources = [
        _write_source(repo_root, "docs/target.md", "レビュー対象の本文。\n"),
    ]
    order = _order(repo_root, sources)
    order_path = _write_order(repo_root, order)
    monkeypatch.setenv("GEMINI_API_KEY", key)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return order, order_path, sources


def _ledger(repo_root):
    return repo_root / _LEDGER_RELATIVE


# ---------------------------------------------------------------------------
# 受入条件1：模擬通信の正例
# ---------------------------------------------------------------------------


def test_positive_send_lands_attempt_response_result(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    calls = _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 0
    ledger = _ledger(repo_root)
    attempt_path = ledger / "ORD-G20-001--attempt-v1.json"
    response_path = ledger / "ORD-G20-001--response-v1.raw"
    result_path = ledger / "ORD-G20-001--result-v1.json"
    assert attempt_path.exists()
    assert response_path.exists()
    assert result_path.exists()
    assert payload == result_path.read_bytes()
    assert response_path.read_bytes() == b'{"candidates":[{"text":"ok"}]}'

    attempt = json.loads(attempt_path.read_bytes()[:-1])
    assert attempt["status"] == "attempt_recorded"
    assert attempt["order"]["identifier"] == "ORD-G20-001"
    assert attempt["order"]["sha256"] == _sha(order)
    assert attempt["external_send_approved"] is True
    without = dict(attempt)
    del without["record_sha256"]
    assert attempt["record_sha256"] == _sha(without)

    result = json.loads(payload[:-1])
    assert result["status"] == "response_stored"
    assert result["http_status"] == 200
    assert result["payload_sha256"] == attempt["payload_sha256"]
    assert result["response_sha256"] == hashlib.sha256(
        b'{"candidates":[{"text":"ok"}]}',
    ).hexdigest()
    without = dict(result)
    del without["record_sha256"]
    assert result["record_sha256"] == _sha(without)
    assert len(calls) == 1


def test_payload_has_fixed_form_and_binding(repo_root, monkeypatch):
    order, order_path, sources = _prepare(repo_root, monkeypatch)
    calls = _install_transport(monkeypatch, [_FakeResponse()])

    _run(order_path)

    body = json.loads(calls[0]["body"].decode("utf-8"))
    text = body["contents"][0]["parts"][0]["text"]
    assert text.startswith("あなたは独立したレビュアです。")
    path, digest = sources[0]
    assert f"----- FILE: {path} (sha256={digest}) -----" in text
    assert "レビュー対象の本文。" in text
    assert calls[0]["url"] == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-pro:generateContent"
    )
    assert calls[0]["headers"]["x-goog-api-key"] == "fake-test-key-not-real"
    assert calls[0]["timeout"] == 300


# ---------------------------------------------------------------------------
# 受入条件2：由来fileの検査とroot実在検査
# ---------------------------------------------------------------------------


def test_source_digest_mismatch_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["source_files"][0]["sha256"] = hashlib.sha256(b"other").hexdigest()
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"source_file_rejected"' in payload
    assert list(_ledger(repo_root).iterdir()) == []


@pytest.mark.parametrize(
    "bad_path",
    (
        "records/requirements/secret.md",
        ".git/config",
        "../outside.md",
        "docs/./target.md",
        "/docs/target.md",
        "unlisted-root.md",
    ),
)
def test_disallowed_source_paths_stop(repo_root, monkeypatch, bad_path):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["source_files"][0]["path"] = bad_path
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"source_file_rejected"' in payload


def test_missing_git_directory_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    shutil.rmtree(repo_root / ".git")
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"invalid_repository_root"' in payload
    assert list(_ledger(repo_root).iterdir()) == []


def test_invalid_utf8_source_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    (repo_root / "docs/target.md").write_bytes(b"\xff\xfe broken")
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"source_file_rejected"' in payload


# ---------------------------------------------------------------------------
# 受入条件3：機微検査と除外
# ---------------------------------------------------------------------------


def test_sensitive_source_content_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    _write_source(repo_root, "docs/target.md", f"本文に {_AWS_KEY} を含む。\n")
    order["source_files"] = [
        {
            "path": "docs/target.md",
            "sha256": hashlib.sha256(
                (repo_root / "docs/target.md").read_bytes(),
            ).hexdigest(),
        },
    ]
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 3
    assert b'"sensitive_data_remaining"' in payload
    assert _AWS_KEY.encode() not in payload
    assert list(_ledger(repo_root).iterdir()) == []


def test_sensitive_purpose_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["purpose"] = f"目的に {_AWS_KEY} を含む"
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 3
    assert b'"sensitive_data_remaining"' in payload


def test_random_identifier_stops_as_specified(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["order_identifier"] = hashlib.sha256(b"uuid-like").hexdigest()
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 3
    assert b'"sensitive_data_remaining"' in payload


def test_fixed_enums_and_declared_digests_are_not_flagged(
    repo_root,
    monkeypatch,
):
    _, order_path, _ = _prepare(repo_root, monkeypatch)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, _ = _run(order_path)

    assert code == 0


# ---------------------------------------------------------------------------
# 受入条件4・5：重複IDと上限
# ---------------------------------------------------------------------------


def test_duplicate_order_stops_without_second_send(repo_root, monkeypatch):
    _, order_path, _ = _prepare(repo_root, monkeypatch)
    calls = _install_transport(monkeypatch, [_FakeResponse(), _FakeResponse()])

    first_code, _ = _run(order_path)
    second_code, second_payload = _run(order_path)

    assert first_code == 0
    assert second_code == 2
    assert b'"duplicate_order"' in second_payload
    assert len(calls) == 1


def test_cumulative_limit_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    core = _core()
    monkeypatch.setattr(core, "_ATTEMPT_LIMIT", 2)
    ledger = _ledger(repo_root)
    for index in range(2):
        (ledger / f"ORD-OLD-{index:03d}--attempt-v1.json").write_bytes(b"{}")
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"limit_exceeded"' in payload
    assert b'"ledger"' in payload


def test_payload_size_limit_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    core = _core()
    monkeypatch.setattr(core, "_PAYLOAD_LIMIT", 64)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"limit_exceeded"' in payload


def test_response_size_limit_stops_after_attempt(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    core = _core()
    monkeypatch.setattr(core, "_RESPONSE_LIMIT", 8)
    _install_transport(monkeypatch, [_FakeResponse(body=b"123456789")])

    code, payload = _run(order_path)

    assert code == 7
    assert b'"response_size_exceeded"' in payload
    ledger = _ledger(repo_root)
    assert (ledger / "ORD-G20-001--attempt-v1.json").exists()
    assert not (ledger / "ORD-G20-001--response-v1.raw").exists()
    assert not (ledger / "ORD-G20-001--result-v1.json").exists()


# ---------------------------------------------------------------------------
# 受入条件6・9：鍵の非表示と環境変数の限定
# ---------------------------------------------------------------------------


def test_key_never_appears_in_outputs(repo_root, monkeypatch):
    key = "fake-secret-key-for-test-0001"
    _, order_path, _ = _prepare(repo_root, monkeypatch, key=key)
    _install_transport(monkeypatch, [_FakeResponse()])

    _, payload = _run(order_path)

    rendered = payload.decode("utf-8")
    assert key not in rendered
    for landed in _ledger(repo_root).iterdir():
        assert key.encode() not in landed.read_bytes()


def test_only_selected_provider_variable_is_read(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "must-not-be-read")
    core = _core()
    read_names = []
    original_get = core._environment_value

    def spying_get(name):
        read_names.append(name)
        return original_get(name)

    monkeypatch.setattr(core, "_environment_value", spying_get)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, _ = _run(order_path)

    assert code == 0
    assert read_names == ["GEMINI_API_KEY"]


def test_missing_credentials_stop(repo_root, monkeypatch):
    _, order_path, _ = _prepare(repo_root, monkeypatch)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"missing_credentials"' in payload
    assert list(_ledger(repo_root).iterdir()) == []


# ---------------------------------------------------------------------------
# 受入条件7：固定経路・provider切り替え・独立性・非追従
# ---------------------------------------------------------------------------


def test_openai_provider_uses_fixed_route(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["destination_provider"] = "openai-api"
    order["destination_model"] = "gpt-5.6-sol"
    order_path = _write_order(repo_root, order)
    monkeypatch.setenv("OPENAI_API_KEY", "fake-openai-key")
    calls = _install_transport(monkeypatch, [_FakeResponse()])

    code, _ = _run(order_path)

    assert code == 0
    assert calls[0]["url"] == "https://api.openai.com/v1/chat/completions"
    assert calls[0]["headers"]["Authorization"] == "Bearer fake-openai-key"
    body = json.loads(calls[0]["body"].decode("utf-8"))
    assert body["model"] == "gpt-5.6-sol"
    assert body["messages"][0]["role"] == "user"


def test_anthropic_provider_uses_fixed_route(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["destination_provider"] = "anthropic-api"
    order["destination_model"] = "claude-opus-5"
    order["pilot_provider"] = "openai-api"
    order_path = _write_order(repo_root, order)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-anthropic-key")
    calls = _install_transport(monkeypatch, [_FakeResponse()])

    code, _ = _run(order_path)

    assert code == 0
    assert calls[0]["url"] == "https://api.anthropic.com/v1/messages"
    assert calls[0]["headers"]["x-api-key"] == "fake-anthropic-key"
    assert calls[0]["headers"]["anthropic-version"] == "2023-06-01"
    body = json.loads(calls[0]["body"].decode("utf-8"))
    assert body["max_tokens"] == 8192


def test_same_pilot_and_destination_stops(repo_root, monkeypatch):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["pilot_provider"] = "gemini-api"
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"reviewer_not_independent"' in payload


@pytest.mark.parametrize(
    ("provider", "model"),
    (
        ("gemini-api", "gpt-5.6-sol"),
        ("openai-api", "claude-opus-5"),
        ("anthropic-api", "gemini-2.5-pro"),
        ("gemini-api", "GEMINI-2.5"),
    ),
)
def test_model_name_rule_mismatch_stops(repo_root, monkeypatch, provider, model):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    order["destination_provider"] = provider
    order["destination_model"] = model
    if provider == "gemini-api":
        order["pilot_provider"] = "anthropic-api"
    else:
        order["pilot_provider"] = "gemini-api"
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"invalid_schema"' in payload


def test_opener_disables_proxy_and_redirects():
    core = _core()
    opener = core._build_opener()
    proxy_handlers = [
        handler
        for handler in opener.handlers
        if handler.__class__.__name__ == "ProxyHandler"
    ]
    assert len(proxy_handlers) == 1
    assert proxy_handlers[0].proxies == {}
    redirect_handlers = [
        handler
        for handler in opener.handlers
        if "Redirect" in handler.__class__.__name__
    ]
    assert len(redirect_handlers) == 1
    assert (
        redirect_handlers[0].redirect_request(
            None, None, None, None, None, None,
        )
        is None
    )


# ---------------------------------------------------------------------------
# 受入条件8：通信失敗・HTTP異常
# ---------------------------------------------------------------------------


def test_http_error_saves_response_and_keeps_attempt(repo_root, monkeypatch):
    _, order_path, _ = _prepare(repo_root, monkeypatch)
    _install_transport(monkeypatch, [_FakeResponse(status=429, body=b"slow down")])

    code, payload = _run(order_path)

    assert code == 7
    assert b'"http_error"' in payload
    ledger = _ledger(repo_root)
    assert (ledger / "ORD-G20-001--attempt-v1.json").exists()
    assert (ledger / "ORD-G20-001--response-v1.raw").read_bytes() == b"slow down"
    assert not (ledger / "ORD-G20-001--result-v1.json").exists()


def test_network_failure_keeps_attempt_without_response(repo_root, monkeypatch):
    _, order_path, _ = _prepare(repo_root, monkeypatch)
    _install_transport(monkeypatch, [OSError("connection reset")])

    code, payload = _run(order_path)

    assert code == 7
    assert payload == _canonical(
        {
            "external_send_approved": True,
            "reason": "network_failure",
            "source": "network",
            "status": "stopped",
        },
    ) + b"\n"
    ledger = _ledger(repo_root)
    assert (ledger / "ORD-G20-001--attempt-v1.json").exists()
    assert not (ledger / "ORD-G20-001--response-v1.raw").exists()


# ---------------------------------------------------------------------------
# 送信指示のschemaと引数
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "mutate",
    (
        lambda order: order.update({"human_approved": False}),
        lambda order: order.update({"destination_provider": "unknown-api"}),
        lambda order: order.update({"unknown_member": "x"}),
        lambda order: order.pop("purpose"),
        lambda order: order.update({"purpose": ""}),
        lambda order: order.update({"schema_version": 2}),
        lambda order: order.update({"repository_root": "relative/path"}),
        lambda order: order.update({"source_files": []}),
    ),
)
def test_order_schema_violations_stop(repo_root, monkeypatch, mutate):
    order, order_path, _ = _prepare(repo_root, monkeypatch)
    mutate(order)
    order_path = _write_order(repo_root, order)
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"invalid_schema"' in payload


@pytest.mark.parametrize(
    "arguments",
    (
        [],
        ["send"],
        ["run", "--order", "/x"],
        ["send", "--order", "/x", "--order", "/x"],
        ["send", "--unknown", "/x"],
    ),
)
def test_malformed_arguments_stop(arguments):
    buffer = io.BytesIO()
    code = _entry().main(arguments, output=buffer)

    assert code == 2
    assert b'"invalid_arguments"' in buffer.getvalue()


def test_relative_order_path_stops():
    buffer = io.BytesIO()
    code = _entry().main(["send", "--order", "order.json"], output=buffer)

    assert code == 2
    assert b'"invalid_path"' in buffer.getvalue()


def test_ledger_root_missing_stops(repo_root, monkeypatch):
    _, order_path, _ = _prepare(repo_root, monkeypatch)
    shutil.rmtree(_ledger(repo_root))
    _install_transport(monkeypatch, [_FakeResponse()])

    code, payload = _run(order_path)

    assert code == 2
    assert b'"invalid_output_root"' in payload
    assert b'"ledger"' in payload


# ---------------------------------------------------------------------------
# 受入条件10・11：配置と保護
# ---------------------------------------------------------------------------


def test_console_script_is_registered():
    import tomllib

    with Path("pyproject.toml").open("rb") as stream:
        configuration = tomllib.load(stream)

    assert configuration["project"]["scripts"][
        "reviewcompass3-gemini-send"
    ] == "tools.egress.gemini_send_entry:main"


def test_existing_egress_modules_unchanged():
    expected = {
        "tools/egress/__init__.py": "8386033f1d8ef3999da06b8a17cd4a9a5282636dda1e77d7d80a4a8b354656fd",
        "tools/egress/approval.py": "cb8f97e1d2b05f0ec7e9bad9e045c80b8378a03167be2d623f13853c3236b243",
        "tools/egress/dry_run.py": "73c5c82dc1eeb24a75593c51cd8a6b01698498c4db0e7df8124124ee7dc207d2",
        "tools/egress/gate.py": "ec611dfa65c0ff8f8ccf586ed491e944430cf80952a797861ea3b06a7f1de0c1",
        "tools/egress/payload.py": "daeb48b1ef3c00f7ae14ba1debfaba7efe564387808e505d57e4c15a14d34a1f",
        "tools/egress/prefilter.py": "c0b6a2da30923802eb419817d55bf8c2eb1f2e6a9a580074b1f90cd77773bf43",
        "tools/egress/sender.py": "05286fe21ee5baf264c80fe8518eccef3602de1c7ada6041e121dd4a2b5bbef8",
    }
    for path, digest in expected.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest, path
