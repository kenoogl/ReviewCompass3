# 契約010 実E2E第5試行（e2e-010-005）Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 実施根拠：利用者の明示指示「e2e-010-005で再実施して」（chat）
- 結果：**停止（`verdict_schema_nonconforming`・終了コード2）。§9-8は未成立のまま**

## 1. 実施と停止【実測】

- 起動：同一対象・同一期待SHA-256、run-id `e2e-010-005`、第4試行の訂正済みprompt（絶対path明示）。
- Reviewerは指示どおり最初の操作で`view_file`を**正しい絶対path**
  （`/Users/Daily/Development/ReviewCompass3/records/session-handoffs/…`）へ実行した。しかし
  `User denied permission for read_file(…)`——**repository内のfileでも読取り承認が必須**で、headless
  では自動拒否→会話終了→`result.response`空→構造不適合停止。
- 消費：入力20,292 token・出力532 token。agy process終了コード0。raw・起動recordは
  `e2e-010-005/`へ不変保存。

## 2. 判明した事実（許可模型の確定）【実測】

1. 既定の許可方式`request-review`では、**fileの中身の読取り（read_file系。view_file・grep_searchを
   含む）はrepository内外を問わず承認必須**。headlessでは承認者不在で自動拒否となる。
2. `list_dir`（一覧）は承認不要（第3・4試行で成功）。
3. `--mode=plan`は許可方式を変えない（5試行連続で`permission_mode: request-review`）。
4. 拒否＝会話即終了・最終応答空、のpatternは4回連続で再確認。
5. 局所調査（送信なし）：agent定義はCLIから一覧のみで作成不可。`~/.antigravity/`等の設定置き場に
   許可規則の保存fileは見当たらない。

## 3. 次の一手（本Evidenceで適用した訂正）

- 固定引数へ`--sandbox`（端末制限つきsandbox実行）を追加した。契約§7.1が「sandbox・作業ディレクトリの
  扱いはRED段の実測で確定」と留保した事項の確定の続きであり、制限を強める方向の旗である。sandbox内では
  読取りが自動許可される可能性を検証する（不成立でも安全停止のみ）。
- 対象試験の固定引数検査を追随。対象33件単独緑（本Evidence記録時点）。

## 4. 見えている代替（次回も読取り拒否の場合）

1. 利用者の対話sessionでの事前許可：利用者がagyを対話で開き、read系道具へ「常に許可」を与えて
   規則が保存されるかを確認する（保存先と headless への効き方は未実測）。
2. 契約改定による方式転換：依頼内容をprompt本文へ埋め込む方式は§7.1（依頼内容の複製禁止）と
   byte上限に抵触し、かつ完了レビューのようにrepository内の複数実装fileを読む用途では成立しない。
   採る場合は範囲の再定義が必要（現時点では非推奨）。

## 5. 残り

- §9-8実E2Eは未成立。再実施は新識別子`e2e-010-006`で利用者指示を得て行う。
