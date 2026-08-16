# Claude → Codex：TODO全Test表示を機械更新するCLIの修正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-todo-test-projection-cli.md`

TDDでCLIを追加し、そのCLIでroot TODOの全Test表示を更新した。**手入力はしていない。停止もしていない。**

## commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 1 RED | `91bba4737c644c796511031cc60183dd79059ca2` | CLI受入test、RED Evidence（実装なし） |
| 2 GREEN | `d8e4a9303581b91ee80f3643253ab45ca3aac160` | CLI実装、test、GREEN Evidence、first／final receipt、TODO更新 |

各commitは明示pathだけをstageした。commit後の`git status --short`は空、
`work_unit_transition --work-status completed`は`next_work_allowed: true`。

## RED／GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_todo_update_path.py` | `4 failed, 16 passed`（`main`不在） | `20 passed` |
| `tests/test_todo_record_generation.py`と合わせて | — | `34 passed` |
| 公式policy runner suite `full` | — | **`910 passed`** |

## CLIの実行と実際の集計

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/2026-08-05-todo-test-projection-correction-first-receipt-v1.json \
  --final-receipt records/development/2026-08-05-todo-test-projection-correction-final-receipt-v1.json
```

出力は`{"status": "updated", ...}`、exit code `0`。

| 段 | 集計 |
| --- | --- |
| first receipt | `{"errors": 0, "failed": 0, "passed": 910, "skipped": 0, "total": 910, "xfailed": 0, "xpassed": 0}` |
| final receipt | 同上（完全一致） |

比較fieldは`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の
6件で、すべて一致した。

## TODO表示

機械が書き換えたのは1行だけである。

```diff
-- 直近の全Test：venv公式runner `892 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `910 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

値は1回目の公式receiptの構造化fieldから生成した。事前に想定していない。
発端は「receiptが905、TODOが892」という食い違いだったが、CLIが得た実値は**910**である。
今回追加したtestの分だけ増えており、この数値もCLIが決めたものである。

自由文、Evidence linkのlabel・path・順序、関連Test行は変わっていない。
Evidence Digestはbytesから再計算され、記録済みの値と一致した。

## 検査結果

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator | 合格（11,741 bytes、active ID 1件） |
| Evidence節に限定したDigest照合 | 合格（26件） |
| TODO表示 vs final receiptの構造化集計 | 一致（910） |
| TODO表示 vs first receiptの構造化集計 | 一致（910） |
| `git diff --check` | 各commitのstage前後で合格 |

## CLIの性質（testで固定）

- pathはproject root基準の相対だけ。絶対path、`..`、symlink、`records/development/`外、`.json`以外、
  同一pathの2回指定を拒否し、公式APIを一度も呼ばず、TODOもreceiptも作らない。
- `policy_test_runner.load_config()`と`execute()`を再利用し、既存`run_two_phase_update()`へ渡す。
  二段更新のlogicを複製していない。
- TODO本文を直接編集しない。更新は`run_two_phase_update()`だけを通る。
- Gitを呼ばない。`subprocess`、`"git"`、shell解釈の手段がmoduleに無いことをtestで確認している。
- 2回の集計が食い違えばTODOを元bytesへ戻して停止する。
- receiptの`stdout`に集計と食い違う数値を入れたfixtureで、出力文字列を読まないことを固定している。

## 報告すべき差異

`tools/development/todo_compaction.py`には**CLI入口が無い**。指示書の検証手順にある
`python3 tools/development/todo_compaction.py TODO_NEXT_SESSION.md`は、何も出力せずexit 0で終わる。
compaction検査は`validate_compacted_todo()`をprogram経由で呼んで実施した（合格）。
`todo_compaction.py`へのCLI追加は今回の固定範囲外のため行っていない。必要であればご指示いただきたい。

## 対象外（変更していない）

- Evidence／Decision一般のrenderer、TODO自由文・link label・path・順序の自動決定。
- Issue state、Task Contract、policy、config、cache root、argv executor、既存操作の移行、外部操作。
- 既存recordの書換え、新しいDecisionの作成。
- CLIへのGit操作、push、外部送信、hook、watcher、schedulerの追加。
- `ISSUE-HTC-66C3E6CA`と`ISSUE-HTC-C9F6C917`は`registered`のままである。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
