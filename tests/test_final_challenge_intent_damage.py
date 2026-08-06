"""Final Challenge 意図毀損検出（CL-6A-10）の規範宣言P1〜P7を固定するtest。

正本設計：docs/design/2026-08-06-final-challenge-intent-damage-proposal.md
（状態`approved`、2026-08-06、Human文言「承認」。§7の3点すべてを承認）

REDと境界例を混在させる。各testのdocstringにどちらかとP対応を明記する。
fixtureは既存E2E test（tests/test_first_review_task_contract_e2e.py）のhelperを
再利用する（前例：tests/test_work6a_coverage_boundaries.py）。

本fileが事実上の契約として固定する最小語彙（提案§3の語に忠実）：

- finding単位の種別field `kind`：`contract`（契約適合性）／`intent_damage`（上位意図毀損）。
  省略時は`contract`（後方互換、P1）。runtime定数`FINDING_KINDS`で閉じる。
- finding単位の発生元field `origin`：`{"route": <route種>, "identity": <str>}`。
  route種は`deterministic_stub`／`subagent`／`external_api`／`human`（P1・P7）。
  runtime定数`FINDING_ORIGIN_ROUTES`で閉じる。
- finding単位のHuman採否field `human_ruling`：`accepted`／`rejected`／`pending`。
  `intent_damage`で省略時は未了（pending）として扱う（P4のfail-closed）。
  rejectの理由は`human_ruling_reason`に残す（P6）。
- blockingの表現はseverity `error`とする（新fieldを足さない。severity語彙は
  既存の`error`＝停止相当を再利用する。提案§2の「意図毀損をerrorで表すと
  Conformance段で落ちる」問題は、P2の種別分離で解消される前提である）。

LLMは呼ばない。所見は固定fixtureとして差し込む（提案§1・§6）。
"""

import importlib

import pytest

import test_first_review_task_contract_e2e as contract_e2e

from tools.task_contract.identity import seal


INTENT_RULE_ID = "INTENT-DAMAGE-REVIEW"
INTENT_REQUIREMENT = "REQ-CONTRACT-004"
INTENT_DESCRIPTION = "成果はContract適合だが、上位Intentの目的を損なっている。"


@pytest.fixture
def runtime():
    return importlib.import_module("tools.task_contract")


def _base(runtime, tmp_path, *, body=contract_e2e.CLEAN_DOCUMENT):
    """既存E2E helperでchainを組み、stub finding_setまで進める。"""

    chain = contract_e2e._chain(runtime, tmp_path, body=body)
    workflow = runtime.new_workflow_state()
    permit = runtime.acquire_permit(
        workflow_state=workflow, context_manifest=chain.context
    )
    base_findings = runtime.run_stub_reviewer(
        contract=chain.contract, context_manifest=chain.context, permit=permit
    )
    return chain, base_findings


def _intent_finding(
    chain,
    finding_id,
    *,
    severity="error",
    route="subagent",
    identity="subagent-intent-lens-a",
    human_ruling=None,
    human_ruling_reason=None,
    description=INTENT_DESCRIPTION,
):
    """固定fixtureとしての`intent_damage` finding。LLMは呼ばない。"""

    source = chain.snapshot["files"][0]
    finding = {
        "finding_id": finding_id,
        "kind": "intent_damage",
        "severity": severity,
        "origin": {"route": route, "identity": identity},
        "target_ref": {
            "relative_path": source["relative_path"],
            "sha256": source["sha256"],
        },
        "requirement_ref": INTENT_REQUIREMENT,
        "rule_id": INTENT_RULE_ID,
        "description": description,
    }
    if human_ruling is not None:
        finding["human_ruling"] = human_ruling
    if human_ruling_reason is not None:
        finding["human_ruling_reason"] = human_ruling_reason
    return finding


def _with_findings(base_findings, extra_findings):
    """stub finding_setへ固定所見を加え、封をし直したfinding_setを返す。"""

    merged = {
        key: value for key, value in base_findings.items() if key != "content_digest"
    }
    merged["findings"] = list(base_findings["findings"]) + list(extra_findings)
    return seal(merged)


def _conformance(runtime, chain, finding_set):
    return runtime.evaluate_conformance(
        contract=chain.contract,
        plan_bundle=chain.compile_verdict["plan_bundle"],
        finding_set=finding_set,
    )


def _challenge(runtime, chain, conformance, finding_set):
    return runtime.evaluate_final_challenge(
        contract=chain.contract,
        conformance_verdict=conformance,
        finding_set=finding_set,
    )


# ---------------------------------------------------------------- P1


def test_p1_intent_damage_kind_and_origin_are_constructible(runtime, tmp_path):
    """P1（RED）：findingは種別`kind`と発生元`origin`（route種とidentity）を保持できる。

    runtimeが種別と発生元の語彙を閉じた定数として宣言し
    （`FINDING_KINDS`・`FINDING_ORIGIN_ROUTES`。前例：`SEVERITY_CLASSES`・
    `ORIGIN_CLASSES`）、`kind: intent_damage`と`origin`を持つfindingを含む
    finding_setが構築・受理でき、種別と発生元が保持されることを固定する。
    現在の実装はfindingに`kind`も`origin`も持たず、語彙定数も無いため、
    定数参照（AttributeError）で失敗するREDである。
    """

    assert runtime.FINDING_KINDS == ("contract", "intent_damage")
    assert runtime.FINDING_ORIGIN_ROUTES == (
        "deterministic_stub", "subagent", "external_api", "human",
    )

    chain, base = _base(runtime, tmp_path)
    findings = _with_findings(
        base,
        [
            _intent_finding(
                chain, "F-INTENT-001", severity="warning",
                human_ruling="accepted",
            )
        ],
    )
    runtime.validate_record(findings)
    intent = [
        item for item in findings["findings"] if item.get("kind") == "intent_damage"
    ]
    assert len(intent) == 1
    assert intent[0]["origin"] == {
        "route": "subagent", "identity": "subagent-intent-lens-a",
    }
    # 受理：種別つきfinding_setでもConformance・Final Challengeは評価を拒まない。
    conformance = _conformance(runtime, chain, findings)
    challenge = _challenge(runtime, chain, conformance, findings)
    assert challenge["record_kind"] == "final_challenge_verdict"


def test_p1_legacy_findings_without_kind_keep_passing(runtime, tmp_path):
    """P1後方互換（境界、いま成功）：種別fieldの無い既存形findingは従来どおり扱われる。

    既存E2E happy path（test_a6・test_c2・test_b10）の再確認であり、
    「種別が無い既存findingは`contract`として扱う」（P1）の後方互換を
    境界として固定する薄いtestである。warningだけの既存形findingで
    Conformance・Final Challengeが従来どおりpassedになり、errorの既存形findingで
    Conformanceが従来どおりfailedになることを、種別導入後も変えない。
    検出機構の追加前から成功しており、追加後も成功し続ける見込みである。
    """

    chain, findings = _base(runtime, tmp_path, body=contract_e2e.WARNING_DOCUMENT)
    assert all("kind" not in item for item in findings["findings"])
    assert {item["severity"] for item in findings["findings"]} == {"warning"}
    conformance = _conformance(runtime, chain, findings)
    challenge = _challenge(runtime, chain, conformance, findings)
    assert conformance["status"] == "passed"
    assert challenge["status"] == "passed"
    assert challenge["human_decision_required"] is True

    error_chain, error_findings = _base(
        runtime, tmp_path / "error", body=contract_e2e.ERROR_DOCUMENT
    )
    assert all("kind" not in item for item in error_findings["findings"])
    error_conformance = _conformance(runtime, error_chain, error_findings)
    assert error_conformance["status"] == "failed"


# ---------------------------------------------------------------- P2


def test_p2_blocking_intent_damage_does_not_fail_conformance(runtime, tmp_path):
    """P2（RED）：Conformanceは`contract`種別のfindingだけで判定する。

    blocking（severity `error`）な`intent_damage` findingが混ざっていても、
    `contract`種別のerrorが無ければConformanceは`passed`のままである
    （審査の分離。REQ-CONTRACT-004）。現在の`_severity_counts`は種別を見ず
    全findingのerrorを数えるため、実測は`failed`になり失敗するREDである。
    """

    chain, base = _base(runtime, tmp_path)
    assert base["findings"] == []  # contract種別のerrorは無い。
    findings = _with_findings(
        base,
        [
            _intent_finding(
                chain, "F-INTENT-001", severity="error", human_ruling="accepted",
            )
        ],
    )
    conformance = _conformance(runtime, chain, findings)
    assert conformance["status"] == "passed"


# ---------------------------------------------------------------- P3（中核）


def test_p3_accepted_blocking_intent_damage_fails_final_challenge(runtime, tmp_path):
    """P3（RED・中核）：Human採否済みでblockingな意図毀損所見はFinal Challengeを落とす。

    Human採否済み（`human_ruling: accepted`）でblocking（severity `error`）な
    `intent_damage` findingが1件あれば、Conformanceが`passed`でも
    `evaluate_final_challenge`は`failed`を返す。これがCL-6A-10の中核負例
    「Contract適合なのに最終審査で落ちる」である。
    現在はConformanceが種別を見ずfailedになる（P2未対応）ため、まず前提の
    assert（conformance passed）で失敗するREDである。P2実装後は、Final Challengeが
    Conformanceの合否を写すだけである限り（execution.py 312行）、
    challenge failedのassertで失敗し続ける。
    """

    chain, base = _base(runtime, tmp_path)
    findings = _with_findings(
        base,
        [
            _intent_finding(
                chain, "F-INTENT-001", severity="error", human_ruling="accepted",
            )
        ],
    )
    conformance = _conformance(runtime, chain, findings)
    assert conformance["status"] == "passed"
    challenge = _challenge(runtime, chain, conformance, findings)
    assert challenge["status"] == "failed"
    assert challenge["human_decision_required"] is True


# ---------------------------------------------------------------- P4


def test_p4_pending_intent_damage_stops_final_challenge_fail_closed(runtime, tmp_path):
    """P4（RED）：Human採否が未了の意図毀損所見があればverdictを出さず停止する。

    採否未了（`human_ruling: pending`、または`intent_damage`でfieldを省略）の
    findingが存在する場合、`evaluate_final_challenge`はverdictを出さず
    fail-closedで停止する（`human_decision_required`の実質化）。停止は実装の流儀
    どおり`ContractError`とし、codeは既存の閉じたstop code
    `human_decision_missing`を用いる。LLM所見だけで受理を通すことも
    覆すこともしない。blockingか否か（severity `error`／`warning`）に
    かかわらず停止する。現在はverdictが返る（DID NOT RAISE）ため失敗するREDである。
    """

    cases = (
        ("blocking-pending", {"severity": "error", "human_ruling": "pending"}),
        ("warning-pending", {"severity": "warning", "human_ruling": "pending"}),
        ("ruling-omitted", {"severity": "error"}),
    )
    for index, (name, keywords) in enumerate(cases):
        chain, base = _base(runtime, tmp_path / name)
        findings = _with_findings(
            base, [_intent_finding(chain, f"F-INTENT-{index + 1:03d}", **keywords)]
        )
        conformance = _conformance(runtime, chain, findings)
        with pytest.raises(runtime.ContractError) as error:
            _challenge(runtime, chain, conformance, findings)
        assert error.value.code == "human_decision_missing"


# ---------------------------------------------------------------- P5


def test_p5_multiple_intent_damage_findings_are_kept_without_auto_merge(
    runtime, tmp_path
):
    """P5（RED）：複数の意図毀損所見は潰さず保持し、自動統合・多数決しない。

    重複（同一rule・同一記述で発生元が異なる2件）と競合（同じ対象への
    accepted 1件とrejected 2件）を含む3件の所見がfinding_setにそのまま残り
    （REQ-TRIAGE-002）、rejectedが多数でも自動多数決で受理せず、
    accepted 1件によってFinal Challengeが`failed`になることを固定する。
    保持のassert自体はいま成功するが、判定のassert（conformance passed・
    challenge failed）が現在の実装（種別を見ないConformance、Conformanceを
    写すだけのFinal Challenge）で失敗するREDである。
    """

    chain, base = _base(runtime, tmp_path)
    injected = [
        _intent_finding(
            chain, "F-INTENT-001", severity="error", human_ruling="accepted",
            route="subagent", identity="subagent-intent-lens-a",
        ),
        _intent_finding(
            chain, "F-INTENT-002", severity="error", human_ruling="rejected",
            human_ruling_reason="上位Intentの毀損には当たらないと裁定した。",
            route="subagent", identity="subagent-intent-lens-b",
        ),
        _intent_finding(
            chain, "F-INTENT-003", severity="error", human_ruling="rejected",
            human_ruling_reason="F-INTENT-002と同じ理由で退けた。",
            route="external_api", identity="external-reviewer-001",
        ),
    ]
    findings = _with_findings(base, injected)

    kept = [
        item for item in findings["findings"] if item.get("kind") == "intent_damage"
    ]
    assert kept == injected  # 重複・競合を含む3件がそのまま残る。統合しない。
    assert len({item["finding_id"] for item in kept}) == 3

    conformance = _conformance(runtime, chain, findings)
    assert conformance["status"] == "passed"
    challenge = _challenge(runtime, chain, conformance, findings)
    # rejected 2件対accepted 1件でも、多数決せずaccepted 1件で落とす。
    assert challenge["status"] == "failed"


# ---------------------------------------------------------------- P6


def test_p6_rejected_intent_damage_does_not_fail_final_challenge(runtime, tmp_path):
    """P6（RED）：Human採否でrejectされた意図毀損所見はFinal Challengeを落とさない。

    blocking（severity `error`）でも`human_ruling: rejected`の`intent_damage`
    findingは判定に影響せず、Conformanceも Final Challengeも`passed`になる。
    rejectの事実と理由（`human_ruling_reason`）はfinding_setに残り、
    Provenanceの`finding_set` node経由で追跡できる。現在はConformanceが
    種別を見ずfailedになるため、conformance passedのassertで失敗するREDである。
    """

    chain, base = _base(runtime, tmp_path)
    findings = _with_findings(
        base,
        [
            _intent_finding(
                chain, "F-INTENT-001", severity="error", human_ruling="rejected",
                human_ruling_reason="対象文書は上位Intentの範囲内と裁定した。",
            )
        ],
    )
    conformance = _conformance(runtime, chain, findings)
    assert conformance["status"] == "passed"
    challenge = _challenge(runtime, chain, conformance, findings)
    assert challenge["status"] == "passed"

    kept = [
        item for item in findings["findings"] if item.get("kind") == "intent_damage"
    ]
    assert kept[0]["human_ruling"] == "rejected"
    assert kept[0]["human_ruling_reason"] == "対象文書は上位Intentの範囲内と裁定した。"


# ---------------------------------------------------------------- P7


def test_p7_origin_routes_are_formally_equivalent(runtime, tmp_path):
    """P7（RED）：所見の発生経路は形式上等価に受理され、経路identityが保持される。

    `deterministic_stub`／`subagent`／`external_api`／`human`のどの経路が
    生成した所見でも、P1の形式（`origin`のrouteとidentity）で受け取り、
    同一内容なら同一の判定（conformance passed・challenge failed）になることを
    固定する。経路identityはfinding_setに保持される。LLM呼び出しはしない
    （fixture所見のroute種の保持までを固定する。提案§4）。
    現在はConformanceが種別を見ずfailedになるため失敗するREDである。
    """

    routes = (
        ("deterministic_stub", "stub-intent-rule-001"),
        ("subagent", "subagent-intent-lens-a"),
        ("external_api", "external-reviewer-001"),
        ("human", "kenoogl"),
    )
    statuses = {}
    for route, identity in routes:
        chain, base = _base(runtime, tmp_path / route)
        findings = _with_findings(
            base,
            [
                _intent_finding(
                    chain, "F-INTENT-001", severity="error",
                    human_ruling="accepted", route=route, identity=identity,
                )
            ],
        )
        kept = [
            item
            for item in findings["findings"]
            if item.get("kind") == "intent_damage"
        ]
        assert kept[0]["origin"] == {"route": route, "identity": identity}

        conformance = _conformance(runtime, chain, findings)
        assert conformance["status"] == "passed"
        challenge = _challenge(runtime, chain, conformance, findings)
        statuses[route] = (conformance["status"], challenge["status"])

    assert set(statuses.values()) == {("passed", "failed")}
