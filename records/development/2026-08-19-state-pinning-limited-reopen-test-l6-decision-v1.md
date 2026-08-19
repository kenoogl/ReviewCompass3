# 状態固定試験の対象限定再開（test_l6の意図保存修正） Human判断record v1

- 判断日：2026-08-19
- 判断者：利用者（Human）
- 記録者：Claude
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`（**状態は`registered`のまま変更しない**。
  同Issueの既裁定「状態固定試験の変更・削除の前にだけ対象限定で再開する」に基づく再開）
- 前例：`records/development/2026-08-18-roots-module-pin-addition-decision-v1.md`（対象限定再開の型）

## 1. 承認文言【記録】

> 対象限定再開を承認。test_l6を終端対応へ意図保存修正

（2026-08-19 chat）

## 2. 対象の限定【判断】

- 変更するのは`tests/test_issue_intake_v4.py::test_l6_repository_issue_set_is_consistent`の
  **1箇所**（`assert len(stored) == len(effective)`）だけ。
- 修正は**意図保存**：試験の目的（issue集合とdecision集合の整合・会話記録issueの内容保護・
  active数0）は全て維持し、「保存された全issueは非終端」という**当時の状態の焼き込み**だけを
  「保存数＝有効（非終端）＋終端」の整合式へ置き換える。
- 本再開は本recordと当該修正のcommitをもって**閉じる**。Issue本体の後続（状態固定試験の
  全体整理）は従前どおり合図待ち。

## 3. 根拠【実測】

- `test_l6`が`assert 8 == 5`で不合格（2026-08-19）。原因は同日の突合裁定（3件をresolvedへ）に
  よる終端状態の**正当な初出現**。終端状態（resolved／rejected）はconfig v4の設計に元々あり、
  `validate_v4_issue_repository`は終端を有効集合から除く設計。
- 同型の焼き込みは同日の自作試験（`test_real_repository_counts_issues`の`registered>=8`）でも
  発生し、内訳の焼き込みを排した形へ修正済み（こちらは当日新設の試験のため本再開の対象外）。

## 4. 未実施

修正の適用と全群green確認・Evidence・commit（本record直後）。
