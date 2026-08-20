# 起動直前のdigest表現物照合の不在 観測record v1

- 記録日：2026-08-20
- 記録者：Claude
- 種別：観測record（改善候補`IC-LAUNCH-DIGEST-TABLE-RECHECK-001`の出所）
- 提起：利用者（Human）。文言【記録】
  > 実装した契約016は全て機械化できているか
  > （棚卸し報告の後）機械化の穴2件を観測record＋改善候補としてwriterで登録してください（仕分けは後日）

## 1. 観測（根拠となる実測・記録）

1. **事象**【実測・2026-08-20】：契約016のterra実E2Eで、依頼recordの組み立て・commit・check合格の
   **後**に対象fileの是正commit（`_render`互換復元＝`52e9f65`）が入り、依頼record内のdigest表の
   `tools/request_builder/core.py`行が現物と不一致（陳腐化）になった。
2. **機械検出層の不在**【実測】：起動（launch）は依頼record自身のSHA-256だけを照合し、record内
   digest表と対象現物の一致は再検査しない（表の照合はReviewerの読取りに委ねる設計）。今回の陳腐化は
   **人の目視**で起動中に気づき、手動停止→現物digestでの別名再組み立て（`f0fd065`）で回避した。
   経緯の正本＝`records/development/2026-08-20-contract-016-e2e-findings-remediation-evidence-v1.md` §4。
3. **既存部品で検出可能**【記録】：組み立て器のcheckはdigest表の現物照合（`digest_mismatch`停止）を
   既に持つ。起動直前にcheckを機械再実行していれば送信前に検出できた。

## 2. 機械化候補の骨子

起動直前のdigest表現物照合を機械化する。案の軸＝(a) launchがcheck相当の表照合を内蔵して不一致を
停止語彙で止める／(b) 起動手順にcheck再実行を必須化し手順書＋機械確認で固定する。自動再生成・
自動修復はしない（fail-closed維持）。

## 3. route

改善候補`IC-LAUNCH-DIGEST-TABLE-RECHECK-001`としてHuman仕分けへ（仕分けは後日＝利用者指示）。
