# Human裁定：守り役後追いレビューの優先度確定と実施範囲（deferred #6）

- 裁定日：2026-08-10
- 裁定者：Human（kenoogl）
- 裁定文言（原文）：「優先度案を承認。まず高19件のみ実施。6件も安全側で含める」
- 前提record：
  - 一覧：`records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md`
    （SHA-256 `77b6ba9fc0bfd7ea17e071dc4e4df59e12f84f4a7d23798dedafe58b6ea6571e`、
    完了レビューv2 `verified`：`0768a9f`）

## 1. 裁定の確定内容

1. **優先度の確定**：一覧record §4・§5のPilot優先度提案（高19・中50・低15）を
   そのまま確定する。
2. **実施範囲**：後追いレビューは**優先度「高」の19 moduleのみ**実施する。
   「中」「低」は保留（別途Human裁定があるまで実施しない）。
3. **要Human判定6件の確定**：安全側ですべて**守り役該当**として扱う。
   - 一覧で暫定「該当」だった3件は判定確定：`bootstrap/review_pipeline.py`（中）・
     `development/policy.py`（中）・`session_logs/pipeline.py`（中）。
   - 一覧で暫定「非該当」だった3件は該当・区分③へ変更し、優先度を次のとおり
     定める（Pilot提案、いずれも本裁定の「高のみ実施」により保留側）：
     `bootstrap/review_cli.py`（中）・`session_logs/source_kind.py`（低）・
     `extraction/known_positives.py`（低）。

## 2. 確定後の集計（一覧record §7からの差分）

- 守り役該当 91 → **94**、非該当 42 → **39**
- 区分③（後追い対象）84 → **87**（高19・中51・低17）
- 実施対象：**高19件**（一覧record §5(a)〜(e)の列挙どおり。本裁定で追加された
  moduleに「高」は無く、19件の構成は不変）
- 要Human判定：0件（全件確定）

一覧record v1は完了レビューv2で`verified`となったsnapshotとして不変のまま保持し、
本裁定recordを差分の正とする。

## 3. 実施方法（確認済み事項の再掲）

高19件は1件ずつ（または同種group単位で）現行体制の独立レビュー
（Pilot fixtureに無い反証の機械実行を含む）にかける。blocking findingが出た場合の
code修正は、都度Human承認を得た別単位（守り役codeの修正は既定`high`）で行う。
