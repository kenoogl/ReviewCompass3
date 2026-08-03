---
evidence_id: RC3-COMMIT-HANDOFF-STABILITY-RED-2026-08-04-V1
recorded_at: 2026-08-04T05:18:39+09:00
status: verified_red
confidentiality_class: project-internal
---

# Commit Handoff Stability RED Evidence V1

## 1. 期待動作

`TODO_NEXT_SESSION.md`のGit欄について、次をtest-firstで固定した。

- commit境界、Git機械取得、commit完了時点のworktree記述を必須にする。
- TODO自身を含むcommit SHA、mutable remote snapshot、未コミットTODO snapshotを拒否する。
- Evidence節などGit欄の外にあるcommit SHAは拒否しない。
- Git欄の欠落と重複を拒否する。
- CLIがmachine-readable reportとexit codeを返す。
- repositoryのtemplateと現行TODOを代表dataとして検査する。

Testは`tests/test_todo_handoff_git_state.py`、SHA-256は
`9af215b6f60e8b515af0adb97b080f66b5c5a6473ff0fd1d7f2bfea780a3797b`である。

## 2. 初回RED

command：`python3 -m pytest -q tests/test_todo_handoff_git_state.py`

結果：`6 failed in 0.04s`、exit code 1。6件すべて
`ModuleNotFoundError: tools.development.todo_handoff`であり、期待するvalidator未実装だけが失敗理由だった。

## 3. 中間RED

validator実装後に同じcommandを再実行し、`5 passed, 1 failed in 0.03s`となった。残る1件は旧templateと
現行TODOがcommit安定形式でないことを代表data Testが検出したものである。Test変更または違反の見逃しではなく、
policy、template、TODOを新契約へ更新する必要がある期待どおりのREDだった。
