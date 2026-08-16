# 外部レビュア一回送信 実送信E2E Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5`（受入条件13）
- 利用者指示：実施承認、model `gemini-3.1-pro-preview`への変更指示、鍵の扱い（先行repo確立解の利用）、
  1回目停止後の(2)裁定（確認用文書で再実行・構造問題は改善候補登録）、送信実行の最終承認（すべて2026-08-16 chat）
- 実施担当：Claude（送信コマンドの実行を含む）

## 1. 鍵の扱い（先行repoの確立解）

【実測】このsessionのプロセス環境は認証系変数を保持しない（session前半にANTHROPIC系が存在し後に不存在と
なる消去挙動を2時点実測で確認。`~/.zshrc`には3 provider鍵とも登録あり）。このため、実行の瞬間に
`zsh -c 'source ~/.zshrc; …'`のサブプロセスで値だけをプロセス環境へ取り出し、1コマンド内で
「取得→渡す→実行」を完結させる方式（ReviewCompass `tools/api_providers/providers.py`の
`_read_api_key_from_zshrc`と同方式）を採った。鍵の値はchat・file・記録・logのどこにも現れない。

## 2. 1回目の安全側停止（送信指示v1・送信なし）

【実測】送信指示v1（資料：暫定体制決定record）は機微検査`sensitive_data_remaining`（source `order`・
終了コード3）で停止した。送信・台帳着地は起きていない（試行record着地前の停止）。原因は資料file名の
51文字hyphen連結（可読）への高乱雑性誤検知（エントロピー3.83）。代替候補（`pyproject.toml`・`AGENTS.md`・
開発方針）の内容も同検知で不合格となることを実測し、実用文書が現水準の検査でほぼ送信不能という構造問題を
特定した。観測record
`records/development/2026-08-16-egress-sensitive-scan-false-positive-observation-v1.json`と改善候補
`IC-EGRESS-SENSITIVE-SCAN-FALSE-POSITIVE-001`（検証器合格）として登録し、対処は後続契約に残した。

## 3. 2回目の成功（送信指示v2・本repositoryで最初の承認済み外部送信）

【実測】検査合格を事前実測した確認用文書`docs/development/e2e-live-send-check.md`（commit済み）を資料と
する送信指示v2で再実行し、成功した。

- 実行：`reviewcompass3-gemini-send send --order …/2026-08-16-g20-live-e2e-order-v2.json`、終了コード0、
  標準エラー0 bytes
- 結果：`status: response_stored`、HTTP 200、`completed_at: 2026-08-16T08:30:47Z`
- 台帳着地（`.reviewcompass/egress-ledger/`）：`ORD-G20-LIVE-E2E-001--attempt-v1.json`（834 bytes）→
  `--response-v1.raw`（4,905 bytes・無加工）→`--result-v1.json`（530 bytes）の順。試行record計数1件
- `payload_sha256`：`69da2e0ad542a27c16530528d4879c91cc37f87dddb711e5d5cb2ee5fe58ad28`
- `response_sha256`：`b5de842f283666f8ce6b6c25b54b26e1cea748e5df0e74ab7a0cc31c50f9f6b6`

## 4. 機械検証

【実測】

- attempt・resultの`record_sha256`：独立再計算と一致
- 応答fileのSHA-256・bytes数：結果recordと一致。標準出力は結果recordと同一bytes
- 鍵の非出現：台帳3 file＋送信指示v2の全bytes走査で0件（鍵値はプロセス内比較だけで出力していない）
- 応答本文：宛先modelは指定どおり`gemini-3.1-pro-preview`（応答内`modelVersion`）。依頼どおり資料の
  受領確認が日本語で返り、資料pathと宣言digestを正しく引用していた
- 台帳3 fileはcommit `54524ab`で履歴へ固定（§7.3の運用）

## 5. 契約対応

受入条件13「利用者の指示の下で実送信E2Eを一回行い、試行record・応答保存・結果record・台帳計数を実環境で
確認する」を充足した。送信は一回だけであり、1回目の停止は送信前の安全側停止（送信回数0）である。

## 6. 未実施

- 製品受入（受入条件14）。限界明示（縮小境界＋機微検査誤検知の構造問題）つきで次に提示する。
- 機微検査精密化（改善候補として登録済み。Human仕分け待ち）。
