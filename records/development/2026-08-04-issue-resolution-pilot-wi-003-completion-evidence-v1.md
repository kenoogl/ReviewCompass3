# Issue Resolution Pilot WI-003 Completion Evidence v1

## 実施

- `tools/development/todo_handoff_projection.py`で、構造化入力から短いroot TODOを決定的に生成した。
- `docs/development/templates/TODO_NEXT_SESSION.template.md`へactive Issue欄とauthority／Evidence欄を追加した。
- `records/development/2026-08-04-issue-resolution-pilot-wi-003-projection-input-v1.json`を固定入力とした。
- WI-007 snapshotとのsource identity一致をTODO書換え直前に再確認し、生成、圧縮検証、原子的置換、再読込照合を機械実行した。

## 結果

| 対象 | 結果 |
|---|---|
| 書換え前TODO／WI-007 snapshot SHA-256 | `16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`で一致 |
| 書換え前 | 85,219 bytes、900 lines、123 Claims |
| 書換え後TODO SHA-256 | `6acb26636c5b50fe4ecb527ce49cc2f78ca3b801e57b612e4fa8a1122b68978e` |
| 書換え後 | 2,824 bytes、64 lines、詳細Claim 0、active Issue 1件、解決済み参照4件 |
| 圧縮validator | 合格。active IDは`ISSUE-PILOT-TODO-GROWTH-001`だけ |
| commit安定validator | `passed`、Finding 0 |
| 関連Test | `38 passed in 0.12s` |
| 公式全Test | `631 passed in 2.64s`、fallback `false` |
| 公式receipt | `records/development/2026-08-04-issue-resolution-pilot-wi-003-green-test-receipt-v1.json`、SHA-256 `0a08ac5b3f9b0692792959137764822497a00668ff33afc8d429e3f32011cd19` |

主要成果物Digest：

- renderer：`tools/development/todo_handoff_projection.py`、SHA-256 `e43982c5c3f0e7930e21995c380d81b998515acd545214ae6efe5a5ec2d5cc89`
- repository結合Test：`tests/test_todo_handoff_projection_repository.py`、SHA-256 `67d1fc2828a0636a1f5d0bc2fee084e3037a56bd3b3138996475237c90866dc9`
- template：`docs/development/templates/TODO_NEXT_SESSION.template.md`、SHA-256 `9bfba3daca9c12ea4854806c9ec0f763d45d68585bbcf653967c5725ebbde4b1`
- projection入力：`records/development/2026-08-04-issue-resolution-pilot-wi-003-projection-input-v1.json`、SHA-256 `0e13d136d951a19e88e28f9397e39cce80815d73e13535b61b0f379fa69710f4`

## 判断

- ACC-002／ACC-003とWI-003 completion conditionを満たす。
- WI-007のbyte-exact snapshotとmanifestは不変であり、WI-005のrestore rehearsalに使用できる。
- 本Evidenceを含むcommitとclean transitionの確認後、WI-004を開始できる。

## 発生した問題と対処

1. テスト用templateには必須2 headingがあったが、repositoryの実templateにはなかった。事前renderが
   `TODO template headings are incomplete`で停止し、TODO書換え前に検出した。実templateを修正し、
   `tests/test_todo_handoff_projection_repository.py`を修正前`1 failed`、修正後`1 passed`として固定した。
   恒久境界は、複製fixtureだけでなく実templateを結合Testの対象にすることである。
2. 関連Test実行時に存在しない`.venv/bin/python3`と、存在しないTest file名を手入力し、各1回再実行した。
   成果物書換えや判定への影響はない。期待executorは版付きrunner設定とrepository file discoveryであり、
   実executorがLLMによるcommand文字列手入力だったことが手戻り原因である。今回は`config/development-test-runner.json`の
   `python3`入口と`rg --files tests`で補正した。targeted suite名簿または専用CLIによる完全機械化は未実施の
   `manual_operation_candidate`としてcheckpointへrouteし、現行IssueのAcceptanceを変更しない。

## 未実施

- WI-004の共通TODO更新promptとCodex／Claude入口参照。
- WI-005のpost-write verification、byte-exact restore rehearsal、Pilot測定、Resolution Verdict候補。
- Resolution VerdictのHuman判断。
