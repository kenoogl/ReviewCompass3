# 契約016 terra E2E判定（rejected）の所見是正Evidence v1

- 実施日：2026-08-20
- 担当：Claude
- 出所：terra指定実E2Eの判定record
  `records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-verdict-v1.md`
  （codex・`gpt-5.6-terra`・`rejected`・blocking 2件。**E2Eの機械経路は完全成立**＝完走・raw保存・
  転記・事後照合4点合格・**rollout観測がterra表記**）
- 実測の正本：測定ブロック
  `records/development/2026-08-20-contract-016-remediation-measurements-v1.md`（宣言
  `records/development/2026-08-20-contract-016-remediation-commands-v1.json`。5項目・二重実行一致・
  合否は`exec`置換の単独実行）

## 1. F-016-001（blocking・high）→ 是正済み

指摘：正準抽出が契約§7.2の**開始境界（先頭見出し行の直後から）**を実装しておらず、見出し前の
偽「- 依頼先：」行に騙され得る。

是正：RED先行（新設の敵対試験
`test_extract_reviewer_line_requires_top_heading_region`——見出し前の偽行＋領域内の正行／偽行のみ／
見出しなし——の失敗を先に確認＝実装前1 failed）→抽出核へ領域開始判定（fence外の先頭`# `見出しを
通過してから走査。見出しが無ければNone＝fail-closed）を最小実装→対象試験全緑（commit `0519daa`）。

## 2. F-016-002（blocking・medium）→ 是正済み

指摘：`reviewer-launch-run.md`のcodex-cli節に「terraは許可済みだが起動選択機構は範囲外」の
旧記載が残り、同file後段の契約016節と矛盾。

是正：旧記載を「`--model`で選択できる（契約016）」へ更新し、契約016節への参照を付けた
（同commit `0519daa`）。

## 3. §9-7 実E2Eの成立【実測】

- terra指定の依頼record組み立て（`assemble --backend codex-cli --model gpt-5.6-terra`）→check
  合格（backend別所属検査の実運用初合格）→起動（`--model gpt-5.6-terra`）→完走・raw保存・
  判定record転記（単独commit `536060f`）・事後照合4点`passed`。
- **rollout観測＝`gpt-5.6-terra`**（launch.jsonの`models_observed`。選択機構と観測が一気通貫で
  機能した機械証明）。
- 領域外読取り点検：raw（`~/.reviewcompass3-private/reviewer-launch/contract-016-e2e-codex-terra-3/`）
  の`command_execution`全9件を機械走査し、repo外への読取り0件。
- 起動前の記載照合も通過（記載＝新形terra行・実行＝codex-cli×terraの一致）。

## 4. 実施中の手戻り2件（原因と再発防止）

1. **転記段の`worktree_not_clean`停止**（run `contract-016-e2e-codex-terra-2`・レビュー自体は完走・
   raw保存済み）：E2E実行中に正規全試験を並行実行し、runnerが生成したreceipt（未追跡file）で
   worktreeが汚れたため。期待executor＝Claudeの逐次運用、実executor＝並行運用の誤り。対処＝
   receiptをcommitして樹を清浄化し、以後**起動中は樹を汚す操作をしない**運用へ（機械化候補：
   起動前のworktree clean検査は既にアダプタが持つ——運用側の順序規律の問題）。
2. **依頼recordのdigest表の陳腐化**（slug `-codex`版）：組み立て後に互換修正commit（`52e9f65`）で
   対象fileが変わった。起動を停止し、現物digestで別名（slug `-codex2`）へ再組み立てして解消。

## 5. あわせて固定した受入材料【実測】

- 正規全試験：初回runは保護対象（運用集計）が`_render`旧引数で4件失敗→**互換受け復元**
  （`52e9f65`。保護対象は無変更）→再実行で**2,668件全合格・終了コード0**（receipt＝
  `records/development/2026-08-20-contract-016-full-test-receipt-v1.json`・commit `2a41167`）。
- 是正後の対象・保護互換suite（reviewer_launch 106件・request_builder 51件・運用集計25件）は
  単独実行の終了コード0（測定ブロック参照）。

## 6. 未実施

- 完了レビュー（agy・Tier 1）の起動と判定。製品受入（Human）。codexによる再レビュー（要否は
  Human判断。E2Eの機械経路と選択機構の実証は本記録で完了済み）。
