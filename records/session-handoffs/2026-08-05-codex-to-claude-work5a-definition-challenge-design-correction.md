# Codex → Claude：Work 5A Definition Challenge設計の循環修正指示

## 指摘

`docs/design/2026-08-05-work5a-definition-challenge-proposal.md`には、設計上の循環がある。

- §1・§4.3はDefinition Challengeをcompileより前に実施すると定める。
- しかし§1・§2.1・D5は、compile後にしか作れない`plan_bundle`をDefinition Challengeの入力に要求する。

このままでは「Definition Challengeに通るためにPlan bundleが要るが、Plan bundleを作るためにDefinition Challengeが要る」
という循環になる。実装、RED、承認へ進まない。

## Claudeが行うこと

既存の設計提案を**第四版として修正**する。新しい提案文書やDecision recordは作らない。

1. Definition Challengeの入力を、compile前に固定できる材料だけへ直す。
   - Requirement definition、review task contract、開発方針、Current Plan、固定material setは使える。
   - `plan_bundle`、Finding集合、Conformance verdict、Final Challenge verdictは入力に使わない。
2. D5のowner分離を、compile前に検査できるContract fieldへ移すか、compile後の別検査へ移すかを明確にする。
   - Definition Challengeの入力へPlan bundleを戻してはならない。
3. Definition Challengeを必須にする新しいContract versionと、既にacceptedなContract version 1の関係を固定する。
   - version 1のrecordを上書き、無効化、後付け変更しない。
   - 新形式がContract version 2を必要とするなら、その理由、stale範囲、初回実Runの順序を明記する。
4. 修正後の正常経路を、循環なしで一行の順序として示す。
   - 例：Requirement／Contract v2／Definition Challenge／compile／…
5. 受入条件、Human判断、実施単位を上記の順序へ合わせる。

## 禁止事項

- 実装、test、TODO、Current Plan、checklist、Requirement、Decision recordを変更しない。
- Challenge Policy、risk catalog、隣接Contractを推測で新設しない。
- Issue Intake候補やIssue Intake設計指示に触れない。

## 検証・報告

- `git diff --check`と、修正後に`plan_bundle`がDefinition Challenge入力へ残っていないことを確認する。
- 修正した設計文書一件だけを一つのコミットにする。
- 完了報告はコミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-definition-challenge-design-correction.md`
