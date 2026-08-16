# 機微検査精密化・改名 契約候補v2 独立確認依頼record v1（Claude→Gemini・Human中継)

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v2の作成担当）
- 依頼先：Gemini（暫定体制。本repositoryのディレクトリを共有しており、対象fileを直接読める）
- 体制根拠：`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`
- レビュー種別：実装開始前の契約定義反証（読取り専用・repositoryへの書込みなし）

## 1. 対象と固定

- 対象契約候補：`records/task-contract/2026-08-16-external-send-scan-refinement-candidate-v2.md`
  - SHA-256：`58e5f9165e2201892377744377a9758f79be7559fe26f82ed114ec246968e6da`
- 起草側自己レビュー（第1・2段。v1→v2の訂正根拠SR-C9-1〜3）：
  `records/development/2026-08-16-external-send-scan-refinement-v1-self-review-v1.md`
  - SHA-256：`1c67b23f3abc42f98a2ac1071b935b01559e0f8a5160d4e3685c6fa7642f8f94`
- 誤検知の観測record（契約の入力）：
  `records/development/2026-08-16-egress-sensitive-scan-false-positive-observation-v1.json`
  - SHA-256：`e6ffac53245501a57555a19b17225c4715ac394bdf37ef1c6cb025446adfb1b4`
- 参考（受入済みの土台。本契約では変更しない）：契約008 v5
  `records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v5.md`、現行実装
  `tools/external_review/gemini_send.py`、検知部品`tools/session_logs/redaction.py`

## 2. 開始時の鮮度検査（Gemini（あなた）が最初に行う）

1. §1の3 file（契約候補v2・自己レビュー・観測record）のSHA-256を機械計算し
   （例：`shasum -a 256 <path>`）、本record記載値との一致を確認する。
2. 不一致の場合は、レビューせずその旨を判定文へ書いて停止する。

## 3. Gemini（あなた）への依頼：反証4点

あなたは独立したレビュアです。対象契約候補v2を読み、次の4点をそれぞれ反証的に検査し、判定を返して
ください。各主張には根拠（契約の節番号、必要なら現行実装・検知部品の関数名）を付けてください。

1. **機械層の一意性**：§7（除外3形式・適用範囲）と§9（変更上限）に、実装者が後決めできる曖昧さ・矛盾・
   漏れがないか。特に、自己レビューSR-C9-1の訂正（`order_identifier`の検査には除外を適用しない出し分け）が
   一意に実装できる書き方になっているか。
2. **X2の通り抜け耐性**：X2の正規表現
   `(?=.*[G-Zg-z_])[A-Za-z0-9]{1,20}(?:[-_]+[A-Za-z0-9]{1,20})+`に、乱雑な鍵が「可読連結」を装って
   通り抜ける形が残っていないか（例：断片20字以下×多数連結の乱雑列、hex外文字を1字だけ混ぜた乱雑hex、
   その他あなたが考える敵対形）。発見した形は、§10.3の敵対集合への追加として提案してよい。
3. **残余riskの受容妥当性**：§7.2の残余risk 3点（40/64桁hex形式の実鍵・大文字乱雑連結・UUIDの従来からの
   対象外）が、緩和4点（既定5 pattern不変・commit済み限定・zshrc鍵管理・台帳監査線）の下で受容可能な
   水準か。受容できないと考える場合は、実用（可読file名・digest記載を含む文書の送信）を壊さない範囲の
   最小の追加緩和を提案する。
4. **縮小境界と上位整合**：改名（§8）の同梱が範囲を不当に広げていないか。契約008の受入済み境界
   （送信規則・保護対象）と本契約の変更上限が矛盾なく共存するか。「受入だけでは後続（依頼組み立て器・
   prompt品質gate・判定取り込み）を完了にしない」ことが誤解なく固定されているか。

## 4. 判定の形式（あなたに求める出力）

- 判定：`開始可`または`修正要`
- `修正要`の場合：同じ原因の変種をまとめた最小数の停止原因と、各原因の最小修正案
- 実施できなかった検査があれば「未検査」として明示する
- 判定文の冒頭にあなたのmodel名を記載し、日本語で返す

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み：改名の同梱（利用者指示）。`redaction.py`・既定5 pattern・egress 7 module・受入済み4製品の
  不変（契約008の保護の継承）。除外を`allow_patterns`（トークン全体一致）で実現する方式（起草時実測で確立）。
  送信規則（宛先・台帳・上限・鍵扱い）の不変。
- 範囲外（「無い」という指摘は不要）：応答解析・監査自動化・旧設計統合・複数送信・依頼組み立て器・
  prompt品質gate・判定取り込み（全て後続）。歴史的recordの旧名書き換え。
- 残余riskを0にすることは本契約の目的ではない（誤検知の解消と保険の維持の均衡点を契約固定するのが目的。
  最終の受容判断は利用者が行う）。

## 6. 手順（Human・Claude向け）

1. 利用者がGeminiへ本依頼recordのpath
   （`records/session-handoffs/2026-08-16-g20-scan-refinement-v2-review-gemini-request-v1.md`）を伝える。
2. Geminiは§2の鮮度検査→§3の反証4点を行い、§4の形式で判定文を返す。
3. 利用者が判定文をClaudeへ貼り戻す。Claudeが判定record
   `records/development/2026-08-16-external-send-scan-refinement-v2-independent-review-v1.md`へ転記・
   commitし、根拠と実物の整合を機械照合する。
4. `開始可`なら利用者へ縮小境界の採用と実装開始を一判断として求める。`修正要`なら停止して利用者へ諮る。
