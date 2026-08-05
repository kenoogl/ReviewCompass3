# 読み取り専用argv executor最小slice RED Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 承認：`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`
  （`records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-decision-v1.md`）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-read-only-argv-executor-slice.md`

## 1. 追加したTest

`tests/test_structured_argv_executor.py`を新規作成した。実装対象module
`tools/development/structured_argv_executor.py`はまだ作っていない。

Testは**実processを起動しない**。runnerをfakeへ差し替え、呼出し回数、受け取ったargv、cwdを
記録して観測する。停止する場合は`runner.calls == []`を必ず確認する。

## 2. RED実行結果

```text
.venv/bin/python3 -m pytest -q tests/test_structured_argv_executor.py
→ 13 errors（ModuleNotFoundError: tools.development.structured_argv_executor）
```

moduleが存在しないため全testが失敗する。実装は書いていない。

## 3. 固定した受入条件

| # | 条件 | test |
| --- | --- | --- |
| 1 | `git status --porcelain -- <pathspec>`がlistのままfake runnerへ一度だけ渡る。空白、引用符、backtick、`$`、`*`、非ASCIIを含むpathspecが結合・展開・分割されない。receiptは既存validatorで検証できる | `test_argv_reaches_the_runner_as_a_list_without_reshaping`、`test_template_without_pathspec_is_accepted`、`test_separator_with_no_pathspec_is_accepted` |
| 2 | 別のGit subcommand、前置option、`--`より前の余分な引数、`--`無しのpathspec、`--porcelain`無し、`git`以外、区切りの二重を拒否し、runner呼出しは0 | `test_operations_outside_the_template_are_rejected` |
| 3 | `project_artifact_write`／`git_metadata_write`／`external`／`unknown`を含むinventoryを拒否し、runnerを一度も呼ばない | `test_non_read_only_inventories_are_rejected` |
| 4 | 空list、空文字列の先頭要素、非文字列要素を拒否する。空文字列の**pathspec**はそのまま渡す | `test_argv_shape_problems_are_rejected` |
| 5 | cwdはproject root基準の相対pathだけ。絶対path、`..`、外への解決、symlink、不在、通常fileを拒否し、`.`と実在directoryを受ける | `test_cwd_boundaries_are_enforced` |
| 6 | preflightが`granted`でない、またはidentityが不一致ならrunnerを一度も呼ばない。executorは権限を判定・付与・再分類しない | `test_preflight_failures_never_reach_the_runner`、`test_executor_does_not_grant_or_reclassify_permissions` |
| 7 | fake runnerの失敗結果はreceiptへ記録し、例外で隠さない。入力検証の失敗とprocess結果の失敗を混同しない | `test_process_failure_is_recorded_not_raised`、`test_input_failure_and_process_failure_are_not_confused` |
| 8 | `argv`をshell文字列へ連結せず、`shell=True`を使わない（source inspection） | `test_module_never_builds_a_shell_string`、`test_module_declares_its_stop_codes` |

## 4. この段階で作っていないもの

- 実装module本体。
- cache root設定、環境変数設定、既存call siteの置換。
- Git metadata書込み、project成果物書込み、external起動。
- 既存testの変更。`tests/test_operation_routing_v2.py`ほか既存testは一切触っていない。

`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。
