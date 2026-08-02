---
lifecycle: provisional
normative_status: successor-candidate
promotion_required: true
---

# Task Contract中心化によるintent改定

## 1. 対象と証拠保持

承認済みの`2026-07-27-reviewcompass3-intent-draft.md`と、開発方法を分離した
`2026-08-02-development-policy-amendment.md`は固定証拠として書き換えない。
本文書はそれらの後に適用する製品intentの改定候補である。

本改定はTask ContractをReviewCompass3の中心概念へ昇格するが、原理A、原理B、
Humanの最終判断、機微情報保護、fail-closed、ポータブルな配置を維持する。

## 2. 「何のために作るか」の追加

ReviewCompass3は、構造化されたRequirementsから局所的なレビュー責務を版付きの
Task Contractとして切り出し、必要なContext、実行能力、検証、Human判断および
Provenanceを同じ責務へ結び付ける。

これにより、要求から成果物までの大域的整合性と、変更単位で実行・検証可能な
局所責務を両立し、LLM、Tool、Humanが何を根拠に、どの境界と権限で、何を満たすまで
処理したかを後から検証できるようにする。

## 3. 「どのようなものを作るか」の置換・追加

既存のReview Task説明を次のように拡張する。

Review Task Contractを、構造化RequirementsとTask Runtimeを接続する
機械解釈可能な中間表現とする。Contractは責務、境界、前提、Context obligation、
許可能力、期待成果、Acceptance Criteria、Provenance obligation、Escalation Policyを
持つ。

Task Contractから、Context Acquisition、Review / Execution、Harness and
Capability、Verification、Provenance Capture、Human Interactionの各Planを
版付きの決定的処理で導出する。各Plan項目を元Contract obligationへ逆引きでき、
未対応、競合、未解決がある場合は実行を開始しない。

Context、Harness、Workflow、Triage、Trace、Session Evidence Source、Portable Lifecycle、
Evidence Evaluation、Self Improvementは、Task Contractから導出されたPlanまたは版付き
成果を受け取るが、それぞれの状態と関門を所有し続ける。Task ContractまたはCompilerは、
各componentの状態を直接変更しない。

Session Evidence Sourceは、利用者が許可したsource universeだけを取り込み、raw原本、
伏字化派生物、要約、mutation verdictを別identityと別保存Policyで管理する。Session取込みを
要求しないContractの実行は妨げない。

Self ImprovementはEvaluation Ledgerから改善仮説を作るが、現行設定を直接変更しない。
固定比較とHuman判断を経たContract、Compiler、PolicyまたはCapture Planの新version候補を
各ownerへ渡し、stale影響検査後の次trialとして適用する。

ReviewCompass3自身の実装では、新規関数または共通処理を書く前に、固定source treeから
生成したSource Symbol Index、共通ルーチン台帳、実コードを照合する。類似候補がある場合は
`reuse / extend / merge / split_with_rationale`のいずれかを選び、Task Contract、Design
Decision、Test、Implementationへ結ぶ。これはコード量の最小化自体ではなく、同じ責務の
重複実装と廃止済み処理の無断復活を防ぎ、保守対象を減らして品質を安定させるためである。

Reviewは、成果のContract適合性を確認するContract Conformance Review、Contract確定前の
欠落と境界を確認するDefinition Challenge、成果検証後に上位Intentと隣接Contractへの
影響を確認するFinal Contract Challengeに分ける。

accepted Delivery Work Itemに束縛されたContractは、局所成功だけでrelease可能とせず、
interface、共有状態、E2E、failure propagation、配置およびlifecycle操作を
Cross-Contract Integrationで検証する。

新規開発とmaintenanceは異なる入口プロファイルとして同じTask Contract Deliveryへ
合流させる。reopenは独立レーンにせず、旧成果を保持して新Runまたは新versionへ移る
継続プロトコルとする。

実装中に上流不整合、境界外問題、blocking依存または循環を発見した場合、現在の
Contractへ暗黙にscopeを追加しない。問題を固定してWork Itemを停止し、上流改定、依存
Contract、backlog、継続、中止のいずれかへ分類する。

既存文書や成果の訂正は、受入条件の真偽、義務またはscopeが変わるかを基準に、意味不変の
軽微修正と意味的reopenへ分ける。reviewとHuman介入の強度は一律にせず、変更意味、状態への
影響、risk、side effectから選択する。

## 4. 「何をしないか」への追加

- Task ContractをRequirementsの正しさや完全性そのものとは扱わない。
- Contractを満たすことだけを理由に、Contract外の重大な問題を無視しない。
- CompilerまたはLLMの推論だけで、欠落Contract項目や実行Planを暗黙に補完しない。
- ReviewCompass3を任意分野のTaskを実行する汎用Agent Runtimeへ拡張しない。
- Contract、Requirement、Policy変更後に、旧Context、旧Plan、旧Runを有効として
  再利用しない。
- Provenance収集を理由に、機微情報、raw data、利用者データを無制限に保存しない。
- 開発checkoutや特定の開発アプリとの物理的な相対位置へ製品を固定しない。
- 入れ子になった問題を非永続な作業stackだけで管理せず、Contract依存グラフへ記録する。
- cancel、deferまたはclose-scopeをRequirement充足とみなさない。
- Session raw、伏字化派生物、要約を同じidentity、access、retention、削除境界へ置かない。
- Self ImprovementからWorkflow設定または現行Policyを直接変更しない。
- 旧interface本数、状態機械数、protocol本数を維持すること自体を設計目的にしない。
- 台帳だけを既存実装の事実源とせず、固定source treeの実コード照合を省略しない。
- 類似候補がある新規関数を、判断記録または分離理由なしに追加しない。
- 廃止済み共通ルーチンを、明示的な再登録判断なしに復活させない。

## 5. 「前提・制約」への追加

- Task Contractは一意ID、version、source Requirement、内容Digestを持つ。
- 全Contract obligationを必要な導出Planへ結び、順逆の被覆を機械検査する。
- 同じContract、Compiler、Policyからは同じPlan bundle identityを生成する。
- Contractまたは上流入力が変わった場合は、依存成果をstaleとして新しいversionを
  作る。
- Tool、ファイル、network、API権限と許可副作用をContractへ明示し、最小権限で
  実行する。
- Operational Provenanceの必須範囲を実行前に定め、欠落時は成果を検証済みにしない。
- 評価観測の欠測と業務上の適合性失敗を区別する。
- 配置は論理rootとManifestから解決し、端末固有パスを成果物identityにしない。
- projectの論理identityは安定IDとし、可変な内容digest、repository root、checkoutごとの
  Bindingから分離する。
- Work Itemは単一active leafを原則とし、blocking依存または循環がある状態でRun permitを
  発行しない。
- 確定済みRequirement、Contract、Testを実装都合で上書きせず、新version、変更理由、
  stale影響閉包、Human判断を結ぶ。
- 同じ入力とEvidenceに対するaccept/reject、義務またはscopeが変わるかを記録し、意味不変の
  訂正だけでworkflow stateを人工的に進めない。
- project固有の方針調整は、base Policy、置換規則、理由、Evidence、決定者を持つ版付き
  Overlayとして保持する。
- pause、cancel、defer、withdraw、close-scopeでは、最後の有効成果、未充足義務、
  cleanup、再開または移管条件を保存する。
- 旧第5段design、interface、state machine、protocol、acceptance testは、固定Digestと
  `preserve / adapt / replace`判定を持ち、replace時も後継ownerと後継testへ結ぶ。

## 6. 「成功の判定基準」への追加

- 全必須RequirementがTask Contractまたは明示的なHuman非採用判断へ結ばれる。
- 全Contract obligationが必要なPlanへ被覆され、各Plan項目を元obligationへ
  逆引きできる。
- 未充足Context、未許可能力、未対応Acceptance Criteria、Provenance欠落がある場合、
  Run開始または完了を拒否できる。
- Contract変更時に依存Context、Plan、Runをstaleとして再構築できる。
- Conformance Finding、Definition Challenge Finding、Final Contract Challenge Findingを
  混同せず保持できる。
- accepted Delivery Work Itemに束縛されたContract間のIntegration VerdictとE2E Evidenceを
  release判断へ結べる。
- new developmentとmaintenanceを共通Deliveryで処理し、freshとreopenを独立に選べる。
- TDD中に発見したblocking依存を別Contractへ切り出し、依存先完了後にfreshnessとstaleを
  再検査して親Work Itemを再開できる。
- Contract依存循環を実行前に検出し、解消またはHumanによる制御終了まで関係Runを
  開始しない。
- 中止した必須Requirementを未充足として保持し、明示的なscope改定なしにreleaseへ
  進めない。
- RequirementからContract、Context、Execution、Result、Evidence、Human判断までを
  一続きにたどれる。
- 既存方式と固定条件で比較し、Evidence Coverage、Context量、Finding品質、
  Human負担、リードタイム、費用、Provenance完全性を実測できる。
- 開発checkout、インストール先、対象project、runtime dataを分離した環境で同じ
  論理動作を検証できる。
- Session取込み範囲、raw／派生物分離、mutation、access、retention、削除を検証できる。
- Improvement Proposalを元Evaluation trial、Human判断、変更対象version、stale閉包、
  次trialへ逆引きでき、直接設定変更を拒否できる。
- 旧9 design、29 interface、8 state machine、14 protocol、37 acceptance testの全件を
  後継owner、schema、failure verdictまたはtestへ逆引きできる。
- 新規関数または共通処理の変更を、固定source tree、候補、再利用判断、Human確認、
  Task Contract、Design Decision、Test、Implementationへ逆引きできる。
- staleなSource Symbol Index、未確認の類似判断、理由のない分離、廃止済みroutineの復活を
  green実装開始前に拒否できる。

## 7. 意図や制約が衝突した場合

上位IntentとTask Contractが衝突する場合はIntentを優先し、Contractを改定する。
RequirementsとContractが衝突する場合はContractを確定せず、Requirementsの曖昧さ、
競合、欠落をHumanへ提示する。

速度、Context削減、自動導出よりも、責務境界、最小権限、一次証拠への追跡、
機微情報と既存成果の保護を優先する。ただし、評価に不要な記録とHuman介入を無制限に
増やさず、実測に基づきCapture PlanとContract粒度を改善する。
