# Task Contract Source Pin GREEN Evidence v1

## 対象

- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-task-contract-source-pin-implementation.md`
- 実装：`tools/development/issue_resolution_pilot.py`
- Test：`tests/test_task_contract_source_pin.py`（11件）
- receipt：`records/development/2026-08-05-task-contract-source-pin-green-test-receipt-v1.json`

## 作成したrecord

| record | 内容 |
| --- | --- |
| `2026-08-05-task-contract-lifecycle-status-early-pilot-v1.json` | `issue-resolution-early-pilot-v1`を`completed_carried_forward`とする |
| `2026-08-05-task-contract-lifecycle-status-session-transcript-v1.json` | `session-transcript-eventual-preservation-v1`を`active_stale`とする |
| `2026-08-05-task-contract-source-pin-early-pilot-v1.json` | early-pilot契約のCurrent Planを`c475bec`のblobへ固定する |

いずれもnew-onlyであり、既存Task Contract fileを変更していない。

## 根拠の記載精度

early-pilotの`completed_carried_forward`の根拠として、後続
`issue-resolution-todo-compaction-implementation-v2`の次の二点を記録した。

1. `parent_contract_ref`がearly-pilot v1を同一SHA-256（`69e2c731…`）で参照している。
2. `work_items[0].status_at_creation`が`completed_carried_forward`であり、
   `carried_forward_work`がWI-001をcontaining commit `64782ec`へ結んでいる。

なお2の`carried_forward_work.source_contract_ref`が指すのはtodo-compaction v1であり、
early-pilot v1そのものではない。根拠recordにはこの区別が分かる形で書いた。

## 検証規則

| lifecycle status | 固定sourceの検証先 |
| --- | --- |
| `active`（status record無しを含む） | working tree。不一致は`fixed source is stale or unavailable` |
| `active_stale` | 検証せず`stale_fixed_source`で停止。source pinで有効化しない |
| `completed`／`completed_carried_forward`／`superseded`／`historical` | source pin recordが必須。pinがある固定sourceは`git cat-file blob <commit>:<path>`で検証 |

pinの無い固定sourceは、pin recordの`unpinned_source_policy: "verify_working_tree"`という
明示宣言に従ってworking treeで検証する。宣言が無い黙ったfallbackはしない。
歴史状態なのにpin recordが一件も無い場合は`pin_unresolvable`で停止する。

停止codeは`pin_unresolvable`と`source_pin_mismatch`に固定した。

## RED／GREEN

RED：`11 failed in 0.41s`（実装が無い状態）。
GREEN：`11 passed`。

固定した受入は次のとおりである。

1. 歴史状態のearly-pilot契約は、Current Planが更新済みでもpinのblobが一致すれば通る（実repositoryで検証）。
2. activeな契約は固定sourceが変われば停止する。
3. `active_stale`はsource pinで通せない。実データのsession-transcript契約でも確認した。
4. pinのcommit不存在、blob不一致、対象contract digest不一致、同一sourceへの競合pinを停止する。
5. source pinの無い歴史状態contractを停止する。working treeが一致していても通さない。
6. CLIは`fixed_source_count`を保ったまま`pin_resolved_count`を追加する。

## Test

- 本件：`11 passed`
- 全test：venv公式runner `713 passed`、Python 3.9.6、pytest 8.4.2、fallback false

既存testの期待値は変更していない。`tests/test_issue_resolution_pilot.py`の
`validate_task_contract_sources(...) == 9`はpin解決後もそのまま成立する。

## 非対象

`session-transcript-eventual-preservation-v1`は`active_stale`のまま残した。
source pinを作っておらず、有効化もしていない。解消はWork 4Aと分離した別作業とする。

Work 4Aの追加実装、Routine Profile再生成、Disposition Proposal生成、外部`DATA_ROOT`への
追加書込みは行っていない。Git historyの書換え、既存Task Contract fileの書換え、
Task Contract v2の作成も行っていない。
