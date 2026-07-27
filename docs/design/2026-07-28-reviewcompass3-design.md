---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
---

# ReviewCompass3 design

構造化正本は`records/design/stage-five-design.json`とする。本書は設計判断を
人が読める形で要約する。

## 共通原則

- LLMは文章読解、意味的関連性、所見、解釈、改善仮説を提案する。
- 機械処理は列挙、Digest、Schema、参照、被覆、状態遷移、保存を検証する。
- Humanは外部送信、意味競合、Finding、方針変更、段完了を判断する。
- 各componentは失敗を値なし診断として残し、未検証状態を成功へ昇格しない。
- Human判断は機械関門を免除しない。Humanと機械の両方を要する判断は
  `hybrid` oracleとして検証する。

## 1. Review Task入力とExecution Context

Review Task定義、材料束、Scope、Composition、Context identity、handoffを
別componentとする。Traceが生成した影響候補母集合をScopeが全件分類し、
確定済みContextは内容Digestと完全性状態で識別する。

## 2. Harnessed Execution

Workflowの開始許可後だけRunを開始する。外部送信はpayload、Provider、
承認者identityへ束縛する。provider responseは解析前にwrite-ahead captureし、
Validationと形式復旧を版付きAttemptとして保持する。

## 3. TriageとHuman判断

担当別結果、重複、競合、Human判断を分離する。Finding候補をDigestで凍結し、
Traceのpre-provenance合格後にだけHumanが採用、拒否、保留を判断する。
判断後のFinal FindingをTraceが再検証し、final provenance合格後にだけ
WorkflowがRunと段階を完了する。

## 4. Semantic Trace

閉じたnode・edge語彙の平文グラフを正本とする。変更単位と閉包規則から
影響候補母集合を生成し、TaskからFindingまでのOperational Provenanceを検証する。
Traceはverdictだけを返し、Run状態やFinding採否を変更しない。

## 5. Session Records

利用者が指定した範囲だけを取込み、raw、伏字化転写、要約、来歴を分離する。
追記、非追記変更、消失を独立検査し、不正派生物を通常保存しない。
Humanは取込範囲と版付き伏字policyを確定するが、原本隔離、権限検査、
retentionおよび削除の機械関門を免除できない。

## 6. Workflow Control

active work、backlog、段階、actionを一意IDで結ぶ。Run開始・完了許可と
成果物書込みを状態機械の関門とし、ReviewCompass3自身にも同じ契約を適用する。
Run開始permitはTask、active work、Context digest、freshness verdictおよび
Execution Spec digestへ束縛し、Harnessが外部送信直前に再検証する。

## 7. Portable Lifecycle

版付きsupported-platform matrixから論理配置を解決する。原子的構造化I/Oと
機微情報隔離を共有境界として提供し、導入・解除は所有対象だけを補償操作する。
Humanが配置または機微情報policyを承認しても、機械的な整合性・権限・
retention・削除関門は常に必須とする。

## 8. Evidence Evaluation

固定対象、基準、証拠、観測値、解釈、限界を分離する。機械的な照合・計算と
LLMによる意味評価を区別し、Humanが意味的競合を判断する。

## 9. Self Improvement

成功、失敗、未確定の実測を条件identity付きledgerへ保存する。改善仮説は
固定比較で検証し、Human承認後だけ次周期へ反映する。

## 段間インターフェースと状態機械

`records/design/stage-five-architecture-integrity.json`を段間契約の正本とする。
ContextからWorkflow、WorkflowからHarness、HarnessからTriage、各段から
Semantic Trace、EvaluationからSelf Improvement、Self Improvementから
次周期Workflowへの入力を、identity、payload、失敗verdict付きで定義する。

Workflow、Run、Attempt、provider capture、Validationおよび
Triage/Provenanceは閉じた状態・event・遷移表を持つ。各遷移はguardと、
結果を外部へ見せる前に何を耐久化するかを定義する。

## 受け入れ試験

37要件それぞれに1件の受け入れ試験を割り当てる。各試験はsetup、stimulus、
expected、negative caseと`machine`、`human`、`hybrid`のoracle種別を持つ。
