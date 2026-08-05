# V4 Human triage永続化：RED Evidence v1

## 対象

指示：`records/session-handoffs/2026-08-05-codex-to-claude-v4-human-triage-persistence.md`

候補bundle内の候補を、Humanの判断recordから指紋付きで参照できるようにする。候補bundleは
機械抽出時のimmutableな観測として保持し、Humanの判断正本は一候補につき一件の
`human_triage_decision` schema version 2とする。

## 固定入力

| 対象 | 値 |
| --- | --- |
| 候補bundle | `records/development/2026-08-05-historical-todo-intake-candidates-v1.json` |
| bundle SHA-256 | `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` |
| V4 config | `config/development-issue-resolution-pilot-v4.json` |
| V4実装 | `tools/development/issue_intake_v4.py` |
| V4受入test | `tests/test_issue_intake_v4.py` |

## 追加した受入test（K1〜K7）

指示§5の7条件を、既存V4受入testへ追加した。

| test | 固定する条件 |
| --- | --- |
| K1 | bundle内candidateをbundle path・bundle SHA・bundle schema version・candidate ID・candidate content digestで参照するV4 decisionが検証を通る |
| K2 | bundle SHA不一致、candidate ID不存在、candidate digest不一致、bundle schema version不一致、未知field、path traversal、path不一致、未知disposition、content digest不一致、V1 schemaのdecisionを拒否する |
| K3 | 同一candidateへ`supersedes`を持たないdecisionが二件あれば拒否し、`supersedes`で旧recordを参照する改訂だけを有効とする。`supersedes`のcontent digestが古い場合も拒否する |
| K4 | decisionなし、`promote_to_issue: false`、`disposition`不一致、candidate参照不一致、競合decisionありではIssue化できない。条件をすべて満たす場合だけIssue recordを作り、そのとき候補の`human_fields`は`null`のままである |
| K5 | 承認済み四decisionが検証を通り、候補bundleのbytesとSHA-256が不変である。保存済みrecordがある場合は、それも検証を通り、決定的に再構築した内容と完全一致する |
| K6 | 旧V1 decisionと旧Pilot検証が通り続け、V1のdecision directoryの内容が増えない |
| K7 | repository全体のV4 decision集合に競合が無い |

## RED実行結果

公式Test runner（`tools/development/policy_test_runner.py`、suite `full`）で実行した。

- receipt：`records/development/2026-08-05-v4-human-triage-persistence-red-test-receipt-v1.json`
- status：`failed`、exit code：`1`
- 結果：`7 failed, 802 passed in 3.85s`

失敗した7testは、追加したK1〜K7である。失敗理由は、V4 configに
`directories.human_triage_decision_v2`が無いこと、および
`build_human_triage_decision`、`human_triage_decision_path`、
`validate_human_triage_decision`、`resolve_effective_triage_decisions`、
`promote_candidate_from_decision`、`validate_triage_decision_repository`、
`canonical_digest`が未実装であることである。

既存の802testは変更しておらず、すべて通過している。

## 設計上の判断（実装前に固定した点）

### V4 decisionを別directoryへ置く理由

既存の`tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`
は、V1のdecision directory`.reviewcompass/workflow/triage-decisions`に対して
`len(decision_files) <= 1`を固定している。この事実は、同directoryへV4 decisionを1件置いた
実験で確認した（`assert 2 <= 1`で失敗）。

V4 decisionを同directoryへ置くと、この既存testを緩めない限り必ず壊れる。testを緩めることも
V1互換性を壊すことも禁止されているため、V4 schema version 2のdecisionは、V4 configで固定する
専用directory`.reviewcompass/workflow/triage-decisions-v4`へ置く。V1 directoryは変更しない。

これはV4 configがV4のdirectory規則を持つという指示§4の枠内であり、集約recordの発明ではない。
粒度は「一候補につき一判断record」のまま維持する。

### `historical_completed`を追加する理由

四候補に対するHumanの判断は「当時の完了済み手順の記録であり、現在解くIssueではない」である。
既存語彙の`reject`は「候補としての内容を退ける」意味になり、「当時は正しく実行され完了した
手順である」という事実を失う。`defer`は「後で扱う」意味になり、現在も未処理であるという
誤読を生む。よってV4 configの`human_triage_decision_v2.dispositions`へ`historical_completed`を
追加して固定する。V1のdisposition語彙は変更しない。
