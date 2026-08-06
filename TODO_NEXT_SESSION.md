# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：本線Work 6Aを継続中。CL-6A-09を独立検証の上で完了し、被覆過大の3項目は訂正recordで残余を明示した。チェックリスト改定で仕分け済み候補の検証が壊れたため、N7・N9をHuman承認で改定し、テスト増加の改善候補を新規登録した。仕分け済み候補は歴史扱いとする。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提

## 最新のauthority／Evidence

- [N7・N9改定Decision](records/development/2026-08-06-intake-v4-n7-n9-amendment-decision-v1.md) — SHA-256 `e0dd5b4ba6c4a1e797cef59c2ba7727e68786303f5a78bbb1ab74962fddcef78`
- [CL-6A-09完了Decision](records/development/2026-08-06-work6a-cl-6a-09-completion-decision-v1.md) — SHA-256 `9a8a21dd1829c712e8903e5d0369dd40b147b83972a00267212dab8e5ddd87eb`
- [対応表の訂正record](records/development/2026-08-06-work6a-inventory-correction-v1.md) — SHA-256 `41b6e8436f437da1eccf911f2e34cff211d5959110ed91e18ce9ea4887bfcdc0`
- [テスト増加の改善候補](.reviewcompass/workflow/improvement-candidates/ic-test-growth-state-pinning-001--v1.json) — SHA-256 `88256c55a281b7449ab863db4c55bb5055abd6c6c622200a36a83eb77f68efa2`
- [テスト増加の観測record](records/development/2026-08-06-test-growth-state-pinning-observation-v1.json) — SHA-256 `d2c304aff35f22ae4cb53971194df957f2602d9f57def34fb33c18f1132130e5`
- [本日の問題一覧（14件）](records/development/2026-08-06-encountered-problem-inventory-v1.md) — SHA-256 `f6d8da5e6d95767a732e2280ec101df5188d9faac4d55621003c8bb5beb4763b`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `cf503cd8090dd78f58030378794be87a3156ac6afc4ffa41c16344fad5beb3c6`
- [登録した課題record](.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json) — SHA-256 `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`

## 次に行う一作業

HumanがIC-TEST-GROWTH-STATE-PINNING-001（テスト増加と状態釘付け）のtriageを裁定する。あわせてWork 6Aの次のRED対象（CL-6A-10のFinal Challenge専用負例）の提案可否を判断する。

開始条件：

- 本修復commitがcleanで全Testが緑であること
- 裁定直前に候補のv3 validatorを再実行すること

完了条件：

- 分類、blocking判定、route、Issue昇格可否が記録されること

後続作業：CL-6A-10の提案を作る場合、意図毀損を機械的に何で表すかの設計判断を先に固定する。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：テスト増加候補のtriage。CL-6A-10提案の作成可否。

## stale・deferred

- stale：仕分け済み候補IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001のevidence_refsは作成時点の固定として保持し、現行bytesとの一致は要求しない（N7・N9改定）。対応表のN9行の旧test名は改定Decisionが正本。
- deferred：Work 6Aの残り9項目、登録済み4課題の着手、テスト整理のWork 8測定、Current Work Projection正式写像、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Intake V4単体候補11 passed、Work 6A境界例1 passed
- 直近の全Test：venv公式runner 1032 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
