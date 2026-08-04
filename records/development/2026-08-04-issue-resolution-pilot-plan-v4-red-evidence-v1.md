# Issue Resolution Pilot Plan v4 RED Evidence v1

- recorded_at: `2026-08-04T12:00:01+09:00`
- source Decision: `DEC-RC3-ISSUE-PILOT-WI-001-SNAPSHOT-BOUNDARY-2026-08-04`
- target Plan: `PLAN-PILOT-TODO-GROWTH-001` version 4
- test: `tests/test_issue_resolution_pilot_plan_v4.py`
- test SHA-256: `b33181054cbea1c20feaadf080a6afe5e6880105e56558fb4d9f47b79ae99971`

## 固定した期待境界

1. WI-001は固定Testを変更しないsnapshot helper GREENへ限定する。
2. WI-007はWI-002とWI-006のcontaining commit後に実TODO snapshot／manifestを作成・再読込する。
3. WI-003はWI-007へ依存し、WI-007 commitではTODO sourceを変更しない。
4. WI-007再読込合格後からWI-003最初のTODO書換えまでsource identityを維持する。
5. session境界などでsourceが変わった場合はWI-003を開始せず、既存snapshotを上書きせず新しい版を作る。
6. Task Contract route順は`WI-001, WI-002, WI-006, WI-007, WI-003, WI-004, WI-005`とする。

## RED結果

- targeted command: `python3 -m pytest -q tests/test_issue_resolution_pilot_plan_v4.py`
- targeted result: `9 failed, 1 passed in 0.08s`
- full command: `python3 -m pytest -q`
- full result: `9 failed, 572 passed in 2.70s`

完成形fixtureは既存の汎用Plan validatorに合格した。失敗9件は、Plan v4実体不在1件と、version 4専用の
snapshot timing closure／recovery拒否が未実装である8件である。既存Plan v1〜v3、Task Contract v1、
固定WI-001 Test、実snapshot、TODO compactionは変更していない。

## 次action

本RED TestとEvidenceをcommitする。containing commit確認後だけ、version 4 validator境界とPlan v4候補を作成し、
固定Testを変更せずGREENにする。
