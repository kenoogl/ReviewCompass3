# 層1の残り3件 RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-VERIFICATION-BOUNDARY-001`（層1）、`DEC-RED-VERIFICATION-ADOPTION-001`（新手順）
- 実装前検索：`records/development/2026-08-07-layer1-remainder-reuse-search-attestation-v1.json`
  （gate `assessed_fresh`、該当101 routine）

## 1. 対象

| 反証 | 固定する拒否 |
| --- | --- |
| C-1（完全解消） | 対応表へ`scope`欄（`complete`／`partial`＋理由）を導入し、`complete`では欄からも宣言からも漏れた実在testを検出する |
| C-2（形式面） | 宣言の`summary`が空白のみの対応表を拒否する |
| R-3 | gateが検索を再実行し、`hits`を空にしたrecordを`search_result_mismatch`で拒否する |
| I-2（機械化可能部分） | 後継decisionの決定時刻が前版より過去へ戻ることを拒否する |

## 2. 宣言→RED対応表の関門（静的検査）

`records/development/2026-08-07-verification-boundary-layer1-declaration-red-map-v1.json`。
恒久検査器で`passed`、宣言9件（L1〜L9）、testの無い宣言0件、双方向一致。

## 3. 実行照合（`DEC-RED-VERIFICATION-ADOPTION-001`の初適用）

RED固定commitの前に`verify_red=True`で照合した【実測】。

**初回：`mismatched: 1`で不合格。** L2（`scope: partial`が範囲外testを対象にしない）を
`red_now: true`と申告していたが、現行の検査器は`scope`欄を読まないため実際には成功していた。
**新手順が初適用で誤申告を1件検出した。**

L2を境界例（`red_now: false`＋`boundary_reason`）へ訂正し、再照合した結果：

    checked=9  verified=9  mismatched=0  unknown=0  → passed

## 4. RED結果

- 対象test：`tests/test_verification_boundary_layer1.py` 9 test。8件が期待どおり失敗、
  L2は境界例として成功（上記の実行照合と一致）。
- 既存全Test：影響なし。

## 5. 状態と次

本RED作業単位のcommit後、固定testを変更せずGREEN実装へ進む。
