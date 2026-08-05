# V4 Issue永続化：RED Evidence v1

## 対象

指示：`records/session-handoffs/2026-08-05-codex-to-claude-v4-issue-persistence-and-session-policy-triage.md`

現行V4の`promote_candidate_from_decision()`はメモリ上のIssue dictを返せるが、V4 Issueのfile path、
content digest、candidate／decision参照の再検証、repository集合検証を持たない。ここを実装する。

旧PilotのIssue directory`.reviewcompass/workflow/issues/`には「Pilot subjectは1件だけ」という
検査があるため、V4 IssueはV4専用directoryへ置く。旧Pilotは変更しない。

## 固定入力

| 対象 | 値 |
| --- | --- |
| V4 config | `config/development-issue-resolution-pilot-v4.json` |
| V4実装 | `tools/development/issue_intake_v4.py` |
| V4受入test | `tests/test_issue_intake_v4.py` |
| 候補bundle | `records/development/2026-08-05-historical-todo-intake-candidates-v1.json` |
| bundle SHA-256 | `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` |
| 既存V4 triage decision | `.reviewcompass/workflow/triage-decisions-v4/` |

## 追加した受入test（L1〜L6）

指示§2の6条件を、既存V4受入testへ追加した。既存のI／J／K系testは変更していない。

| test | 固定する条件 |
| --- | --- |
| L1 | Human decisionから作ったV4 Issueを、決定的なpathとcontent digestで保存・再読込・検証できる。初期stateは`registered`で、active Issueに数えない。`triage_decision_ref`はdecisionのpath・file SHA-256・content digestを持つ。候補bundleのbytesは不変である |
| L2 | V4 Issue directoryが旧Issue directoryと同一、またはconfigに存在しない場合、config validationが`config_invalid`で拒否する |
| L3 | bundle SHA、candidate digest、decision file SHA、decision content digest、decision pathのpath escape、存在しないdecision path、未知field、content digest、record pathの改竄をすべて拒否する。保存後にdecision fileを書き換えた場合も参照が成立しない |
| L4 | Human decisionなし、`promote_to_issue: false`、`disposition`不一致ではIssueを作れない。issue ID不一致のrecordを拒否し、同一candidateへ有効Issueが二件あればrepository検証が拒否する |
| L5 | 旧PilotのIssue directoryは1件のままで、旧PilotのvalidatorがそのIssueを通す。V4 validatorは旧Issueを`v4_issue_schema_version_unsupported`で扱い、V4語彙で再判定しない |
| L6 | V4 Issue repository集合検証が通り、有効Issueの参照するdecisionが`blocking: false`かつ昇格承認済みである。active Issueは0件である |

L1、L3、L4は、実repositoryを触らないよう、候補bundleだけを写した一時作業rootの上で
decision fileとIssue fileを実際に書き出して検証する。

## RED実行結果

公式Test runner（`tools/development/policy_test_runner.py`、suite `full`）で実行した。

- receipt：`records/development/2026-08-05-v4-issue-persistence-red-test-receipt-v1.json`
- status：`failed`、exit code：`1`
- 結果：`3 failed, 809 passed, 3 errors in 3.85s`

失敗・エラーの6件は、追加したL1〜L6である。理由は、V4 configに`directories.issue_record_v2`が
無いこと、および`build_v4_issue_record`、`v4_issue_path`、`validate_v4_issue_record`、
`validate_v4_issue_repository`が未実装であることである。

既存の809testは変更しておらず、すべて通過している。
