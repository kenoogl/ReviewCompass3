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

対象Featureを`FEAT-TASK-CONTRACT-CONTROL`と`FEAT-WORKFLOW-CONTROL`とする。
ReviewCompass2の承認済みintent P-5、共通ルーチン台帳、`R-F6-010`、`R-F6-011`を
前身要件として継承し、Task Contract TDD DeliveryとProvenanceへ接続する。

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
  - ID、目的、入力、出力、完了条件の最小task核と、追加したBoundary、Capabilities、
    Provenance、Escalation、Dependencyの対応
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
  - 任意のProject Policy Overlay、base Policy参照、調整理由、Evidence、supersedes
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
  - 同じbase PolicyとProject Policy Overlayから同じ実効PolicyとAgent entryを再生成できる
  - Overlay変更時は依存するContractだけがstale候補になる
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
  - change semantics、state effect、side effect、riskから選択したVerification Profile
  - 成果物、Test、Evidence
- 出力
  - Conformance Finding集合
  - Definition Challenge Finding集合とverdict
  - Final Contract Challenge Finding集合とverdict
  - Contract改定またはRequirement再検討要求
  - Verification Profile選択理由と充足verdict
- 停止条件
  - 三つのreview目的、実行時点または材料範囲を区別できない
  - blocking Challenge Findingがあるまま成果をacceptedにしようとする
  - blocking分類を固定したChallenge PolicyまたはHuman裁定へ逆引きできない
  - 選択したVerification Profileの必須test、独立review、Human判断またはEvidenceが欠ける
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
  - blocking Challenge FindingがDelivery Work Itemの`accepted`遷移を拒否する
  - 非意味的な訂正は軽量な整合性検査、Requirementまたはscopeの意味変更は独立reviewを
    含むhigh profileへ決定的に分類される
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
  - Policy Overlay、Policy Adjustment、変更意味、state effect、Verification Profileのevent
  - Implementation Discovery、再利用判断、Human確認、台帳更新、廃止routine検査のevent
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
  - project固有の規則変更を、置換前後のPolicy、理由、Evidence、決定者へ逆引きできる
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

システムは、accepted Delivery Work Itemに束縛されたTask Contract間のinterface、共有
状態、E2E、failure propagation、配置およびlifecycle操作をIntegration Planとして固定し、
全体Intentに対するIntegration Verdictを生成しなければならない。

- 入力
  - accepted Delivery Work Item、Task Contract、Plan bundleのidentity
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
  - staleなContract、Plan、Bindingまたは未acceptedのWork Itemを入力に含む
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

## REQ-WORKFLOW-005 開発入口とreopen routing

システムは、作業の発生源を`new_development`または`maintenance`、継続方法を`fresh`
または`reopen`として独立に固定し、同じTask Contract Deliveryへ決定的にrouteしなければ
ならない。

- 入力
  - work originとcontinuation mode
  - source Intent、Requirement、Contract、baselineのidentity
  - reopen時のprior Work Item、Run、失敗、判断、成果
  - maintenance時のtrigger、維持invariant、regression scope、compatibility、rollback
- 出力
  - 一意IDを持つWork Itemとrouting verdict
  - 作成または再利用するRequirement、Contract、Planのidentity
  - reopen basisとfreshness検査要求
- 停止条件
  - originまたはcontinuation modeが曖昧である
  - prior identityと理由を持たずreopenしようとする
  - 観測可能な義務変更をmaintenance内部だけで確定しようとする
  - 旧成果を上書きしてreopenしようとする
- 復旧条件
  - routing入力を訂正する
  - RequirementまたはContractの新versionを作り、再routeする
- 失敗時に保存するもの
  - routing候補、入力identity、不一致、必要な上流戻り先
- 受け入れ条件
  - 二つのoriginと二つのcontinuation modeの全組合せが共通Deliveryへ到達する
  - reopen後もprior失敗、判断、成果を逆引きできる
  - 義務変更を含むmaintenance fixtureがRequirementsへrouteされる
- 対象外
  - originごとにContract、TDD、Provenanceの別engineを実装すること
  - reopenを旧Work Itemのin-place変更とすること

## REQ-WORKFLOW-006 TDDからの上流改定

システムは、TDD中に発見した不整合をUpstream Inconsistency Findingとして固定し、
Implementation、Design Decision、Task Contract、Requirement、Feature Partitioning、Intentの
うち変更が必要な最下位層へ分類してから、改定または実装継続を判断しなければならない。
同じ入力とEvidenceに対するaccept/reject、義務またはscopeが変わり得るかを
`acceptance_truth_changed`として判定し、軽微修正と意味的reopenを区別しなければならない。

- 入力
  - 検出元Work Item、Contract、Run、TDD phase
  - 競合するRequirement、Design、Test、ImplementationとEvidence
  - 代替Design、実現可能性、risk、costの検討結果
  - prior / proposed Acceptance Criteria、義務、scope
- 出力
  - 改定対象層とclassification verdict
  - `change_semantics`、`acceptance_truth_changed`、`state_effect`と判定根拠
  - prior identity、proposed identity、理由を持つRevision Proposal
  - 影響閉包、stale候補、Test migration候補
  - Human decisionまたは実装継続指示
- 停止条件
  - 実装を通す都合だけで期待またはRequirementを変更しようとする
  - Evidence、prior digest、影響閉包または判断authorityがない
  - 確定済み成果をin-placeで上書きしようとする
  - 意味変更の可能性を解消せず軽微修正として完了しようとする
- 復旧条件
  - 現ContractとTestを維持してImplementationを訂正する
  - 意味不変のeditorialまたはevidence-only訂正として、stateを進めず理由と差分を保存する
  - 承認済みRevision Proposalから新versionを作り、被覆検査とcompileをやり直す
- 失敗時に保存するもの
  - Finding、検出時checkpoint、分類候補、Evidence、不採用案、Human判断
- 受け入れ条件
  - 実装不良fixtureは上流を変更せずImplementationへ戻る
  - 誤字、参照、帰属の訂正でAcceptance Criteriaの真偽と義務が変わらないfixtureは
    `acceptance_truth_changed: false`となり、Contract versionを増やさない
  - Acceptance Criteria、必須義務またはscopeが変わるfixtureは
    `acceptance_truth_changed: true`となり、意味的reopenへrouteされる
  - 軽微修正中に意味変更が判明したfixtureは処理を停止し、Revision Proposalを生成する
  - Requirement不良fixtureは旧Requirementを保持した新versionと依存staleを生成する
  - 上流改定後は旧TDD cycleを再利用せず、新Test versionのredから開始する
- 対象外
  - 実装困難をRequirement誤りと自動判定すること
  - Human判断なしにIntent、scopeまたは必須義務を弱めること

## REQ-WORKFLOW-007 依存発見と循環制御

システムは、TDD中に発見した境界外問題をDependency Discovery Recordとして固定し、
blocking依存を持つ親Work Itemを停止し、Contract依存グラフから実行可能な単一active
leafを選ばなければならない。

- 入力
  - 発見元Work Item、Contract、Run、TDD phase、checkpoint
  - 問題のscope分類、Evidence、blocking判定
  - version付きContract依存graphと許可されたrelation vocabulary
- 出力
  - child Contract候補またはnon-blocking backlog disposition
  - `blocked_by_dependency`、`blocked_by_cycle`またはactive leaf verdict
  - strongly connected componentとCycle Resolution Record
  - 親Work Itemの再開条件
- 停止条件
  - Contract境界外問題を現在のContractへ暗黙追加する
  - 未解決blocking依存または循環を持つWork ItemへRun permitを発行する
  - relation type、方向、owner、versionのいずれかが未定義である
- 復旧条件
  - 誤った辺、ownerまたは依存方向を訂正する
  - 共通前提Contract、版付きinterface、phase分割、Contract統合または上流改定で循環を解く
  - 解消不能なWork Itemをdeferまたはcancelする
- 失敗時に保存するもの
  - discovery、親checkpoint、依存graph、SCC、解消案、選択理由、Human判断
- 受け入れ条件
  - `A requires B requires C`ではCだけがactive leafになる
  - C完了後にB、Aの順でfreshness、stale、compileを再検査して再開する
  - `A requires B requires A`では両方のRun permitを拒否する
  - non-blocking問題は親を止めずbacklogへ移る
- 対象外
  - 問題対処を非永続な再帰call stackだけで管理すること
  - 循環中の実装順を根拠なく選んで実行すること

## REQ-WORKFLOW-008 制御された中止とscope disposition

システムは、進行中Work Itemを`pause`、`cancel`または`close-scope`候補として制御終了し、
未充足義務、最後の有効成果、cleanup、再開または移管条件を失わず保存しなければ
ならない。

- 入力
  - Work Item、Contract、Run、TDD phase、最後のcheckpoint
  - 終了種別、理由分類、Evidence、代替案、risk、cost
  - 未処理義務、部分side effect、cleanupとrollback計画
  - decision authorityとrelease scope
- 出力
  - `paused`または`cancelled`の耐久Work Item状態
  - `deferred`、`withdrawn`、移管または不採用のscope disposition候補
  - cleanup verdict、未充足Requirement、release blocking verdict
- 停止条件
  - 必須Requirementをcancelだけで充足済みにする
  - 部分side effect、cleanup、未処理、移管先または再開条件が未解決である
  - Human判断なしにrelease scope、Intentまたは必須義務を縮小する
- 復旧条件
  - paused Work Itemをfreshness検査後に同Contractの新Runまたは新versionで再開する
  - scopeの新versionとHuman判断を固定し、Portfolio被覆を再検査する
- 失敗時に保存するもの
  - 終了候補、実行者、決定者、理由、Evidence、checkpoint、未処理、cleanup、移管先
- 受け入れ条件
  - pause後に上流変更がなければ新Run、変更があれば新versionへrouteされる
  - cancelした必須Requirementが`unfulfilled`としてreleaseをblockする
  - close-scopeは全残項目の完了、対象外、移管、不採用分類とHuman判断がなければ拒否される
- 対象外
  - pauseまたはcancelをContract acceptanceとみなすこと
  - 未処理を黙って残したままstageまたはreleaseをcompletedにすること

## REQ-WORKFLOW-009 実装前の共通ルーチン照合

システムは、Implementation Task Contractのred確認後、green実装で新規関数または共通処理を
書く前に、固定source treeから生成したSource Symbol Index、Reusable Routine Ledger、
実コードを照合し、Implementation Discovery Recordと再利用判断を確定しなければならない。

- 入力
  - Implementation Task Contract、Delivery Work Item、red Testのidentity
  - 固定source tree、repository、Project BindingのidentityとDigest
  - 同じsource treeから生成したSource Symbol Indexのidentity、generator、schema、Digest
  - Reusable Routine Ledgerのversion、Digest、active／retired routine、alias、統廃合履歴
  - Index、Ledger、Discovery Recordのschemaと原子的I/O policy
  - 予定する新規または変更symbolの責務、入出力、side effect、利用境界
- 出力
  - 検索scope、query、候補symbol、candidate Evidenceを持つImplementation Discovery Record
  - `candidate_found | no_candidate`のdiscovery outcome
  - `candidate_found`の場合は`reuse | extend | merge | split_with_rationale`の判断
  - LLM proposalとHuman confirmationを分離した判断record
  - Task Contract、Work Item、Design Decision、Test、Implementation、commitへの関係
  - Ledger登録、統合、retireまたは再登録の追記候補
  - Portable Lifecycleへ渡す原子的なLedger／Discovery更新操作
- 停止条件
  - source treeとIndexのDigestが一致しない、またはIndexを再生成できない
  - 台帳だけを調べ、固定source treeと実コードを照合していない
  - 候補があるのに4分類、理由またはHuman確認がない
  - `split_with_rationale`に責務境界、非互換条件または分離理由がない
  - retired routineまたはaliasと同じ責務を、再登録判断なしに追加しようとする
  - Discovery RecordをTask Contract、red Testまたは予定Implementationへ結べない
  - schema不適合、閉じた語彙外の判断、過去の判断または統廃合履歴の変更がある
  - Ledgerを検証済みのPortable Lifecycle操作を経ず直接変更しようとする
- 復旧条件
  - current source treeからIndexを再生成し、候補探索をやり直す
  - 既存routineの再利用、拡張または統合へDesign Decisionを訂正する
  - 分離が必要なら理由とHuman確認を追加する
  - retired routineの再登録を新しいDesign DecisionとHuman判断として記録する
- 失敗時に保存するもの
  - source／Index／Ledger identity、検索scope、候補、診断、未確認proposal、拒否理由
- 受け入れ条件
  - 同じ固定source treeとPolicyから同じSource Symbol Index identityを再生成できる
  - 類似候補がないfixtureは`no_candidate`となり、4分類を偽造せずgreen実装へ進める
  - 同一責務の候補があるfixtureは、Human確認済み4分類がなければgreen実装を拒否する
  - stale Index、理由のない分離、retired routineの無断復活をそれぞれ拒否する
  - 再利用判断から候補実装、Task Contract、Test、Design Decision、最終commitへ逆引きできる
  - Ledgerの過去判断と統廃合履歴を上書きせず、新しい記録として追加する
  - schema違反と閉じた語彙外の判断を拒否し、書込み失敗注入後も直前の有効Ledgerを読める
  - Ledgerの直接変更を検出し、検証済み操作による追記へ戻す
- 対象外
  - 名前または埋込み類似度だけで意味的同一性を自動確定すること
  - Human確認だけでsource tree、Indexまたは実コード照合を省略すること
  - 初期Pilotの結果なしにImplementation Task Contractを正式製品Runtimeへ拡大すること

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
- Contract definition lifecycleはTask Contract Controlが所有し、Work Item lifecycle、
  routing、block、resume、termination、Run permitはWorkflowが所有する。
- `REQ-WORKFLOW-004`の自己適用はstableなContract能力だけを必須経路へ使用する。
- `REQ-WORKFLOW-005`〜`009`を追加し、entry routing、上流改定、依存・循環、制御終了、
  実装前共通ルーチン照合をWorkflowの観測可能な義務とする。
- `REQ-WORKFLOW-009`は初期段階ではReviewCompass3自身のImplementation Task Contractへ
  Project Architecture Policyとして適用し、Pilot後のHuman判断なしに正式Runtime範囲へ
  拡大しない。

### FEAT-SESSION-RECORDS

- `REQ-SESSION-001`は取込みsource universeをContext obligation、利用者判断、Project
  Bindingへ束縛し、Session取込みを要求しないContractの実行を妨げない。
- `REQ-SESSION-002`はraw原本、伏字化派生物、要約、来歴を別identity、別access、別retention、
  別削除Policyへ置き、派生物をContext candidateとしてだけ渡す。
- `REQ-SESSION-003`は追記、非追記変更、消失のmutation verdictをContext freshnessと
  Provenanceへ結び、未解決時に旧派生物の再利用を拒否する。
- Session RecordsはWork Item、Run、Context採否を直接変更せず、Session Evidence Sourceとして
  Context RuntimeとPortable Lifecycleへ接続する。

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
- `REQ-IMPROVE-001`はEvaluation case、condition、pair、trial、実行条件を固定し、異なる条件を
  同一比較群にしない。
- `REQ-IMPROVE-002`は直接的なWorkflow設定変更を置換し、Human判断付きの版付きImprovement
  Proposal、対象owner、prior／proposed identity、stale閉包、rollback、次trialを要求する。
- 承認済みProposalも各ownerの通常のchallenge、compile、migrationまたはPolicy解決を迂回せず、
  未承認または検証不足の候補を現行方針から隔離する。

## 3. 新しい境界

最低限、次のinterfaceを設計へ追加する。

- Requirements / Trace → Task Contract Portfolio
- Task Contract Control → Context Runtime
- Task Contract Control → Workflow
- Task Contract Control → Harness
- Task Contract Control → Semantic Trace
- Task Contract Control → Portable Lifecycle
- Task Contract Control → Evidence Evaluation
- Workflow → Task Contract Control / Portfolio
- Workflow → Semantic Trace
- Workflow → Requirements change authority
- Session Evidence Source → Context Runtime
- Session Evidence Source → Portable Lifecycle / Semantic Trace
- Evidence Evaluation → Self Improvement
- Self Improvement → Task Contract / Compiler / Policy / Capture Plan owner

各interfaceはContract ID、version、digest、Plan ID、obligation ID、Work Item ID、
relation type、failure verdictを持つ。Task Contract Controlは各consumerの状態遷移を
直接行わず、WorkflowはContractまたはRequirementの版を直接変更しない。

## 4. 要件差分の完了条件

- 新しい`REQ-CONTRACT-001`〜`007`と`REQ-WORKFLOW-005`〜`009`の各入力、出力、停止、
  復旧、保存、受け入れ、対象外が確定する。
- 既存37 requirementsへの影響を`preserve / adapt / replace / defer`で全件分類する。
- 旧9 design、29 interface、8 state machine、14 protocolを全件分類し、replace対象にも
  successor owner、failure verdict、後継testを割り当てる。
- 新旧Requirementの順逆被覆に未解決がない。
- 新しいinterfaceと所有責務が競合しない。
- 受け入れ試験ID、oracle種別、negative caseが各新Requirementへ一件以上ある。
- 第5段の旧承認候補を上書きせず、新しい差分監査へ結べる。
- Session Evidence SourceとSelf Improvement Proposalの旧testを含む全37 acceptance testに、
  `preserve / adapt / replace`と後継test IDがある。
- ReviewCompass2のP-5、`R-F6-010`、`R-F6-011`を`REQ-WORKFLOW-009`の各obligationへ
  逆引きでき、4分類、Human確認、追記履歴、retired routine検査を取りこぼしていない。
