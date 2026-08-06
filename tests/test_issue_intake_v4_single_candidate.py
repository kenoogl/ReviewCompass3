"""Issue Intake V4 単体候補参照と候補全件検証の受入test（規範宣言N1〜N12）。

正本設計：docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md
（`approved`、2026-08-06 Human承認済み）

N5・N6は既存test 2件（tests/test_issue_intake_v4.py の
`test_k7_repository_decision_set_has_no_conflict`と
`test_l6_repository_issue_set_is_consistent`）の条件変更で固定する。
本fileはそれ以外のN1〜N4、N7〜N12を固定する。各testのdocstringに、
いま失敗するRED testか、いま成功する境界例（回帰防止）かを明記する。
"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_V4 = PROJECT_ROOT / "config/development-issue-resolution-pilot-v4.json"
CONFIG_V2 = PROJECT_ROOT / "config/development-issue-resolution-pilot-v2.json"
CONFIG_V3 = PROJECT_ROOT / "config/development-issue-resolution-pilot-v3.json"

BUNDLE = "records/development/2026-08-05-historical-todo-intake-candidates-v1.json"
BUNDLE_SHA = "e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e"

# 実在の単体候補record（Human仕分け判断の対象）。
# records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md §1に固定済み。
CANDIDATE_PATH = (
    ".reviewcompass/workflow/improvement-candidates/"
    "ic-authority-reference-digest-check-001--v1.json"
)
CANDIDATE_SHA256 = (
    "d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6"
)
CANDIDATE_CONTENT_DIGEST = (
    "760d9ef9811e6d95c9af406a6664e0e2ef5df9c33e32aa6ebbc33721c931753f"
)
CANDIDATE_ID = "IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001"
DECISION_ID = "DEC-IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001"
ISSUE_ID = "ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001"

DECISION_FILE = (
    ".reviewcompass/workflow/triage-decisions-v4/"
    "dec-ic-authority-reference-digest-check-001--v1.json"
)
ISSUE_FILE = (
    ".reviewcompass/workflow/issues-v4/"
    "issue-authority-reference-digest-check-001--v1.json"
)

CANDIDATE_DIRECTORY = ".reviewcompass/workflow/improvement-candidates"
ALLOWLIST_NAME = "historical-allowlist-v1.json"
ALLOWLIST_PATH = f"{CANDIDATE_DIRECTORY}/{ALLOWLIST_NAME}"
HISTORICAL_CANDIDATE_NAME = "ic-historical-todo-issue-intake-001--v1.json"


@pytest.fixture
def intake():
    return importlib.import_module("tools.development.issue_intake_v4")


@pytest.fixture
def pilot():
    return importlib.import_module("tools.development.issue_resolution_pilot")


@pytest.fixture
def config(intake):
    return intake.load_config(CONFIG_V4)


def _single_candidate_ref():
    """N1の単体形式candidate_ref（4 key厳密一致）を組み立てる。"""

    return {
        "record_path": CANDIDATE_PATH,
        "record_sha256": CANDIDATE_SHA256,
        "candidate_id": CANDIDATE_ID,
        "candidate_content_digest": CANDIDATE_CONTENT_DIGEST,
    }


def _single_form_decision(intake, **overrides):
    """単体形式candidate_refを持つ有効なdecision dictを組み立てる。

    `build_human_triage_decision`はbundle path前提で単体形式に未対応のため、
    dictを直接書く。値はMarkdown裁定
    `records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`
    §3を基礎とし、昇格だけを提案N10のHuman承認（「載せてよい」）で承認側とした。
    """

    document = {
        "record_kind": "human_triage_decision",
        "schema_version": 2,
        "decision_id": DECISION_ID,
        "decision_version": 1,
        "decided_at": "2026-08-06T13:33:25+09:00",
        "decision_maker": "human",
        "candidate_ref": _single_candidate_ref(),
        "human_fields": {
            "unresolved": True,
            "recurrence": True,
            "impact": "medium",
            "priority": "low",
            "promote_to_issue": True,
        },
        "disposition": "issue_resolution",
        "blocking": False,
        "rationale": (
            "参照Digestのずれは実際に発生し修復済みで、再発の経緯も測定済みである。"
            "正式Issueとして登録し追跡する。"
        ),
        "next_action": "課題recordを登録のみ行う。着手はHuman判断まで開始しない。",
        "supersedes": None,
        "issue_promotion": {"approved": True, "issue_id": ISSUE_ID},
    }
    document.update(overrides)
    document["content_digest"] = intake.canonical_digest(document)
    return document


def _rehashed(intake, decision, **changes):
    updated = dict(decision)
    updated.update(changes)
    updated["content_digest"] = intake.canonical_digest(updated)
    return updated


def _record_files(pilot, configs, path):
    """候補recordがv2またはv3 configのvalidatorに合格するかを返す。"""

    for legacy_config in configs:
        try:
            pilot.validate_record_file(
                path, project_root=PROJECT_ROOT, config=legacy_config
            )
            return True
        except pilot.PilotValidationError:
            continue
    return False


# ------------------------------------------------- (a) 単体候補参照 N1・N2・N4


def test_n1_single_form_candidate_ref_decision_validates(intake, config):
    """N1（RED）：単体形式candidate_refを持つ有効decisionが合格する。

    現状は`validate_human_triage_decision`がcandidate_refのkey集合を
    bundle形式の5 keyに厳密固定しているため、実在候補
    `ic-authority-reference-digest-check-001--v1.json`を指す正しい単体形式でも
    拒否される。実装後は合格することを固定する。
    """

    decision = _single_form_decision(intake)
    path = intake.human_triage_decision_path(decision, config=config)
    assert path == (
        config["directories"]["human_triage_decision_v2"]
        + "/dec-ic-authority-reference-digest-check-001--v1.json"
    )
    assert intake.validate_human_triage_decision(
        decision, path=path, project_root=PROJECT_ROOT, config=config
    ) is True


def test_n1_candidate_ref_key_set_deviations_are_rejected(intake, config):
    """N1負例（境界、いま成功）：keyの過不足・両形式の混在は拒否される。

    現状もkey集合の厳密一致検査で拒否され、実装後も
    「key集合で形式を判別し、過不足・混在は拒否する」（N1）により
    拒否され続けることを固定する回帰防止testである。
    """

    decision = _single_form_decision(intake)
    path = intake.human_triage_decision_path(decision, config=config)
    single = _single_candidate_ref()
    bundle_style = {
        "bundle_path": BUNDLE,
        "bundle_sha256": BUNDLE_SHA,
        "bundle_schema_version": 1,
        "candidate_id": CANDIDATE_ID,
        "candidate_content_digest": CANDIDATE_CONTENT_DIGEST,
    }
    deficient = {
        key: value
        for key, value in single.items()
        if key != "candidate_content_digest"
    }
    variants = (
        deficient,
        dict(single, bundle_path=BUNDLE),
        dict(bundle_style, record_path=CANDIDATE_PATH),
        {**bundle_style, **single},
    )
    for candidate_ref in variants:
        broken = _rehashed(intake, decision, candidate_ref=candidate_ref)
        with pytest.raises(intake.IntakeError) as error:
            intake.validate_human_triage_decision(
                broken, path=path, project_root=PROJECT_ROOT, config=config
            )
        assert error.value.code == "human_triage_decision_field_unknown"


def test_n2_single_form_fingerprint_mismatches_are_rejected(intake, config):
    """N2（RED、happy path依存）：単体形式の指紋不一致はfail-closedで拒否される。

    現状は単体形式そのものが拒否されるため、まず正しいdictの合格を確認する
    （この最初のassertionが現状の失敗点である）。実装後は、合格するdictを
    1点だけ壊したrecord_sha256不一致・candidate_id不一致・content_digest不一致の
    それぞれが、正しい理由（IntakeError）で拒否されることを固定する。
    """

    decision = _single_form_decision(intake)
    path = intake.human_triage_decision_path(decision, config=config)
    assert intake.validate_human_triage_decision(
        decision, path=path, project_root=PROJECT_ROOT, config=config
    ) is True

    stale_file = _rehashed(
        intake,
        decision,
        candidate_ref=dict(_single_candidate_ref(), record_sha256="0" * 64),
    )
    with pytest.raises(intake.IntakeError):
        intake.validate_human_triage_decision(
            stale_file, path=path, project_root=PROJECT_ROOT, config=config
        )

    # candidate_id不一致：decision IDと参照candidate_idの束縛（N4）を保ったまま、
    # 参照先fileの実内容と食い違うcandidate_idを指す。
    mismatched_id = _rehashed(
        intake,
        decision,
        decision_id="DEC-IC-PILOT-TODO-GROWTH-001",
        candidate_ref=dict(
            _single_candidate_ref(), candidate_id="IC-PILOT-TODO-GROWTH-001"
        ),
    )
    with pytest.raises(intake.IntakeError):
        intake.validate_human_triage_decision(
            mismatched_id,
            path=intake.human_triage_decision_path(mismatched_id, config=config),
            project_root=PROJECT_ROOT,
            config=config,
        )

    stale_content = _rehashed(
        intake,
        decision,
        candidate_ref=dict(
            _single_candidate_ref(), candidate_content_digest="0" * 64
        ),
    )
    with pytest.raises(intake.IntakeError):
        intake.validate_human_triage_decision(
            stale_content, path=path, project_root=PROJECT_ROOT, config=config
        )


def test_n4_single_form_decision_id_must_be_bound_to_the_candidate(intake, config):
    """N4（RED）：単体形式でもdecision IDは`DEC-<candidate_id>`規則に従う。

    現状は単体形式のcandidate_refがkey集合検査で先に拒否されるため、
    誤りの理由が`human_triage_decision_field_unknown`になる。実装後は
    ID束縛の検査に到達し、`human_triage_decision_identity_invalid`で
    拒否されることを固定する。
    """

    renamed = _single_form_decision(intake, decision_id="DEC-OTHER-TOPIC-001")
    path = intake.human_triage_decision_path(renamed, config=config)
    with pytest.raises(intake.IntakeError) as error:
        intake.validate_human_triage_decision(
            renamed, path=path, project_root=PROJECT_ROOT, config=config
        )
    assert error.value.code == "human_triage_decision_identity_invalid"


# ------------------------------------------------- (a) 既存decisionの保護 N3


def test_n3_existing_bundle_form_decisions_keep_validating(intake, config):
    """N3（境界、いま成功）：既存41 decisionのbundle形式は変更なしで合格し続ける。

    単体形式decisionが将来追加されても壊れないよう、bundle形式
    （candidate_refに`record_path` keyを持たないもの）だけを数えて41件を固定する。
    """

    effective = intake.validate_triage_decision_repository(
        project_root=PROJECT_ROOT, config=config
    )
    bundle_form = {
        candidate_id: decision
        for candidate_id, decision in effective.items()
        if "record_path" not in decision["candidate_ref"]
    }
    assert len(bundle_form) == 41
    for candidate_id, decision in bundle_form.items():
        assert decision["candidate_ref"]["candidate_id"] == candidate_id
        assert decision["candidate_ref"]["bundle_path"] == BUNDLE
        assert decision["candidate_ref"]["bundle_sha256"] == BUNDLE_SHA
        assert decision["decision_maker"] == "human"


# --------------------------------------------- (c) 候補置き場の全件検証 N7〜N9


def test_n7_all_candidate_records_validate_or_are_allowlisted(pilot):
    """N7（RED）：候補置き場の全JSONは、validator合格またはallowlist宣言を要する。

    `.reviewcompass/workflow/improvement-candidates/`の全JSON record
    （歴史allowlist file自身を除く）が、(a) v2またはv3 configの
    `validate_record_file`に合格する、または (b) 歴史allowlist file
    `historical-allowlist-v1.json`に載っている、のどちらかであることを固定する。
    現状はallowlistが未作成で、`ic-historical-todo-issue-intake-001--v1.json`が
    どちらの条件も満たさないため失敗する。
    """

    configs = (pilot.load_config(CONFIG_V2), pilot.load_config(CONFIG_V3))
    directory = PROJECT_ROOT / CANDIDATE_DIRECTORY
    allowlist_file = PROJECT_ROOT / ALLOWLIST_PATH
    allowed_names = set()
    if allowlist_file.is_file():
        allowlist = json.loads(allowlist_file.read_text(encoding="utf-8"))
        allowed_names = {
            Path(entry["path"]).name for entry in allowlist["entries"]
        }
    unaccounted = []
    for path in sorted(directory.glob("*.json")):
        if path.name == ALLOWLIST_NAME:
            continue
        if _record_files(pilot, configs, path):
            continue
        if path.name in allowed_names:
            continue
        unaccounted.append(path.name)
    assert unaccounted == []


def test_n8_historical_allowlist_declares_the_single_seed_entry(intake):
    """N8（RED）：歴史allowlistは機械可読で、初期entryは歴史候補1件だけである。

    allowlist file `historical-allowlist-v1.json`が存在し、各entryが
    `path`・`reason`・`successor_ref`を持ち、初期entryが
    `ic-historical-todo-issue-intake-001--v1.json`の1件であることを固定する。
    現状はfileが未作成のため失敗する。
    """

    allowlist_file = PROJECT_ROOT / ALLOWLIST_PATH
    assert allowlist_file.is_file()
    allowlist = json.loads(allowlist_file.read_text(encoding="utf-8"))
    entries = allowlist["entries"]
    assert isinstance(entries, list)
    assert len(entries) == 1
    for entry in entries:
        for field in ("path", "reason", "successor_ref"):
            assert field in entry
            assert entry[field]
    assert Path(entries[0]["path"]).name == HISTORICAL_CANDIDATE_NAME
    assert (
        PROJECT_ROOT / CANDIDATE_DIRECTORY / HISTORICAL_CANDIDATE_NAME
    ).is_file()


def test_n9_authority_reference_candidate_passes_the_v3_validator(pilot):
    """N9（境界、いま成功）：対象候補はv3 configのvalidatorで合格し続ける。

    `ic-authority-reference-digest-check-001--v1.json`の実bytesと
    content_digestが固定値のまま、v3 validatorに合格することを固定する
    回帰防止testである。
    """

    config = pilot.load_config(CONFIG_V3)
    candidate_file = PROJECT_ROOT / CANDIDATE_PATH
    assert (
        hashlib.sha256(candidate_file.read_bytes()).hexdigest() == CANDIDATE_SHA256
    )
    result = pilot.validate_record_file(
        candidate_file, project_root=PROJECT_ROOT, config=config
    )
    assert result.record_kind == "improvement_candidate"
    assert result.record_id == CANDIDATE_ID
    assert result.content_digest == CANDIDATE_CONTENT_DIGEST


# ------------------------------- (d) 仕分け判断の機械可読化と課題登録 N10〜N12


def test_n10_machine_readable_decision_record_is_persisted(intake, config):
    """N10（RED）：Human仕分け判断が単体形式でV4レーンへ機械可読に置かれている。

    `triage-decisions-v4/dec-ic-authority-reference-digest-check-001--v1.json`が
    存在し、`validate_human_triage_decision`に合格し、Markdown裁定§3を基礎に
    昇格だけをHuman承認（「載せてよい」）で承認側へ更新した値を持つことを
    固定する。現状はfileが未作成のため失敗する。
    """

    decision_file = PROJECT_ROOT / DECISION_FILE
    assert decision_file.is_file()
    record = json.loads(decision_file.read_text(encoding="utf-8"))
    assert intake.validate_human_triage_decision(
        record, path=DECISION_FILE, project_root=PROJECT_ROOT, config=config
    ) is True
    assert record["decision_id"] == DECISION_ID
    assert record["decision_version"] == 1
    assert record["decision_maker"] == "human"
    assert record["candidate_ref"] == _single_candidate_ref()
    assert record["disposition"] == "issue_resolution"
    assert record["blocking"] is False
    assert record["human_fields"]["unresolved"] is True
    assert record["human_fields"]["recurrence"] is True
    assert record["human_fields"]["impact"] == "medium"
    assert record["human_fields"]["priority"] == "low"
    assert record["human_fields"]["promote_to_issue"] is True
    assert record["issue_promotion"] == {"approved": True, "issue_id": ISSUE_ID}


def test_n11_every_bundle_candidate_has_an_effective_decision(intake, config):
    """N11（境界、いま成功）：bundle内41候補すべてに有効decisionが存在する。

    閉鎖Evidenceの「未判断0件」を、以後は機械が維持する。単体形式decisionが
    将来追加されても壊れないよう、bundle候補ID集合が有効decisionのkey集合に
    含まれること（部分集合）を固定する。
    """

    decisions = intake.load_triage_decisions(project_root=PROJECT_ROOT, config=config)
    effective = intake.resolve_effective_triage_decisions(decisions)
    bundle = json.loads((PROJECT_ROOT / BUNDLE).read_text(encoding="utf-8"))
    bundle_ids = {item["candidate_id"] for item in bundle["candidates"]}
    assert len(bundle_ids) == 41
    undecided = sorted(bundle_ids - set(effective))
    assert undecided == []


def test_n12_issue_is_registered_and_nothing_is_in_progress(intake, config):
    """N12（RED）：課題recordが`registered`で登録され、着手は0件のままである。

    `issues-v4/issue-authority-reference-digest-check-001--v1.json`が存在し、
    `validate_v4_issue_record`に合格し、`state: registered`であること、かつ
    `in_progress`のIssueが0件のままであることを固定する。
    現状はfileが未作成のため失敗する。
    """

    issue_file = PROJECT_ROOT / ISSUE_FILE
    assert issue_file.is_file()
    record = json.loads(issue_file.read_text(encoding="utf-8"))
    assert intake.validate_v4_issue_record(
        record, path=ISSUE_FILE, project_root=PROJECT_ROOT, config=config
    ) is True
    assert record["issue_id"] == ISSUE_ID
    assert record["issue_version"] == 1
    assert record["state"] == "registered"
    assert record["candidate_ref"]["candidate_id"] == CANDIDATE_ID
    issues = intake.load_v4_issues(project_root=PROJECT_ROOT, config=config)
    assert any(item["issue_id"] == ISSUE_ID for item in issues)
    assert intake.count_active_issues(issues) == 0
