# operation routing v2 receipt整合性 訂正GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 訂正Decision：`DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`
  （`records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md`、
  SHA-256 `f73f06e12f464a27ded059522e37015acbd2f9487d7d65d55ed96823a6f8033b`）
- 元の承認Decision：`DEC-MACHINE-OPERATION-ROUTING-001`（変更していない）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-operation-routing-receipt-integrity.md`

## 1. REDで再現した改竄

修正前の実装は、Git metadataへの書込みを含むinventoryから作った**正当なreceipt**に対し、
receipt内のpreflight情報の`required_permissions`と`missing_permissions`を空へ書き換え、
Digestを計算し直すと**受理してしまった**。

RED実行：`.venv/bin/python3 -m pytest -q tests/test_operation_routing_v2.py` → **`6 failed, 17 passed`**

失敗した6件は次である。

| test | 固定した振る舞い |
| --- | --- |
| `test_receipt_with_emptied_preflight_requirements_is_rejected` | 必要権限を空へ改竄しDigestを合わせ直したreceiptを拒否する |
| `test_receipt_carries_a_complete_revalidatable_preflight` | receiptが完全なpreflight recordを持ち、inventoryに対して再検証できる |
| `test_standalone_preflight_with_wrong_requirements_is_rejected` | preflight単体の必要権限が食い違えば、自己Digestが正しくても拒否する |
| `test_standalone_preflight_with_inconsistent_missing_or_verdict_is_rejected` | 未取得集合とverdictの組合せが再計算値と違えば拒否する。語彙外の取得済み権限も拒否する |
| `test_receipt_schema_version_two_is_required` | receiptはschema version 2だけを受理し、version 1を拒否する |
| `test_receipt_binds_inventory_and_preflight_identity` | receiptのschema versionが2であること |

既存testは削除・弱化していない。receiptのschema versionを1から2へ上げる指示に伴い、
`test_receipt_binds_inventory_and_preflight_identity`の該当assertionだけを`1`から`2`へ更新した。
他のassertionは変更していない。

## 2. 修正内容

`tools/development/operation_routing.py`（SHA-256 `0fb5636feac3e12c42104830cd710bdb2a6f9398b784edf211c57128e1cd9178`）

1. `validate_permission_preflight(preflight, inventory=...)`がinventoryを再検証し、必要権限を
   `required_permissions(inventory)`で**再計算**するようにした。
2. `granted_permissions`をhost attestationの語彙として厳密に検証し、`missing_permissions`が
   「再計算した必要権限 − granted_permissions」と一致することを要求するようにした。
3. verdictは、missingが空なら`granted`、そうでなければ`approval_required`だけを受理する。
   自己Digestが正しくても意味が違えば拒否する。
4. execution receiptは抜粋ではなく、**完全な検証済みpreflight record**を保存する。
   receipt validatorはそれをinventoryに対して再検証し、`granted`でなければ拒否する。
5. receipt recordだけschema versionを**2**へ上げた。inventoryとpreflightは**1のまま**である。
   version 1のreceiptは`receipt_schema_version_unsupported`で明示的に拒否する。
6. receiptの`content_digest`、inventory identity、preflight identity、operation結果の順序・ID照合は
   従来どおり維持した。
7. 実行callbackは、`unknown`、`external`、権限不足、改竄preflightのいずれでも一度も呼ばれない。

新設した停止codeは`preflight_requirement_mismatch`と`preflight_verdict_mismatch`である。
どちらも`STOP_CODES`へ追加し、testで意味を固定した。

## 3. GREEN

| 対象 | 結果 |
| --- | --- |
| `.venv/bin/python3 -m pytest -q tests/test_operation_routing_v2.py` | `23 passed` |
| 公式全test（policy runner suite `full`） | `852 passed` |

公式全testのreceiptは
`records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-test-receipt-v1.json`
である。RED testだけのcommitは作っていない。実装中にtestの期待を緩めていない。

## 4. fault injection（改竄拒否とcallback 0回）

停止条件ごとに、callbackの呼出し記録を独立に確認した。

| 注入した状態 | 停止code | callback |
| --- | --- | --- |
| receiptのpreflight必要権限を空へ改竄し、preflightとreceiptのDigestを両方合わせ直す | `preflight_requirement_mismatch` | 検証で追加呼出しなし |
| preflight単体の必要権限を改竄し自己Digestを合わせ直す | `preflight_requirement_mismatch` | 呼出しなし |
| 分類`unknown`を含むinventory | `unknown_classification_not_executable` | **0回** |
| `external`を含むinventory（attestationは充足） | `external_operation_not_supported` | **0回** |
| 必要権限に対しattestationが空 | `approval_required` | **0回** |

呼出し回数は、callbackの呼出しを記録する独立のrecorderで数えた。報告文だけを根拠にしていない。

## 5. receipt schema v2

- execution receiptの`schema_version`は**2**である。
- operation inventoryの`schema_version`は**1のまま**である。
- permission preflightの`schema_version`も**1のまま**である。
- version 1のexecution receiptは受理しない。抜粋しか持たず改竄を検出できないためである。

## 6. 既存v1 Evidenceのstale化

次の二つは削除も書換えもしていない。承認対象の実装結果を記録した履歴として残す。
ただしreceipt validatorの欠陥が判明した時点で**stale**であり、§3最小縦切りの有効な完了根拠ではない。

| stale化した記録 | SHA-256 |
| --- | --- |
| `records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md` | `e4f8d9f865e6b6d35e7d00a21eba54c13b1ed331fca3183827b1262d285d88eb` |
| `records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json` | `b6f55b5c7096b19106656403d9a7ad975f79debff61767827ac425be111d018a` |

有効な完了根拠は、訂正Decisionと本Evidenceである。
`DEC-MACHINE-OPERATION-ROUTING-001`はHumanの承認事実として有効なままである。

## 7. 非対象

Git、shell、外部processの起動、外部送信、host／sandbox権限の取得・迂回・自動承認、cache root固定、
構造化argv executor、既存直接shell操作の置換、Codex hostのJavaScript tool構文、外部toolのAPI schema、
V4 Issue recordのstate変更、Task Contractの新規作成、policy runnerの変更は行っていない。

`ISSUE-HTC-C9F6C917`は`registered`のままで、C9全体をclosedにしていない。
後続のargv executor、cache root、既存操作移行は未実施である。
