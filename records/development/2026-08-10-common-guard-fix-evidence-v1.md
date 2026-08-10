# Evidence：group A（共通正本）blocking 2件の修正

- 範囲固定：`records/session-handoffs/2026-08-10-claude-pilot-common-guard-fix-scope-v1.md`
  （`3594172`）＋`…-scope-v2.md`（`35d2fe6`、指紋pinの扱いを追加）。
  範囲レビューv2 `verified`：`9fd43ba`
- Human承認（2026-08-10）：「組A修正 risk highを確定、着手を承認する」／
  「組A RED開始を承認する」
- 作成日：2026-08-10
- executor：Claude（Pilot。mode `role_neutral_pilot_review`、Reviewer=codex、Closer=codex、risk `high`）

## 1. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| SCOPE v1 | `3594172` | 範囲固定のみ |
| 範囲レビューv1 | `867d0b1` | Codex作成。要修正・blocking 1件（pin fileの欠落） |
| SCOPE v2 | `35d2fe6` | commit境界・変更可能path・受入条件5の差し替えのみ |
| 範囲レビューv2 | `9fd43ba` | Codex作成。`verified`・blocking 0 |
| RED | `a84b8ca` | test 2 fileのみ |

## 2. RED（実装前・単独実行）

- command：`.venv/bin/python3 -m pytest tests/test_common_digests.py
  tests/test_common_errors_paths_output.py tests/test_common_module_pins.py
  tests/test_shared_function_sweep.py tests/test_first_review_task_contract_e2e.py`
- 結果：**15 failed / 110 passed**、exit `1`
- 内訳：F-A1関連12件（非JSON互換8態様の非拒否、Digest衝突2組、`seal`・
  `canonical_bytes`の非拒否）、F-A2関連3件（case別名・NFC/NFD別名・別名配下の子path）
- **更新していない既存test**：`test_common_module_pins.py`・
  `test_shared_function_sweep.py`・`test_first_review_task_contract_e2e.py`は
  変更せず、RED時点で合格していた（既存testの契約更新は本単位では不要だった）
- environment：Python 3.9.6、pytest 8.4.2

### 2.1 追加した反証test

- F-A1：`TestJsonCompatibilityIsEnforced`（非文字列key・nested非文字列key・tuple・
  nested tuple・NaN・+Inf・-Inf・nested NaN・set・bytesの10態様、
  `{1:"value"}`と`{"1":"value"}`／tupleとlistのDigest衝突2組、`seal`・
  `validate_record`・`canonical_bytes`の各拒否）
- F-A2：`TestWithinHandlesPathAliases`（case別名・NFC/NFD別名が
  `os.path.samefile`と同じ判定になること、別名配下の子path、root外の拒否維持、
  存在しないpathの従来判定維持）
- 正例：`TestExistingDigestValuesAreUnchanged`（既知3 documentのDigestが独立oracleと
  一致、および**実台帳`records/development/*.json`の宣言Digestと再計算値の一致**）

## 3. GREEN実装

| finding | 実装 |
| --- | --- |
| F-A1 | `tools/common/digests.py`へ`require_json_compatible`と`canonical_json_bytes`を新設。非文字列key・非JSON型（tuple・set・bytes等）・非有限数を`DigestInputError`（`FailClosedError`継承、code `digest_input_not_json_compatible`）で拒否し、`json.dumps`は`allow_nan=False`。`canonical_content_digest`はmapping以外も拒否。`tools/task_contract/identity.py`は`canonical_bytes`と新設`_content_digest_or_stop`でこれを`ContractError("schema_violation")`へ変換し、`seal`・`validate_record`が使う |
| F-A2 | `tools/common/paths.py`の`within`に`_same_entity_within`を追加。字句上の解決後比較で内側と判定できない場合に限り、`os.stat`のdevice・inode（`os.path.samestat`）でtargetとその祖先をrootと照合する。root外は従来どおり`False`、存在しないpathは解決後pathでの判定を維持 |

**維持した制約**：`identity.content_digest`は共通正本`canonical_content_digest`への
**直結のまま**（`tests/test_shared_function_sweep.py`が要求する写しの禁止）。
canonical仕様（key順・`ensure_ascii=False`・`separators`・`content_digest`除外）・
Digest algorithm・`within`呼び出し側は未変更。

### 3.1 指紋pinの更新（scope v2 §2の例外）

`tests/test_common_module_pins.py`の`_PINS`のうち2値のみを更新した
（`git diff --stat`＝2 insertions / 2 deletions、key構成と検査logicは不変）。

| 対象 | 更新前 | 更新後 |
| --- | --- | --- |
| `tools/common/digests.py` | `db6b8305…` | `fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7` |
| `tools/common/paths.py` | `daa32579…` | `039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec` |

pin更新のHuman承認根拠：2026-08-10「組A修正 risk highを確定、着手を承認する」、
裁定record `records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md`
（commit `4bb1c9b`）。更新前は当該2件が失敗し、更新後に`5 passed`となった。

## 4. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED（実装前） | 上記5 file | 15 failed / 110 passed | `1` |
| targeted GREEN | `pytest tests/test_common_digests.py tests/test_common_errors_paths_output.py` | **57 passed** | `0` |
| 全test（pin更新前） | `pytest tests/` | 2 failed（pin 2件のみ）/ 1449 passed | `1` |
| 公式全Test（pin更新後） | `policy_test_runner --suite full --receipt records/development/2026-08-10-common-guard-fix-test-receipt-v1.json` | **1451 passed**、status `passed`（failed 0・error 0・skipped 0） | `0` |
| `git diff --check` | 各commit前 | 指摘なし | `0` |

## 5. 受入条件の対応（scope v1 §5、v2 §4）

1. 危険側：`{1:"value"}`と`{"1":"value"}`、tupleとlist、NaNを含むrecordは、
   Digest計算・`seal`・`validate_record`・`canonical_bytes`のいずれでも拒否される。
   case差・NFC/NFD差の実在pathは`os.path.samefile`と同一判定になった。
2. 正例：既知documentのDigestは独立oracleと一致。**実台帳のrecordは宣言Digestと
   一致し続け、値の変化は無かった**（停止条件§8-3には該当せず）。
   JSON互換検査により拒否された実台帳recordも無かった（§8-2に該当せず）。
3. 既存test：更新なしで合格を維持（sweepの直結要求を満たすため実装側を調整）。
   公式全Test 1451 passed。
4. 上流設計・config・schema・既存record：未変更。

## 6. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/common/digests.py` | `fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7` |
| `tools/common/paths.py` | `039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec` |
| `tools/task_contract/identity.py` | `fddffe6617c225e9fbedd33ea722316ea41f37c1f76c93cfbce3060ed55b5422` |
| `tests/test_common_digests.py` | `3f52229b177324cd463dc80e6cf031ac685598dab0d92bc9a4801e2cdf15364c` |
| `tests/test_common_errors_paths_output.py` | `61f21966c3488f73a66baa40d75c31720c1ecd2da08cab80832070025033028a` |
| `tests/test_common_module_pins.py` | `fc7dcde0b182b1ee0a8a57759f0c8bf240c5956e9258e63ae77e2c2d0cdd392e` |
| 公式receipt | `429ca5d4ae990893837df90509837fc5f2e6f73ff83438e6fb87bda38cdb3fd5` |

## 7. 未実施

group B（5件）・C（5件）・D（7件）の計17件は判定recordのまま保持。
TODO・checklist反映はCloser。push・履歴書換えは未実施。
