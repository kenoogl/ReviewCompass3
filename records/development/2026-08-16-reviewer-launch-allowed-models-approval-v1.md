# 契約010 許可model一覧の利用者承認record v1

- 判断日：2026-08-16
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：契約010 §7.1「許可model一覧の値は実E2E前の利用者承認recordで確定して定数へ固定」の履行

## 1. 承認文言【記録】

> gemini-3.1-pro-high を指定

> 一覧はgemini-3.1-pro-highの1件で承認する。定数へ固定して

（いずれも2026-08-16 chat。1通目はmodel名の指定、2通目はClaudeの推奨文言と同一の全文承認。
両者は同じ判断を指す）

## 2. 根拠となった機械出力【記録：利用者提供】

利用者が実行した`agy models`の出力（2026-08-16 chat貼り付け）：

```text
gemini-3.7-flash-high     Gemini 3.7 Flash (High)
gemini-3.7-flash-medium   Gemini 3.7 Flash (Medium)
gemini-3.7-flash-low      Gemini 3.7 Flash (Low)
gemini-3.6-flash-high     Gemini 3.6 Flash (High)
gemini-3.6-flash-medium   Gemini 3.6 Flash (Medium)
gemini-3.6-flash-low      Gemini 3.6 Flash (Low)
gemini-3.5-flash-high     Gemini 3.5 Flash (High)
gemini-3.5-flash-medium   Gemini 3.5 Flash (Medium)
gemini-3.5-flash-low      Gemini 3.5 Flash (Low)
gemini-3.1-pro-high       Gemini 3.1 Pro (High)
gemini-3.1-pro-low        Gemini 3.1 Pro (Low)
```

## 3. 確定事項

1. `tools/reviewer_launch/core.py`の契約固定定数を
   `ALLOWED_RESPONSE_MODELS = ("gemini-3.1-pro-high",)`へ固定する（1件のみ・最も厳格な一覧）。
2. 以後の一覧変更は契約改定として扱う（契約010 §7.1）。
3. 選定理由：暫定体制の実績Reviewer（契約009指摘3件全て正当・契約010候補v2判定）と同一のmodelで
   あり、危険度high検証に最上位Pro系・高推論努力を用いる。
4. 不確実性の明示：応答stream内のmodel表記がCLI識別子か表示名かは実E2Eまで不明。表記不一致の場合は
   `response_model_not_allowed`で停止し、未加工出力の実表記を持ち帰って一覧訂正（契約改定）を諮る。

## 4. 未実施

- 実E2E（利用者の明示指示待ち）、独立完了レビュー、製品受入。
