# 運用集計コマンド（評価データ取得計画 順序5）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「順序5（運用集計コマンド）に着手してください。まず範囲固定
  文書から」（2026-08-18 chat。裁定「執筆と並行」は論文計画v2 §1判断4）
- 記録者：Claude
- 上位計画：評価データ取得計画v1 §3優先2・§4-5（SHA-256はTODO Evidence欄で固定済み）。
  復元可能性表`records/development/2026-08-17-evaluation-recoverability-map-v1.md` §3が入力の正
- 基準commit：`59d6c4c`（作業tree clean）
- 必読入力の適用：本件は既存recordとlaunch計測メタの機械集計のみ（LLM読み書き・外部送信なし）。
  文字列理解原則の対象外だが、fail-closed（未知形式は数えず件数報告）は設計へ取り込む

## 1. 手順1〜2：入力の所在と実測

| 入力 | 所在 | 実測（2026-08-18） |
| --- | --- | --- |
| launch計測メタ | `/Users/keno/.reviewcompass3-private/reviewer-launch/<run>/launch.json` | 49実行。`elapsed_seconds`あり＝**31**（rq2系・順序1のcommit `b33b72b`以後）、なし＝**18**（cr-011〜014・e2e系＝計測メタ導入前） |
| H7承認点 | `records/development/*.md`の「承認文言」欄 | **46 file**（grep実測） |
| H4手動記入（placeholder） | `<<記入:`はrequest-builder系の資材にのみ存在。旧依頼record（session-handoffs）は0件 | 対象母集団の特定に request-builder 資材の精査が要る |
| H5束縛表 | 受入判断recordの束縛表 | 表記が record ごとに揺れ、正準形の特定が要る |
| コスト（道具呼び出し） | セッションログ保全先 | 時系列parser新設が要る（最重量） |

## 2. 手順4：接続点と範囲の判断

復元可能性表§3の従軸5系統のうち、**機械集計の形が今日の記録から一意に定まるのは2系統**
（launch実測・H7承認点）。残り3系統（H4手動記入・H5・コスト）は母集団特定または新parser設計が
先に要る。段階構成とし、v1は2系統を確実に固定して残りを明示繰り越しする（論文計画v2 §1判断4
「数字が出れば該当章を厚くする」に整合。作業票§3・§5）。

- 新設module：`tools/evaluation/operational_metrics.py`（集計装置の既存置き場。
  `rq2_paired_trial.py`と同格）。一行JSON・終了コード0／2の repo 規約に従う。
- dataset固定：実行出力を`records/development/2026-08-18-operational-metrics-dataset-v1.json`
  へ新版固定（論文計画v2 §4の「装置による再集計・新版record」規則）。
- 保護：既存試験への影響なし（新設のみ）。root解決は`tools/common/roots.py`（本日一元化）を使う。

## 3. 手順3：digest表【実測】

```text
890996191d60ec6ea49742345ac60599071aa88ea3cbc5070e051d2f6d4dbd25  tools/evaluation/rq2_paired_trial.py
478476817a5fcc755c7e96f33cfe2a68f093e0a4dd26ae3405cbac2ff8d33791  tools/common/roots.py
```

## 4. 手順5：正式再利用検索

作業別計画の先行commit後に実行し、証明書を
`records/development/2026-08-18-operational-metrics-reuse-search-attestation-v1.json`へ固定する。

## 5. 未実施

- 手順5の実行、作業票の適用、RED、GREEN、dataset固定、Evidence、TODO反映。
