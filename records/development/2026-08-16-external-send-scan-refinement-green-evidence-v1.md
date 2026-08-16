# 機微検査精密化・改名 実装成功Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-EXTERNAL-SEND-SCAN-REFINEMENT-009 / v2`（採用済み）
- 採用判断：`records/development/2026-08-16-external-send-scan-refinement-adoption-decision-v1.md`
  （commit `3d3773d`）
- 実装担当：Claude
- 方式：改名（挙動不変・全緑確認）→失敗試験の固定→最小実装→退行確認

## 1. 改名（契約§8）

【実測】commit `0762748`。`gemini_send.py`→`send.py`、`gemini_send_entry.py`→`send_entry.py`、
`tests/test_gemini_send.py`→`tests/test_external_review_send.py`、実行名
`reviewcompass3-gemini-send`→`reviewcompass3-external-review-send`。挙動不変で対象49件全緑、
コード・設定・試験から旧名（`gemini_send`・`gemini-send`）の残存0を全文検索で確認。歴史的record・
台帳の旧名表記は不変。

## 2. 失敗試験の固定（RED）

【実測】commit `b9458cb`（試験1 fileのみ）。受入条件1〜3の12試験を追加し、精密化を要する3件
（可読な長いhyphen連結file名の資料・40/64桁hexと下線連結や大文字IDを含む文書・purpose内の正規hex記載が
停止しないことを期待）だけが現実装で失敗（`3 failed, 58 passed`）。乱雑列6種＋39/41/63/65桁境界hexの
停止維持9試験は現実装でも合格（維持の固定）。

## 3. 最小実装（GREEN）

【実測】契約§9の変更上限内で`tools/external_review/send.py`だけを変更した。

1. §7.1の除外3形式（X1a・X1b・X2）を契約固定の定数`_HIGH_ENTROPY_ALLOW_PATTERNS`として直書き
   （設定・環境・引数・送信指示から変更不能）。
2. `_scan_text`へ`allow_high_entropy_exclusions`引数を追加し、`find_high_entropy`の公開引数
   `allow_patterns`へ渡す（`redaction.py`は無変更）。既定5 pattern検査は全fieldで従来どおり。
3. §7.2の出し分け：`_scan_order`のJSON走査で`path == ("order_identifier",)`のときだけ除外なし
   （乱雑識別子の停止仕様を維持）。由来file内容の検査（`_build_payload`経由）は除外適用。

## 4. 機械確認（各単独command・終了コード個別判定）

【実測】

- 対象試験：61件成功、終了コード0（既存49件＋精密化12件。RED 3件がGREENへ、敵対9件は維持）
- egress関連：107件成功、終了コード0
- G02対象158件・G08対象107件・G24対象111件・実行器75件・G30基盤e2e 38件：各単独成功、終了コード0
- 保護path（契約v2固定commit `76a1050`からの差分：redaction.py・egress 7 module・task_contract 5 file・
  受入済み4製品とその試験）：差分0、終了コード0
- 正規全試験（禁止認証隔離条件）：2,375件成功、終了コード0
- `git diff --check`：終了コード0

## 5. 本線中の別件対処（利用者承認済み・独立commit）

【記録】正規全試験で、契約008実送信E2Eの未加工応答台帳file内のbase64値を、layout境界検査が絶対pathと
誤検知する既存衝突が顕在化した（契約009の変更とは独立）。利用者承認(1)の下、検査部品へ台帳応答raw
（`--response-v1.raw`固定名）の除外を加え、除外意図を固定する試験1件を追加した（commit `3e9a9f7`、
layout 13件・正規全試験2,375件全緑）。

## 6. 訂正後の内容識別値

| path | SHA-256 |
| --- | --- |
| `tools/external_review/send.py` | `fcecb2e35ffca0b6341cd7e102c4e6f0dc8b7b5871c36d87b8eae0a07a8d0197` |
| `tools/external_review/send_entry.py` | `ebe8f0b4908493d464fdb8e39bfe09d59c1fa8e16b1dec643e2e79d4f7dcdd5e` |
| `tests/test_external_review_send.py` | `b0c1628cda54e5a1ddb562354d9c0158439cc0b8d83b4f4aa7a5c163b5c82759` |
| `pyproject.toml` | `b56851fa65aa9b30a98413c059d385b97daa874fdea960c93c01c0cde26e69d3` |

## 7. 未実施

- 独立完了レビュー（受入条件7。暫定体制：Gemini・Human中継）
- 実用文書の実送信E2E一回（受入条件8。利用者指示による）
- 製品受入（受入条件9。残余riskの最終受容を含む）
