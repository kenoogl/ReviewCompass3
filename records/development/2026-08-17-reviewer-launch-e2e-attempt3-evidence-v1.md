# 契約010 実E2E第3試行（e2e-010-003）Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 実施根拠：利用者の明示指示「e2e-010-003で再実施して」（chat）
- 結果：**停止（`verdict_schema_nonconforming`・終了コード2）。§9-8は未成立のまま**。model照合は
  今回から通過し、停止点はさらに先へ進んだ

## 1. 実施と停止【実測】

- 起動：同一対象・同一期待SHA-256、run-id `e2e-010-003`、第2試行の訂正済み引数
  （`--mode=plan`・`--print=<本文>`・訂正済み固定prompt）。
- agy process終了コード0。未加工出力・起動recordは私有領域`e2e-010-003/`へ不変保存。
- 消費：入力25,497 token（うちcache読取り16,245）・出力1,713 token。

## 2. 判明した事実【実測】

1. model照合は通過（`init.model`＝`gemini-3.1-pro-high`。第2試行の解析訂正が有効）。
2. `--mode=plan`を渡しても`init.permission_mode`は`request-review`のままだった（許可方式の表示は
   変わらない）。
3. **作業領域内の読取りは自動許可される**：Reviewerの`list_dir`はDONE（成功）。
4. 停止の真因：2手目の`grep_search`が**作業領域外`/Users/keno`（利用者home）を読もうとして自動拒否**
   （`User denied permission for read_file(/Users/keno)`）となり、会話がその時点で終了、最終
   `result.response`が空文字列→`verdict_schema_nonconforming`で停止（第2試行で追加した停止試験の
   事象と同型）。
5. 拒否＝会話即終了のpatternが再確認された（拒否をReviewerへ返して続行させる機構はない）。
6. 副次確認：作業領域外への読取りは機械層で拒否される（repositoryの外が読めない境界が実測で確認
   された。これは契約§7.4-1の緩和として働く事実）。

## 3. 訂正【実測】

- 固定promptへ2点を追加：(1)「現在のdirectory（作業領域）内だけを相対pathで読み、作業領域外へは
  一切アクセスしない（自動拒否＝レビュー終了）」、(2)「最初の操作としてview_fileで対象依頼record
  （相対path）を開く」。探索系道具（grep_search等）が領域外へ向かう誘因を断つ。
- 対象試験の固定要素検査へ`view_file`・`作業領域`の2 assertionを追加。
- 検証：対象試験33件単独緑（本Evidence記録時点）。

## 4. 残り

- §9-8実E2Eは未成立。再実施は新識別子`e2e-010-004`で利用者指示を得て行う。
- 残る未知：view_fileから始めた場合にレビュー全体（複数file読取り→構造化出力）が完走するか、
  `--json-schema`の強制が最終`response`へ働くか。
