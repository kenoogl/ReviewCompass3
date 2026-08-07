# 層2（機械が支援する）GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-VERIFICATION-BOUNDARY-001`（層2）
- RED Evidence：`records/development/2026-08-07-verification-boundary-layer2-red-evidence-v1.md`

## 1. 実装

| 反証 | 導入した支援 |
| --- | --- |
| **O-1** | 分類の下限規則。既知の危険な操作が軽い分類を名乗るinventoryを`classification_below_minimum`で拒否する |
| **A-1** | pathspec形式検査。区切りの後ろのoption形・絶対path・親escapeを`pathspec_invalid`で拒否し、**拒否時は何も実行しない** |
| **X-2** | `exclusion_impact`。除外指定が落とすsymbol件数をentry別に報告する。**拒否ではなく表示**である |

**層2の位置づけを機械可読に宣言した**（Y4・Y11）：`guarantee: typo_detection_not_safety`、
`coverage: known_cases_only`、`enforcement: reported_for_human_review`。
規則の合格を安全の根拠にしてはならない旨をconfigとcodeへ明記した。

- targeted：`tests/test_verification_boundary_layer2.py` 11 test。RED 9＋境界例2 → GREEN 11/11。
- 公式全Test：`1122 passed`、exit `0`。

## 2. 既存の境界設計との衝突と解決（記録）

最初の実装は下限規則を`operation_routing.py`のcode内定数として持たせた。これにより既存test
`test_host_attestation_is_an_input_not_a_permission_check`が失敗した——同testは
**「このmoduleのsourceに`git`という語が現れてはならない」**ことを検査しており、
「project側は特定toolの知識を持たず、分類と権限計算だけを行う」という境界を守っていた。
私の実装はその境界を侵していた。

**解決**：下限規則を外部config `config/development-classification-minimums.json`へ出した。
moduleは規則を読んで適用するだけで、特定toolの知識をcodeに持たない。既存の境界testは無変更で
合格し、規則の追加・変更はconfig変更（Human判断を伴う）として扱えるようになった。
層2の位置づけ（誤記検出であり網羅しない）にも合う。

**既存testが設計の意図を守った実例**であり、テストが仕様の記録として働いたことを記録に残す。

## 3. 実行照合（`DEC-RED-VERIFICATION-ADOPTION-001`）

RED固定commit前に照合し、`checked=11 verified=11 mismatched=0 unknown=0`で`passed`。
今回は誤申告なし（前回の層1では1件検出した）。

## 4. stale閉包

`build_operation_inventory`へ検査を追加したため、既存の全inventory生成経路が新規則を通る。
公式全Testが合格していることで、既存の正当な操作が誤って止められていないことを確認した
（境界例Y3・Y8も同趣旨をfixtureで固定している）。

## 5. 残余

- 層3（明示）が残る。O-2・O-3（host権限の自己申告）、O-4（実行結果の説明文）、I-1（Human裁定文）、
  P-1（候補の提案文）、C-2の意味的妥当性。
- 下限規則の網羅性は保証しない。configに無い危険操作は素通りする（宣言済みの限界）。
