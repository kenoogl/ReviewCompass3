# Human裁定：守り役後追いレビュー指摘26件の修正順序

- 裁定日：2026-08-10
- 裁定者：Human（kenoogl）
- 裁定文言（原文）：「推奨案で」
  （Pilot推奨＝「組E（外部送信・機密）→ 組A（共通の土台）→ 組B・C・D の順で、
  組ごとに危険度『高』の修正単位を立てる」に対する承認）

## 1. 前提（#6第2単位の結果）

高19 moduleの独立レビューで、18 moduleが`reported_unverified`、blocking Finding
合計26件。合格は`tools/session_logs/private_validation.py`の1件のみ。

| group | 判定record | commit | blocking |
| --- | --- | --- | --- |
| A 共通正本 | `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-a-v1.md` | `17613d2` | 2 |
| B 公式検証oracle | `…-group-b-v1.md` | `46f2465` | 5 |
| C 現在地正本 | `…-group-c-v1.md` | `f02c32c` | 5 |
| D 実行・台帳境界 | `…-group-d-v1.md` | `e0e5d33` | 7 |
| E 外部送信・機微境界 | `…-group-e-v1.md` | `8a7da31` | 7 |

## 2. 確定した進め方

1. **修正順序**：E → A → B → C → D。
   - Eを先頭にする理由：外部送信・機微境界の欠陥は情報漏えいに直結する。
   - Aを次にする理由：digest・path境界は他の全moduleが依存する共通正本であり、
     先に直すと後続groupの修正が単純になる。
2. **単位の粒度**：**1 groupにつき1修正単位**とする。各単位は既定`high`
   （守り役codeの修正）であり、着手のたびにHumanのrisk確定と承認を要する。
3. **各単位の手順**：範囲固定 → `high`範囲レビュー（Codex）→ Human裁定 →
   RED（反証testのみ）→ GREEN（実装）→ 完了レビュー（Codex）→ Closer。
4. **未修正の保持**：着手していないgroupのFindingは判定recordのまま保持し、
   一括修正・先取り修正は行わない。

## 3. 本裁定が決めていないこと

- 各単位内の細目（修正方式の選択、slice分割、新しい方針値の採否）は、
  各単位の範囲固定でPilotが提案し、Humanが確定する。
- レビュー基準・上流設計の変更は含まない（既存authorityへの適合修正のみ）。
