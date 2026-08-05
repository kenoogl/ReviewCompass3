# task専用Python cache root RED Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 承認：`DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-task-python-cache-slice.md`

## 1. この段階で作っていないもの

実装moduleは作っていない。`tools/development/task_python_cache.py`は存在しない。
Testだけを追加した。既存codeも既存Testも変更していない。

## 2. 追加したTest

`tests/test_task_python_cache.py`を新規作成した。全26件（parametrizeを展開した数）で、
固定する内容は次である。

### 2.1 副作用なしの解決

| test | 固定する条件 |
| --- | --- |
| `test_resolution_is_deterministic_and_writes_nothing` | Layout v3、project manifestの固定`project_id`、runtime root、`development`、safeなtask IDから`<runtime_root>/projects/<project_id>/development/cache/python-bytecode/<task_id>`を決定的に解決する。2回解決しても同じ値で、runtime rootは作られない |
| `test_project_identity_comes_from_the_manifest` | `resolve_task_cache`は`project_id`引数を受け取らない。project IDはmanifestから読む |

### 2.2 明示初期化だけが作る

| test | 固定する条件 |
| --- | --- |
| `test_initialization_creates_only_the_cache_and_task_directory` | 初期化はLayout v3の`cache` rootとtask directoryだけを作る。`data`、`state`、`logs`、`evaluation`、`sensitive`、`config`は作らない |
| `test_initialization_is_repeatable` | 二度目の初期化でも同じpathを返し、既にある内容を壊さない |

### 2.3 環境値生成

| test | 固定する条件 |
| --- | --- |
| `test_environment_mapping_holds_only_the_bytecode_prefix` | `PYTHONPYCACHEPREFIX`だけを持つmappingを返す。値は解決済みtask directoryの絶対pathである |
| `test_environment_mapping_does_not_change_the_running_process` | mappingを作るだけでは実行中processの環境が一切変わらない |

### 2.4 安全境界

`Layout v3の初期化操作`（`initialize_project_runtime_layout`）を、呼ばれたら失敗する関数へ
差し替えたうえで、次を拒否することを確認する。いずれも初期化を一度も呼ばない。

- unsafeなtask ID：`""`、`"."`、`".."`、`"../escape"`、`"a/b"`、`"a\\b"`、`".hidden"`、`"task id"`
- unsafeなprofile：`""`、`"runtime "`、`"../development"`、`"staging"`
- 相対runtime root
- project内へ重なるruntime root
- symlinkになっているcache target（別directoryへ書き出さないことも確認する）
- cache path上に既にある通常file（fileのまま残ることも確認する）
- project manifestが無いproject root

### 2.5 保持境界（source inspection）

`test_module_has_no_deletion_or_retention_or_global_environment_change`は、moduleのsourceに
削除手段、時間ベースの判断、実行中processの環境書換え、既存runner／executorへの接続が
無いことを確認する。`cleanup`、`purge`、`evict`、`expire`という名前の公開関数も存在しない。

`test_module_reuses_the_approved_layout_resolver`は、Layout v3のresolverとinitializerを
再利用し、別のpath規則を作らないことを確認する。

### 2.6 実際のbytecode出力の隔離

`test_child_process_writes_bytecode_only_under_the_task_directory`は、一時directoryだけで
完結するprojectとruntime rootを作り、`PYTHONPYCACHEPREFIX`のmappingを明示的に子Python
processへ渡す。子processがmoduleを1つ取り込んだあと、次を機械確認する。

- project内に`__pycache__`が1つも作られない。
- task directory配下に`.pyc` fileが作られる。

## 3. 実ホーム配下を作っていないこと

Testはすべて`tmp_path`（pytestが用意する一時directory）配下だけを使う。
runtime rootは`<tmp_path>/runtime/.reviewcompass3`である。
実際の`~/.reviewcompass3`、`ReviewCompass3-data`、既存の`DATA_ROOT`、`SENSITIVE_ROOT`、
project内には一切書いていない。

## 4. RED実行結果

```text
.venv/bin/python3 -m pytest -q tests/test_task_python_cache.py
→ 26 errors

E   ModuleNotFoundError: No module named 'tools.development.task_python_cache'
```

公式全Testと合わせた状態。

```text
.venv/bin/python3 -m pytest -q
→ 916 passed, 26 errors
```

既存916件は影響を受けていない。26件はすべて実装module不在によるもので、
期待どおりの失敗である。
