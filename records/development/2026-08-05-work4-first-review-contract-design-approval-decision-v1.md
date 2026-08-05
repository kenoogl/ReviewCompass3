# DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001

## Decision

Humanは2026-08-05に
`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`を承認した。
これによりWork 4の最初のslice設計が確定し、Work 5Aの実装へ進める。

## 固定した五点（提案§9）

1. review対象は`docs/`配下の指定した一文書に限定する。
2. 直接束縛Requirementは提案§7の16件とし、残り34件は`deferred`とする。
3. `warning`はConformanceとFinal Challengeを自動失格にしない。ただしHuman decisionは
   正常経路でも常に必須であり、`warning`を無視してaccepted artifactを自動確定してはならない。
   `error`は停止する。
4. `tools/bootstrap/`は参照だけとし、Work 5AのRuntime componentへ昇格しない。
5. ConformanceとFinal Challengeは、異なる論理ownerと異なるrecordで実行する。
   Humanは両verdictの後に独立してdecisionを行い、どちらのownerにもならない。

## 後続評価の扱い

提案§11のE2〜E7は本承認の実装scopeに入らない。`deferred`とする。
E2（対象文書を変える）、E4（LLM shadow評価）、E5（LLMを非権威の助言として組み込む）の開始には、
それぞれ別途Human判断が必要である。

## 承認範囲

- 提案§1〜§10（対象scenario、Contract構造、record・owner・順序、正常経路と負例、
  Work 5A範囲とdefer境界、Work 4A／4Bの境界、Requirement対応16件、受入条件案）
- Work 5Aで`tools/task_contract/`に最小Runtime packageを実装すること

## 承認しないこと

- Work 4全体、Work 5A、Work 4Bの完了
- 実文書に対するreview run、Human decision、accepted artifactの作成
- Requirement、Requirement authority、既存bootstrap、Work 4A Evidence、Work 4B scopeの変更
- LLM、外部送信、外部`DATA_ROOT`、Git write／push／PR／CIの使用

## 根拠

- Human approval：2026-08-05。対象は
  `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`。
  実装範囲の固定は
  `records/session-handoffs/2026-08-05-codex-to-claude-work5a-first-review-contract-implementation.md`。
- 先行Decision：`DEC-WORK4A-EARLY-EXIT-001`
