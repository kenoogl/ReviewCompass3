# TODO全Test表示 機械更新CLI GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-66C3E6CA`
- 承認：`DEC-RECORD-GENERATION-PLAN-001`（TODO最小縦切りの範囲内。新しいDecisionは作っていない）
- RED Evidence：`records/development/2026-08-05-todo-test-projection-cli-red-evidence-v1.md`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-todo-test-projection-cli.md`

## 1. 直した不一致

作業開始時点で、次の食い違いがあった。

| 対象 | 値 |
| --- | --- |
| 読み取り専用argv executorのGREEN receipt | `passed 905／total 905` |
| `TODO_NEXT_SESSION.md`の`## Git・Test`節 | `892 passed` |

Testもexecutorも失敗していない。原因は、二段更新経路（`run_two_phase_update()`）を呼ばずに
TODO本文を直接更新したことである。数値を手で直すのではなく、その経路を機械処理として起動できる
CLIを追加し、CLIで修正した。

## 2. 実装したCLI

`tools/development/todo_update_path.py`へ追加した。

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/<first>.json \
  --final-receipt records/development/<final>.json
```

- `--todo`、`--first-receipt`、`--final-receipt`は必須である。
- pathはproject root基準の相対だけを受ける。絶対path、`..`、symlinkを拒否する。
  receiptは`records/development/`直下の`.json`だけを許し、同じpathを2回指定することも拒否する。
  pathが不正なら公式APIを一度も呼ばず、TODOもreceiptも作らない。
- `policy_test_runner.load_config()`と`policy_test_runner.execute()`を再利用し、既存の
  `run_two_phase_update()`へ渡す。二段更新のlogicを複製していない。
- CLIはTODO本文を直接編集しない。更新は`run_two_phase_update()`だけを通る。
- Gitを呼ばない。commitもpushもしない。moduleに`subprocess`、`"git"`、shell解釈の手段が
  無いことをtestで確認している。
- 出力はJSONで、`status`、`first_receipt`、`final_receipt`、`test_summary`を持つ。

## 3. RED→GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_todo_update_path.py` | `4 failed, 16 passed`（`main`不在） | `20 passed` |
| `tests/test_todo_record_generation.py` | — | `14 passed`（2 file合計`34 passed`） |
| 公式policy runner suite `full` | — | `910 passed` |

## 4. CLIの実行結果（実修正）

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/2026-08-05-todo-test-projection-correction-first-receipt-v1.json \
  --final-receipt records/development/2026-08-05-todo-test-projection-correction-final-receipt-v1.json
```

出力（JSON）。

```json
{"final_receipt": "records/development/2026-08-05-todo-test-projection-correction-final-receipt-v1.json",
 "first_receipt": "records/development/2026-08-05-todo-test-projection-correction-first-receipt-v1.json",
 "status": "updated",
 "test_summary": {"errors": 0, "failed": 0, "passed": 910, "skipped": 0, "total": 910,
                  "xfailed": 0, "xpassed": 0}}
```

exit code は`0`。

| 段 | receipt | 集計 |
| --- | --- | --- |
| first | `records/development/2026-08-05-todo-test-projection-correction-first-receipt-v1.json` | `passed 910／total 910` |
| final | `records/development/2026-08-05-todo-test-projection-correction-final-receipt-v1.json` | `passed 910／total 910` |

`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の6 fieldが
一致したことを独立に照合した。

## 5. TODOの実際の変更範囲

機械が書き換えたのは**1行だけ**である。

```diff
-- 直近の全Test：venv公式runner `892 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `910 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

- 全Test行は**1回目の公式receiptの構造化fieldからだけ**生成した。値を事前に想定・手記入していない。
  実行前は`905`との差だけを問題にしていたが、CLIが得た実値は`910`である（この作業で追加したtestの分だけ
  増えている）。この数値もCLIが決めたものであり、こちらで指定していない。
- 自由文、Evidence linkのlabel・path・順序、関連Test行は変わっていない。
- 既存のEvidence Digestはbytesから再計算され、記録済みの値と一致した。
- stdoutの文字列は読んでいない。testでは、receiptの`stdout`に集計と食い違う数値（`999 passed`）を
  入れ、それが本文へ現れないことを確認している。

## 6. 独立照合

| 検証 | 結果 |
| --- | --- |
| TODO表示 == final receiptの構造化集計 | 一致（910） |
| TODO表示 == first receiptの構造化集計 | 一致（910） |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator | 合格 |
| Evidence節に限定したDigest照合 | 一致 |

なお`tools/development/todo_compaction.py`にはCLI入口が無く、
`python3 tools/development/todo_compaction.py TODO_NEXT_SESSION.md`は何も出力せず終了する。
検証は`validate_compacted_todo()`をprogram経由で呼んで行った。CLIの追加は今回の範囲外である。

## 7. 対象外（変更していない）

- Evidence／Decision一般のrenderer、TODO自由文・Evidence link label・path・順序の自動決定。
- Issue state、Task Contract、policy、config、cache root、argv executor、既存操作の移行、外部操作。
- 既存recordの書換え。新しいDecisionも作っていない。
- CLIにGit操作、push、hook、watcher、schedulerを追加していない。

`ISSUE-HTC-66C3E6CA`と`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。
