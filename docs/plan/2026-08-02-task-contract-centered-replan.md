---
lifecycle: provisional
normative_status: current-plan-candidate
promotion_required: true
---

# Task Contract中心化によるReviewCompass3再計画

## 1. 目的

Task Contractを構造化RequirementsとRuntimeの間に置き、ReviewCompass3の開発段階を
大域的仕様形成と局所的TDD Deliveryへ再構成する。既存成果を捨てず、変更影響を
差分で扱い、最小E2Eで有効性と配置可能性を実測する。

## 2. 固定baseline

次を履歴baselineとして保持し、上書きしない。

- 2026-07-27 intent承認成果
- Feature Partitioningと37 requirements
- 2026-07-28第5段designと適合性監査候補
- 第5段構造化正本の9 design、29 interface、8 state machine、14 protocol、37 acceptance test
- 第0段から第2段の実装、テスト、Evidence
- 2026-08-02開発方針改定
- Task Contract centered engineeringの外部議論文書とDigest
- LLMGPで試行されたSDD/TDD hybridのAgent entry、Task ledger、dependency定義のDigestと
  そこから採用した運用規則
- ReviewCompass2のIssue／Plan実績、Issue→Plan粒度関門Issue、Plan独立レビューR1／R2の
  固定commit、artifact Digest、そこから採用する品質関門

第5段候補の状態は`awaiting_human_approval`である。本再計画は第5段完了を承認せず、
Task Contract差分を反映するための再開理由になる。

## 3. 新しい標準ステージ

今後のReviewCompass3開発は次を標準とする。

```text
Stage A: Intent
Stage B: Feature Partitioning
Stage C: Requirements
Stage D: Task Contract Portfolio
Stage E: Task Contract TDD Delivery
Stage F: Cross-Contract Integration
Stage G: Release Evaluation
```

### Stage A: Intent

目的、利用者、成功、非目標、原則、優先順位を確定する。実装方法と特定Runtime構造を
過剰に固定しない。ただしTask ContractをRequirementsとRuntimeの実行可能な中間表現
とする製品方針はintentへ置く。

### Stage B: Feature Partitioning

大域的責務、所有境界、依存、共有境界を分ける。Task Contract Controlを新Featureと
して追加し、既存componentの状態所有を維持する。

### Stage C: Requirements

外部から観測できる義務、入力、出力、停止、復旧、保存、受け入れ、対象外を定義する。
Task Contractへ写像可能なatomic obligationと由来を保持する。

### Stage D: Task Contract Portfolio

全Requirementの受け先、Contract間依存、risk、cross-contract acceptanceを固定する。
実行予定のないContractまで詳細化せず、未被覆と競合を検出できる最小定義にする。
依存辺追加時に循環を検査し、未解決blocking依存を持たない実行可能leafを識別する。

### Stage E: Task Contract TDD Delivery

Contract定義を`draft → challenged → approved`、Plan bundleを`compiled |
not_compilable`、Delivery Work Itemを`queued → active → red → implementation_ready →
green → verified → accepted`で進める。Design、旧Task記述、Implementationを全体段階に
せず、Contractの実現成果として作る。`implementation_ready`ではSource Symbol Index、
Reusable Routine Ledger、実コードを照合し、必要な再利用判断を確定する。green後は同一
Contract versionとAcceptance Testを維持してrefactorし、green再確認後にverifiedへ進む。

### Stage F: Cross-Contract Integration

accepted Delivery Work Itemに束縛されたContract間のinterface、共有状態、E2E、failure
propagation、配置、update、uninstallを検証する。局所Work Itemがすべて成功しても
全体Intentを満たさない場合、Portfolio、RequirementsまたはIntentへ戻す。版付き
Integration Plan、E2E Evidence、failure propagation Evidence、Integration Verdictを
成果とする。

### Stage G: Release Evaluation

supported-platform matrix、配布物、migration、データ保護、Provenance完全性、
Evaluation Profile、既存方式との比較結果を確認し、release可否をHumanが判断する。

### Development routing

SDD workflow、maintenance、reopenを独立engineとして実装しない。

```text
work_origin: new_development | maintenance
continuation_mode: fresh | reopen
```

4組合せを同じTask Contract Deliveryへrouteする。new developmentは必要に応じてIntent、
Feature Partitioning、Requirementsから開始する。maintenanceは既存baseline、invariant、
regression、compatibility、migration、rollbackを入力にし、義務変更時はRequirementsへ
戻る。reopenは旧成果を保持した新Work Item、RunまたはContract versionとして開始する。

### Cross-cutting Issue Resolution Path

Issue処理を新しい第8の全体Stageまたは独立実装engineにしない。問題、Finding、障害、改善
候補は、発見Stageにかかわらず次の横断経路へ入れる。

```text
Problem / Finding / Incident
  → Issue Record
  → Issue Triage and Disposition
  → Issue Resolution Plan
  → Plan Challenge
  → Intent / Feature / Requirements / Task Contract Portfolio / direct Work Item
  → compiled Plan bundle
  → Task Contract TDD Delivery
  → Resolution Verdict
```

Issueは観測した問題とEvidenceを、Issue Resolution Planは意味的な対処方針と作業分解を、
compiled Plan bundleはTask Contractから決定的に導出するRuntime設定を所有する。これらを
同じPlanまたは状態機械へ統合しない。Plan承認、Work Item完了、commit作成だけではIssueを
resolvedにせず、Acceptance Evidenceを持つResolution Verdictで閉じる。

現在の作業内で解消できず後日扱う問題、blocking依存、上流改定、複数作業にまたがる問題、
反復またはsystemicな問題、高risk問題はIssue Recordを必須とする。現在のContract内で即時に
訂正してEvidenceまで得られる一過性の実装誤りをすべてIssue化し、backlogを増殖させない。

## 4. フィードバック

ステージは一方向に凍結しない。戻り条件を明示する。

- Contract challengeで上位欠落を検出：Requirementsへ戻る
- 複数Featureの責務競合：Feature Partitioningへ戻る
- 成功条件または非目標の競合：Intentへ戻る
- compile不能：Contract、Policy、Capability Catalogの該当箇所へ戻る
- red testを定義不能：ContractまたはRequirementへ戻る
- TDD中の不整合：Implementation、Design、Contract、Requirement、Feature、Intentのうち
  変更が必要な最下位層へ戻る
- 受入条件の真偽・義務・scopeが変わらない訂正：stateを進めず、訂正理由とEvidenceを
  旧成果へ結ぶ
- 受入条件の真偽・義務・scopeが変わる訂正：軽微修正を中止し、意味的reopenへ移る
- blocking依存発見：親Work Itemを停止し、依存graphの単一active leafへ移る
- dependency cycle：全関係permitを停止し、PortfolioまたはArchitecture Policyへ戻る
- E2E不成立：Contract Portfolioまたはcross-contract interfaceへ戻る
- 評価不能：Capture PlanまたはEvaluation Profileへ戻る
- deploy不能：Portable RequirementまたはArchitecture Policyへ戻る
- IssueからPlanへの移送不足：Resolution Planを改定しPlan Challengeをやり直す
- Plan対象、Issue、Requirement、Policyまたはreview材料のDigest変更：旧Challenge合格を
  staleにし、実行permitを停止する

戻る場合は旧成果を削除せず、新versionと変更理由を結ぶ。

## 5. 現在地からの移行作業

### Work 1: 方針と固定入力

- 外部議論文書のDigestを固定する。
- 保存可能な原文はrepository内の不変snapshotへ保持し、source ID、capture日時、
  confidentiality、retention、artifact pathを記録する。保存しない場合は理由と
  `non_reconstructable`を明記する。
- 採用した議論をdecision ID、指示、意味、採否理由へ結ぶ。
- LLMGP先行実験を規範ではなく経験的Evidenceとして固定し、採用品と非採用品を区別する。
- ReviewCompass2の共通ルーチン台帳を前身の承認済み方針として固定し、P-5、
  `R-F6-010`、`R-F6-011`、DP-039、DP-040、実台帳の関係を記録する。
- ReviewCompass2のIssue／Plan schema、実案件、Issue→Plan粒度関門Issue、Plan review
  R1／R2を固定し、有効だった経路と未解決だった品質関門を区別する。
- Task Contractの適用範囲をReview Task Contractへ限定する。
- 旧第5段候補をbaselineとして凍結する。
- 本改定文書群のsource、関係、statusを記録する。
- `stage-five-design.json`と`stage-five-architecture-integrity.json`を要約Markdownではなく
  構造化baselineとしてDigest固定する。

完了条件：入力Digest、適用範囲、非目標、旧候補状態が一意である。

### Work 2: intent差分

- Task Contractのcontrol and provenance planeを追加する。
- 汎用Agent Runtime化を除外する。
- 二層review、最小権限、stale、配置非依存、評価可能性を追加する。
- 同一・類似関数の再利用、統合、理由付き分離と廃止routine復活防止を開発品質原則へ
  追加する。
- 問題を後日の実施計画へ結ぶ追跡性と、Plan品質を実装開始条件へ結線する原則を追加する。

完了条件：旧intentの維持事項と置換事項が競合なく区別され、Human判断候補になる。

### Work 3: requirements差分

- `FEAT-TASK-CONTRACT-CONTROL`を追加する。
- `REQ-CONTRACT-001`〜`007`を確定する。
- `REQ-WORKFLOW-005`〜`009`を確定する。
- Architecture Policyのidentity、競合、優先順位、stale伝播を`001`〜`003`へ組み込む。
- Project Policy Overlay、変更意味、state effect、risk別Verification Profileを組み込む。
- Definition ChallengeとFinal Contract Challengeを`004`で分離する。
- Cross-Contract IntegrationとIntegration Verdictを`007`で定義する。
- entry routing、Upstream Revision、Dependency Discovery、Controlled Terminationを
  `REQ-WORKFLOW-005`〜`008`で定義する。
- Source Symbol Index、Reusable Routine Ledger、Implementation Discovery Record、
  green実装前gateを`REQ-WORKFLOW-009`で定義する。
- `REQ-WORKFLOW-010`候補としてIssueの永続登録、triage、disposition、再検討を定義する。
- `REQ-WORKFLOW-011`候補としてIssue Resolution Plan、Plan Challenge、stale、
  Resolution Verdictを定義する。
- `REQ-CONTRACT-003`のPortfolio入力へHuman承認済みResolution PlanとIssue被覆を追加する
  差分を検討する。
- 既存37 requirementsを`preserve / adapt / replace / defer`へ全件分類する。
- Session Evidence Sourceの任意取込み、raw／派生物分離、mutation、access、retention、削除を
  既存`REQ-SESSION-001`〜`003`の差分として固定する。
- Self Improvementの直接設定変更を版付きImprovement Proposalへ置換し、既存
  `REQ-IMPROVE-001`〜`002`の差分として固定する。
- 新旧Requirementとatomic obligationの順逆被覆を検査する。

完了条件：未被覆、重複所有、未定義interface、未解決停止条件がない。

### Work 4: design差分

- Contract schema、Portfolio、Compiler、Plan bundleを設計する。
- Architecture Policy schemaと決定的なPolicy解決を設計する。
- Project Policy Overlay、Policy Adjustment Event、Agent entry生成を設計する。
- 既存Context、Workflow、Harness、Triage、Trace、Session Records、Portable、Evaluation、
  Self Improvementへ接続する。
- Contract lifecycleとfailure propagationを状態機械へ追加する。
- Provenanceの型付き複数関係、Evaluation trial identity、Deployment Manifest、安定した
  Project Identity、Bindingを設計する。
- Integration Plan、E2E Evidence、Integration Verdictを設計する。
- Contract、Work Item、Run、Portfolioの状態所有を分離する。
- work routing、upstream revision、dependency discovery、cycle resolution、controlled
  terminationのprotocolと状態機械を設計する。
- `acceptance_truth_changed`を中心とした軽微修正／意味的reopen分類と、変更意味・state
  effect・riskからのVerification Profile選択を設計する。
- 事実層のSource Symbol Index、意味層のReusable Routine Ledger、4分類の再利用判断、
  Human確認、retired routine検査、配置、Provenanceを設計する。
- Issue Record、Issue Disposition、Issue Resolution Plan、Plan Challenge Record、
  Resolution Verdictのschemaと独立stateを設計する。
- WorkflowがIssue lifecycle、Triageがduplicate／merge／conflict、Task Contract Controlが
  承認済みPlanからPortfolio／Contractへのroute、Semantic Traceが関係検証を所有するよう
  分担する。新componentは初期Pilotで不足が実証されるまで追加しない。
- Plan ChallengeをDefinition Challenge、Contract Conformance、Compiler validationと分離し、
  review目的、入力、Finding、verdict、実行permitへの効果を混同しない。
- Planまたは固定材料のDigest変更で旧Challengeをstaleにし、未解決blocking Findingがある
  Resolution PlanからWork Itemを開始できない状態遷移を設計する。
- 旧9 design、29 interface、8 state machine、14 protocolを`preserve / adapt / replace`へ
  全件分類し、旧表現を置換してもfailure verdictと永続化順序を維持する。
- 旧37 acceptance testを全件分類し、各旧test IDへ後継test IDとoracleを割り当てる。

完了条件：全新Requirementに受け先、interface、状態、acceptance testがある。

### Work 5: 最小Task Contract E2E

小さな仕様変更一件を対象に、次の一本を通す。

```text
Requirement
  → Review Task Contract
  → compile
  → Context Manifest
  → stub reviewer
  → Contract Conformance
  → Final Contract Challenge
  → Human decision
  → Provenance verdict
  → accepted artifact
```

初期実装では一Contract type、一Compiler version、一実行トポロジに限定する。
汎用DSL、plugin system、任意Task orchestrationを先に作らない。
最初のWork Itemは`new_development / fresh`とし、後続fixtureでmaintenanceとreopenを
同じDeliveryへ通す。

Review Task Contractの最小E2Eがstableになった後、ReviewCompass3自身の小さなhelper追加を
内部Implementation Task Contractとして一件だけ実行する。固定source treeからIndexを生成し、
red確認、候補探索、Human確認、`implementation_ready`、green、commitまでを通す。このPilotは
自己開発Evidenceであり、Implementation Task Contractを正式製品Runtime対象へ昇格しない。

Issue Resolution Pathは最小Review Task E2Eの前提にしない。E2Eがstableになった後、実在する
non-blocking Issue一件を選び、Issue Record、Triage、Resolution Plan、独立Plan Challenge、
Task Contract route、Resolution Verdictまでを手作業で一周する。最初からschema、CLI、
scheduler gateを実装せず、手作業Pilotで必須field、review観点、費用、停止条件を固定する。
ただしPilot対象Work Itemは、対象Digestに束縛したPlan Challenge合格がなければ開始しない。

### Work 6: TDD negative path

- Contract obligation欠落
- source Requirement未解決
- Plan被覆欠落
- Context不足
- capabilityまたはpermission過剰
- Contract変更後のstale
- crash後の再開
- 必須Provenance event欠落
- optional Evaluation observation欠落
- Contract適合だがRequirement欠落
- maintenanceが観測可能な義務変更を内包する
- reopen元のidentityまたは理由が欠落する
- TDD中の実装不良をRequirement変更として処理しようとする
- 意味不変の誤字・参照訂正でContract versionまたはworkflow stateを変更する
- Acceptance Criteria、義務またはscopeの変更を軽微修正として閉じる
- 軽微修正中に判明した意味変更をUpstream Revisionへ切り替えない
- high Verification Profileの独立reviewまたはHuman gateを省略する
- Project Policy Overlayの理由、Evidenceまたは置換元Policyが欠ける
- staleなSource Symbol Indexでgreen実装を開始する
- 類似候補がある新規関数に4分類またはHuman確認がない
- `split_with_rationale`に責務境界または分離理由がない
- retired routineを再登録判断なしに復活させる
- `no_candidate`を4分類へ混ぜ、存在しない候補判断を作る
- IssueとResolution Planの参照が切れている
- Issueの禁止事項、対象外、Human判断またはEvidenceがResolution Planへ移送されない
- 赤Testだけがあり、それをgreenにする実装作業がない
- Work Itemごとのexpected outcome、oracle、検証方法または完了判定が単独で閉じない
- Plan Challenge未実施またはblocking Finding未解決のPlanからWork Itemを開始する
- Issue、Plan、Requirement、Policyまたはreview材料の変更後に旧Challenge合格を再利用する
- Plan承認、commitまたはWork Item完了だけでIssueをresolvedにする
- deferred Issueに再検討条件、ownerまたは次回確認時点がない
- Session取込み範囲が未承認、rawと派生物が同一境界、mutationが未解決である
- Session contextが不要なContractをSession未取込みだけで停止する
- Self Improvementが版付きProposalとowner検証を経ず現行設定を変更する
- 旧interfaceまたはprotocolを置換した際にfailure verdict、期待終端、永続化順序を失う
- 旧acceptance testを後継testと義務対応なしに削除する
- blocking依存の親へRun permitを発行する
- `A requires B requires C`のactive leafを誤る
- `A requires B requires A`の循環中にRunを開始する
- cancelした必須Requirementを充足済みにする
- 未処理を分類せずclose-scopeする

各負例をredとして確認し、同じContract versionのAcceptance Criteriaを変更せず実装を
修正してgreenにする。green後はAcceptance Testを変更せずrefactorし、greenを再確認する。
RequirementまたはContract期待が誤っていた場合は新versionへ移り、Test変更理由を
記録する。

### Work 7: deployment E2E

- source checkoutとinstalled codeを分離する。
- target projectとruntime rootを別配置にする。
- Reusable Routine Ledgerをproject成果、Source Symbol IndexとDiscovery Recordを
  project外runtime dataとして別配置にする。
- Issue RecordとIssue Resolution Planを共有project成果、Plan Challengeのraw responseを
  project外runtime data、Human判断とResolution Verdictを共有可能なProvenanceとして
  分離配置する。
- OS標準配置、環境設定、明示overrideの優先順位を検証する。
- Project BindingとIntegration Manifestを検証する。
- project移動、update、migration、uninstallを検証する。
- sensitive storeの権限とretentionを検証する。
- project内容変更で`project_id`が変わらないこと、同一projectの複数checkoutを異なる
  Bindingとして扱えることを検証する。

### Work 8: evaluation Pilot

既存Review Task方式とTask Contract方式を、同じ対象、source universe、model、Tool、
budgetで比較する。

共通ルーチン照合は、同じRequirement、source tree、red Testを固定し、従来の実装探索と
Implementation Discovery gateの条件を分けて比較する。比較のために重複実装を製品成果へ
故意に統合せず、隔離fixtureまたは事前に期待判断を固定したcaseを使う。

各試行はevaluation case、condition、pair、trial、実行順序、model・Tool・budget設定、
label作成者、評価者、confidenceへ結ぶ。無作為化、盲検化、反復数はProfileで指定し、
初期Pilotで未指定の場合も未指定であることを記録する。

初期評価領域は次に限定する。

- Context obligation充足とContext量
- Finding Precision、Recall、責務外指摘率
- RequirementからEvidenceまでの追跡可能率
- Contract作成からacceptedまでの時間と再作業
- Human介入回数と判断時間
- 上流改定、blocking依存、cycle、pause、cancelの件数、理由、解消時間
- reuse、extend、merge、split_with_rationale、no_candidateの件数
- 重複実装の事前検出率、retired routine復活検出数、候補誤判定、Human確認時間
- Issue登録からtriage、Plan承認、Work開始、Resolution Verdictまでの時間
- Plan Challengeで実装前に検出した欠落、実現不能、禁止事項喪失、依存問題の件数
- Plan改定回数、実装後手戻り、stale合格再利用拒否、deferred滞留、false blocking、
  reviewerとHumanの負担
- Tool、token、費用、保存量

Pilot完了条件は優位性の確定ではなく、必要eventの取得、指標再計算、欠測、privacy、
比較可能性、記録負担を確認できることである。

## 6. 最初のTask Contract

最初のContractは、ReviewCompass3自身の小さな文書変更を対象とするReview Task
Contractとする。Implementation Task Contractを初回から正式Runtime対象にしない。

最初のContractへ含める最小責務は次である。

- 固定Requirementと変更Targetの適合性をレビューする
- source universeとScopeを固定する
- 必須Contextを構築する
- stub reviewerで決定的なFindingを得る
- ConformanceとChallengeを分離する
- Human判断を対象Digestへ束縛する
- Requirementからaccepted artifactまでをProvenanceで結ぶ

## 7. Designの扱い

独立した全体Design段階は廃止するが、設計判断は次に分けて保持する。

### Architecture Policy

複数Contractへ共通する制約を版付きで保持する。

- 原理Aの責務分担
- component state ownership
- ID、Digest、Schema
- securityとpermission
- external send
- Human decision
- storageとdeployment
- cross-contract interface
- Implementation Reuse Policy、4分類、retired routine policy

各Policyは`policy_id`、version、digest、owner、適用範囲、rule ID、優先順位、
supersedes関係、競合解決を持つ。未解決または同順位競合のPolicyはcompile入力にしない。

### Design Decision

一Contractまたは少数Contractに局所的な実現判断を保持する。

- 対象Contractとobligation
- alternatives
- selected design
- rationale
- affected TestとImplementation
- rollbackまたはreplacement条件

### Issue Resolution Planとcompiled Plan bundle

Issue Resolution Planは原因仮説、代替案、選択理由、scope、non-scope、禁止事項、作業項目、
依存、expected outcome、oracle、検証方法、risk、deployment、rollbackを保持する意味成果で
ある。compiled Plan bundleは承認済みTask Contractから導出するRuntime成果であり、Issue
Resolution Planの代替ではない。

ReviewCompass2第3版の「Acceptance Test参照だけを作業項目に置く」方式はそのまま採用しない。
Task ContractとResolution Planに期待、境界、禁止事項、oracleを残し、Testは実行可能な一つの
Evidenceとして参照する。Testで表現できないHuman判断、手順、全称否定、配布先検証、増加する
観測値には、manual acceptance種別と受け皿を明示する。

## 8. リスクベースTDD

既存開発方針を維持する。

- low：関連自動テスト
- medium：関連テストと全テスト
- high：全テスト、fault injection、代表データ、独立review

保存、削除、機微情報、権限、状態遷移、外部送信、migration、uninstall、Provenance
完全性は原則highとする。

Profileはartifact種別だけで固定せず、`change_semantics`、`state_effect`、risk、side effect
から選ぶ。editorialとevidence-only訂正は意味不変を検査し、Contract、Requirement、scopeの
意味変更は誤ったoracleをTDDだけで見逃さないよう独立reviewを含むhighを原則とする。

赤テストだけのcommitは必須にしない。統合対象commitは原則greenにする。文書、調査、
Contract候補探索には形式的なred-greenを強制しない。

問題発見を再帰的な実装stackにしない。境界外問題はDependency Discovery Recordへ移し、
WIPは未解決blocking依存を持たない単一active leafに制限する。親の部分変更はcheckpoint
として隔離し、依存解消後にfreshness、stale、compile、関連Testを再確認する。

## 9. Provenanceと評価の運用

各RunはCapture Planに従って一次eventを追記する。metricはeventを変更せず再計算する。

eventのappend順序は`previous_event_id`、意味的依存は閉じた語彙の複数`relations`で
記録する。比較評価に必要なcase、condition、pair、trial、実行条件、評価者も一次event
または参照先へ固定する。

project固有の運用調整は、base Policy、Project Policy Overlay、置換規則、理由、Evidence、
決定者、適用期間をPolicy Adjustment Eventへ固定する。Agent entryは解決済みPolicyから
生成し、手作業の追記だけを正本にしない。

- Operational Provenance欠落：Runをverifiedまたはacceptedにしない
- optional評価観測欠落：成果を保ち評価状態だけを下げる
- Outcome Label不足：Recallなど該当metricを計算しない
- metric変更：旧projectionを残して新versionで再計算する
- 改善反映：固定比較とHuman承認後だけ次周期へ適用する
- Session Evidence：取込み範囲、raw／派生物、mutation、Context採否を別eventで保持する
- Self Improvement：版付きProposalを各ownerへ渡し、stale検査後の次trialとして評価する
- Implementation Discovery：source／Index／Ledger、候補、4分類、Human確認、
  Design Decision、Test、Implementation、commitを結ぶ
- Issue Resolution：発見event、Issue、disposition、Resolution Plan全version、Plan Challenge、
  reviewer、Finding、Human判断、Task Contract、Work Item、Evidence、Resolution Verdictを結ぶ

Issue関係には少なくとも`reported_by / addresses / planned_by / challenged_by / duplicates /
merged_into / deferred_by / resolved_by`を閉じた候補語彙として検討する。Issue、Plan、review
材料のDigestとChallenge Policyを固定し、どれかが変われば旧Challenge verdictをstaleにする。

## 10. デプロイを最初から扱う規則

各Task Contractは、必要なlogical root、allowed read / write、integration、機密性、
retentionを宣言する。CompilerはDeployment Manifestへ解決できないContractを
`not_compilable`にする。

`project_id`はProject Manifestに保存した安定IDとし、内容digest、repository root、
checkoutごとのBindingから分離する。project移動と通常の内容変更ではBindingまたは
artifact digestだけを更新する。

実装中も開発checkoutのimportや相対配置だけで成功扱いにしない。少なくとも
distribution testでは別install root、別project root、別runtime rootを使用する。

Reusable Routine Ledgerは共有project成果として`PROJECT_ROOT`へ置く。Source Symbol Indexは
再生成可能な派生物、Implementation Discovery RecordはRun証拠として`DATA_ROOT`へ置く。
判断時の各DigestをProvenanceへ固定し、checkout移動時は絶対pathではなくProject Bindingを
更新する。

Issue RecordとIssue Resolution Planは`.reviewcompass/issues/`と
`.reviewcompass/resolution-plans/`を共有project成果の候補配置とする。model raw response、
一時review context、checkpointは`DATA_ROOT`または`SENSITIVE_ROOT`へ置く。Issue本文には
機微Evidenceの内容を複製せず、access-controlled artifactのidentityとDigestを参照する。

## 11. 停止条件

- Task Contractの適用範囲が汎用Agent Runtimeへ暗黙拡大した
- source RequirementまたはContract obligationの被覆が不明である
- Compilerが未対応obligationを黙って落とす
- Challenge Reviewの固定材料と完了条件がない
- Definition ChallengeとFinal Contract Challengeを区別できない
- Architecture Policyのidentity、適用範囲、優先順位または競合解決がない
- accepted Delivery Work Item間のIntegration Verdictを生成できない
- work originとcontinuation modeを同じ軸として扱い、独立レーンを重複実装する
- blocking依存または循環を持つWork ItemへRun permitを発行する
- 上流変更を実装都合で行う、または確定済み成果をin-placeで上書きする
- pause、cancel、close-scopeで未充足義務、cleanup、移管先またはHuman判断がない
- 必須Provenanceを保存できない
- 評価値とOperational verdictを混同する
- 開発checkoutまたは特定アプリ配置がruntime必須条件になる
- sensitive dataの分類、権限、retentionがない
- 第5段旧候補を変更後設計の承認証拠として再利用する
- source tree、Source Symbol Index、Reusable Routine Ledgerのいずれかを照合せず新規関数を
  実装する
- 類似候補の判断、Human確認、分離理由またはretired routine検査が欠ける
- Issue、Resolution Plan、compiled Plan bundle、Work Itemを同じidentityまたは状態機械へ
  押し込める
- IssueからPlanへ粒度、oracle、禁止事項、対象外または依存が移送されていない
- Plan Challengeのblocking verdictがWork Item開始permitへ結線されていない
- Planまたは固定材料の変更後も旧Challenge合格が有効なままである
- Plan承認またはWork Item完了をIssue解決Evidenceとして代用する

## 12. 新しい第5段相当の完了条件

- Task Contract中心intentがHuman判断済みである。
- 新requirementsと既存37 requirementsの差分被覆が完了している。
- Contract schema、Compiler、Plan、state、interface、deployment、evaluationが設計済みで
  ある。
- Architecture Policy、型付きProvenance関係、Project Binding、Integration Verdictが
  設計済みである。
- routing、upstream revision、dependency・cycle、controlled terminationが設計済みである。
- Session Evidence SourceとSelf Improvement Proposalが設計済みである。
- Source Symbol Index、Reusable Routine Ledger、Implementation Discovery、green実装前gate、
  4分類、retired routine検査が設計済みである。
- Issue Record、Issue Resolution Plan、Plan Challenge、Resolution Verdict、risk別review、
  stale、実行permit、Provenance、配置が設計済みである。
- Issue→Planの粒度、単独判定可能性、禁止事項保持、TDD closureを検査する受け入れ試験と、
  手作業Pilotの評価項目が確定している。
- 旧9 design、29 interface、8 state machine、14 protocol、37 acceptance testの全件に
  disposition、successor owner、後継testまたはfailure verdictがある。
- 新旧設計の`preserve / adapt / replace / defer`監査が完了している。
- 最小E2Eと負例のAcceptance Testが確定している。
- 未解決review Findingがない。
- 新しい承認候補が旧候補、変更理由、全Evidenceへ結ばれている。

## 13. 実装へ進む条件

新しい第5段相当の設計全体を巨大な基盤として先に実装しない。Humanが方向と最小
Contractを承認した後、Work 5の一本に必要な薄いvertical sliceから実装する。

E2Eで実測されていない汎用化、追加Schema、Contract type、adapter、評価指標はbacklogへ
置き、具体的な不足が確認されるまで必須化しない。

Issue Resolution Pathも同じ順序を守る。まず手作業Pilotと独立Plan Challengeを実施し、
次にschema validatorとProvenance記録をTDDで実装し、最後にWorkflow permitへ結線する。
未検証のIssue管理UI、外部tracker同期、汎用project-management機能は先に実装しない。
