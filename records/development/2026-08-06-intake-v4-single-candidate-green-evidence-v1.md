# Issue Intake V4 単体候補参照と候補全件検証 GREEN Evidence v1

- 正本設計：`docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md`
  （`approved`、2026-08-06 Human承認済み。規範宣言N1〜N12）
- 宣言→RED対応表：`records/development/2026-08-06-intake-v4-declaration-red-map-v1.json`
  （REDの無いN 0件を機械確認済み）
- N10の値の出典：`records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md`
  （Markdown裁定`DEC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`）
- 実行環境：Python 3.9.6、pytest 8.4.2、公式venv runner、fallback `false`
- 実行時刻：2026-08-06T14:40:39+09:00（公式全Test receiptの`recorded_at`）
- RED基準commit：`d6b043a`（RED 7件＋境界4件を固定。公式全Test `1024 passed / 7 failed`）

## 0. 何を行ったのか（範囲の明示）

**同じTestを弱めずGREENにした。** RED commit `d6b043a`が固定した
`tests/test_issue_intake_v4_single_candidate.py`（RED 7件＋境界4件）は1文字も変更しておらず
（§5参照。file SHA-256は`d6b043a`時点と現在で同一）、実装1 fileの変更とrecord 3件の
new-only作成だけで11件すべてを通した。

**課題は登録のみで、着手していない。** 新Issue
`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`は`state: registered`（version 1）であり、
`in_progress`のIssueは実装前と同じく**0件**である（N12、§3参照）。

**行っていないこと**は次である。

- bundle形式の既存経路の変更（N3）。`_load_candidate_bundle`は無変更である。
- 既存41 decision、既存3 Issue、候補bundle、V1凍結レーン（`triage-decisions`、`issues`）、
  config v1〜v4、schema、checklist、Current Planの変更。
- 深さ・派生元fieldの追加、Work 6A残り項目、Work 8前倒し（提案§9の非対象）。
- commit、push、外部送信。

変更fileは`tools/development/issue_intake_v4.py`の1件だけである
（`git diff --stat`：`1 file changed, 141 insertions(+), 36 deletions(-)`）。
`git status --porcelain`は当該実装1件の変更（` M`）と、new-onlyのrecord 3件の未追跡
（`??`）だけを示す。

## 1. 固定入力（機械計算したSHA-256）

`shasum -a 256`で計算した。実装fileは**変更後**、record 3件は**作成後**の値である。

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md` | `d5164077b8a53141eb647e57f4746e3347ac4650c03a0d1d553571348fc63358` |
| `records/development/2026-08-06-intake-v4-declaration-red-map-v1.json` | `c24ebaf58eee3ce2d318084697051d41c9669e30aa756086706f9f110117ce40` |
| `records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md` | `be9e7d3a2af88a4452a5055d39be8a6e2f77514a5529a134db2086fb49664fb9` |
| `.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json` | `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6` |
| `tests/test_issue_intake_v4_single_candidate.py`（`d6b043a`時点＝現在。無変更） | `19b9da920359d55f2786e7f117db64916a250ab496f28dac1a2059a01f623a79` |
| `tools/development/issue_intake_v4.py`（変更後） | `3f864f4707badb744967490adf04f987abbba55f29362409a84d9ac00e25911e` |
| `.reviewcompass/workflow/improvement-candidates/historical-allowlist-v1.json`（新規） | `25bf17ae9d53a5a01f370b477c001d6e040a7e1e645e00cb25dbd4caa0043c0a` |
| `.reviewcompass/workflow/triage-decisions-v4/dec-ic-authority-reference-digest-check-001--v1.json`（新規） | `919f9c8803301297ed8a20e52333029020b17a4f8c7e24329fab1cf90f4a46bb` |
| `.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json`（新規） | `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe` |

提案§2の固定入力3件（問題一覧`f6d8da5e…`、Markdown裁定`be9e7d3a…`、対象候補`d4e801aa…`）の
うち後2件を上表で再計算し、記載値と一致した。宣言→RED対応表が固定する提案SHA
`d5164077…`も一致した。

## 2. N1〜N12のRED→GREEN対比

行番号はすべて変更後の`tools/development/issue_intake_v4.py`のものである。RED時の失敗は
RED基準commit `d6b043a`での実測（公式全Test `1024 passed / 7 failed`、失敗7件はすべて
対象test file内）に基づく。

| N | test（対応表どおり） | RED時 | GREEN後の実装箇所 |
| --- | --- | --- | --- |
| N1 | `test_n1_single_form_candidate_ref_decision_validates`（RED） | key集合が bundle 5 keyに厳密固定され、正しい単体形式でも`human_triage_decision_field_unknown` | 2形式のkey集合定数（624-633行）、形式判別`_candidate_ref_form`（636-645行）、`validate_human_triage_decision`での適用（862-869行） |
| N1負例 | `test_n1_candidate_ref_key_set_deviations_are_rejected`（境界） | 成功 | 過不足・混在はどちらのkey集合とも一致せず、同じ`human_triage_decision_field_unknown`で拒否され続ける（636-645行） |
| N2 | `test_n2_single_form_fingerprint_mismatches_are_rejected`（RED） | 単体形式そのものが拒否され、最初のassertで失敗 | `_load_candidate_record`（648-673行）：file実在（658行、`candidate_record_unavailable`）、実bytes SHA-256（660-662行、`candidate_record_digest_mismatch`）、record内`candidate_id`（667-670行、`candidate_not_found`）、record内`content_digest`（671-672行、`candidate_digest_mismatch`）。停止code追加は48-49行。呼出しは`_load_referenced_candidate`（676-687行）経由で888-891行 |
| N3 | `test_n3_existing_bundle_form_decisions_keep_validating`（境界） | 成功 | bundle経路は無変更（`_load_candidate_bundle`本体は非変更）。§3の再検証でbundle形式41件が変更なしで合格 |
| N4 | `test_n4_single_form_decision_id_must_be_bound_to_the_candidate`（RED） | key集合検査で先に落ち、誤codeが`human_triage_decision_field_unknown` | 単体形式がkey集合検査を通過し、既存のID束縛検査（876-883行、無変更）へ到達して`human_triage_decision_identity_invalid`で拒否 |
| N5 | `test_k7_repository_decision_set_has_no_conflict`（境界、RED commitで条件変更済み） | 成功 | 実装変更不要。単体形式decision追加後も54 passedで合格（§3） |
| N6 | `test_l6_repository_issue_set_is_consistent`（境界、RED commitで条件変更済み） | 成功 | 実装変更不要。単体形式Issue追加後も54 passedで合格（§3） |
| N7 | `test_n7_all_candidate_records_validate_or_are_allowlisted`（RED） | allowlist未作成で`ic-historical-todo-issue-intake-001--v1.json`が未宣言 | 歴史allowlist `historical-allowlist-v1.json`をnew-onlyで作成。他の候補2件はv2またはv3 validatorで合格 |
| N8 | `test_n8_historical_allowlist_declares_the_single_seed_entry`（RED） | file不存在 | 同上。top-levelは`{"entries": [...]}`、entryは`path`・`reason`・`successor_ref`を持ち、初期entryは歴史候補1件のみ。後継は`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`（`records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md`、SHA-256 `01987923…`） |
| N9 | `test_n9_authority_reference_candidate_passes_the_v3_validator`（境界） | 成功 | 対象候補は無変更（file SHA `d4e801aa…`のまま）。v3 validator合格を継続 |
| N10 | `test_n10_machine_readable_decision_record_is_persisted`（RED） | file不存在 | `build_human_triage_decision`へ単体形式対応を追加（725-782行、単体分岐は742-761行）し、機械処理で`dec-ic-authority-reference-digest-check-001--v1.json`を生成。`content_digest`は正準計算。値はMarkdown裁定§3のとおりで、昇格だけをHuman承認（「載せてよい」）により`issue_promotion: {approved: true, issue_id: ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001}`へ更新。`rationale`・`next_action`はMarkdown裁定§2・§4の要約 |
| N11 | `test_n11_every_bundle_candidate_has_an_effective_decision`（境界） | 成功 | bundle内41候補すべてに有効decisionが存在（§3の再検証で41件一致、未判断0件） |
| N12 | `test_n12_issue_is_registered_and_nothing_is_in_progress`（RED） | file不存在 | `build_v4_issue_record`へ単体候補（本文が`problem`）対応を追加（1126-1131行）し、`validate_v4_issue_record`の参照検証を両形式対応へ（1201-1205行）。生成した`issue-authority-reference-digest-check-001--v1.json`は`state: registered`・version 1で、decisionへの`triage_decision_ref`（file SHA-256・content_digest束縛）を持つ。`in_progress`は0件のまま |

decision ID規則（`DEC-<candidate_id>`）、保存path規則、`human_fields`検証、昇格整合検査は
既存codeのまま両形式に適用されている（N4。876-883行、884-886行、893行以降は無変更）。

## 3. Testと再検証の実測

いずれも自分で実行して確認した。

| 対象 | command | 結果 |
| --- | --- | --- |
| 対象Test | `.venv/bin/python3 -m pytest -q tests/test_issue_intake_v4_single_candidate.py` | **`11 passed in 0.04s`** |
| 隣接する既存Test | `.venv/bin/python3 -m pytest -q tests/test_issue_intake_v4.py tests/test_issue_resolution_pilot.py` | **`54 passed in 0.13s`** |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt <scratchpad>` | **`1031 passed`**（failed 0） |

公式全Test receiptの内訳は次である。receiptはscratchpad配下だけに置き、
repositoryへは保存していない。

| 項目 | 実測値 |
| --- | --- |
| status | `passed`（exit code 0） |
| passed / failed / errors / skipped | 1031 / 0 / 0 / 0 |
| xfailed / xpassed | 0 / 0 |
| total | 1031 |
| command | `.venv/bin/python3 -m pytest -q` |
| python_version / pytest_version | 3.9.6 / 8.4.2 |
| fallback_used | `false` |
| config_digest | `890380460e063e508145450cf6e80865409d20035dfc2265b99c364f03b8b6ea` |
| source_state_digest | `748a1b974dfa815638a040037cd524398e7313e0c37e52ac39d934b681fdf093` |
| recorded_at | `2026-08-06T14:40:39+09:00` |

RED基準の`1024 passed / 7 failed`（total 1031）から、totalは変わらず失敗7件がすべて
GREENになった。`config_digest`はRED時と同一である。

### validator変更に伴う再検証（提案§7の緩和）

実装後に`validate_triage_decision_repository`と`validate_v4_issue_repository`を
repository全件へ再実行した。

| 項目 | 実測値 |
| --- | --- |
| 有効decision | **42件**（既存41＋新1）。全件合格 |
| うちbundle形式／単体形式 | 41件／1件 |
| 有効Issue | **4件**（既存3＋新1）。全件合格 |
| Issueのstate | 4件すべて`registered` |
| `in_progress` | **0件** |

### 既存Testを弱めていないこと

| 検証 | 結果 |
| --- | --- |
| 変更fileの数 | `tools/development/issue_intake_v4.py` 1件のみ |
| GREEN実装時の`tests/`変更 | 0件（対象test fileのSHA-256は`d6b043a`時点と現在で同一の`19b9da92…`） |
| fixture変更 | 0件 |
| skip／xfail／assertion緩和 | 0件 |
| 既存record変更 | 0件（record 3件はすべてnew-only） |

## 4. 変更していない範囲

- `tests/`配下すべて。1 byteも触っていない。
- `tools/`配下のうち`tools/development/issue_intake_v4.py`以外すべて
  （`issue_resolution_pilot.py`を含む）。
- 候補bundle本体`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`
  （SHA `e01c0feb…`のまま）と、bundle指紋を参照する58 file。
- 既存41 decision、既存3 Issue、候補record 3件（対象候補は`d4e801aa…`のまま）。
- V1凍結レーン（`triage-decisions`、`issues`）、config v1〜v4、
  `improvement_candidate`のschema、checklist、Current Plan、製品schema、UI、automation。
- 既存記録（`records/`配下の既存file）。上書き、削除、無効化、stale化はしていない。
- commit、push、tag、PR、CI、外部送信、LLM呼び出しは行っていない。

## 5. 残っている限界

1. **V1凍結レーンは凍結のままである。** 単体形式はV4レーン
   （`triage-decisions-v4`、`issues-v4`）だけに導入し、V1の解除・追加は行っていない。
2. **bundleは不変のままで、bundle経路の条件も変えていない。** bundle形式のdecision・
   Issueは従来どおり既知bundle SHA `e01c0feb…`に束縛される（N5・N6）。単体形式の保存先も
   `triage-decisions-v4`／`issues-v4`のみで、ID規則・実在検証・digest束縛は既存のまま
   適用される（提案§7の緩和）。
3. **深さ・派生元fieldは未導入である**（提案§9のとおり別途判断）。単体形式のcandidate_refは
   候補recordを直接指すだけで、候補間の派生関係は表現しない。
4. **新Issueは登録のみで、解決計画・着手はしていない。** 着手（`in_progress`化）と
   検査器の実装・判別規則（対象keyのallowlist）の確定は、decisionの`next_action`のとおり
   Human判断まで開始しない。
5. **歴史allowlistのentry検査はTest側の形（`path`・`reason`・`successor_ref`の存在と
   非空）にとどまる。** allowlist自身を検証する専用validatorは作っていない。entry追加は
   new-onlyの宣言とHuman判断による。
6. **単体形式の候補検証は指紋照合（file SHA-256・`candidate_id`・`content_digest`）で
   あって、候補recordの中身のschema再検証ではない。** 候補自体の合格はN7の全件検証
   （v2／v3 validator）が別経路で維持する。
