# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Work 6A中核negative pathのGREEN後、非authority入力の拒否対象を上位文書が名指しする4件へ広げ、判定語彙をauthority基準へ訂正した。RED EvidenceとGREEN Evidence v1の誤りと陳腐化は訂正recordで置換した。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-HTC-C9F6C917`：`registered / nonblocking`、影響：shellによる決定的操作の手戻り候補を集約する既存Issue。現行のHuman判断を停止しない、次：現行route判断へ割り込ませず、既存Issueとして保持する

## 最新のauthority／Evidence

- [非authority入力 拡大GREEN Evidence](records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md) — SHA-256 `79c5783c6f759c631aeabc41916fcc93f914984e2278ab1acb29589e1119a5ac`
- [Evidence訂正record](records/development/2026-08-06-work6a-evidence-correction-v1.md) — SHA-256 `219eefc14dcda02d4ea72e70682bcaf0fe9ea98d752cb25aacc79dcee64871b7`
- [非authority入力 採択Decision](records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md) — SHA-256 `2991aed38dd7e6f294774baa0ff98d664168bd8f2fffdc3337e7228938109af8`
- [Work 6A GREEN Evidence v1](records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md) — SHA-256 `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c`
- [Work 6A項目と既存Testの対応inventory](records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json) — SHA-256 `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16`
- [案A承認Decision](records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md) — SHA-256 `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `1bd743b0fd110342900996199b2a81eaf2b42440f28318f931e43a78b039a550`
- [機械操作の根本原因Issue](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`

## 次に行う一作業

Humanがchecklist CL-6A-08への完了印の可否と、恒久検査器をIssueレーンへ載せる形式を判断する。

開始条件：

- 拡大GREENと訂正recordを含むcommitがcleanであること
- Human判断が出るまでchecklistのcheckboxを変更しないこと

完了条件：

- CL-6A-08の完了可否がDecisionへ記録されること
- 恒久検査器の改善候補recordをどの形式で作るかが確定すること

後続作業：完了印を付ける場合はEvidenceを接続する。検査器は改善候補からHuman triage判断を経てIssueへ昇格させる。

## blocker・Human判断待ち

- blocker：なし。Current Work Projection正式写像、正式Portfolio／Work Item／Workflow state、Work 6Aの残り20項目は開始しない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：checklist CL-6A-08の完了可否。恒久検査器の改善候補recordの形式（過去TODO由来でない候補は既存2形式のどちらにもそのまま載らない）。

## stale・deferred

- stale：RED Evidence§8-2が挙げた壊れる既存test名と、GREEN Evidence v1が記述する定数名・関数名・診断文言・行番号は、訂正recordで置換した。旧recordは履歴として保持する。
- deferred：Current Work Projection正式写像、同じTestを変更しないrefactor後再確認、Work 6Aのうち承認範囲外20項目、入力側へのauthority宣言方式、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Work 6A negative 10 passed、隣接する既存projection関連13 passed
- 直近の全Test：venv公式runner 1017 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
