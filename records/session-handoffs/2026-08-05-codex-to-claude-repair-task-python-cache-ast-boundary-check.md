# Codex → Claude：task Python cacheのAST境界検査を修復する指示

## Human指示と目的

**Humanは、cache最小sliceの完了報告で見つかった検査の誤検知に対し「対応」と指示した。**

対象は`tools/development/task_python_cache.py`の「禁止操作を含まない」ことを確かめる受入検査だけである。
現在の文字列検索は、正しい公開関数名`bytecode_environment`に含まれる`environ`まで誤検知した。
その場では`os.environ`へ狭めてGREENにしたが、これは再発防止になっていない。

今回の目的は、禁止語の文字列検索を**Python ASTによる操作検査**へ置き換えることだけである。
cacheの配置、所有、保持、実ホームでの初期化、既存processへの適用は変更しない。

## 誰が何をするか

- **Human**は、この修復をP1（次の作業単位）として指示した。
- **Codex**は、修復範囲、禁止事項、受入条件をこの文書へ固定する。
- **Claude**は、改善候補を記録し、RED→GREENでAST検査へ置換し、結果を報告する。

これは`ISSUE-HTC-C9F6C917`に紐付く`Test／oracle不良`の改善候補である。新しい正式Issue、Plan、Task Contract、
policyの作成・変更はしない。

## 作業単位1：改善候補の記録（code／testを変更しない）

次を新規作成する。

`records/development/2026-08-05-task-python-cache-ast-boundary-inspection-improvement-candidate-v1.md`

必須内容：

- `candidate_kind: improvement_candidate`、分類`Test／oracle不良`、優先度`P1`、状態`adopted_for_next_slice`。
- 発生元：task Python cache最小slice、`c9587db`、既存GREEN Evidenceの該当節。
- 事象：`environ`の部分文字列検索が`bytecode_environment`を誤検知したこと。
- 原因：操作の意味ではなく文字列の出現だけを検査したこと。
- 影響：今回の実装の振る舞いは壊していないが、同方式を他の検査へ複製すると誤検知・手戻りを起こす。
- route：既存`ISSUE-HTC-C9F6C917`へ紐付け、この作業単位でAST検査へ修復する。
- この候補は、実ホーム初期化等の未承認範囲を許可しないこと。

この候補だけを最初の意味的commitにする。TODOはこの時点では更新しない。

## 作業単位2：RED Test（実装を変更しない）

1. 新規module `tools/development/python_ast_boundary_check.py`の受入Testを、
   `tests/test_python_ast_boundary_check.py`として作成する。RED commitの時点ではmoduleを作らない。

2. Testは、少なくとも次を固定する。

   - 正しい識別子`bytecode_environment`を含むsourceは、`environ`という部分文字列だけで違反にしない。
   - `os.environ`への読取・代入・subscript操作を違反として検出する。
   - aliasを使う`import os as runtime_os; runtime_os.environ[...]`も検出する。
   - `os.putenv()`、`os.remove()`、`os.rmdir()`、`os.unlink()`、`shutil.rmtree()`の呼出しを検出する。
   - `Path(...).unlink()`と、`from pathlib import Path as P; P(...).unlink()`を検出する。
   - `time.time()`および`datetime.datetime.now()`を検出する。これらは時間ベースの保持・削除判断を
     この最小moduleに入れないという境界の検査である。
   - sourceを構文解析できない場合は、例外を出して続行しない。
   - 現在の`tools/development/task_python_cache.py`を検査すると違反ゼロである。

3. Testが期待する公開APIは、次だけとする。

   ```python
   findings = inspect_python_source_boundaries(source_text)
   ```

   結果は比較可能な不変値（例えばソート済みtuple）にする。各findingは、検出した正規化済み操作名を
   少なくとも含む。位置情報等の任意の詳細を結果の同一性へ持ち込まない。

4. RED実行と結果を次へ記録する。

   `records/development/2026-08-05-task-python-cache-ast-boundary-red-evidence-v1.md`

TestとRED Evidenceだけを第2の意味的commitにする。`task_python_cache.py`はこのcommitで変更しない。

## 作業単位3：GREEN実装と既存cache Testの置換

1. `tools/development/python_ast_boundary_check.py`を新規作成する。

   - Python標準ライブラリ`ast`だけを使う決定的な解析であること。外部process、LLM、network、filesystem書込みをしない。
   - aliasesを解決して上記の操作を検出する。検出対象以外の名前・属性を、部分文字列一致で違反にしない。
   - sourceが不正ならfail-closedで例外にする。
   - cache配置・初期化・削除・環境変数変更を実行しない。これは**検査器**であり、実行器ではない。

2. `tests/test_task_python_cache.py`の`test_module_has_no_deletion_or_retention_or_global_environment_change`を、
   文字列の禁止語検索からこのAST検査器を呼ぶ検査へ置換する。
   `task_python_cache.py`の振る舞いを変更しない。

3. 次を作成する。

   - `records/development/2026-08-05-task-python-cache-ast-boundary-green-evidence-v1.md`
   - `records/development/2026-08-05-task-python-cache-ast-boundary-green-first-receipt-v1.json`
   - `records/development/2026-08-05-task-python-cache-ast-boundary-green-test-receipt-v1.json`

4. `tests/test_python_ast_boundary_check.py`、`tests/test_task_python_cache.py`、関連Layout Test、公式全Testを実行する。
   TODOの全Test数は、必ず既存CLIで上記first/final receiptから更新する。手入力しない。
   TODOの最新Evidenceでは、旧cache GREEN Evidenceを消さず、今回のAST GREEN Evidenceを追加する。
   size上限に近づく場合は、更新規則に従い今回と無関係で上位Evidenceに置換済みの参照だけを外し、理由をEvidenceに記録する。

GREEN実装、置換後Test、GREEN Evidence、first/final receipt、CLI更新済みTODOを第3の意味的commitにする。

## 禁止事項・停止条件

- `tools/development/task_python_cache.py`、Layout v3、cache配置規則、既存Decision、Issue state、Task Contract、
  policy、configを変更しない。
- 実際の`~/.reviewcompass3`、`ReviewCompass3-data`、既存DATA_ROOT、SENSITIVE_ROOTへ書き込まない。
- cache初期化、cleanup、retention automation、既存runner／executorへの接続、環境変数のglobal変更、
  Windows adapter、migration、外部送信を実装しない。
- ASTに現れない動的実行やimportの一般解決を推測で追加しない。上記列挙対象を正確に扱えない設計矛盾が出た場合は、
  局所patchをせず停止して報告する。
- 通常の意味的commitは、明示path stage、`git diff --check`、関連Test、必要なTODO validator、
  commit後のread-only照合、`python3 tools/development/work_unit_transition.py --work-status completed`を満たせば実施してよい。

## Claudeの完了報告

Git管理外の次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-repair-task-python-cache-ast-boundary-check.md`

候補record、RED／GREEN commit SHA、RED結果、検出対象と誤検知を避ける仕組み、関連Testと全Test、
TODO更新、未実施の範囲を、事実とEvidence pathを対応付けて報告する。
