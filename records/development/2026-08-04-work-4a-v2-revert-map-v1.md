# Work 4A v2 Revert Map v1

## Purpose

Work 4A v2試作の撤回範囲を、commit subjectではなくpathと対象commitで示す。
v1と同じくhistoryを書き換えず、revert commitで戻す。

## 承認

`DEC-WORK4A-REBUILD-DESIGN-003`のrevert承認（2026-08-04の会話における
「提示した範囲でコミット済みv2試作をrevertしてよい。v2試作moduleとv2 E2E testだけを削除し、
TODOとチェックリストはv3の現在値を維持すること。」）。

## 撤回範囲

| 対象source commit | 表題 | 撤回したpath | 撤回しなかったpath |
| --- | --- | --- | --- |
| `33218e0` | Implement Work 4A v2 identity chain | `tools/development/work4a_rebuild_v2.py`（225行） | `TODO_NEXT_SESSION.md`（v3の現在値を維持） |
| `df2bd3c` | Define Work 4A v2 acceptance | `tests/test_work4a_rebuild_v2_e2e.py`（198行） | `TODO_NEXT_SESSION.md`（v3の現在値を維持）、`docs/development/2026-08-03-initial-development-checklist.md`（v3 authorityへ前進更新） |

両source commitは現在のHEADより前にあり、その後TODOとchecklistが変更されている。
このため`git revert`による機械的な巻き戻しは衝突する。TODOとchecklistは現在値が正しいので、
file削除だけを撤回操作とし、checklistはv3 authorityへ前進更新した。後退更新は行っていない。

## 保持したもの

| 保持対象 | 理由 |
| --- | --- |
| `293b596` Work 4A v2開始条件仕様、v1 revert map | v3がPolicy artifactとsource universeの仕様を継承する。v1 revert mapは実施記録として有効 |
| `61e635f` v3設計、`DEC-WORK4A-REBUILD-DESIGN-003`、TODO | 現行の実装正本 |
| `e215cea`、`f53eb51`、`6258aaf` Project-first Runtime Layout v3 | 独立承認済みの基盤。v1 revertでも保持した |
| `docs/design/2026-08-04-work-4a-rebuild-design-v2-proposal.md` | `superseded_for_implementation`として履歴保持 |
| 外部`DATA_ROOT` | 削除、移動、書込みのいずれも行っていない |

## 撤回しなかった既知の残余

`tools/development/work4a_rebuild.py`と`tests/test_work4a_rebuild_e2e.py`（v1試作、`c4bfb57`）は
今回の承認範囲外のため残している。`DEC-WORK4A-REBUILD-DESIGN-002`および`-003`により
実装正本でもactual artifactの根拠でもなく、v3実装はこれらを参照・import・拡張しない。
処分はHumanの別判断とする。

## 影響

- `tests/test_work4a_rebuild_v2_e2e.py`の4件が消える。v3 RED testを作るまでWork 4A v2系のtestは0件になる。
- 全test件数は削除分だけ減る。revert後に公式runnerで全testを実行し、receiptを固定する。
- 一括resetは使っていない。対象は上表の2 fileだけである。
