---
evidence_id: RC3-ISSUE-RESOLUTION-PILOT-ISSUE-PLAN-RED-2026-08-04-V1
recorded_at: 2026-08-04T08:53:33+09:00
status: verified_red
confidentiality_class: project-internal
---

# Issue Resolution Pilot Issue／Plan RED Evidence V1

## 固定Test

`tests/test_issue_resolution_pilot_issue_plan.py`、SHA-256
`bbc2d159507364f426783f31ac0a336da4c82181d7332221319884e0248e0d85`

Testは次を要求する。

- version 1設定を変更せず、version 2でIssue RecordとIssue Resolution Planを追加する。
- IssueをHumanが承認したCandidate、Triage Decision、ObservationへDigest付きで接続する。
- mutableな`current_status`、未承認Issue ID、stale Decision、誤配置を拒否する。
- Planをexact Issue versionとDigestへ接続する。
- scope、禁止事項、Issue義務、作業項目、Acceptance、oracle、rollbackの欠落を拒否する。
- Work Itemから未知のobligation、Acceptance、oracle、rollbackへの参照を拒否する。

## 初回RED

command：`python3 -m pytest -q tests/test_issue_resolution_pilot_issue_plan.py`

結果：`16 failed in 0.40s`、exit code 1。16件すべてversion 2 Pilot設定が未作成であることによる
`PilotValidationError: cannot load Pilot config`で失敗した。既存version 1設定、Candidate、Triage Decision、
validatorの回帰は失敗理由ではない。
