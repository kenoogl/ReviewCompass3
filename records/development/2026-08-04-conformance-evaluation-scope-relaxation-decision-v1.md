# DEC-CONFORMANCE-SCOPE-RELAXATION-001

## Decision

Humanは`docs/design/2026-08-04-conformance-evaluation-scope-relaxation-proposal.md`を承認し、
旧ReviewCompassの`conformance-evaluation`に関する二つの制限をWork 4Aの範囲で緩和した。

| # | 現行 | 緩和後 |
| --- | --- | --- |
| 1 | 管理下で開発したcodeでは、requirementsとdesignのLLM逆推定を通常経路にしない（継承記録§5） | Work 4Aの範囲で、routineの責務分析と処置label提案に限り通常経路として使う |
| 2 | 本Workは初期開発へ入れない（Deferred Work 9） | Work 4Aの範囲で先行して使う |

## 緩和しないもの

緩和は「使ってよいか」だけである。次の規律は維持する。

- 文書生成と適合判定を分離する。
- 推定時に既存仕様を遮断し、後段で比較する。
- 推定根拠としてcode referenceを保持する。
- 生成物は`draft_only`とし、派生文書から規範正本を直接更新しない。
- 意味変更候補はHuman判断へ渡す。
- 機械がHuman dispositionを先取りしない。
- LLM由来の記述は非権威（advisory）とし、生成元を記録する。
- 派生物からDecision、Entry、Baselineを自動生成しない。

v3.1改訂案では、「推定根拠としてcode referenceを保持する」を`evidence_refs`必須、
参照範囲の同一Routine Profile内限定、生成元の必須fieldとして具体化する。

## 範囲

適用範囲はWork 4A Reusable Routine Ledgerに限る。
Deferred Work 9のAs-Built projector、Markdown renderer、Documentation Conformance gateの
実装着手を承認するものではない。

## 対象文書の扱い

`records/sources/2026-08-02-reviewcompass-conformance-evaluation.md`は固定source recordであり、
本文をin-place変更しない。位置づけの更新は本Decisionを正本とする。
前身repositoryのcodeは複製しない。継承するのは責務と語彙である。

## 根拠

- Human approval：2026-08-04の会話における次の承認。

  > v3.1設計改訂と、Work 4Aに限定したconformance-evaluation利用範囲の緩和を承認する。

- 対象提案：`docs/design/2026-08-04-conformance-evaluation-scope-relaxation-proposal.md`
- 継承記録：`records/sources/2026-08-02-reviewcompass-conformance-evaluation.md`
  （前身固定commit `cab302d4b32af790628b811b3566f39d55781fa5`）
