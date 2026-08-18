# roots.py指紋pin追加のHuman判断record v1（状態固定試験の対象限定再開）

- 判断日：2026-08-18
- 承認文言（逐語）：「1については、最終的には指紋固定の一覧に載せるのなら、いつかはやらないと
  いけないので実施。」（2026-08-18 chat。判定1＝配置依存解消Evidence §7-1・作業票§5-1の
  Human確認点に対する裁定）
- 記録者：Claude
- 対象：`tests/test_common_module_pins.py`の`_PINS`へ`tools/common/roots.py`を1行追加

## 1. 対象限定再開【手続き】

第5段完了Decision §9
（`records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md`・
SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`）の定め
「状態固定試験の変更・削除、または別途承認されたWork 8測定の前にだけ、対象限定で再開する」に
より、本変更の前に`ISSUE-TEST-GROWTH-STATE-PINNING-001`を**対象限定で再開**した。

- 再開範囲：`tests/test_common_module_pins.py`への上記1行追加**のみ**。Issue本体の未解決範囲
  （凍結理由の宣言file化・変異検査・他の状態固定試験の張り方）には踏み込まない。
- Issue状態：`registered`のまま**変更しない**（TODOの定めどおり）。本record末尾の確認をもって
  従前の`第3段完了・条件付き再開待ち`へ復帰する。

## 2. 追加したpin【機械出力の転記】

`shasum -a 256`の出力そのまま（配置依存解消Evidence §1の値と一致）：

```text
478476817a5fcc755c7e96f33cfe2a68f093e0a4dd26ae3405cbac2ff8d33791  tools/common/roots.py
```

## 3. pin更新のHuman承認記録

`test_common_module_pins.py`冒頭の定め「本pinの更新はHuman承認の記録を伴うこと」および
`DEC-SHARED-FUNCTION-POLICY-001`（共通部品の変更はHuman承認）に対する承認記録は**本record**で
あり、承認文言は冒頭の逐語である。判断の理由（利用者）：最終的に載せるものなら先送りしても
総量は減らないため、新設と同じ作業単位内で載せる。

## 4. 実施と機械確認【実測・2026-08-18】

| 対象 | 変更前 | 変更後 | 終了コード |
| --- | --- | --- | --- |
| `tests/test_common_module_pins.py` | 5 passed | **6 passed** | 0 |
| `tests/test_common_roots.py`（併走確認） | — | 6 passed | 0 |
| `tests/test_shared_function_sweep.py`（併走確認） | — | 25 passed | 0 |

## 5. 復帰の確認

本変更は上記1行のみで完了し、`ISSUE-TEST-GROWTH-STATE-PINNING-001`は`registered / 第3段完了・
条件付き再開待ち`へ復帰した（record・状態とも変更なし）。

## 6. 未実施

- Issue本体（宣言file化・変異検査等）の解決——従前どおりWork 8前の限定再開の枠のまま。
- push（従前どおり利用者の運用に従う）。
