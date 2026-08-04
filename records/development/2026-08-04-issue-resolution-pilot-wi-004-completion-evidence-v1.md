# Issue Resolution Pilot WI-004 Completion Evidence v1

## 実施

- `docs/development/prompts/todo-handoff-update.md`をCodex／Claude共通の唯一のTODO更新promptとして作成した。
- `AGENTS.md`の重複TODO意味規則を共通promptへの一参照へ置き換えた。
- root `CLAUDE.md`を同じpromptへのlink-only入口として作成した。
- WI-004用projection入力を別versioned fileにし、root TODOをWI-005入口へ機械更新した。

## 結果

| 対象 | 結果 |
|---|---|
| RED | targeted `1 passed, 2 failed`、全体`632 passed, 2 failed`。共通prompt未作成だけで失敗 |
| GREEN targeted | `3 passed in 0.02s` |
| 共通prompt | 2,160 bytes、repository内同名file 1件 |
| AGENTS入口 | prompt path参照1件、独立TODO意味規則0 |
| Claude入口 | prompt path参照1件、link以外の本文0、第二authority負例は拒否 |
| 更新後TODO | 2,893 bytes、64 lines、active Issue 1件、SHA-256 `388ccc4699a8aa1438a4f04b6ce88abc73ef07e5fd9664c87763056d2bd24769` |
| commit安定validator | `passed`、Finding 0 |
| 公式全Test | `634 passed in 2.99s`、fallback `false` |
| 公式receipt | `records/development/2026-08-04-issue-resolution-pilot-wi-004-green-test-receipt-v1.json`、SHA-256 `7cd110a4dadffaa5d7ee2c62051b409bda7bac8f8eab95767787853f10f3195e` |

主要成果物Digest：

- prompt：`docs/development/prompts/todo-handoff-update.md`、SHA-256 `63bb72d3dd702aa073ceba9b979b55f79497139e7433fc36822b041947fd7d49`
- AGENTS入口：`AGENTS.md`、SHA-256 `e1fd78f1c746c386697d36561040bea46ace2e067f297018838dffb099e5b931`
- Claude入口：`CLAUDE.md`、SHA-256 `9fca6c61b0e6468e8a0e39e050df0cb2584f7e95690c0b9830b701e291d5bf0f`
- Test：`tests/test_todo_handoff_prompt_entrypoints.py`、SHA-256 `cb2d557990bc01b4365b8ea8fdcd78f130a82eb65362f8b7a0ef5f393015d461`
- projection入力：`records/development/2026-08-04-issue-resolution-pilot-wi-004-projection-input-v1.json`、
  SHA-256 `dd16dbf7d10fe2eda86e5d6e4b5e1cf5b12c083832f8ded935d2d790113ff98f`

## 判断

- OBL-004、ACC-005、ORACLE-005とWI-004 completion conditionを満たす。
- 本Evidenceを含むcommitとclean transition後、WI-005を開始できる。
- Resolution VerdictとIssue解決はHuman判断が必要であり、未実施のまま維持する。

## 発生した問題と対処

- TODO更新入力を作る際、WI-003の固定projection入力をin-place更新しかけた。TODO生成前のDigest照合で、
  WI-003 Completion Evidenceが固定したSHAを壊すことを検出したため、変更を戻し、
  `2026-08-04-issue-resolution-pilot-wi-004-projection-input-v1.json`を新規作成した。WI-003入力SHAは
  `0e13d136d951a19e88e28f9397e39cce80815d73e13535b61b0f379fa69710f4`のままである。
- 期待executorはversioned artifactの不変性validator、実executorはLLMによるpath選択と機械Digest照合だった。
  手戻り原因候補は更新対象pathの手選択である。版付きprojection入力のin-place変更拒否Test／writerは未実施の
  `manual_operation_candidate`としてcheckpointへrouteし、WI-005のstale閉包確認対象にする。

## 未実施

- WI-005のpost-write再読込、snapshot restore rehearsal、Pilot測定、Resolution Verdict候補。
- Resolution VerdictのHuman判断、Issue解決、早期Pilot完了、Work 4移行。
