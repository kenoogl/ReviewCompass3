---
lifecycle: provisional
normative_status: review-candidate
promotion_required: true
---

# Task Contract中心化 design改定

## 1. 対象

本文書は、`2026-07-28-reviewcompass3-design.md`と構造化第5段設計を固定baselineとして
保持し、Task Contract中心化に必要なcomponent、interface、状態、Provenance、評価、
配置の差分を定義する。

旧9 design、29 interface、8 state machine、14 protocol、37 acceptance testの個別判定は
`2026-08-02-stage-five-to-task-contract-inheritance.md`を正本とする。旧表現を`replace`する
場合も、安全性義務、failure verdict、後継owner、後継testを失わない。

既存の第5段承認候補は`awaiting_human_approval`のまま上書きしない。本改定と対応する
構造化設計、受け入れ試験、適合性監査が完成した後、新しい承認候補を生成する。

6 Plan、Challenge、関数台帳、Provenanceの意味上の分離を維持しながら物理実装とHuman作業を
軽量化する境界は、
[Task Contract設計の過剰実装を避ける境界に関するメモ](2026-08-03-overdesign-boundaries-memo.md)
を参照する。

## 2. 設計原則

- Task ContractをRequirementsとRuntime間のcontrol and provenance planeにする。
- Task ContractとCompilerは宣言とprojectionを所有し、consumer状態を変更しない。
- Plan生成をLLMの非公開推論に委ねず、決定的validatorで検査する。
- Runtimeで観測する非決定値は、入力条件と結果を固定して後段へ渡す。
- Contract conformanceとContract challengeを分離する。
- Operational ProvenanceとEvaluation Observationsを分離する。
- 実コードから生成するSource Symbol Indexと、人が確認するReusable Routine Ledgerを
  分離し、green実装前に両方を照合する。
- 意味上の責務分離を、独立したauthority、lifecycle、security、failure recoveryまたは実測scaleの
  根拠なしに、独立artifact、component、state machine、Human gateへ展開しない。
- 開発checkout、installed code、project、runtime data、sensitive storeを分離する。
- stableでない自己適用能力を必須経路へ置かない。

## 3. 新component：Task Contract Control

`DES-TASK-CONTRACT-CONTROL`を追加し、次を所有する。

- Task Contract schemaとversion
- Task Contract Portfolio
- RequirementとContract obligationの被覆
- Contract definition lifecycle
- Architecture Policyのidentity、適用範囲、優先順位解決
- CompilerとPlan bundle
- Contract、Compiler、Policy変更時のstale閉包
- consumerへ渡すPlan interface

所有しないものは次である。

- Contextの取得・採用
- Workflowの作業段階とRun permit
- HarnessのRun・Attempt状態
- Findingの採否
- Operational Provenance graphの検証
- 構造化成果物の物理保存
- 評価結果の意味的解釈

### 3.1 Contract schema

構造化正本はJSON互換の閉じたschemaとし、Identityと9領域を持つ。各obligationは
一意の`obligation_id`を持ち、配列位置をidentityにしない。

正規化は次を固定する。

- UTF-8
- key順序
- number、boolean、nullの許可範囲
- set相当配列の順序規則
- path、URI、IDの正規化
- schema version
- Digest algorithm

Contract本文とHuman承認判断は別recordにする。承認対象recordがContract digest、
source Requirement digest、challenge結果digestへ束縛された場合だけ`approved`へ進む。

### 3.2 Architecture Policy

Architecture Policyは複数Contractへ共通する制約を、Task Contract本文と分離して
保持する。

```text
ArchitecturePolicy
├── policy_id / version / digest
├── owner
├── applicability_scope
├── rules[]
│   ├── rule_id
│   ├── subject
│   ├── constraint
│   └── priority
├── supersedes
├── effective_status
└── conflict_resolution
```

Policy解決は固定したPolicy集合、適用範囲、優先順位から決定的に行う。適用Policyが
不足する場合は`policy_unresolved`、同順位で競合する場合は`policy_conflict`とし、
Compilerへ渡さない。Policy変更時はruleとContract obligationの依存辺から影響閉包を
求め、無関係なContract成果をstaleにしない。

project固有の調整は基本Policy本文へ追記せず、版付きProject Policy Overlayとして保持する。

```text
ProjectPolicyOverlay
├── overlay_id / version / digest
├── project_id / binding_id
├── base_policy_refs
├── applicability_scope
├── adjustments[]
│   ├── adjustment_id
│   ├── replaces_rule / replacement_rule
│   ├── reason / evidence_refs
│   ├── decided_at / decided_by
│   └── supersedes
└── effective_status
```

commit guardのdeadlockや一律reviewの過剰負荷のような運用結果は、失敗事象と置換規則を
Policy Adjustment Eventとして残す。Agent entryは固定したbase PolicyとOverlayの解決結果
から生成し、末尾への追記だけをPolicy正本にしない。Overlayも通常Policyと同じ競合解決、
Digest固定、stale影響閉包の対象とする。

#### Implementation Reuse Policy

ReviewCompass3自身のImplementation Task Contractには、ReviewCompass2のP-5を継承した
Architecture Policyを適用する。

```text
ImplementationReusePolicy
├── policy_id / version / digest
├── applicability_scope
├── source_language_and_root_rules
├── symbol_index_generator / schema
├── candidate_search_rules
├── candidate_decisions: reuse | extend | merge | split_with_rationale
├── human_confirmation_policy
├── retired_routine_policy
└── provenance_and_gate_rules
```

候補探索の結果は`candidate_found | no_candidate`とする。`no_candidate`は4分類へ追加する
第五の判断ではなく、比較対象が見つからなかった探索結果である。`candidate_found`の場合に
限り4分類を必須とし、LLM proposalとHuman confirmationを別recordとして保持する。

事実層と意味層を分離する。

```text
SourceSymbolIndex
├── index_id / schema_version / digest
├── project_id / binding_id
├── source_tree_identity / digest
├── generator_identity / digest
└── symbols[]
    ├── symbol_id / language / kind / qualified_name
    ├── source_path / location / content_digest
    ├── signature / imports / callers / callees
    └── doc_and_test_refs

ReusableRoutineLedger
├── ledger_id / version / digest
├── routines[]
│   ├── routine_id / responsibility / canonical_symbols
│   ├── aliases / status: active | retired
│   └── origin / replacement / retirement refs
├── consolidation_history[]
└── previous_version
```

Source Symbol Indexは固定source treeから全symbolを機械生成する派生事実であり、手作業で実コードの
存在を追加・削除しない。Reusable Routine Ledgerはpublic、共有、cross-contract、high-risk、
重複候補、retired、今回の影響閉包または新規・統廃合提案に該当するroutineについて、人が確認した
責務、alias、状態、統廃合履歴を保持し、過去entryを上書きしない。単純accessor、generated code、
外部vendorなどは明示した規則でLedger対象外にできるが、Index上の存在を削除しない。両方と実コードを
照合し、片方だけを判断根拠にしない。

初回の製品実装前に、確定したLayout Baselineを使ってsource pathとsymbol identity規則を固定し、
既存の全関数・methodをSource Symbol Indexへ収録する。HumanはIndex生成・対象外規則、coverage／
freshness統計、public／共有／high-risk抽出、重複候補、retired routine、representative sample、
未解決候補の処置を確認する。全symbolの意味entry作成をbaseline完了条件にしない。今回の変更範囲に
必要なLedger判断が未解決なら、最初のImplementation Task Contractへ`implementation_ready`を発行しない。
配置変更後は旧Indexを利用せず、Layout Baseline、Project Binding、source treeの新identityから再生成する。

Index生成器が存在しないbootstrap時は、固定source treeを読み、固定schemaのIndexだけを出力する
隔離development toolを最小例外として作成できる。生成器のTestと独立reviewを先に行い、生成後の
最終Indexへ生成器自身も収録する。Runtime capabilityとしての採用は別Task Contractで判断する。

Review / Execution PlanはImplementation Task Contractの場合だけImplementation Discovery
Planを内包する。これは6種類のPlanへ第7の全Contract必須Planを追加するものではない。

```text
ImplementationDiscoveryRecord
├── discovery_id / schema_version / digest
├── task_contract / work_item / red_test refs
├── source_tree / symbol_index / ledger refs and digests
├── planned_symbols / search_scope / queries
├── candidates / evidence refs
├── outcome: candidate_found | no_candidate
├── proposed_decision / rationale / proposer
├── human_confirmation_ref
├── retired_routine_verdict
└── design / implementation / commit refs
```

### 3.3 Compiler

Compilerは純粋なprojection coreと、外部capability catalogを解決するvalidation境界に
分ける。

```text
Contract + fixed Policy + fixed Catalog
  → normalize
  → validate references
  → project six typed Plan views
  → verify obligation coverage
  → verify cross-plan consistency
  → Plan bundle identity
```

外部Toolの存在、OS capability、利用可能なProviderなどの時変観測はPlan生成結果へ
混ぜず、固定したCapability Resolution Recordとして入力化する。

### 3.4 Plan bundle

Plan bundleは次を持つ。

- bundle ID、version、digest
- Contract ID、version、digest
- Compiler ID、version、digest
- PolicyとCatalogのidentity
- 6 typed Plan viewの安定keyとcoverage
- obligation coverage map
- unresolvedとdiagnostic
- Evidence Extraction ContractとEvidence Consumption Closure
- Assurance Obligation Matrix
- Validator Assurance ProfileとReview Quality Contract

Implementation Task ContractではReview / Execution Plan内のImplementation Discovery Planと
`REQ-WORKFLOW-009`の対応を被覆mapへ追加する。Review Task Contractなど実装を行わない型では
このPlan項目を生成しない。

一つでも必須Planが生成不能または被覆不足の場合、bundleは`not_compilable`であり、
consumerへ開始可能なPlanとして渡さない。

6 Planは一つのimmutable Plan bundle内のtyped viewであり、bundle全体に一つのidentity、version、
digest、compile verdictを持つ。共通のContract、Policy、Catalog、risk、source、permissionはbundle共通部へ
一度だけ保存し、consumerへ必要なviewを決定的にprojectionする。viewを利用者が直接編集せず、
独立approval、独立lifecycle、独立state machineを持たせない。共通の中間modelから全viewを生成し、
view間のpoint-to-point整合protocolを作らない。

特定viewの独立保存またはprocess分離は、ownerと更新周期、security、retention、failure recovery、
またはscaleの独立性が実測された場合だけ別Task Contractで判断する。分離してもbundle identity、
Contractからの導出関係、obligation coverageを維持する。

## 4. 既存componentの改定

### 4.1 Context Runtime（Review Context Feature owner）

Context RuntimeはTask定義を所有しない。Context Acquisition Planを受け取り、候補取得、
Scope分類、Composition、Manifest、freshnessを所有する。

Context Manifestへ追加する項目は次である。

- ContractとPlan identity
- Context obligation ID
- selection mode（`impact_slice | expanded_scope | full_consistency`）
- fixed change unit、semantic graph、closure ruleのidentity
- source universe量、変更単位数、影響閉包単位数
- selected sourceとversion
- 各候補への到達理由、採否、採用目的
- transformation chain
- excluded candidateと理由
- unresolved obligation
- contradiction
- trustとfreshness verdict
- review payloadのbyte、token、時間、費用
- scope拡大時の起点、理由、判断主体、追加材料、拡大前後の量、終了条件
- confidentiality class
- material adequacy verdictとcompleteness oracle
- `insufficient_evidence | out_of_level`の分類と処置
- 必須source／Findingのconsumer参照

`impact_slice`は既定modeであり、固定変更単位から版付き意味graphと閉包規則をたどった影響
候補、必要なEvidence抜粋、Contract必須材料だけをCompositionする。source universeへ到達不能な
材料を追加した場合、universe identityの変更によりfreshnessは再検査するが、選択材料集合と
payloadは増やさない。

`expanded_scope`と`full_consistency`は、graph、閉包規則またはEvidenceの欠落・stale・競合、
global invariant、横断Policy、未解決循環、Verification ProfileまたはDecision Authorityの要求に
限って選べる。通常sliceへの暗黙追加として扱わず、別Context identityとProvenanceを作る。
budget超過時は必須材料を切り捨てず、Evidence closureを保つ分割・再構成、またはHuman
escalationへrouteする。どの経路でも安全な入力を確定できない場合はRun permitを要求しない。

既存資料を探索するPlanでは、開始entry、展開規則、分類軸、終了条件、除外条件、完全性oracleを
Evidence Extraction Contractとして固定する。候補は`adopt | adapt | reject | defer`へ全件分類し、
採用sourceまたはFindingをRequirement、Contract obligation、Verification、Decisionのいずれにも
接続できない場合は`evidence_consumption_incomplete`としてContextを充足済みにしない。

### 4.2 Workflow

WorkflowはContract definition lifecycleを直接変更しない。`approved`なContractと
`compiled`なPlan bundleに対して、active work、Context freshness、必要承認を検査して
Run permitを発行する。

Workflowは次を所有する。

- `new_development | maintenance`のwork origin
- `fresh | reopen`のcontinuation mode
- Work Item lifecycleと単一active leaf
- Upstream Inconsistency Findingのrouting
- Dependency Discovery Recordとblocking状態
- pause、cancel、scope disposition要求

Contract定義、Plan bundle、Run / Attempt、Requirement scope自体の状態は所有しない。

permitは次へ束縛する。

- Task Contract ID、version、digest
- Plan bundle ID、digest
- Context Manifest ID、digest、freshness
- active work ID
- required approval ID
- validator version、発行時刻、期限

Work Itemが`blocked_by_dependency`、`blocked_by_cycle`、`revision_pending`、`paused`、
`cancellation_pending`のいずれか、またはPortfolioが実行可能leafと判定しない場合は
permitを発行しない。

### 4.3 Harness

HarnessはReview / Execution PlanとHarness and Capability Planを受け取る。Tool、root、
network、Provider、budget、side effectをPlanの許可範囲外へ拡張できない。

各Attemptは次を記録する。

- Contract、Plan、Context、permit identity
- actor、Tool、Provider、model
- resolved permissionとroot
- resource usageとbudget残量
- side effect requestとresult
- request、raw capture、Validation、retry

### 4.4 Triage

TriageはFindingへ`review_layer`を追加する。

- `contract_conformance`
- `definition_challenge`
- `final_contract_challenge`

開発制御に関するFindingは`finding_kind`で、`upstream_inconsistency`、
`dependency_discovery`、`cycle_detection`、`termination_candidate`を区別する。

Challenge Findingはsource Requirement、Architecture Policy、risk catalogまたは隣接
ContractへのEvidence referenceを必須とする。blocking Challenge Findingがある場合、
Delivery Work Itemを`accepted`へ進めず、ContractまたはRequirementの改定要求を
Workflowへ返す。

`contract_conformance | definition_challenge | final_contract_challenge`はVerdictの意味、基準、
failure routeとして分離するが、常に別Review Runを要求しない。low riskでは一つのRunが共有材料と
deterministic validationから複数の型付きVerdictを生成できる。mediumは影響に応じてConformanceと
Final Challengeを独立させ、highまたは外部・不可逆side effectでは必要な独立reviewerとHuman gateを
要求する。同じFinding候補をVerdictごとに複製せず、共有Evidenceと各判断を別identityで結ぶ。

### 4.5 Semantic Trace

Operational Provenance graphへ次のchainを追加する。

```text
Intent / Requirement evidence
  → Task Contract Portfolio
  → Task Contract
  → Compilation
  → Plan bundle
  → Work routing / Work Item
  → Context Manifest
  → Workflow permit
  → Source Symbol Index / Reusable Routine Ledger
  → Implementation Discovery / Human confirmation
  → Run / Attempt
  → Result / Evidence
  → Dependency / Revision / Termination decision
  → Conformance / Challenge
  → Human decision
  → accepted artifact
```

各Plan項目とRuntime eventはContract obligationへ逆引きできなければならない。

Semantic TraceはSource Symbol Index、Reusable Routine Ledger、Implementation Discovery
Recordのschemaと関係検証を所有する。Workflowはgreen実装permitを所有し、Portable
LifecycleはLedgerとrecordの原子的書込みを所有する。Semantic Traceは実装またはWork Item
状態を直接変更しない。

後続開発ではSemantic TraceがAs-Built Recordのschema、固定入力からのprojection、
Task Contract obligationと実装symbolの双方向照合、Documentation Conformance Verdictを
所有する。Task Contract Controlは文書化に必要なProvenance obligationを提供し、Workflowは
有効化後のverification gateとUpstream Revisionへのroutingを所有する。Portable Lifecycleは
暫定projectionとaccepted成果の分離配置を所有する。初期実装ではprojectorを実装せず、
将来の再構成に必要なidentity、relation、Digestを既存eventへ保持する。

### 4.6 Evidence Evaluation

Evidence EvaluationはEvaluation Profile、一次event、Outcome Labelを読み、metric
projectionを生成する。event自体を変更せず、次を分離する。

- measurement
- comparison
- interpretation
- limitation
- Human decision

### 4.7 Portable Lifecycle

Portable Lifecycleは全新componentへ共通する論理root、構造化I/O、分類、retention、
migration、所有境界を提供する。各componentは保存対象と分類を指定するが、独自の
root解決とsecret保存を実装しない。

### 4.8 Cross-Contract Integration

Task Contract Controlはaccepted Delivery Work Itemに束縛されたContract集合、interface、
共有状態owner、Integration Manifest、Project Bindingから版付きIntegration Planを
生成する。WorkflowはPlanを受理し、E2Eとfailure propagationを実行する。Semantic Traceは
Contract単位EvidenceとIntegration Verdictを結び、Release Evaluationは
`integration_passed`だけをrelease判断材料として受理する。

Task Contract Controlはconsumerの実行状態を直接変更しない。interface競合、owner重複、
stale入力、局所成功・全体Intent不成立は`integration_failed`として耐久保存する。

### 4.9 Session Evidence Source

Session Recordsは独立stageではなく、Context Runtimeへ候補を渡す版付きsource adapterとする。

```text
SessionEvidenceSource
├── source_universe / human_decision_ref
├── raw_record_id / digest / sensitive_store_ref
├── redaction_policy_id / version / digest
├── derived_record_id / digest
├── mutation_verdict
├── access / retention / deletion policy refs
└── context_candidate / provenance relations
```

raw、伏字化派生物、要約を同じidentityまたは保存境界にしない。raw原本から派生物を再生成
でき、追記、非追記変更、消失を区別する。未解決mutation、機微情報検査不合格、Policy不一致
では派生物をContextへ渡さない。Session contextを要求しないContractは通常実行できる。

Session Evidence SourceはContext採否、Work Item、Run状態を変更しない。Context Runtimeが
Context Acquisition Planに従って候補を採否し、Portable Lifecycleが保存とaccessを、Semantic
TraceがrawからContext Manifestまでの来歴を検証する。

source adapterはsourceの実効retention、capture deadline、取得時点、復元方法、復元検証を
Availability Recordへ保存する。`source_missing | source_expired | non_reconstructable`は候補ゼロや
正常な空sessionと区別し、必須sourceならRunを開始しない。復元成功は参照の存在だけでなく、
期待digest、構造、派生物再生成の確認を要する。

bootstrapでは完全なSession Records Runtimeに先立ち、次の最小Capture ProfileをLayout Baselineへ
束縛して準備する。

```text
SessionLogBootstrapRecord
├── session_id / source_identity / source_kind
├── started_at / captured_at / capture_deadline
├── raw_record_id / digest / sensitive_store_ref
├── derived_record_id / redaction_policy_ref
├── completeness / mutation_verdict / availability_verdict
├── confidentiality / access / retention
└── capture_actor / authorization_ref / restore_verification_ref
```

rawは既定で`SENSITIVE_ROOT`、伏字化派生物、要約、索引は別identityで`DATA_ROOT`へ置く。Work 2
以降の議論、判断、調査、変更を取得対象にできる状態をbootstrap完了条件とし、rawから派生物を
再生成するrestore fixtureを通す。source adapterが利用できない場合もAvailability Recordを残す。
このprofileは開発Evidence保全用であり、外部送信、許可範囲拡大、無期限retentionまたは完成した
製品Session Records能力として扱わない。

### 4.10 Self Improvement

Self ImprovementはEvaluation Ledgerを読み、現行設定を直接変更せず版付きImprovement
Proposalを生成する。

```text
ImprovementProposal
├── proposal_id / version / digest
├── evaluation_case / condition / pair / trial refs
├── hypothesis / fixed_comparison / limitations
├── target_owner / target_artifact_type
├── prior_identity / proposed_change
├── risk / stale_impact / rollback
├── human_decision_ref
└── next_trial_profile
```

targetはTask Contract、Compiler、Architecture／Project Policy、Capture Planのいずれかとする。
承認済みProposalも各ownerのchallenge、compile、Policy解決、migrationを迂回しない。適用結果は
旧baselineと異なるtrialとして記録し、未承認、比較不能、対象不明、stale閉包不明のProposalを
現行方針から隔離する。

## 5. ContractとWork lifecycle state machine

### 5.1 Contract definition lifecycle

```text
draft
  ├─ definition_challenge_failed → revision_required
  └─ definition_challenge_passed → challenged

challenged
  ├─ approval_rejected → rejected
  └─ approval_granted → approved

approved
  ├─ upstream_changed → stale
  └─ replaced_by_new_version → superseded
```

`revision_required`、`stale`、`rejected`、`superseded`は旧versionを変更しない耐久状態と
する。`not_compilable`と`compiled`はContract本文の状態ではなく、固定したContract、
Compiler、Policy、Catalogに対するPlan bundle verdictとする。

### 5.2 Work routing

```text
WorkItem
├── work_id / version / digest
├── work_origin: new_development | maintenance
├── continuation_mode: fresh | reopen
├── contract_id / version / digest
├── plan_bundle_id / digest
├── prior_work / run / decision refs
├── checkpoint_ref
├── dependency_refs
├── state / reason
└── resume_or_disposition_conditions
```

maintenanceはbaseline、trigger、維持invariant、regression scope、compatibility、migration、
rollbackを追加で持つ。reopenはprior identityと理由を必須とし、旧Work Itemを変更せず
新しいWork Item versionを作る。

### 5.3 Delivery Work Item lifecycle

```text
queued
  └─ permit_ready → active

active
  └─ red_confirmed → red

red
  └─ implementation_discovery_passed → implementation_ready

implementation_ready
  └─ tests_passed → green

green
  ├─ refactor_completed_and_tests_passed → green
  ├─ verification_failed → revision_pending
  └─ verification_passed → verified

verified
  ├─ final_challenge_blocking → revision_pending
  └─ acceptance_granted_or_not_required → accepted

queued | active | red | implementation_ready | green | verified
  ├─ blocking_dependency_found → blocked_by_dependency
  ├─ dependency_cycle_found → blocked_by_cycle
  ├─ upstream_inconsistency_found → revision_pending
  ├─ pause → paused
  ├─ cancel_requested → cancellation_pending
  └─ scope_exit_requested → scope_disposition_pending

blocked_by_dependency | paused
  └─ resume_conditions_satisfied → ready

ready
  ├─ freshness_failed → revision_pending
  └─ permit_ready → active

revision_pending
  ├─ revision_rejected → ready
  └─ revision_approved → replaced

blocked_by_cycle
  ├─ cycle_resolved → ready
  └─ termination_selected → cancellation_pending

cancellation_pending
  ├─ cancellation_rejected → ready
  └─ cleanup_and_decision_passed → cancelled

scope_disposition_pending
  ├─ scope_change_rejected → ready
  └─ scope_change_approved_and_cleanup_passed → cancelled
```

`accepted`、`cancelled`、`replaced`はWork Itemの耐久終端である。`blocked_by_cycle`は循環を解くか
controlled terminationが決まるまでpermit不能である。Contractの期待を変えずDesignまたは
Implementationだけを修正する場合は同Contractに束縛した新Work Itemまたは新Runを作る。
ContractまたはRequirementを変える場合は旧Work Itemを`revision_pending`から終了し、
新Contract versionと新Work Itemのredへ移る。

`implementation_ready`はredを確認した後、固定source tree、Source Symbol Index、Reusable
Routine Ledger、実コードの照合と必要なHuman確認が完了した状態である。独立した全体stage
ではなく、green実装permitの耐久gateである。source tree変更でIndexがstaleになった場合は
`implementation_ready`を再利用せず、同Run内でIndexとDiscovery Recordを更新するか、影響が
ContractまたはTestへ及ぶ場合は通常のRevision Protocolへ送る。

### 5.4 Upstream Revision Protocol

TDD中の不整合はUpstream Inconsistency Findingとして、検出元、競合対象、Evidence、
代替Design、risk、cost、checkpointを固定する。Findingには次を持たせる。

- `change_semantics`: `editorial | evidence_only | implementation_only |
  contract_semantic | requirement_semantic | scope_semantic`
- `acceptance_truth_changed`: booleanと判定根拠
- `state_effect`: `no_state_change | advances_workflow | changes_contract |
  changes_requirement | changes_scope | external_or_irreversible`
- prior / proposed Acceptance Criteria、義務、scopeの差分

同じ入力とEvidenceでaccept/reject、義務またはscopeが変わり得る場合は
`acceptance_truth_changed: true`とする。`false`の軽微修正は旧成果と訂正理由を結ぶが、
ContractまたはRequirementの新versionとworkflow前進を要求しない。作業中に`true`と判明
した場合は軽微修正を停止し、意味的reopenへ切り替える。

次の順で、変更が必要な最下位層を選ぶ。

1. Implementation
2. Design Decision
3. Task Contract
4. Requirement
5. Feature Partitioning
6. Intent

実装都合だけで上流を弱めない。上流変更にはprior / proposed identity、影響閉包、stale、
Test migration、Human authorityを持つRevision Proposalを要求する。承認時は旧成果を
上書きせず、Portfolio被覆、compile、redを新versionでやり直す。却下時は現Contractと
Testを維持してImplementationへ戻る。

### 5.5 Dependency Discoveryとcycle resolution

境界外問題はDependency Discovery Recordとして次を持つ。

- discovery IDと発見元Work Item、Contract、Run、phase
- scopeとblocking分類
- Evidenceと親checkpoint
- child Contract候補またはbacklog disposition
- `requires`、`blocks`、`discovered_during`、`related_to`関係
- 親の再開条件

blocking依存は親を`blocked_by_dependency`にし、schedulerは依存graphの未解決blocking辺を
持たない単一active leafだけを選ぶ。新しい依存辺ごとにstrongly connected componentを
計算し、自己循環または複数node循環を`blocked_by_cycle`にする。

Cycle Resolution Recordは、誤辺除去、owner・方向訂正、共通前提Contract、版付きinterface
またはstub、phase分割、不可分Contract統合、上流再設計、defer、cancelの候補と判断を
保持する。循環解消後も親を直接再開せず、Contract、Plan、Context、checkpointのfreshnessと
staleを検査する。

### 5.6 Controlled Termination Protocol

`pause`は再開予定、`cancel`は現在のWork Item終了、`close-scope`はRequirementまたはRelease
scopeの上流改定候補とする。終了判断は理由、Evidence、代替案、最後の有効成果、未処理、
部分side effect、cleanup、rollback、移管先、再開条件、決定者を持つ。

cancelled Work Itemが必須Requirementを自動充足することはない。Requirementは`unfulfilled`
としてreleaseをblockするか、Humanが承認した新scope versionで`deferred`、`withdrawn`、
移管、不採用へ分類する。全残項目の処置、被覆、整合、移管先が確定しないclose-scopeを
completedとして扱わない。

## 6. TDD成果物

一つのTask Contract TDD cycleは次を関連付ける。

- Contractとsource Requirements
- challenge結果
- Plan bundle
- Acceptance TestとEvidence Test
- red確認証拠
- Source Symbol Index、Reusable Routine Ledger、Implementation Discovery Record
- LLM proposal、Human confirmation、retired routine verdict
- Design Decision
- Implementation change
- green確認証拠
- refactor変更、同一Acceptance Test identity、green再確認証拠
- risk-based verification
- conformance結果
- Definition Challenge結果とFinal Contract Challenge結果
- work origin、continuation mode、prior Work Item
- Upstream Inconsistency FindingとRevision Proposal
- Dependency Discovery、親checkpoint、cycle resolution
- pause、cancelまたはscope disposition判断
- Human acceptance
- Operational Provenance verdict

Test変更を禁止しない。RequirementまたはContractの期待が変わった場合、新Contract
version、変更理由、新Test versionを結び、同一Contractの実装都合による期待値変更と
区別する。

### 6.1 Verification Profile

Verification Planは`change_semantics`、`state_effect`、Contract risk、side effect、対象Policy
から版付きVerification Profileを選ぶ。初期Profileは既存開発方針の`low | medium | high`を
使い、必要なtest範囲、Challenge、独立性、reviewer数、Human判断、保存Evidenceを固定する。

- `editorial`と`evidence_only`：意味不変の根拠と参照整合を検査する
- `implementation_only`：現ContractとTestを維持し、riskに応じたtestを実行する
- `contract_semantic`：Definition Challenge、被覆、compile、redを新versionでやり直す
- `requirement_semantic`と`scope_semantic`：独立reviewを含むhigh profileを原則とする
- `external_or_irreversible`：意味不変でもhigh profileとHuman gateを要求する

一律の独立三者reviewやcommit gateをschemaへ固定しない。Profile選択根拠と実際に実行した
検証を別eventで保持し、必要なprofileを満たさない場合は`verified`へ進めない。

Definition ChallengeはContract versionごと、Conformanceは成果候補または成果versionごと、Final
Challengeはaccept前または上位・隣接影響の変更時を既定とする。stale後は影響を受けたVerdictだけを
再実行する。Verdict identityの分離を、全state transitionでの三重Run、固定reviewer数、固定round数、
一律Human gateへ読み替えない。

各validatorはValidator Assurance Profileとして、validatorと入力前提のversion、既知正例、負例、
境界例、mutationまたはfault injection、独立oracle、代表実データの要否を持つ。validatorまたは
前提変更時は旧verdictをstaleにし、必要fixtureを再実行する。Findingがゼロであることだけを
validatorの正しさのEvidenceにしない。

Review Quality Contractは固定verdict、severity、Finding schema、`insufficient_evidence`、
`out_of_level`、材料十分性、独立性、収束条件を持つ。書込みを伴うWorkはriskに応じて出力の再読込、
関連validator、stale閉包をpost-write verificationで確認し、未実行なら`verified`へ進めない。

## 7. Provenance Event設計

### 7.1 event共通field

全event共通のenvelopeは次へ限定する。

- `event_id`
- `event_type`
- `schema_version`
- `occurred_at`
- `actor_type`と`actor_identity`
- 該当する`project_id`、`work_item_id`、`run_id`、`attempt_id`
- `input_refs`と`input_digests`
- `output_refs`と`output_digests`
- `confidentiality_class`と`retention_class`
- `previous_event_id`
- `relations`

Requirement、Task Contract、obligation、state before／after、decision、reason、change semantics、
Verification Profile、execution conditions、duration、resource usage、costなどは、必要なevent typeの
payloadへ置く。全eventへ空または無関係なfieldを要求しない。共通envelopeとtype-specific payloadは
別schema versionを持てるが、event identityとtyped relationで一つのgraphとして検証する。

`relations`の各項目は`relation_type`、`target_type`、`target_id`、`target_digest`を持つ。
最初の閉じた関係語彙は次とする。

- `derived_from`
- `compiled_from`
- `satisfies`
- `evidences`
- `supersedes`
- `invalidates`
- `evaluates`
- `decided_by`
- `requires`
- `blocks`
- `discovered_during`
- `related_to`
- `resumes_from`
- `terminated_by`
- `matches`
- `reuses`
- `extends`
- `merges`
- `splits_from`
- `retires`

内容そのものを重複保存せず、不変成果物への参照とDigestを基本にする。
`previous_event_id`はappend順序だけを表し、意味的な依存関係は`relations`で表す。一つの
eventは複数の入力、成果、Evidence、判断へ関係を持てる。relationはevent typeごとの許可集合を
schemaで定め、すべてのeventが全relationを使用できる巨大共通schemaにしない。

### 7.2 event分類

- Contract lifecycle event
- Work routing、checkpoint、block、resume、termination event
- compilation event
- Context acquisition / selection / exclusion event
- Evidence extraction / classification / consumption closure event
- Assurance matrix compilation / enforcement event
- Context scope expansion / full consistency selection event
- permission and capability resolution event
- Workflow permit event
- execution / Tool / LLM / Human event
- artifact and side effect event
- Verification event
- validator assurance / post-write verification event
- Conformance / Challenge Finding event
- Human decision event
- Dependency discovery、cycle detection、cycle resolution event
- Upstream revision proposalとscope disposition event
- Policy overlay、adjustment、verification profile selection event
- Source Symbol Index generation、candidate search、reuse proposal、Human confirmation、
  routine consolidation／retirement／re-registration event
- Session ingestion、raw isolation、derivation、mutation、Context adoption event
- Session source availability、capture deadline、restore、restore verification event
- Improvement hypothesis、proposal、Human decision、owner application、next trial event
- deployment and migration event
- evaluation observation event

この分類は全低水準操作を耐久eventにする要求ではない。file read、symbol検索、個々のTest assertion、
debug logなどは、Contract、risk、side effect、復旧に必要なCapture Profileが要求する場合だけ運用または
診断eventとして取得する。

### 7.3 完全性

Capture PlanはContract type、risk、side effect、実行経路ごとの必須event集合と、次の保存層を持つ。

- 必須・耐久event：Contract、Plan、Context、Source Snapshot、Run、Verification、Decision、authority、
  permit、state、side effect、acceptance、stale、termination、integration、release
- 運用event：retry、checkpoint、lease、cache、増分更新、scope expansion
- 診断・raw data：debug log、詳細trace、raw response、session raw、performance sample
- 派生物：query index、metric、dashboard、graph cache、As-Built候補

Traceは必須・耐久event、関係、Digest、順序を検査する。欠落時はRun結果を削除せず、
`provenance_incomplete`としてWorkflowへ返す。authority変更または外部・不可逆side effectの前に必要な
eventはwrite-aheadで保存する。運用eventは安全性義務を損なわない範囲でbatch化でき、診断dataは
sampling、quota、rotation、期限付きretentionを適用できる。Decision、authority、state transition、
external send、acceptanceをsamplingしない。派生物は一次eventから再生成可能とし、同じretentionを
要求しない。

### 7.4 As-Built projection（後続開発）

As-Built projectionは新しい開発stageまたは独立した業務状態を追加せず、有効化された
Implementation Task ContractのVerification Planが要求する派生成果とverdictとして扱う。

```text
Task Contract / obligation
  + Operational Provenance
  + Test / Design Decision / Evidence
  + fixed source tree / Source Symbol Index / commit
  → As-Built Record
  → As-Built Documentation / Trace Matrix / change history
  → Documentation Conformance Verdict
  → verified | Upstream Revision Proposal | provenance repair
```

As-Built Recordは少なくとも次を持つ。

- `record_id`、`schema_version`、`projector_identity`、`projector_version`
- source Requirement、Task Contract、obligation、Work Item、RunのidentityとDigest
- source tree、commit、実装symbol、公開interface、data、state、error、side effect
- Test、Design Decision、Evidence、configuration、deployment、migrationへの参照
- 既知制限、未解決Issue、Provenance completeness
- `complete | partial | stale | conflicting`の状態
- 全入力Digestとprior accepted Recordへの`supersedes`関係

MarkdownはRecordから導出する人間向けviewであり、編集されたMarkdownを実装事実または
Requirementsの正本にしない。同じ固定入力とprojector versionから意味的に同じRecordを
再生成できなければならない。

Documentation Conformanceは順方向、逆方向、再現性の三検査を行う。順方向はobligationから
Test、Design Decision、Implementation、Evidenceの被覆を検査する。逆方向は固定source treeと
Source Symbol Indexから外部観測可能な実装を探索し、所有ContractまたはFindingへ帰属させる。
再現性検査は入力Digest、生成器version、出力Digestを検証する。Provenanceだけを入力にせず、
sourceとTestの独立照合を残す。

Finding分類は`unrealized_obligation`、`unattributed_implementation`、
`implementation_detail`、`upstream_inconsistency`、`provenance_incomplete`、
`stale_projection`とする。`implementation_detail`はAs-Builtだけへ反映できる。外部義務、
accept/reject、scopeを変える候補は仕様本文へ自動反映せず、Upstream Revision Protocolへ
渡す。Provenanceを持たない既存codebaseは標準projectionと混同せず、コード解析とHuman協働の
`legacy_reconstruction`へrouteする。

本節は設計上の後続契約を固定するが、Work 1〜8、最初のTask Contract、初期vertical slice、
初期releaseではprojector、Markdown renderer、独立legacy解析、verification gateを実装しない。
初期実装が必須とするのは、後からRecordを作れるidentity、relation、Digestの保存だけである。

## 8. Evaluation設計

### 8.1 記録層

- Operational Provenance：業務適合性に必須
- Evaluation Observations：評価用実測
- Outcome Labels：比較の基準値

### 8.2 Evaluation Profile

```text
EvaluationProfile
├── profile_id / version / digest
├── evaluation_questions
├── hypotheses
├── target_contract_types
├── required_observations
├── outcome_label_policy
├── baseline_definition
├── comparison_conditions
├── trial_design
│   ├── evaluation_case_id
│   ├── condition_id
│   ├── pair_id
│   ├── trial_index
│   ├── execution_order
│   ├── randomization / blinding / repetitions
│   └── model / tool / budget / configuration identities
├── metric_definitions
├── labeler / evaluator / confidence / adjudication
├── missing_data_policy
├── confidentiality
└── retention
```

Task ContractはEvaluation Profileを任意参照する。業務上必須でない観測の欠落は
`partially_evaluable`または`not_evaluable`を返すが、Contract conformanceを自動的に
失敗させない。

初期Pilotではrandomization、blinding、repetitionsを必須にしない。ただし未指定を
明示し、case、condition、pair、trial、実行順序、実行条件、評価者へ各比較値を逆引き
できなければならない。

Evaluation Profileは、Task applicability、Context adequacy、Controllability、
Dependability、Auditability、Adaptability、Verifiabilityの7軸へ仮説とmetricを対応
付けられる。この7軸は製品の合否条件ではなく、実務可用性を分析する評価分類とする。

### 8.3 初期metric

- Acceptance Criteria充足率
- Context obligation充足率
- Evidence Coverage
- source universeのbyte／token、変更単位数、影響閉包単位数
- Context候補、採用、除外、review payloadのbyte／token数
- source universeに対するpayload比、変更単位に対する影響閉包比
- `impact_slice | expanded_scope | full_consistency`の件数、拡大理由、追加量
- Finding Precision、Recall、採用率、責務外指摘率
- material adequacy、必須source消費率、未消費Finding数
- `insufficient_evidence`、`out_of_level`、post-write再検出件数
- validator既知欠陥検出率、正常fixture誤停止率、mutation生存数
- Provenance Completeness
- Contract作成、compile、red-to-green、acceptedまでの時間
- Contract、Test、Design、Implementationの改定回数
- Human問い合わせ数、承認時間
- Tool呼出、token、外部費用
- stale検出と再構築時間
- Work Item中断回数、blocking依存数、依存深さ、active leaf切替回数
- dependency cycle件数、解消方法、解消時間、未解消率
- pause、cancel、defer、close-scope件数と理由、投入済み時間・費用
- 上流改定の対象層、影響閉包、再作業時間
- reuse、extend、merge、split_with_rationale、no_candidateの件数
- 重複候補の事前検出率、候補誤判定、retired routine復活検出、再利用判断時間
- 手動設定数、自動導出率、設定不整合数

RecallとPrecisionは既知欠陥、注入欠陥、Human確定FindingなどOutcome Labelがある場合
だけ計算する。

### 8.4 Evaluation Ledger

Ledger entryはprofile、対象Run集合、metric version、baseline、結果、欠測、限界、
Human解釈を保持する。一次eventと過去projectionを上書きせず、新metric versionで
再計算した結果を追加する。

## 9. 配置設計

### 9.0 論理topologyとdeployment profile

論理責務は物理process、container、hostから分離する。

```text
Integration Client
  → Control Plane
      ├─ Task Contract Control
      ├─ Workflow / durable state
      ├─ Context and Policy resolution
      ├─ Decision / permit
      └─ Operational Provenance
  → Execution Plane
      ├─ Harnessed Execution
      ├─ LLM / Tool / Test adapters
      └─ output capture / checkpoint
```

Control Planeは何を、どの固定Planと権限で実行するかを所有する。Execution Planeはpermitに従う
実作業を行うが、Contract本文、Work Itemのauthority state、accepted verdictを変更しない。
workerはauthorityを持つ唯一のstateをprocess memoryまたはlocal一時fileだけに保持せず、Attempt、
side effect、capture、checkpointをdurable eventへ結ぶ。crash後は同じidentityを照合し、重複side
effectを防いで再開する。

deployment profileは次の3値とする。

| profile | 初期状態 | topology | 追加関門 |
|---|---|---|---|
| `local_integrated` | 初期実装対象 | 単一machine・単一利用者。論理境界は維持し、物理process数とtransportは固定しない | root分離、structured I/O、crash再開、stable／development分離 |
| `shared_runtime` | 後続 | 共有Control Planeとproject側Local Execution Agent | 認証、remote threat model、data locality、offline、通信障害、最小permission |
| `distributed_hybrid` | deferred | 複数Execution Worker、GPU／HPC等 | scheduler、重複実行、scale、tenant、costの実測Evidence |

profileは環境名だけでなく、component placement、endpointまたはlocal transport、state owner、failure
model、permission、supported capabilityをDeployment Manifestへ固定する。Docker、PostgreSQL、Object
Storage、Kubernetesなどはprofileの必須条件にせず、Design Decisionとdeployment E2Eで選ぶ。

### 9.1 論理root

```text
CODE_ROOT
CONFIG_ROOT
PROJECT_ROOT
DATA_ROOT
STATE_ROOT
LOG_ROOT
CACHE_ROOT
SENSITIVE_ROOT
EVALUATION_ROOT
```

`PROJECT_ROOT`以外は既定で対象repository外とする。`SENSITIVE_ROOT`はアクセス境界を
他のdataから分離できなければならない。

bootstrap Evidenceを保存する前に、各logical root、Git管理境界、相対参照基準、Project Manifest、
Project Binding、stable／development分離、所有・retention・削除、override優先順位をLayout Baseline Recordとして
固定する。空の配置fixtureで別checkoutとproject移動後のlink解決を確認する。baseline後のmanaged
path変更は通常のfile編集ではなく、新baseline version、影響閉包、全link検査、data migration、
rollbackを持つmigrationとして扱う。

### 9.2 project内配置

共有・version管理する候補は次とする。

```text
.reviewcompass/
├── contracts/
│   ├── portfolio.json
│   └── task-contracts/
├── policies/
├── requirement-maps/
├── design-decisions/
├── reuse/
│   └── shared-routines.json
└── verified-artifacts/
    └── as-built/                  # 後続開発でaccepted Recordと文書を配置
```

project内へ置かないものは次である。

- raw provider response
- 生セッションログ
- secretとcredential
- lockとcheckpoint
- cache
- 端末固有の絶対パス
- 未検査の機微情報

### 9.3 project外配置

```text
CONFIG_ROOT/
  reviewcompass3.json
  integrations.json

DATA_ROOT/projects/<project-id>/
  provenance/
  runs/
  contexts/
  compiled-plans/
  implementation-discovery/
    indices/
    records/
  as-built/                        # 後続開発の未検証projection

STATE_ROOT/projects/<project-id>/
  checkpoints/
  locks/
  scheduler/

LOG_ROOT/
  runtime/
  integrations/

CACHE_ROOT/projects/<project-id>/
  contexts/
  search/
  compiled/

SENSITIVE_ROOT/projects/<project-id>/
  raw/
  quarantine/
  sensitive-reports/

EVALUATION_ROOT/projects/<project-id>/
  observations/
  labels/
  projections/
  ledger/
```

### 9.4 Deployment Manifest

Deployment Manifestは次を持つ。

- deployment ID、owner、schema version
- deployment profile、environment role（`stable | development`）
- installed code identity
- supported-platform matrix identity
- logical root binding
- Control Plane／Execution Plane placement、endpointまたはlocal transport
- durable state owner、checkpoint store、failure model
- project binding
- integration binding
- owned resource inventory
- migration version
- permission、confidentiality、retention policy

解決優先順位は、明示CLI設定、versioned user setting、許可された環境変数、OS標準配置
の順とする。相対パスを受理する場合はProject内成果物だけに限定し、固定した
`PROJECT_ROOT`へ安全に解決する。Runtime rootは解決後の絶対パスとして検査する。

### 9.5 Project Binding

`project_id`はProject Manifestに永続保存したUUIDまたは明示的な安定IDとし、repository
絶対パスや可変なproject内容digestから生成しない。Project Manifestの内容identityは
`project_manifest_digest`として別に持つ。

Binding recordは`binding_id`、`project_id`、checkout instance、現在のrepository root、
取得時刻、検証結果を持つ。同一論理projectの複数checkoutは同じ`project_id`と異なる
`binding_id`で区別する。project移動後はBindingだけを更新し、Contract、project、成果物
identityを変えない。

### 9.6 Integration Manifest

Codex、Claude、IDEなどとの関係は次で表す。

- integration ID、adapter type、adapter version
- application identity
- source root
- hookまたはcommand
- allowed read / write root
- executableとconfiguration identity
- capability、permission、owner

開発アプリとReviewCompass3の隣接配置を前提にしない。adapterが未対応、source rootが
不明、権限が過剰、ownerが曖昧な場合は導入しない。

shared profileでは、Integration ManifestにLocal Execution Agentのidentity、version、project
binding、allowed operation、read／write root、command allowlist、credential scope、有効期間、
revocation、offline policyを追加する。共有Control Planeはlocal repositoryを直接mountする包括権限を
既定で持たない。Agentは固定requestとpermitの範囲だけを実行し、raw local dataを必要以上にserverへ
返さない。

### 9.7 distribution unit

初期の配布・更新単位を次へ分ける。

| unit | 内容 | 更新時の扱い |
|---|---|---|
| Runtime Core | Contract compile、Workflow、state、Provenanceのcodeとschema | install／migration／rollbackを必要とする |
| Integration Client | CLI、IDE hook、adapter入口 | Core compatibilityをManifestで検査する |
| Capability Adapter | LLM、Tool、command、test等の検証済み実行adapter | version、permission、side effect、ownerを固定する |
| Project Artifacts | Task Contract、Portfolio、Policy、Requirement map、Prompt、Design Decision | Runtime再deployなしにversion更新できる |

Project Artifactsは実行定義と入力であり、任意のexecutable codeを含めない。新しい実行方式が必要な
場合はCapability Adapterをinstalled codeとしてpreflight、verification、permission reviewへ通す。
汎用Task Registryまたはplugin loaderは初期範囲に含めない。

### 9.8 stable／development bootstrap

ReviewCompass3自身を開発するときは、確認済みstable deploymentとdevelopment candidateを別の
Deployment Manifest、CODE_ROOT、STATE_ROOT、DATA_ROOT、LOG_ROOT、CACHE_ROOTへ置く。共用可能な
project成果は明示Bindingとread／write authorityを持つ場合だけ共有する。

stable deploymentがdevelopment sourceとcandidate artifactをreviewし、candidateは自分自身の
release可否を決める唯一のoracleにならない。updateはcandidateをstaging rootへ配置し、旧stableで
migration dry-run、E2E、Provenance、rollbackを確認してから原子的にstable bindingを切り替える。
切替後のpost-write検証が失敗した場合は旧stable identityへ戻す。

## 10. install、update、uninstall

### install

1. 配布物identityとsupported platformを検証する。
2. 書込み前preflightでroot、権限、容量、衝突を検査する。
3. Deployment Manifestと所有対象を確定する。
4. code、config、integration、schedulerを段階的に配置する。
5. 各段階を再読込検証し、失敗時は完了済み操作を逆順に補償する。

### update

1. code schema、config schema、event schema、Contract schemaのmigration planを作る。
2. 既存dataを変更する前にbackup identityを固定する。
3. development candidateをstableと分離したstaging rootへ配置する。
4. 新旧runtimeで読める境界を明示し、旧stableからcandidateのmigration dry-runを検証する。
5. migrationとstable binding切替を追記型eventとして記録し、再読込照合する。
6. post-write検証失敗時は旧確認済み版とbindingへ戻す。

### uninstall

1. owned resource inventoryを検証する。
2. schedulerを停止し、hookとintegrationを解除する。
3. installed codeと所有configだけを削除する。
4. project成果、Provenance、Evaluation、利用者data、sensitive dataを既定で保持する。
5. data削除は別の明示操作とretention policyで行う。

## 11. 受け入れ試験差分

- source checkout、installed code、target project、全runtime rootを別場所に置いて
  Task Contract E2Eが完了する。
- `local_integrated`でControl／Executionのstructured I/Oを保ったまま単一processと分離processの
  いずれかを選べ、process topologyがContract identityを変えない。
- Execution WorkerをAttempt中に停止し、durable checkpointから重複side effectなしに再開できる。
- stableとdevelopmentが別root、Manifest、stateを使い、candidateがstable stateへ無許可で
  書き込めない。
- stableからcandidateのupdateを検証し、切替後失敗で旧stableへrollbackできる。
- `shared_runtime`を有効化するprofileでは、serverからlocal repositoryへの直接包括accessを拒否し、
  Local Execution Agentの期限付きallowlist内操作だけを許す。
- Project Artifactsだけの更新ではRuntime Coreの再installを要求せず、Capability Adapter追加では
  code verificationとpermission reviewを要求する。
- project移動後にBinding更新だけで同じContract identityを再利用できる。
- project内容変更で`project_id`が変わらず、manifestと成果物digestだけが更新される。
- 同一projectの複数checkoutが異なるBindingとして衝突なく解決される。
- 成果物内の未許可絶対パスを検出する。
- Contract obligationを一件落とすとcompileを拒否する。
- Plan項目のobligation参照を切るとRun permitを拒否する。
- 6 Plan viewが一つのbundle identityから決定的に生成され、viewを独立approvalまたは独立lifecycleへ
  変更すると拒否する。
- 必須Provenance eventを落とすと`verified`を拒否する。
- 任意の診断eventまたは再生成可能な派生indexだけを落としても、必須eventが完全なら業務成果を
  `provenance_incomplete`にしない。
- Evidence抽出候補を未分類にする、または採用Findingのconsumerを外すとContext充足を拒否する。
- Assurance Obligation Matrixのenforcement、permit効果、復旧、Evidenceを一つずつ外すとcompileを拒否する。
- validatorが既知違反を見逃すmutationを生存させず、既知正常例をblockingにしない。
- validatorまたは入力前提の変更後、fixture再実行なしに旧verdictを再利用できない。
- Evidence不足をFindingなしへ丸めず`insufficient_evidence`とし、責務外指摘を`out_of_level`で分離する。
- 書込み後にだけ現れる不整合をpost-write verificationで検出し、未実行時は`verified`を拒否する。
- 同じ変更単位、意味graph、閉包規則、Contract必須材料から同じ影響候補、採否、review
  payloadを再生成できる。
- source universeへ影響関係のない材料だけを追加すると、freshness再検査は行うが選択材料、
  payload byte数、payload token数は増えない。
- 意味関係辺またはContract必須材料を変更すると、影響閉包とpayloadが規則どおり変わり、
  prior Contextをstaleとして拒否する。
- 関係欠落、global invariantまたは横断Policyにより局所閉包を確定できない場合、暗黙に全文を
  追加せず、理由付きscope拡大、別の全文整合review、分割またはHuman escalationへrouteする。
- 許可条件、Decision Authority、拡大理由、追加材料を欠く`expanded_scope`または
  `full_consistency`を拒否し、budget超過による必須Evidenceの黙示的切捨ても拒否する。
- 後続開発のAs-Built能力を有効化したprofileでは、同じ固定入力とprojector versionから
  同じRecordを再生成し、source変更時に旧Recordを`stale_projection`と判定する。
- 後続開発の双方向照合では、未実現obligationと未帰属の外部観測可能実装を区別し、意味変更
  候補を本文更新ではなくUpstream Revision Proposalへ渡す。
- 任意Evaluation observationだけを落とすと`partially_evaluable`になる。
- Requirementを欠くContract fixtureをDefinition Challengeが実行前に検出する。
- Contract適合だが上位Intentまたは隣接Contractを損なうfixtureをFinal Contract
  Challengeが検出する。
- low riskの一Review RunがConformance、Definition、Finalの別Verdictを生成でき、high profileでは
  必要な独立reviewerまたはHuman gateの省略を拒否する。
- interface不整合、owner競合、局所成功・全体Intent不成立をIntegrationで拒否する。
- 一Contractの失敗がIntegration Planどおり全体verdictへ伝播する。
- new development / maintenanceとfresh / reopenの4組合せが共通Deliveryへrouteされる。
- 実装不良は現ContractとTestを維持し、Requirement不良は新versionとstale閉包を生成する。
- 誤字訂正とEvidence参照訂正は`acceptance_truth_changed: false`となり、Contract versionと
  workflow stateを変更しない。
- Acceptance Criteria、必須義務、scopeの変更は`acceptance_truth_changed: true`となり、
  意味的reopenと新versionへrouteされる。
- 軽微修正中に意味変更を検出すると処理を停止し、Upstream Revision Protocolへ切り替える。
- 同一変更でもriskとstate effectが異なれば異なるVerification Profileが選択され、
  profile未充足時は`verified`を拒否する。
- base PolicyとProject Policy Overlayから同じAgent entryを再生成でき、Overlay変更では
  依存するContractだけがstaleになる。
- 同じ固定source treeとgeneratorから同じSource Symbol Index identityを再生成できる。
- 全symbolを機械Indexへ収録したまま、LedgerのHuman確認をpublic、共有、high-risk、重複、retired、
  影響閉包へ限定し、対象外private helperの意味entry不足だけで`implementation_ready`を拒否しない。
- red確認後、類似候補を持つ新規関数はHuman確認済みの`reuse | extend | merge |
  split_with_rationale`がなければ`implementation_ready`へ進めない。
- `no_candidate`を4分類と混同せず記録し、候補なしの実装を不必要に停止しない。
- stale Index、理由のない`split_with_rationale`、retired routineの無断復活を拒否する。
- 再利用判断からsource tree、候補symbol、Ledger、Task Contract、Test、Design Decision、
  Implementation、commitへ逆引きできる。
- Ledger、Index、Discovery Recordのschema違反と閉じた語彙外判断を拒否し、Ledger書込み
  失敗注入後も直前の有効versionを読める。
- Session取込みなしでもSession obligationを持たないContractが実行できる。
- 許可範囲外Sessionを取込まず、raw／派生物へ別access、retention、削除Policyを適用する。
- Session rawから派生物を再生成でき、非追記変更または消失時に旧Context再利用を拒否する。
- Self Improvementが現行Workflow設定を直接変更しようとすると拒否する。
- Improvement Proposalを元Evaluation trial、Human判断、対象owner、新version、stale閉包、
  次trialへ逆引きできる。
- `A requires B requires C`ではCだけにpermitを発行し、完了後にB、Aを順に再検査する。
- `A requires B requires A`では両Work Itemを`blocked_by_cycle`としてpermitを拒否する。
- blockingでない境界外問題は親を止めずbacklogへ移す。
- pause後のreopenでfreshnessを再検査し、必要なら新Contract versionへrouteする。
- cancelした必須Requirementが`unfulfilled`としてreleaseをblockする。
- close-scopeは全残項目の処置とHuman判断がなければ拒否される。
- install途中失敗を注入し、所有対象だけを逆順補償する。
- update失敗後に旧成果を再読込できる。
- uninstall後もproject、Provenance、Evaluation、利用者dataが保持される。
- 権限のない主体がSENSITIVE_ROOTを読めない。
- macOS、Linux、Windows profileで論理rootとintegration dry-runを検証する。

## 12. 既存設計の分類方針

- `DES-REVIEW-CONTEXT`：adapt
- `DES-HARNESSED-EXECUTION`：adapt
- `DES-REVIEW-TRIAGE`：adapt
- `DES-SEMANTIC-TRACE`：adapt
- `DES-SESSION-RECORDS`：adapt
- `DES-WORKFLOW-CONTROL`：adapt
- `DES-PORTABLE-LIFECYCLE`：adapt
- `DES-EVIDENCE-EVALUATION`：adapt
- `DES-SELF-IMPROVEMENT`：adapt
- `DES-TASK-CONTRACT-CONTROL`：new
- `DES-AS-BUILT-PROJECTION`：defer（後続Task ContractでSemantic Traceへ追加）

component、interface、state machine、protocol、acceptance testの全件分類は
`2026-08-02-stage-five-to-task-contract-inheritance.md`へ固定する。旧固定本数とpoint-to-point
topologyは維持しないが、identity field、生成順、永続化順序、failure verdictを後継schema、
failure matrix、testへ移す。promotion前の差分監査では、固定commitの実装・テスト証拠と本
改定requirementsを入力に順逆被覆を確定する。
