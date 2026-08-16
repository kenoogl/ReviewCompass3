# 外部レビュー準備・実施の機械化目標 v1

- 記録日：2026-08-16
- 指示者：利用者（Human）
- 記録者：Claude
- 種別：利用者目標の固定（後続契約定義の入力）

## 1. 利用者の指示

【記録】利用者は2026-08-16、外部APIレビューの品質がレビューpromptの適切性に大きく依存するという
試行錯誤の経験知（自己レビュー→文脈整理→prompt作成→promptレビュー→送信の念入り手続き）を示し、
次を指示した。

> repositoryの手順書として固定するだけではなく、この機能自体を機械処理化、手続き自動化、導線配備として
> ツールとして整備する必要があると考えている。

## 2. 目標の解釈

外部レビューの準備から実施までの一連——(1)対象の自己レビュー（定義反証checklist）、(2)文脈整理
（判断済み・既知の弱点・範囲外）、(3)依頼promptの機械組み立て、(4)prompt品質gate（敵対役・判定役の
多周確認）、(5)送信、(6)判定の取り込み——を、手作業と属人性を減らす形で機械処理化し、受入済み部品の
導線（運用契約→実行→記録着地）に載せる。

## 3. 既にある材料【実測】

| 材料 | 所在 | 使える段 |
| --- | --- | --- |
| 正本手順書（9段） | `WindTurbineWake/ReviewCompass/.reviewcompass/guidance/API_REVIEW_PROMPT_QUALITY.md` | 全体の設計参照 |
| 多周gateの実施証跡 | `WindTurbineWake/LLMGP/.reviewcompass/specs/_cross_feature/reviews/`（敵対役・判定役・5周収束） | (4)の設計参照 |
| prompt機械組み立ての先行実装 | `ReviewCompass/tools/api_providers/api_review_prompt_builder.py`・`prompt_templates/` | (3)の設計参照 |
| レビュー計画の機械生成 | RC3 `reviewcompass3-review-plan`（対象・項目・担当・周回数） | (1)(4) |
| 材料固定 | RC3 G02 prepare（受入済み） | (3) |
| 機微検査 | RC3 `tools/session_logs/redaction.py`（受入済み再利用） | (3)(5) |
| 外部送信 | RC3 G20送信module（契約候補v2・定義中） | (5)、(4)の自動周回の土台 |
| 結果整理 | G02 organize（未着手の後続） | (6) |
| Task Contract向けの別方式 | RC3 `docs/design/2026-08-05-work5a-definition-challenge-proposal.md`（決定的定義検査） | (1) |

## 4. 段階の方針

- 本目標は一括では作らない。G20送信module（契約008）の完了後、縦切りごとに契約・独立確認・受入で進める。
- 想定する縦切り（順序・採否はHuman判断）：(a)依頼組み立て器（checklist・文脈整理雛形・依頼recordの機械組み立て）、
  (b)prompt品質gate（G20経由の敵対役・判定役自動周回）、(c)判定取り込み（応答→G02 organize→判定record）。
- 暫定運用（Gemini手動運搬）の間も、5段の念入り手続きをClaudeの作業手順として適用する。手順書化は本線の
  区切りで行う。
