# 第3段 G06共通処理試験整理 作業票 v1

- 作成日：2026-08-14
- 状態：`approved / implementation_pending`
- 基準commit：`f879af5`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 危険度：`high（既存試験の意味変更と削除）`
- 作業担当：操縦役
- 完了レビュー担当：新規サブエージェント
- Human承認：2026-08-13、G06案Bを承認。2026-08-14、先行するWork 5B整理完了

## 1. 目的

G06の現在保証を維持しながらlist再帰の見逃しを閉じ、固有保証のない三試験を整理する。

## 2. 入力と根拠

- G06訂正済みEvidence：`records/development/2026-08-13-stage3-g06-common-guards-reassessment-evidence-v1.md`
- G06限定修正後確認：`records/development/2026-08-13-stage3-g06-common-guards-reassessment-correction-review-v1.md`
- Work 5B整理後の正規全試験：1,731件成功

## 3. 作業範囲と対象外

変更対象は`tests/test_common_digests.py`一件と実施Evidence一件だけ。

- `{"nested": {"items": (1, 2)}}`を`{"items": [(1, 2)]}`へ置換する。
- `test_distinct_values_never_share_a_digest`の二つの引数別試験を削除する。
- `test_real_ledger_records_keep_their_digest`一件を削除する。

経路五件、非文字列key、tuple、非有限数、set、bytes、Task Contract三境界、正常文書三件は維持する。
製品コード、他試験、設定、記録・台帳、正本、TODOは変更しない。新しい試験・検査器・台帳を作らない。

## 4. 期待する成果

- G06は24件から21件、関連四fileは87件から84件になる。
- list要素の再帰検査を外す欠陥を置換一件が検出する。
- 正規全試験は1,731件から三件減の1,728件で成功する。

## 5. 機械確認

1. G06 21件と関連四file 84件を単独実行する。
2. リポジトリ外複製でlist要素の再帰検査を外し、置換一件が失敗することを確認する。
3. 正規入口から全試験を実行し、1,728件成功を確認する。
4. Git差分、構文木、`git diff --check`で変更範囲と残る条件を確認する。

## 6. レビュー事項

新規サブエージェントが一回の独立完了レビューで、三件だけの整理、list再帰検出、残す保証、全試験、禁止事項を確認する。

## 7. 停止・完了条件

対象一file以外の試験・コード変更、期待件数不一致、関連試験または全試験失敗、別の現在利用者の発見で停止する。
承認範囲の実施、全確認成功、結果commit、独立レビュー`verified`、作業遷移成功で完了する。
