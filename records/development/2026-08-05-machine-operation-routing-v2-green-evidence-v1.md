# 機械操作routing v2 最小縦切り GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 承認：`DEC-MACHINE-OPERATION-ROUTING-001`
  （`records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md`、
  SHA-256 `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969`）
- 承認対象の設計：`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`の§3だけ
  （SHA-256 `7c812b68b4b4b0cd282af29b44ff117e78aa172b6f2b830f6d684856f9bf7a31`）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-machine-operation-routing-v2-slice.md`

## 1. 実装物

| 種別 | path | SHA-256 |
| --- | --- | --- |
| module | `tools/development/operation_routing.py` | `f735299433b49b868b713dfcc4ed1973c7d4771f906242e3e3932e39bf269049` |
| 受入test | `tests/test_operation_routing_v2.py` | `6da141f20f7b8a31e270c6a2dc2195cbce20c908633d81e0e939e51b703d6fc4` |

moduleは決定的なlibraryであり、shellも外部processも起動しない。既存のpolicy runnerへの
import依存を持たない。最小CLIはinventoryを読んでpreflightをJSONで出すだけで、commandを実行しない。

## 2. RED→GREEN

| 段階 | 実行 | 結果 |
| --- | --- | --- |
| RED | `.venv/bin/python3 -m pytest -q tests/test_operation_routing_v2.py` | `16 errors`（moduleが存在しないため全testが失敗） |
| GREEN（対象test） | 同上 | `16 passed` |
| GREEN（公式全test） | policy runner suite `full` | `845 passed` |

RED testだけのcommitは作っていない。実装中にtestの期待を緩めていない。

公式全testのreceiptは
`records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json`である。

## 3. 受入条件1〜9の対応

| # | 条件 | 対応するtest |
| --- | --- | --- |
| 1 | inventoryがoperation ID、version、分類、必要権限、content digestを持ち、非正規JSON・未知field・重複ID・空ID・不正Digestを拒否する | `test_inventory_carries_identity_classification_permission_and_digest`、`test_inventory_rejects_broken_shapes` |
| 2 | 分類は5語だけを受理し、`unknown`はfail-closed | `test_only_the_five_classifications_are_accepted`、`test_unknown_classification_is_fail_closed` |
| 3 | preflightがinventory全体から必要権限を重複なく一回で得る。read-onlyだけなら空 | `test_preflight_collects_required_permissions_once_without_duplicates`、`test_read_only_inventory_requires_no_permission` |
| 4 | 取得済み権限が足りなければ`approval_required`となり、callbackを一度も呼ばず、必要権限を一回の集合で返す | `test_missing_permission_stops_before_any_callback`、`test_empty_attestation_requests_every_permission_in_one_set` |
| 5 | 権限がそろうときだけcallbackを実行する。host入力はattestationであり、project内がsandbox権限を検査・付与したことにはしない | `test_execution_runs_only_when_attestation_covers_every_permission`、`test_host_attestation_is_an_input_not_a_permission_check` |
| 6 | `external`はattestationがあっても`external_operation_not_supported`で停止する | `test_external_operations_are_not_supported_by_this_runner` |
| 7 | receiptがinventoryとpreflight verdict／実行結果を結ぶ。identity不一致、preflight未通過、未知fieldを拒否する | `test_receipt_binds_inventory_and_preflight_identity`、`test_receipt_with_a_different_inventory_identity_is_rejected`、`test_receipt_without_a_granted_preflight_is_rejected` |
| 8 | `git add`／`git commit`相当は`git_metadata_write`、`git status`／`git diff --check`相当は`read_only`。moduleはGit commandを実行しない | `test_git_argv_fixtures_show_the_expected_classification` |
| 9 | project artifact writeとGit metadata writeが混在しても必要権限を最初に一回で返し、途中で追加要求しない | `test_mixed_write_kinds_are_requested_once_without_later_additions` |

受入条件5の「project内が権限を検査しない」ことは、moduleのsource textに
外部process起動やOS操作の語が現れないことをtestで機械確認している。報告文だけを根拠にしていない。

## 4. fault injection

停止条件ごとに、callbackの呼出し記録を独立に確認した。いずれもcallbackは**一度も呼ばれていない**。

| 注入した状態 | 停止code | callback呼出し |
| --- | --- | --- |
| 分類`unknown`を含むinventory | `unknown_classification_not_executable` | 0回 |
| 必要権限に対しattestationが空 | `approval_required`（必要権限を一回の集合で返す） | 0回 |
| `external`を含むinventory（attestationは充足） | `external_operation_not_supported` | 0回 |
| receiptを別inventoryへ照合 | `receipt_identity_mismatch` | 検証で追加呼出しなし |

## 5. host境界

- 承認と取得済み確認は**host側**に置く。project内は必要な権限種別を計算して出すだけである。
- `host attestation`はcallerが渡す入力である。moduleがOS、sandbox、Codex hostの権限を
  検査・付与・迂回することはない。
- Codex hostのJavaScript tool構文と外部toolのAPI schemaはproject内では解決できない。
  `HTC-A5D1BCCA`は解決済みとして扱わない。
- 必要な権限が未取得なら、最初の書込みを一度も試さず停止し、hostへ一回の要求を渡す。

## 6. 今回の対象外

次はこの作業単位に含めていない。

- shellを実行する汎用argv executor、`shell=True`相当、既存直接shell操作の置換
- cache rootの固定
- Gitへの実書込み、push、tag、外部送信、host／sandbox権限の取得・迂回・自動承認
- Codex hostのJavaScript tool構文、外部toolのAPI schemaへの対応
- `ISSUE-HTC-66C3E6CA`が扱うEvidence／TODOの定型欄生成
- V4 Issue recordのstate変更、正式製品schema／UI／automation、Task Contractの新規作成

`ISSUE-HTC-C9F6C917`のIssue recordは`registered`のままであり、file digestも変更していない。
V4 Issueの正式Plan化や実装一般が完了したわけではない。
