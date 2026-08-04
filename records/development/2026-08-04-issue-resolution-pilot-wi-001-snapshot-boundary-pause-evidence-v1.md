# Issue Resolution Pilot WI-001 Snapshot Boundary Pause Evidence v1

- recorded_at: `2026-08-04T11:38:55+09:00`
- Task Contract: `TC-RC3-ISSUE-RESOLUTION-TODO-COMPACTION-2026-08-04-V1`
- work_item_id: `WI-001`
- status: `pause_and_triage`

## 実施

固定Testを変更せず`tools/development/todo_snapshot.py`を実装した。実装SHA-256は
`a2c7010844146d2c5a2f44bc5ac1be8a2f6389cef33c9eb68079e6440d61f783`、固定Test SHA-256は
`890f65df6734c314287a4d76c48232874560cb597f66122ab24d47d9e3c66521`である。

- command: `python3 -m pytest -q tests/test_todo_snapshot.py`
- result: `9 passed in 0.03s`

実際の`TODO_NEXT_SESSION.md`、snapshot、manifestは作成または変更していない。

## 停止理由

Plan v3 ACC-001は圧縮直前TODOのsnapshotを要求する。一方、Task Contract v1はWI-001をWI-002とWI-006より
先に完了・commitする。両後続Work ItemではAGENTS.mdに従ってTODOを更新するため、今snapshotすると圧縮直前には
source identityが変わる。固定Testもsnapshot後のsource変更を意図どおり拒否する。したがって、現行順序のまま
実snapshotを作ると、ACC-001、WI-003開始条件、rollback sourceのいずれかを真として扱えない。

固定Observationは
`records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-observation-v1.json`、SHA-256
`53891d8fc134caa48185f62b77e435679d13bb90e8723bf5b337600dea9cdec3`である。

## 改善候補とroute提案

Improvement Candidateは
`records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-candidate-v1.json`、file SHA-256
`9bc2bb3d921902cd46cd56607290fb71b9681400784725ee8bd7de9ecfc87a35`、content Digest
`f037398f905ed48973b6a059b5f59bf3b36b6f35097ea819716be7aeda107cc2`である。current Issue内の版付き
Upstream Revision候補として、identity、source参照、file SHA-256、content Digestを機械照合した。

candidate kindは`plan_acceptance_and_work_item_order_gap`、routeは`current_issue_plan_revision`である。
Acceptanceの真偽とrollback sourceへ影響するため、現行Workを停止し、Human判断を待つ。

推奨案はPlan／Task Contractを版付き改定し、WI-001をhelper実装・GREENへ限定すること、WI-002とWI-006の
完了・commit後かつWI-003直前に実snapshotを作成・再読込する独立Work Itemを追加することである。Plan v3、
Task Contract v1、固定Testはin-place変更しない。
