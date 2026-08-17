"""契約010 Reviewer起動アダプタ（第1 backend：agy）の境界テスト。

契約：records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md
外部起動は行わない（subprocess差替えの単体試験。実行器試験の型を流用）。
"""

import hashlib
import importlib
import json
import os
import subprocess as host_subprocess
from pathlib import Path

import pytest


FORBIDDEN_VARIABLES = (
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_GENAI_API_KEY",
    "GOOGLE_APPLICATION_CREDENTIALS",
)
TEST_MODEL = "gemini-test-model"


def _core():
    return importlib.import_module("tools.reviewer_launch.core")


def _record_module():
    return importlib.import_module("tools.reviewer_launch.record")


def _entry():
    return importlib.import_module("tools.reviewer_launch.entry")


def _operations():
    return importlib.import_module(
        "tools.operations.operation_contract_run"
    )


def _sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git(repository, *arguments):
    return host_subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture()
def clean_environment(monkeypatch):
    for name in FORBIDDEN_VARIABLES:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture()
def repository(tmp_path):
    repo = tmp_path / "repo"
    (repo / "records" / "session-handoffs").mkdir(parents=True)
    _git_init(repo)
    request = repo / "records" / "session-handoffs" / (
        "2026-08-16-sample-review-agy-request-v1.md"
    )
    request.write_text(
        "# 依頼record（試験用）\n\n- 対象：sample\n",
        encoding="utf-8",
    )
    _git(repo, "add", "records/session-handoffs")
    _git(repo, "commit", "-m", "Add sample request record")
    return repo


def _git_init(repo):
    repo.mkdir(exist_ok=True)
    _git_bare_safe(repo)


def _git_bare_safe(repo):
    host_subprocess.run(
        ("git", "init", "-q", str(repo)),
        capture_output=True,
        text=True,
        check=True,
    )
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "commit.gpgsign", "false")


def _request_relative(repository):
    return (
        "records/session-handoffs/"
        "2026-08-16-sample-review-agy-request-v1.md"
    )


def _stream_text(model=TEST_MODEL, verdict=None, extra_lines=(), response=None):
    # agyのstream実形式（e2e-010-002実測）：event鍵で
    # init（init.modelにmodel名）／step_update／result（result.responseに
    # 構造化出力のJSON本文）が流れる。
    verdict_value = verdict
    if verdict_value is None:
        verdict_value = _valid_verdict()
    response_text = (
        json.dumps(verdict_value, ensure_ascii=False)
        if response is None
        else response
    )
    lines = [
        json.dumps(
            {
                "conversation_id": "c-1",
                "event": "init",
                "init": {"model": model, "permission_mode": "plan"},
            }
        ),
        json.dumps(
            {
                "event": "step_update",
                "step_update": {"step_index": 0, "state": "DONE"},
            }
        ),
        *extra_lines,
        json.dumps(
            {
                "event": "result",
                "result": {"status": "SUCCESS", "response": response_text},
            }
        ),
    ]
    return "\n".join(lines) + "\n"


def _valid_verdict():
    return {
        "reviewer": {"provider": "google", "model": TEST_MODEL},
        "freshness": {
            "expected": "0" * 64,
            "observed": "0" * 64,
            "result": "match",
        },
        "target": {
            "path": "records/session-handoffs/sample.md",
            "commit": "0" * 40,
        },
        "findings": [],
        "unexamined": [],
        "verdict": "verified",
        "summary": "問題なし",
    }


def _write_project_config(projects_root, repository, with_grant=True):
    projects_root.mkdir(parents=True, exist_ok=True)
    repo = str(Path(repository).resolve())
    value = {
        "id": "proj-test",
        "name": "test-project",
        "projectResources": {
            "resources": [
                {"gitFolder": {"folderUri": "file://" + repo}}
            ]
        },
    }
    if with_grant:
        value["permissionGrants"] = {
            "permissionGrants": {
                "allow": ["read_file(%s)" % repo],
            }
        }
    (projects_root / "proj-test.json").write_text(
        json.dumps(value, ensure_ascii=False), encoding="utf-8"
    )


class _FacadeRecorder:
    def __init__(self, stdout="", exit_code=0):
        self.calls = []
        self.stdout = stdout
        self.exit_code = exit_code

    def run(self, arguments, **keywords):
        self.calls.append((tuple(arguments), keywords))
        return host_subprocess.CompletedProcess(
            arguments,
            self.exit_code,
            stdout=self.stdout,
            stderr="",
        )


def _launch(repository, monkeypatch, facade, **overrides):
    core = _core()
    monkeypatch.setattr(
        core, "ALLOWED_RESPONSE_MODELS", (TEST_MODEL,), raising=True
    )
    monkeypatch.setattr(core.subprocess, "run", facade.run, raising=True)
    projects_root = repository.parent / "projects-config"
    _write_project_config(projects_root, repository)
    monkeypatch.setattr(
        core, "PROJECTS_CONFIG_ROOT", projects_root, raising=True
    )
    request = _request_relative(repository)
    expected = _sha256_file(repository / request)
    values = {
        "repository": repository,
        "request_relative_path": request,
        "expected_sha256": expected,
        "private_root": repository.parent / "private",
        "backend_name": "antigravity-cli",
        "run_id": "run-001",
    }
    values.update(overrides)
    return core.launch_review(**values)


# ---- 認証遮断（§9-2） ----


@pytest.mark.parametrize("variable", FORBIDDEN_VARIABLES)
def test_forbidden_auth_environment_stops_before_launch(
    repository, monkeypatch, clean_environment, variable
):
    core = _core()
    monkeypatch.setenv(variable, "secret")
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch(repository, monkeypatch, facade)
    assert caught.value.reason == "api_key_environment_forbidden"
    assert facade.calls == []


# ---- 独立性tier判定（§9-3） ----


def test_tier_one_declared_for_cross_provider():
    core = _core()
    assert core.judge_tier("google") == 1


def test_same_provider_backend_stops():
    core = _core()
    with pytest.raises(core.LaunchStop) as caught:
        core.judge_tier("anthropic")
    assert caught.value.reason == "reviewer_not_independent_tier"


def test_unknown_backend_stops(repository, monkeypatch, clean_environment):
    core = _core()
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch(
            repository,
            monkeypatch,
            facade,
            backend_name="unknown-backend",
        )
    assert caught.value.reason == "backend_unknown"
    assert facade.calls == []


# ---- 起動引数の固定（§7.1） ----


def test_fixed_arguments_exact(clean_environment):
    # E2E e2e-010-001の実測でagyの--printが値旗と判明したため
    # `--旗=値`形式・位置引数なしへ訂正。e2e-010-002の実測で既定の
    # request-review方式がheadlessで自動拒否となるため、読み取り専用
    # 相当として--mode=planを確定した（契約§7.1がRED段実測へ留保した
    # 事項。書込みを許すaccept-editsは引き続き禁止）。
    core = _core()
    arguments = core.build_arguments(
        "agy", "prompt-text", TEST_MODEL, "proj-test"
    )
    schema_text = json.dumps(
        core.VERDICT_SCHEMA, ensure_ascii=False, sort_keys=True
    )
    assert arguments == [
        "agy",
        "--output-format=stream-json",
        "--json-schema=" + schema_text,
        "--model=" + TEST_MODEL,
        "--mode=plan",
        "--sandbox",
        "--project=proj-test",
        "--disable-slash-commands",
        "--print-timeout=600s",
        "--print=prompt-text",
    ]
    assert "--dangerously-skip-permissions" not in arguments
    assert "--mode=accept-edits" not in arguments


def test_prompt_contains_fixed_elements(repository):
    # e2e-010-002の実測（headlessでcommand許可が自動拒否）により、
    # shasum実行指示を読取り道具限定・not_computable申告の指示へ訂正。
    core = _core()
    request = _request_relative(repository)
    digest = _sha256_file(repository / request)
    prompt = core.build_prompt(str(repository), request, digest)
    assert request in prompt
    assert digest in prompt
    assert "Reviewer" in prompt
    assert "shasum" not in prompt
    assert "not_computable" in prompt
    assert "読取り道具" in prompt
    assert "書込み" in prompt
    assert "unexamined" in prompt
    # e2e-010-003の実測（作業領域外grepで自動拒否→終了）による追加固定
    assert "view_file" in prompt
    assert "作業領域" in prompt
    # e2e-010-004の実測（読取り道具は絶対path要求）による追加固定
    assert str(repository) in prompt
    assert "%s/%s" % (repository, request) in prompt
    assert "絶対path" in prompt


def test_prompt_byte_limit_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    monkeypatch.setattr(core, "PROMPT_BYTE_LIMIT", 16, raising=True)
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch(repository, monkeypatch, facade)
    assert caught.value.reason == "prompt_payload_limit_exceeded"
    assert facade.calls == []


# ---- 許可model一覧（§7.1：空のままでは起動しない） ----


def test_empty_allowed_models_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    monkeypatch.setattr(core.subprocess, "run", facade.run, raising=True)
    request = _request_relative(repository)
    monkeypatch.setattr(
        core, "ALLOWED_RESPONSE_MODELS", (), raising=True
    )
    with pytest.raises(core.LaunchStop) as caught:
        core.launch_review(
            repository=repository,
            request_relative_path=request,
            expected_sha256=_sha256_file(repository / request),
            private_root=repository.parent / "private",
            backend_name="antigravity-cli",
            run_id="run-001",
        )
    assert caught.value.reason == "allowed_models_unfixed"
    assert facade.calls == []


def test_allowed_models_fixed_to_approved_value():
    core = _core()
    assert core.ALLOWED_RESPONSE_MODELS == (
        "gemini-3.1-pro-high",
        "claude-opus-5",
    )


# ---- project束縛と読取り恒久許可（e2e-010-006後の実測に基づく） ----


def test_project_binding_missing_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    monkeypatch.setattr(
        core, "ALLOWED_RESPONSE_MODELS", (TEST_MODEL,), raising=True
    )
    monkeypatch.setattr(core.subprocess, "run", facade.run, raising=True)
    monkeypatch.setattr(
        core,
        "PROJECTS_CONFIG_ROOT",
        repository.parent / "no-projects",
        raising=True,
    )
    request = _request_relative(repository)
    with pytest.raises(core.LaunchStop) as caught:
        core.launch_review(
            repository=repository,
            request_relative_path=request,
            expected_sha256=_sha256_file(repository / request),
            private_root=repository.parent / "private",
            backend_name="antigravity-cli",
            run_id="run-001",
        )
    assert caught.value.reason == "project_binding_missing"
    assert facade.calls == []


def test_read_grant_missing_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    monkeypatch.setattr(
        core, "ALLOWED_RESPONSE_MODELS", (TEST_MODEL,), raising=True
    )
    monkeypatch.setattr(core.subprocess, "run", facade.run, raising=True)
    projects_root = repository.parent / "projects-config-nogrant"
    _write_project_config(projects_root, repository, with_grant=False)
    monkeypatch.setattr(
        core, "PROJECTS_CONFIG_ROOT", projects_root, raising=True
    )
    request = _request_relative(repository)
    with pytest.raises(core.LaunchStop) as caught:
        core.launch_review(
            repository=repository,
            request_relative_path=request,
            expected_sha256=_sha256_file(repository / request),
            private_root=repository.parent / "private",
            backend_name="antigravity-cli",
            run_id="run-001",
        )
    assert caught.value.reason == "read_grant_missing"
    assert facade.calls == []


# ---- 鮮度（起動直前の再計算。§7.3-1前半） ----


def test_request_digest_mismatch_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch(
            repository,
            monkeypatch,
            facade,
            expected_sha256="f" * 64,
        )
    assert caught.value.reason == "request_record_stale"
    assert facade.calls == []


def test_missing_request_record_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch(
            repository,
            monkeypatch,
            facade,
            request_relative_path="records/session-handoffs/none.md",
        )
    assert caught.value.reason == "request_record_unreadable"
    assert facade.calls == []


# ---- 起動と保存（§9-4） ----


def test_successful_launch_saves_raw_and_launch_record(
    repository, monkeypatch, clean_environment
):
    facade = _FacadeRecorder(stdout=_stream_text())
    result = _launch(repository, monkeypatch, facade)
    assert result["status"] == "succeeded"
    assert result["tier"] == 1
    assert result["model"] == TEST_MODEL
    private_root = repository.parent / "private"
    raw_path = private_root / "run-001" / "reviewer.raw.json"
    launch_path = private_root / "run-001" / "launch.json"
    assert raw_path.is_file()
    assert launch_path.is_file()
    raw_document = json.loads(raw_path.read_text(encoding="utf-8"))
    assert raw_document["assignment"]["provider"] == "google"
    assert raw_document["assignment"]["route"] == "independent"
    launch_document = json.loads(
        launch_path.read_text(encoding="utf-8")
    )
    assert launch_document["tier"] == 1
    assert launch_document["exit_code"] == 0
    assert launch_document["backend"] == "antigravity-cli"
    assert result["raw_digest"] == raw_document["raw_digest"]


def test_disallowed_model_stops_after_raw_saved(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder(stdout=_stream_text(model="other-model"))
    with pytest.raises(core.LaunchStop) as caught:
        _launch(repository, monkeypatch, facade)
    assert caught.value.reason == "response_model_not_allowed"
    raw_path = (
        repository.parent / "private" / "run-001" / "reviewer.raw.json"
    )
    assert raw_path.is_file()


def test_nonzero_exit_stops_and_saves_failure(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder(stdout="", exit_code=3)
    with pytest.raises(core.LaunchStop) as caught:
        _launch(repository, monkeypatch, facade)
    assert caught.value.reason == "launch_failed"
    raw_path = (
        repository.parent / "private" / "run-001" / "reviewer.raw.json"
    )
    assert raw_path.is_file()
    raw_document = json.loads(raw_path.read_text(encoding="utf-8"))
    assert raw_document["status"] == "failed"


def test_schema_nonconforming_result_stops_after_raw_saved(
    repository, monkeypatch, clean_environment
):
    core = _core()
    broken = dict(_valid_verdict())
    del broken["verdict"]
    facade = _FacadeRecorder(stdout=_stream_text(verdict=broken))
    with pytest.raises(core.LaunchStop) as caught:
        _launch(repository, monkeypatch, facade)
    assert caught.value.reason == "verdict_schema_nonconforming"
    raw_path = (
        repository.parent / "private" / "run-001" / "reviewer.raw.json"
    )
    assert raw_path.is_file()


def test_empty_response_stops_after_raw_saved(
    repository, monkeypatch, clean_environment
):
    # e2e-010-002の実測事象の固定：result.responseが空文字列の場合は
    # 転記せず停止する（rawは保存済み）。
    core = _core()
    facade = _FacadeRecorder(stdout=_stream_text(response=""))
    with pytest.raises(core.LaunchStop) as caught:
        _launch(repository, monkeypatch, facade)
    assert caught.value.reason == "verdict_schema_nonconforming"
    raw_path = (
        repository.parent / "private" / "run-001" / "reviewer.raw.json"
    )
    assert raw_path.is_file()


# ---- 判定schemaの検証（§7.2） ----


def test_verdict_vocabulary_enforced():
    record_module = _record_module()
    value = _valid_verdict()
    value["verdict"] = "maybe"
    with pytest.raises(record_module.VerdictInvalid):
        record_module.validate_verdict(value)


def test_findings_identifier_uniqueness():
    record_module = _record_module()
    value = _valid_verdict()
    finding = {
        "identifier": "F-1",
        "severity": "high",
        "blocking": True,
        "claim": "重複",
        "evidence_path": "records/x.md",
        "evidence_location": "§1",
    }
    value["findings"] = [finding, dict(finding)]
    with pytest.raises(record_module.VerdictInvalid):
        record_module.validate_verdict(value)


def test_freshness_mismatch_rejected():
    record_module = _record_module()
    value = _valid_verdict()
    value["freshness"]["result"] = "mismatch"
    with pytest.raises(record_module.VerdictInvalid) as caught:
        record_module.validate_verdict(value)
    assert "mismatch" in str(caught.value)


def test_freshness_not_computable_requires_reason():
    record_module = _record_module()
    value = _valid_verdict()
    value["freshness"] = {
        "expected": "0" * 64,
        "observed": "not_computable",
        "result": "not_computable",
    }
    with pytest.raises(record_module.VerdictInvalid):
        record_module.validate_verdict(value)
    value["freshness"]["reason"] = "端末実行が許可されていない"
    record_module.validate_verdict(value)


# ---- 判定recordの機械転記（§9-5） ----


def _transcribe(repository, verdict=None, run_id="run-001"):
    record_module = _record_module()
    request = _request_relative(repository)
    value = verdict if verdict is not None else _valid_verdict()
    return record_module.transcribe_verdict_record(
        repository=repository,
        request_relative_path=request,
        request_sha256=_sha256_file(repository / request),
        verdict=value,
        tier=1,
        backend_name="antigravity-cli",
        model=TEST_MODEL,
        raw_digest="a" * 64,
        raw_store_kind="private_root_immutable_store",
        run_id=run_id,
    )


def test_transcription_creates_single_record_commit(repository):
    result = _transcribe(repository)
    record_path = repository / result["record_relative_path"]
    assert record_path.is_file()
    assert result["record_relative_path"].startswith(
        "records/session-handoffs/"
    )
    assert "-verdict-" in result["record_relative_path"]
    shown = _git(
        repository,
        "show",
        "--name-only",
        "--format=%H",
        "HEAD",
    ).stdout.splitlines()
    changed = [line for line in shown[1:] if line.strip()]
    assert changed == [result["record_relative_path"]]
    body = record_path.read_text(encoding="utf-8")
    assert "google" in body
    assert TEST_MODEL in body
    assert "Tier 1" in body
    assert "headless" in body
    assert "a" * 64 in body


def test_transcription_refuses_dirty_worktree(repository):
    record_module = _record_module()
    (repository / "records" / "dirty.md").write_text(
        "dirty\n", encoding="utf-8"
    )
    _git(repository, "add", "records/dirty.md")
    with pytest.raises(record_module.TranscriptionStop) as caught:
        _transcribe(repository)
    assert caught.value.reason == "worktree_not_clean"


def test_transcription_collision_stops(repository):
    record_module = _record_module()
    _transcribe(repository)
    with pytest.raises(record_module.TranscriptionStop) as caught:
        _transcribe(repository)
    assert caught.value.reason == "verdict_record_exists"


# ---- 事後照合4点（§7.3・§9-6） ----


def test_post_verification_passes_on_good_state(repository):
    record_module = _record_module()
    request = _request_relative(repository)
    target_commit = _git(
        repository, "rev-parse", "HEAD"
    ).stdout.strip()
    result = _transcribe(repository)
    verification = record_module.post_verify(
        repository=repository,
        request_relative_path=request,
        request_sha256=_sha256_file(repository / request),
        record_relative_path=result["record_relative_path"],
        target_commit=target_commit,
        raw_digest="a" * 64,
    )
    assert verification["status"] == "passed"
    assert verification["checks"] == [
        "freshness",
        "single_record_commit",
        "evidence",
        "schema_form",
    ]


def test_post_verification_detects_stale_request(repository):
    record_module = _record_module()
    request = _request_relative(repository)
    target_commit = _git(
        repository, "rev-parse", "HEAD"
    ).stdout.strip()
    result = _transcribe(repository)
    with pytest.raises(record_module.TranscriptionStop) as caught:
        record_module.post_verify(
            repository=repository,
            request_relative_path=request,
            request_sha256="f" * 64,
            record_relative_path=result["record_relative_path"],
            target_commit=target_commit,
            raw_digest="a" * 64,
        )
    assert caught.value.reason == "request_record_stale"


def test_post_verification_detects_multi_path_commit(repository):
    record_module = _record_module()
    request = _request_relative(repository)
    target_commit = _git(
        repository, "rev-parse", "HEAD"
    ).stdout.strip()
    result = _transcribe(repository)
    extra = repository / "records" / "extra.md"
    extra.write_text("extra\n", encoding="utf-8")
    _git(repository, "add", "records/extra.md")
    _git(
        repository,
        "commit",
        "--amend",
        "--no-edit",
        "-q",
    )
    with pytest.raises(record_module.TranscriptionStop) as caught:
        record_module.post_verify(
            repository=repository,
            request_relative_path=request,
            request_sha256=_sha256_file(repository / request),
            record_relative_path=result["record_relative_path"],
            target_commit=target_commit,
            raw_digest="a" * 64,
        )
    assert caught.value.reason == "verdict_commit_not_single"


def test_post_verification_detects_raw_digest_mismatch(repository):
    record_module = _record_module()
    request = _request_relative(repository)
    target_commit = _git(
        repository, "rev-parse", "HEAD"
    ).stdout.strip()
    result = _transcribe(repository)
    with pytest.raises(record_module.TranscriptionStop) as caught:
        record_module.post_verify(
            repository=repository,
            request_relative_path=request,
            request_sha256=_sha256_file(repository / request),
            record_relative_path=result["record_relative_path"],
            target_commit=target_commit,
            raw_digest="b" * 64,
        )
    assert caught.value.reason == "raw_digest_mismatch"


# ---- G30操作登録と入口（§9-7） ----


def test_g30_operation_registered():
    operations = _operations()
    definition = operations._OPERATIONS["reviewer_launch_prepare"]
    assert definition["input_names"] == ("request",)
    assert definition["binding_positions"] == {
        "request": ("request", "sha256"),
    }
    assert callable(definition["entry"])


def test_g30_prepare_outputs_binding(repository):
    entry = _entry()
    import io

    buffer = io.BytesIO()
    request = _request_relative(repository)
    exit_code = entry.g30_main(
        [
            "check",
            "--input-root",
            str(repository),
            "--request",
            request,
        ],
        output=buffer,
    )
    assert exit_code == 0
    payload = buffer.getvalue()
    assert payload.endswith(b"\n")
    result = json.loads(payload.decode("utf-8"))
    assert result["status"] == "ok"
    assert result["request"]["sha256"] == _sha256_file(
        repository / request
    )
    assert result["tier"] == 1
    assert isinstance(result["prompt_bytes"], int)


def test_entry_missing_arguments_exits_2():
    entry = _entry()
    import io

    buffer = io.BytesIO()
    exit_code = entry.main(["launch"], output=buffer)
    assert exit_code == 2
    result = json.loads(buffer.getvalue().decode("utf-8"))
    assert result["status"] == "stopped"


# ---- 契約012：claude-subagent backendとTier 2／3受容 ----

SUBAGENT_TEST_MODEL = "claude-test-model"


def _subagent_stream(model=SUBAGENT_TEST_MODEL, result_text=None, verdict=None):
    value = verdict if verdict is not None else _valid_verdict()
    text = (
        json.dumps(value, ensure_ascii=False)
        if result_text is None
        else result_text
    )
    lines = [
        json.dumps({"type": "system", "subtype": "init", "model": model}),
        json.dumps({"type": "result", "result": text}),
    ]
    return "\n".join(lines) + "\n"


def _launch_subagent(repository, monkeypatch, facade, **overrides):
    core = _core()
    for name in core.CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        core,
        "SUBAGENT_ALLOWED_RESPONSE_MODELS",
        (SUBAGENT_TEST_MODEL,),
        raising=True,
    )
    monkeypatch.setattr(core.subprocess, "run", facade.run, raising=True)
    request = _request_relative(repository)
    values = {
        "repository": repository,
        "request_relative_path": request,
        "expected_sha256": _sha256_file(repository / request),
        "private_root": repository.parent / "private",
        "backend_name": "claude-subagent",
        "run_id": "run-sub-001",
        "accept_tier": 3,
        "acceptance_ref": request,
    }
    values.update(overrides)
    return core.launch_review(**values)


def test_subagent_backend_registered():
    core = _core()
    backend = core.BACKENDS["claude-subagent"]
    assert backend["provider"] == "anthropic"
    assert backend["declared_tier"] == 3
    assert backend["read_tool_name"] == "Read"
    assert backend["executable"] == "claude"


def test_agy_backend_values_unchanged():
    core = _core()
    backend = core.BACKENDS["antigravity-cli"]
    assert backend["provider"] == "google"
    assert backend["executable"] == "agy"
    assert backend["read_tool_name"] == "view_file"
    assert backend["declared_tier"] == 1


def test_union_allowed_models_preserved():
    core = _core()
    assert core.SUBAGENT_ALLOWED_RESPONSE_MODELS == ("claude-opus-5",)
    assert core.ALLOWED_RESPONSE_MODELS == (
        "gemini-3.1-pro-high",
        "claude-opus-5",
    )


def test_subagent_without_acceptance_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch_subagent(
            repository,
            monkeypatch,
            facade,
            accept_tier=None,
            acceptance_ref=None,
        )
    assert caught.value.reason == "reviewer_not_independent_tier"
    assert facade.calls == []


def test_subagent_wrong_accept_tier_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch_subagent(repository, monkeypatch, facade, accept_tier=2)
    assert caught.value.reason == "reviewer_not_independent_tier"
    assert facade.calls == []


def test_subagent_acceptance_ref_missing_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    with pytest.raises(core.LaunchStop) as caught:
        _launch_subagent(
            repository,
            monkeypatch,
            facade,
            acceptance_ref="records/development/absent-acceptance.md",
        )
    assert caught.value.reason == "acceptance_reference_missing"
    assert facade.calls == []


def test_subagent_empty_allowed_models_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    for name in core.CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(core.subprocess, "run", facade.run, raising=True)
    monkeypatch.setattr(
        core, "SUBAGENT_ALLOWED_RESPONSE_MODELS", (), raising=True
    )
    request = _request_relative(repository)
    with pytest.raises(core.LaunchStop) as caught:
        core.launch_review(
            repository=repository,
            request_relative_path=request,
            expected_sha256=_sha256_file(repository / request),
            private_root=repository.parent / "private",
            backend_name="claude-subagent",
            run_id="run-sub-001",
            accept_tier=3,
            acceptance_ref=request,
        )
    assert caught.value.reason == "allowed_models_unfixed"
    assert facade.calls == []


def test_subagent_forbidden_env_stops(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder()
    for name in core.CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "secret")
    monkeypatch.setattr(
        core,
        "SUBAGENT_ALLOWED_RESPONSE_MODELS",
        (SUBAGENT_TEST_MODEL,),
        raising=True,
    )
    monkeypatch.setattr(core.subprocess, "run", facade.run, raising=True)
    request = _request_relative(repository)
    with pytest.raises(core.LaunchStop) as caught:
        core.launch_review(
            repository=repository,
            request_relative_path=request,
            expected_sha256=_sha256_file(repository / request),
            private_root=repository.parent / "private",
            backend_name="claude-subagent",
            run_id="run-sub-001",
            accept_tier=3,
            acceptance_ref=request,
        )
    assert caught.value.reason == "api_key_environment_forbidden"
    assert facade.calls == []


def test_subagent_forbidden_constant_equals_executor():
    core = _core()
    from tools.development.claude_implementation_executor import (
        FORBIDDEN_AUTH_ENVIRONMENT,
    )

    assert tuple(core.CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT) == tuple(
        FORBIDDEN_AUTH_ENVIRONMENT
    )


def test_subagent_arguments_fixed(clean_environment):
    core = _core()
    from tools.development.claude_implementation_executor import (
        DISALLOWED_TOOLS,
    )

    arguments = core.build_claude_arguments(
        "claude", "prompt-text", SUBAGENT_TEST_MODEL
    )
    assert arguments == [
        "claude",
        "--print",
        "--output-format",
        "stream-json",
        "--verbose",
        "--tools",
        "Read,Glob,Grep",
        "--allowedTools",
        "Read(/**)",
        "--disallowedTools",
        *DISALLOWED_TOOLS,
        "--permission-mode",
        "dontAsk",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--disable-slash-commands",
        "--no-chrome",
        "--model",
        SUBAGENT_TEST_MODEL,
        "prompt-text",
    ]
    tools_value = arguments[arguments.index("--tools") + 1]
    assert "Edit" not in tools_value
    assert "Write" not in tools_value
    assert "--dangerously-skip-permissions" not in arguments


def test_prompt_read_tool_insertion(repository):
    core = _core()
    request = _request_relative(repository)
    digest = _sha256_file(repository / request)
    prompt = core.build_prompt(
        str(repository), request, digest, read_tool_name="Read"
    )
    assert "Read" in prompt
    assert "view_file" not in prompt


def test_subagent_successful_launch_saves_and_returns(
    repository, monkeypatch, clean_environment
):
    facade = _FacadeRecorder(stdout=_subagent_stream())
    result = _launch_subagent(repository, monkeypatch, facade)
    assert result["status"] == "succeeded"
    assert result["tier"] == 3
    assert result["model"] == SUBAGENT_TEST_MODEL
    private_root = repository.parent / "private"
    raw_document = json.loads(
        (private_root / "run-sub-001" / "reviewer.raw.json").read_text(
            encoding="utf-8"
        )
    )
    assert raw_document["assignment"]["provider"] == "anthropic"
    launch_document = json.loads(
        (private_root / "run-sub-001" / "launch.json").read_text(
            encoding="utf-8"
        )
    )
    assert launch_document["tier"] == 3
    assert launch_document["accept_tier"] == 3
    assert launch_document["acceptance_reference"] == _request_relative(
        repository
    )


def test_subagent_fenced_result_extracted(
    repository, monkeypatch, clean_environment
):
    text = (
        "```json\n"
        + json.dumps(_valid_verdict(), ensure_ascii=False)
        + "\n```"
    )
    facade = _FacadeRecorder(stdout=_subagent_stream(result_text=text))
    result = _launch_subagent(
        repository, monkeypatch, facade, run_id="run-sub-002"
    )
    assert result["status"] == "succeeded"


def test_subagent_disallowed_model_stops_after_raw_saved(
    repository, monkeypatch, clean_environment
):
    core = _core()
    facade = _FacadeRecorder(stdout=_subagent_stream(model="other-model"))
    with pytest.raises(core.LaunchStop) as caught:
        _launch_subagent(
            repository, monkeypatch, facade, run_id="run-sub-003"
        )
    assert caught.value.reason == "response_model_not_allowed"
    raw_path = (
        repository.parent / "private" / "run-sub-003" / "reviewer.raw.json"
    )
    assert raw_path.is_file()


def test_g30_prepare_backend_optional(repository):
    entry = _entry()
    import io

    buffer = io.BytesIO()
    request = _request_relative(repository)
    exit_code = entry.g30_main(
        [
            "check",
            "--input-root",
            str(repository),
            "--request",
            request,
            "--backend",
            "claude-subagent",
        ],
        output=buffer,
    )
    assert exit_code == 0
    result = json.loads(buffer.getvalue().decode("utf-8"))
    assert result["backend"] == "claude-subagent"
    assert result["tier"] == 3


def test_entry_launch_acceptance_ref_missing(repository, monkeypatch):
    entry = _entry()
    core = _core()
    import io

    for name in core.CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        core,
        "SUBAGENT_ALLOWED_RESPONSE_MODELS",
        (SUBAGENT_TEST_MODEL,),
        raising=True,
    )
    buffer = io.BytesIO()
    request = _request_relative(repository)
    exit_code = entry.main(
        [
            "launch",
            "--repository",
            str(repository),
            "--request",
            request,
            "--expected-sha256",
            _sha256_file(repository / request),
            "--private-root",
            str(repository.parent / "private"),
            "--run-id",
            "run-sub-004",
            "--backend",
            "claude-subagent",
            "--accept-tier",
            "3",
            "--acceptance-ref",
            "records/development/absent-acceptance.md",
        ],
        output=buffer,
    )
    assert exit_code == 2
    result = json.loads(buffer.getvalue().decode("utf-8"))
    assert result["reason"] == "acceptance_reference_missing"
