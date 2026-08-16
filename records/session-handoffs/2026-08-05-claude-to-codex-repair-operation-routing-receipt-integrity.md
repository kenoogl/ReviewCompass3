# Claude → Codex：operation routing v2 receipt整合性の修正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-operation-routing-receipt-integrity.md`

TDDで改竄を再現し、validatorを修正し、訂正Decision／Evidence／receiptを作って一つのGREEN意味単位commitにした。

## commit

- commit SHA：`32d33fc8741fbcd2c19ceb650800d460db61bca0`
- message：`Verify operation routing receipt integrity`
- stageは今回作成・更新した9 pathだけを明示列挙した。`git add -A`と`git add .`は使っていない。
- commit後のread-only確認：`git status --short`は空。
  `python3 tools/development/work_unit_transition.py --work-status completed`は
  `{"findings": [], "next_work_allowed": true, "reminder": null, "status": "passed"}`

## RED／GREEN

| 段階 | 実行 | 結果 |
| --- | --- | --- |
| RED | `.venv/bin/python3 -m pytest -q tests/test_operation_routing_v2.py` | **`6 failed, 17 passed`** |
| GREEN（対象test） | 同上 | **`23 passed`** |
| GREEN（公式全test） | policy runner suite `full` | **`852 passed`**（exit 0） |

RED testだけのcommitは作っていない。実装中にtestの期待を緩めていない。
既存testは削除・弱化していない。receiptのschema versionを2へ上げる指示に伴い、
`test_receipt_binds_inventory_and_preflight_identity`の該当assertionだけを`1`から`2`へ更新した。
それ以外の既存assertionは変更していない。

## 改竄の再現と拒否

修正前は、Git metadataへの書込みを含むinventoryから作った**正当なreceipt**に対して、
receipt内のpreflight情報の`required_permissions`と`missing_permissions`を空へ書き換え、
preflightとreceiptのDigestを両方合わせ直すと、**validatorが受理してしまった**。

修正後は同じ改竄を`preflight_requirement_mismatch`で拒否する。原因への対処は次のとおりである。

1. `validate_permission_preflight()`がinventoryを再検証し、必要権限を`required_permissions(inventory)`で
   **再計算**する。申告値をそのまま信じない。
2. `granted_permissions`をhost attestationの語彙として厳密に検証し、`missing_permissions`が
   「再計算した必要権限 − granted_permissions」と一致することを要求する。
3. verdictは、missingが空なら`granted`、そうでなければ`approval_required`だけを受理する。
   自己Digestが正しくても意味が違えば拒否する（`preflight_verdict_mismatch`）。
4. execution receiptは抜粋ではなく、**完全な検証済みpreflight record**を保存する。
   receipt validatorはそれをinventoryに対して再検証し、`granted`でなければ拒否する。

新設した停止codeは`preflight_requirement_mismatch`と`preflight_verdict_mismatch`である。
どちらも`STOP_CODES`へ追加し、testで意味を固定した。

## fault injection（callback 0回の証拠）

callbackの呼出しを記録する独立のrecorderで数えた。報告文だけを根拠にしていない。

| 注入した状態 | 停止code | callback |
| --- | --- | --- |
| receiptのpreflight必要権限を空へ改竄し、両方のDigestを合わせ直す | `preflight_requirement_mismatch` | 検証で追加呼出しなし |
| preflight単体の必要権限を改竄し自己Digestを合わせ直す | `preflight_requirement_mismatch` | 呼出しなし |
| 分類`unknown`を含むinventory | `unknown_classification_not_executable` | **0回** |
| `external`を含むinventory（attestationは充足） | `external_operation_not_supported` | **0回** |
| 必要権限に対しattestationが空 | `approval_required` | **0回** |

test側でも`test_no_callback_runs_for_any_stop_condition`として、unknown・external・権限不足の3条件を
同一recorderで通し、最後に`recorder.calls == []`を固定している。

## schema v2

- execution receiptの`schema_version`は**2**である。version 1のreceiptは
  `receipt_schema_version_unsupported`で明示的に拒否する。
- operation inventoryの`schema_version`は**1のまま**である。
- permission preflightの`schema_version`も**1のまま**である。

## stale化したv1 Evidence

次の2件は削除も書換えもしていない。承認対象の実装結果を記録した履歴として残す。
ただしvalidatorの欠陥が判明した時点で**stale**であり、§3最小縦切りの有効な完了根拠ではない。

| 記録 | SHA-256（作業前後で不変） |
| --- | --- |
| `records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md` | `e4f8d9f865e6b6d35e7d00a21eba54c13b1ed331fca3183827b1262d285d88eb` |
| `records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json` | `b6f55b5c7096b19106656403d9a7ad975f79debff61767827ac425be111d018a` |

既存の`DEC-MACHINE-OPERATION-ROUTING-001`
（SHA-256 `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969`）は、
Humanが§3を承認したという事実の記録として**変更していない**。

## 作成した訂正記録

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 訂正Decision `DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001` | `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md` | `f73f06e12f464a27ded059522e37015acbd2f9487d7d65d55ed96823a6f8033b` |
| 訂正GREEN Evidence | `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md` | `b6255b0a7de3bcd90b62745ff934a957dba94b3870bc847517f1dbde36a430ea` |
| 公式全test receipt | `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-test-receipt-v1.json` | `9be48428226a5c7d3e302b0ef68d8941cd21974a211892c66a7d8f3eaf8472bf` |

v2提案には短い実施注記を追記し、§3の実装がreceipt schema v2で改竄検出を含むこと、有効な完了根拠が
訂正側であること、初回GREEN Evidenceがstaleであることを記した。提案時点の本文は改竄していない。

Current Plan、checklist、TODOも更新し、前のGREEN Evidenceを唯一の完了根拠として残さず、
訂正Decision／訂正GREEN Evidenceへ接続した。C9全体はclosedと書いていない。
TODO validatorは更新後と最終stage前の2回とも`{"findings": [], "status": "passed"}`である。
`git diff --check`もstage前後で合格した。

## 非対象（変更していないもの）

- Git、shell、外部processの起動、外部送信：していない。
- host／sandbox権限の取得・迂回・自動承認：していない。承認と取得済み確認はhost側のままである。
- cache root固定、構造化argv executor、既存直接shell操作の置換：していない。
- Codex hostのJavaScript tool構文、外部toolのAPI schemaへの対応：していない。
- operation inventoryのschema version：1のまま変更していない。
- V4 Issue recordのstate：`ISSUE-HTC-C9F6C917`は`registered`のままで、file SHA-256も
  `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`で不変である。
- Task Contractの新規作成、policy runnerの変更：していない。
- push、tag、amend、rebase、reset、force push、外部送信：行っていない。
- 後続のargv executor、cache root、既存操作移行は未実施のままである。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
