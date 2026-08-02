# ReviewCompass3文書索引

## 現在の更新候補

Task Contract中心化に関する現行の後継候補は次の順に読む。

1. `concepts/2026-08-02-task-contract-centered-engineering.md`
2. `intent/2026-08-02-task-contract-centered-intent-amendment.md`
3. `requirements/2026-08-02-task-contract-requirements-delta.md`
4. `design/2026-08-02-task-contract-design-amendment.md`
5. `design/2026-08-02-stage-five-to-task-contract-inheritance.md`
6. `plan/2026-08-02-task-contract-centered-replan.md`
7. `development/2026-08-02-development-policy.md`

議論の固定原文と変更判断は次へ保持する。

- `../records/sources/2026-08-02-task-contract-source.md`
- `../records/sources/2026-08-02-llmgp-hybrid-experiment.md`
- `../records/sources/2026-08-02-reviewcompass2-shared-routine-ledger.md`
- `../records/sources/2026-08-02-reviewcompass2-issue-plan-path.md`
- `../records/task-contract/task-contract-centered-documentation-v1.json`
- `../records/task-contract/task-contract-centered-documentation-v2.json`
- `../records/task-contract/task-contract-centered-documentation-v3.json`
- `../records/task-contract/task-contract-centered-documentation-v4.json`
- `../records/task-contract/task-contract-centered-documentation-v5.json`
- `../records/task-contract/task-contract-centered-documentation-v6.json`

## 適用関係

- 2026-07-27から2026-07-28のintent、concept、requirements、design、planは固定済みの
  baselineであり、過去の承認と監査証拠の参照先として保持する。
- 2026-08-02のTask Contract文書群は、それらを上書きしない差分・後継候補である。
- 2026-08-02の開発方針は、リスクベースのテストファースト、段階的自己適用、
  Human判断範囲を定める。
- Task Contract文書群は第5段完了承認を代替しない。構造化requirements、design、
  acceptance test、差分監査を経て新しい承認候補を生成する必要がある。
- Task Contract requirements差分は`REQ-CONTRACT-001`〜`007`を対象とし、最後の要件で
  accepted Delivery Work Itemに束縛されたContract間のIntegration Verdictを定義する。
- Workflow requirements差分は`REQ-WORKFLOW-005`〜`009`を追加し、new developmentと
  maintenanceのrouting、reopen、上流改定、依存・循環、制御終了、実装前の共通ルーチン
  照合を定義する。
- SDD workflow、maintenance、reopenは三つの独立engineにせず、二つのwork originと
  fresh / reopenのcontinuation modeを共通Task Contract Deliveryへrouteする。
- LLMGPのSDD/TDD折衷試行は先行実験Evidenceとして扱い、受入条件の真偽を基準とする
  reopen分類、変更のstate effect、risk別review、Project Policy Overlayを明示的に採用する。
- 旧第5段の9 design、29 interface、8 state machine、14 protocol、37 acceptance testは
  継承matrixで`preserve / adapt / replace`へ全件分類する。replaceは旧表現の廃止であり、
  安全性義務、failure verdict、successor owner、後継testの削除を意味しない。
- ReviewCompass2のP-5と共通ルーチン台帳を前身方針として継承する。実コードから生成する
  Source Symbol Indexと意味判断を保持するReusable Routine Ledgerを分離し、red確認後の
  green実装前に`reuse / extend / merge / split_with_rationale`を判断する。
- ReviewCompass2のIssue→Plan経路を継承し、横断的なIssue Resolution Pathとして計画する。
  Issue Resolution Planをcompiled Plan bundleから分離し、Plan Challengeのblocking verdictを
  Work Item開始permitへ結線する。最初は最小E2E後の手作業Pilotとする。

## 固定baseline

- `intent/2026-07-27-reviewcompass3-intent-draft.md`
- `concepts/2026-07-27-task-runtime-concept.md`
- `requirements/review-context-requirements.md`
- `requirements/remaining-feature-requirements.md`
- `design/2026-07-28-reviewcompass3-design.md`
- `plan/2026-07-27-reviewcompass3-rebuild-plan.md`
- `plan/2026-08-02-development-policy-amendment.md`

固定baselineの内容を更新する必要がある場合、現在のパスを直接書き換えず、改定文書、
source Digest、置換範囲、変更理由を記録する。
