# Claude → Codex：読み取り専用argv executor最小sliceの実装 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-read-only-argv-executor-slice.md`

承認された読み取り専用argv executor最小sliceだけを、3つの意味的commitで実施した。**停止はしていない。**

## commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 1 承認記録 | `abb066f19fa0e0f39bd11ae50f31a4ca6b627134` | Decision、Plan状態注記、TODO、approval receipt（code／testを含まない） |
| 2 RED | `752b50931bd81561b6a74fbe85865af475afcb26` | 受入test、RED Evidence（実装を含まない） |
| 3 GREEN | `fbaa170634b283244b1b1a425a39a86ab9e4c432` | 実装module、test調整、GREEN Evidence、GREEN receipt、TODO |

各commitは明示pathだけをstageした。`git add -A`と`git add .`は使っていない。
commit後の`git status --short`は空、
`python3 tools/development/work_unit_transition.py --work-status completed`は
`{"findings": [], "next_work_allowed": true, "reminder": null, "status": "passed"}`。

## 変更file

| commit | file |
| --- | --- |
| 1 | `records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-decision-v1.md`（新規）、`docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md`（状態注記の追記）、`TODO_NEXT_SESSION.md`、`records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-test-receipt-v1.json`（新規） |
| 2 | `tests/test_structured_argv_executor.py`（新規）、`records/development/2026-08-05-machine-operation-routing-read-only-argv-red-evidence-v1.md`（新規） |
| 3 | `tools/development/structured_argv_executor.py`（新規）、`tests/test_structured_argv_executor.py`（拒否層の明示）、`records/development/2026-08-05-machine-operation-routing-read-only-argv-green-evidence-v1.md`（新規）、`records/development/2026-08-05-machine-operation-routing-read-only-argv-green-test-receipt-v1.json`（新規）、`TODO_NEXT_SESSION.md` |

## RED／GREEN

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_structured_argv_executor.py` | `13 errors`（module不在） | `13 passed` |
| `tests/test_operation_routing_v2.py`（既存、無変更） | — | `23 passed` |
| 公式policy runner suite `full` | — | **`905 passed`** |

receiptの対応。

| receipt | SHA-256 | 集計 |
| --- | --- | --- |
| 承認記録時点 | `85f411ad3083ee7580e140dce3d0c858bebf4ad1e3ae3a2c032ce9122f5d0d39` | `passed 892／total 892` |
| GREEN | `f7eaf735fb0dde4e0d96bc9dcb53b5af522faa7cf784d34d788b8de81cbe59d2` | `passed 905／total 905` |

差の13件は今回追加したtestである。

## Decision

`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`
（`records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-decision-v1.md`、
SHA-256 `2982646b43a74d856d9b18af527b743b10ac3d8874f03ee39afba825752a8864`）。

Humanの承認文言、承認範囲、対象外、参照入力6件のpathと作成時SHA-256を記録した。
後続Plan提案には実施状態注記を追記し、Plan全体は`awaiting_human_approval`のままで、
§2.1と§3.2のargv executor最小sliceだけが実装承認済みであることを明記した。

## 実装の要点

- argvは**listのまま**runnerへ渡す。shell文字列へ組み立てない。診断文でも結合しない
  （`repr(argv[:4])`を使う）。
- 起動できるのは、inventory全操作が`read_only`で、argvが`git status --porcelain`＋任意の
  `-- <pathspec...>`に一致する場合だけである。
- inventory／preflight／receiptは既存`operation_routing`のまま。executorは権限を判定・付与・
  再分類しない。`read_only`だけのinventoryでは必要権限も付与済み権限も空のままであることをtestで固定した。
- cwdはproject root基準の相対pathだけ。絶対path、`..`、外への解決、symlink、不在、通常fileを拒否する。
- 停止code：`inventory_not_read_only`、`template_mismatch`、`argv_invalid`、`cwd_invalid`、
  `runner_result_invalid`。既存routingのcodeはそのまま伝える。**いずれの停止でもrunnerを一度も呼ばない。**
- processの失敗（非0終了）は例外にせずreceiptへ`failed`として記録し、入力検証の失敗と区別する。
- **既定のrunnerを持たない。** 実processを起動するのは、呼出し側が`subprocess_runner`を明示的に
  渡した場合だけである。

## 実装中に決めたこと（GREEN Evidenceに詳細）

1. 空のargv listと非文字列要素は、executorへ届く前に既存inventory validatorが`inventory_invalid`で
   拒否する。testの期待を実際に拒否する層へ合わせた。保証（拒否され、runnerを呼ばない）は変えていない。
2. 診断文でもargvを文字列へ結合しないよう`repr`へ変更した。
3. 既定runnerを持たせず、明示的に渡した場合だけ起動する形にした。

## validator結果

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| compaction validator | 合格（11,741 bytes、active ID 1件） |
| 参照整合 | 26件一致（機械計測。TODOの記載件数も同値へ更新） |
| `git diff --check` | 各commitのstage前後で合格 |

TODOが上限を超えたため、更新規則に従って累積していた中間Evidence linkを3行整理した。

## 未実施範囲（承認範囲外のまま）

- cache rootの決定的な固定。次の別sliceのままである。
- 既存の直接操作の移行、移行inventoryの作成、既存call siteの置換。
- Git metadata書込み、project成果物書込み、external操作の起動。
- 環境変数の設定。
- host側tool構文、外部送信。**project内で解決したとは書いていない。**
- `git status --porcelain`以外の実行template。
- Issue recordのstate、Task Contract、policy、config、既存Decision、既存testの変更。
  `ISSUE-HTC-C9F6C917`は`registered`のままで、`tools/development/operation_routing.py`も無変更
  （SHA-256 `0fb5636feac3e12c42104830cd710bdb2a6f9398b784edf211c57128e1cd9178`）。
- push、tag、amend、rebase、reset、force push、履歴書換え、外部送信、hook、watcher、scheduler。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。
