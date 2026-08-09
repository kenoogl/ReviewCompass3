"""V4 Issue resolve tool（deferred #1・案B）の受入テスト。

範囲固定：records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v2.md
Human裁定（2026-08-10）：risk high確定・案B（in-place遷移＋解決record）・遷移元registeredのみ

固定するのは、(1)registeredのissueだけをresolved／rejectedへin-place遷移できること
（file名・issue_version不変、変更はstateとcontent_digestのみ）、(2)解決recordの
new-only作成、(3)遷移後の台帳が正規検証（record＋repository）に合格すること、
(4)非Human裁定・stale・遷移元違反・path逸脱・記録衝突のfail-closedと無変更保証。

fixtureは既存intake testの正規生成経路（実configの読み取り専用利用・候補bundleの
tmp複製・正規裁定→issue生成）を再利用し、実workflow台帳へは一切触れない。
"""

import hashlib
import importlib
import json
import shutil
from pathlib import Path

import pytest

import test_issue_intake_v4 as intake_fixtures


PROJECT_ROOT = Path(__file__).parents[1]
CONFIG_V4 = PROJECT_ROOT / "config/development-issue-resolution-pilot-v4.json"
BUNDLE = intake_fixtures.BUNDLE
CANDIDATE_A = intake_fixtures.SESSION_POLICY_CANDIDATE
ISSUE_A = intake_fixtures.SESSION_POLICY_ISSUE_ID
CANDIDATE_B = "HTC-66C3E6CA"
ISSUE_B = "ISSUE-HTC-66C3E6CA"
RECORD_PATH = "records/development/2026-08-10-v4-issue-resolution-fixture-v1.json"


def _module():
    return importlib.import_module("tools.development.issue_resolution_v4")


@pytest.fixture
def intake():
    return importlib.import_module("tools.development.issue_intake_v4")


@pytest.fixture
def config(intake):
    return intake.load_config(CONFIG_V4)


@pytest.fixture
def workspace(tmp_path, config):
    """候補bundleだけを写した作業用project root。実repositoryは触らない。"""

    root = tmp_path / "project"
    (root / BUNDLE).parent.mkdir(parents=True)
    shutil.copy2(PROJECT_ROOT / BUNDLE, root / BUNDLE)
    for key in ("human_triage_decision_v2", "issue_record_v2"):
        (root / config["directories"][key]).mkdir(parents=True)
    return root


def _registered_issue(
    intake,
    config,
    workspace,
    *,
    candidate_id=CANDIDATE_A,
    issue_id=ISSUE_A,
):
    decision = intake_fixtures._approving_decision(
        intake,
        config,
        workspace,
        candidate_id=candidate_id,
        issue_id=issue_id,
    )
    candidate = intake_fixtures._bundle_candidate(
        json.loads((workspace / BUNDLE).read_text(encoding="utf-8")),
        candidate_id,
    )
    issue = intake.build_v4_issue_record(
        candidate=candidate,
        decision=decision,
        project_root=workspace,
        config=config,
        created_at=intake_fixtures.CREATED_AT,
        problem="合成fixtureの追跡対象問題。",
        decisions=[decision],
    )
    path = intake.v4_issue_path(issue, config=config)
    intake_fixtures._write_json(workspace, path, issue)
    return path, issue


def _force_state(intake, workspace, issue_path, state):
    """fixture専用：issueのstateを書き換えdigestを正しく再計算する。"""

    file = workspace / issue_path
    document = json.loads(file.read_text(encoding="utf-8"))
    document["state"] = state
    document.pop("content_digest")
    document["content_digest"] = intake.canonical_digest(document)
    intake_fixtures._write_json(workspace, issue_path, document)
    return document


def _ruling(workspace, text="解決を承認する。"):
    relative = "records/development/2026-08-10-resolution-ruling-fixture.md"
    file = workspace / relative
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text, encoding="utf-8")
    return relative, hashlib.sha256(file.read_bytes()).hexdigest()


def _evidence(workspace, name="2026-08-10-resolution-evidence-fixture.md"):
    relative = "records/development/" + name
    file = workspace / relative
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("解決のEvidence本文。\n", encoding="utf-8")
    return "%s=%s" % (relative, hashlib.sha256(file.read_bytes()).hexdigest())


def _run(
    module,
    capsys,
    workspace,
    issue_path,
    *,
    to="resolved",
    ruling,
    ruling_sha,
    evidence,
    record_path=RECORD_PATH,
    human_id="kenoogl",
    decided_at="2026-08-10T12:00:00+09:00",
):
    arguments = [
        "--config",
        str(CONFIG_V4),
        "--project-root",
        str(workspace),
        "--issue",
        issue_path,
        "--to",
        to,
        "--human-id",
        human_id,
        "--decided-at",
        decided_at,
        "--ruling",
        ruling,
        "--ruling-sha256",
        ruling_sha,
        "--resolution-record",
        record_path,
    ]
    for item in evidence:
        arguments.extend(["--evidence", item])
    exit_code = module.run(tuple(arguments))
    payload = json.loads(capsys.readouterr().out)
    return exit_code, payload


def test_registered_issue_resolves_in_place(intake, config, workspace, capsys):
    """正例1・境界11：registered→resolvedのin-place遷移と解決record作成。"""

    module = _module()
    issue_path, before = _registered_issue(intake, config, workspace)
    before_bytes = (workspace / issue_path).read_bytes()
    ruling, ruling_sha = _ruling(workspace)
    evidence = _evidence(workspace)

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
    )

    assert exit_code == 0
    assert payload["status"] == "ok"
    after = json.loads((workspace / issue_path).read_text(encoding="utf-8"))
    assert after["state"] == "resolved"
    assert after["issue_version"] == before["issue_version"]
    assert after["content_digest"] == intake.canonical_digest(after)
    assert after["content_digest"] != before["content_digest"]
    unchanged = {
        key: value
        for key, value in after.items()
        if key not in ("state", "content_digest")
    }
    assert unchanged == {
        key: value
        for key, value in before.items()
        if key not in ("state", "content_digest")
    }
    assert (workspace / issue_path).read_bytes() != before_bytes

    record = json.loads((workspace / RECORD_PATH).read_text(encoding="utf-8"))
    assert record["issue"]["issue_id"] == ISSUE_A
    assert record["issue"]["path"] == issue_path
    assert record["issue"]["content_digest_before"] == before["content_digest"]
    assert record["issue"]["content_digest_after"] == after["content_digest"]
    assert record["transition"] == {"from": "registered", "to": "resolved"}
    assert record["human"]["human_id"] == "kenoogl"
    assert record["human"]["ruling"]["path"] == ruling
    assert record["human"]["ruling"]["sha256"] == ruling_sha
    assert len(record["evidence"]) == 1


def test_registered_issue_can_be_rejected(intake, config, workspace, capsys):
    """正例2：rejectedへの遷移も同様に成立する。"""

    module = _module()
    issue_path, _before = _registered_issue(intake, config, workspace)
    ruling, ruling_sha = _ruling(workspace, "却下を裁定する。")
    evidence = _evidence(workspace)

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        to="rejected",
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
    )

    assert exit_code == 0
    assert payload["status"] == "ok"
    after = json.loads((workspace / issue_path).read_text(encoding="utf-8"))
    assert after["state"] == "rejected"


def test_ledger_passes_canonical_validation_and_others_unchanged(
    intake, config, workspace, capsys
):
    """正例3・境界10：正規検証（record＋repository）合格と他record bytes不変。"""

    module = _module()
    issue_path, _issue_a = _registered_issue(intake, config, workspace)
    other_path, _issue_b = _registered_issue(
        intake,
        config,
        workspace,
        candidate_id=CANDIDATE_B,
        issue_id=ISSUE_B,
    )
    other_bytes = (workspace / other_path).read_bytes()
    ruling, ruling_sha = _ruling(workspace)
    evidence = _evidence(workspace)

    exit_code, _payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
    )

    assert exit_code == 0
    assert (workspace / other_path).read_bytes() == other_bytes
    after = json.loads((workspace / issue_path).read_text(encoding="utf-8"))
    assert intake.validate_v4_issue_record(
        after, path=issue_path, project_root=workspace, config=config
    ) is True
    effective = intake.validate_v4_issue_repository(
        project_root=workspace, config=config
    )
    assert CANDIDATE_A not in effective
    assert CANDIDATE_B in effective


@pytest.mark.parametrize("source_state", ("in_progress", "resolved", "rejected"))
def test_rejects_sources_other_than_registered(
    intake, config, workspace, capsys, source_state
):
    """負例4：遷移元がregistered以外（二重解決を含む）を拒否し、無変更を保つ。"""

    module = _module()
    issue_path, _before = _registered_issue(intake, config, workspace)
    _force_state(intake, workspace, issue_path, source_state)
    frozen = (workspace / issue_path).read_bytes()
    ruling, ruling_sha = _ruling(workspace)
    evidence = _evidence(workspace)

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
    )

    assert exit_code == 5
    assert payload["reason"] == "issue_state_not_registered"
    assert (workspace / issue_path).read_bytes() == frozen
    assert not (workspace / RECORD_PATH).exists()


@pytest.mark.parametrize("ruling_case", ("missing", "sha_mismatch"))
def test_rejects_non_human_ruling(intake, config, workspace, capsys, ruling_case):
    """負例5：非Human裁定（裁定record不読・SHA不一致）を拒否し、無変更を保つ。"""

    module = _module()
    issue_path, _before = _registered_issue(intake, config, workspace)
    frozen = (workspace / issue_path).read_bytes()
    if ruling_case == "missing":
        ruling = "records/development/absent-ruling.md"
        ruling_sha = "a" * 64
    else:
        ruling, _real = _ruling(workspace)
        ruling_sha = "b" * 64
    evidence = _evidence(workspace)

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
    )

    assert exit_code == 5
    assert payload["reason"] == "human_ruling_invalid"
    assert (workspace / issue_path).read_bytes() == frozen
    assert not (workspace / RECORD_PATH).exists()


def test_rejects_stale_issue_record(intake, config, workspace, capsys):
    """負例6：content_digest不一致（改竄・stale）の拒否と無変更。"""

    module = _module()
    issue_path, _before = _registered_issue(intake, config, workspace)
    file = workspace / issue_path
    document = json.loads(file.read_text(encoding="utf-8"))
    document["problem"] = "改竄された本文。"
    intake_fixtures._write_json(workspace, issue_path, document)
    frozen = file.read_bytes()
    ruling, ruling_sha = _ruling(workspace)
    evidence = _evidence(workspace)

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
    )

    assert exit_code == 5
    assert payload["reason"] == "issue_record_invalid"
    assert file.read_bytes() == frozen
    assert not (workspace / RECORD_PATH).exists()


@pytest.mark.parametrize("invalid_case", (
    "unknown_target",
    "evidence_escape",
    "evidence_sha_mismatch",
    "evidence_empty",
))
def test_rejects_invalid_targets_and_evidence(
    intake, config, workspace, capsys, invalid_case
):
    """負例7：未知の遷移先・Evidence逸脱・SHA不一致・空Evidenceの拒否。"""

    module = _module()
    issue_path, _before = _registered_issue(intake, config, workspace)
    frozen = (workspace / issue_path).read_bytes()
    ruling, ruling_sha = _ruling(workspace)
    to = "resolved"
    evidence = [_evidence(workspace)]
    if invalid_case == "unknown_target":
        to = "closed"
        expected = "target_state_invalid"
    elif invalid_case == "evidence_escape":
        evidence = ["../outside.md=%s" % ("c" * 64)]
        expected = "evidence_invalid"
    elif invalid_case == "evidence_sha_mismatch":
        relative = evidence[0].split("=")[0]
        evidence = ["%s=%s" % (relative, "d" * 64)]
        expected = "evidence_invalid"
    else:
        evidence = []
        expected = "evidence_invalid"

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        to=to,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=evidence,
    )

    assert exit_code == 5
    assert payload["reason"] == expected
    assert (workspace / issue_path).read_bytes() == frozen
    assert not (workspace / RECORD_PATH).exists()


@pytest.mark.parametrize("record_case", ("conflict", "outside_records"))
def test_rejects_bad_resolution_record_paths(
    intake, config, workspace, capsys, record_case
):
    """負例8：解決recordの既存衝突（new-only）と置き場所逸脱の拒否。"""

    module = _module()
    issue_path, _before = _registered_issue(intake, config, workspace)
    frozen = (workspace / issue_path).read_bytes()
    ruling, ruling_sha = _ruling(workspace)
    evidence = _evidence(workspace)
    record_path = RECORD_PATH
    if record_case == "conflict":
        existing = workspace / RECORD_PATH
        existing.parent.mkdir(parents=True, exist_ok=True)
        existing.write_text("既存record。\n", encoding="utf-8")
        existing_bytes = existing.read_bytes()
        expected = "resolution_record_conflict"
    else:
        record_path = "tools/misplaced-resolution.json"
        expected = "resolution_record_path_invalid"

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
        record_path=record_path,
    )

    assert exit_code == 5
    assert payload["reason"] == expected
    assert (workspace / issue_path).read_bytes() == frozen
    if record_case == "conflict":
        assert (workspace / RECORD_PATH).read_bytes() == existing_bytes
    else:
        assert not (workspace / record_path).exists()


def test_post_validation_failure_restores_everything(
    intake, config, workspace, capsys
):
    """負例9：事後の正規検証失敗時、issue bytesを完全復元しrecordも残さない。"""

    module = _module()
    issue_path, _before = _registered_issue(intake, config, workspace)
    frozen = (workspace / issue_path).read_bytes()
    ledger = workspace / config["directories"]["issue_record_v2"]
    corrupt = ledger / "issue-broken--v1.json"
    corrupt.write_text("{broken json", encoding="utf-8")
    ruling, ruling_sha = _ruling(workspace)
    evidence = _evidence(workspace)

    exit_code, payload = _run(
        module,
        capsys,
        workspace,
        issue_path,
        ruling=ruling,
        ruling_sha=ruling_sha,
        evidence=[evidence],
    )

    assert exit_code == 5
    assert payload["reason"] == "post_validation_failed"
    assert (workspace / issue_path).read_bytes() == frozen
    assert not (workspace / RECORD_PATH).exists()
