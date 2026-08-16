# Claude → Codex：task Python cacheのAST境界検査 修復 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-task-python-cache-ast-boundary-check.md`

指示の3作業単位をすべて実施した。**停止していない。**

## commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 1 改善候補 | `eb02a04939bc3c985f5a28d671366ddd2c03418e` | 候補recordだけ（code、test、TODOは変更しない） |
| 2 RED | `a386d7a50cd79689670fa8e01a27aafabc66e6d6` | `tests/test_python_ast_boundary_check.py`、RED Evidence（検査器なし） |
| 3 GREEN | `9ebefba1e332f5bb8623cebf36dd96e82ea5ef9d` | 検査器、置換後Test、GREEN Evidence、first／final receipt、CLI更新済みTODO |

各commitは明示pathだけをstageした。commit後の`git status --short`は空、
`work_unit_transition --work-status completed`は3回とも`next_work_allowed: true`。

## 候補record

`records/development/2026-08-05-task-python-cache-ast-boundary-inspection-improvement-candidate-v1.md`

`candidate_kind: improvement_candidate`、分類`Test／oracle不良`、優先度`P1`、
状態`adopted_for_next_slice`、route は既存`ISSUE-HTC-C9F6C917`への紐付けである。
発生元は`c9587dbf6135524f4abdee4cd8e02cf16319088d`と、cache GREEN Evidenceの
「3. RED Testに1点だけ訂正を入れた」節を対応付けて記載した。
実ホーム初期化などの未承認範囲を許可しないことも明記している。

## RED結果

```text
.venv/bin/python3 -m pytest -q tests/test_python_ast_boundary_check.py
→ 19 errors（ModuleNotFoundError: tools.development.python_ast_boundary_check）

.venv/bin/python3 -m pytest -q
→ 942 passed, 19 errors
```

Evidence：`records/development/2026-08-05-task-python-cache-ast-boundary-red-evidence-v1.md`

## 検出対象

公開APIは`inspect_python_source_boundaries(source_text)`だけである。結果は正規化済み操作名を
重複なくソートしたtupleで、行や列の位置を同一性へ持ち込まない。

| 正規化名 | 対象 |
| --- | --- |
| `os.environ` | 読取、subscript読取、subscript代入、`update()`など接触すべて |
| `os.putenv` | 実行中processの環境書換え |
| `os.remove`／`os.rmdir`／`os.unlink` | fileとdirectoryの削除 |
| `shutil.rmtree` | 木ごとの削除 |
| `pathlib.Path.unlink` | `Path(...)`を作って削除methodを呼ぶ形 |
| `time.time`／`datetime.datetime.now` | 時間ベースの保持・削除判断を入れない境界 |

## 誤検知を避ける仕組みと見逃しを減らす仕組み

- 判定はASTのnodeに対して行う。docstringや識別子の中に同じ文字列が現れても、
  `ast.Name`でも`ast.Attribute`でもないため違反にならない。`bytecode_environment`という
  関数名と`os.environ`という語を含むdocstringだけのsourceが違反ゼロになることをTestで固定した。
- 名前は必ずimport束縛から辿る。辿れない名前は違反にしない。`time.sleep()`、`os.path.join()`は
  違反にならない。
- 別名を解決するので、`import os as runtime_os`、`from os import environ`、
  `from pathlib import Path as P`、`from datetime import datetime`のいずれの書き方も
  同じ正規化名になる。参照するだけでも違反とする。
- 引き受けない範囲を明示した。変数へ入れ替えた後の値、`getattr`等の動的呼出し、
  相対importと`*` importは解決しない。指示の「推測で追加しない」に従い、広げていない。
  列挙対象の検出には影響しない。
- 構文解析できないsourceは`PythonAstBoundaryError`（code `source_unparsable`）で止まり、
  結果を返して続行しない。
- 検査器のsource自身をASTで解析し、importするtop-level moduleが`ast`だけであることを
  Testで確認している。外部process、network、filesystem書込みの手段を持たない。

## 既存cache Testの置換

`tests/test_task_python_cache.py::test_module_has_no_deletion_or_retention_or_global_environment_change`
を、禁止語の文字列検索から検査器の呼出しへ置き換えた。

旧検査が持っていた「既存runner／executorへ接続しない」「外部processを起動しない」条件は
AST検査器の対象外なので、落とさないために
`test_module_imports_no_runner_executor_or_external_process`を追加した。
`task_python_cache.py`のimport集合をASTで取り出し、
`{dataclasses, json, re, pathlib, tools.layout}`と完全一致することを確認する。

`tools/development/task_python_cache.py`は**1文字も変更していない**（`git diff HEAD`で確認済み）。

## 関連Testと全Test

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_python_ast_boundary_check.py` | `19 errors` | `19 passed` |
| `tests/test_task_python_cache.py` | — | `27 passed` |
| Layout関連を含む4 file合計 | — | `65 passed` |
| 公式policy runner suite `full` | `942 passed, 19 errors` | **`962 passed`** |

first receiptとfinal receiptはどちらも`passed 962／total 962`で完全一致した。

## TODO更新

全Test表示は既存CLI経由で公式receiptから更新した（`942 passed` → `962 passed`）。手入力していない。
最新Evidenceには旧cache GREEN Evidenceを残したまま、今回のAST GREEN Evidenceを追加した。

size上限（12,288 bytes）に近づいたため、更新規則に従い、今回と無関係で上位Evidenceに
置換済みの参照2件だけを外した。理由はGREEN Evidenceの「6. TODOから外した参照と理由」に記録している。

| 外した参照 | 理由 |
| --- | --- |
| V4 Issue永続化 GREEN | 検証は閉じており、現況の正本はIssue record 3件（TODOに残存） |
| 過去TODO候補一覧 | 41件は全件triage済みで未判断0件。判断結果の正本はtriage decisionとIssue record |

参照件数は機械計測し、TODOの記載を実値25件へ合わせた。最終は12,096 bytes、25件である。

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator | 合格 |
| Evidence節に限定したDigest照合 | 合格（25件） |
| TODO表示 vs first／final receiptの構造化集計 | 一致（962） |
| `git diff --check` | 各commitのstage前後で合格 |
| commit後のread-only照合 | working treeはclean |

## 未実施の範囲

- `tools/development/task_python_cache.py`、Layout v3、cache配置規則、既存Decision、
  Issue state、Task Contract、policy、configは変更していない。
- 実際の`~/.reviewcompass3`、`ReviewCompass3-data`、既存`DATA_ROOT`、`SENSITIVE_ROOT`へは
  一切書いていない。
- cache初期化、掃除、保持期限の自動化、既存runner／executorへの接続、環境変数のglobal変更、
  Windows adapter、既存操作の移行、外部送信は実装していない。
- 新しい正式Issue、Plan、Task Contract、policyは作っていない。
  `ISSUE-HTC-C9F6C917`のstateは`registered`のままである。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
