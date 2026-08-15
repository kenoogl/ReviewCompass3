# Session記録安全保存 独立完了再レビュー v2

- 実施日：2026-08-15
- 対象HEAD：`555f9a1a0f4390d4f38f0a3a0f83ea5e0043b46a`
- 前回：独立完了レビューv1 `修正要` 4件
- 方式：同じ独立担当、read-only、repository外合成反例

## 結論

`修正要`

【実測】前回4指摘のうち、片root中断、operation authority、監査印再利用は解消した。途中製品出力は初回保存中断と
削除中断では解消したが、保存再開中の再中断に残差があった。新しい範囲拡張、秘密出力経路、既存正式入口変更は0件だった。

## 残る止める指摘

1. **重大：確定印公開直前の有効な途中状態を削除計画できない。**
   契約§8.2、§8.5、受入条件12は、両operationが`committed`でも`commit.json`未公開なら状態を`incomplete`として
   中止可能にする。実装は一度両stateを許すが、共通validatorへ`incomplete`だけを渡して`record_conflict`となった。
   表示stateは`incomplete`のまま、validatorだけ`incomplete/committed`双方を許す必要がある。
2. **重大：保存再開中の再故障が`incomplete/3`を維持せず例外詳細を出す。**
   契約§8.5、受入条件19に反する。初回raw公開後停止は`incomplete/3`だが、同じ入力での再開中に派生物公開後で再停止すると
   `stopped/4`となり、注入した例外詳細がJSONへ出た。安全なoperation照合後に再開処理を始めた場合だけ、再故障も固定した
   `StorageIncomplete`へ変換する必要がある。既存不一致や事前属性違反は`stopped`のままにする。

【実測】受入条件1から21の未接続は2件、条件12と19である。条件17を含む前回operation authority違反は解消した。
条件22のHuman受入へはまだ進めない。

【実測】対象95件、関連30件は終了コード0、全試験receiptは1,860件成功だった。追加診断は
`precommit_plan=record_conflict`、初回中断`[3,incomplete,例外詳細なし]`、再開中断
`[4,stopped,例外詳細あり]`を返した。独立担当による成果物・Git index変更は0件、最終worktreeはcleanだった。
