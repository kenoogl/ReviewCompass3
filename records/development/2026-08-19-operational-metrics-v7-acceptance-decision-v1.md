# 運用集計v7 受入・作業票§4確定 Human判断record v1

- 判断日：2026-08-19
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：作業単位（運用集計v7＝系統意味づけ・道具正規化・活動時間）の受入と、
  作業票§4「Humanの確認が要る点（覆せる形）」3点の確定

## 1. 承認文言【記録】

> v7を受入とする。作業票§4の3点も現行案で確定

（2026-08-19 chat）

## 2. 判断対象の束縛【実測】

```text
bcfbd10d9e6a04ace9ebafcfaf8a63c92373988a7f68a3e20bf45a8d9f771dd6  docs/development/2026-08-18-operational-metrics-v7-work-ticket-v1.md
d131575fd704505ffc90cf5a8e32361c89ba6a2a56aec43f86b917a0fe3e3341  records/development/2026-08-18-operational-metrics-v7-evidence-v1.md
7702463b46678ab52cf15b3f077fc590f51a2707fab5ab64bf6356ff5c3843c2  records/development/2026-08-18-operational-metrics-dataset-v7.json
```

## 3. 確定した3点（作業票§4の現行案）

1. **活動時間の窓＝600秒既定**（保全の活動窓と同値）。固定bucket（≤60／≤600／≤3600／
   >3600秒）の併載は維持し、窓の再選択は再集計だけで可能なまま。
2. **namespace導出＝`_namespace`の直接import（案A）**。式の複製（案B）・保全moduleへの
   公開wrapper追加（案C）は採らない。
3. **Codex道具計数＝呼び出し2種のみ**（`function_call`・`custom_tool_call`。`*_output`・
   event系は数えず二重計上を回避）。

## 4. 効果

- v7作業単位の受入が完了し、作業票§4の確認待ちは解消。dataset v7と台帳追補v2
  （執筆用固定）の位置づけは変わらない。
- 3点はいずれも設計上「覆せる形」（窓は引数・bucket併載、importは1箇所、規則集合は定数）の
  まま確定であり、将来の変更は通常の改善候補経路で扱う。

## 5. 未実施

なし（本recordのcommitのみ）。
