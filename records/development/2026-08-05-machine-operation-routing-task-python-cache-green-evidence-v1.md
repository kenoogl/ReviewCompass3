# task専用Python cache root GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 承認：`DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001`
- RED Evidence：`records/development/2026-08-05-machine-operation-routing-task-python-cache-red-evidence-v1.md`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-task-python-cache-slice.md`

## 1. 実装したもの

`tools/development/task_python_cache.py`を新規作成した。責任は3つだけである。

| API | 性質 | 内容 |
| --- | --- | --- |
| `resolve_task_cache()` | read-only | `<runtime_root>/projects/<project_id>/development/cache/python-bytecode/<task_id>`を決める。directoryを一切作らない |
| `initialize_task_cache()` | 明示的な作成 | Layout v3の`cache` rootとtask directoryだけを作る |
| `bytecode_environment()` | 生成のみ | `PYTHONPYCACHEPREFIX`だけを持つmappingを返す。実行中processの環境を変えない |

- 配置規則は新しく作らず、`tools.layout.baseline`の`resolve_project_runtime_layout()`と
  `initialize_project_runtime_layout()`をそのまま使う。Layout v3の正本recordはproject内の
  `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`から読む。
- project IDは`.reviewcompass/project-manifest.json`からだけ読む。`resolve_task_cache()`は
  `project_id`引数を持たないので、callerが別projectのcacheへ書くことはできない。
- profileは`development`だけを受け付ける。承認範囲がそこだけだからである。
- 作る前に、runtime rootからtask directoryまでの経路にsymlinkとdirectoryでない通常fileが
  無いことを確認する。1つでもあれば、Layout v3の初期化を**一度も呼ばずに**停止する。
- 削除、保持期限の自動判断、既存runnerやexecutorへの接続、実行中processの環境書換えは
  実装していない。

## 2. RED→GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_task_python_cache.py` | `26 errors`（実装module不在） | `26 passed` |
| Layout v3 Test `tests/test_project_runtime_layout.py` | — | 合格 |
| `tests/test_layout_baseline.py`と合わせた3 file | — | `45 passed` |
| 公式policy runner suite `full` | `916 passed, 26 errors` | **`942 passed`** |

## 3. RED Testに1点だけ訂正を入れた

保持境界のsource inspectionで、禁止語に`environ`を挙げていた。これは指示が求める公開API名
`bytecode_environment`自身に含まれてしまい、実装が何をしていても必ず失敗する条件だった。
意図（実行中processの環境を書き換えない）を正しく表す`os.environ`へ直した。
`putenv`、削除手段、時間ベースの判断、既存runnerへの接続の禁止はそのまま残している。
他のTestは緩めていない。

## 4. 実際に作った一時directoryの範囲

Testはすべて`tmp_path`（pytestが用意する一時directory）配下だけを使う。

- fake project：`<tmp_path>/checkout/`（Project Manifestとv3正本recordの複製だけを置く）
- runtime root：`<tmp_path>/runtime/.reviewcompass3/`
- 作られるのは`projects/<project_id>/development/cache/`と
  その下の`python-bytecode/<task_id>/`だけである。

初期化のTestで、同じprofile配下の`data`、`state`、`logs`、`evaluation`、`sensitive`と
runtime root直下の`config`が作られないことを機械確認している。

## 5. bytecode隔離の実測

一時project配下に`sample_module.py`を置き、`bytecode_environment()`が返したmappingを
明示的に子Python processへ渡して取り込ませた。

| 確認項目 | 結果 |
| --- | --- |
| 子processの終了code | `0`（標準出力は`1`） |
| project内の`__pycache__` | `0`件 |
| task directory配下の`.pyc` | 1件以上あり |

`PYTHONPYCACHEPREFIX`を渡すだけで、bytecodeの出力先がtask directory配下へ移ることを
実際の子processで確認した。想定ではなく実測である。

## 6. 実ホーム配下を作っていないこと

実際の`~/.reviewcompass3`は2026-08-04のWork 4Aで既に存在しており、中身は
`projects/reviewcompass3/development/data/work4a/`だけである。
この作業の前後で確認した結果は次である。

- `cache`という名前のdirectoryは1つも無い。
- `python-bytecode`という名前のdirectoryは1つも無い。
- 本session（21:00以降）に更新されたfileは1件も無い。

`ReviewCompass3-data`、既存の`DATA_ROOT`、`SENSITIVE_ROOT`、project内にも書いていない。

## 7. TODOの全Test表示

既存のTODO更新CLIを通して公式receiptから更新した。手入力していない。

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/2026-08-05-machine-operation-routing-task-python-cache-green-first-receipt-v1.json \
  --final-receipt records/development/2026-08-05-machine-operation-routing-task-python-cache-green-test-receipt-v1.json
```

| 段 | 集計 |
| --- | --- |
| first receipt | `{"errors": 0, "failed": 0, "passed": 942, "skipped": 0, "total": 942, "xfailed": 0, "xpassed": 0}` |
| final receipt | 同上（完全一致） |

```diff
-- 直近の全Test：venv公式runner `916 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `942 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

## 8. 対象外（実装していない）

- 実際のホーム配下の初期化、既存processへの自動適用。
- `policy_test_runner`、`structured_argv_executor`、既存call siteへの接続。
- 掃除・保持期限の自動化、時間ベースの削除、global cacheの書換え。
- 実行中processの環境変数の変更。
- Windows adapter、既存操作の移行、移行inventoryの作成。
- Git metadata書込み、project成果物書込み、external操作、host側tool構文、外部送信。
- Issue state、Task Contract、policy、config、既存Decisionの変更。

`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。
