# 運用集計v2（H5束縛表・承認点定義）実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「運用集計v2（H5束縛表など）に進んでください」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-operational-metrics-v2-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-operational-metrics-v2-prescan-v1.md`
- 基準commit：`e69a322`→文書commit `337dd56`→証明書commit `bd76852`→実装は本recordと同一commit

## 1. 成果物

| file | 内容 | SHA-256 |
| --- | --- | --- |
| `tools/evaluation/operational_metrics.py`【拡張】 | 集計3（H5束縛照合）＋`field_count`＋schema_version 2 | `f7d550ab269c28f1f84ef49badeea7de8457147506cb9aeff7293e069874d786` |
| `tests/test_operational_metrics.py`【拡張】 | 追加4本（束縛3分類・採点外計上・欄形式計数・schema 2）＝計9本 | `ea52bdba20d3dde2a479a4c95e1defbebbadc561c825828ad78fedcc74d6b722` |
| `records/development/2026-08-18-operational-metrics-dataset-v2.json`【新設】 | 実データ集計の固定（装置出力そのまま。v1は不変＝digest再計算一致） | `d39fbf1f641ae426a63736856cb99d7c3e02620894aae517c6c7e13ee476c0fd` |

## 2. RED→GREEN【機械出力の転記】

- RED1：追加4本失敗・既存5本緑・単独終了コード1。RED2（欄形式の定義漏れ是正）：見出し形式の
  追加試験1本失敗→正規表現拡張で緑。
- GREEN：9本緑・`tests/test_common_roots.py`・`tests/test_rq2_paired_trial.py`・
  `tests/test_shared_function_sweep.py`各単独終了コード0。`git diff --check`合格。
- 再利用：digest計算は`tools.common.digests.file_sha256`を束ね直し（複製禁止の掃引に適合）。

## 3. 実データ集計（dataset v2の要旨）

- **H5束縛照合**：走査686 record・採点対象268組——**一致208（77.6%）・不一致59（22.0%）・
  file欠落1（0.4%）**。採点外＝組の閉じない出現104・総hex出現2,389（書式C＝表cellは v3 対象）。
- **不一致59の定義**：束縛は記録時点のdigestであり、fileの版の前進でも不一致になる。v2は分類
  報告のみで「破損」と断定しない（作業票§5-1）。
- **file欠落1の機械特定**：`2026-08-17-rq2-apparatus-prescan-v1.md`が参照する正解表**v1**。
  v1はpath改訂の**v2へ置き換えられ現存しない**（git履歴には残る。版の前進の実例であり、
  束縛の破損ではない）。
- **承認点**：record_count **49**・**field_count 35**（行頭からmarkdown構造記号だけを挟んで
  `承認文言`が現れる行を持つrecord。箇条書き・見出し両形式を含む）。

## 4. 手戻り・自己言及の記録（正直な記載）

1. `field_count`の初回定義が見出し形式（`## 1. 承認文言【記録】`）を数え漏らした（初回実測7）。
   試験を先に追加（RED）→正規表現拡張→**35**へ是正。定義＝「行頭からmarkdown構造記号
   （箇条書き・引用・見出し・番号）だけを挟んで`承認文言`が現れる行を持つrecord数」。
2. 総hex出現は事前走査実測2,386→実行時**2,389**（＋3＝v2事前走査record自身が含むdigest）。
   承認点も47→**49**（＋2＝v1 Evidence・v2事前走査）。計測が計測対象に入る自己言及は既知の
   性質として毎版明記する。

## 5. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED追加分のみ失敗・既存緑 | 合格（§2） |
| 2 | GREEN各単独0 | 合格（§2） |
| 3 | 実データ実行0・採点対象と総hexの整合 | 合格（268組採点・2,389 hex・差は書式C 1,048と採点外104ほか＝§3） |
| 4 | dataset v2固定・v1不変 | 合格（v1 digest `6a85d7d8…`再計算一致） |
| 5 | 証明書`start_allowed: true` | 合格（commit `bd76852`・直接一致25件＝`file_sha256`等の再利用根拠） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 6. v3へ繰り越し

書式C（表cell 1,048件）の表schema対応・`digest_differs`の履歴照合（git遡り）・H4手動記入・
コストとassemble/check近似（セッションログ時系列parser）。

## 7. 未実施

- TODO反映とcommit。push（利用者の運用に従う）。論文への取り込み（執筆スレッドの領分）。
