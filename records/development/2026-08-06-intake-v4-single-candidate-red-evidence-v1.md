# Issue Intake V4 単体候補参照 RED Evidence v1

- 承認正本：`docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md`
  （状態`approved`、§8のHuman文言による承認を含む）
- 基礎裁定：`records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`
  （`DEC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`）
- 対応表：`records/development/2026-08-06-intake-v4-declaration-red-map-v1.json`
- 実行環境：Python 3.9.6、pytest 8.4.2、公式venv runner、fallback `false`
- 実行時刻：2026-08-06T14:30:44+09:00（公式全Test receiptの`recorded_at`）

## 0. 何を固定したのか（範囲の明示）

**固定したのはRED testと、承認済み条件変更（N5・N6）の既存test 2件だけである。
GREEN実装は行っていない。** `tools/`配下の実装コード、allowlist file、
機械可読decision record、Issue recordのいずれも作成・変更していない。
RED 7件はいずれもその不在（単体形式未対応、allowlist未作成、record未作成）で
失敗しており、この記録はREDの成立を示すものであって、対象振る舞いが実装された
ことを示すものではない。GREEN側（実装、allowlist作成、decision・Issue record作成）は
別作業である。

## 1. 固定入力（機械計算したSHA-256）

`shasum -a 256`で計算した。

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md` | `d5164077b8a53141eb647e57f4746e3347ac4650c03a0d1d553571348fc63358` |
| `records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md` | `be9e7d3a2af88a4452a5055d39be8a6e2f77514a5529a134db2086fb49664fb9` |
| `.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json` | `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6` |
| `records/development/2026-08-05-historical-todo-intake-candidates-v1.json`（候補bundle） | `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` |
| `tests/test_issue_intake_v4_single_candidate.py`（新規） | `19b9da920359d55f2786e7f117db64916a250ab496f28dac1a2059a01f623a79` |
| `tests/test_issue_intake_v4.py`（k7・l6のみ変更後） | `dccc29c0700b4909495bf51bf6e73cbefb28cd33f570318e361f8d21e711d4cd` |
| `tools/development/issue_intake_v4.py`（未変更） | `7a1d557e82acd6554c3e137345f02ba476cbf448184a9a0348dca6beec26e27a` |
| `tools/development/issue_resolution_pilot.py`（未変更） | `f0c1801a43d1ed1a9ac9d932d82c5796fb244d502d3f78985f4d968cfb4a3750` |
| `records/development/2026-08-06-intake-v4-declaration-red-map-v1.json` | `c24ebaf58eee3ce2d318084697051d41c9669e30aa756086706f9f110117ce40` |

対象候補の`content_digest`は`760d9ef9811e6d95c9af406a6664e0e2ef5df9c33e32aa6ebbc33721c931753f`
（Markdown裁定§1の固定値と一致することを実測した）。

## 2. 追加した12 testと規範宣言N1〜N12の対応

新規11 testは`tests/test_issue_intake_v4_single_candidate.py`、N5・N6は
`tests/test_issue_intake_v4.py`の既存2 testの条件変更である。

| N | test関数 | 種別 |
| --- | --- | --- |
| N1 | `test_n1_single_form_candidate_ref_decision_validates` | RED |
| N1負例 | `test_n1_candidate_ref_key_set_deviations_are_rejected` | 境界（いま成功） |
| N2 | `test_n2_single_form_fingerprint_mismatches_are_rejected` | RED（happy path依存） |
| N3 | `test_n3_existing_bundle_form_decisions_keep_validating` | 境界（いま成功） |
| N4 | `test_n4_single_form_decision_id_must_be_bound_to_the_candidate` | RED |
| N5 | `test_k7_repository_decision_set_has_no_conflict`（条件変更） | 境界（変更後も成功） |
| N6 | `test_l6_repository_issue_set_is_consistent`（条件変更） | 境界（変更後も成功） |
| N7 | `test_n7_all_candidate_records_validate_or_are_allowlisted` | RED |
| N8 | `test_n8_historical_allowlist_declares_the_single_seed_entry` | RED |
| N9 | `test_n9_authority_reference_candidate_passes_the_v3_validator` | 境界（いま成功） |
| N10 | `test_n10_machine_readable_decision_record_is_persisted` | RED |
| N11 | `test_n11_every_bundle_candidate_has_an_effective_decision` | 境界（いま成功） |
| N12 | `test_n12_issue_is_registered_and_nothing_is_in_progress` | RED |

## 3. 実測した失敗内容（RED 7件）

`.venv/bin/python3 -m pytest tests/test_issue_intake_v4_single_candidate.py -v`を
自分で実行して確認した実測値である。`7 failed, 4 passed in 0.09s`、collected 11 items、
error 0件、import error 0件。

| N | 失敗したassertion | 実測値 |
| --- | --- | --- |
| N1 | `assert intake.validate_human_triage_decision(...) is True`（164行） | `IntakeError: human_triage_decision_field_unknown: candidate_ref`（`issue_intake_v4.py` 769行のkey集合厳密一致検査） |
| N2 | 同上のhappy path確認（218行） | `IntakeError: human_triage_decision_field_unknown: candidate_ref`（同769行） |
| N4 | `assert error.value.code == "human_triage_decision_identity_invalid"`（278行） | `AssertionError`：実測は`human_triage_decision_field_unknown`（ID束縛検査に到達する前にkey集合検査で拒否される） |
| N7 | `assert unaccounted == []`（339行） | `AssertionError: assert ['ic-historical-todo-issue-intake-001--v1.json'] == []`（v2・v3両validatorに不合格、かつallowlist未作成） |
| N8 | `assert allowlist_file.is_file()`（352行） | `AssertionError: assert False`（`historical-allowlist-v1.json`が未作成） |
| N10 | `assert decision_file.is_file()`（401行） | `AssertionError: assert False`（`dec-ic-authority-reference-digest-check-001--v1.json`が未作成） |
| N12 | `assert issue_file.is_file()`（447行） | `AssertionError: assert False`（`issue-authority-reference-digest-check-001--v1.json`が未作成） |

失敗原因は7件とも対象の振る舞い・recordが未実装・未作成であることであって、
import error、fixture不在、環境差ではない。N1・N2・N4は`candidate_ref`のkey集合が
bundle形式の5 keyに厳密固定されていること（`issue_intake_v4.py` 764-769行）、
N7・N8はallowlist fileの不在、N10・N12は機械可読recordの不在に帰着する。

歴史候補がvalidator不合格であることの実測（N7の前提）：
`ic-historical-todo-issue-intake-001--v1.json`はv2・v3どちらのconfigでも
`PilotValidationError: classification candidate is invalid`で不合格である。
残り2候補（`ic-pilot-todo-growth-001--v1.json`、
`ic-authority-reference-digest-check-001--v1.json`）はv2・v3両方で合格する。

## 4. 境界例が成功する実測（4件）

同じ実行で`4 passed`を確認した。

| N | test | 成功の実測根拠 |
| --- | --- | --- |
| N1負例 | `test_n1_candidate_ref_key_set_deviations_are_rejected` | key欠落1種・混在3種の計4 variantがすべて`human_triage_decision_field_unknown`で拒否される。実装後も「過不足・混在は拒否」（N1）で拒否され続けることを固定する |
| N3 | `test_n3_existing_bundle_form_decisions_keep_validating` | `validate_triage_decision_repository`の有効decisionのうちbundle形式が41件、全件`bundle_sha256 == e01c0feb…`、`decision_maker == human` |
| N9 | `test_n9_authority_reference_candidate_passes_the_v3_validator` | 対象候補がv3 configの`validate_record_file`で合格し、`record_id`・`content_digest`・file SHA-256が固定値と一致 |
| N11 | `test_n11_every_bundle_candidate_has_an_effective_decision` | bundle内候補ID 41件に対し、`resolve_effective_triage_decisions`の未判断が実測0件（41件すべてに有効decisionあり）。**実行して成功を確認した** |

## 5. k7・l6の条件変更（N5・N6）と変更後の実測

変更は`tests/test_issue_intake_v4.py`の2 test（`git diff --stat`実測：
`1 file changed, 22 insertions(+), 2 deletions(-)`、docstring追加を含む）だけである。

| test | 変更内容 |
| --- | --- |
| `test_k7_repository_decision_set_has_no_conflict` | `bundle_sha256 == BUNDLE_SHA`のassertを`if "record_path" not in decision["candidate_ref"]:`で囲み、「bundle形式のdecisionは既知bundle SHAを指す」へ狭めた。単体形式（`record_path` keyを持つもの）は対象外 |
| `test_l6_repository_issue_set_is_consistent` | Issue側の`bundle_sha256 == BUNDLE_SHA`のassertを同じ条件で囲んだ |

他のassert（candidate_id一致、`decision_maker`、`state: registered`、昇格整合、
`in_progress` 0件、file数と有効数の一致）は変更していないため、既存41 decision・
3 Issueの保護は変わらない。単体形式recordはまだ存在しないため、変更後もこの2 testは
現repositoryで成功し続ける。実測：
`.venv/bin/python3 -m pytest tests/test_issue_intake_v4.py -q`で`38 passed in 0.12s`。

## 6. 公式全Testの実測

`.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt <scratchpad>`
を実行した。receiptはscratchpad配下だけに置き、repositoryへは保存していない。

| 項目 | 実測値 |
| --- | --- |
| status | `failed`（exit code 1） |
| passed | 1024 |
| failed | 7 |
| errors | 0 |
| skipped | 0 |
| xfailed / xpassed | 0 / 0 |
| total | 1031 |
| command | `.venv/bin/python3 -m pytest -q` |
| python_version | 3.9.6 |
| pytest_version | 8.4.2 |
| fallback_used | `false` |
| config_digest | `890380460e063e508145450cf6e80865409d20035dfc2265b99c364f03b8b6ea` |
| source_state_digest | `c4c56776bc5093d11ea3477d237cdee79dacaef09adc5f5b1b9e2e9fa37389a5` |

失敗7件は新規file`tests/test_issue_intake_v4_single_candidate.py`の7件だけである。
既存Testはk7・l6の条件変更後を含めてすべて成功しており（1024 passed）、
既存の受入済み挙動を1件も壊していない。

test関数の機械計数（`tests/test_*.py`をASTで解析）は次である。

| 対象 | 新規を含む | 新規を除く |
| --- | --- | --- |
| testファイル | 141 | 140 |
| `test_`関数 | 838 | 827 |

## 7. 宣言→RED対応表の機械検査

`records/development/2026-08-06-intake-v4-declaration-red-map-v1.json`に、
N1〜N12それぞれの対応test、`red_now`、境界例の理由を記録した。ASTで対象2 fileの
test関数名の実在を照合した結果、`missing_tests: []`、`unmapped_declarations: []`
（testの無いNは0件）である。REDを持つ宣言7件（N1・N2・N4・N7・N8・N10・N12）、
境界固定の宣言5件（N3・N5・N6・N9・N11）で、提案§5の関門（REDの無いNが0件）を満たす。

## 8. 変更していない範囲

- 実装コード（`tools/`配下すべて。`issue_intake_v4.py`、`issue_resolution_pilot.py`を含む。
  §1のSHA-256で未変更を固定した）。
- 既存Test（k7・l6の2件以外。`tests/`配下の既存140 fileのうち変更は
  `tests/test_issue_intake_v4.py`の1 fileだけ）。
- 候補bundle、既存41 decision、既存3 Issue、V1凍結レーン、config v1〜v4、schema、
  checklist、Current Plan、TODO、既存記録（上書き、削除、無効化、stale化はしていない）。
- allowlist file、機械可読decision record、Issue recordは**作成していない**
  （GREEN側の仕事であり、REDはその不在で失敗する）。
- commit、push、tag、PR、CI、外部送信は行っていない。作業終了時点の`git status`は、
  変更1件（`tests/test_issue_intake_v4.py`）、未追跡3件（新規test 1件、記録2件）だけである。
