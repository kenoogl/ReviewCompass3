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

既存の第5段承認候補は`awaiting_human_approval`のまま上書きしない。本改定と対応する
構造化設計、受け入れ試験、適合性監査が完成した後、新しい承認候補を生成する。

## 2. 設計原則

- Task ContractをRequirementsとRuntime間のcontrol and provenance planeにする。
- Task ContractとCompilerは宣言とprojectionを所有し、consumer状態を変更しない。
- Plan生成をLLMの非公開推論に委ねず、決定的validatorで検査する。
- Runtimeで観測する非決定値は、入力条件と結果を固定して後段へ渡す。
- Contract conformanceとContract challengeを分離する。
- Operational ProvenanceとEvaluation Observationsを分離する。
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

### 3.3 Compiler

Compilerは純粋なprojection coreと、外部capability catalogを解決するvalidation境界に
分ける。

```text
Contract + fixed Policy + fixed Catalog
  → normalize
  → validate references
  → project six Plans
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
- 6 PlanのIDとdigest
- obligation coverage map
- unresolvedとdiagnostic

一つでも必須Planが生成不能または被覆不足の場合、bundleは`not_compilable`であり、
consumerへ開始可能なPlanとして渡さない。

## 4. 既存componentの改定

### 4.1 Review Context

Review ContextはTask定義を所有しない。Context Acquisition Planを受け取り、候補取得、
Scope分類、Composition、Manifest、freshnessを所有する。

Context Manifestへ追加する項目は次である。

- ContractとPlan identity
- Context obligation ID
- selected sourceとversion
- transformation chain
- excluded candidateと理由
- unresolved obligation
- contradiction
- trustとfreshness verdict
- token、時間、費用
- confidentiality class

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
  → Run / Attempt
  → Result / Evidence
  → Dependency / Revision / Termination decision
  → Conformance / Challenge
  → Human decision
  → accepted artifact
```

各Plan項目とRuntime eventはContract obligationへ逆引きできなければならない。

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
  └─ tests_passed → green

green
  ├─ refactor_completed_and_tests_passed → green
  ├─ verification_failed → revision_pending
  └─ verification_passed → verified

verified
  ├─ final_challenge_blocking → revision_pending
  └─ acceptance_granted_or_not_required → accepted

queued | active | red | green | verified
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

## 7. Provenance Event設計

### 7.1 event共通field

各eventは最低限、次を持つ。

- `event_id`
- `event_type`
- `schema_version`
- `occurred_at`
- `actor_type`と`actor_identity`
- `requirement_ids`
- `task_contract_id`、`version`、`digest`
- `obligation_ids`
- `run_id`と任意の`attempt_id`
- `state_before`と`state_after`
- `input_refs`と`input_digests`
- `output_refs`と`output_digests`
- `decision`と`reason`
- `change_semantics`、`acceptance_truth_changed`、`state_effect`
- `verification_profile_id`、`version`、`digest`
- `execution_conditions`
- `duration`、`resource_usage`、`cost`
- `confidentiality_class`
- `retention_policy`
- `previous_event_id`
- `relations`

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

内容そのものを重複保存せず、不変成果物への参照とDigestを基本にする。
`previous_event_id`はappend順序だけを表し、意味的な依存関係は`relations`で表す。一つの
eventは複数の入力、成果、Evidence、判断へ関係を持てる。

### 7.2 event分類

- Contract lifecycle event
- Work routing、checkpoint、block、resume、termination event
- compilation event
- Context acquisition / selection / exclusion event
- permission and capability resolution event
- Workflow permit event
- execution / Tool / LLM / Human event
- artifact and side effect event
- Verification event
- Conformance / Challenge Finding event
- Human decision event
- Dependency discovery、cycle detection、cycle resolution event
- Upstream revision proposalとscope disposition event
- Policy overlay、adjustment、verification profile selection event
- deployment and migration event
- evaluation observation event

### 7.3 完全性

Capture PlanはContract typeと実行経路ごとの必須event集合を持つ。Traceは必須event、
関係、Digest、順序を検査する。欠落時はRun結果を削除せず、`provenance_incomplete`として
Workflowへ返す。

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
- Context候補、採用、除外、token数
- Finding Precision、Recall、採用率、責務外指摘率
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
- 手動設定数、自動導出率、設定不整合数

RecallとPrecisionは既知欠陥、注入欠陥、Human確定FindingなどOutcome Labelがある場合
だけ計算する。

### 8.4 Evaluation Ledger

Ledger entryはprofile、対象Run集合、metric version、baseline、結果、欠測、限界、
Human解釈を保持する。一次eventと過去projectionを上書きせず、新metric versionで
再計算した結果を追加する。

## 9. 配置設計

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
└── verified-artifacts/
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
- installed code identity
- supported-platform matrix identity
- logical root binding
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
3. 新旧runtimeで読める境界を明示する。
4. migrationを追記型eventとして記録し、再読込照合する。
5. 失敗時は旧確認済み版へ戻す。

### uninstall

1. owned resource inventoryを検証する。
2. schedulerを停止し、hookとintegrationを解除する。
3. installed codeと所有configだけを削除する。
4. project成果、Provenance、Evaluation、利用者data、sensitive dataを既定で保持する。
5. data削除は別の明示操作とretention policyで行う。

## 11. 受け入れ試験差分

- source checkout、installed code、target project、全runtime rootを別場所に置いて
  Task Contract E2Eが完了する。
- project移動後にBinding更新だけで同じContract identityを再利用できる。
- project内容変更で`project_id`が変わらず、manifestと成果物digestだけが更新される。
- 同一projectの複数checkoutが異なるBindingとして衝突なく解決される。
- 成果物内の未許可絶対パスを検出する。
- Contract obligationを一件落とすとcompileを拒否する。
- Plan項目のobligation参照を切るとRun permitを拒否する。
- 必須Provenance eventを落とすと`verified`を拒否する。
- 任意Evaluation observationだけを落とすと`partially_evaluable`になる。
- Requirementを欠くContract fixtureをDefinition Challengeが実行前に検出する。
- Contract適合だが上位Intentまたは隣接Contractを損なうfixtureをFinal Contract
  Challengeが検出する。
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
- `DES-SESSION-RECORDS`：preserveまたはadapt
- `DES-WORKFLOW-CONTROL`：adapt
- `DES-PORTABLE-LIFECYCLE`：adapt
- `DES-EVIDENCE-EVALUATION`：adapt
- `DES-SELF-IMPROVEMENT`：adapt
- `DES-TASK-CONTRACT-CONTROL`：new

最終分類は、固定commitの実装・テスト証拠と本改定requirementsを入力にした差分監査で
確定する。
