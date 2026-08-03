---
evidence_id: RC3-WORK-UNIT-COMMIT-REMINDER-RED-2026-08-04-V1
recorded_at: 2026-08-04T07:10:31+09:00
status: verified_red
confidentiality_class: project-internal
---

# Work Unit Commit Reminder RED Evidence V1

## 期待動作

- 完了済み作業単位にdirty差分があれば、未コミットを通知して次作業を停止する。
- 完了済み作業単位がcleanなら、commit関門を通過する。
- 作業中のdirty差分を、完了済み・未コミットと誤判定しない。
- Git状態を`git status --porcelain=v1 --untracked-files=all`で機械取得する。
- CLIがmachine-readableな結果とexit codeを返す。

固定Testは`tests/test_work_unit_transition.py`、SHA-256は
`08ffe474117ceeedbb746d6b0278ca0dc29f859f7348c37dfb141a7f8dcbea4f`である。

## 初回RED

command：`python3 -m pytest -q tests/test_work_unit_transition.py`

結果：`5 failed in 0.04s`、exit code 1。5件すべて
`ModuleNotFoundError: tools.development.work_unit_transition`であり、期待する遷移preflight未実装だけが
失敗理由だった。
