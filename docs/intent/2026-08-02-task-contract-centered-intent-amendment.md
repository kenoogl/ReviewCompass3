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

Context、Harness、Workflow、Triage、Trace、Portable Lifecycle、Evidence
Evaluationは、Task Contractから導出されたPlanを受け取るが、それぞれの状態と
関門を所有し続ける。Task ContractまたはCompilerは、各componentの状態を直接
変更しない。

Reviewは、成果のContract適合性を確認するContract Conformance Review、Contract確定前の
欠落と境界を確認するDefinition Challenge、成果検証後に上位Intentと隣接Contractへの
影響を確認するFinal Contract Challengeに分ける。

accepted Contractは局所成功だけでrelease可能とせず、interface、共有状態、E2E、
failure propagation、配置およびlifecycle操作をCross-Contract Integrationで検証する。

## 4. 「何をしないか」への追加

- Task ContractをRequirementsの正しさや完全性そのものとは扱わない。
- Contractを満たすことだけを理由に、Contract外の重大な問題を無視しない。
- CompilerまたはLLMの推論だけで、欠落Contract項目や実行Planを暗黙に補完しない。
- ReviewCompass3を任意分野のTaskを実行する汎用Agent Runtimeへ拡張しない。
- Contract、Requirement、Policy変更後に、旧Context、旧Plan、旧Runを有効として
  再利用しない。
- Provenance収集を理由に、機微情報、raw data、利用者データを無制限に保存しない。
- 開発checkoutや特定の開発アプリとの物理的な相対位置へ製品を固定しない。

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

## 6. 「成功の判定基準」への追加

- 全必須RequirementがTask Contractまたは明示的なHuman非採用判断へ結ばれる。
- 全Contract obligationが必要なPlanへ被覆され、各Plan項目を元obligationへ
  逆引きできる。
- 未充足Context、未許可能力、未対応Acceptance Criteria、Provenance欠落がある場合、
  Run開始または完了を拒否できる。
- Contract変更時に依存Context、Plan、Runをstaleとして再構築できる。
- Conformance Finding、Definition Challenge Finding、Final Contract Challenge Findingを
  混同せず保持できる。
- accepted Contract間のIntegration VerdictとE2E Evidenceをrelease判断へ結べる。
- RequirementからContract、Context、Execution、Result、Evidence、Human判断までを
  一続きにたどれる。
- 既存方式と固定条件で比較し、Evidence Coverage、Context量、Finding品質、
  Human負担、リードタイム、費用、Provenance完全性を実測できる。
- 開発checkout、インストール先、対象project、runtime dataを分離した環境で同じ
  論理動作を検証できる。

## 7. 意図や制約が衝突した場合

上位IntentとTask Contractが衝突する場合はIntentを優先し、Contractを改定する。
RequirementsとContractが衝突する場合はContractを確定せず、Requirementsの曖昧さ、
競合、欠落をHumanへ提示する。

速度、Context削減、自動導出よりも、責務境界、最小権限、一次証拠への追跡、
機微情報と既存成果の保護を優先する。ただし、評価に不要な記録とHuman介入を無制限に
増やさず、実測に基づきCapture PlanとContract粒度を改善する。
