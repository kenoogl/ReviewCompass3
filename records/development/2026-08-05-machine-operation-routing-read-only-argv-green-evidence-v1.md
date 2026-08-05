# 読み取り専用argv executor最小slice GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-C9F6C917`
- 承認：`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`
  （`records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-decision-v1.md`）
- RED Evidence：`records/development/2026-08-05-machine-operation-routing-read-only-argv-red-evidence-v1.md`
  （SHA-256 `b7d5dd188bbd8151074283e96240045d560e98fc241aed49d88c7a4386228190`）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-read-only-argv-executor-slice.md`

## 1. 実施内容

`tools/development/structured_argv_executor.py`を新規作成した。

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 実装module | `tools/development/structured_argv_executor.py` | `c697c9804ff5decdf21530744c97752b564bb42a895bcb2544dec2d81ea206ea` |
| 受入test | `tests/test_structured_argv_executor.py` | `9166e680d6c1b528163df23e5ecb0852c5fdf614875818737a265bc49760b9ff` |

### 何をするmoduleか

argvを**配列のまま**渡して読み取り専用操作を起動する。起動できるのは、次の両方を満たす場合だけである。

1. inventoryの全操作が`read_only`であること。
2. 各操作のargvが`git status --porcelain`＋任意の`-- <pathspec...>`に一致すること。

inventory、preflight、receiptは既存の`operation_routing`をそのまま使う。executorは権限を
判定・付与・再分類しない。`read_only`だけのinventoryでは必要権限が空になり、executorはそこへ
何も足さない。

### 停止codeと責任の分担

| 停止code | 誰が拒否するか |
| --- | --- |
| `inventory_invalid`、`inventory_digest_mismatch`、`host_attestation_invalid`、`approval_required` | 既存の`operation_routing`（そのまま伝える） |
| `inventory_not_read_only` | executor（分類が`read_only`以外） |
| `template_mismatch` | executor（template外のargv） |
| `argv_invalid` | executor（空の実行fileなど） |
| `cwd_invalid` | executor（絶対path、`..`、外への解決、symlink、不在、通常file） |
| `runner_result_invalid` | executor（runnerの戻り値に`returncode`が無い等） |

いずれの停止でも**runnerを一度も呼ばない**。

### runnerの契約

`runner(argv, cwd=cwd)`。`argv`はlist、`cwd`は検証済みの絶対pathである。
**既定のrunnerを持たない**。実processを起動したい場合だけ、呼出し側が`subprocess_runner`を
明示的に渡す。`subprocess_runner`はargvをlistのまま渡し、shellを経由しない。

## 2. 結果

| command | 結果 |
| --- | --- |
| `.venv/bin/python3 -m pytest -q tests/test_structured_argv_executor.py`（RED時） | `13 errors`（module不在） |
| 同（GREEN時） | `13 passed` |
| `.venv/bin/python3 -m pytest -q tests/test_operation_routing_v2.py` | `23 passed` |
| 公式policy runner suite `full` | `905 passed` |

receiptの対応。

| receipt | SHA-256 | 集計 |
| --- | --- | --- |
| `records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-test-receipt-v1.json` | `85f411ad3083ee7580e140dce3d0c858bebf4ad1e3ae3a2c032ce9122f5d0d39` | 承認記録時点。`passed 892／total 892` |
| `records/development/2026-08-05-machine-operation-routing-read-only-argv-green-test-receipt-v1.json` | `f7eaf735fb0dde4e0d96bc9dcb53b5af522faa7cf784d34d788b8de81cbe59d2` | GREEN時点。`passed 905／total 905` |

差の13件は、今回追加した`tests/test_structured_argv_executor.py`の13 testである。

## 3. 判断（実装中に決めたこと）

### 3.1 拒否する層を、testの期待に合わせて明示した

RED時、空のargv listと非文字列要素は、executorへ届く前に既存の`operation_routing`の
inventory validatorが`inventory_invalid`で拒否することが分かった。executor独自の`argv_invalid`は、
inventory validatorを通過する「空文字列の実行file」で機能する。

testの期待を、実際に拒否する層へ合わせた。**保証は変えていない**。いずれの場合も拒否され、
runnerは一度も呼ばれないことをtestで確認している。二重に同じ検証を持たせるより、
先に走る層の結果をそのまま伝えるほうが、停止codeの意味が一つに定まる。

### 3.2 診断文でもargvを文字列へ結合しない

`template_mismatch`の詳細に`" ".join(argv[:4])`を使っていたが、これはshell文字列ではないものの
「argvを文字列へ結合する」書き方である。source inspection testの趣旨に合わせ、`repr(argv[:4])`へ
変更した。listの形のまま示すため診断の情報量は落ちていない。

### 3.3 既定runnerを持たせなかった

実processを起動するrunnerを既定にすると、testや誤用で意図せず起動しうる。既定は持たせず、
`subprocess_runner`を明示的に渡した場合だけ起動する形にした。承認範囲（起動経路の提供）は満たしつつ、
既定で何も起動しない。

## 4. 未実施（承認範囲外のまま）

- cache rootの決定的な固定。次の別sliceのままである。
- 既存の直接操作の移行、移行inventoryの作成、既存call siteの置換。
- Git metadata書込み、project成果物書込み、external操作の起動。
- 環境変数の設定。
- host側tool構文、外部送信。**project内で解決したとは主張しない。**
- `git status --porcelain`以外の実行template。
- Issue recordのstate変更、Task Contract、policy、config、既存Decision、既存testの変更。
  `ISSUE-HTC-C9F6C917`は`registered`のままである。

## 5. 既存への影響

既存testは1件も変更していない。`tests/test_operation_routing_v2.py`は`23 passed`のままである。
`tools/development/operation_routing.py`も変更していない
（SHA-256 `0fb5636feac3e12c42104830cd710bdb2a6f9398b784edf211c57128e1cd9178`）。
今回のsliceは新規moduleと新規testの追加だけである。
