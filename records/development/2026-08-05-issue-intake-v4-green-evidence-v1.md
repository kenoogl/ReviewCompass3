# Issue Intake V4 GREEN Evidence v1

## 対象

- 実装：`tools/development/issue_intake_v4.py`、`config/development-issue-resolution-pilot-v4.json`
- Test：`tests/test_issue_intake_v4.py`（25件）
- 正本設計：`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`
- RED：`records/development/2026-08-05-issue-intake-v4-red-evidence-v1.md`
- receipt：`records/development/2026-08-05-issue-intake-v4-green-test-receipt-v1.json`

## 結果

- V4 acceptance：`25 passed`
- 全test：venv公式runner `802 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- **従来失敗していた1件（`test_repository_contains_only_the_single_valid_pilot_subject`）も解消した。**

## 実装した不変条件

| 不変条件 | 実装 |
| --- | --- |
| 登録数に上限を置かない | v4 configは`maximum_issue_subjects`も`maximum_registered_issues`も持たない。`load_config`が存在を拒否する |
| `in_progress`は最大1件 | `count_active_issues`は`in_progress`だけを数える。二件目は`active_issue_limit_exceeded` |
| 非active状態は算入しない | `registered`、`untriaged`、`deferred`、`suspended`、`resolved`、`rejected`を数えない |
| 登録だけで中断しない | `register_issue`が`suspend_issue_ids`を`suspend_requires_blocks_and_ruling`で拒否 |
| 再開は解決か裁定が必要 | `resume_issue`が未解決blockerかつ裁定なしを`resume_requires_resolution_or_ruling`で拒否 |
| 循環する関係を正本へ保存しない | `propose_blocks`が提案関係をまず検査し、循環なら`relations`をそのまま返す |
| 循環時は作業中0件 | 影響Issueを`suspended`へ移し、0件でなければ`cycle_detection_partial_write` |
| candidateの必須証跡8件 | `validate_root_cause_candidate`が欠落を`root_cause_candidate_incomplete`で拒否 |
| 原子性 | candidate作成と`suspended`化を一単位で返す。途中失敗は両方書き込まない |
| candidateは無権限 | `authorize_from_root_cause_candidate`がHuman裁定なしを`human_ruling_required`で拒否 |
| 自動昇格の禁止 | `promote_candidate_to_issue`が`promote_to_issue`真かつ裁定ありを要求 |
| TODO再累積の防止 | `build_todo_projection`は`in_progress`の入口だけ。禁止markerと上限を`validate_todo_projection`で検査 |

## 実装中に見つけて直した欠陥

初回の候補抽出は、`- `で始まる項目の**先頭行だけ**を引用として切り出していた。
実snapshotの項目は複数行に折り返されており、X3（「実装済み」等＋commit SHA）の語が
継続行にある項目を除外できず、履歴2件が候補に混入していた（43件）。

継続行を同じ項目へ畳んでから規則を適用する形へ修正し、41件になった。
除外できた2件はいずれも`commit f9adef4で実装済み`と明記された履歴である。
testの期待は変更していない。

## 既存testの取扱い

`tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`
の検査対象を、設計§1.3に従い「候補file数が1件」から次へ置き換えた。

- Issue recordがちょうど1件である（Pilot subjectは1件のまま）。
- v2規約の候補`IC-PILOT-TODO-GROWTH-001`が引き続きv2 configで検証を通る。
- 他の候補はV4 intakeの語彙で作られるため、V2 configで再判定しない。

testを緩めたのではなく、**契約に合った不変条件へ検査対象を移した**。
Pilot subjectが1件であることは、むしろ以前より直接的に検査している。

v2、v3のconfigとrecordは変更していない。既存Issueへ`state`を書き込んでいない。

## 非対象

候補の自動Issue昇格、優先順位付け、統合、根本原因Issue化、再開はいずれも行っていない。
Plan作成、実作業開始、外部送信、pushも行っていない。
