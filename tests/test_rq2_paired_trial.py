"""RQ2 paired evaluation装置のAcceptance Test。

作業票（docs/development/2026-08-17-rq2-apparatus-work-ticket-v1.md）§4を固定する。
- 条件A／B／C／Dの対象path集合が事前走査§3の表どおりであること
- B→Cで材料選択が不変・A（資料多）で増える・Dで必須材料が欠けること
- 依頼recordがcheck合格まで機械組み立てできること
- 実行メタ（入力トークン）はresultイベントの累計から取ること
- 採点・集計・中断条件が機械判定であること
- **本試験は外部起動を一切行わない**（禁止fakeで機械確認）
"""

import importlib
import json
import subprocess as host_subprocess


def _rq2():
    return importlib.import_module("tools.evaluation.rq2_paired_trial")


def _rq1():
    return importlib.import_module(
        "tools.evaluation.rq1_contract_completeness"
    )


def _git(repository, *arguments):
    return host_subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
        check=True,
    )


MATERIAL_A = "# 材料A\n\n表の定義がここにある。\n"
MATERIAL_B = "# 材料B\n\n観測した実物形がここにある。\n"
POOL_TEXT = "# 無関係資料\n\n本ケースの主題とは関係のない文章である。\n"


def _project(tmp_path, *, pool=False):
    """一時projectへ要求定義とケース材料を置く（実repositoryへ触れない）。"""

    rq1 = _rq1()
    rq2 = _rq2()
    root = rq1._project(
        tmp_path, "rq2-case", definition_ids=rq1._FULL_REQUIREMENTS
    )
    case_dir = root / rq2.CASE_ROOT / "case-001"
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "material-a.md").write_text(MATERIAL_A, encoding="utf-8")
    (case_dir / "material-b.md").write_text(MATERIAL_B, encoding="utf-8")
    if pool:
        for index in range(3):
            (case_dir / ("pool-%02d.md" % index)).write_text(
                POOL_TEXT, encoding="utf-8"
            )
    _git(root, "init", "--quiet")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "seed")
    return root


def _case():
    return {
        "case_id": "case-001",
        "group": "real_defect",
        "materials": (
            "docs/evaluation/rq2-cases/case-001/material-a.md",
            "docs/evaluation/rq2-cases/case-001/material-b.md",
        ),
        "required_material": (
            "docs/evaluation/rq2-cases/case-001/material-a.md"
        ),
    }


def test_condition_target_paths_follow_prescan_table(tmp_path):
    rq2 = _rq2()
    root = _project(tmp_path, pool=True)
    case = _case()
    selected = {
        condition: rq2.select_target_paths(
            project_root=root, case=case, condition=condition
        )
        for condition in rq2.CONDITIONS
    }
    # B＝登録材料のみ。C＝Bと同一（契約へ渡すpathは変えない）
    assert selected["B"] == case["materials"]
    assert selected["C"] == case["materials"]
    # A1（資料少）・A2（資料多）＝ディレクトリ内の全file。選択規則は同一で、
    # 差は物理内容（プールの在／不在）にある。ここではプール在の状態で5件。
    assert len(selected["A1"]) == 5
    assert selected["A1"] == selected["A2"]
    assert set(case["materials"]).issubset(set(selected["A1"]))
    # D＝必須材料を1件欠く
    assert case["required_material"] not in selected["D"]
    assert len(selected["D"]) == len(case["materials"]) - 1


def test_selection_invariant_between_b_and_c(tmp_path):
    rq2 = _rq2()
    case = _case()
    without_pool = _project(tmp_path / "a", pool=False)
    with_pool = _project(tmp_path / "b", pool=True)
    signature_b = rq2.selection_signature(
        rq2.build_case_context(
            project_root=without_pool, case=case, condition="B"
        )[1]
    )
    signature_c = rq2.selection_signature(
        rq2.build_case_context(
            project_root=with_pool, case=case, condition="C"
        )[1]
    )
    assert signature_b == signature_c
    assert signature_b["count"] == 2
    # 対照：A（資料多）は選択が増える
    signature_a = rq2.selection_signature(
        rq2.build_case_context(
            project_root=with_pool, case=case, condition="A1"
        )[1]
    )
    assert signature_a["count"] == 5


def test_build_case_request_passes_check(tmp_path):
    rq2 = _rq2()
    request_builder = importlib.import_module("tools.request_builder.core")
    root = _project(tmp_path, pool=False)
    relative_path = rq2.build_case_request(
        project_root=root,
        case=_case(),
        condition="B",
        record_date="2026-08-17",
    )
    text = (root / relative_path).read_text(encoding="utf-8")
    assert "<<記入:" not in text
    # 命名は正式経路の規約（日付＋slug＋-request-v1.md）。実測で確定した形。
    assert relative_path == (
        "records/session-handoffs/2026-08-17-rq2-case-001-b-request-v1.md"
    )
    _git(root, "add", "-A")
    _git(root, "commit", "--quiet", "-m", "request")
    verdict = request_builder.check(
        repository=root, request_relative_path=relative_path
    )
    assert verdict["status"] == "ok"


def test_extract_usage_takes_result_event_total():
    rq2 = _rq2()
    raw = "\n".join(
        [
            json.dumps({"event": "step_update", "step_update": {
                "usage": {"input_tokens": 10, "output_tokens": 1}}}),
            json.dumps({"event": "step_update", "step_update": {
                "usage": {"input_tokens": 20, "output_tokens": 2}}}),
            json.dumps({"event": "result", "result": {
                "usage": {"input_tokens": 30, "output_tokens": 3}}}),
        ]
    )
    usage = rq2.extract_usage(raw)
    # 段別の合計ではなくresultイベントの累計を正とする（実測の形）
    assert usage == {"input_tokens": 30, "output_tokens": 3}


def test_extract_usage_reports_unavailable_without_result():
    rq2 = _rq2()
    raw = json.dumps({"event": "step_update", "step_update": {
        "usage": {"input_tokens": 10, "output_tokens": 1}}})
    assert rq2.extract_usage(raw) is None


def test_scoring_sheet_and_judgments(tmp_path):
    rq2 = _rq2()
    findings = [
        {"finding_id": "F-LLM-001", "severity": "error",
         "description": "表と実物が矛盾する。",
         "target_ref": {"relative_path": "docs/x.md", "sha256": "0" * 64}},
        {"finding_id": "F-LLM-002", "severity": "warning",
         "description": "体裁が揃っていない。",
         "target_ref": {"relative_path": "docs/x.md", "sha256": "0" * 64}},
    ]
    sheet = rq2.build_scoring_sheet(
        [{"case_id": "case-001", "condition": "B", "findings": findings}]
    )
    assert len(sheet) == 2
    assert sheet[0]["case_id"] == "case-001"
    assert sheet[0]["finding_id"] == "F-LLM-001"
    scoring = rq2.apply_judgments(
        sheet,
        {
            ("case-001", "B", "F-LLM-001"): "detected",
            ("case-001", "B", "F-LLM-002"): "false_positive",
        },
    )
    assert scoring[("case-001", "B")] == {
        "detected": True, "false_positive": 1, "out_of_scope": 0,
    }


def test_apply_judgments_rejects_unjudged_finding():
    rq2 = _rq2()
    sheet = rq2.build_scoring_sheet(
        [{"case_id": "case-001", "condition": "B", "findings": [
            {"finding_id": "F-LLM-001", "severity": "error",
             "description": "x",
             "target_ref": {"relative_path": "docs/x.md"}}]}]
    )
    try:
        rq2.apply_judgments(sheet, {})
    except ValueError:
        return
    raise AssertionError("未裁定のFindingを黙って通してはならない")


def test_aggregate_reports_invariance_and_usage():
    rq2 = _rq2()
    trials = [
        {"case_id": "case-001", "condition": "B", "group": "real_defect",
         "status": "succeeded", "selection": {"count": 2},
         "usage": {"input_tokens": 100, "output_tokens": 10},
         "scoring": {"detected": True, "false_positive": 0,
                     "out_of_scope": 0}},
        {"case_id": "case-001", "condition": "C", "group": "real_defect",
         "status": "succeeded", "selection": {"count": 2},
         "usage": {"input_tokens": 110, "output_tokens": 12},
         "scoring": {"detected": True, "false_positive": 1,
                     "out_of_scope": 0}},
        {"case_id": "case-008", "condition": "B", "group": "pass",
         "status": "succeeded", "selection": {"count": 1},
         "usage": {"input_tokens": 90, "output_tokens": 8},
         "scoring": {"detected": False, "false_positive": 2,
                     "out_of_scope": 1}},
    ]
    metrics = rq2.aggregate(trials)
    assert metrics["selection_invariance"]["holds"] is True
    assert metrics["selection_invariance"]["cases_differing"] == []
    # 欠陥ケースだけを検出率の分母にする（合格系は誤検出側で数える）
    assert metrics["by_condition"]["B"]["detection_rate"] == 1.0
    assert metrics["by_condition"]["B"]["false_positive_total"] == 2
    assert metrics["by_condition"]["C"]["input_tokens_mean"] == 110.0


def test_aggregate_flags_selection_difference():
    rq2 = _rq2()
    trials = [
        {"case_id": "case-001", "condition": "B", "group": "real_defect",
         "status": "succeeded", "selection": {"count": 2},
         "usage": {"input_tokens": 100, "output_tokens": 10},
         "scoring": {"detected": True, "false_positive": 0,
                     "out_of_scope": 0}},
        {"case_id": "case-001", "condition": "C", "group": "real_defect",
         "status": "succeeded", "selection": {"count": 5},
         "usage": {"input_tokens": 300, "output_tokens": 10},
         "scoring": {"detected": True, "false_positive": 0,
                     "out_of_scope": 0}},
    ]
    metrics = rq2.aggregate(trials)
    assert metrics["selection_invariance"]["holds"] is False
    assert metrics["selection_invariance"]["cases_differing"] == ["case-001"]


def test_stop_conditions_are_machine_judged():
    rq2 = _rq2()
    ok = rq2.evaluate_stop_conditions(
        [{"status": "succeeded"}] * 5, launched_count=5
    )
    assert ok["stop"] is False
    three_failures = rq2.evaluate_stop_conditions(
        [{"status": "succeeded"}] + [{"status": "failed"}] * 3,
        launched_count=4,
    )
    assert three_failures["stop"] is True
    assert "consecutive_failures" in three_failures["reasons"]
    at_limit = rq2.evaluate_stop_conditions(
        [{"status": "succeeded"}] * 35, launched_count=35
    )
    assert at_limit["stop"] is True
    assert "absolute_limit_reached" in at_limit["reasons"]
    unable = rq2.evaluate_stop_conditions(
        [{"status": "succeeded"}] * 6 + [{"status": "unable"}] * 4,
        launched_count=10,
    )
    assert unable["stop"] is True
    assert "unable_ratio_exceeded" in unable["reasons"]


def test_run_case_never_spawns_process(tmp_path, monkeypatch):
    rq2 = _rq2()
    root = _project(tmp_path, pool=False)
    calls = []

    def fake_launcher(*, request_relative_path, expected_sha256):
        calls.append(request_relative_path)
        return {
            "verdict": {
                "verdict": "verified_with_findings",
                "findings": [
                    {"identifier": "1. 指摘", "claim": "表と実物が矛盾する。",
                     "severity": "error", "blocking": True,
                     "evidence_path": (
                         "docs/evaluation/rq2-cases/case-001/material-a.md"),
                     "evidence_location": "L3"},
                ],
            },
            "raw_text": json.dumps(
                {"event": "result",
                 "result": {"usage": {"input_tokens": 42,
                                      "output_tokens": 7}}}
            ),
        }

    def forbidden(*args, **kwargs):
        raise AssertionError("外部プロセス起動は本試験で禁止である")

    monkeypatch.setattr(
        "tools.evaluation.rq2_paired_trial.launch_guard", forbidden
    )
    result = rq2.run_case(
        project_root=root,
        case=_case(),
        condition="B",
        record_date="2026-08-17",
        launcher=fake_launcher,
        commit=lambda message: _git(root, "add", "-A") and None,
    )
    assert len(calls) == 1
    assert result["status"] == "succeeded"
    assert result["usage"] == {"input_tokens": 42, "output_tokens": 7}
    assert result["selection"]["count"] == 2
    assert result["findings"][0]["severity"] == "error"


def test_extract_read_paths_and_scope_check():
    """reviewerが実際に読んだfileを機械抽出し、範囲外読取りを検出する。

    正解表を私有領域へ退避しても、repository内には設計・裁定recordが残り、
    そこに答の一部が書かれている。事前に消し切るのではなく**読まれたことを
    事後に機械検出**して、汚染した実行を集計から外す（実測：raw応答の
    step_update/tool_info/parameters/AbsolutePathに読取りpathが残る）。
    """

    rq2 = _rq2()
    raw = "\n".join(
        [
            json.dumps({"event": "step_update", "step_update": {
                "tool_info": {"parameters": {"AbsolutePath":
                    "/repo/docs/evaluation/rq2-cases/case-001/material-a.md"}}}}),
            json.dumps({"event": "step_update", "step_update": {
                "tool_info": {"parameters": {"AbsolutePath":
                    "/repo/records/development/leak.md"}}}}),
            json.dumps({"event": "result", "result": {
                "usage": {"input_tokens": 1, "output_tokens": 1}}}),
        ]
    )
    paths = rq2.extract_read_paths(raw, repository_root="/repo")
    assert paths == (
        "docs/evaluation/rq2-cases/case-001/material-a.md",
        "records/development/leak.md",
    )
    report = rq2.check_read_scope(
        paths,
        allowed=("docs/evaluation/rq2-cases/case-001/material-a.md",),
        request_relative_path="records/session-handoffs/req.md",
    )
    assert report["clean"] is False
    assert report["outside"] == ("records/development/leak.md",)
    clean = rq2.check_read_scope(
        ("docs/evaluation/rq2-cases/case-001/material-a.md",
         "records/session-handoffs/req.md"),
        allowed=("docs/evaluation/rq2-cases/case-001/material-a.md",),
        request_relative_path="records/session-handoffs/req.md",
    )
    assert clean["clean"] is True
    assert clean["outside"] == ()
