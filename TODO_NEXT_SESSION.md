# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：案A承認後のWork 6A中核negative pathをRED testとして固定した。Current Work Projection正式写像はdeferredのままである。GREEN実装は未承認であり開始していない。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-HTC-C9F6C917`：`registered / nonblocking`、影響：shellによる決定的操作の手戻り候補を集約する既存Issue。Work 6AのGREEN判断を停止しない、次：現行route判断へ割り込ませず、既存Issueとして保持する

## 最新のauthority／Evidence

- [Work 6A RED Evidence](records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md) — SHA-256 `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20`
- [Work 6A項目と既存Testの対応inventory](records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json) — SHA-256 `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16`
- [案A承認Decision](records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md) — SHA-256 `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda`
- [Current Work Projection後続route提案](docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md) — SHA-256 `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `1bd743b0fd110342900996199b2a81eaf2b42440f28318f931e43a78b039a550`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`
- [Development Policy](docs/development/2026-08-02-development-policy.md) — SHA-256 `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18`
- [機械操作の根本原因Issue](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`

## 次に行う一作業

HumanがWork 6AのGREEN実装範囲を判断する。

開始条件：

- RED testとRED Evidenceを含むcommitがcleanであること
- GREEN実装範囲がHuman判断で確定するまで実装を変更しないこと

完了条件：

- GREEN実装範囲の承認または不承認がDecisionへ記録されること
- 新schema、state、authority、Contract変更を含む場合はその可否が明示されること

後続作業：承認された範囲だけを、同じRED testを弱めずにGREENへ進める。範囲外はdeferredのまま保持する。

## blocker・Human判断待ち

- blocker：Work 6AのGREEN実装はHuman判断待ちであり開始しない。Current Work Projection正式写像と新schemaも開始しない。
- Human判断待ち：Work 6AのGREEN実装範囲の確定。RED Evidence§8の既知制約3点を判断材料とする。

## stale・deferred

- stale：旧TODOの「Work 6A項目のinventoryと未被覆RED test作成」はRED固定の完了により解消した。
- deferred：Current Work Projection正式写像、同じTestを変更しないrefactor後再確認、Work 6Aのうち承認範囲外20項目、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：新規RED 6 failed、既存projection関連11 passed
- 直近の全Test：venv公式runner 1007 passed / 6 failed（失敗は新規RED 6件のみ、total 1013）、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
