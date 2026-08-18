# 論文データ台帳 追補 v1（計画v2固定以降のEvidence）

- 記録日：2026-08-18
- 記録者：Claude（**開発スレッド**。計画v2 §3の分担規則＝「論文データの更新は開発スレッドが
  装置で再集計し新版として固定、執筆側は固定版のみ引用」に基づくデータ固定の通知。本追補の
  作成は利用者指示「前回、論文用のレポートに追記して以降のエビデンスを追記する」による）
- 位置づけ：計画v1 §2台帳の**従軸欄（#1〜4＝当時「順序5でこれから」）を実データで埋める追補**。
  v1・v2は不変（新版固定の原則）。digest表は機械生成（転記なし）

## 1. 新規固定Evidence（2026-08-18・計画v2固定以降）

| 内容 | path | SHA-256 |
| --- | --- | --- |
| RQ2採点7語彙の形式判断record（採点方法論の正本所在） | `records/development/2026-08-18-rq2-answer-key-vocabulary-format-decision-v1.md` | `63f74966614251c1ad6a268cb021099df783a591e7149bf2b32086cd228825a9` |
| 運用集計dataset v1（launch実測・承認点） | `records/development/2026-08-18-operational-metrics-dataset-v1.json` | `6a85d7d87239bdc17afbad3459c9bdca52d1402cbfc0137039388fb3619cdd25` |
| 運用集計dataset v2（H5束縛照合の初版） | `records/development/2026-08-18-operational-metrics-dataset-v2.json` | `d39fbf1f641ae426a63736856cb99d7c3e02620894aae517c6c7e13ee476c0fd` |
| 運用集計dataset v3（表cell束縛を追加） | `records/development/2026-08-18-operational-metrics-dataset-v3.json` | `ef79c8e506cd0e276a80a1bb0a8ed17d2d337ce89925ec8c25b107001859ffbb` |
| 運用集計dataset v4（git履歴照合） | `records/development/2026-08-18-operational-metrics-dataset-v4.json` | `faad88327bf4a0a987fb88e8b8eff45a0f55b50d959e6b08a833da33d6cbc8bb` |
| 運用集計dataset v5（H4自動導出率・保全規模） | `records/development/2026-08-18-operational-metrics-dataset-v5.json` | `2b6d9bbe5c99c44eeee08d3e32b9d4718cdc0d6c8fce322f9b604e8f6fdaf186` |
| 運用集計dataset v6（最新固定版：時系列・欠落由来） | `records/development/2026-08-18-operational-metrics-dataset-v6.json` | `94cfd626c817fd084514cdaf4ccedf6b01c94ffb98d7dbfdd8e1b6a1e18e3995` |
| 運用集計Evidence v6（定義と限界の正本・v1〜v5への入口） | `records/development/2026-08-18-operational-metrics-v6-evidence-v1.md` | `ed2a8f8914e01f4a9ef65f1e519a01bbf19e331517725237f1c78e1dd6800e68` |
| LLM／機械分担の精査record（機械化度の記述材料） | `records/development/2026-08-18-llm-machine-split-audit-v1.md` | `4b191e098a100abcb243e66e3c070157e3055c7e10f169513acaf14513c1cbbc` |
| 測定ブロック完全性guard Evidence（測定方法論の記述材料） | `records/development/2026-08-18-measurement-block-integrity-guard-evidence-v1.md` | `0825a5defdbb771939728500822aa228705979b9e5c752cc8dda6e7a2c6252e0` |

## 2. 従軸の数字（執筆用の要旨。引用時はdataset v6を正とし転記後に機械照合）

| 台帳# | 指標 | 実測値（dataset v6） | 対応章（v1 §1） |
| --- | --- | --- | --- |
| #1 | H4自動導出率 | **93.9%**（依頼record雛形の非空33行中、LLM記入欄は2）3類型同値 | §5実用性 |
| #2 | H5追跡可能率 | **95.9%**（束縛1,199組中、一致848＋版の前進298。真の不一致は**13件**） | §7監査性 |
| #2 | 欠落の由来 | 34件＝削除・改名8＋履歴なし23＋絶対path3（全数機械分類） | §7監査性 |
| #3 | H7承認点 | 49 record（欄形式35）・日付分布つき | §5・§7 |
| #4 | コスト | Claude形式系統：560会話・128,150行・**厳密tool_use 28,210回**。保全規模＝8日間で約3.5GB | §6・§7 |

## 3. 方法論の補足（§6採点・§7監査の記述材料）

- 採点7語彙の正本所在は形式判断record（表1）——正解表v2（事前登録・封緘）とは別版を立てない裁定込み。
- 測定は「宣言→機械実行→二重実行一致検査→生成file参照」の機械化鎖で行われ、数値の手書き転記を
  排除している（監査性の実装例として§7で言及可能。定義と限界は各Evidenceが正本）。

## 4. 注記

- 執筆スレッドへ：dataset v6が従軸の最新固定版。数値の転記後は本表のdigestで機械照合すること。
- 開発スレッドの以後の新版（v7以降）は同形式の追補v2として固定する。
