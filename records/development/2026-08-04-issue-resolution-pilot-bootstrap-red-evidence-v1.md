---
evidence_id: RC3-ISSUE-RESOLUTION-PILOT-BOOTSTRAP-RED-2026-08-04-V1
recorded_at: 2026-08-04T08:18:05+09:00
status: verified_red
confidentiality_class: project-internal
---

# Issue Resolution Pilot Bootstrap RED Evidence V1

## 期待動作

- development限定Pilot設定が一つのIssue subjectと二つの初期record kindへscopeを固定する。
- Task Contractの固定sourceがpathとSHA-256で解決できる。
- Improvement CandidateのID、version、path、content Digest、source／Evidence参照を検査する。
- Human Triage DecisionのCandidate binding、Human authority、Issue昇格整合を検査する。
- Human以外のIssue昇格、stale Candidate参照、誤配置、Digest不一致を拒否する。
- TODO projectionはactiveな既知IDだけを許可し、詳細な手戻り履歴とCandidate本文の複製を拒否する。

固定Testは`tests/test_issue_resolution_pilot.py`、SHA-256は
`007b85a63f93b6ffeb12139717bc9abc2c19ad5c13424ce27ebdbeff698d13f6`である。

## 初回RED

command：`python3 -m pytest -q tests/test_issue_resolution_pilot.py`

結果：`15 failed in 0.11s`、exit code 1。15件すべて
`ModuleNotFoundError: tools.development.issue_resolution_pilot`であり、期待するPilot validator未実装だけが
失敗理由だった。
