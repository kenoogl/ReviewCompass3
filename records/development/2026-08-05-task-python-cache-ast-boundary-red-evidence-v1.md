# task Python cache AST境界検査 RED Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 改善候補：`records/development/2026-08-05-task-python-cache-ast-boundary-inspection-improvement-candidate-v1.md`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-task-python-cache-ast-boundary-check.md`

## 1. この段階で作っていないもの

検査器`tools/development/python_ast_boundary_check.py`は作っていない。
`tools/development/task_python_cache.py`も変更していない。Testだけを追加した。

## 2. 追加したTest

`tests/test_python_ast_boundary_check.py`を新規作成した。19件（parametrizeを展開した数）である。
期待する公開APIは次だけである。

```python
findings = inspect_python_source_boundaries(source_text)
```

### 2.1 誤検知しないこと

| test | 固定する条件 |
| --- | --- |
| `test_correct_identifier_is_not_a_violation` | `bytecode_environment`という正しい関数名と、`os.environ`という語を含むdocstringだけのsourceは違反ゼロである |
| `test_unrelated_names_and_attributes_are_not_violations` | `time.sleep()`と`os.path.join()`は違反にしない |

### 2.2 実行中processの環境

| test | 固定する条件 |
| --- | --- |
| `test_process_environment_access_is_detected` | `os.environ`の読取、subscript読取、subscript代入、`update()`のいずれも`os.environ`として検出する |
| `test_aliased_module_and_from_import_are_detected` | `import os as runtime_os`経由と`from os import environ`経由も検出する |

### 2.3 削除と環境書換えの呼出し

| test | 検出する操作 |
| --- | --- |
| `test_os_level_removal_calls_are_detected` | `os.putenv`、`os.remove`、`os.rmdir`、`os.unlink` |
| `test_tree_removal_call_is_detected` | `shutil.rmtree` |
| `test_path_removal_call_is_detected` | `Path(...).unlink()`と`from pathlib import Path as P`経由の`P(...).unlink()` |

### 2.4 時間ベースの判断

`test_time_based_calls_are_detected`は、`time.time()`、`datetime.datetime.now()`、
`from datetime import datetime`経由の`datetime.now()`を検出することを固定する。
時間ベースの保持・削除判断をこの最小moduleへ入れないための境界検査である。

### 2.5 結果の形と失敗の扱い

| test | 固定する条件 |
| --- | --- |
| `test_result_is_a_sorted_immutable_value_without_position` | 結果はtupleで、ソート済みで、行の順序や空行を変えても同じ値になる。位置情報を同一性へ持ち込まない |
| `test_repeated_operations_are_reported_once` | 同じ操作が複数回現れても1件にまとめる |
| `test_unparsable_source_raises_instead_of_returning` | 構文解析できないsourceは`PythonAstBoundaryError`（code `source_unparsable`）で止まる。結果を返して続行しない |

### 2.6 検査器そのものの性質と実対象

| test | 固定する条件 |
| --- | --- |
| `test_checker_uses_only_the_standard_ast_module` | 検査器のsourceをASTで解析し、import しているtop-level moduleが`ast`だけであることを確認する。外部process、network、filesystem書込みの手段を持たない |
| `test_current_task_python_cache_module_has_no_findings` | 現在の`tools/development/task_python_cache.py`は違反ゼロである |

## 3. RED実行結果

```text
.venv/bin/python3 -m pytest -q tests/test_python_ast_boundary_check.py
→ 19 errors

E   ModuleNotFoundError: No module named 'tools.development.python_ast_boundary_check'
```

公式全Testと合わせた状態。

```text
.venv/bin/python3 -m pytest -q
→ 942 passed, 19 errors
```

既存942件は影響を受けていない。19件はすべて検査器module不在によるもので、期待どおりの失敗である。

## 4. この段階で変更していないもの

- `tools/development/task_python_cache.py`と、その既存Test。
- Layout v3、cache配置規則、既存Decision、Issue state、Task Contract、policy、config。
- `TODO_NEXT_SESSION.md`。この作業単位では更新しない。
