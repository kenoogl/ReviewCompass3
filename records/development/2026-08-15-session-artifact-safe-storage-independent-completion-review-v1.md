# Session記録安全保存 独立完了レビュー v1

- 実施日：2026-08-15
- 対象HEAD：`c0eeed76d1f7b59a99694c09c34936c040a6b8c1`
- 担当：開始前レビュー担当とは別の独立担当
- 方式：read-only、repository外の合成fixtureによる限定反証

## 結論

`修正要`

【実測】対象85件と関連30件は終了コード0、最終EvidenceのDigest、全試験receipt、HEAD、clean状態は一致した。
一方、製品受入を止める独立原因4件を再現した。

## 止める指摘

1. **重大：片rootだけ残った保存中断を再開も中止もできない。**
   契約§8.5、受入条件12は片方の有効operationからの再開または確認済み中止を要求する。sensitive側だけに
   有効な`operation.json`を残すと、`plan-delete`は成功するが、`store`再試行は`record_busy`、`delete`は
   `record_unrecoverable`となった。欠けた側を完全照合後だけ安全作成する必要がある。
2. **重大：operation schemaと記録内容を利用時点で照合していない。**
   契約§8.2、§8.4、§8.5、受入条件17に反する。両rootの正準operationから`raw.bin`を除いても計画はrawを
   対象化し、期待raw SHAを偽値へ変えても`delete_planned`となった。固定schema改変後に`load-derived`が
   `loaded`となる反例も成立した。完全な共通validatorと実在本文Digest照合が必要である。
3. **重大：監査印公開後の再試行が再提示時刻に依存する。**
   契約§3責務7、§8.7に反する。`deleted.json`作成後・operation除去前に停止し、同じ確認値と1秒後の
   `deleted_at`で再試行すると、監査印を再生成して`record_conflict`となった。既存の有効監査bytesを正本として
   操作情報除去だけを続ける必要がある。
4. **高：途中失敗の製品出力区分がない。**
   契約§8.5の`incomplete`と§8.7の`deletion_incomplete`が製品入口・試験に存在せず、全`StorageStop`を
   `stopped`へ平坦化している。有効operationが残る書込み後失敗だけを途中結果へ変換し、事前拒否と区別する必要がある。

【実測】受入条件1から21の番号付き未接続は2件、条件12と17である。加えて契約本文に固定された監査印公開後の
再試行と途中出力区分が未実装であるため、条件22のHuman受入へ進めない。

## commandと変更確認

【実測】`.venv/bin/python3`による対象85件と関連30件は成功した。repository外合成診断は
`one_root_incomplete_store_retry=record_busy`、`one_root_incomplete_delete=record_unrecoverable`、
`changed_deleted_at_retry=record_conflict`、`false_expected_digest_plan=delete_planned`、operation意味改変後の
load=`loaded`を返した。片側`operation.json.tmp=deleting`の同じ確認値再試行は成功した。

【実測】独立担当による製品code、試験、契約、Evidence、TODO、Git indexの変更は0件で、最終worktreeはcleanだった。

【判断】最終検証Evidence v1と同時点のTODO完了表示は、本指摘の修正・再検証・独立再レビューまでstaleとする。
