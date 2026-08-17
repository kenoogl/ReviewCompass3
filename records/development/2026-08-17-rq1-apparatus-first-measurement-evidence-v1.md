# RQ1装置 実装・初回計測 Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 作業票：`docs/development/2026-08-17-rq1-apparatus-work-ticket-v1.md`（v1承認・2026-08-17）
- 上位計画：評価データ取得計画v1 §3優先1a・§4順序2

## 1. 実装【実測】

- 正式再利用検索：計画`records/development/2026-08-17-rq1-apparatus-reuse-search-plan-v1.json`
  （先行commit `af588fa`）→`status: completed`・**`start_allowed: true`**・直接一致13件。
  証明書`records/development/2026-08-17-rq1-apparatus-reuse-search-attestation-v1.json`
  （commit `b8853fb`）
- RED：`tests/test_rq1_contract_completeness.py`（commit `47c3e41`・6本全失敗・単独終了コード1）
- GREEN：`tools/evaluation/`新設（`rq1_contract_completeness.py`——既存task_contract部品の
  読み取り専用利用・fixture 4群12件の登録形・指標集計・CLI）。commit `0b5424b`。
  装置試験6本＋保護対象`test_first_review_task_contract_e2e.py` 38本＝44本全通過
  （単独終了コード0）。`tools/task_contract/`本体・既存試験は無変更
- 実装中の修正1件：`context_obligations`は義務IDのlist（dict想定が誤り）——注入細工をlist形式へ
  修正（GREEN内・記録のため明示）

## 2. 初回計測【実測・要約JSONの転記】

実行：`.venv/bin/python3 -m tools.evaluation.rq1_contract_completeness --base-dir <一時領域>`
（単独終了コード0）

```json
{"false_stop_rate": 0.0, "negative_detection_rate": 1.0, "obligation_to_plan_coverage": 1.0, "regeneration_match_rate": 1.0, "requirement_to_obligation_coverage": 1.0}
```

fixture 12件（normal 3・missing 3・conflict 3・stale 3）の観測内訳：

| fixture | 観測 | 検出経路 |
| --- | --- | --- |
| normal-full-binding／partial-binding／alt-document | succeeded（3/3） | ——（誤停止0） |
| missing-definition-file／definitions-directory | stopped | bind段`schema_violation`（定義不在） |
| missing-contract-section | blocking | compile段`contract_section_missing` |
| conflict-unknown-requirement | stopped | bind段`unreceived_obligation` |
| conflict-unknown-allowed／orphan-obligation | blocking | compile段`unreceived_obligation`（被覆検査） |
| stale-binding-tamper／contract-tamper | blocking | seal照合`content_digest_mismatch` |
| stale-definition-rewrite | blocking | 再束縛比較`binding_drift` |

- 異常なし（負値・分母0なし）。negative 9件は**全件が実行前検査で検出**され（検出率1.0）、
  正常3件に誤停止なし（誤停止率0.0）。compile再生成はbyte一致×3回で全件一致（決定性の実証）。
- 本値は**fixture初版に対する装置の健全性確認**であり、論文のRQ1本計測（fixture拡充後）の
  baselineとなる。

## 3. 受入条件との対応（作業票v1 §5）

1. 正式検索証明書：充足（`start_allowed: true`・commit `b8853fb`）
2. RED：充足（`47c3e41`・単独終了コード1）
3. GREEN：充足（`0b5424b`・44本・単独終了コード0）
4. 初回計測：充足（§2の転記・異常なしの機械確認）
5. commit・移行検証：完了報告時に最終確認

## 4. 未実施

- fixture拡充（本計測に向けた類型追加）・RQ2装置（順序4）・reviewer接続（順序3）。
- TODO・見取り図への反映。
