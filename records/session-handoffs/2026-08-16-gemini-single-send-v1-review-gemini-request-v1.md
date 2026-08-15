# Gemini一回送信 契約候補v1 独立確認依頼record v1（Claude→Gemini・Human中継）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v1の作成担当）
- 依頼先：Gemini（暫定体制。利用者が手動で運搬する）
- 体制根拠：`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`
- レビュー種別：実装開始前の契約定義反証（読取り専用・repositoryへのaccessなし）

## 1. 対象

- 対象契約候補：`records/task-contract/2026-08-16-gemini-single-send-candidate-v1.md`
  - SHA-256：`a1cad58471d5928239d64c7a6fdf63211bbfaef199b89f4d57df6709d4e7b627`
  - 固定commit：`680bad1`
- Geminiはrepositoryを読めないため、契約候補の全文は利用者が運搬する文面に含める。

## 2. Geminiへ依頼する反証4点

1. **Human承認境界の整合**：§2「送信ごとの人の確認なし」の取り決めが、契約採用・作業指示・台帳・失効という
   残りの人の関与と整合し、無承認の自発送信を許す穴がないか。
2. **機械層の一意性**：§7〜§10（機微検査、path allowlist、digest束縛、payload固定形、送信前試行record、
   累計上限、重複ID停止、鍵の非表示）に、実装者が後決めできる曖昧さ・矛盾・漏れがないか。
3. **不可逆リスクの残余**：一回送信・再試行なし・試行record先行の設計で、二重送信・送信内容のすり替え・
   鍵漏えい・台帳の空白が起き得る経路が残っていないか。
4. **縮小境界の明示**：G20全体でないこと、後続（応答解析・監査自動化・旧設計統合）が残ること、
   受入だけでは候補5を完了にしないことが誤解なく固定されているか。

## 3. 判定の形式（Geminiに求める出力）

- 判定：`開始可`または`修正要`
- `修正要`の場合：同じ原因の変種をまとめた最小数の停止原因と、各原因の最小修正案
- 各主張に根拠（契約の節番号への参照）を付ける

## 4. 判定の取り込み

利用者がGeminiの判定をClaudeへ渡し、Claudeが判定record
`records/development/2026-08-16-gemini-single-send-v1-independent-review-v1.md`へ転記・commitする。
冒頭にReviewer（Gemini・利用者提供のmodel名）とHuman中継である旨を記載し、Claudeが判定内容と契約の
節参照の整合を機械照合する。
