# Codex → Claude：Work 4設計提案のRequirement対応表訂正

## 実行者と対象

**実行者はClaudeである。** Claudeは本ファイルを読み、承認前の設計提案にある一つの数え方の
不整合だけを訂正する。

対象：`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` §7

## 検出した不整合

本文は「直接束縛するRequirementは14件、残り35件」と記すが、対応表には15件の
Requirement IDがある。さらに、本文で`REQ-WORKFLOW-004`を満たすと主張するのに、
対応表と受入条件にその対応がない。

これはHumanの新しい判断を必要としない文書内整合の訂正である。Requirementの意味、scope、
実装範囲を変更しない。

## 訂正内容

1. 直接束縛数を**16件**へ訂正する。
2. §7の対応表に`REQ-WORKFLOW-004`を追加する。
   - Contract obligation：ReviewCompass3自身の文書を、通常のContract、Context、Harness、
     Triage、Trace、Workflow関門でreviewする。自己対象の特例や関門迂回を許さない。
   - 受入test：`A11 自己対象でも通常経路・関門を迂回しない`。
3. §8.1へA11を追加する。
4. 「残る35件」を**残る34件**へ訂正する。
5. TODOにある当該proposalのDigestだけを再計算して更新する。

表内の15件と追加する1件の合計16件、50 Requirementとの差34件が一致することを機械的に確認する。

## 禁止事項

- 提案の他節、後続評価E1〜E7、Current Plan、checklist、Requirement、code、test、schema、policy、
  Decision Record、Task Contract、外部DATA_ROOTを変更しない。
- LLM呼出、レビュー実行、Human判断の代行をしない。

## 検証とコミット

- TODO structure検査、TODO参照Digest検査、`git diff --check`、公式venv runnerの全testを実行する。
- proposalとTODOだけを一つのコミットにする。
- 完了報告はコミットに混ぜず、
  `records/session-handoffs/2026-08-05-claude-to-codex-work4-design-proposal-correction.md`へ書く。
  報告にはcommit SHA、訂正後Digest、検証結果、未実施範囲だけを記録する。
