# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AはDefinition Challenge設計とHuman Contract approval gateの採用を終え、Claude実装handoffを固定した。
- 現在作業：Work 5A Definition Challenge。Codexの設計・指示作成は完了し、HumanがClaudeへ実装指示書を渡して完了連絡を待つ段階である。Codexは実装を行わず、Claude完了後に独立検証する。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-HTC-C9F6C917`：`registered / nonblocking`、影響：shellによる決定的操作の手戻り候補を集約する既存Issue。今回のClaude委譲を停止しない、次：現行Workへ割り込まず、Definition Challenge実装と独立検証の後に扱う

## 最新のauthority／Evidence

- [Claude向けDefinition Challenge実装指示](records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-implementation.md) — SHA-256 `520d3220fc190c27b69161d4a5e8cafd446a5a6d63e04e72c3d094b220fd6961`
- [approval gate採用Decision](records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-adoption-decision-v1.md) — SHA-256 `90f4f8a82041955c0fc4125b88fdd9ab80658a13a22f6eb1027fcbc4f35e2ac3`
- [approval gate Amendment](docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md) — SHA-256 `881a9192322e1e1176d3b453dfa121b6dea1a99a6e1c438ad637fc209ed5d0da`
- [Definition Challenge承認済み設計](docs/design/2026-08-05-work5a-definition-challenge-proposal.md) — SHA-256 `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f`
- [機械操作の根本原因Issue](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `ca1e62f8b43f9bf26ce7fd250a8daad90af82ec699a1bd0124096c786e50da0d`

## 次に行う一作業

HumanがClaudeへDefinition Challenge実装指示書を渡し、Claudeの作業終了後にCodexへ知らせる。

開始条件：

- commit `be82301`の実装指示書と、開始基準commit `6b6c989`の固定資料をClaudeが読めること
- Claude開始時のworktreeに他者の未コミット変更が無いこと

完了条件：

- Claudeが指示書の停止境界まで実施し、RED、GREEN、初回Runのcommitと完了報告を作ること
- HumanがClaudeの作業終了をCodexへ知らせること

後続作業：CodexがClaudeのcommit、差分、Digest、RED／GREEN／全Test、初回Definition Challenge Runを独立検証し、Contract version 2のHuman承認要否を提示する。

## blocker・Human判断待ち

- blocker：なし。実装作業はClaudeへの受け渡し待ちであり、Codexは完了通知まで実装しない。
- Human判断待ち：現在は指示書のClaudeへの受け渡しだけ。初回Definition Challenge Runがpassedの場合、後続でContract version 2を承認するかHumanが判断する。

## stale・deferred

- stale：旧pause_and_triage表示とupstream_revision判断待ちは、採用Decision `DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`により置換済み。実装開始判断の根拠に使わない。
- deferred：Contract version 2承認後のcompileとReview Run、Work 5A Current Work Projection正式record写像、refactor後再確認、Work 6A、Architecture Policy、Challenge Policy、risk catalog、隣接Contract検査、汎用Challenge framework、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：既存Work 5A `tests/test_first_review_task_contract_e2e.py`を再実行し`38 passed`（0.15秒）。Definition Challengeの新TestはClaudeがREDから作成する。
- 直近の全Test：venv公式runner `962 passed`、Python 3.9.6、pytest 8.4.2、fallback false（今回は再実行していない）。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
