# Work 4A v3.1 Acceptance GREEN Evidence v1

## 対象

- 実装：`tools/development/work4a_rebuild_v3.py`（v3.1差分を追加）
- Test：`tests/test_work4a_rebuild_v3_1_e2e.py`（21件）
- 正本設計：`docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md`
- 承認：`DEC-WORK4A-REBUILD-DESIGN-004`
- RED：`records/development/2026-08-04-work-4a-v3-1-acceptance-red-evidence-v1.md`
- receipt：`records/development/2026-08-04-work-4a-v3-1-acceptance-green-test-receipt-v1.json`

## 結果

- v3.1 acceptance：`21 passed`
- v3 acceptance：`22 passed`（変更していない）
- 全test：venv公式runner `702 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 実装した不変条件

| 不変条件 | 実装 |
| --- | --- |
| Routine Profileは機械事実のみ | `validate_routine_profile_document`が`_ROUTINE_FIELDS`外を`unknown_field`で拒否 |
| 痕跡は構文一致のみ | `_effect_markers`が呼出名の一致だけで付ける。別名輸入と間接呼出を追わない |
| 未検出は副作用なしを意味しない | `marker_detection.absence_does_not_imply_no_effect`が`true`でなければ`marker_detection_flag_missing` |
| symbol_id重複で停止 | `_collect_routines`が重複時に`symbol_id_collision`と全`code_reference`を返す |
| lambdaは除外して記録 | `excluded_constructs`へ件数と位置を残す |
| Proposalは非権威 | `advisory`が`true`でなければ`advisory_used_as_authority` |
| 参照は同一Profile内のみ | 未知IDと自己参照を`advisory_reference_unresolved` |
| 根拠必須 | `evidence_refs`が空または語彙外`kind`で`advisory_evidence_missing` |
| 根拠の整合 | `code_reference`がProfileの値と一致しなければ`advisory_reference_unresolved` |
| 生成元の束縛 | `routine_profile_content_digest`不一致で`content_digest_mismatch` |
| dispositionはHumanのみ | `build_entry_documents`が`disposition_source`以外を`advisory_used_as_authority` |
| group取りこぼし禁止 | `expand_group_rules`が未該当を`group_coverage_incomplete` |
| 構造一致は手掛かり | `structural_match_group_id`は同一`structure_digest`へ機械割当。`merge`を自動確定しない |

## 実装中に判明した設計上の論点と対処

候補要約の分類keyについて、機械の候補分類（`known`／`unknown`）とHumanの処置（`reuse`ほか）の
二軸が同じfieldを共有していた。v3.1で軸を分けた結果、Policy v2では`new`が語彙から外れる。

対処として、Attestationの`candidate_run`節へ`extraction_rule_version`を記録し、
**候補実行が宣言した抽出規則versionで語彙の軸を決める**ようにした。
規則v1の候補実行は従来語彙、規則v2は候補分類語彙で検証する。
これによりv3の既存Attestationを読めるまま、v3.1の軸分離を満たす。

## testの調整

`test_i14_rule_v2_creates_new_candidate_run`で、既存Candidate Runを作る呼出へ
`extraction_rule_version=1`を明示した。
`build_candidate_run`の既定値をPolicyの宣言versionから取るようにしたため、
「既存の規則v1のrun」と「新しい規則v2のrun」を区別する必要が生じたためである。

受入条件そのもの（新しいIDになること、既存recordが書き換わらないこと）は変更していない。
他の20件は初回作成時のままである。

## 非対象

LLMによるDisposition Proposalの実生成は行っていない。testはschemaと検証だけを対象とする。
Operational Human Decision、Entry、Relation、Baselineの実データ作成も行っていない。
