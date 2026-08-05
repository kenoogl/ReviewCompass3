# V4 Human triage永続化：GREEN Evidence v1（実装）

## 対象

指示：`records/session-handoffs/2026-08-05-codex-to-claude-v4-human-triage-persistence.md`
RED Evidence：`records/development/2026-08-05-v4-human-triage-persistence-red-evidence-v1.md`

この記録は**実装だけ**の作業単位を対象とする。承認済み四decision recordは別の作業単位で作る。

## 実装したもの

### 1. V4 Human triage decision schema version 2

`config/development-issue-resolution-pilot-v4.json`へ`human_triage_decision_v2`を追加し、
`tools/development/issue_intake_v4.py`へvalidatorと組み立て関数を実装した。

decision recordのfieldは次の15個で固定する。これ以外のfieldは拒否する。

`record_kind`、`schema_version`、`decision_id`、`decision_version`、`decided_at`、
`decision_maker`、`candidate_ref`、`human_fields`、`disposition`、`blocking`、
`rationale`、`next_action`、`supersedes`、`issue_promotion`、`content_digest`

`candidate_ref`は次の5個で固定する。候補bundleと候補の両方を指紋で押さえる。

| field | 意味 |
| --- | --- |
| `bundle_path` | 候補bundleの相対path |
| `bundle_sha256` | 候補bundle fileのSHA-256 |
| `bundle_schema_version` | 候補bundleのschema version |
| `candidate_id` | bundle内の`HTC-...` |
| `candidate_content_digest` | 候補自身の`content_digest` |

ID規則：`decision_id`は`DEC-<candidate_id>`、または`DEC-<candidate_id>-<接尾辞>`とする。
これにより、decision IDだけで対象候補が一意に読み取れる。

path規則：`{directories.human_triage_decision_v2}/{decision_id小文字}--v{decision_version}.json`

content digest規則：`content_digest`を除いた正準JSON（キー昇順、区切り最小、非ASCIIそのまま）の
SHA-256とする。既存V4の`_canonical_digest`と同一である。

fail-closedで拒否する条件と停止codeは次のとおり。

| 条件 | 停止code |
| --- | --- |
| 未知field、field欠落 | `human_triage_decision_field_unknown`／`human_triage_decision_field_invalid` |
| schema version不一致（V1 decisionを含む） | `human_triage_decision_schema_version_unsupported` |
| bundle pathの絶対path・`..`脱出 | `human_triage_decision_path_invalid` |
| record pathがID規則と不一致 | `human_triage_decision_path_mismatch` |
| bundle fileのSHA不一致 | `candidate_bundle_digest_mismatch` |
| bundle schema version不一致 | `candidate_bundle_schema_version_mismatch` |
| candidate ID不存在 | `candidate_not_found` |
| candidate digest不一致 | `candidate_digest_mismatch` |
| 未知disposition | `human_triage_decision_disposition_invalid` |
| 昇格の整合性違反 | `human_triage_decision_promotion_inconsistent` |
| content digest不一致 | `human_triage_decision_digest_mismatch` |

### 2. 判断の競合と改訂

`resolve_effective_triage_decisions()`が候補ごとにdecisionを束ね、有効なものを一つだけ決める。

- 同一候補に`supersedes`を持たないdecisionが二件以上あれば`human_triage_decision_conflict`で拒否する。
- 改訂は旧recordを上書きせず、`decision_version`を上げ、`supersedes`へ旧recordの
  `decision_id`・`decision_version`・`content_digest`を持たせる。
- `supersedes`の参照先が無い、digestが古い、versionが増えていない、同じrecordを二重に改訂している
  場合はいずれも拒否する。
- `validate_triage_decision_repository()`が、V4 decision directoryのrecordを単体検証したうえで、
  集合としての競合も確認する。
- V1 decisionはV4 directoryの外にあり読み込まない。V4規則で再判定も変更もしない。

### 3. Issue昇格の権限をdecisionへ移す

`promote_candidate_from_decision()`は、次をすべて満たす場合だけIssue recordを作る。

- `decision_maker`が`human`である
- `promote_to_issue`が`true`である
- `disposition`が`issue_resolution`である
- decisionのcandidate参照が、渡された候補およびbundle digestと完全一致する
- 同一候補に競合する有効decisionが無い

満たさない場合は`human_triage_decision_required`、または具体的な検証codeで停止する。
この関数は候補bundleの`human_fields`を読まず、書き換えもしない。候補の`human_fields`は
生成時の未記入観測（すべて`null`）のまま保持される。

既存V1の昇格規則（`tools/development/issue_resolution_pilot.py`）と、既存V4の
`promote_candidate_to_issue()`は変更していない。

## RED→GREEN

| 段階 | receipt | 結果 |
| --- | --- | --- |
| RED | `records/development/2026-08-05-v4-human-triage-persistence-red-test-receipt-v1.json` | `failed`／exit 1／`7 failed, 802 passed` |
| GREEN | `records/development/2026-08-05-v4-human-triage-persistence-green-test-receipt-v1.json` | `passed`／exit 0／`809 passed` |

いずれも公式Test runner（`tools/development/policy_test_runner.py`、suite `full`）で実行した。
RED時に追加した受入test K1〜K7は、実装中に一度も変更していない。

## 語彙追加の根拠：なぜ`reject`だけでは不十分か

四候補に対するHumanの判断は「当時の完了済み手順の記録であり、現在解くIssueではない」である。

- `reject`は「候補の内容を退ける」意味になる。四候補は当時正しく実行され完了した手順の記録であり、
  内容が誤っていたわけではない。`reject`を使うと、後から読む者に「その観測は誤りだった」と
  読ませてしまい、事実を失う。
- `defer`は「今は扱わず後で扱う」意味になる。四候補は完了済みであり、後で扱う予定は無い。
  `defer`を使うと未処理の滞留として誤読される。
- `duplicate`は他recordとの重複を意味するが、四候補に重複疑いは無い（bundleの
  `duplicate_suspect_count`は0）。

よって`historical_completed`をV4 configの`human_triage_decision_v2.dispositions`へ追加して固定した。
V1のdisposition語彙（`config/development-issue-resolution-pilot.json`ほか）は変更していない。

## directoryを分けた根拠

既存の`tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`
は、V1 decision directory`.reviewcompass/workflow/triage-decisions`に対して
`len(decision_files) <= 1`を固定している。同directoryへ追加のdecision fileを1件置くと
`assert 2 <= 1`で失敗することを実験で確認した。

既存testを緩めることも、V1互換性を壊すことも禁止されているため、V4 schema version 2のdecisionは
V4 configで固定する専用directory`.reviewcompass/workflow/triage-decisions-v4`へ置く。
`load_config()`は、この二つのdirectoryが同一である設定を`config_invalid`で拒否する。

粒度は「一候補につき一判断record」のままであり、集約recordは作っていない。

## 変更したfile（この作業単位）

- `config/development-issue-resolution-pilot-v4.json`
- `tools/development/issue_intake_v4.py`
- `tests/test_issue_intake_v4.py`
- `.reviewcompass/workflow/triage-decisions-v4/.gitkeep`（新規directory）
- 本Evidenceと二つのreceipt、RED Evidence

候補bundle`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`、
旧Pilotのconfig／record、V1 decisionは変更していない。
