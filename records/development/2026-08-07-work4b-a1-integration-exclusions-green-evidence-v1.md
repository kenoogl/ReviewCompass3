# 構成A-1 統合除外宣言 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001`、`DEC-INTEGRATION-EXCLUSION-ENTRIES-001`
- RED Evidence：`records/development/2026-08-07-work4b-a1-integration-exclusions-red-evidence-v1.md`

## 1. 実装

`tools/development/integration_exclusions.py`を新設した。除外宣言recordの検証（必須field、
理由種別4語彙、**Human承認Decision参照の実在とDigest一致**、content digest）、new-only保存、
決定的な除外判定（symbol接頭・module path一致）、fail-closed読み込みを含む。既存moduleは
変更していない。

- targeted：`tests/test_integration_exclusions.py` `5 passed`、exit `0`。固定testは変更していない。
- 公式全Test：exit `0`（1071 passed）。既存Testは弱めていない。

## 2. 実record

`.reviewcompass/workflow/integration-exclusions/integration-exclusions-001--v1.json`
（`RC3-INTEGRATION-EXCLUSIONS-001`、content digest
`7efdce0fb40a7228fd5a3fce90f7eaaee4e0e38a180e456245c50ea868f061fc`）。
承認済み3 entry（E1凍結レーン：旧Pilot固定検証器3関数、E2版固定：Intake v2検証経路、
E3歴史保持：旧37要件移行器）を、裁定Decisionへの参照付きで固定した。

post-write確認【実測】：validator合格、再読込一致、除外判定の正例2件（E1・E3の対象が該当）と
負例1件（現行helperは非該当）を機械確認した。

## 3. これで解決したこと

`DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001` §2が記録した「凍結が機械可読な形でどこにも宣言されて
いない」状態が、本recordにより一箇所の機械可読宣言へ集約された。構成A-2（絞り込み順位表）は
本宣言を機械参照し、該当対象を候補から落とし、落とした件数を表示する。

## 4. 残余と限界

- 除外判定が機械適用できるのはsymbol接頭とmodule path一致のみ。E2（config_lane）はroutine単位の
  機械除外に写像されず、順位表生成時の「経路統合を候補にしない」規則とLLM prompt除外で扱う
  （A-2実装時の宣言に含める）。
- 本helperは順位表の候補脱落を決める守り役codeであり既定`high`。
  `ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`の反証レビュー対象に含める。
- entryの追加・削除は後継versionの候補提示とHuman裁定を経る（承認Decision §3）。
