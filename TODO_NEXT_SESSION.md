# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Work 6A中核negative pathの承認範囲をGREENにした。同じTestを弱めていない。Current Work Projection正式写像はdeferredのままである。拒否対象の拡張と判定語彙の訂正はHumanが採択済みで、REDから着手する。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-HTC-C9F6C917`：`registered / nonblocking`、影響：shellによる決定的操作の手戻り候補を集約する既存Issue。拡張REDの開始を停止しない、次：現行route判断へ割り込ませず、既存Issueとして保持する

## 最新のauthority／Evidence

- [Work 6A GREEN Evidence](records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md) — SHA-256 `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c`
- [Work 6A GREEN範囲Decision](records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md) — SHA-256 `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb`
- [Work 6A RED Evidence](records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md) — SHA-256 `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20`
- [Work 6A項目と既存Testの対応inventory](records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json) — SHA-256 `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16`
- [案A承認Decision](records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md) — SHA-256 `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `1bd743b0fd110342900996199b2a81eaf2b42440f28318f931e43a78b039a550`
- [Current Plan](docs/current/reviewcompass3-plan-current.md) — SHA-256 `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f`
- [機械操作の根本原因Issue](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`

## 次に行う一作業

拒否対象を上位文書が名指しする成果物へ広げ、判定語彙をauthority基準へ改める変更を、REDから固定する。

開始条件：

- GREEN実装とEvidenceを含むcommitがcleanであること
- 採択Decisionをnew-onlyで記録してからRED testを追加すること

完了条件：

- 拡張対象の負例が期待した理由でREDになること
- 同じTestを弱めずGREENにし、公式全Testが緑になること
- RED Evidenceの事実誤りを訂正recordへ固定すること

後続作業：拡張後、checklist CL-6A-08へ完了印を付けるかをHumanが判断する。Work 6Aの残り20項目は承認範囲外のままである。

## blocker・Human判断待ち

- blocker：なし。Current Work Projection正式写像、正式Portfolio／Work Item／Workflow state、Work 6Aの残り20項目は開始しない。
- Human判断待ち：拡張完了後のchecklist CL-6A-08の完了可否。恒久検査器のIssueレーン投入の可否。

## stale・deferred

- stale：旧TODOの「GREEN実装範囲のHuman判断待ち」は採択により解消した。RED Evidence§8-2が挙げた壊れる既存test名は誤りであり、訂正recordで置換する。
- deferred：Current Work Projection正式写像、同じTestを変更しないrefactor後再確認、Work 6Aのうち承認範囲外20項目、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 6A negative 6 passed、隣接する既存projection関連13 passed
- 直近の全Test：venv公式runner 1013 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
