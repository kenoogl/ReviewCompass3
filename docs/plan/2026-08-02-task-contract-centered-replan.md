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
- ReviewCompassのconformance-evaluation要件・設計・実装の固定commitとDigest、そこから
  継承する実装由来差分、draft-only更新候補、reopen handoff、置換するcode-only逆推定

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

Issue処理を新しい第8の全体Stageまたは独立実装engineにしない。以下はWork 8の手作業Pilotで
検証する概念modelであり、初期製品の確定schemaまたは自動state machineではない。問題、Finding、
障害、改善候補を発見Stageにかかわらず扱えるか、次の横断経路で確認する。

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

手作業Pilotでは、現在の作業内で解消できず後日扱う問題、blocking依存、上流改定、複数作業に
またがる問題、反復またはsystemicな問題、高risk問題を暫定Issue記録の対象とする。現在の
Contract内で即時に訂正してEvidenceまで得られる一過性の実装誤りをすべてIssue化し、backlogを
増殖させない。正式な登録義務はPilot後のRequirements化で判断する。

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
- ReviewCompass2のfreeze原因と横断知見を固定し、Evidence Extraction Contractで探索開始集合、
  展開規則、分類、終了条件、除外、完全性oracleを定める。候補全件を採用、修正採用、不採用、
  保留へ分類し、採用知見のEvidence Consumption Closureを確認する。
- Task Contractの適用範囲をReview Task Contractへ限定する。
- 旧第5段候補をbaselineとして凍結する。
- 本改定文書群のsource、関係、statusを記録する。
- `stage-five-design.json`と`stage-five-architecture-integrity.json`を要約Markdownではなく
  構造化baselineとしてDigest固定する。

完了条件：入力Digest、適用範囲、非目標、旧候補状態が一意であり、必須sourceと採用Findingに
未分類または消費先なしがない。

### Work 1A: 配置baseline

bootstrap成果を保存する前に、論理root、Git管理境界、相対参照基準、Project Manifest、Project
Binding、stable／development分離、所有・retention・削除、path override優先順位をLayout Baseline
Recordへ固定する。空の配置fixtureで別checkoutとproject移動後の参照、Manifest、Binding、文書linkを
検査し、端末固有絶対pathがproject成果へ混入しないことを確認する。baseline後のmanaged path変更は
通常編集ではなく、影響閉包、link検査、rollbackを持つmigrationとして扱う。

### Work 1B: Session Log Bootstrap

Work 1Aの保存境界を使い、Work 2以降の議論、判断、調査、変更からSession Evidenceを残せる最小
capture profileを準備する。取込み対象と許可主体、session ID、source identity、開始・取得時刻、
capture deadline、content Digest、完全性、confidentiality、access、retention、mutation、source
availabilityを固定する。

rawは既定で`SENSITIVE_ROOT`、伏字化派生物、要約、索引は別identityで`DATA_ROOT`へ置く。rawから
派生物を再生成するrestore fixtureを確認し、取得不能、期限切れ、不完全取得を`source_missing |
source_expired | non_reconstructable`として正常な空sessionと区別する。これはbootstrap Evidence用の
最小基盤であり、Session Records製品機能の完成、外部送信、許可外取込み、無期限retentionを意味しない。

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
- `REQ-CONTRACT-008`として実装文書projectionの将来契約を確定するが、初期実装対象には
  含めない。
- `REQ-WORKFLOW-005`〜`009`を確定する。
- Architecture Policyのidentity、競合、優先順位、stale伝播を`001`〜`003`へ組み込む。
- Project Policy Overlay、変更意味、state effect、risk別Verification Profileを組み込む。
- Definition ChallengeとFinal Contract Challengeを`004`で分離する。
- Cross-Contract IntegrationとIntegration Verdictを`007`で定義する。
- entry routing、Upstream Revision、Dependency Discovery、Controlled Terminationを
  `REQ-WORKFLOW-005`〜`008`で定義する。
- Source Symbol Index、Reusable Routine Ledger、Implementation Discovery Record、
  green実装前gateを`REQ-WORKFLOW-009`で定義する。
- `REQ-WORKFLOW-010`と`011`は、Issueの永続登録、triage、Resolution Plan、Plan Challenge、
  stale、Resolution Verdictを扱うpost-Pilot仮説として名前だけを保持する。Work 8の手作業Pilot前に
  正式Requirement、製品schemaまたは実行permitを確定しない。
- `REQ-CONTRACT-003`のPortfolio入力へResolution PlanとIssue被覆を追加するかは、Work 8の
  手作業Pilotで必要性と粒度を確認した後に判断する。
- 既存37 requirementsを`preserve / adapt / replace / defer`へ全件分類する。
- Session Evidence Sourceの任意取込み、raw／派生物分離、mutation、access、retention、削除を
  既存`REQ-SESSION-001`〜`003`の差分として固定する。
- Self Improvementの直接設定変更を版付きImprovement Proposalへ置換し、既存
  `REQ-IMPROVE-001`〜`002`の差分として固定する。
- 新旧Requirementとatomic obligationの順逆被覆を検査する。

完了条件：未被覆、重複所有、未定義interface、未解決停止条件がない。

### Work 4: design差分と最初のslice選定

- Contract schema、Portfolio、Compiler、Plan bundleを設計する。
- Architecture Policy schemaと決定的なPolicy解決を設計する。
- Project Policy Overlay、Policy Adjustment Event、Agent entry生成を設計する。
- 既存Context、Workflow、Harness、Triage、Trace、Session Records、Portable、Evaluation、
  Self Improvementへ接続する。
- Context入力を変更単位からの影響閉包、Evidence抜粋、Contract必須材料で決定的に構成し、
  無関係な文書総量から分離する。広域scopeと全文整合reviewは理由付きの別modeとして設計する。
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
- Issue Resolution Pathについては、Work 8の手作業Pilotに必要な暫定owner、routing、記録項目、
  Plan Challenge観点だけを設計する。Issue Record等の製品schema、独立state、Workflow permit、
  自動stale判定はPilot結果を受けるDeferred Work 10まで確定しない。
- Assurance Obligation Matrix、Validator Assurance Profile、Review Quality Contract、
  Evidence Consumption Closure、post-write verificationを6 Plan内の横断成果として設計する。
- Session sourceの実効retention、capture deadline、source欠落／期限切れ／再構成不能、復元検証を
  Session Evidence SourceとPortable Lifecycleへ割り当てる。
- 旧9 design、29 interface、8 state machine、14 protocolを`preserve / adapt / replace`へ
  全件分類し、旧表現を置換してもfailure verdictと永続化順序を維持する。
- 旧37 acceptance testを全件分類する。最初のslice対象には後継test IDとoracleを割り当て、
  範囲外はsuccessor owner、依存、着手条件を持つ`deferred`として詳細化を後続Contractへ送る。

完了条件：全新Requirementに受け先または明示的deferがあり、最初のsliceにはinterface、状態、
acceptance testがある。範囲外の詳細設計は最小E2Eをblockしない。

### Work 4A: 関数台帳baseline

配置baseline後にsource treeとsymbol identity規則を固定し、既存の全関数・methodをSource Symbol
Indexへ機械収録する。Indexはsymbol ID、qualified name、kind、source path、signature、visibility、
参照関係、Test参照、content Digestを持ち、同一source treeから再生成できなければ完了しない。

再利用判断対象をReusable Routine Ledgerへ責務、入出力、side effect、制約、類似候補、利用箇所、
active／retired、後継、統廃合履歴とともに登録する。Index、Ledger、実codeのcoverage、freshness、
重複候補、retired routineをHumanが確認する。両baseline確定前に製品実装codeを追加せず、最初の
Implementation Task Contractへ`implementation_ready`を発行しない。
既存のIndex生成器がない場合、固定入力と出力schemaを持つ最小bootstrap生成器だけを隔離した
development toolingとして作成できる。独立Testとreviewを行い、最終Indexには生成器自身も収録する。
正式Runtime能力への流用は別Task Contractを必要とする。

### Work 5A: 最小Review Task Contract happy path

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

### Work 6A: 初期sliceのTDD negative path

- Contract obligation欠落
- source Requirement未解決
- Plan被覆欠落
- Context不足
- capabilityまたはpermission過剰
- Contract変更後のstale
- crash後の再開
- 必須Provenance event欠落
- Evidence抽出候補の未分類、または採用Findingのconsumer欠落
- 規則の宣言はあるがenforcement、permit効果、復旧、Evidenceのいずれかがない
- validatorが既知違反を見逃す、正常fixtureを誤ってblockingにする
- validator変更後にfixture再実行なしで旧verdictを再利用する
- Evidence不足をFindingなしに丸める、責務外Findingを混在させる
- 書込み後にだけ生じる不整合をpost-write verificationしない
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
- 赤Testだけがあり、それをgreenにする実装作業がない
- Work Itemごとのexpected outcome、oracle、検証方法または完了判定が単独で閉じない
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

AI委譲、用語Runtime統制、Issue Resolution automation、Session拡張、Self Improvementなど
初期slice外の負例はDeferred Acceptance Catalogへ保存する。対象能力のTask ContractがPortfolioへ
入った時点でredとして有効化し、初期Review Task Contractの完了をblockしない。

### Work 5B: 内部Implementation Task Contract Pilot

Work 6Aの中核負例がgreenになった後、ReviewCompass3自身の小さなhelper追加を一件だけ実行する。
red、固定source tree、Index、Ledger、候補探索、Human確認、`implementation_ready`、green、台帳更新、
post-write verification、commitを通す。このPilotは自己開発Evidenceであり、Implementation Task
Contractを正式製品Runtime対象へ昇格しない。

### Work 7A: `local_integrated`最小deployment E2E

- source checkoutとinstalled codeを分離する。
- target projectとruntime rootを別配置にする。
- Reusable Routine Ledgerをproject成果、Source Symbol IndexとDiscovery Recordを
  project外runtime dataとして別配置にする。
- Issue RecordとIssue Resolution Planを共有project成果、Plan Challengeのraw responseを
  project外runtime data、Human判断とResolution Verdictを共有可能なProvenanceとして
  分離配置する。
- OS標準配置、環境設定、明示overrideの優先順位を検証する。
- Project BindingとIntegration Manifestを検証する。
- project移動と複数checkoutを検証する。
- sensitive storeの権限とretentionを検証する。
- project内容変更で`project_id`が変わらないこと、同一projectの複数checkoutを異なる
  Bindingとして扱えることを検証する。

### Work 8: evaluation Pilot

既存Review Task方式とTask Contract方式を、同じ対象、source universe、model、Tool、
budgetで比較する。

変更規模比例の検証では、同じ変更、意味graph、Contract材料を固定したままsource universeへ
無関係な材料だけを追加するpaired trialと、意味関係辺を変更して影響閉包を広げるtrialを行う。
`source_universe_bytes`、`changed_unit_count`、`impact_closure_unit_count`、
`review_input_bytes`、`review_input_tokens`、selection mode、scope拡大理由を一次観測へ残す。

共通ルーチン照合は、同じRequirement、source tree、red Testを固定し、従来の実装探索と
Implementation Discovery gateの条件を分けて比較する。比較のために重複実装を製品成果へ
故意に統合せず、隔離fixtureまたは事前に期待判断を固定したcaseを使う。

Issue Resolution Pathはここで初めて手作業Pilotする。実在するnon-blocking Issue一件を選び、
暫定Issue記録、Triage、Resolution Plan、独立Plan Challenge、Task Contractへのroute、
Resolution Verdictまでを一周する。製品schema、CLI、scheduler gateは実装せず、必須field、
owner、review観点、費用、停止条件、stale条件を観測する。Pilot対象Work Itemは、対象Digestに
束縛したPlan Challenge合格がなければ開始しない。

各試行はevaluation case、condition、pair、trial、実行順序、model・Tool・budget設定、
label作成者、評価者、confidenceへ結ぶ。無作為化、盲検化、反復数はProfileで指定し、
初期Pilotで未指定の場合も未指定であることを記録する。

初期評価領域は次に限定する。

- Context obligation充足、source universe量、変更単位数、影響閉包、review入力byte／token数
- 無関係材料追加時のpayload不変性、scope拡大率、拡大理由、追加量
- Finding Precision、Recall、責務外指摘率
- material adequacy、必須source消費率、未消費Finding、`insufficient_evidence`、`out_of_level`
- validator既知違反検出率、正常fixture誤停止率、mutation生存数、post-write再検出
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

### Work 7B: lifecycle deployment E2E

Work 8で最小方式の観測可能性を確認した後、update、migration、uninstall、stableからcandidateへの
staging、migration dry-run、原子的切替、rollbackを検証する。Layout Baselineの変更が必要な場合は
通常のfile移動で直さず、新baseline version、全link検査、data migration、rollbackを先に通す。

### Deferred Work 9: 実装文書projection

Task Contract TDDのaccepted成果から、Operational Provenance、Test、Design Decision、
Implementation、Source Symbol Indexを固定入力としてAs-Built Recordを生成し、人間向け
As-Built Documentation、Trace Matrix、変更履歴、drift reportを再生成する。Requirementsと
Task Contractは規範正本のままとし、意味変更候補は本文へ自動反映せずUpstream Revision
Proposalとreopenへ渡す。Provenanceのない既存codebase向けには、旧conformance-evaluationの
コード解析とHuman協働を`legacy_reconstruction`として補助的に継承する。

本Workは初期開発へ入れない。Work 1〜8、最初のTask Contract、初期vertical slice、初期製品
releaseの完了条件またはblocking依存にしない。初期開発は、後からprojectionできるidentity、
relation、DigestをProvenanceへ保存するところまでを担う。

着手判断は、次を満たした後にHumanが行う。

- acceptedされたImplementation Task Contractと実運用Provenanceが一件以上ある
- source symbol、Test、Design Decision、commitまでの必須関係と欠測が実測されている
- 生成文書の利用者、更新頻度、保存価値が確認されている
- project内accepted成果とproject外暫定projectionの配置がdeployment E2Eで検証済みである
- 初期開発のblocking問題より優先する根拠がある

着手後は、単一Task Contractの機械可読Record、決定的再生成、双方向trace、stale検出を
最小sliceとする。Feature集約文書、LLMによる説明改善、legacy reconstruction、独立コード
監査は、その最小sliceの評価後に段階導入する。

### Deferred Work 10: Issue Resolution automation

Work 8の手作業Pilotで必須field、owner、停止条件、stale条件、費用が確認された後に、別の
Task Contractとして着手を判断する。最初のsliceで`REQ-WORKFLOW-010`と`011`の正式化、Issue Record、
Resolution Plan、Plan Challenge、Resolution Verdictのschema validator、Provenance記録をTDDで
実装する。その検証後にだけWorkflow permitへ結線する。Issue管理UI、外部tracker同期、汎用
project-management機能は対象外とする。

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

As-Built Record、実装文書renderer、Documentation Conformance gate、legacy reconstructionは
最初のContractに含めない。ただし将来のprojectionに必要なidentity、relation、Digestを
失わないProvenance記録は含める。

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

能力固有の条件は、その能力または対応Task Contractが現在のscopeに入った時だけ適用し、
Deferred能力を初期sliceの暗黙依存にしない。

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
- Layout Baselineが未確定、またはmanaged path変更をlink検査とmigrationなしで行う
- Session Log Bootstrapの取込み範囲、raw保存境界、access、retention、source availability記録、
  restore fixtureが未確定である
- sensitive dataの分類、権限、retentionがない
- 第5段旧候補を変更後設計の承認証拠として再利用する
- source tree、Source Symbol Index、Reusable Routine Ledgerのいずれかを照合せず新規関数を
  実装する
- 類似候補の判断、Human確認、分離理由またはretired routine検査が欠ける
- Issue Resolution automationがscope内なのに、Issue、Resolution Plan、compiled Plan bundle、
  Work Itemを同じidentityまたは状態機械へ押し込める
- Issue Resolution automationがscope内なのに、IssueからPlanへ粒度、oracle、禁止事項、対象外、
  依存が移送されない、またはPlan Challengeのblocking verdictが開始permitへ結線されない
- Issue Resolution automationがscope内なのに、固定材料変更後の旧Challenge合格、Plan承認、
  Work Item完了をIssue解決Evidenceとして代用する
- 必須sourceまたは採用Findingにconsumerがなくても材料抽出を完了とする
- PolicyまたはContractの宣言だけで、runtime enforcement、停止、復旧、Evidenceを保証済みとする
- validator自体の正例、負例、境界例を検証せず、Findingゼロを品質保証に使う

## 12. 新しい第5段相当の完了条件

- Task Contract中心intentがHuman判断済みである。
- 新requirementsと既存37 requirementsの差分被覆が完了している。
- 全50 Requirementに受け先または明示的deferがあり、最初のReview Task Contractに必要な
  Contract schema、Compiler、Plan、state、interface、deployment、evaluationが詳細設計済みである。
- 最初のsliceに必要なArchitecture Policy、Provenance、Project Binding、Integration、routing、
  upstream revision、dependency・cycle、controlled terminationが設計済みである。
- Layout Baselineが固定され、空の配置fixtureで相対参照、Manifest、Binding、project移動を
  確認済みである。
- Session Log Bootstrapでraw／派生物の分離、capture deadline、source availability、mutation、
  restore fixtureが確認済みであり、Work 2以降のEvidenceを記録できる。
- Source Symbol IndexとReusable Routine Ledgerの初期baseline、coverage、freshness、重複候補、
  4分類、retired routine検査がHuman確認済みである。
- Issue Resolution Pathの暫定owner、routing、手作業Pilotの記録項目と評価項目が確定し、製品
  schema、正式Requirement、実行permitがDeferred Work 10へ明示的に分離されている。
- Evidence Extraction Contract、Consumption Closure、Assurance Obligation Matrix、Validator
  Assurance Profile、Review Quality Contract、post-write verificationのownerと負例が確定している。
- 実装文書projectionがdeferred Workとしてowner、成果物、配置、着手条件まで定義され、
  初期Workと初期releaseをblockしない。
- 旧9 design、29 interface、8 state machine、14 protocol、37 acceptance testの全件に
  dispositionとsuccessor ownerがあり、最初のslice対象には後継testまたはfailure verdictがある。
- 新旧設計の`preserve / adapt / replace / defer`監査が完了している。
- 最小E2EとWork 6Aの負例が確定し、Deferred Acceptance Catalogが初期完了条件から分離されている。
- 未解決review Findingがない。
- 新しい承認候補が旧候補、変更理由、全Evidenceへ結ばれている。

## 13. 実装へ進む条件

新しい第5段相当の設計全体を巨大な基盤として先に実装しない。Humanが方向、Layout Baseline、
Session Log Bootstrap、関数台帳baseline、最小Contractを承認した後、Work 5Aの一本に必要な薄い
vertical sliceから実装する。

初期順序は`Work 1 → Work 1A → Work 1B → Work 2 → Work 3 → Work 4 → Work 4A → Work 5A →
Work 6A → Work 5B → Work 7A → Work 8 → Work 7B`とする。その後は実測された不足だけを次
Task Contractへ送り、関連ContractがacceptedになるたびにCross-Contract Integrationを反復する。

E2Eで実測されていない汎用化、追加Schema、Contract type、adapter、評価指標はbacklogへ
置き、具体的な不足が確認されるまで必須化しない。

As-Built projector、文書renderer、Documentation Conformance gate、legacy reconstructionも
このbacklogに置く。初期開発中に個別Markdown生成が便利でも正式Runtime能力へ昇格させず、
Deferred Work 9の着手条件と新しいTask Contractを経て実装する。

Issue Resolution Pathも同じ順序を守る。まず手作業Pilotと独立Plan Challengeを実施し、
次にschema validatorとProvenance記録をTDDで実装し、最後にWorkflow permitへ結線する。
未検証のIssue管理UI、外部tracker同期、汎用project-management機能は先に実装しない。
