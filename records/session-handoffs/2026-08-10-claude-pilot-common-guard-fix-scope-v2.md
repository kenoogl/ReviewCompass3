# 範囲固定 v2：group A（共通正本）blocking 2件の修正 — 指紋pinの扱いを追加

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビューv2待ち
- 先行：scope v1（`3594172`）。範囲レビューv1（`867d0b1`、要修正・blocking 1件
  ＝`tests/test_common_module_pins.py`の欠落）により、v1をRED開始の根拠にできない。
  v1は変更せず保持し、本v2が有効な範囲固定となる。v1の§1〜§5・§8・§9は不変で、
  **§6 commit境界と§7 変更可能pathのみを差し替える**。

## 1. 指摘の反映（SR-CG-SCOPE-001）

`tests/test_common_module_pins.py`は、共通正本moduleのSHA-256を`_PINS`として固定し、
無断変更を検出するtestである。同fileのdocstringは「本pinの更新はHuman承認の記録を
伴うこと」と定めている。

- v1はこのfileを変更可能pathへ挙げていなかった。そのため、実装を変えた瞬間に
  公式全Testが失敗し、「範囲を守ること」と「全Test合格」を両立できなかった。
- 本v2で`tests/test_common_module_pins.py`を変更可能pathへ加える。
- pin更新のHuman承認根拠：**2026-08-10「組A修正 risk highを確定、着手を承認する」**
  および修正順序の裁定record（`records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md`、
  commit `4bb1c9b`）。Evidenceにこの文言とcommitを転記する。

## 2. commit境界（v1 §6の差し替え）

| # | commit | 変更file（これ以外を含めない） |
| --- | --- | --- |
| 1 | **SCOPE v2**（本commit） | 本文書のみ |
| 2 | **RED** | `tests/test_common_digests.py`・`tests/test_common_errors_paths_output.py` |
| 3 | **GREEN** | `tools/common/digests.py`・`tools/common/paths.py`・`tools/task_contract/identity.py`、**`tests/test_common_module_pins.py`（`_PINS`の値のみ）**、Evidence（新規）、receipt（新規） |
| 4 | **review request** | 依頼書のみ（ignore検査exit `1`確認のうえ） |

- GREENでのtest変更は**指紋pinの値更新に限る**。pinは実装bytesから機械的に導かれる
  派生値であり、振る舞いの期待ではない。**期待の追加・削除・緩和は行わない**
  （`_PINS`のkey構成と検査logicは不変）。この一点だけがGREENでのtest変更として
  許される例外であり、他のtest fileはGREENで変更しない。
- pin更新前後の実測（更新前の失敗と更新後の合格）をEvidenceへ記録する。
- REDの定義・既存testの扱い（削除・緩和の禁止、契約更新の可否、RED後のtest変更に
  Human承認を要すること）はv1 §6の規定どおりで不変。

## 3. 変更可能path（v1 §7の差し替え）

実装：`tools/common/digests.py`、`tools/common/paths.py`、
`tools/task_contract/identity.py`

Test：`tests/test_common_digests.py`、`tests/test_common_errors_paths_output.py`、
`tests/test_common_module_pins.py`（**`_PINS`の値のみ**）

記録（新規）：
- `records/development/2026-08-10-common-guard-fix-evidence-v1.md`
- `records/development/2026-08-10-common-guard-fix-test-receipt-v1.json`
- `records/session-handoffs/2026-08-10-claude-pilot-common-guard-fix-review-request-v1.md`

これ以外のfile（他tool・既存record・config・schema・上流設計・TODO）は変更しない。

## 4. 受入条件への追加

v1 §5の1〜4は不変。次を加える。

5. `tests/test_common_module_pins.py`の`_PINS`は、**GREEN後の実装bytesと一致**し、
   key構成・検査logicが修正前と同一であること（diffで確認できる形にする）。
