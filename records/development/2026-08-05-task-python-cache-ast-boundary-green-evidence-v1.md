# task Python cache AST境界検査 GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 改善候補：`records/development/2026-08-05-task-python-cache-ast-boundary-inspection-improvement-candidate-v1.md`
- RED Evidence：`records/development/2026-08-05-task-python-cache-ast-boundary-red-evidence-v1.md`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-task-python-cache-ast-boundary-check.md`

## 1. 直した誤検知

禁止操作を含まないことを確かめる受入検査は、禁止語をsource文字列から部分一致で探していた。
禁止語`environ`が、指示の求める正しい公開関数名`bytecode_environment`の中にも現れるため、
実装が何をしていても違反になった。その場では`os.environ`へ狭めてGREENにしたが、方式は同じで
再発防止になっていなかった。

今回、この検査を文字列一致からAST（抽象構文木。sourceを構文として解析した木）による
操作検査へ置き換えた。

## 2. 実装した検査器

`tools/development/python_ast_boundary_check.py`を新規作成した。公開APIは1つだけである。

```python
findings = inspect_python_source_boundaries(source_text)
```

結果は、検出した操作の正規化名を重複なくソートしたtupleである。行や列の位置は結果へ
持ち込まない。同じ操作が何度現れても1件になる。

### 2.1 検出する操作

| 正規化名 | 検出対象 |
| --- | --- |
| `os.environ` | 読取、subscript読取、subscript代入、`update()`などの接触すべて |
| `os.putenv` | 実行中processの環境書換え |
| `os.remove`／`os.rmdir`／`os.unlink` | fileとdirectoryの削除 |
| `shutil.rmtree` | 木ごとの削除 |
| `pathlib.Path.unlink` | `Path(...)`を作って削除methodを呼ぶ形 |
| `time.time` | 時間に基づく判断 |
| `datetime.datetime.now` | 同上 |

`time.time`と`datetime.datetime.now`は、時間ベースの保持・削除判断をこの最小moduleへ
入れないという境界の検査である。

### 2.2 誤検知を避ける仕組み

- 判定はASTのnodeに対して行う。docstringや識別子の中に同じ文字列が現れても、
  それは`ast.Name`でも`ast.Attribute`でもないため違反にならない。
  `bytecode_environment`という関数名と、`os.environ`という語を含むdocstringだけの
  sourceが違反ゼロになることをTestで固定した。
- 名前は必ずimport束縛から辿る。束縛を辿れない名前は`None`を返し、違反にしない。
  `time.sleep()`や`os.path.join()`は検出対象の正規化名にならないので違反にならない。

### 2.3 見逃しを減らす仕組み

import束縛を集めて別名を解決するため、次はいずれも同じ正規化名になる。

- `import os` → `os.environ`
- `import os as runtime_os` → `runtime_os.environ`も`os.environ`
- `from os import environ` → `environ`だけの記述も`os.environ`
- `from pathlib import Path as P` → `P(...).unlink()`も`pathlib.Path.unlink`
- `from datetime import datetime` → `datetime.now()`も`datetime.datetime.now`

参照そのものを違反とする。呼び出さずに受け渡すだけでも同じ能力を持つためである。

### 2.4 引き受けない範囲（設計上の境界）

import束縛から辿れる名前だけを解決する。次は扱わない。指示の「ASTに現れない動的実行や
importの一般解決を推測で追加しない」に従い、推測で広げていない。

- 一度変数へ入れ替えた後の値（例：`target = Path(x)`のあとの`target.unlink()`）。
- `getattr`や文字列からの動的な呼出し。
- 相対importと`*` import。

この境界は列挙対象の検出には影響しない。列挙された形はすべて検出できることをTestで固定した。

### 2.5 検査器そのものの性質

標準ライブラリ`ast`だけを使う決定的な解析である。検査器のsource自身をASTで解析し、
importしているtop-level moduleが`ast`だけであることをTestで確認している。
外部process、network、filesystemへの書込みの手段を持たない。
構文解析できないsourceは`PythonAstBoundaryError`（code `source_unparsable`）で止まり、
結果を返して続行しない。

## 3. 既存cache Testの置換

`tests/test_task_python_cache.py::test_module_has_no_deletion_or_retention_or_global_environment_change`
を、禁止語の文字列検索からこの検査器の呼出しへ置き換えた。

```python
assert boundary_check.inspect_python_source_boundaries(source) == ()
```

旧検査が持っていた「既存runner／executorへ接続しない」「外部processを起動しない」という
条件は、AST検査器の対象ではない。これを落とさないために、同じfileへ
`test_module_imports_no_runner_executor_or_external_process`を追加した。
`task_python_cache.py`のimport集合をASTで取り出し、
`{dataclasses, json, re, pathlib, tools.layout}`と完全一致することを確認する。
文字列検索より狭く、確実である。

`tools/development/task_python_cache.py`は**1文字も変更していない**（`git diff`で確認済み）。
振る舞いは変えていない。

## 4. RED→GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_python_ast_boundary_check.py` | `19 errors`（検査器module不在） | `19 passed` |
| `tests/test_task_python_cache.py` | — | `27 passed` |
| Layout関連2 fileを含む4 file合計 | — | `65 passed` |
| 公式policy runner suite `full` | `942 passed, 19 errors` | **`962 passed`** |

## 5. TODOの全Test表示

既存のTODO更新CLIを通して公式receiptから更新した。手入力していない。

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/2026-08-05-task-python-cache-ast-boundary-green-first-receipt-v1.json \
  --final-receipt records/development/2026-08-05-task-python-cache-ast-boundary-green-test-receipt-v1.json
```

| 段 | 集計 |
| --- | --- |
| first receipt | `{"errors": 0, "failed": 0, "passed": 962, "skipped": 0, "total": 962, "xfailed": 0, "xpassed": 0}` |
| final receipt | 同上（完全一致） |

```diff
-- 直近の全Test：venv公式runner `942 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `962 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

TODOの最新Evidenceには、旧cache GREEN Evidenceを残したまま今回のAST GREEN Evidenceを追加した。
size上限（12,288 bytes）に近づいたため、更新規則に従い、今回と無関係で上位Evidenceに
置換済みの参照だけを外した。外した参照と理由は次の節に記す。

## 6. TODOから外した参照と理由

| 外した参照 | 理由 |
| --- | --- |
| `records/development/2026-08-05-v4-issue-persistence-green-evidence-v1.md` | V4 Issue永続化はHuman承認のうえ検証を閉じている。現況の正本は`.reviewcompass/workflow/issues-v4/`のIssue record 3件で、それらはTODOに残っている |
| `records/development/2026-08-05-historical-todo-intake-candidates-v1.json` | 過去TODO候補41件は全件triage済みで未判断は0件である。判断結果の正本はV4 triage decisionとIssue recordで、Issue recordはTODOに残っている |

どちらも今回のAST修復とは無関係で、上位のEvidenceに置換済みの参照である。
今回の修復に関係する参照（cache承認Decision、cache GREEN Evidence、AST GREEN Evidence）は
すべて残している。件数は毎回機械計測し、TODOの記載を実値25件へ合わせた。

## 7. 対象外（変更していない）

- `tools/development/task_python_cache.py`、Layout v3、cache配置規則。
- 既存Decision、Issue state、Task Contract、policy、config。
- 実際の`~/.reviewcompass3`、`ReviewCompass3-data`、既存`DATA_ROOT`、`SENSITIVE_ROOT`。
  この作業で一切書いていない。
- cache初期化、掃除、保持期限の自動化、既存runner／executorへの接続、環境変数のglobal変更、
  Windows adapter、既存操作の移行、外部送信。

`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。新しい正式Issue、Plan、
Task Contract、policyは作っていない。
