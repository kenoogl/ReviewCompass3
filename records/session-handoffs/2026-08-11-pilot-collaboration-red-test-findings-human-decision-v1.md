# 操縦者別連携 RED受入テスト所見 Human裁定 v1

- 日付：2026-08-11
- 裁定者：Human
- 裁定文言：`RT-PC-001〜004を全件採用する`
- 裁定文言の出典：本作業の会話
- 対象所見：`RT-PC-001`、`RT-PC-002`、`RT-PC-003`、`RT-PC-004`
- 対象レビュー：`records/session-handoffs/2026-08-11-pilot-collaboration-red-test-review-v1.md`
- 対象レビューSHA-256：`6cf381e20fd4bc1f18d808d0b2237a94cf434a35ddfef8780e1374cc3b295607`
- 対象RED commit：`df48bbafe29b62e2efe26e0e7b1ddebc75e47f2b`
- 裁定：`accept_all_for_red_test_revision`

## 裁定内容

新規テスト4件だけを変更し、次を反映する。

1. 禁止されたprocess起動経路を直接の`subprocess.run`と文字列リテラルだけに限定せず検出する。既存保存処理の
   共通境界使用は、未使用importだけで合格しない確認へ変える。
2. launch記録のraw SHA-256不一致と、判定rawの`audit_parsed_sha256`不一致を故障注入し、保存、停止code、
   非解析を確認する。
3. 要求対応表が参照するtest関数の実在を機械照合する。
4. 変更範囲testは実行時のHEADとworktree全体を使わず、固定した実装対象commit範囲だけを検査する。

修正後は各test fileの単独RED、計50件の収集、既存1470件、差分検査を再実行し、別の新しい会話状態で
再レビューする。再レビューが`verified`になるまでproduction実装へ進まない。
