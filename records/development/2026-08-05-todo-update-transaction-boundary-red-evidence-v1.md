# TODO二段更新の例外復元境界 RED Evidence v1

- 対象Issue：`ISSUE-HTC-66C3E6CA`
- 承認：`DEC-RECORD-GENERATION-PLAN-001`（TODO最小縦切りの範囲内。新しいDecisionは作らない）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-todo-update-transaction-boundary.md`

## 1. 独立再現（修正前）

`tools/development/todo_update_path.py`は「どこかで失敗したらTODOを更新前のbytesへ戻す」と仕様化して
いるが、`run_two_phase_update()`は`TodoUpdatePathError`だけを捕捉していた。

再現手順と実測結果。

```text
first receipt: 正常
TODO candidate write: 正常
second official test: RuntimeError("second run unavailable")
```

```text
raised: RuntimeError second run unavailable
calls: ['first', 'second']
todo_restored: False
更新後のTODO行: - 直近の全Test：venv公式runner `7 passed`、…
```

2回目の公式Test実行が通常の例外を送出すると、TODOは1回目receiptで更新されたまま**戻らない**。
呼出し元へ返るのも`TodoUpdatePathError`ではなく素の`RuntimeError`である。

これは局所的な例外処理の不足ではなく、二段更新を「最終確認まで原状復帰可能なtransaction」として
境界定義・受入Testへ落とし切れていなかった設計不足である。

## 2. 追加したTest（実装は変更していない）

`tests/test_todo_update_path.py`へ6件追加した。既存の不一致receipt、read-back破損、
validator失敗のtestは緩めていない。

| test | 固定する条件 |
| --- | --- |
| `test_second_run_exception_restores_the_todo` | 2回目runnerが`RuntimeError`を送出しても、TODOは元bytesへ戻る。呼出し順は`first, second`。呼出し元には`TodoUpdatePathError`が返り、codeは`STOP_CODES`にある |
| `test_first_run_exception_never_touches_the_todo` | 1回目runnerが失敗したらTODOを一度も変更せず、2回目を呼ばず、`TodoUpdatePathError`が返る |
| `test_unexpected_exception_inside_the_update_restores_the_todo` | validatorが`ValueError`を送出してもTODOは元bytesへ戻る |
| `test_keyboard_interrupt_is_not_swallowed` | `KeyboardInterrupt`は捕捉せずそのまま伝わる。sourceに`except BaseException`が無い |
| `test_unreadable_final_receipt_restores_the_todo` | 公式APIがreceipt pathを返すのにfileが無い場合、CLIは停止JSONと非0を返し、TODOは元bytesへ戻る |
| `test_cli_reports_a_second_run_exception_as_a_stop` | CLI経由で2回目runnerが例外を送出しても、停止JSONと非0を返し、tracebackを通常出力へ流さず、TODOは元bytesへ戻る |

## 3. RED実行結果

```text
.venv/bin/python3 -m pytest -q tests/test_todo_update_path.py
→ 4 failed, 22 passed
```

失敗した4件は、2回目runner例外、1回目runner例外、最終receipt読取失敗、CLI経由の2回目runner例外である。
`test_unexpected_exception_inside_the_update_restores_the_todo`と
`test_keyboard_interrupt_is_not_swallowed`は現状でも通る（前者は既存の`except Exception`が
`todo_verification_failed`へ正規化していたため、後者は`except BaseException`が無いため）。
これらは回帰を防ぐために残す。

## 4. この段階で作っていないもの

- 実装の変更。`tools/development/todo_update_path.py`は触っていない。
- TODOの更新。全Test行は`910 passed`のままである。
- Evidence／Decisionの一般化、自由文・Evidence linkの自動生成。
- Issue state、Task Contract、policy、config、cache root、argv executor、移行inventory、外部操作。

`ISSUE-HTC-66C3E6CA`のstateは`registered`のままである。
