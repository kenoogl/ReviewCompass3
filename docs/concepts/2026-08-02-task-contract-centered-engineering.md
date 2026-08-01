---
lifecycle: provisional
normative_status: successor-candidate
promotion_required: true
---

# Task Contract中心のReviewCompass3開発・実行構想

## 1. 位置付け

本文書は、Task ContractをReviewCompass3の要求、実行、検証、Provenanceを結ぶ
中心概念として採用する後継構想である。次の固定済み成果を破棄せず、導出関係を
再構成する。

- intentとFeature Partitioning
- 37 requirements
- Review Task、Execution Context、Review Runの概念
- Context、Harness、Triage、Trace、Workflow、Portable、Evaluationの各責務
- 第0段から第5段までに作成した実装、テスト、監査証拠

Task Contractは既存componentへ追加する独立文書ではない。構造化Requirementsから
局所的な実行責務を切り出し、Context、実行、能力、検証、Human介入、Provenanceを
同じ責務へ結び付ける、機械解釈可能な中間表現である。

## 2. 中心命題

ReviewCompass3は次の導出関係を正本とする。

```text
Intent
  → Feature Partitioning
  → Requirements
  → Task Contract Portfolio
  → versioned Task Contract
  → deterministic compilation
      ├─ Context Acquisition Plan
      ├─ Review / Execution Plan
      ├─ Harness and Capability Plan
      ├─ Verification Plan
      ├─ Provenance Capture Plan
      └─ Human Interaction Plan
  → Context Manifest
  → Harnessed Execution
  → Contract Conformance / Contract Challenge
  → Human decision
  → verified artifacts, evidence and state
```

これにより、何を実行するかだけでなく、次を同じContractから説明できるようにする。

- どのRequirementから責務を切り出したか
- 責務の内外と禁止された副作用は何か
- どのContextがなぜ必要か
- どのTool、権限、予算を使えるか
- 何を成果として生成するか
- 何を満たせば完了か
- どの証拠を残すか
- どの条件でHumanへ戻すか

## 3. 適用範囲

正式な製品対象は、ソフトウェア開発成果をレビューする`Review Task Contract`とする。
ReviewCompass3自身の開発では`Implementation Task Contract`を内部成果物として試行
できるが、stableな実行能力へ昇格するまではReviewCompass3自身の必須実行経路に
置かない。

Research Taskなど他領域のTask Contractは、比較・研究上の参照対象にはできるが、
ReviewCompass3の初期製品範囲には含めない。

## 4. Task Contractモデル

Task ContractはIdentityに加え、次の9領域を持つ。

```text
TC = <R, B, P, CO, C, O, A, V, E>
```

- `R: Responsibility`
- `B: Responsibility Boundary`
- `P: Preconditions`
- `CO: Context Obligations`
- `C: Allowed Capabilities`
- `O: Expected Outputs`
- `A: Acceptance Criteria`
- `V: Provenance Obligations`
- `E: Escalation Policy`

### 4.1 Identity

- `task_contract_id`
- `contract_type`
- `version`
- `source_requirement_ids`
- `prior_contract_id`
- `content_digest`
- `schema_version`

Identityは物理ファイルパスを永続identityにしない。Requirement、Contract、成果物は
安定IDと内容Digestで識別し、現在解決された物理パスは観測値として別に記録する。

### 4.2 ResponsibilityとBoundary

- goal
- obligations
- in-scope
- out-of-scope
- prohibited effects
- downstream responsibility
- completion owner

責務はRequirementへ逆引きできなければならない。必須Requirementに受け先がなく、
Humanが非採用を決められる閉じた例外にも該当しない場合、Contractを確定しない。

### 4.3 Preconditions

- required workflow state
- assumptions
- dependency Contract
- required policy version
- required platform capability
- freshness requirement

前提が未充足、競合、staleの場合はcompileまたはRun開始を停止する。

### 4.4 Context Obligations

各Context obligationは、Contract obligationへ結び、次を持つ。

- required evidence type
- authoritative source
- source universeとScope規則
- requiredまたはoptional
- freshness
- trust
- confidentiality
- token、時間、費用上限
- conflict policy
- satisfaction criteria

Contextは関連文書集合ではなく、Contract obligationを満たす実行時成果物として
構築する。

### 4.5 Allowed Capabilities

- allowed Toolとadapter
- read、write、network、API権限
- resource budget
- allowed side effects
- prohibited side effects
- Human approvalが必要な能力

能力の許可は、実際の主体identity、対象root、期限、目的へ束縛する。包括的、無期限、
対象不明の権限をContractから導出しない。

### 4.6 Expected OutputsとAcceptance Criteria

- output schema
- expected artifact
- allowed side effect
- acceptance criterion
- review criterion
- completion condition
- oracle type

TestはTask Contract全体の代替仕様ではない。Acceptance CriteriaまたはEvidence
Obligationを実行可能にしたoracleの一つとして扱う。

### 4.7 Provenance Obligations

- required nodeとedge
- required evidence
- retention
- execution recording
- evaluation observation
- confidentiality classification
- missing-data policy

Provenanceは実行後に可能な範囲で集めるのではなく、ContractからCapture Planを
事前に導出する。

### 4.8 Escalation Policy

- Human approval point
- unresolved condition
- failure policy
- retry policy
- Contract challenge condition
- Requirementへ戻す条件

Humanはすべての実行へ介入せず、意味的裁定、外部送信、不可逆操作、方針変更、
段完了などContract上の判断点へ選択的に参加する。

## 5. Task Contract Portfolio

Requirementsの後に、Task Contract Portfolioを作る。Portfolioは詳細実装計画ではなく、
次を機械検査するための母集合である。

- 全Requirementの受け先
- Contract間依存
- cross-contract acceptance条件
- Contractの優先度とリスク
- 対象外またはHuman非採用判断
- Contractの状態とversion

全Contractを最初から詳細化しない。Portfolio段階ではID、責務、Requirement対応、
依存、リスクを固定し、実行対象になったContractだけを完全な実行契約へ展開する。

## 6. Compilerと導出Plan

Task Contract Compilerは、Contractを状態変更せず、版付きPlanへ射影する決定的な
componentとする。Compiler version、Contract digest、Policy digestが同じ場合は、
同じPlan bundle identityを返さなければならない。

各Plan項目は一つ以上のContract obligation IDを持ち、Contract obligationは必要な
Planへすべて受け渡されなければならない。

### 6.1 Context Acquisition Plan

- 取得対象
- source universe
- Scopeと閉包規則
- 取得主体
- freshness、trust、confidentiality
- 変換と圧縮規則
- budget
- 充足検査

### 6.2 Review / Execution Plan

- 実行主体とトポロジ
- step順序
- 入出力
- 停止点
- retry
- Run終端条件

### 6.3 Harness and Capability Plan

- Prompt、Tool、Policy、Schema
- Provider、model、endpoint
- allowed rootと権限
- resource budget
- side effect
- external send gate

### 6.4 Verification Plan

- Acceptance Criteria
- Contract conformance criteria
- Contract challenge criteria
- testとvalidator
- machine、human、hybrid oracle
- completion verdict

### 6.5 Provenance Capture Plan

- 必須event
- node、edge、Digest
- raw、派生物、診断の保存境界
- Evaluation observation
- retention、削除、機密性

### 6.6 Human Interaction Plan

- 承認対象
- 判断主体と権限
- 提示材料
- 判断値
- 理由
- 未解決時の戻り先

Compilerが対応できないobligation、競合、未定義能力、未解決参照を検出した場合、
Planを部分的に成功扱いせず、診断付きの`not_compilable`を返す。

## 7. component責務

Task Contractをcontrol planeとしても、既存componentの状態所有責務は維持する。

- Task Contract Control：Contract、Portfolio、compile、obligation被覆
- Context Runtime：Context取得、構成、Manifest、freshness
- Workflow：active work、段階、Run permit、成果物書込み許可
- Harness：Run、Attempt、送信、capture、Validation、Retry内部状態
- Triage：Finding候補の保持、重複と競合
- Semantic Trace：意味グラフ、影響閉包、Operational Provenance検証
- Portable Lifecycle：配置、構造化I/O、機微情報、導入・解除
- Evidence Evaluation：評価基準、指標projection、解釈限界
- Self Improvement：比較結果から改善候補を提案し、Human承認後に反映

Task ContractまたはCompilerは、これらcomponentの状態を直接変更しない。Planを提供し、
各componentが自分の関門で受理または拒否する。

## 8. 開発ステージ

大域的な仕様形成はRequirementsまでとし、それ以降をTask Contract単位の反復へ
変更する。

```text
Intent
  → Feature Partitioning
  → Requirements
  → Task Contract Portfolio
  → Task Contract TDD Delivery Cycle
  → Cross-Contract Integration
  → Release Evaluation
```

従来の全体段階としてのDesign、Task記述、Implementationは廃止する。Designと
Implementation自体は廃止せず、各Task Contractを実現・検証する版付き成果物とする。

セキュリティ境界、状態所有、共通Schema、IDとDigest、外部送信、Human判断、
cross-contract interface、配置などの全体制約は、Requirementsまたは版付き
Architecture PolicyとしてTask Contractの前提にする。

Architecture Policyは`policy_id`、version、digest、適用範囲、owner、規則の優先順位、
supersedes関係を持つ。ContractとCompilerは適用Policyのidentityを固定し、未解決または
競合するPolicyを暗黙補完しない。影響するPolicyが変わった場合、依存するContract、
Plan、Context、Runだけをstaleにする。

## 9. Task Contract TDD Delivery Cycle

一つのContractは次の状態を進む。

```text
draft
  → challenged
  → approved
  → compiled
  → red
  → green
  → verified
  → accepted
```

### 9.1 draft

Requirementsから責務、境界、前提、Context、能力、成果、検証、来歴、
escalationを定義する。

### 9.2 challenged

Definition Challengeとして、Contractが狭すぎないか、Requirementを欠落していないか、
禁止副作用、依存、cross-contract責務が妥当かを実行前に検査する。

### 9.3 approved

意味的な責務境界、外部効果、Human判断点を確定する。機械的に決定可能な事項へ
包括的なHuman承認を要求しない。

### 9.4 compiled

Compilerが6種類のPlanを生成し、obligation被覆と参照を検証する。

### 9.5 red

振る舞いを持つContractのAcceptance CriteriaまたはEvidence Obligationをテスト化し、
未実装または変更前の挙動で満たされないことを確認する。

### 9.6 green

必要なDesign DecisionとImplementationによってテストを通す。Design Decisionは
Contract、Requirement、Test、Implementationへ結ぶ。green後は同じContract versionと
Acceptance Testを維持してrefactorし、関連テストが再びgreenであることを確認する。
refactorは独立した永続状態にせず、green内の版付き活動とeventとして記録する。

### 9.7 verified

関連テスト、リスクに応じた全テスト・fault injection・代表データ・独立レビュー、
Contract conformance、Provenance完全性を検証する。その後、Final Contract Challengeで
成果を含む状態が上位Intent、隣接Contract、安全性、配置を損なわないことを検査する。

### 9.8 accepted

Human判断が必要なContractだけ最終判断を記録し、cross-contract integrationへ
渡せる状態にする。

Contractまたは上流Requirementが変わった場合、`approved`以降をstaleとし、旧成果を
残した新versionとしてchallengeとcompileをやり直す。

## 10. 二層レビュー

### 10.1 Contract Conformance Review

- 宣言された責務を満たしたか
- 境界外変更がないか
- 禁止副作用がないか
- Preconditionsが維持されたか
- Context obligationとEvidence obligationが充足したか
- Acceptance Criteriaを満たしたか

### 10.2 Contract Challenge Review

- source Requirementsを取りこぼしていないか
- 境界が狭すぎないか、広すぎないか
- cross-contract gapがないか
- 安全性、権限、配置、Provenance要件が不足していないか
- Contractを満たしても上位Intentを損なわないか

Challengeは二つの時点で実行する。Definition ChallengeはContract確定前にRequirement
被覆、境界、能力、Policyを検査する。Final Contract ChallengeはConformance完了後に、
成果を含む状態で上位Intentと隣接Contractへの影響を検査する。両者のFinding、材料、
verdictを別identityで保持する。

Challengeは無制限の一般レビューにしない。source Requirements、Architecture Policy、
既知risk catalog、隣接Contractを固定材料とする。blocking分類は版付きChallenge
Policyで決め、機械判定不能な場合だけHumanへ送る。blockingなContract欠陥は
Requirementsまたは新しいContract versionへ戻し、実行結果だけを修正して閉じない。

## 11. Provenanceと評価

記録は3層へ分ける。

- Operational Provenance：実行とContract適合性を再構成する必須証拠
- Evaluation Observations：時間、費用、回数、欠測などの実測値
- Outcome Labels：既知欠陥、Human裁定、見逃し、手戻りなどの基準値

Operational Provenance欠落時は`verified`または`accepted`へ進めない。任意の評価値が
欠けた場合は成果を無効にせず、評価状態を`partially_evaluable`または
`not_evaluable`にする。

Evaluation ProfileはTask Contractと分離した版付き定義とし、仮説、必要観測、
baseline、比較条件、指標、欠測、privacy、retentionを持つ。Contractは必要な場合だけ
Evaluation Profileを参照し、CompilerがCapture Planへ観測を追加する。

評価値は一次eventを上書きせず、固定したmetric定義から再計算する。結果とHumanの
解釈、限界、方針判断を分離する。

一次eventは追記順を示す前eventだけでなく、`derived_from`、`compiled_from`、
`satisfies`、`evidences`、`supersedes`、`invalidates`、`evaluates`、`decided_by`などの
閉じた型付き関係を複数保持する。これにより、一つの結果へ複数のContract、Plan、
Context、Evidence、Human判断が寄与する場合も後から再構成できる。

## 12. デプロイと配置

開発checkout、インストール済みcode、対象project、runtime data、機微情報保存を
分離する。

```text
development checkout
  != installed code
  != target project workspace
  != runtime data
  != sensitive/raw store
```

物理的な相対位置を契約にせず、OS標準配置、明示設定、Deployment Manifest、
Project Binding、Integration Manifestから論理rootを解決する。

projectの論理identityはProject Manifestに保存した安定IDとする。project内容のdigest、
現在のrepository root、checkoutごとのBindingは別identityとして保持し、移動や通常の
内容変更でContractまたはprojectの論理identityを変えない。

主な論理区画は次とする。

- code installation
- user configuration
- project workspace
- runtime data
- runtime state
- logs
- cache
- sensitive/raw store
- evaluation store

プロジェクト内には共有すべきTask Contract、Requirement対応、Design Decision、
検証済み成果を置ける。raw response、生セッション、secret、lock、cache、端末固有の
絶対パスは置かない。

Codex、Claude、IDEなどの開発アプリとの関係は、隣接ディレクトリなどの推測ではなく、
adapter、source root、hook、実行command、権限、ownerを持つIntegration Manifestで
表す。

## 13. 検証仮説

初期評価では次を優先する。

- Task Contractで必要Evidenceの被覆が上がるか
- 不要Contextと責務外Findingが減るか
- Requirementから成果までの追跡可能率が上がるか
- Harness手動設定と設定不整合が減るか
- Human介入を必要な判断点へ限定できるか
- Contractまたは状態変更後に正しいContextとPlanを再構築できるか
- 追加手続きの時間、トークン、保存量が効果に見合うか

これらを、Task applicability、Context adequacy、Controllability、Dependability、
Auditability、Adaptability、VerifiabilityというLLMの実務可用性の評価軸へ対応付ける。
この7軸は製品Requirementではなく、Evaluation Profileで仮説とmetricを整理するための
非規範的な評価枠組みとする。

同じ対象、source universe、model、Tool、budgetを固定した既存方式との比較を行う。
初期Pilotは仮説証明ではなく、観測可能性、欠測、privacy、記録負担、指標再計算を
確認する。後続比較に必要なcase、condition、pair、trial、実行順序、model・Tool・budget
設定、label作成者、評価者、confidenceは初回から記録する。無作為化、盲検化、反復数は
Evaluation Profileで指定し、初期Pilotの一律必須条件にはしない。

## 14. 非目標

- 汎用Agent Runtimeを作ること
- Task ContractをRequirementの真実性や完全性そのものと扱うこと
- Contract外問題を無条件に無視すること
- LLMの非公開推論だけでContractまたはPlanを補完すること
- すべてのContext候補探索と採用を完全自律化すること
- 開発checkoutや特定アプリのファイル配置へruntimeを固定すること
- Provenanceを理由に機微情報を無制限に保存すること
- 記録数、テスト数、Contract数だけを品質指標にすること

## 15. 現行成果からの移行

既存のReview Task定義はTask Contract候補へ、Execution SpecとHarness contractは
compiled Plan候補へ、Execution ContextはContext Manifest候補へ位置付け直す。

既存componentは次のように扱う。

- preserve：Triage、raw capture、状態保存など責務が変わらない部分
- adapt：Context、Harness、Workflow、Trace、Portable、Evaluationのinterface
- replace：7項目だけのReview Task定義と、導出元を持たない個別設定
- defer：Research Taskなど初期製品範囲外のContract type

第5段の既存承認候補は固定baselineとして保持する。Task Contract差分を反映した
intent、requirements、design、受け入れ試験を作成し、新しい第5段相当の承認候補を
生成するまで完成設計として昇格しない。
