# Claude → Codex：Task Contract固定入力の恒久対応 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-task-contract-source-pin-implementation.md`

## 1. 作成したrecord

| record | 内容 |
| --- | --- |
| `records/development/2026-08-05-task-contract-lifecycle-status-early-pilot-v1.json` | `issue-resolution-early-pilot-v1`を`completed_carried_forward`とする。contract path、contract file SHA-256 `69e2c731…`、根拠source、content digestを持つ |
| `records/development/2026-08-05-task-contract-lifecycle-status-session-transcript-v1.json` | `session-transcript-eventual-preservation-v1`を`active_stale`とする。根拠はDevelopment Policyの固定Digest `d37a60ab…`と現在値`9078276d…`の不一致 |
| `records/development/2026-08-05-task-contract-source-pin-early-pilot-v1.json` | early-pilot契約のみ。`docs/current/reviewcompass3-plan-current.md`をSHA-256 `0ab828f4…`とcommit `c475becb…`へ固定。`applicable_lifecycle_statuses`を歴史状態4種に限定 |
| `records/development/2026-08-05-task-contract-source-pin-green-evidence-v1.md` | GREEN Evidence |

いずれもnew-only。既存Task Contract fileは1 byteも変更していない。
`session-transcript-eventual-preservation-v1`のsource pinは作成していない。

根拠の記載について一点補足する。early-pilotの`completed_carried_forward`の根拠として、
後続v2の`parent_contract_ref`（early-pilot v1を同一SHA-256で参照）と、
`work_items[0].status_at_creation: completed_carried_forward`の両方を記録した。
ただし`carried_forward_work.source_contract_ref`が指すのはtodo-compaction v1であり、
early-pilot v1そのものではない。status recordにはこの区別が分かる形で書いた。

## 2. RED／GREEN結果

- RED：`11 failed in 0.41s`。実装が存在しない状態で11件すべて失敗。
- GREEN：`11 passed`。

固定した受入は指示の6項目に対応する。歴史状態のearly-pilot契約がPlan更新後もpinで通ること、
activeな契約が固定source変更で停止すること、`active_stale`がpinで通らないこと、
pinのcommit不存在・blob不一致・contract digest不一致・競合pinの停止、
pin無し歴史状態の停止（working tree一致時も通さない）、CLIの既存key保持である。

停止codeは`pin_unresolvable`と`source_pin_mismatch`に固定した。
`active_stale`は`stale_fixed_source`で停止する。

pinの無い固定sourceは、pin recordの`unpinned_source_policy: "verify_working_tree"`という
明示宣言に従ってworking treeで検証する。宣言のない黙ったfallbackはしていない。

## 3. 全test結果

- venv公式runner `713 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- receipt：`records/development/2026-08-05-task-contract-source-pin-green-test-receipt-v1.json`
- Plan・Checklist確定後の再実行：`713 passed`、
  receipt `records/development/2026-08-05-work-4a-v3-1-plan-alignment-green-test-receipt-v1.json`

既存testの期待値は変更していない。`tests/test_issue_resolution_pilot.py`の
`validate_task_contract_sources(...) == 9`はpin解決後もそのまま成立する。

誤った`green`名で保存されていた失敗receiptは
`2026-08-04-work-4a-v3-1-plan-alignment-failure-test-receipt-v1.json`へ改名して確定した。

## 4. commit SHA

| # | SHA | 内容 |
| --- | --- | --- |
| 1 | `77412633c36d22ced397fb04849de5852174db68` | Verify task contract fixed sources by lifecycle status |
| 2 | `7798acbcae103e385b3e570acca832a9853983fe` | Align plan and checklist with Work 4A v3.1 |

commit 1にPlan・Checklist・TODOを含めていない。
commit 2はcommit 1のGREEN確認後に作成した。
Git historyの書換え、既存Task Contract fileの書換え、Task Contract v2の作成はしていない。

## 5. 別作業へ残したもの

`session-transcript-eventual-preservation-v1`は`active_stale`のまま残した。
source pinを作らず、有効化もしていない。固定するDevelopment Policyの不一致は
Work 4A v1のrevert commit `3bca31c`に由来する。解消はWork 4Aと分離した別作業とする。
