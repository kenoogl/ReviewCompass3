---
lifecycle: provisional
normative_status: successor-candidate
promotion_required: true
---

# 第5段設計からTask Contract中心設計への継承matrix

## 1. 目的

本文書は、2026-07-28第5段設計の安全性、責務、失敗動作、受け入れ義務を、Task Contract
中心設計へどのように継承するかを固定する。旧設計を一括廃棄または暗黙継承せず、各資産を
次へ分類する。

- `preserve`：意味、owner、停止条件を維持して取り込む
- `adapt`：意味を維持し、Task Contract、Plan、Work Item、Provenanceへidentityまたはownerを
  修正して取り込む
- `replace`：旧表現または重複制御を廃止し、同じ義務を後継資産へ移す

`replace`は安全性要件の削除を意味しない。後継owner、後継test、失敗verdictを持たない
廃止は認めない。

## 2. 固定baseline

| artifact | SHA-256 | 役割 |
|---|---|---|
| `docs/design/2026-07-28-reviewcompass3-design.md` | `f250cf6bf91afd1e7c786952a1fb9c9530ccac2a51ef14b34172f5be65ccd8b5` | 人間可読要約 |
| `records/design/stage-five-design.json` | `29ed55927061c9991ec7bbad3f03c929214527b653979d3453c9bbd7eb499c4f` | 9 designと37 acceptance testの構造化正本 |
| `records/design/stage-five-architecture-integrity.json` | `8b7e7666fd1918a4da0981e22fa274fa62e77f0b96ec7c47fd4aac09cac77f2a` | 29 interface、8 state machine、14 protocolの構造化正本 |
| `records/design/stage-five-approval-candidate.json` | `a1e211f4d63144f52cd5c8bf36c9b111a0715a205a8ce71ecb52f034172ab0b5` | 旧第5段承認候補 |

旧承認候補は`awaiting_human_approval`の履歴証拠であり、新設計の承認証拠へ流用しない。

## 3. そのまま取り込むinvariant

- LLMは意味的候補を提示し、機械は列挙、Schema、Digest、参照、被覆、状態、保存を検証する。
- Humanは意味的裁定を行うが、機械関門を免除できない。
- 未検証、欠測、競合、保存不能を成功へ昇格しない。
- provider responseは解析前にwrite-ahead captureし、raw、派生物、診断を分離する。
- 外部送信判断をpayload、Provider、model、endpoint、account、region、判断主体、権限、期限へ
  束縛する。
- Finding候補、重複・競合、Human判断、Final Findingを別identityで保持する。
- 原子的保存、再読込照合、機微情報隔離、retention、所有対象だけの補償を維持する。
- measurement、comparison、interpretation、limitation、Human decisionを分離する。
- 改善は固定比較とHuman承認後だけ新versionとして次周期へ反映する。

これらは共通Architecture Policyと各Task ContractのPreconditions、Capabilities、
Provenance Obligations、Escalation Policyへ写像する。

## 4. design componentの継承

旧9 componentを丸ごと廃止しない。旧stage依存の責務とidentityを修正する。

| legacy design | disposition | successor owner | 継承内容 |
|---|---|---|---|
| `DES-REVIEW-CONTEXT` | `adapt` | Context Runtime | 7項目Review TaskはTask Contractへ移し、候補取得、Scope、Composition、Context Manifest、freshnessを所有する |
| `DES-HARNESSED-EXECUTION` | `adapt` | Harness | 手作業Execution Specをcompiled Planへ置換し、Run、Attempt、send gate、capture、Validation、retryを維持する |
| `DES-REVIEW-TRIAGE` | `adapt` | Triage | model別結果、重複、競合、Human判断を保持し、Conformance、Definition Challenge、Final Challengeを区別する |
| `DES-SEMANTIC-TRACE` | `adapt` | Semantic Trace | Requirement、Contract、Plan、Work Item、Run、Evidenceを含む閉じた型付きgraphへ拡張する |
| `DES-SESSION-RECORDS` | `adapt` | Session Evidence Source | 独立stageにせずContext sourceとして接続し、raw、伏字化、要約、mutation、access、retentionの独立lifecycleを維持する |
| `DES-WORKFLOW-CONTROL` | `adapt` | Workflow | global stage状態を廃止し、Work Item routing、単一active leaf、permit、block、resume、termination、write gateを所有する |
| `DES-PORTABLE-LIFECYCLE` | `adapt` | Portable Lifecycle | 既存保存境界を維持し、Deployment Manifest、Project Binding、Integration Manifestを追加する |
| `DES-EVIDENCE-EVALUATION` | `adapt` | Evidence Evaluation | Evaluation Profile、Observation、Outcome Label、版付きmetric projectionを導入する |
| `DES-SELF-IMPROVEMENT` | `adapt` | Self Improvement | 直接設定変更を廃止し、Contract、Compiler、Policy、Capture Planの版付きImprovement Proposalを生成する |
| なし | `new` | Task Contract Control | 新設componentとしてContract、Portfolio、Policy、compile、obligation被覆を所有する |

### 4.1 Session Evidence Source

```text
user-approved source universe
  → scoped ingestion
  → isolated raw record
  → redacted or derived record
  → mutation verdict
  → Context candidate
  → Context Manifest
```

Session取込みは任意であり、ContractがSession contextを要求しない場合は通常実行を妨げない。
rawと派生物は別identity、別access、別retention、別削除Policyを持つ。Session Evidence Sourceは
Context採否、Work Item、Run状態を直接変更しない。

### 4.2 Self Improvement

```text
Evaluation Ledger
  → Improvement Hypothesis
  → fixed comparison
  → Human decision
  → versioned Contract / Compiler / Policy / Capture Plan proposal
  → stale impact analysis
  → approved next trial
```

Self Improvementは現行設定またはWorkflow状態を直接変更しない。承認済み提案だけを各ownerの
通常version protocolへ渡す。適用後も新しいtrialと旧baselineを区別する。

## 5. interfaceの継承

旧29本というpoint-to-point topologyと固定本数は廃止する。identity field、生成順、owner、
failure verdictは次の六つのinterface familyへ移す。

- Contract / Plan / Context
- Work Item / Permit / Run Result
- Approval / Capability / External Send
- Attempt / Capture / Validation
- Finding / Challenge / Provenance
- Evaluation / Improvement / Policy Change

| legacy interface | disposition | successor |
|---|---|---|
| `IF-CONTEXT-TRACE-IDENTITY` | `adapt` | Context ManifestとProvenance relation |
| `IF-CONTEXT-WORKFLOW-REQUEST` | `replace` | Contextは要求を送らず、Work Item permit検査がContext Manifestを参照する |
| `IF-EVALUATION-IMPROVEMENT-PACKAGE` | `adapt` | Evaluation Ledger → Improvement Proposal |
| `IF-HARNESS-CAPTURE-RESULT` | `preserve` | Attempt内Capture Result |
| `IF-HARNESS-EVALUATION-OBSERVATION` | `adapt` | Run／Attempt／Profileに束縛したEvaluation Observation |
| `IF-HARNESS-SEND-APPROVAL-DECISION` | `adapt` | Human Interaction Planに束縛したApproval Decision |
| `IF-HARNESS-SEND-APPROVAL-REQUEST` | `adapt` | Contract、Plan、payload、送信条件に束縛したApproval Request |
| `IF-HARNESS-TRACE-CAPTURES` | `adapt` | Capture、Validation、retryのProvenance event |
| `IF-HARNESS-TRIAGE-RESULTS` | `adapt` | Contract、Plan、Contextに束縛したResult Set |
| `IF-HARNESS-VALIDATION-CANDIDATE` | `preserve` | Attempt内Validation Candidate |
| `IF-HARNESS-VALIDATION-RESULT` | `preserve` | Attempt内Validation Result |
| `IF-HARNESS-WORKFLOW-RUN-RESULT` | `adapt` | Work Item、permit、Run終端に束縛したRun Result |
| `IF-HARNESS-WORKFLOW-START-REQUEST` | `adapt` | compiled PlanとContext Manifestを持つPermit Request |
| `IF-IMPROVEMENT-WORKFLOW-CHANGE` | `replace` | owner別の版付きChange Proposal。Workflowへ直接適用しない |
| `IF-PORTABLE-CONTEXT-STORE` | `adapt` | 共通Artifact Store contract |
| `IF-PORTABLE-HARNESS-STORE` | `adapt` | 共通Artifact StoreとSensitive／Raw Store contract |
| `IF-PORTABLE-SESSION-STORE` | `adapt` | Session raw／derived用の分離Store contract |
| `IF-PORTABLE-WORKFLOW-STORE` | `adapt` | Work Item、Run、Portfolio別の原子的Store contract |
| `IF-SESSION-CONTEXT-MATERIAL` | `adapt` | Session Evidence CandidateとContext obligation relation |
| `IF-TRACE-CONTEXT-SCOPE` | `adapt` | Context Acquisition PlanとScope Candidate relation |
| `IF-TRACE-RUN-FINALVERDICT` | `replace` | 単一の版付きFinal Provenance Verdict参照 |
| `IF-TRACE-RUN-PREVERDICT` | `replace` | 単一の版付きPre-Provenance Verdict参照 |
| `IF-TRACE-TRIAGE-FINALVERDICT` | `replace` | 同じFinal Provenance VerdictをTriageが参照する |
| `IF-TRACE-TRIAGE-PREVERDICT` | `replace` | 同じPre-Provenance VerdictをTriageが参照する |
| `IF-TRACE-WORKFLOW-FINALVERDICT` | `replace` | 同じFinal Provenance VerdictをWorkflowが参照する |
| `IF-TRACE-WORKFLOW-PREVERDICT` | `replace` | 同じPre-Provenance VerdictをWorkflowが参照する |
| `IF-TRIAGE-TRACE-CANDIDATE` | `adapt` | Finding Candidate provenance event |
| `IF-TRIAGE-TRACE-FINAL` | `adapt` | Human DecisionとFinal Finding provenance event |
| `IF-WORKFLOW-HARNESS-PERMIT` | `adapt` | Contract、Plan、Context、Work Item、approvalへ束縛したRun Permit |

shared Verdict化しても各consumerのfail-closed関門は残す。Verdictを参照できない、Digestが
一致しない、対象identityが異なる場合、Run、Triage、Work Itemを成功へ進めない。

## 6. state machineの継承

| legacy state machine | disposition | successor |
|---|---|---|
| `SM-ATTEMPT` | `adapt` | Contract、Plan、Context、Run identityを追加したAttempt lifecycle |
| `SM-PROVIDER-CAPTURE` | `preserve` | write-ahead Capture lifecycle |
| `SM-VALIDATION` | `adapt` | Verification Planとvalidator identityへ束縛したValidation lifecycle |
| `SM-RUN` | `adapt` | Work Item、approval、capture状態を所有せず、一回のRun終端だけを所有する |
| `SM-WORKFLOW` | `replace` | Delivery Work Item lifecycleとRun permit guard |
| `SM-TRIAGE-PROVENANCE` | `replace` | Finding Candidate／Decision lifecycleと独立Provenance Verdict |
| `SM-IMPROVEMENT` | `adapt` | Improvement Hypothesis／Proposal／Trial lifecycle |
| `SM-CONFIGURATION` | `replace` | Contract、Compiler、Policy、Capture Planの各version lifecycle |

Contract definition、Delivery Work Item、Run／Attempt、Portfolio dependency、Requirement／
Release scopeを同じ状態機械へ統合しない。

## 7. protocolの継承

旧14本という固定数を廃止し、Run Start、Attempt Execution、Finding Finalization、
Cross-Contract Integration、Improvementのprotocol familyと型付きfailure matrixへ再編する。

| legacy protocol | disposition | successor |
|---|---|---|
| `PROTOCOL-RUN-START` | `adapt` | Contract／Plan／Context／Work Item permitを検査するRun Start |
| `PROTOCOL-RETRY-SEND` | `adapt` | Retry Policy、budget、再承認条件を持つAttempt Execution |
| `PROTOCOL-FINDING-FINALIZATION` | `adapt` | Conformance、Challenge、Human Decision、Provenanceを分離したFinalization |
| `PROTOCOL-FINDING-PREFAIL` | `replace` | Finding Finalization failure matrixのpre-verdict分岐 |
| `PROTOCOL-FINDING-FINALFAIL` | `replace` | Finding Finalization failure matrixのfinal-verdict分岐 |
| `PROTOCOL-IMPROVEMENT-CYCLE` | `replace` | versioned Improvement Proposalと次trial protocol |
| `PROTOCOL-ATTEMPT-CAPTURE-VALIDATION` | `adapt` | Planに束縛したAttempt Execution |
| `PROTOCOL-DISPATCH-FAILURE` | `replace` | Attempt Execution failure matrix |
| `PROTOCOL-CAPTURE-DIAGNOSTIC-FAILURE` | `replace` | Attempt Execution failure matrix |
| `PROTOCOL-CAPTURE-QUARANTINE` | `replace` | Attempt Execution failure matrix |
| `PROTOCOL-CAPTURE-IRRECOVERABLE` | `replace` | Attempt Execution failure matrix |
| `PROTOCOL-VALIDATION-FAILURE` | `replace` | Attempt Execution failure matrix |
| `PROTOCOL-RUN-START-FAILURE` | `replace` | Run Start failure matrix |
| `PROTOCOL-RETRY-FAILURE` | `replace` | Attempt Execution failure matrix |

各旧failure prefix、期待終端、永続化順序、Run Result handoffをfailure matrixへ移し、単に
protocol本数を減らすために失敗branchを削除しない。

## 8. acceptance testの継承

37件すべてに後継testを割り当てる。`replace`対象も旧negative behaviorを後継testで再現する。

| acceptance test | disposition | proposed successor test | successor focus |
|---|---|---|---|
| `AT-CONTEXT-001` | `replace` | `AT-TC-CONTEXT-001` | 7項目TaskではなくTask Contract必須領域の欠落拒否 |
| `AT-CONTEXT-002` | `adapt` | `AT-TC-CONTEXT-002` | Context source、本文、出所、Digest、prior identity |
| `AT-CONTEXT-003` | `adapt` | `AT-TC-CONTEXT-003` | Acquisition Planに基づくsource universeとScope全件分類 |
| `AT-CONTEXT-004` | `adapt` | `AT-TC-CONTEXT-004` | Contract、Plan、Manifest変更による旧identity再利用拒否 |
| `AT-CONTEXT-005` | `preserve` | `AT-TC-CONTEXT-005` | 採用材料と採用主体の追跡、暗黙追加拒否 |
| `AT-CONTEXT-006` | `adapt` | `AT-TC-CONTEXT-006` | Plan／Manifest handoffとfreshness再検査 |
| `AT-CONTEXT-007` | `preserve` | `AT-TC-CONTEXT-007` | 原子的保存、再読込、access、retention、削除 |
| `AT-EXEC-001` | `adapt` | `AT-TC-EXEC-001` | Contract、Plan、Context、Work Itemへ束縛したpermit |
| `AT-EXEC-002` | `preserve` | `AT-TC-EXEC-002` | payloadと送信条件を固定したapproval request／decision |
| `AT-EXEC-003` | `preserve` | `AT-TC-EXEC-003` | 全失敗branchのRun Result生成とWork Itemへの伝播 |
| `AT-EXEC-004` | `adapt` | `AT-TC-EXEC-004` | Verification Profileが要求したrole／model結果の完全性 |
| `AT-EXEC-005` | `preserve` | `AT-TC-EXEC-005` | Validationと意味を変える復旧のHuman裁定 |
| `AT-EXEC-006` | `adapt` | `AT-TC-EXEC-006` | Contract、Plan、Profileを含むeffective execution identity |
| `AT-TRIAGE-001` | `adapt` | `AT-TC-TRIAGE-001` | 実行topologyに応じた結果件数とraw参照 |
| `AT-TRIAGE-002` | `preserve` | `AT-TC-TRIAGE-002` | 重複元、競合主張、未解決提示 |
| `AT-TRIAGE-003` | `adapt` | `AT-TC-TRIAGE-003` | Conformance／ChallengeとWork Item終端へのfailure propagation |
| `AT-TRACE-001` | `preserve` | `AT-TC-TRACE-001` | 閉じた型付きgraphと一次Evidence到達性 |
| `AT-TRACE-002` | `adapt` | `AT-TC-TRACE-002` | RequirementとContract obligationの順逆被覆 |
| `AT-TRACE-003` | `preserve` | `AT-TC-TRACE-003` | 決定的診断とvalidator失敗後の確定拒否 |
| `AT-TRACE-004` | `adapt` | `AT-TC-TRACE-004` | Contract dependencyと版付き影響閉包 |
| `AT-TRACE-005` | `adapt` | `AT-TC-TRACE-005` | Conformance／Challenge別のProvenance Verdictと伝播 |
| `AT-SESSION-001` | `preserve` | `AT-TC-SESSION-001` | 利用者指定範囲だけの任意取込み |
| `AT-SESSION-002` | `preserve` | `AT-TC-SESSION-002` | raw／派生物の再生成、分離Policy、機微情報検査 |
| `AT-SESSION-003` | `preserve` | `AT-TC-SESSION-003` | 追記、非追記変更、消失の区別 |
| `AT-WORKFLOW-001` | `adapt` | `AT-TC-WORKFLOW-001` | Portfolioから選ぶ単一active leaf |
| `AT-WORKFLOW-002` | `adapt` | `AT-TC-WORKFLOW-002` | Run ResultからWork Item blockedへのfailure propagation |
| `AT-WORKFLOW-003` | `preserve` | `AT-TC-WORKFLOW-003` | 許可範囲外artifact writeの無変更拒否 |
| `AT-WORKFLOW-004` | `adapt` | `AT-TC-WORKFLOW-004` | stable能力だけを使うReviewCompass3自己適用 |
| `AT-PORTABLE-001` | `adapt` | `AT-TC-PORTABLE-001` | Deployment ManifestとProject Bindingによるlogical root |
| `AT-PORTABLE-002` | `preserve` | `AT-TC-PORTABLE-002` | 部分書込み後の旧版保持と不正構造拒否 |
| `AT-PORTABLE-003` | `adapt` | `AT-TC-PORTABLE-003` | install、update、uninstallとBinding／Manifest所有対象 |
| `AT-PORTABLE-004` | `preserve` | `AT-TC-PORTABLE-004` | sensitive分類、access、retention、削除、改変検出 |
| `AT-EVAL-001` | `adapt` | `AT-TC-EVAL-001` | Evaluation Profile、対象、基準、Evidence、stale |
| `AT-EVAL-002` | `adapt` | `AT-TC-EVAL-002` | Evaluation Observationとmetric／解釈／限界の分離 |
| `AT-EVAL-003` | `preserve` | `AT-TC-EVAL-003` | 固定入力からの再計算と失敗例保持 |
| `AT-IMPROVE-001` | `adapt` | `AT-TC-IMPROVE-001` | Evaluation trial、条件identity、比較可能性 |
| `AT-IMPROVE-002` | `replace` | `AT-TC-IMPROVE-002` | 直接設定適用を拒否し、版付きProposal、Human判断、staleを検証 |

分類結果は`preserve: 15`、`adapt: 20`、`replace: 2`である。旧test IDは来歴参照として残し、
後継test IDと`supersedes`または`validates_same_obligation_as`で結ぶ。

## 9. 廃止する旧表現

- 7項目Review Taskを正式Runtime入力の正本とすること
- 手作業Execution Specを実行正本とすること
- Design、Task、Implementationを全体stageとして進めること
- Contract、Work Item、Run、Portfolio、Requirement scopeをWorkflow状態へ集約すること
- 29本のpoint-to-point interfaceと14本のprotocolを固定数として維持すること
- 同じProvenance Verdictをconsumer別interfaceとして重複生成すること
- failure-only protocolを正常protocolと独立した重複手順として保守すること
- Self ImprovementがWorkflow設定を直接変更すること
- 全変更へ同じmulti-model reviewまたはHuman gateを要求すること

## 10. promotion条件

- 本baselineの4 DigestがProvenance recordへ固定される。
- 全9 legacy designにsuccessor ownerがある。
- 全29 interfaceのidentity fieldとfailure verdictが後継schemaまたはtestへ結ばれる。
- 全8 state machineの状態所有移管が競合しない。
- 全14 protocolのfailure prefix、期待終端、永続化順序が後継failure matrixで被覆される。
- 全37 acceptance testに後継test IDと実行可能なoracleがある。
- Session Evidence SourceとSelf Improvement Proposalのrequirements、design、negative testが
  確定する。
- 新旧構造化成果物の順逆被覆監査に未解決がない。
