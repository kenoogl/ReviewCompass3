# TODO_NEXT_SESSION

更新日：2026-08-05

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AはDefinition Challenge設計承認後のTDD preflightでpause_and_triageしている。
- 現在作業：Work 5A Definition Challenge。承認済み設計のHuman Contract approvalをcompile前に検証するrecordと機械gateが未定義であるため、Testと実装を開始していない。blocking候補はIC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-HTC-C9F6C917`：`registered / nonblocking`、影響：Digest照合のshell手順で発生したnonblocking候補IC-SHELL-PATH-VARIABLE-DIGEST-CHECK-001を既存根本原因へroute済み。Work 5Aのblocking原因とは別件、次：現行Workには割り込まず、Work 5Aのblocking候補をHuman triageする

## 最新のauthority／Evidence

- [Definition Challenge approval gate blocking候補](records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-improvement-candidate-v1.md) — SHA-256 `96ee100a0633be4525e59f27d090e6460657e26352416e88d0261172845ff18d`
- [Definition Challenge承認Decision](records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md) — SHA-256 `9ca6a0f75c00f2979437fceca225ede10d28c84f1578a1624db0f04747d7214d`
- [Definition Challenge承認済み設計](docs/design/2026-08-05-work5a-definition-challenge-proposal.md) — SHA-256 `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f`
- [shell Digest検査手戻り候補](records/development/2026-08-05-shell-path-variable-digest-check-improvement-candidate-v1.md) — SHA-256 `f879f027f218676b457a6c9cd100775de4d21e637308bc239cd6a75a615743ec`
- [機械操作の根本原因Issue](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `ca1e62f8b43f9bf26ce7fd250a8daad90af82ec699a1bd0124096c786e50da0d`

## 次に行う一作業

IC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001をHuman triageし、upstream_revisionを採用するか判断する。

開始条件：

- blocking候補と固定sourceのDigestが有効であること
- Humanが停止判定とrouteを裁定すること

完了条件：

- upstream_revisionの採用／却下／risk受容をHuman Decisionに固定する
- 採用時はcontract_approval recordとcompile事前gateの最小境界を版付き設計として承認する

後続作業：採用されたUpstream Revisionのcommitとclean transition後にだけ、Contract v2とDefinition ChallengeのRED Testへ進む。

## blocker・Human判断待ち

- blocker：Human Contract approvalをcompile前に強制するrecord identity、schema、Digest結線、stop codeが未定義である。Acceptanceと必須Provenanceに影響するためpause_and_triage。
- Human判断待ち：IC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001のupstream_revision提案を採用するかどうか。推奨はcontract_approval recordをDefinition Challenge verdictとcompile verdictの間に追加し、欠落・拒否・改竄・identity不一致をfail-closedにする案。

## stale・deferred

- stale：Definition Challengeの実装開始判断はblocking候補のpause_and_triage解除まで利用しない。承認済み設計とDecisionは自動改定せず、Human判断待ちとする。
- deferred：Work 5A Current Work Projection正式record写像、refactor後再確認、Work 6A、Architecture Policy、Challenge Policy、risk catalog、隣接Contract検査、汎用Challenge framework、UI、automation、Work 8正式評価。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：未実行（TDD開始前に停止。既存Work 5Aの最終確認は`777 passed`）
- 直近の全Test：venv公式runner `962 passed`、Python 3.9.6、pytest 8.4.2、fallback false（今回は再実行していない）
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
