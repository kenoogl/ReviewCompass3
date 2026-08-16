# 機微検査精密化・改名 独立完了レビュー依頼record v1（Claude→Gemini・Human中継）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・実装担当）
- 依頼先：Gemini（暫定体制。本repositoryのディレクトリを共有しており、対象fileを直接読める）
- 体制根拠：`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`
- レビュー種別：実装完了後の独立完了レビュー（契約v2受入条件7。読取り専用・repositoryへの書込みなし）
- 5段手続き：第1・2段（起草側自己レビューと文脈整理）は
  `records/development/2026-08-16-external-send-scan-refinement-impl-self-review-v1.md`として固定済み
- 先行判定：契約候補v2の独立確認`開始可`（あなた自身の判定）
  `records/development/2026-08-16-external-send-scan-refinement-v2-independent-review-v1.md`

## 1. 対象と固定

- 実装commit（GREEN）：`0665120`（除外3形式の定数直書き＋identifier出し分け＋Evidence＋TODO）
- 先行commit：改名`0762748`（挙動不変）、RED`b9458cb`（3 failed, 58 passed）、
  layout除外の独立対処`3e9a9f7`（利用者承認済みの別件）
- 採用中の契約v2：`records/task-contract/2026-08-16-external-send-scan-refinement-candidate-v2.md`
  - SHA-256：`58e5f9165e2201892377744377a9758f79be7559fe26f82ed114ec246968e6da`
- 実装成功Evidence：`records/development/2026-08-16-external-send-scan-refinement-green-evidence-v1.md`
  - SHA-256：`9e001507dcc4b39c840e6345a9ed708acdaf19b848a6a211bfd9cdae07ddb7f7`
- 起草側自己レビュー：`records/development/2026-08-16-external-send-scan-refinement-impl-self-review-v1.md`
  - SHA-256：`e0e4a287ba0448da858942adf979c5c43ef12e92a97994a4889c486bae911ce0`
- 製品成果物：

| path | SHA-256 |
| --- | --- |
| `tools/external_review/send.py` | `fcecb2e35ffca0b6341cd7e102c4e6f0dc8b7b5871c36d87b8eae0a07a8d0197` |
| `tools/external_review/send_entry.py` | `ebe8f0b4908493d464fdb8e39bfe09d59c1fa8e16b1dec643e2e79d4f7dcdd5e` |
| `tests/test_external_review_send.py` | `b0c1628cda54e5a1ddb562354d9c0158439cc0b8d83b4f4aa7a5c163b5c82759` |
| `pyproject.toml` | `b56851fa65aa9b30a98413c059d385b97daa874fdea960c93c01c0cde26e69d3` |
| `tools/layout/baseline.py`（独立対処） | `1e240112be0152af433061171cc2418632b565e080442a6182bd36a3e3969a97` |
| `tests/test_layout_baseline.py`（独立対処） | `2a4bf5e01e6b9050fe6be50db923d24d1107fee4a3222bb2ebea04404f74ef52` |

## 2. 開始時の鮮度検査（Gemini（あなた）が最初に行う）

1. §1の対象file（契約v2・Evidence・自己レビュー・製品成果物6件）のSHA-256を機械計算し、本record記載値
   との一致を確認する。
2. 可能なら`git status --short`が空であることを確認する。
3. 不一致の場合は、レビューせずその旨を判定文へ書いて停止する。

## 3. Gemini（あなた）への依頼：反証4点

あなたは独立したレビュアです。対象fileを直接読み、次の4点を反証的に検査し、判定を返してください。
各主張には根拠（契約の節番号、fileの関数名・行の内容）を付けてください。

1. **誤合格**：対象試験61件が実装の欠陥を見逃す構成になっていないか。特に精密化12試験（RED 3件＋敵対9件）が
   契約§7の除外3形式と適用範囲を固定する検出力を持つか、境界値（39/41/63/65桁hex・断片20字・
   hex外文字要求）の網羅に穴がないか。
2. **未接続**：§7.2の出し分けが全検査経路で契約と一致するか——`_scan_order`のJSON走査（field値・
   dict key名）、`_build_payload`の由来file内容、`order_identifier`だけの除外なし。適用すべき場所への
   適用漏れ、適用してはならない場所への適用がないか。
3. **禁止作用**：除外が契約の3形式・適用範囲の外へ漏れていないか——定数が設定・環境・引数から変更可能に
   なっていないか、既定5 pattern検査が弱まっていないか、`redaction.py`・egress 7 module・受入済み4製品が
   不変か（Evidenceの保護差分0と矛盾しないか）。
4. **上位目的への悪影響**：改名の完全性（コード・設定・試験の旧名残存0、歴史的recordは不変）と、
   layout検査の応答raw除外（独立対処）が境界検査の趣旨（自作成果物への絶対path混入禁止）を
   損なっていないか（除外は台帳固定名`--response-v1.raw`だけで、他fileの検知維持が試験で固定されているか）。

## 4. 判定の形式（あなたに求める出力）

- 判定：`verified`（4類型すべて0件）または`修正要`
- `修正要`の場合：最小数の指摘と各指摘の最小修正案。blocking／non-blockingを区別する
- 実施できなかった検査は「未検査」として明示する
- 判定文の冒頭にあなたのmodel名を記載し、日本語で返す

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み：除外3形式と適用範囲（契約v2 §7・あなたの`開始可`判定）。残余risk 3点の暫定受容（採用判断。
  最終受容は製品受入で扱う）。改名の同梱（利用者指示）。layout除外の対処方針（利用者承認）。
- 範囲外：応答解析・監査自動化・旧設計統合・複数送信・依頼組み立て器・prompt品質gate・判定取り込み
  （後続）。実送信E2E（受入条件8。本レビュー合格後に利用者指示で実施）。製品受入（受入条件9）。
- 事実の明示：対象試験内の`_AWS_KEY`・乱雑列・鍵風文字列はすべて機微検査試験用の合成値であり実鍵ではない。

## 6. 手順（Human・Claude向け）

1. 利用者がGeminiへ本依頼recordのpath
   （`records/session-handoffs/2026-08-16-g20-scan-refinement-completion-review-gemini-request-v1.md`）を伝える。
2. Geminiは§2の鮮度検査→§3の反証4点を行い、§4の形式で判定文を返す。
3. 利用者が判定文をClaudeへ貼り戻す。Claudeが判定record
   `records/development/2026-08-16-external-send-scan-refinement-completion-review-v1.md`へ転記・commitし、
   根拠と実物の整合を機械照合する。
4. `verified`なら利用者へ実用文書の実送信E2E（受入条件8）の実施判断を求める。`修正要`なら停止して諮る。
