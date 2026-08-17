"""reviewer接続adapter（順序3）のAcceptance Test。

作業票（docs/development/2026-08-17-reviewer-bridge-work-ticket-v1.md）§2〜§4を固定する。
- 正式経路の機械駆動（assemble→機械記入→check合格）。placeholder残存の禁止
- finding変換表（§4）：blocking真→error格上げ・出所llm_review・unresolved明示・sealed
- 本作業は外部起動ゼロ（fakeのみ。subprocess監視で機械確認）
"""

import importlib
import json
import subprocess as host_subprocess


def _bridge():
    return importlib.import_module("tools.evaluation.reviewer_bridge")


def _rq1():
    return importlib.import_module(
        "tools.evaluation.rq1_contract_completeness"
    )


def _runtime():
    return importlib.import_module("tools.task_contract")


def _git(repository, *arguments):
    return host_subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
        check=True,
    )


def _experiment_repo(tmp_path):
    rq1 = _rq1()
    root = rq1._project(
        tmp_path, "bridge-case", definition_ids=rq1._FULL_REQUIREMENTS
    )
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "seed")
    return root


def _chain(root):
    runtime = _runtime()
    rq1 = _rq1()
    binding = runtime.bind_requirements(
        project_root=root, requirement_ids=rq1._FULL_REQUIREMENTS
    )
    snapshot = runtime.read_source_snapshot(
        project_root=root,
        target_paths=(rq1.TARGET,),
        base_commit="BASE",
        head_commit="HEAD",
    )
    contract = runtime.build_review_task_contract(
        contract_id="TC-BRIDGE-CASE",
        contract_version=1,
        requirement_binding=binding,
        target_paths=(rq1.TARGET,),
    )
    compile_verdict = runtime.compile_contract(
        contract=contract, requirement_binding=binding
    )
    context = runtime.build_context_manifest(
        contract=contract,
        plan_bundle=compile_verdict["plan_bundle"],
        source_snapshot=snapshot,
    )
    return contract, context


def test_compose_request_body_reflects_contract(tmp_path):
    bridge = _bridge()
    root = _experiment_repo(tmp_path)
    contract, context = _chain(root)
    request_body, decided_scope = bridge.compose_request_body(
        contract, context
    )
    assert contract["responsibility"]["goal"] in request_body
    assert any(
        material["relative_path"] in request_body
        for material in context["material_bundle"]
    )
    assert decided_scope.strip()


def test_build_free_text_request_passes_check(tmp_path):
    bridge = _bridge()
    rq1 = _rq1()
    request_builder = importlib.import_module("tools.request_builder.core")
    root = _experiment_repo(tmp_path)
    contract, context = _chain(root)
    request_body, decided_scope = bridge.compose_request_body(
        contract, context
    )
    relative_path = bridge.build_free_text_request(
        repository=root,
        record_date="2026-08-17",
        slug="rq2-case-bridge-test",
        title="実験ケースの妥当性レビュー",
        target_paths=(rq1.TARGET,),
        request_body=request_body,
        decided_scope=decided_scope,
    )
    text = (root / relative_path).read_text(encoding="utf-8")
    assert "<<記入:" not in text
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "request record")
    verdict = request_builder.check(
        repository=root, request_relative_path=relative_path
    )
    assert verdict["status"] == "ok"


def test_convert_findings_maps_blocking_and_unresolved(tmp_path):
    bridge = _bridge()
    runtime = _runtime()
    root = _experiment_repo(tmp_path)
    contract, context = _chain(root)
    material = context["material_bundle"][0]
    verdict_findings = [
        {
            "identifier": "1. 指摘A",
            "claim": "本文の主張が根拠と一致しない。",
            "severity": "info",
            "blocking": True,
            "evidence_path": material["relative_path"],
            "evidence_location": "L3",
        },
        {
            "identifier": "2. 指摘B",
            "claim": "軽微な表現の揺れ。",
            "severity": "info",
            "blocking": False,
            "evidence_path": "docs/unknown.md",
            "evidence_location": "",
        },
    ]
    finding_set = bridge.convert_findings(
        verdict_findings, context_manifest=context
    )
    assert finding_set["record_kind"] == "finding_set"
    assert finding_set["calls_llm"] is True
    assert finding_set["reviewer"] == "llm_review_via_launch"
    first, second = finding_set["findings"]
    assert first["severity"] == "error"
    assert first["rule_id"] == "llm_review"
    assert first["target_ref"]["relative_path"] == material["relative_path"]
    assert first["target_ref"]["sha256"] == material["sha256"]
    assert second["severity"] == "info"
    assert second["target_ref"]["sha256"] == "unresolved"
    conformance = runtime.evaluate_conformance(
        contract=contract,
        plan_bundle=runtime.compile_contract(
            contract=contract,
            requirement_binding=runtime.bind_requirements(
                project_root=root,
                requirement_ids=_rq1()._FULL_REQUIREMENTS,
            ),
        )["plan_bundle"],
        finding_set=finding_set,
    )
    assert conformance["status"] == "failed"


def test_fake_launch_roundtrip_never_spawns(tmp_path, monkeypatch):
    bridge = _bridge()
    root = _experiment_repo(tmp_path)
    contract, context = _chain(root)
    calls = []

    def fake_launcher(*, request_relative_path, expected_sha256):
        calls.append((request_relative_path, expected_sha256))
        return {
            "verdict": "verified_with_findings",
            "findings": [
                {
                    "identifier": "1. 検査済み",
                    "claim": "対象は妥当である。",
                    "severity": "info",
                    "blocking": False,
                    "evidence_path": context["material_bundle"][0][
                        "relative_path"
                    ],
                    "evidence_location": "L1",
                }
            ],
        }

    def forbidden_run(*args, **kwargs):
        raise AssertionError("external process launch is forbidden here")

    monkeypatch.setattr(
        "tools.evaluation.reviewer_bridge.subprocess_guard", forbidden_run
    )
    finding_set = bridge.launch_and_convert(
        request_relative_path="records/session-handoffs/fake-request.md",
        expected_sha256="0" * 64,
        context_manifest=context,
        launcher=fake_launcher,
    )
    assert len(calls) == 1
    assert finding_set["reviewer"] == "llm_review_via_launch"
    assert finding_set["findings"][0]["severity"] == "info"
