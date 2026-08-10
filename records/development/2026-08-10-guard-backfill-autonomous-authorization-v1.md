# Human裁定：group B〜Dの自律実行の包括承認

- 裁定日：2026-08-10
- 裁定者：Human（kenoogl）
- 裁定文言（原文）：「組BからDまで自律的に実行。停止条件に触れたときと、修正の承認が
  要るときだけ止めよ」

## 1. 本裁定が与える承認

group B・C・Dの各修正単位について、次を**事前に**与える。単位ごとの個別確認は不要。

1. risk `high`の確定。
2. 各単位の着手承認。
3. 各単位のRED開始承認。
4. GREEN着手承認、レビュー依頼の送付。

## 2. 本裁定が与えていない承認（引き続きHumanで停止する）

1. **各範囲固定の停止条件**（scope §8相当）に触れた場合。特に、
   - 変更可能path以外の変更が必要になった場合
   - 上流設計・config・schemaの変更が必要と判明した場合
   - 既存台帳・既存recordの再計算や移行が必要と判明した場合
2. **修正の承認**——次の2種。
   - RED以後のtest変更（理由の記録を伴う）
   - 完了レビューでblocking Findingが出た場合のcode・test修正
3. 上記以外で、Human境界（意味的裁定）に当たる判断が必要になった場合。

## 3. 進め方

裁定record `records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md`
（commit `4bb1c9b`）の順序どおり B → C → D。1 groupにつき1修正単位で、各単位は
範囲固定 → `high`範囲レビュー（Codex）→ RED → GREEN → 完了レビュー → Closerを踏む。
範囲レビューで要修正となった場合、Pilotはscope改訂版を作って再レビューする
（Human停止は§2に該当する場合のみ）。

## 4. 対象（未修正17件）

| group | 対象module | blocking |
| --- | --- | ---: |
| B 公式検証oracle | `policy_test_runner.py`・`pytest_summary.py`・`declaration_red_map_check.py`・`work_unit_transition.py` | 5 |
| C 現在地正本 | `todo_handoff.py`・`todo_update_path.py` | 5 |
| D 実行・台帳境界 | `structured_argv_executor.py`・`issue_intake_v4.py`・`layout/baseline.py` | 7 |
