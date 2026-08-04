# Work 4A v1 Prototype Removal Map v1

## Purpose

Work 4A v1試作の撤去範囲を、commit subjectではなくpathで示す。
過去commit全体はrevertせず、現在のfileだけを削除する。

## 承認

`DEC-WORK4A-REBUILD-DESIGN-003`の範囲外として保留していたv1試作について、
2026-08-04の会話でHumanが撤去を承認した。

> 承認する。v1試作の撤去を承認する。
> 対象は tools/development/work4a_rebuild.py と
> tests/test_work4a_rebuild_e2e.py の削除だけとする。
> 過去コミット全体はrevertせず、現在のTODOとチェックリストは維持すること。

## 撤去範囲

| 削除したpath | 行数 | 由来commit |
| --- | --- | --- |
| `tools/development/work4a_rebuild.py` | 290 | `c4bfb57` Implement Work 4A identity chain |
| `tests/test_work4a_rebuild_e2e.py` | 280 | `377c610` Define Work 4A rebuild acceptance |

削除前に、この2 file以外からの参照が無いことを機械確認した。
参照は`tests/test_work4a_rebuild_e2e.py`自身のimportと、v2 revert mapの記述だけであった。

## 撤去しなかったもの

| 対象 | 理由 |
| --- | --- |
| `c4bfb57`、`377c610`を含む過去commit | 承認範囲外。historyは書き換えず、revertもしない |
| `TODO_NEXT_SESSION.md` | v3の現在値を維持する。後退更新しない |
| `docs/development/2026-08-03-initial-development-checklist.md` | v3 authorityの現在値を維持する |
| `docs/design/2026-08-04-work-4a-rebuild-design-proposal.md`（v1設計） | 履歴として保持する |
| 外部`DATA_ROOT` | 削除、移動、書込みのいずれも行っていない |

## 影響

- v1 E2E test `4件`が消える。撤去前の全testは685件、撤去後は681件になる。
- v3実装（`tools/development/work4a_rebuild_v3.py`）はv1を参照・importしていないため、機能への影響はない。
- これによりWork 4Aの試作moduleはv3だけになり、誤った参照モデルを実装したcodeはworking treeから無くなった。

## 現在の停止点

外部`DATA_ROOT`の初期化、実データの観測、候補routineの選定は実施していない。
これらはHumanの個別承認を待つ。
