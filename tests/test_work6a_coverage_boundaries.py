"""Work 6A被覆境界の確認test（対応表CL-6A-01残余の閉鎖）。

対応表`records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`の
CL-6A-01「Contract／Requirement／Plan／Context／Provenance欠落を検出する」は、
Plan欠落だけ直接の負例を引用していなかった。本fileはその残余を閉じる境界例である。

本fileのtestはREDではない。検出機構（`tools/task_contract/execution.py`の
汎用node検査loop。`verify_provenance`の入力検査と`validate_provenance_verdict`の
node検査）は既に実装済みであり、追加時点で成功する見込みの境界例である。
訂正記録：`records/development/2026-08-06-work6a-inventory-correction-v1.md`
"""

import importlib
import json

import pytest

import test_first_review_task_contract_e2e as contract_e2e


@pytest.fixture
def runtime():
    return importlib.import_module("tools.task_contract")


def test_missing_compile_verdict_is_rejected_as_provenance_node_missing(runtime, tmp_path):
    """CL-6A-01境界例：Plan欠落は`provenance_node_missing`で拒否される。

    Planは`compile_verdict`（`plan_bundle`を内包する）のnodeとして来歴に現れる。
    `test_b8_broken_provenance_edge_is_not_verified`と同じ除去系の書き方で、
    生成側`verify_provenance`と検証側`validate_provenance_verdict`の双方が
    `compile_verdict`の欠落を汎用node検査loopで停止することを固定する。
    境界例であり、検出機構は実装済みのため追加時点で成功する見込みである。
    """

    chain = contract_e2e._chain(runtime, tmp_path)
    _workflow, permit, findings, conformance, challenge = contract_e2e._run_to_challenge(
        runtime, chain
    )
    human = runtime.record_human_decision(
        contract=chain.contract, context_manifest=chain.context, finding_set=findings,
        conformance_verdict=conformance, final_challenge_verdict=challenge,
        decision="approved", human_id=contract_e2e.HUMAN_ID,
        decided_at=contract_e2e.DECIDED_AT,
    )

    # 生成側：compile_verdict入力を除去すると、b8と同じくnode欠落として停止する。
    with pytest.raises(runtime.ContractError) as generation:
        runtime.verify_provenance(
            requirement_binding=chain.binding, contract=chain.contract,
            compile_verdict=None, context_manifest=chain.context,
            permit=permit, finding_set=findings, conformance_verdict=conformance,
            final_challenge_verdict=challenge, human_decision=human,
        )
    assert generation.value.code == "provenance_node_missing"
    assert generation.value.detail == "compile_verdict"

    # 検証側：完成済みverdictからcompile_verdict nodeだけ除去しても停止する。
    verdict = runtime.verify_provenance(
        requirement_binding=chain.binding, contract=chain.contract,
        compile_verdict=chain.compile_verdict, context_manifest=chain.context,
        permit=permit, finding_set=findings, conformance_verdict=conformance,
        final_challenge_verdict=challenge, human_decision=human,
    )
    broken = json.loads(json.dumps(verdict))
    broken["verified_nodes"] = [
        item for item in broken["verified_nodes"]
        if item["node_role"] != "compile_verdict"
    ]
    with pytest.raises(runtime.ContractError) as validation:
        runtime.validate_provenance_verdict(broken)
    assert validation.value.code == "provenance_node_missing"
    assert validation.value.detail == "compile_verdict"
