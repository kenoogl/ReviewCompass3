# 契約010 実E2E第4試行（e2e-010-004）Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 実施根拠：利用者の明示指示「e2e-010-004で再実施して」（chat）
- 結果：**停止（`verdict_schema_nonconforming`・終了コード2）。§9-8は未成立のまま**

## 1. 実施と停止【実測】

- 起動：同一対象・同一期待SHA-256、run-id `e2e-010-004`、第3試行の訂正済みprompt（作業領域内・
  view_file開始）。
- agy process終了コード0。未加工出力・起動recordは私有領域`e2e-010-004/`へ不変保存。
- 消費：入力32,255 token（うちcache読取り56,866の表示。累計計上とみられる）・出力3,934 token。

## 2. 判明した事実

1. 【実測】step列：agent_response→`error_message`2回（中身のない標識step）→`list_dir`成功
   （作業領域内）→**実在しない絶対path`/workspace`への`list_dir`が自動拒否**
   （`User denied permission for read_file(/workspace)`）→会話終了→`result.response`空→
   構造不適合停止。
2. 【推測（状況証拠つき）】読取り道具のpath引数は絶対path要求である。根拠：(a) 道具引数名が
   `AbsolutePath`・`SearchPath`（第3・4試行のstep記録で実測）、(b) 「相対pathで読む」指示の直後に
   error_message 2回、(c) その後Reviewerが`/workspace`という絶対pathを推測して拒否死。
   error_message stepに詳細が載らないため断定はできないが、絶対pathを与える訂正は推測が外れて
   いても安全側である。

## 3. 訂正【実測】

- `build_prompt`へ対象repositoryの絶対pathを引数追加し、固定文面を訂正：対象repository（作業領域）の
  絶対path・対象依頼recordの絶対pathを明示し、「読取り道具のpath引数にはrepository配下の絶対path
  だけを渡す」「最初の操作はview_fileで対象recordの絶対pathを開く」へ変更。呼出し3箇所
  （launch_review・G30入口・試験）を追随。
- 対象試験の固定要素検査へ絶対path 3 assertionを追加。
- 検証：対象試験33件単独緑（本Evidence記録時点）。

## 4. 残り

- §9-8実E2Eは未成立。再実施は新識別子`e2e-010-005`で利用者指示を得て行う。
- 残る未知：絶対path指定でview_file→レビュー完走→`--json-schema`強制の実効。
- 観察メモ：拒否＝会話即終了のpatternは3回連続で再確認。私有領域の起動record・rawは4試行分が
  不変保存されており、反復の監査線として機能している。
