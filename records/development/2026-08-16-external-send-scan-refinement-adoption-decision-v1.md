# 機微検査精密化・改名 縮小境界・契約v2採用・実装開始 利用者判断 v1

- 判断日：2026-08-16
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：縮小境界の採用、作業契約の採用、実装開始の承認、残余riskの暫定受容
- 契約：`TC-RC3-PRODUCT-EXTERNAL-SEND-SCAN-REFINEMENT-009 / v2`

## 1. 承認文言

利用者は独立確認`開始可`の報告と一判断の提示を受け、chatで「契約009 v2を採用し、実装を開始せよ」と応えた。

## 2. 承認が固定するもの

1. 縮小境界の採用：機微検査の精密化（除外3形式・適用範囲の限定）と送信路の改名だけの縦切り。
2. 作業契約の採用：契約v2
   - path：`records/task-contract/2026-08-16-external-send-scan-refinement-candidate-v2.md`
   - SHA-256：`58e5f9165e2201892377744377a9758f79be7559fe26f82ed114ec246968e6da`
3. 実装開始：契約§9の変更上限・§10の受入条件・§11の停止条件の下で開始する。RED試験固定→最小実装→
   退行確認→GREEN commit→独立完了レビュー準備まで進めて停止する。
4. 残余risk 3点（§7.2）の暫定受容。最終受容は製品受入（受入条件9）で改めて確認する。

## 3. 判断の前提Evidence

- 起草側自己レビュー（SR-C9-1の内部矛盾を機械検証で発見・訂正）：
  `records/development/2026-08-16-external-send-scan-refinement-v1-self-review-v1.md`
- Gemini独立確認`開始可`（反証4点すべて肯定・根拠4点の機械照合一致）：
  `records/development/2026-08-16-external-send-scan-refinement-v2-independent-review-v1.md`

## 4. 本承認に含まれないもの

- 実用文書の実送信E2E（受入条件8）の実施指示。都度の利用者指示による。
- 製品受入（受入条件9）。独立完了レビュー合格後に一判断として提示する。
