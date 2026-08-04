# Issue Resolution Pilot Task Contract v2 RED Evidence v1

## 対象

- Test：`tests/test_issue_resolution_pilot_implementation_task_contract_v2.py`
- Test SHA-256：`afe238e5fa1857e5ea5ea03a5bc20bbd0e7216d3ddbeb16eb6af8e69c3b7aa13`
- 承認済みPlan：`.reviewcompass/workflow/resolution-plans/plan-pilot-todo-growth-001--v4.json`
- Plan Approval Decision：`records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v4-decision.json`

## 固定した期待境界

- Task Contract v2をPlan v4、Challenge v4、Approval DecisionへDigest付きで結線する。
- WI-001のhelper実装完了と実snapshot未作成を、既存Evidenceとcontaining commitから繰り越す。
- Work Item順を`WI-001, WI-002, WI-006, WI-007, WI-003, WI-004, WI-005`へ固定する。
- WI-007はTODOを書き換えずsource identityを固定し、WI-003はWI-007 containing commitとsource identityの
  再読込一致後だけ開始できるようにする。
- Task Contract v2 containing commit確認前のWI-002、実snapshot、TODO compactionを禁止する。

## RED確認

- targeted：`python3 -m pytest -q tests/test_issue_resolution_pilot_implementation_task_contract_v2.py`
- 結果：`8 failed in 0.07s`
- 全体：`python3 -m pytest -q`
- 結果：`8 failed, 581 passed in 2.69s`
- 失敗identity：専用validator未実装7件、repository上のTask Contract v2実体不在1件。
- 既存581 Testは合格しており、既存機能の退行は観測していない。

## 判定

期待したREDである。Task Contract v2実体と専用validatorは作成しておらず、実snapshot、WI-002、TODO compaction、
Issue解決も開始していない。RED作業単位のcontaining commitとclean transitionを確認した後だけGREEN実装へ進む。
