# Claude → Codex：task専用Python cache root最小slice 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-task-python-cache-slice.md`

指示の3作業単位をすべて実施した。**停止していない。**

## commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 1 承認記録 | `0b11b7d76737ebd1de2fdba96e08aecbaef197fc` | Decision、Plan状態注記、TODO、承認時のfirst／final receipt（codeとtestは含まない） |
| 2 RED | `fd858928bb9337161b4bebf84c1fd7b0f4907969` | `tests/test_task_python_cache.py`、RED Evidence（実装なし） |
| 3 GREEN | `c9587dbf6135524f4abdee4cd8e02cf16319088d` | 実装、test、GREEN Evidence、GREEN first／test receipt、CLI生成済みTODO |

各commitは明示pathだけをstageした。commit後の`git status --short`は空、
`work_unit_transition --work-status completed`は3回とも`next_work_allowed: true`。

## Decision

`DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001`
（`records/development/2026-08-05-machine-operation-routing-task-python-cache-approval-decision-v1.md`）

配置・所有・保持は新しく決めず、Human承認済みのLayout v3をそのまま使うことを明記した。
外部rootは`<runtime_root>/projects/<project_id>/development/cache/`である。
固定入力7件の作成時SHA-256を記録した。

Plan提案`docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md`の
実施状態注記へ、Plan全体は`awaiting_human_approval`のまま、§2.2のcache root最小sliceだけが
このDecisionで承認された旨と、未承認項目（実ホーム配下の初期化、既存processへの自動適用、
掃除・保持期限の自動化、Windows adapter、既存操作の移行）を追記した。

## RED／GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_task_python_cache.py` | `26 errors`（実装module不在） | `26 passed` |
| Layout v3 Test 3 file合計 | — | `45 passed` |
| 公式policy runner suite `full` | `916 passed, 26 errors` | **`942 passed`** |

GREEN receiptのfirst／finalは両方とも`passed 942／total 942`で完全一致した。
TODOの全Test表示は既存CLI経由で公式receiptから更新した（`916 passed` → `942 passed`）。手入力していない。

### RED Testの1点訂正

保持境界のsource inspectionで禁止語に`environ`を挙げていたが、これは指示が求める公開API名
`bytecode_environment`自身に含まれ、実装が何をしていても必ず失敗する条件だった。
意図（実行中processの環境を書き換えない）を正しく表す`os.environ`へ直した。
`putenv`、削除手段、時間ベースの判断、既存runnerへの接続の禁止はそのまま残している。
他のTestは緩めていない。この訂正はGREEN Evidenceにも記録した。

## 実際に作成した一時directoryの範囲

Testはすべて`tmp_path`（pytestが用意する一時directory）配下だけを使う。

- fake project：`<tmp_path>/checkout/`（Project Manifestとv3正本recordの複製だけ）
- runtime root：`<tmp_path>/runtime/.reviewcompass3/`
- 作られるのは`projects/<project_id>/development/cache/`とその下の
  `python-bytecode/<task_id>/`だけである。

同じprofile配下の`data`、`state`、`logs`、`evaluation`、`sensitive`と、runtime root直下の
`config`が作られないことをTestで機械確認している。

## bytecode隔離の実測

一時project配下に`sample_module.py`を置き、`bytecode_environment()`が返したmappingを
明示的に子Python processへ渡して取り込ませた。

| 確認項目 | 結果 |
| --- | --- |
| 子processの終了code | `0`（標準出力は`1`） |
| project内の`__pycache__` | `0`件 |
| task directory配下の`.pyc` | 1件以上あり |

## 実ホーム配下を作っていないこと

`~/.reviewcompass3`は2026-08-04のWork 4Aで既に存在しており、中身は
`projects/reviewcompass3/development/data/work4a/`だけである。本作業の前後で確認した。

- `cache`という名前のdirectoryは1つも無い。
- `python-bytecode`という名前のdirectoryは1つも無い。
- 本session（21:00以降）に更新されたfileは1件も無い。

`ReviewCompass3-data`、既存の`DATA_ROOT`、`SENSITIVE_ROOT`、project内にも書いていない。

## 検査結果

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator | 合格（12,176 bytes、上限12,288） |
| Evidence節に限定したDigest照合 | 合格（26件） |
| TODO表示 vs first／final receiptの構造化集計 | 一致（942） |
| `git diff --check` | 各commitのstage前後で合格 |
| commit後のread-only照合 | working treeはclean |

TODOは上限に近づいたため、更新規則に従って既に上位Evidenceで置き換えられた参照2件
（定型記録生成のPlan提案時receipt、読み取り専用argv executorのGREEN receipt）を外した。
件数は毎回機械計測した。

## 実装の性質（Testで固定）

- `resolve_task_cache()`はread-onlyで、directoryを一切作らない。2回呼んでも同じ値である。
- `resolve_task_cache()`は`project_id`引数を持たない。project IDはProject Manifestからだけ読む。
- profileは`development`だけを受け付ける。承認範囲がそこだけだからである。
- unsafeなtask ID、unsafeなprofile、相対runtime root、project内へ重なるruntime root、
  symlinkのcache target、経路上の通常file、manifestの無いproject rootを拒否し、
  Layout v3の初期化を**一度も呼ばない**（初期化関数を差し替えて確認している）。
- moduleのsourceに削除手段、時間ベースの判断、実行中processの環境書換え、既存runner／
  executorへの接続が無いことをsource inspectionで固定している。
- 別のpath規則を作らず、`resolve_project_runtime_layout()`と
  `initialize_project_runtime_layout()`を再利用している。

## 対象外（変更していない）

- 実際のホーム配下の初期化、既存processへの自動適用、既存call siteの変更。
- `policy_test_runner`、`structured_argv_executor`への接続。
- 掃除・保持期限の自動化、時間ベースの削除、global cacheの書換え、環境変数のglobal変更。
- Windows adapter、既存操作の移行、移行inventoryの作成。
- Git metadata書込み、project成果物書込み、external操作、host側tool構文、外部送信。
- Issue state、Task Contract、policy、config、既存Decision。
- `ISSUE-HTC-C9F6C917`と`ISSUE-HTC-66C3E6CA`は`registered`のままである。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
