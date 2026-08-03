---
lifecycle: provisional
normative_status: consolidated-successor-candidate
document_role: terminology
promotion_required: true
generated_at: 2026-08-03
generated_from:
  - path: records/sources/2026-08-02-source-catalog.json
    sha256: 1a40adcec2af6c9f2829af9f4a90cc33bfe6d9cb3fd0e1e305014d71356bd6bb
  - path: records/sources/2026-08-02-reviewcompass2-terminology-control.md
    sha256: 0f84865e862f3b7cf0917476157afb5a2185177d158412bb7d6ea4d351a941f6
  - path: docs/current/reviewcompass3-intent-current.md
    sha256: 307bdbcc39d028064ea3ed715ccac38fb68760ac1e8a13b46d4caf3803c11c59
  - path: records/sources/2026-08-02-deployment-topology-discussion.md
    sha256: 95209eadae62ec80ef98cd23182266d657540576f6f542fdbc136f3c5d01c67b
  - path: records/sources/2026-08-02-reviewcompass2-change-scaled-review-input.md
    sha256: 125b53a62de2d34198f8e2721f37612b8b1b8fbe3a4714d0133c4cfa80a358fb
  - path: records/sources/2026-08-02-reviewcompass2-cross-cutting-lessons.md
    sha256: b337bbe723dc416c25eb0d94849029c377077172543af1491a31bc1c18d0c7ac
  - path: docs/design/2026-08-03-current-work-projection-memo.md
    sha256: 940bff56f749bebdff08698882ca92dbe8505cb4692ba864c8ee7b76b4f01595
---

# ReviewCompass3 統合用語集

## 1. この文書の役割

この文書は、ReviewCompass3のIntent、Requirements、計画、Task Contract、設計、実装、記録で
使うdomain固有語の意味を揃える。利用者向けの日本語表示名と、schemaやcodeで使う英語の
canonical tokenを対応付け、同じ語を異なる意味で使うことと、同じ概念へ複数の名前を与える
ことを防ぐ。

この文書はReviewCompass2の用語集をそのまま移したものではない。Task Contract中心のstage、
二つのwork origin、fresh／reopen continuation、component所有state、Decision Authority、
配置非依存のdeploymentに合わせて再定義した後継候補である。Human承認前は正式な正本ではない。

## 2. 用語統制の規則

### 2.1 登録対象

次を用語集への登録対象とする。

- 製品固有の概念、役割、成果物、判断、状態、workflow、検査、記録
- schema、Policy、設定で使うenum、relation、identifierの意味
- 一般語と異なる限定的な意味で使う語
- 日本語と英語tokenの対応がないと誤解しやすい語

一般的な日本語、programming languageの通常語、library固有語をすべて登録するものではない。
自由文に現れる全単語の完全な機械検査は初期範囲に含めない。

### 2.2 登録と変更

- 新しいdomain用語は、規範文書で使う前または同じ変更内で定義する。
- 一つの概念には一つのcanonical termを割り当てる。
- 日本語表示名と英語tokenを併記する。schemaとcodeでは英語tokenを使う。
- aliasは新しい概念として扱わず、canonical termへの一方向の読み替えにする。
- 定義の意味変更はin-place訂正にせず、新version、理由、影響範囲を記録する。
- 廃止語は削除せず`retired`として後継語を示す。
- 緊急の遡及登録は許すが、未登録だった期間と影響文書を記録する。

### 2.3 用語集とschemaの境界

この用語集は人が意味を理解する正本候補である。実行時に許可するstate、relation、decision
classなどの閉じた値は、対応するschemaまたはPolicyを機械正本とする。用語集はその登録先と
意味を示すが、Markdown本文だけからallowlistを生成しない。両者が違う場合は進行を止め、
意味を決めてから同じ変更で同期する。

### 2.4 表記

- 人向け文書では、初出時に「日本語表示名（`canonical_token`）」を示し、その後は読みやすい
  方を使う。
- `ID`、`Digest`、state、relation、path、schema fieldはcode表記にする。
- `Human`は権限を持つ人、`AI`は判断または生成を行う人工知能、`LLM`はAIを実現するmodelの
  一種として区別する。
- `Task`だけ、`Plan`だけ、`Context`だけの省略は、参照先が一意でない場所では使わない。

### 2.5 用語統制自身の用語

- **用語統制（`terminology_control`）**：domain用語の登録、使用、変更、alias、retirement、
  schemaとの同期を管理すること。
- **domain用語（`domain_term`）**：ReviewCompass3固有の意味を持ち、通常語だけでは境界が
  明らかにならない語。
- **canonical term（`canonical_term`）**：一つの概念を規範文書で一貫して指す代表名。
- **canonical token（`canonical_token`）**：schema、code、IDでcanonical termを表す英語token。
- **日本語表示名（`display_name_ja`）**：利用者向け文書と画面でcanonical termを示す日本語名。
- **alias**：過去記録または互換入力で受け入れる別名。新しい規範文書の代表名には使わない。
- **retired term**：現行文書では使用せず、過去記録の解釈用に後継語とともに保持する旧語。
- **遡及登録（`retrospective_registration`）**：既に使われていた未登録語を後から登録し、
  使用期間、理由、影響範囲を履歴へ残すこと。
- **閉じた語彙（`closed_vocabulary`）**：登録された値だけを許し、未登録値を拒否する値集合。
- **読み替え（`term_mapping`）**：旧語またはaliasを現行canonical termへ一方向に対応付けること。

## 3. 文書とauthority

- **Intent（`intent`）**：製品の存在理由、利用者、守る原則、しないこと、成功の状態を定める
  最上位文書。実装方法の詳細は持たない。
- **Feature（`feature`）**：一つのownerへ割り当てられる大域的な製品責務。画面や実装moduleの
  名前ではない。
- **Requirement（`requirement`）**：外部から観測できる義務、制約、停止、復旧、受入条件を
  atomicに表したもの。実装方法を指定するDesign Decisionと区別する。
- **Task Contract（`task_contract`）**：Requirementを実行可能な限定作業へつなぐ版付きの
  仕事の約束。目的、境界、前提、Context、許可能力、期待出力、受入条件、Provenance、
  escalationを固定する。旧「Task記述」の読み替えではなく、controlとprovenanceの単位である。
- **Architecture Policy（`architecture_policy`）**：複数Task Contractへ共通する設計制約と
  安全規則。個別Contractへ同じ規則を複製しないための版付きsourceである。
- **Project Policy Overlay（`project_policy_overlay`）**：base Policyを変更せず、特定projectで
  適用する差分。置換規則、理由、Evidence、決定者、期間を持つ。
- **Design Decision（`design_decision`）**：Task Contractを満たす方法について選択した実装上の
  判断。RequirementまたはTask Contractの意味を変更するauthorityは持たない。
- **改善候補（`improvement_candidate`）**：自己適用中に見つかった問題、改善案または新機能案を、
  現行の受入基準を変更する前に固定する記録。発生元Work、固定source、Evidence、影響、分類候補、
  停止判定、route、consumer、Outcomeを追跡する。Issue、RequirementまたはTask Contractへは
  自動昇格しない。
- **正本（`normative_source`）**：ある情報について現時点でauthorityを持つ唯一の記録先。
  `provisional`または`candidate`の文書は、承認されるまで正本ではない。
- **統合最新版（`consolidated_current`）**：過去文書を削除せず、現在の意味を一つに解決した
  successor候補。最新版であることは承認済みであることを意味しない。
- **Authority（`authority`）**：判断、変更、許可、停止または取消しを有効にする権限。
  文書の優先順位とactorの権限を同じ語で曖昧にしないよう、必要に応じて
  `document_authority`と`decision_authority`を使い分ける。
- **Identity（`identity`）**：成果物、判断、実行を他と区別し、後から同じ対象を参照するための
  安定した識別情報。内容の同一性を示すDigestとは別である。
- **Digest（`digest`）**：特定内容をhash algorithmで照合する値。同じIDでもDigestが変われば
  同じ内容として扱わない。

## 4. 開発stageと作業単位

- **Stage（`stage`）**：開発成果のauthorityと確認目的を分ける工程区分。現在はIntent、Feature
  Partitioning、Requirements、Task Contract Portfolio、Task Contract TDD Delivery、
  Cross-Contract Integration、Release Evaluationの7段である。旧6段SDDの`design`、`tasks`、
  `implementation`は独立した大域stageではない。
- **Task Contract Portfolio（`contract_portfolio`）**：Requirementの受け先、Contract間依存、
  risk、cross-contract acceptanceをまとめて検証する版付き集合。
- **Delivery Work Item（`delivery_work_item`）**：一つのTask Contract versionを実現する実行単位。
  `queued`から`accepted | cancelled | replaced`までのlifecycleを持ち、旧「案件」と区別する。
- **Delivery Work Item state**：`queued | active | red | implementation_ready | green | verified |
  accepted | blocked_by_dependency | blocked_by_cycle | paused | ready | revision_pending |
  cancellation_pending | scope_disposition_pending | cancelled | replaced`を閉じた状態値とする。
  `blocked`または`completed`は説明上の総称であり、state値として保存しない。
- **work origin（`work_origin`）**：仕事が新規要求から始まったか、既存成果の保守から始まったかを
  示す分類。値は`new_development | maintenance`である。
- **continuation mode（`continuation_mode`）**：仕事が新しい開始か、過去の仕事の再開かを示す
  分類。値は`fresh | reopen`である。
- **maintenance**：既存baseline、compatibility、migration、rollbackを追加条件として始まる
  work origin。上位義務が変わればRequirementsへ戻る。
- **reopen**：確定済み成果をin-placeで開き直さず、prior identityと理由を持つ新versionまたは
  新Work Itemとして再開するcontinuation mode。
- **Issue Record（`issue_record`）**：実行中に見つかった、現在のContract境界で安全に解決できない
  問題の発生記録。問題の存在を示すもので、解決手順や解決済みの証明ではない。
- **Issue Resolution Plan（`issue_resolution_plan`）**：一つ以上のIssueを解決するための独立した
  計画。Task ContractからcompileされるPlan bundleとは別のidentityを持つ。
- **Plan Challenge（`plan_challenge`）**：Issue Resolution Planを実行前に独立して審査し、
  blocking verdictを開始permitへ結ぶreview。
- **Upstream Revision（`upstream_revision`）**：実装中に上位のRequirement、Feature、Intentなどの
  意味変更が必要と分かったとき、現在の仕事へ押し込まず新versionへ戻す経路。
- **Termination（`termination`）**：Work Itemを通常accept以外で制御終了すること。`pause`は再開
  予定、`cancel`は現在のWork Item終了、`close-scope`はRequirementまたはrelease scopeを
  新versionで変更する判断であり、いずれも要求達成を意味しない。
- **WIP（`work_in_progress`）**：正式なaccept前の途中成果。WIP commitを完了判断や正本昇格と
  混同しない。
- **Deferred Acceptance Catalog（`deferred_acceptance_catalog`）**：初期scope外の能力について、
  将来必要なnegative Acceptance Testと失敗条件を実装permitから切り離して保存する台帳。対応する
  Task ContractがPortfolioへ入った時にredとして有効化し、存在だけで初期sliceをblockしない。

## 5. Task ContractとPlan

- **Plan bundle（`plan_bundle`）**：固定Task Contract、Policy、Capability Resolutionから
  決定的にcompileされた6 Planと、その被覆・整合結果のまとまり。Issue Resolution Planと
  同じ`Plan`ではない。
- **Context Acquisition Plan**：対象材料を特定、取得、検証、固定するPlan。
- **Review / Execution Plan**：誰が何をどの順序で実行するかを定めるPlan。
- **Harness and Capability Plan**：model、Tool、permission、実行条件を解決するPlan。
- **Verification Plan**：どのtest、review、oracleで結果を確かめるかを定めるPlan。
- **Provenance Capture Plan**：必須event、relation、保存時点を定めるPlan。
- **Human Interaction Plan**：Humanの判断またはescalationが必要な地点と材料を定めるPlan。
  AIへ判断委譲する場合も、範囲外時にHumanへ戻す経路を持つ。
- **Evidence Extraction Contract**：既存Evidenceを探索するときのsource universe、開始entry、
  展開規則、分類、終了条件、除外、完全性oracleを固定する横断契約。第7 Planではない。
- **Evidence Consumption Closure**：必須sourceと採用FindingがRequirement、Contract obligation、
  VerificationまたはDecisionの消費先へ接続され、扱い先なしが残っていない状態。
- **Assurance Obligation Matrix**：重要な規則について、宣言、runtime enforcement、failure verdict、
  permit効果、復旧、保存Evidenceの被覆を対応付けた表現。
- **Allowed Capability（`allowed_capability`）**：Contract内で使用を許されたmodel、Tool、操作、
  permission。実行環境で利用可能であるだけでは許可を意味しない。
- **Obligation（`obligation`）**：RequirementまたはTask Contractが必ず満たす一つの義務。
  配列位置ではなく安定した`obligation_id`で参照する。
- **Permit（`permit`）**：固定入力と必要条件の照合後、特定の状態遷移または操作だけを許可する
  版付き記録。一般的な権限や永続的承認ではない。

## 6. Context、実行、review

- **Review Context Feature（`FEAT-REVIEW-CONTEXT`）**：Review Taskの材料、Scope、Context identity、
  freshnessに関する製品責務。runtime component名ではない。
- **Context Runtime（`context_runtime`）**：Context Acquisition Planを受け、候補取得、分類、構成、
  Manifest、freshnessを所有するruntime component。旧文書でcomponentを指す`Review Context`は
  本語へ読み替える。
- **Session Records Feature（`FEAT-SESSION-RECORDS`）**：Sessionの取込み、raw保全、派生、mutation、
  lifecycleに関する製品責務。
- **Session Evidence Source（`session_evidence_source`）**：Session Records FeatureをContext候補へ
  接続する版付きsource adapter。独立stageまたはContext ownerではない。
- **Session Log Bootstrap（`session_log_bootstrap`）**：Layout Baseline固定後、Work 2以降の開発
  sessionを失わないために準備する最小capture profile。raw／派生物分離、機密性、access、retention、
  capture deadline、mutation、availability、restore検証を持つが、完成した製品機能ではない。
- **Review Task（`review_task`）**：固定した対象と判断基準を審査する意味的な実行単位。
  実装を行うImplementation Task Contractと区別する。
- **source universe**：材料を探索・検査してよい根拠付き母集合。project全体や会話履歴を暗黙に
  含めない。
- **Scope（`scope`）**：source universeから今回対象にする範囲と除外理由。permissionや責務境界と
  混同しない。
- **影響スライス（`impact_slice`）**：変更単位から版付き意味graphと閉包規則で到達した影響候補、
  必要なEvidence抜粋、Task Contract必須材料から決定的に構成する既定のreview入力。
- **Scope拡大（`expanded_scope`）**：局所的な影響スライスでは安全に判断できない理由を固定し、
  Decision Authorityの下で対象材料を追加するreview入力mode。暗黙の全文追加ではない。
- **全文整合review（`full_consistency`）**：global invariantまたは残余riskを確認するため、通常の
  変更reviewとは別の固定条件、Context identity、Provenanceで行う広域review。
- **Execution Context（`execution_context`）**：一つの実行に使うことが確定した入力、基準、
  identity、Digestの集合。材料候補のsource universeとは別である。
- **Harnessed Execution（`harnessed_execution`）**：actor、Prompt、Tool、Validation、Retry、
  Loggingを固定Planに従って制御する実行。
- **Run（`run`）**：固定Contract、Context、Plan bundleに対する一回のまとまった実行記録。
- **Attempt（`attempt`）**：一つのRun内の個別試行。成功、失敗、timeoutを問わず記録する。
- **Retry（`retry`）**：失敗したAttemptを上書きせず、同じ固定条件に新しいAttemptを追加すること。
  条件が変わる場合はRetryではなく新Runまたは新versionである。
- **Finding（`finding`）**：Evidence参照を持つreview上の主張。採用されたFindingだけをIssueと
  呼ぶのではなく、FindingとIssue Recordは別の成果物である。
- **独立review（`independent_review`）**：review対象の起草過程や他担当の結論を暗黙に共有せず、
  固定材料だけで行うreview。
- **実行独立性（`execution_independence`）**：担当同士が互いの結果と会話文脈を共有せず別実行で
  ある性質。
- **model独立性（`model_independence`）**：担当へ割り当てたmodel系列またはmodelが異なる性質。
  実行独立性とは別に記録する。
- **Conformance（`conformance`）**：成果が固定Requirement、Contract、schema、Policyへ適合するかを
  確認すること。対象そのものの妥当性を問い直すChallengeとは別である。
- **Challenge（`challenge`）**：定義、Planまたは成果の前提、境界、目的適合性を問い直すreview。
  `Definition Challenge`、`Final Contract Challenge`、`Plan Challenge`は対象が異なる。
- **Review Quality Contract**：reviewのverdict、severity、Finding schema、材料十分性、独立性、
  収束条件を固定する横断契約。
- **insufficient evidence（`insufficient_evidence`）**：判断に必要な材料が足りず、問題なしとも
  適合とも確定できないreview verdictまたはFinding分類。
- **out of level（`out_of_level`）**：指摘内容は有用でも、現在のreview責務または層の判定対象外で
  あり、適切なownerへrouteすべき分類。

## 7. test、確認、判断

- **TDD（`test_driven_development`）**：期待する振る舞いをtestで先に表し、redを確認してから
  implementationを進め、同じ期待をgreenにする開発cycle。
- **red Evidence（`red_evidence`）**：実装前のtestが意図した理由で失敗した事実。testが壊れて
  失敗しただけの結果は含めない。
- **green Evidence（`green_evidence`）**：対象testが実装後に通過した事実。Contract全体のaccept、
  integration、release完了を単独では意味しない。
- **Verification（`verification`）**：固定された期待、test、review、oracleに照らしてEvidenceを
  確認すること。
- **Validator Assurance Profile**：validatorと入力前提のversion、既知正例、負例、境界例、
  mutation、独立oracle、代表実データの要否を固定し、validator自体の妥当性を確かめる定義。
- **post-write verification**：書込み後の実成果を再読込し、関連validator、参照整合、stale閉包を
  確認する検証。生成または書込み処理の成功だけでは代用しない。
- **Acceptance（`acceptance`）**：成果が対象ContractまたはRequirementの義務を満たしたと有効な
  authorityが判断すること。testのgreenやcommitだけでは成立しない。
- **Approval（`approval`）**：文書、Plan、権限、外部送信などを、その対象Digestと範囲に限って
  許可する判断。成果のAcceptanceとは区別する。
- **Completion（`completion`）**：定義された義務、検証、判断、Provenanceが揃い、対象lifecycleを
  終端へ移せる状態。作業を中止または先送りしたことをCompletionと呼ばない。
- **Evaluation（`evaluation`）**：手続きやAIの能力が有効だったかを、baseline、trial、観測、
  Outcome Label、metricで比較すること。個別成果のVerificationとは別である。
- **Outcome Label（`outcome_label`）**：後から確認された正誤、実欠陥、誤acceptなど、評価対象の
  帰結を示すlabel。実行時の自己評価をそのまま正解labelにしない。
- **fail-closed**：必要な材料、定義、authority、検査結果がないとき、推測で通さず停止または
  不合格側にする原則。
- **stale**：参照した入力、Policy、authorizationなどが変わり、以前の結果を現行判断へ再利用
  できない状態。成果を削除することではない。
- **復旧入口（`recovery_path`）**：停止理由、未充足条件、必要操作を示し、条件を満たした後に
  正規に再開する経路。

## 8. 判断主体とAIへの委譲

- **Human**：目的とPolicyを定め、委譲を設定、変更、停止、取消しできる人。すべての個別判断を
  常に自分で行うactorという意味ではない。
- **AI**：生成、意味判断、reviewまたは委譲された限定判断を行う人工知能system。特定のmodel、
  provider、agent製品だけを指さない。
- **LLM**：文章を入力・生成できるlarge language model。AI actorを構成し得るが、Tool、Workflow、
  Policyを含むAI system全体と同義ではない。
- **機械処理（`machine_process`）**：列挙、照合、state遷移、保存など、定義済み規則に従う処理。
  LLMを使わないという意味ではなく、意味裁量を持たない責務を指す。
- **Decision Authority（`decision_authority`）**：特定decision classを有効に決められる権限。
- **Decision Record（`decision_record`）**：判断対象、Digest、decision class、actor、authority、
  Evidence、理由、結果を分離して保存する記録。
- **Delegation Authorization（`delegation_authorization`）**：HumanがAIへ限定的なDecision Authorityを
  与える版付き記録。decision class、scope、modelまたはcapability、permission、期間、能力Evidence、
  停止、escalation、取消しを固定する。
- **能力Evidence（`capability_evidence`）**：対象業務とriskを固定したtrialとOutcomeから、AIが
  委譲対象の判断を行えるか評価する根拠。AI一般への評判やmodel名だけでは成立しない。
- **human-only（`human_only`）**：AI提案は利用できるが、対象判断をHumanだけが確定するmode。
- **shadow evaluation（`shadow_evaluation`）**：AIとHumanが独立に判断するが、AI判断を業務stateへ
  反映せず、能力Evidenceだけを得るmode。
- **supervised delegation（`supervised_delegation`）**：AI判断を候補として扱い、Humanの事前確認後に
  業務stateへ反映する期限・件数限定mode。
- **bounded delegation（`bounded_delegation`）**：有効なDelegation Authorizationの範囲内で、Humanの
  事前確認なしにAI判断を反映できるmode。Humanが停止・取消しでき、範囲外はHumanへ戻す。
- **Escalation（`escalation`）**：AIまたは機械が判断不能、範囲外、競合、異常を検出し、必要な材料と
  ともに上位authorityへ判断を戻すこと。失敗を隠すfallbackではない。

## 9. Provenanceと記録

- **Evidence**：主張、判断、検証を裏付ける固定可能な資料または実行結果。
- **実施報告照合（`execution_claim_verification`）**：会話、TODO、checklistまたは最終報告の実施・
  結果・判断Claimを、対象identity、固定source、Evidence、観測した事後状態と照合すること。
  EvidenceがないClaimは`reported_unverified`、報告と事後状態が競合する場合は
  `report_execution_mismatch`とし、報告文だけを完了根拠にしない。
- **Provenance**：成果、判断、実行が何から、誰により、どの権限と処理を経て生じたかを示す
  来歴関係の総称。
- **Operational Provenance**：Requirement、Contract、Context、Run、Attempt、Result、Decision、
  Test、Implementationを実行上のeventとrelationで結ぶ追記型記録。
- **追記型（`append_only`）**：過去eventを消して現在値へ置き換えず、新しいeventとrelationを
  追加して変更を表す方式。
- **Relation（`relation`）**：二つのidentity間の意味関係。許可値はschemaの閉じた語彙を正とし、
  自由文で新しいrelation typeを作らない。
- **影響閉包（`impact_closure`）**：変更または失効した対象からrelationをたどり、再確認が必要な
  下流成果を漏れなく求めた集合。
- **Provenance incomplete**：必須eventまたはrelationが欠け、成果をverifiedまたはacceptedに
  できない状態。成果自体は削除しない。
- **As-Built projection（`as_built_projection`）**：accepted Task ContractのProvenance、Test、
  Design Decision、Implementation、symbolから実装済み機能の説明を再生成する後続能力。
  Requirementsを自動変更する機能ではない。
- **現在位置プロジェクション（`current_work_projection`）**：固定Plan、Task Contract Portfolio、
  Work Item、Dependency、Decision、Provenance、Source Snapshot、Test Evidenceから、全体計画上の位置、
  active作業、次の実行可能作業、blocker、Human判断待ち、staleを決定的に導出する派生view。
  手編集する状態正本ではなく、初期textと後続UIが同じstructured projectionを利用する。

## 10. 実装の再利用

- **Source Symbol Index（`source_symbol_index`）**：実codeから機械生成するsymbol、signature、path、
  relationの索引。再利用の意味判断は持たない。
- **Reusable Routine Ledger（`reusable_routine_ledger`）**：routineの責務、alias、再利用判断、統廃合、
  retirementを保持する版付き台帳。Indexと実codeを照合して使う。
- **Implementation Discovery（`implementation_discovery`）**：green実装前にIndex、Ledger、実codeを
  調べ、候補と判断根拠を記録する作業。
- **reuse**：既存routineを責務変更なしにそのまま使う判断。
- **extend**：既存routineの責務を整合する形で広げて使う判断。
- **merge**：複数の重複または類似routineを一つのownerへ統合する判断。
- **split with rationale（`split_with_rationale`）**：類似実装と分けて作る理由、境界、将来の統合条件を
  明記して別実装にする判断。
- **retired routine**：廃止済みで、新しい登録判断なしに再利用または同責務で復活させてはならない
  routine。

## 11. Deploymentと保存

- **deployment profile（`deployment_profile`）**：componentの配置、通信境界、state owner、
  permission、failure modelを一組として固定した配置形態。単なるinstall先の名前ではない。
- **local integrated profile（`local_integrated`）**：単一machine、単一利用者を対象とする初期profile。
  配布と起動は一括でもよいが、Control Plane、Execution Plane、project、runtime dataの論理境界を
  維持する。
- **shared runtime profile（`shared_runtime`）**：共有serverにControl Planeを置き、project固有の
  local操作をLocal Execution Agentへ委ねる後続profile。
- **distributed hybrid profile（`distributed_hybrid`）**：複数のExecution Agent、worker、GPUまたは
  HPC等へ実行を配置する後続profile。実測されたscaleまたはdata locality要件なしに導入しない。
- **Control Plane（`control_plane`）**：Task Contract、Plan、Workflow state、Policy、permit、
  Decision、Provenanceを所有し、何をどの条件で実行するかを制御する論理責務。
- **Execution Plane（`execution_plane`）**：固定Planとpermitを受け、LLM、Tool、command、testなどの
  実作業を行う論理責務。Contractやaccepted stateのauthorityを持たない。
- **Execution Worker（`execution_worker`）**：Execution Planeの処理を行う実行体。crash後に再開
  できるよう、authorityを持つ唯一の状態をprocess内だけに保持しない。
- **Local Execution Agent（`local_execution_agent`）**：shared runtimeから直接読めないlocal file、
  Git、commandを、Project Bindingと最小permissionの範囲で実行するagent。
- **stable deployment（`stable_deployment`）**：確認済みcode、schema、configで現在の開発やreviewを
  支える環境。development candidateからstateとrootを分離する。
- **development deployment（`development_deployment`）**：次versionを実装・検証する環境。自分自身の
  合否を唯一決定する環境にはしない。
- **distribution unit（`distribution_unit`）**：独立したidentity、version、依存、install、update、
  rollbackを持つ配布単位。Runtime Core、integration client、Capability Adapter、project artifactを
  同じ単位として扱わない。
- **Capability Adapter（`capability_adapter`）**：CLI、API、MCP、LLM、container等の実行方式を
  Harnessed Executionへ接続する検証済みadapter。project側Task Contractだけで任意codeをload
  できる仕組みではない。
- **論理root（`logical_root`）**：code、project、data、state、log、cache、sensitive data、evaluationを
  役割別に示す論理配置。特定端末の絶対pathではない。
- **Layout Baseline（`layout_baseline`）**：初回実装前に、logical root、Git管理境界、相対参照基準、
  Manifest、Binding、stable／development分離、所有・retention・path解決順を固定する版付き記録。
  managed pathの変更は本文の上書きではなく、後継baselineとmigrationで行う。
- **Project Manifest（`project_manifest`）**：projectの安定IDとversion管理する設定を示す記録。
- **Project Binding（`project_binding`）**：project IDと特定checkoutまたは配置を結ぶ記録。projectの
  移動や複数checkoutをProject Manifestの書換えで表さない。
- **Integration Manifest（`integration_manifest`）**：Codex、IDE、CLIなどとの接続、source root、
  command、read／write root、capability、permission、ownerを示す記録。
- **Deployment Manifest（`deployment_manifest`）**：配布code、supported platform、logical root、
  Binding、owned resource、migration、permission、confidentiality、retentionを示す記録。
- **owned resource**：ReviewCompass3が作成・更新・解除できるとManifestで明示されたresource。
  uninstall時に未登録のproject成果を削除しない。
- **機微情報（`sensitive_information`）**：secret、credential、個人情報、生会話など、通常dataと
  分離した権限、送信、retentionが必要な情報。
- **retention**：記録種別ごとの保存期間、保持理由、削除条件。uninstallとdata削除を同じ操作に
  しない。

## 12. 旧語の読み替えと非推奨語

| 旧語または曖昧語 | 現行の扱い |
|---|---|
| SDDの6段 | 7つの`stage`へ置換 |
| SDD本筋／reopen／maintenanceの3 lane | `work_origin`と`continuation_mode`へ分解 |
| Task記述 | `task_contract`へ置換 |
| 案件 | 文脈により`delivery_work_item`または`issue_record`へ分解 |
| 単一状態台帳／関門完了台帳 | component所有stateと`operational_provenance`へ置換 |
| 承認停止点 | `decision_authority`、`decision_record`、`permit`へ分解 |
| 代理判定 | `shadow_evaluation`から`bounded_delegation`までの段階導入へ置換 |
| 共通ルーチン台帳 | `source_symbol_index`と`reusable_routine_ledger`へ責務分離 |
| deploy-manifest | `deployment_manifest`と各Bindingへ置換 |
| Middleware／Review App | `control_plane`、`execution_plane`、integration clientの責務として再分解 |
| Task Package | project側Task Contract／Policyと、installed code側`capability_adapter`へ分離 |
| Task Registry | `contract_portfolio`、Project Manifest、検証済みadapter登録へ責務分離 |
| production／staging | 現在の自己開発では`stable_deployment`／`development_deployment`を使う |
| Task | 単独使用を避け、`review_task`、`task_contract`、`delivery_work_item`を明示 |
| Plan | 単独使用を避け、`plan_bundle`または`issue_resolution_plan`を明示 |
| 完了 | `green`、`verified`、`accepted`、`completion`のどれかを明示 |
| 独立 | `execution_independence`または`model_independence`を明示 |
| AI／LLM | system actorを指すときはAI、modelを指すときはLLMを使う |

## 13. 用語追加時の確認

新しい規範用語を追加するときは、少なくとも次を確認する。

1. 既存語で同じ概念を表せないか。
2. 日本語表示名とcanonical tokenが一対一か。
3. 一般語より狭い意味なら、その境界が説明されているか。
4. 類似語との違いと、旧語からの読み替えが示されているか。
5. schemaまたはPolicyの閉じた値なら、機械正本と同期しているか。
6. 意味変更なら、影響閉包とstale対象が記録されているか。
7. Intentの平易さを損なう内部語をIntent本文へ持ち込んでいないか。

## 14. 初版の適合判断

ReviewCompass2から、登録制、canonical term、alias／retirement、意味変更履歴、平易な操作語、
実行独立性とmodel独立性の区別、再利用4分類を修正採用した。旧6段SDD、3 lane、単一状態台帳、
旧gate、代理判定、旧deployment区分は現在の設計へ置換した。旧レビュー方式と意味単位管理の
詳細語は、現行Requirementsで必要になるまで登録を保留する。
