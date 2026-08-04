---
evidence_id: RC3-ISSUE-RESOLUTION-PILOT-ISSUE-PLAN-COMPLETION-2026-08-04-V1
recorded_at: 2026-08-04T09:00:18+09:00
status: verified_completed
confidentiality_class: project-internal
---

# Issue Resolution Pilot Issue／Plan Completion Evidence V1

## 完了範囲

Task Contract
`TC-RC3-ISSUE-RESOLUTION-EARLY-PILOT-2026-08-04-V1`の三番目の作業単位
`create the promoted Issue and Resolution Plan if Human approved`を完了した。

- Humanが昇格を承認した一件だけをIssue Recordへ固定した。
- IssueをObservation、Candidate、Triage Decision、Completion EvidenceへDigest付きで結んだ。
- IssueとPlanを別identity、別version、別content Digestとして保存した。
- PlanへIssue obligation、作業項目、scope、non-scope、禁止事項、Acceptance、oracle、risk、deployment、
  rollback、recovery、Task Contract route候補を固定した。
- version 1設定を変更せず、Issue／Planを追加したversion 2設定を作成した。
- Plan Challenge、TODO snapshot、TODO compaction、prompt、validator実装、Verdictはまだ実施していない。

## 固定成果物

- Issue Record：`.reviewcompass/workflow/issues/issue-pilot-todo-growth-001--v1.json`
  - file SHA-256：`2c0ac23012b0b325cd45bafbac3d13c56ec64f45d49919c8b73dd9a210273c1a`
  - content Digest：`0389f68d81af61d570177228e246bb481eea97af23d5454c99831f8bc7c72319`
- Issue Resolution Plan：
  `.reviewcompass/workflow/resolution-plans/plan-pilot-todo-growth-001--v1.json`
  - file SHA-256：`2d753a371913b9d38bef570283a7122ea3ed08d96d041c3020943e1389a738d5`
  - content Digest：`d6c3f3f8a050242c63b4fc6d1d127926cd12426cfb4a8fd736dbd43bdded2768`
- Pilot設定v2：`config/development-issue-resolution-pilot-v2.json`、SHA-256
  `9af4837d968c4088f1ecbaffbf49fc7002667695cd067ee9d8ad33fceaeeb9ff`
- validator：`tools/development/issue_resolution_pilot.py`、SHA-256
  `ad320ab92b92162282e287e7ea0afff55aa4d6c4d5378180dc2ae328a2fa6176`
- RED Evidence：
  `records/development/2026-08-04-issue-resolution-pilot-issue-plan-red-evidence-v1.md`、SHA-256
  `42e283b446543cd55a27c11c71bfc07efb98b3ea0682d297f2a64d57b84d102c`
- 現行Issue／Plan Test：`tests/test_issue_resolution_pilot_issue_plan.py`、SHA-256
  `1e369c5b98566b3fbcd5a9f35248189a3d9360ec102a4ffdb98ec3cc40f57f4a`

## 検証

- RED：version 2設定未実装だけを理由に`16 failed in 0.40s`となった。
- GREEN：同じ16 Testを変更せず`16 passed in 0.05s`となった。
- repository実体がIssue一件、Plan一件であることをpost-write Testへ追加し、現行Issue／Plan Testは
  `17 passed in 0.06s`となった。
- version 1／2関連Testは`33 passed in 0.08s`となった。
- actual Issue／PlanはCLI validatorでID、version、配置、Human promotion、参照、Digest、義務coverage、
  Acceptance／oracle／rollback参照に合格した。
- 公式全Test結果は
  `records/development/2026-08-04-issue-resolution-pilot-issue-plan-green-test-receipt-v1.json`を正本とする。

## Plan Challengeへ残すHuman判断

Planは次を提案しているが、まだ承認されていない。

- 圧縮後TODO全体の上限を`12288 bytes`とする。
- `docs/development/prompts/todo-handoff-update.md`を共通promptとし、`AGENTS.md`と新しいroot
  `CLAUDE.md`から一回ずつ参照する。
- byte-exact snapshotと別manifestを`records/session-handoffs/`へ保存する。
- snapshot／restore、validator、compaction、共通prompt、post-write Verdictを一つのTask Contractで順序実行する。
- 失敗時は決定的restore helperでTODOをsnapshotへ戻し、Issueを未解決のまま保持する。

Plan ChallengeではIssue obligation coverage、作業粒度、TDD closure、禁止事項とnon-scopeの移送、12 KiB上限、
Claude入口、依存、oracle、rollbackの実現可能性を裁定する。blocking Findingが残る間はTODO compactionを開始しない。

## 手戻り・機械処理

本作業単位では、期待したRED以外の失敗、手入力Digest、参照転記訂正、権限再試行は発生しなかった。semanticな
Issue／Plan本文はLLMが作成し、ID、version、path、file Digest、content Digest、参照、coverage、Testは機械処理で
検証した。
