---
lifecycle: provisional
normative_status: review-candidate
promotion_required: true
---

# Task Contract中心化 requirements差分

## 1. 位置付け

本文書は、承認済み37 requirementsを固定証拠として保持したまま、Task Contractを
共通制御面として追加する差分候補である。既存Requirement IDの意味を履歴上で
書き換えず、新Featureと新Requirementを追加し、既存Requirementとのinterface変更を
定義する。

対象Featureを`FEAT-TASK-CONTRACT-CONTROL`とする。

## REQ-CONTRACT-001 版付きTask Contract

システムは、構造化Requirementsから切り出した局所責務を、Identity、Responsibility、
Boundary、Preconditions、Context Obligations、Allowed Capabilities、Expected Outputs、
Acceptance Criteria、Provenance Obligations、Escalation Policyを持つ版付きTask
Contractとして固定しなければならない。

- 入力
  - source Requirement IDと内容identity
  - 適用するArchitecture PolicyのID、version、digest、適用範囲
  - Task Contract type、goal、obligation
  - in-scope、out-of-scope、prohibited effect
  - required state、assumption、dependency
  - Context、能力、成果、検証、来歴、escalationの各定義
- 出力
  - 一意ID、version、内容Digestを持つTask Contract
  - RequirementとContract obligationの順逆対応
- 停止条件
  - 必須領域が欠落、空、未解決、競合している
  - source Requirementを解決できない
  - 必須RequirementにContract obligationの受け先がない
  - prohibited effectとallowed side effectが競合する
  - 適用すべきArchitecture Policyが未解決または競合している
- 復旧条件
  - RequirementまたはContractを訂正し、新しいversionとして再検証する
- 失敗時に保存するもの
  - 拒否候補、source identity、項目別診断、競合
- 受け入れ条件
  - 各必須領域を一つずつ欠落させたContractが確定前に拒否される
  - 同じ正規化入力から同じContract digestが得られる
  - 全Contract obligationをsource Requirementへ逆引きできる
- 対象外
  - ContractだけでRequirementの真実性を保証すること
  - LLMが欠落項目を暗黙補完して確定すること

## REQ-CONTRACT-002 決定的なPlan compilation

システムは、固定したTask Contract、Compiler、Policyから、Context Acquisition、
Review / Execution、Harness and Capability、Verification、Provenance Capture、
Human InteractionのPlan bundleを決定的に生成しなければならない。

- 入力
  - Task Contract ID、version、digest
  - Compiler ID、version、digest
  - Architecture PolicyのID、version、digest、適用範囲、優先順位
  - Schema、supported capability catalog
- 出力
  - 6種類の版付きPlan
  - Plan bundle identity
  - Contract obligationとPlan項目の順逆被覆
- 停止条件
  - Compilerが扱えないobligationがある
  - Plan間で権限、順序、停止条件、保存条件が競合する
  - 未定義Tool、権限、oracle、event、保存区画を要求する
  - 適用Policyの不足、競合または優先順位を決定できない
- 復旧条件
  - Contract、Compiler、Policyまたはcapability catalogを新versionとして訂正する
- 失敗時に保存するもの
  - 入力identity、生成可能だった診断、未対応obligation、競合
- 受け入れ条件
  - 同じ固定入力から同じPlan bundle identityが得られる
  - 各Plan項目が一つ以上のContract obligation IDを持つ
  - 必要Planへ受け渡されないobligationが一件でもあれば`not_compilable`になる
  - Policy順序を変えず同じ固定入力をcompileすると同じPolicy解決結果になる
- 対象外
  - Runtime stateをCompilerが変更すること
  - LLMの推論だけで実行Planを確定すること

## REQ-CONTRACT-003 Portfolio被覆とstale伝播

システムは、RequirementsとTask Contract Portfolioの順逆被覆を検査し、Contract、
Requirement、CompilerまたはPolicy変更時に依存Plan、Context、Runをstaleとして
再利用拒否しなければならない。

- 入力
  - Requirement母集合
  - Task Contract Portfolio
  - Requirement、Contract、Plan、Context、Runの依存辺
  - prior identityとcurrent identity
- 出力
  - Portfolio被覆verdict
  - stale対象の閉包と再compile要求
- 停止条件
  - 必須Requirementの受け先がない
  - Contract間責務が競合または禁止循環を持つ
  - staleなPlan、Context、Runを再利用しようとする
- 復旧条件
  - Portfolioまたは依存辺を訂正する
  - 新しいContract versionをcompileし、新しいRunを開始する
- 失敗時に保存するもの
  - 未被覆、競合、変更元、影響閉包、拒否再利用対象
- 受け入れ条件
  - Requirement、Contract、Compiler、Policyを一つずつ変更すると依存先だけが
    staleになる
  - 無関係なContract成果はstaleにならない
  - 旧成果を残したまま新versionへ関係をたどれる
  - Policy変更時は適用範囲に含まれる依存先だけがstaleになる
- 対象外
  - stale履歴を削除または上書きすること
  - 物理ファイルの更新時刻だけで意味的依存を判断すること

## REQ-CONTRACT-004 二層Contract review

システムは、成果のTask Contract適合性を検証するContract Conformance Reviewと、
Contract確定前のDefinition Challenge、成果検証後のFinal Contract Challengeを、目的、
材料、Finding、完了条件を混同せず実行できなければならない。

- 入力
  - Task Contractとsource Requirements
  - compiled Verification Plan
  - Architecture Policy、Challenge Policy、risk catalog、隣接Contract
  - 成果物、Test、Evidence
- 出力
  - Conformance Finding集合
  - Definition Challenge Finding集合とverdict
  - Final Contract Challenge Finding集合とverdict
  - Contract改定またはRequirement再検討要求
- 停止条件
  - 三つのreview目的、実行時点または材料範囲を区別できない
  - blocking Challenge Findingがあるまま成果をacceptedにしようとする
  - blocking分類を固定したChallenge PolicyまたはHuman裁定へ逆引きできない
  - Contract外問題を根拠なしに無制限探索する
- 復旧条件
  - ContractまたはRequirementを新versionとして訂正し再reviewする
  - review scopeとchallenge基準を訂正する
- 失敗時に保存するもの
  - 全Finding、review phase、分類、Evidence、Policy判定、未解決、Human裁定
- 受け入れ条件
  - Requirementを欠くContract fixtureをDefinition Challengeが実行前に検出する
  - Contractを満たすが上位Intentまたは隣接Contractを損なう成果fixtureをFinal Contract
    Challengeが検出する
  - Contract違反fixtureをConformanceへ分類する
  - blocking Challenge FindingがContractの`accepted`遷移を拒否する
- 対象外
  - Contract適合だけをシステム妥当性とみなすこと
  - Challengeを一般的な無制限レビューにすること

## REQ-CONTRACT-005 Provenance Capture Plan

システムは、Task ContractのProvenance Obligationsから実行前にCapture Planを生成し、
Contract、Plan、Context、Execution、Result、Evidence、Human判断を必須eventと型付き
関係で記録しなければならない。

- 入力
  - ContractとProvenance Obligations
  - Plan bundle
  - event schema、retention、confidentiality policy
- 出力
  - 版付きCapture Plan
  - 追記型Operational Provenance event
  - 閉じた関係語彙に従う複数の型付きevent関係
  - 必須event完全性verdict
- 停止条件
  - 必須eventまたは関係を記録できない
  - 保存区画、機密性、retentionを解決できない
  - eventがContractまたはRun identityへ結線できない
- 復旧条件
  - 設定を訂正し、未開始なら新しいPlanをcompileする
  - 確認済みeventから値なし診断付きの新Runを開始する
- 失敗時に保存するもの
  - 保存可能な直前event、欠落種別、値なし診断
- 受け入れ条件
  - 必須eventを一種類ずつ欠落させると`verified`遷移が拒否される
  - eventからRequirementとContract obligationへ逆引きできる
  - 機微情報分類違反時に通常保存されない
  - 複数入力から生成した成果を各入力へ関係型とDigest付きで逆引きできる
  - event追記順序と意味的な依存関係を独立して再構成できる
- 対象外
  - 評価目的を理由に全raw dataを無期限保存すること
  - Provenance Storeが業務状態を所有すること

## REQ-CONTRACT-006 Evaluation Profileと再計算

システムは、評価仮説、必要観測、baseline、比較条件、指標、欠測、privacy、retentionを
版付きEvaluation Profileとして固定し、一次eventから評価指標を再計算できなければ
ならない。

- 入力
  - Evaluation Profile
  - Operational Provenance event
  - Evaluation Observation
  - Outcome Label
  - metric定義とversion
  - evaluation case、condition、pair、trial、実行順序
  - model、Tool、budget、設定のidentity
  - label作成者、評価者、confidence、裁定履歴
- 出力
  - 再現可能なmetric projection
  - `evaluable`、`partially_evaluable`、`not_evaluable`の評価状態
  - 解釈と限界を分離したEvaluation Ledger entry
- 停止条件
  - profile、metric、比較条件のidentityが欠ける
  - 指標計算が一次eventへ逆引きできない
  - 異なる条件を同一baselineとして比較する
- 復旧条件
  - profileまたはmetricの新versionで再計算する
  - 欠測を明示して比較対象から分離する
- 失敗時に保存するもの
  - 入力identity、欠測、計算診断、部分結果
- 受け入れ条件
  - 同じ固定eventとmetricから同じ評価値が得られる
  - metric version変更時に旧評価を保持した新projectionになる
  - 任意評価観測の欠測だけでは業務成果を無効にしない
  - 比較値をcase、condition、trial、実行条件、評価者へ逆引きできる
  - 無作為化、盲検化、反復数をProfileで未指定の初期Pilotも、未指定を明示して保存する
- 対象外
  - 指標だけで意味的な改善方針を自動決定すること
  - baselineなしにTask Contract方式の優位性を確定すること

## REQ-CONTRACT-007 Cross-Contract Integration

システムは、accepted Task Contract間のinterface、共有状態、E2E、failure propagation、
配置およびlifecycle操作をIntegration Planとして固定し、全体Intentに対するIntegration
Verdictを生成しなければならない。

- 入力
  - accepted Task Contract集合とPlan bundle identity
  - cross-contract interfaceと共有状態owner
  - Integration Manifest、Project Binding、Deployment Manifest
  - Contract単位のVerification、Conformance、Final Challenge Evidence
- 出力
  - 版付きIntegration Plan
  - cross-contract E2Eとfailure propagation Evidence
  - `integration_passed`または`integration_failed`のIntegration Verdict
  - Release Evaluationへ渡すEvidence bundle identity
- 停止条件
  - schema、権限、順序、共有状態ownerまたはfailure propagationが競合する
  - staleまたは未acceptedのContract、Plan、Bindingを入力に含む
  - 局所Contractが成功しても全体Intentまたはcross-contract acceptanceを満たさない
  - install、update、migrationまたはuninstallの必要条件を解決できない
- 復旧条件
  - Portfolio、Contract、interface、PolicyまたはBindingを新versionとして訂正する
  - 影響するContractだけを再検証し、新しいIntegration Planを実行する
- 失敗時に保存するもの
  - 入力identity、競合interface、共有状態owner、実行済みEvidence、失敗伝播、verdict理由
- 受け入れ条件
  - interface schema不整合を実行開始前に拒否する
  - 一Contractの失敗がPlanどおり隣接Contractと全体verdictへ伝播する
  - 局所テストがすべて成功してもIntentを満たさないfixtureを`integration_failed`にする
  - Release EvaluationからIntegration Verdictと全Evidenceへ逆引きできる
- 対象外
  - Task Contract ControlがWorkflowまたはconsumerの実行状態を直接変更すること
  - Contract単位の成功だけでrelease可能とみなすこと

## 2. 既存requirementsへの差分

### FEAT-REVIEW-CONTEXT

- `REQ-CONTEXT-001`の7項目Review Task定義は、履歴上は保持し、正式Runtimeでは
  `REQ-CONTRACT-001`のReview Task Contractへ置換する。
- `REQ-CONTEXT-002`〜`007`はContext Acquisition Plan、Contract digest、
  obligation IDを入力へ追加する。
- Context Manifestは採用材料だけでなく、Context obligation、除外候補、変換、
  未充足、矛盾、token・時間・費用を保持する。

### FEAT-HARNESSED-EXECUTION

- `REQ-EXEC-001`の実行仕様をcompiled Review / Execution PlanとHarness and
  Capability Planへ置換する。
- `REQ-EXEC-002`はContractが許可した能力、root、side effect、budgetを送信identityへ
  追加する。
- `REQ-EXEC-006`はContract、Plan bundle、Evaluation Profileのidentityを観測値へ
  結ぶ。

### FEAT-SEMANTIC-TRACE

- `REQ-TRACE-002`の上流義務へRequirement、Contract obligation、Plan項目を追加する。
- `REQ-TRACE-005`のOperational Provenance起点をReview Task入力から、Requirement、
  Task Contract、Compilationへ拡張する。

### FEAT-WORKFLOW-CONTROL

- `REQ-WORKFLOW-002`のRun permitをContract digest、Plan bundle digest、freshness、
  required approvalへ束縛する。
- Contract lifecycleはTask Contract Controlが所有し、作業段階とRun permitは
  Workflowが所有する。
- `REQ-WORKFLOW-004`の自己適用はstableなContract能力だけを必須経路へ使用する。

### FEAT-PORTABLE-LIFECYCLE

- `REQ-PORTABLE-001`へDeployment Manifest、Project Binding、Integration Manifest、
  contract、run、evaluation、sensitiveの論理rootを追加する。
- `project_id`はProject Manifestに保存した安定IDとし、project内容digest、repository
  root、checkoutごとのBinding identityから分離する。
- `REQ-PORTABLE-002`をContract、Plan、event、ledgerの共通原子的I/Oへ適用する。
- `REQ-PORTABLE-003`へversion migration、adapter、project bindingの所有対象を追加する。
- `REQ-PORTABLE-004`へTask ContractのconfidentialityとCapture Planのretentionを
  接続する。

### FEAT-EVIDENCE-EVALUATION

- `REQ-EVAL-001`〜`003`は`REQ-CONTRACT-006`のEvaluation Profileとmetric projectionを
  消費し、結果の意味的評価、比較、限界を所有する。

### FEAT-SELF-IMPROVEMENT

- 改善候補はEvaluation Ledgerの固定比較を根拠とし、Contract、Compiler、Policy、
  Capture Planのどれを変更する仮説かを明示する。

## 3. 新しい境界

最低限、次のinterfaceを設計へ追加する。

- Requirements / Trace → Task Contract Portfolio
- Task Contract Control → Context Runtime
- Task Contract Control → Workflow
- Task Contract Control → Harness
- Task Contract Control → Semantic Trace
- Task Contract Control → Portable Lifecycle
- Task Contract Control → Evidence Evaluation
- Evidence Evaluation → Self Improvement

各interfaceはContract ID、version、digest、Plan ID、obligation ID、failure verdictを
持つ。Task Contract Controlは各consumerの状態遷移を直接行わない。

## 4. 要件差分の完了条件

- 新7 requirementsの各入力、出力、停止、復旧、保存、受け入れ、対象外が確定する。
- 既存37 requirementsへの影響を`preserve / adapt / replace / defer`で全件分類する。
- 新旧Requirementの順逆被覆に未解決がない。
- 新しいinterfaceと所有責務が競合しない。
- 受け入れ試験ID、oracle種別、negative caseが各新Requirementへ一件以上ある。
- 第5段の旧承認候補を上書きせず、新しい差分監査へ結べる。
