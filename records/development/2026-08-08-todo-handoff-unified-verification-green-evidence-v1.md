# TODO handoff単一検証入口 GREEN Evidence v1

- 実施日：2026-08-08
- 対象Issue：`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`
- Human着手指示：本sessionの「対応」
- 制約：hook／guarded commitを追加せず、実行者が明示する単一commandの終了コードを直接判定する

## 1. 固定入力

| role | path／identity | SHA-256 |
| --- | --- | --- |
| Issue正本 | `.reviewcompass/workflow/issues-v4/issue-todo-handoff-verification-gap-001--v1.json` | `475b0ea27b331b1d44e3883a30c575d21ebd14ab14b894725e8aa9121e51bba5` |
| 発生観測 | `records/development/2026-08-07-todo-handoff-verification-gap-observation-v1.json` | `01f57093a875059d738f7045cfc9ca124dde3d838f6bed4f1a9c533382a43dcc` |
| Human triage Decision | `.reviewcompass/workflow/triage-decisions-v4/dec-ic-todo-handoff-verification-gap-001--v1.json` | `929a7638b4f5c3fdb8b0ad2e2236cb8f9c5410103adfc9f07c1c3af9f321ebc0` |
| RED containing commit | `ebadd12` | commit objectをGitでread-only照合 |

## 2. TDD結果

REDでは次の2件だけが失敗し、既存8件は通過した。終了コードは`1`だった。

1. commit安定Git欄に合格する12,289-byte TODOを、旧CLIが`passed`／終了コード`0`で通した。
2. 共通手順に単一入口の契約が無かった。

RED Testだけをcommit `ebadd12`へ固定した後、`tools/development/todo_handoff.py`のCLIを既存の
`tools.development.todo_update_path.default_verify()`へ接続した。これにより次の既存検証を一つの
終了コードへ集約した。

- commit安定Git欄：`todo_handoff.validate_commit_stable_git_section`
- 12,288-byte上限、active ID 1件、禁止履歴0、参照到達性：`todo_compaction.validate_compacted_todo`
- Evidence節の参照Digest一致：`todo_record_generation.verify_reference_digests`

共通手順は、単一commandをpipeや`;`連結で代替せず、終了コードを直接判定する規則へ更新した。
hookとguarded commitは追加していない。

## 3. GREEN検証

| 検証 | command／対象 | 結果 |
| --- | --- | --- |
| targeted | `tests/test_todo_handoff_git_state.py`、`tests/test_todo_handoff_prompt_entrypoints.py` | `10 passed`、exit `0` |
| 関連回帰 | 上記＋`tests/test_todo_compaction.py`、`tests/test_todo_update_path.py` | `48 passed`、exit `0` |
| 旧実TODOへの新CLI | 12,617 bytesの旧TODO | `TODO exceeds 12288 bytes`、exit `1` |
| compact projection | `todo_handoff_projection.render_todo_handoff`とroot TODOの再読込比較 | byte-identical、3,871 bytes |
| compact後の実CLI | `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md` | `passed`、exit `0` |
| 公式全Test | policy runner `full` | `1269 passed`、exit `0`、Python 3.9.6、pytest 8.4.2、fallback `false` |
| 公式receipt | `records/development/2026-08-08-todo-handoff-unified-verification-green-test-receipt-v1.json` | SHA-256 `4dbcdb642ddeb35552748873e02f04056f7a84c6ae9ba31b26d45270b62626d4` |
| 差分検査 | `git diff --check` | 合格 |

実装identityは次のとおりである。

| path | SHA-256 |
| --- | --- |
| `tools/development/todo_handoff.py` | `fbc6279b6471913f490b604940c14ef792b139e35819c951a0e4406ce5994d61` |
| `tools/development/todo_update_path.py`（再利用、変更なし） | `3396e9d8131c8059661a7a264503faafe7ad1d5b8af96b09d9483385e873bd31` |
| `tools/development/todo_compaction.py`（再利用、変更なし） | `31358ea25bcabbd93762710efe528caef5c3b094fcbdb6111dde30d92389cb90` |
| `docs/development/prompts/todo-handoff-update.md` | `bb6b7b1364886b0c22591c4a48d5d2ed5b8aadc947152ce285cf70e19aba0591` |
| `tests/test_todo_handoff_git_state.py` | `c4f6ff744c442536c6e83f9d476092b9f82d0f308a02e64920e7eeaeb2d3d426` |
| `tests/test_todo_handoff_prompt_entrypoints.py` | `7d43de146a9fe2cfc292fe4bc3b5c969ce9049ea8cbc0feb3711c00cdcf07b94` |

## 4. 判断境界と残余

- 【実測】Issueが記録した二tool分離は、単一CLIが両検証の失敗を非0へ反映することで解消した。
- 【実測】旧TODOのbyte超過も同じCLIで検出し、正規projectionで上限内へ修復した。
- shellの外側で実行者が明示的にpipeを追加すれば、shellの終了コード規則による隠蔽はなお可能である。
  そのため共通手順は単独実行を要求し、内部ではpipeを使わない。これはIssue正本が指定した
  「実行者が明示実行するcommandとして単一入口と終了コード直接判定」の境界である。
- Issue recordの`resolved`変更とResolution VerdictはHuman判断であり、本実装では行っていない。
