# TODO二段更新の例外復元境界 GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-66C3E6CA`
- 承認：`DEC-RECORD-GENERATION-PLAN-001`（TODO最小縦切りの範囲内。新しいDecisionは作っていない）
- RED Evidence：`records/development/2026-08-05-todo-update-transaction-boundary-red-evidence-v1.md`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-todo-update-transaction-boundary.md`

## 1. 修正前に再現した不整合

```text
first receipt: 正常
TODO candidate write: 正常
second official test: RuntimeError("second run unavailable")

raised: RuntimeError second run unavailable
calls: ['first', 'second']
todo_restored: False
```

`run_two_phase_update()`が`TodoUpdatePathError`だけを捕捉していたため、2回目の公式Test実行が
通常の例外を送出するとTODOは1回目receiptで更新されたまま戻らず、呼出し元には素の`RuntimeError`が返っていた。

## 2. 実装した境界

`tools/development/todo_update_path.py`だけを変更した。

- `_run_official_phase()`を追加し、公式Test実行とreceipt取得に由来する失敗を
  `official_test_failed`へ正規化する。`TodoUpdatePathError`はそのまま通す。
- 1回目の公式Testは`try`の外で呼ぶ。この段階ではTODOを一度も書いていないので、
  復帰のためのwriteも行わない。
- 書き始めてから確定するまでの区間へ`except Exception`を追加し、想定外の失敗も
  原状復帰したうえで`todo_update_failed`で停止する。既存の`TodoUpdatePathError`経路は変えていない。
- `_restore()`は現bytesが元bytesと同じなら何も書かない。戻せない場合は`todo_restore_failed`で停止する。
  復元が成功した場合は`raise`で元の失敗をそのまま返し、隠さない。
- CLIは`load_config()`の失敗を`config_load_failed`と非0 exitで返す。TODO更新は
  引き続き`run_two_phase_update()`だけを通る。

`except BaseException`は使っていない。`KeyboardInterrupt`と`SystemExit`は`Exception`を継承しないため捕捉されない。
二段比較、`default_verify()`、atomic write、receiptの構造化集計は再実装していない。

## 3. 修正後の失敗注入結果（実測）

```text
2回目runner例外: TodoUpdatePathError code=official_test_failed calls=['first', 'second'] todo_restored=True
1回目runner例外: TodoUpdatePathError code=official_test_failed calls=['first']           todo_restored=True
validator想定外例外: TodoUpdatePathError code=todo_verification_failed                    todo_restored=True
KeyboardInterrupt: 捕捉せず伝播
```

1回目runner例外の`todo_restored=True`は「元bytesと一致」の意味であり、この経路ではTODOへのwriteが
一度も起きていない（`calls`が`first`だけで、2回目を呼んでいない）。

CLI経由は`tests/test_todo_update_path.py`で固定した。最終receipt fileが読めない場合も、
2回目runnerが例外を送出する場合も、停止JSONと非0 exitを返し、tracebackを通常出力へ流さず、
TODOは元bytesへ戻る。

## 4. RED→GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_todo_update_path.py` | `4 failed, 22 passed` | `26 passed` |
| `tests/test_todo_record_generation.py`と合計 | — | `40 passed` |
| 公式policy runner suite `full` | — | **`916 passed`** |

既存の不一致receipt、read-back破損、validator失敗のTestは緩めていない。

## 5. CLIの実行と実際の集計

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/2026-08-05-todo-update-transaction-boundary-first-receipt-v1.json \
  --final-receipt records/development/2026-08-05-todo-update-transaction-boundary-final-receipt-v1.json
```

出力は`{"status": "updated", ...}`、exit code `0`。

| 段 | 集計 |
| --- | --- |
| first receipt | `{"errors": 0, "failed": 0, "passed": 916, "skipped": 0, "total": 916, "xfailed": 0, "xpassed": 0}` |
| final receipt | 同上（完全一致） |

`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の6 fieldが一致した。

## 6. TODOの実際の変更範囲

機械が書き換えたのは1行だけである。

```diff
-- 直近の全Test：venv公式runner `910 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `916 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

値は1回目の公式receiptの構造化fieldから生成した。手入力していない。
自由文、Evidence linkのlabel・path・順序、関連Test行は変わっていない。

## 7. 独立照合

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator | 合格（11,741 bytes） |
| Evidence節に限定したDigest照合 | 合格（26件） |
| TODO表示 vs first receiptの構造化集計 | 一致（916） |
| TODO表示 vs final receiptの構造化集計 | 一致（916） |
| `git diff --check` | 合格 |

`tools/development/todo_compaction.py`にはCLI入口が無いため、compaction検査は
`validate_compacted_todo()`をprogram経由で呼んで実施した。CLI追加は今回の範囲外である。

## 8. 対象外（変更していない）

- Evidence／Decision一般化、自由文・Evidence linkの自動生成。
- Issue state、Task Contract、policy、config、cache root、argv executor、移行inventory、外部操作。
- 既存recordの書換え。新しいDecisionも作っていない。
- Git操作、push、hook、watcher、schedulerの追加。

`ISSUE-HTC-66C3E6CA`と`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。
