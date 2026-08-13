# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段は401件の候補列挙と最初の一件の予備調査まで進んだが、整理判断の範囲が狭かったため、意味的な全体単位での再評価へ戻る。
- 現在作業：最初の候補について、履歴対応表を現在状態の合否判定器として扱った独立レビューの裁定と、一関数だけを最小単位とした選定の双方を未採択とした。整理・削除は役割分類と総費用で判断する方針を正本へ追加し、新規Codexの変更点限定レビューはverified、Claudeへの手動受け渡し待ちである。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 現在有効性を再判定済み / 401件列挙完了 / 最初の候補群を再評価待ち`、影響：試験一件だけの局所判断では、現在保証と履歴資料の役割、保持・削除・修正連鎖・将来調査の総費用を取り落とす、次：当該試験と関連するRED／GREEN証跡、宣言対応表、現在保証、正規入口を一つの候補群として読み取り再評価する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [整理判断の範囲・役割・総費用 方針採用判断v1](records/development/2026-08-13-cleanup-decision-scope-and-lifecycle-policy-adoption-v1.md) — SHA-256 `a6eb37969e7c16b97f970e76b08b9b9a082ffba2336019a69ae0db4aa23778c5`
- [試験増加・状態固定Issue現在有効性の再判定v1](records/development/2026-08-13-test-growth-state-pinning-current-validity-decision-v1.md) — SHA-256 `1609dfdd76b25c86b38bd105f4199cbbc1636614c5f68256fdee61879c3bddac`
- [整理判断方針のCodex変更点限定レビューv1](records/development/2026-08-13-cleanup-decision-scope-policy-delta-review-v1.md) — SHA-256 `a4fed4dcd6e8cd5849ae97618a334fd345c05aa2925af135ac225166aae6528f`
- [Claude向け整理判断方針の変更点レビュー指示v1](records/session-handoffs/2026-08-13-claude-cleanup-decision-scope-policy-delta-review-prompt-v1.md) — SHA-256 `2d43a86a93ba69c363aa938c4bd4b2efc8ee8cbcfc3a21b83147a5bb1c46a275`

## 次に行う一作業

第3段の読み取り調査として、最初の候補を一関数ではなく意味的に関係する成果物群として再評価する。試験、対応表、証跡、コード、設定は変更しない。

開始条件：

- Codexと利用者が手動で受け渡すClaudeの変更点限定レビューが完了し、文言、導線、既存方針との矛盾に止める指摘がない
- 対象試験、RED／GREEN証跡、宣言対応表、現在の関連試験と正規入口のpath・参照・時点を機械列挙する
- 履歴時点の対応表を現在状態の合否判定器として使わず、観測した不一致と現在欠陥の裁定を分ける

完了条件：

- 各構成物を現在の動作保証、履歴・監査資料、両方、役割終了へ分類し、意味的に完結した最小単位を示す
- 維持、整理、別候補へ移る三案について、反復費用、一回費用、修正連鎖、将来調査・監査費用、回復可能性、増加誘因を比較する
- 選んだ境界が狭すぎないかを独立レビューで反証し、削除・統合・使用停止をせず利用者判断へ渡す

後続作業：利用者が候補群の境界、役割分類、危険度、実施案を判断した後、その意味単位だけの作業票と開始確認へ進む。

## blocker・Human判断待ち

- blocker：Claudeの変更点限定レビュー未完了。現在候補の削除または撤回は未承認である。
- Human判断待ち：Claudeへ固定指示を手動で渡し、結果を戻す。その後の再評価で、最初の整理単位を当該候補群とするか、維持するか、別候補へ移るかを判断する。

## stale・deferred

- stale：一関数だけを最小整理単位とする案、および履歴対応表の現在不一致だけを削除案の停止根拠とする裁定は、再評価完了まで採否に使わない。
- deferred：401件の残りの内容分類と試験削減、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体的な変異検査、外部実装経路の再開と保証範囲再裁定。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：現行の履歴対応表を現在試験へ照合すると、既存の欠落2件・未対応15件でfailed。これは時点の違いを示す観測であり、現在欠陥の裁定には用いない。Codex変更点限定レビューはverified、止める指摘0件、報告不一致0件。
- 直近の全Test：直近の公式入口は1,739件成功、失敗・エラー・除外0、Python 3.13.14、代替実行なし、終了コード0。本方針変更では再実行しない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
