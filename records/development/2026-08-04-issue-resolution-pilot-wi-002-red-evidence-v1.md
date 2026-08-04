# Issue Resolution Pilot WI-002 RED Evidence v1

## 対象

- Work Item：`WI-002`
- Task Contract：`records/task-contract/issue-resolution-todo-compaction-implementation-v2.json`
- Task Contract containing commit：`156c82349682cd2cd454cde2570355605acedf82`
- Test：`tests/test_todo_compaction.py`
- Test SHA-256：`c5dd608f2561130d3fb46ffa23bb6363e823d65eaa89c89b14a4741e788315a1`

## 固定した期待境界

- TODO全体は12288 bytesちょうどを合格、12289 bytesを拒否する。
- 過去Claim、手戻り詳細section、session時系列logを拒否する。
- active Issue IDは既知の一件だけを許可し、未知IDと重複IDを拒否する。
- authority／Evidenceのrepository相対参照を解決し、壊れた参照を拒否する。
- snapshot／manifestのDigest一致後だけbyte-exact restoreを行う。
- snapshot改変、manifest改変、restore後不一致を拒否し、失敗時は変更前TODOへ戻す。

## RED確認

- targeted：`python3 -m pytest -q tests/test_todo_compaction.py`
- 結果：`12 failed in 0.10s`
- 全体：`python3 -m pytest -q`
- 結果：`12 failed, 590 passed in 2.92s`
- 失敗identity：12件すべて`ModuleNotFoundError: tools.development.todo_compaction`。
- fixture準備、既存Task Contract参照、既存590 Testには別の失敗を観測していない。

## 判定

期待したREDである。`tools/development/todo_compaction.py`、実snapshot、TODO compaction、WI-006、
Resolution Verdictは作成または開始していない。RED containing commitとclean transition確認後だけ、固定Testを
変更せずvalidator／restore実装へ進む。
