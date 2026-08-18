# 運用集計コマンド（順序5）実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「順序5（運用集計コマンド）に着手してください。まず範囲固定
  文書から」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-operational-metrics-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-operational-metrics-prescan-v1.md`
- 基準commit：`59d6c4c`→文書commit `7c85dfa`→証明書commit `17151ef`→実装は本recordと同一commit

## 1. 成果物

| file | 内容 | SHA-256 |
| --- | --- | --- |
| `tools/evaluation/operational_metrics.py`【新設】 | launch実測の分計＋承認点分布の集計装置（一行JSON・0／2・fail-closed） | `ff5b26e3ab3c6fa7ead6214d302b7cd500e7bfbd2a456c0c0bcc45897c38511c` |
| `tests/test_operational_metrics.py`【新設】 | 分計・統計値・日付分布・一行JSON・終了コード・`-m`疎通の5本 | `1efd0c8f09df8e18d77dcb69c48ce85e97324e6846c84df109334968f8e29c0e` |
| `records/development/2026-08-18-operational-metrics-dataset-v1.json`【新設】 | 実データ集計の固定（装置出力そのまま・転記なし） | `6a85d7d87239bdc17afbad3459c9bdca52d1402cbfc0137039388fb3619cdd25` |

## 2. RED→GREEN【機械出力の転記】

- RED：`5 failed`・単独終了コード**1**（module未存在）。
- GREEN：新設5件・roots 6件・RQ2装置14件——各単独終了コード**0**。
- 一元化の維持：`grep -rn "parents\[" tools/ --include="*.py"`＝`tools/common/roots.py`の1件のみ。
- `git diff --check`＝合格。

## 3. 実データ集計（dataset v1の要旨）

実行：`.venv/bin/python3 -m tools.evaluation.operational_metrics --launch-root
/Users/keno/.reviewcompass3-private/reviewer-launch`（records-rootは既定＝`records/development`）・
終了コード0。

- **launch実測（H4）**：instrumented **30**・legacy **18**・skipped **0**（計48実行）。
  `elapsed_seconds`＝最小37.78・中央値65.44・平均78.35・最大182.95・合計2,350.42秒。
  `prompt_bytes`＝最大1,626・平均1,624.4（30実行）。
- **承認点（H7）**：**47** record・日付分布は2026-08-05〜08-18（ピーク08-17＝22件）。

## 4. 手戻りの記録（正直な記載）

1. **事前走査§1の母数「49実行・あり31」は誤り**。RQ2 datasetの「31実行の機械記録」（実起動30回
   ＋起動前停止1件）をlaunch保存数と混同した**推測転記**で、grep相当の全件機械計数をしなかった。
   機械実測は**48実行（30＋18）・skipped 0**（`ls -d`計数48・rq2系dir 30・メタ欠落0で照合済み）。
   作業票の受入条件3「母数49（31＋18）」も同じ誤りを継承していた。条件の意図（実データ全件が
   分計に入り取りこぼしがない）は48＝30＋18・skipped 0で満たす。
2. **承認点の母数は事前走査grep実測46に対し実行時47**。差1件は事前走査record自身が「承認文言」
   の文字列を含むため（計測が計測対象に入る自己言及）。dataset定義は「文字列を含むrecord数」の
   まま正とし、意味解釈（欄としての承認のみ数える）はv2の論点とする。

## 5. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED単独非0 | 合格（exit 1） |
| 2 | GREEN各単独0（新設・roots・RQ2装置） | 合格 |
| 3 | 実データ実行0・母数一致 | **条件文の数値を訂正のうえ合格**（§4-1。48＝30＋18・skipped 0・承認点47） |
| 4 | dataset v1固定・digest機械転記 | 合格（§1・§3） |
| 5 | 証明書`start_allowed: true` | 合格（commit `17151ef`・直接一致2件＝`roots.repo_root`ほか。新設の妥当性に反例なし） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 6. v2へ繰り越し（作業票§3の再掲）

H4手動記入（placeholder律）・H5（束縛表照合）・コストとH4 assemble/check近似（セッションログ
時系列parser）。承認点定義の意味解釈（§4-2）。

## 7. 未実施

- TODO反映とcommit。push（従前どおり）。論文原稿への取り込み（執筆スレッドの領分）。
