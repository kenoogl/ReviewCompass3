# TODO全Test表示 機械更新CLI RED Evidence v1

- 対象Issue：`ISSUE-HTC-66C3E6CA`
- 承認：`DEC-RECORD-GENERATION-PLAN-001`（TODO最小縦切りの範囲内。新しいDecisionは作らない）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-todo-test-projection-cli.md`

## 1. 直した問題

読み取り専用argv executorのGREEN receipt
`records/development/2026-08-05-machine-operation-routing-read-only-argv-green-test-receipt-v1.json`は
`passed 905／total 905`である。

一方、`TODO_NEXT_SESSION.md`の`## Git・Test`節は`892 passed`のままだった（作業開始時に確認）。

原因はTestやexecutorの失敗ではない。`tools/development/todo_record_generation.py`と
`tools/development/todo_update_path.py`に公式receiptの構造化`test_summary`から全Test行を更新する
機能があるのに、前作業でその二段更新経路を**呼ばず**、TODO本文を直接更新したことである。

数値を手で直さない。既存の`run_two_phase_update()`を機械処理として起動できるCLIを追加し、
そのCLIで修正する。

## 2. 追加したTest（実装は書いていない）

`tests/test_todo_update_path.py`へCLIの受入testを4件追加した。既存testは変更していない。

| test | 固定する条件 |
| --- | --- |
| `test_cli_updates_the_full_test_line_from_the_first_receipt` | 公式APIを2回呼び、1回目でfirst receipt、2回目でfinal receiptを作る。全Test行は**1回目のreceiptの構造化field**から作られる。receiptの`stdout`にはわざと食い違う数値（`999 passed`）を入れ、それが本文へ現れないことを確かめる。自由文、link label／path、関連Test行は不変。出力はJSONでstatus、両receipt path、集計を持つ |
| `test_cli_requires_every_path_argument` | `--todo`、`--first-receipt`、`--final-receipt`のいずれが欠けても停止する |
| `test_cli_rejects_unsafe_paths_without_touching_anything` | 絶対path、`..`、`records/development/`外、`.json`以外のreceipt pathを`receipt_path_invalid`で拒否する。TODOの絶対path、`..`、symlinkを`todo_path_invalid`で拒否する。いずれも公式APIを一度も呼ばず、TODOもreceiptも作らない |
| `test_cli_restores_the_todo_when_the_two_runs_disagree` | 2回の集計が食い違えば`receipt_summary_mismatch`で停止し、TODOを元bytesへ戻す |
| `test_cli_never_calls_git`（既存の趣旨を拡張） | moduleに`subprocess`、`"git"`、`os.system`、shell解釈optionの手段が無い |

testは公式Testを実際には走らせない。`policy_test_runner.execute`相当をfakeへ差し替え、
呼出し回数、suite、receipt pathを記録して観測する。

## 3. RED実行結果

```text
.venv/bin/python3 -m pytest -q tests/test_todo_update_path.py
→ 4 failed, 16 passed
```

失敗はいずれも`AttributeError: module 'tools.development.todo_update_path' has no attribute 'main'`
に由来する。CLIは未実装である。

## 4. この段階で作っていないもの

- CLIの実装。
- TODO本文の変更。全Test行は`892 passed`のままである。
- Evidence／Decisionの一般化、自由文・link label・path・順序の自動生成。
- Issue state、Task Contract、policy、config、cache root、argv executor、既存操作の移行。

`ISSUE-HTC-66C3E6CA`と`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。
