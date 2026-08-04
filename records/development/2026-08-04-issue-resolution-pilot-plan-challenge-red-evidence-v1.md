---
evidence_id: RC3-ISSUE-RESOLUTION-PILOT-PLAN-CHALLENGE-RED-2026-08-04-V1
recorded_at: 2026-08-04T09:07:07+09:00
status: verified_red
confidentiality_class: project-internal
---

# Issue Resolution Pilot Plan Challenge RED Evidence V1

固定Testは`tests/test_issue_resolution_pilot_plan_challenge.py`、SHA-256
`07fa652f27cbf4c46c56f3cf0ad1ddaf67b9eb1ab3f76af095ce66a034757ecf`である。

Testは次を要求する。

- version 2設定を変更せず、version 3でPlan Challengeを追加する。
- Challengeをexact Issue／Plan version、file SHA-256、content Digestへ束縛する。
- 必須10観点の欠落とstale Plan bindingを拒否する。
- `block`観点には対応するblocking Findingを要求する。
- blocking FindingがあるChallengeを`ready_for_human_approval`にしない。
- Human Decisionの必要性をChallenge自身が解除できない。

初回command：`python3 -m pytest -q tests/test_issue_resolution_pilot_plan_challenge.py`

結果：`7 failed in 0.21s`、exit code 1。7件すべてversion 3 Pilot設定が未作成であることによる
`PilotValidationError: cannot load Pilot config`で失敗した。既存Issue、Plan、version 2 validatorの回帰は
失敗理由ではない。
