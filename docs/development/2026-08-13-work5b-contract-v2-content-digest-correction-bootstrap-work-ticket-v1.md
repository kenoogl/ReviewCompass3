# Work 5B契約v2 内容識別値限定訂正 作業票 v1

- 作成日：2026-08-13
- 状態：`approved / implementation_pending`
- 現在段階：立て直し計画v5 第3段
- 基準commit：`999469f`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`から分離した現在参照中の記録不一致
- 対象種別：構造化された記録・宣言データ
- 危険度：`medium`
- 作業担当：操縦役
- 完了レビュー担当：新規サブエージェント
- Human承認：2026-08-13、利用者がG06案Bと分離し、本訂正を先に実施する順序を承認

## 1. 目的

`records/development/2026-08-07-work5b-implementation-task-contract-v2.json`について、
2026-08-10の承認済み変更で取り残された自己の`content_digest`だけを、現在内容から一意に再計算した値へ訂正する。
契約本文、識別子、版、固定参照、受入条件、履歴の意味は変更しない。

## 2. 入力と根拠

- G06訂正済みEvidence：
  `records/development/2026-08-13-stage3-g06-common-guards-reassessment-evidence-v1.md`
- G06限定修正後確認：
  `records/development/2026-08-13-stage3-g06-common-guards-reassessment-correction-review-v1.md`
- 変更原因commit：`f8c01b5`
- 変更原因Evidence：
  `records/development/2026-08-10-official-oracle-fix-evidence-v1.md`
- 内容識別値の現行正本：`tools/common/digests.py::canonical_content_digest`
- 現在利用者：`tests/test_work5b_contract.py`

【実測】基準commitでは宣言値が
`3f865f8603a99f2698628c60c2a7ea6a9e7dd47e50b2d1134fd7babd542cbe59`、
現在内容からの再計算値が
`32a26be73b2a98126559f62303da3556198b1ebc82057048128e604a63646f7e`であり、一致しない。
`f8c01b5`は固定試験fileのSHA-256一箇所をHuman承認のうえ更新したが、自己の`content_digest`を更新しなかった。

## 3. 作業範囲と対象外

変更対象は次の一file・一値だけとする。

- `records/development/2026-08-07-work5b-implementation-task-contract-v2.json`
  - `content_digest`を旧値から再計算値へ置換する。

対象外：契約本文、固定参照、v1、試験、製品コード、検査コード、設定、正本、チェックリスト、G06試験整理、
他の内容識別値付き記録、全記録走査、新しい検査器・試験・台帳、外部送信、履歴書換え、第3段完了判断。

本作業は実装方法を選ぶ変更ではなく、内容から一意に定まる値の機械的訂正である。現行開発方針の例外に従い、
三案比較を行わない。コードの振る舞い変更でもないため、赤緑の試験追加を行わない。

## 4. 期待する成果

- 対象recordがJSONとして読める。
- `record_kind`、`task_contract_id`、`task_contract_version`、`fixed_sources`、`work_items`など、
  `content_digest`以外の内容は基準commitと同一である。
- 宣言した`content_digest`が、現行共通処理と標準JSON・SHA-256による独立計算の双方に一致する。
- `tests/test_work5b_contract.py`の六件が成功する。

## 5. 機械で確認する事実と正規入口

1. Git差分から、変更pathが対象record一件、変更内容が`content_digest`一値だけであることを確認する。
2. Pythonの標準JSON処理で読み込み、`content_digest`を除外した正準JSONからSHA-256を独立計算する。
3. `tools.common.digests.canonical_content_digest`の結果とも一致することを確認する。
4. 対象recordから`content_digest`以外を除いた基準commitとの比較が同一であることを確認する。
5. `.venv/bin/python3 -B -m pytest -q tests/test_work5b_contract.py`を単独実行する。
6. 一時入力で本文一値を変更した場合に、宣言値との不一致を独立計算が検出することを確認する。
7. `git diff --check`を実行する。

## 6. レビューで判断する事項

新規サブエージェントが一回の独立完了レビューで、次を確認する。

- 2026-08-10の承認済み変更から導かれる機械的訂正だけで、履歴の意味変更ではないか。
- 変更範囲が一file・一値だけか。
- 共通処理とは別の独立計算でも新しい値が一致するか。
- 形式、識別子、版、上流参照、欠落、重複、改変入力の観点で不整合を増やしていないか。
- 関連六試験が成功し、禁止した新機構を増やしていないか。

## 7. 停止条件と完了条件

次の場合は停止する。

- `content_digest`以外の変更が必要になる。
- 別record、試験、コード、設定、正本の変更が必要になる。
- 独立計算と共通処理の値が一致しない。
- 関連試験が失敗する。
- 契約の意味変更または新しいHuman裁定が必要と判明する。

完了条件は、対象一値の訂正、§5の全確認成功、意味的に完結した結果commit、独立完了レビュー`verified`、
作業単位遷移検査の成功である。完了後は別作業としてG06案Bへ進む。
