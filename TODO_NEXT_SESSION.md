# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeへ委譲する。
- 現在作業：Work 5A happy pathの固定EvidenceとCodex独立検証は完了。Current Work Projection正式写像には必要な正式recordが不足しており、後続route提案の案AがHuman判断待ちである。委譲指示を案A承認とは解釈しない。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-HTC-C9F6C917`：`registered / nonblocking`、影響：shellによる決定的操作の手戻り候補を集約する既存Issue。今回の引き継ぎとroute判断を停止しない、次：現行route判断へ割り込ませず、既存Issueとして保持する

## 最新のauthority／Evidence

- [Claude開発継続引き継ぎ](records/session-handoffs/2026-08-06-codex-to-claude-development-continuation.md) — SHA-256 `5d488a132777bf012bc433e7929c4db60c8a174077f543936b8d786f918f2563`
- [Current Work Projection後続route提案](docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md) — SHA-256 `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `54d3b9f4eee5889b3b4d85e94c665eba0c643996ddf74f45f6a514389af00d02`
- [Contract v2 Review受理records](records/development/2026-08-06-work5a-contract-v2-review-acceptance-records-v1.json) — SHA-256 `151c63c838850a3da319b5f1eaa8cf0d02379aed85b0a592f124e3624c275354`
- [Contract v2 Review受理Evidence](records/development/2026-08-06-work5a-contract-v2-review-acceptance-evidence-v1.md) — SHA-256 `3edf6f88bd85619c9e75868f066ddc1d0b66c41e842d27cd05abffac64d9bed5`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18`
- [機械操作の根本原因Issue](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`

## 次に行う一作業

Claudeが開発継続引き継ぎとroute提案を全文確認し、Humanへ案Aを承認するか明確に確認する。

開始条件：

- 本引き継ぎ、チェックリスト、TODOを含むcommitがcleanであること
- 固定文書とEvidenceのDigestが引き継ぎ記載値に一致すること

完了条件：

- Humanの案Aに対する承認または不承認がnew-only Decisionへ記録されること
- 判断結果に応じてチェックリストとTODOのrouteが更新されること

後続作業：案A承認時だけWork 6Aの既存negative test inventoryと未被覆RED test作成へ進む。不承認時はWork 6Aを開始せず、選択されたrouteへ提案を改定する。

## blocker・Human判断待ち

- blocker：案AのHuman判断が出るまで、Work 6A、Projection正式写像、新schemaの実装を開始しない。
- Human判断待ち：Current Work Projection正式写像を必要recordが揃うまでdeferし、Work 6A REDへ進む案Aを承認するか。

## stale・deferred

- stale：旧TODOの「CodexがClaudeの受理recordを独立検証する」は完了済みであり、本引き継ぎとroute判断待ちへ置換した。旧Contract承認待ちとReview受理待ち表示も解消済みである。
- deferred：Current Work Projection正式写像、同じTestを変更しないrefactor後再確認、Work 6A RED以外の後続Work、Work 6A GREEN、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Definition Challengeと既存Work 5Aを合わせて83 passed
- 直近の全Test：venv公式runner 1007 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
