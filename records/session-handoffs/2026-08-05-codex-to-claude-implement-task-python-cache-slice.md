# Codex → Claude：task専用Python cache root最小sliceの実装指示

## Human承認と既決の配置規則

**Humanは、`ISSUE-HTC-C9F6C917`の次の最小sliceとしてtask専用Python cache rootを実装するよう指示した。**

cacheの配置・所有・保持は新たに決めない。Human承認済みのLayout v3をそのまま使う。

- 正本：`records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`
- 承認：`records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json`
- 外部root：`<runtime_root>/projects/<project_id>/<profile>/cache/`
- 現在対象profile：`development`
- cache rootの意味：project外、Git管理外、runtime所有、`evictable`、runtimeが所有cacheを削除可能
- runtime rootの既定：home相対`.reviewcompass3`。ただし今回のTestは一時directoryだけを使い、
  実際のホーム配下を作成しない。

## 誰が何をするか

- **Human**は、この最小sliceの実装を指示した。
- **Codex**は、Layout v3に従う範囲と対象外を固定する。
- **Claude**は、DecisionとPlan状態注記を先に記録し、TDDでcache rootの解決・明示初期化・環境値生成を実装する。

これはcache rootの最小sliceだけの承認である。既存processへの自動適用、既存操作の移行、cleanup自動化は承認していない。

## 作業単位1：承認記録（codeは変更しない）

1. 次を作成する。

   `records/development/2026-08-05-machine-operation-routing-task-python-cache-approval-decision-v1.md`

   Decision IDは`DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001`とする。
   Human指示、Layout v3の配置・保持規則、承認範囲、対象外、固定入力の作成時SHA-256を記録する。

2. `docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md`へ状態注記を追記する。
   - Plan全体は`awaiting_human_approval`のままである。
   - cache root最小sliceだけが上記Decisionで承認された。
   - 実際のホーム配下の初期化、既存processへの自動適用、cleanup／retention automation、Windows adapter、
     既存操作の移行は未承認と明記する。

3. TODOを共通手順で更新し、DecisionとPlan状態を最新authority／Evidenceへ追加する。
   全Test表示は必ず既存CLI
   `python -m tools.development.todo_update_path`を通して公式receiptから更新する。手編集しない。

4. CLIは次の固定pathへfirst/final receiptを作る。

   - `records/development/2026-08-05-machine-operation-routing-task-python-cache-approval-first-receipt-v1.json`
   - `records/development/2026-08-05-machine-operation-routing-task-python-cache-approval-final-receipt-v1.json`

   Decision、Plan注記、TODO、上記first/final receiptだけを1つの意味的commitにする。code／testは混ぜない。

## 作業単位2：RED Test（実装しない）

次を新規作成する。

`tests/test_task_python_cache.py`

実装moduleはまだ作らない。Testは少なくとも次を固定する。

1. **副作用なしの解決**：Layout v3、project manifestのstable `project_id`、runtime root、`development`、
   safeなtask IDから、次を決定的に解決する。解決だけではdirectoryを作らない。

   `<runtime_root>/projects/<project_id>/development/cache/python-bytecode/<task_id>`

2. **明示初期化だけが作る**：専用の初期化操作は、Layout v3の`cache` rootと上記task directoryだけを作る。
   data／state／logs／evaluation／sensitiveやconfig rootは作らない。

3. **環境値生成**：`PYTHONPYCACHEPREFIX`だけを持つ環境mappingを返す。mappingを生成するだけでは
   `os.environ`を変更しない。値は解決済みtask directoryの絶対pathである。

4. **安全境界**：project IDはproject manifestから得る。unsafe task ID、unsafe profile、相対runtime root、
   project内へ重なるruntime root、symlinkを含むtarget、存在する通常fileをdirectoryとして使う入力を拒否し、
   初期化操作を呼ばない。

5. **保持境界**：cleanup／削除関数、時間ベースretention、global cacheの書換え、既存runnerの環境変更は
   このmoduleに存在しないことをsource inspectionで固定する。

6. **実際のbytecode出力の隔離**：一時runtime rootだけを使い、`PYTHONPYCACHEPREFIX`環境mappingを明示的に
   子Python processへ渡す小さなTestを作る。cache fileがtask directory配下にだけ作られ、project内には
   `__pycache__`が作られないことを機械確認する。

RED実行と結果を次へ記録する。

`records/development/2026-08-05-machine-operation-routing-task-python-cache-red-evidence-v1.md`

RED TestとRED Evidenceだけを第2の意味的commitにする。

## 作業単位3：GREEN実装（最小slice）

次を新規作成する。

`tools/development/task_python_cache.py`

実装要件：

- `tools.layout.baseline`のpublic Layout v3 resolver／initializerを再利用し、別のpath規則を作らない。
- project IDは`.reviewcompass/project-manifest.json`から読み、callerが任意のproject IDを渡して別projectのcacheへ
  書けないようにする。
- 解決と初期化を別APIにする。解決はread-only、初期化だけが明示的にcache directoryを作る。
- task directoryはcache rootの配下だけに作る。safe identifier以外、symlink、通常file、root脱出はfail-closedで拒否する。
- `PYTHONPYCACHEPREFIX`の環境mappingを返すだけにし、`os.environ`のglobal変更をしない。
- cleanup、削除、retention automation、既存`policy_test_runner`や`structured_argv_executor`への接続、
  実際の`~/.reviewcompass3`作成を追加しない。

GREEN後、次を作成する。

- `records/development/2026-08-05-machine-operation-routing-task-python-cache-green-evidence-v1.md`
- `records/development/2026-08-05-machine-operation-routing-task-python-cache-green-first-receipt-v1.json`
- `records/development/2026-08-05-machine-operation-routing-task-python-cache-green-test-receipt-v1.json`

関連Test、Layout v3 Test、公式全Testを実行する。TODOの全Test行は、上記first/final GREEN receiptの
構造化集計を既存TODO更新CLI経由で反映する。

GREEN実装、test、GREEN Evidence、GREEN receipt、CLI生成済みTODOを第3の意味的commitにする。

## 共通の禁止事項と停止条件

- 実際の`~/.reviewcompass3`、`/Users/Daily/Development/ReviewCompass3-data`、既存`DATA_ROOT`、
  `SENSITIVE_ROOT`、project内にcacheを作成・移動・削除しない。
- 既存processへの自動適用、`policy_test_runner`／executorの既存call siteの変更、環境変数のglobal変更をしない。
- cleanup／retention automation、Windows adapter、migration inventory、Git metadata書込み、project成果物書込み、
  external操作、host側tool構文、外部送信を実装しない。
- Issue state、Task Contract、policy、config、既存Decisionを変更しない。
- path policyやLayout v3の権威と矛盾する入力・要求が出た場合は、局所patchを選ばず停止して報告する。

各commit前に`git diff --check`、TODO validator、compaction validator、参照整合を実行する。commit後に
read-only照合と`python3 tools/development/work_unit_transition.py --work-status completed`を実行する。

## Claudeの完了報告

Git管理外の次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-implement-task-python-cache-slice.md`

Decision、RED／GREEN commit SHA、実際に作成した一時directoryの範囲、bytecode隔離結果、全Test、
実ホーム配下を作っていないこと、対象外を簡潔に報告する。
