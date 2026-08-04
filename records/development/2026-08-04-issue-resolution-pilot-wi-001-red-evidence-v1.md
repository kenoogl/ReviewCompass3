# Issue Resolution Pilot WI-001 RED Evidence v1

- recorded_at: `2026-08-04T11:30:13+09:00`
- Task Contract: `TC-RC3-ISSUE-RESOLUTION-TODO-COMPACTION-2026-08-04-V1`
- Task Contract SHA-256: `661df56b9f2c78a261e3b345e727bf9cd47bbf09225186c529cceadf32eb56cd`
- work_item_id: `WI-001`
- test: `tests/test_todo_snapshot.py`
- test SHA-256: `890f65df6734c314287a4d76c48232874560cb597f66122ab24d47d9e3c66521`

## 固定した期待境界

1. UTF-8、絵文字、最終改行なしを含むTODO sourceをbyte-exact snapshotへ複製する。
2. snapshotとは別のJSON manifestへsource／snapshot path、SHA-256、bytes、lines、Claim数を記録し、manifest content Digestを持つ。
3. source、snapshot、manifestを再読込して一致を検証する。
4. Claim 0件と最終改行なしを境界例として受理する。
5. snapshot改変、snapshot後のsource変更、既存出力衝突をそれぞれ異なる理由で拒否する。
6. snapshotとmanifestの出力を`records/session-handoffs/`配下へ限定し、repository外escapeを拒否する。

## RED結果

- targeted command: `python3 -m pytest -q tests/test_todo_snapshot.py`
- targeted result: `9 failed in 0.08s`
- full command: `python3 -m pytest -q`
- full result: `9 failed, 562 passed in 3.01s`
- failure identity: 9件すべて`ModuleNotFoundError: tools.development.todo_snapshot`

既存562 Testは合格した。失敗は期待module未実装だけで、実TODO、snapshot、manifestは作成または変更していない。

## 次action

本REDテストとEvidenceをcommitする。commit後、テストを変更せず`tools.development.todo_snapshot`を実装し、9件すべてをGREENへする。
