# Claude → Codex：TODO二段更新の例外復元境界の修正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-todo-update-transaction-boundary.md`

RED/GREEN手順で修正した。**停止していない。TODOの全Test行は手入力していない。**

## commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 1 RED | `21cb2057ea106bc172b872e3e822ba77f1860774` | 失敗注入Test 6件、RED Evidence（実装変更なし） |
| 2 GREEN | `2af8b24cc16b0b3cba0412960957f7c1707b0905` | `todo_update_path.py`修正、GREEN Evidence、first／final receipt、CLI生成済みTODO |

各commitは明示pathだけをstageした。commit後の`git status --short`は空、
`work_unit_transition --work-status completed`は`next_work_allowed: true`。

## 修正前の再現

```text
raised: RuntimeError second run unavailable
calls: ['first', 'second']
todo_restored: False
```

`run_two_phase_update()`が`TodoUpdatePathError`だけを捕捉していたため、TODOは1回目receiptで
更新されたまま戻らず、呼出し元には素の`RuntimeError`が返っていた。

## 修正後の失敗注入結果（実測）

```text
2回目runner例外: TodoUpdatePathError code=official_test_failed calls=['first', 'second'] todo_restored=True
1回目runner例外: TodoUpdatePathError code=official_test_failed calls=['first']           todo_restored=True
validator想定外例外: TodoUpdatePathError code=todo_verification_failed                    todo_restored=True
KeyboardInterrupt: 捕捉せず伝播
```

1回目runner例外の`todo_restored=True`は「元bytesと一致」の意味で、この経路ではTODOへのwriteが
一度も起きていない（2回目を呼んでいない）。

CLI経由（最終receipt fileが読めない場合、2回目runnerが例外を送出する場合）は、停止JSONと
非0 exitを返し、tracebackを通常出力へ流さず、TODOを元bytesへ戻すことをTestで固定した。

## 実装した境界

- `_run_official_phase()`で公式Test実行・receipt取得の失敗を`official_test_failed`へ正規化。
- 1回目runnerは`try`の外。失敗しても復帰writeを行わない。
- 書き始めから確定までの区間に`except Exception`を追加し、原状復帰のうえ`todo_update_failed`で停止。
- `_restore()`は元bytesと同じなら書かない。戻せない場合は`todo_restore_failed`。成功時は元の失敗を隠さない。
- CLIは`load_config()`失敗を`config_load_failed`と非0 exitで返す。TODO更新は`run_two_phase_update()`だけを通る。

`except BaseException`は使っていない。二段比較、`default_verify()`、atomic write、
receiptの構造化集計は複製していない。

## RED／GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_todo_update_path.py` | `4 failed, 22 passed` | `26 passed` |
| `tests/test_todo_record_generation.py`と合計 | — | `40 passed` |
| 公式policy runner suite `full` | — | **`916 passed`** |

既存の不一致receipt、read-back破損、validator失敗のTestは緩めていない。

## CLIのfirst/final集計

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
| first | `{"errors": 0, "failed": 0, "passed": 916, "skipped": 0, "total": 916, "xfailed": 0, "xpassed": 0}` |
| final | 同上（完全一致） |

比較fieldは`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の
6件で、すべて一致した。

## TODO表示

機械が書き換えたのは1行だけである。

```diff
-- 直近の全Test：venv公式runner `910 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `916 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

自由文、Evidence linkのlabel・path・順序、関連Test行は変わっていない。

## 検査結果

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator | 合格（11,741 bytes） |
| Evidence節に限定したDigest照合 | 合格（26件） |
| TODO表示 vs first／final receiptの構造化集計 | 一致（916） |
| `git diff --check` | 各commitのstage前後で合格 |
| commit後のread-only照合 | working treeはclean |

## 報告すべき差異

`tools/development/todo_compaction.py`にはCLI入口が無く、
`python3 tools/development/todo_compaction.py TODO_NEXT_SESSION.md`は何も出力せず終了する。
検査は`validate_compacted_todo()`をprogram経由で呼んで実施した（合格）。CLI追加は今回の範囲外である。
前回の完了報告でも同じ差異を報告しており、状況は変わっていない。

## 対象外（変更していない）

- Evidence／Decision一般化、自由文・Evidence linkの自動生成。
- Issue state、Task Contract、policy、config、cache root、argv executor、移行inventory、外部操作。
- 既存recordの書換え。新しいDecisionも作っていない。
- Git操作、push、hook、watcher、schedulerの追加。
- `ISSUE-HTC-66C3E6CA`と`ISSUE-HTC-C9F6C917`は`registered`のままである。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
