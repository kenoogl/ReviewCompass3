# Task-Contract-Centric Context Engineering Architecture

## 1. 基本構想

本アーキテクチャは、明示的かつ機械解釈可能な責務境界を持つ**Task Contract**を中心に、ユーザの意図または要求を、LLM・ツール・人間が協調する実行ランタイムへ接続する。

基本構造は次のとおりである。

```
要求・ユーザ意図
        ↓
構造化された要件
        ↓
Task Contract
        ↓
実行ランタイム
├── コンテキスト要求の導出
├── コンテキストの収集・構築
├── LLM・Tool・Humanの実行
├── 実行ハーネス
├── 成果物の検証
└── Provenanceの収集
        ↓
成果物・証拠・状態更新
```

Task Contractは、単なるタスク名やプロンプトではない。遂行すべき責務、その境界、必要な情報、利用可能な能力、期待される成果物、検証条件を宣言的に表現した実行契約である。

本アーキテクチャの中心命題は次のように表現できる。

> Task Contractを要求と実行の間に置くことにより、LLMに何を実行させるかだけでなく、何を根拠として、どの範囲で、どのツールを用い、どの条件を満たすまで実行し、何を証拠として残すかを一貫して制御する。

## 2. アーキテクチャ全体

```
flowchart TB
  A["要求・ユーザ意図"] --> B["構造化された要件"]
  B --> C["Task Contract"]

  C --> D["Task Contract Interpreter / Compiler"]

  D --> CP["Context Acquisition Plan"]
  D --> RP["Review / Execution Plan"]
  D --> HP["Harness Configuration"]
  D --> VP["Verification Plan"]
  D --> PP["Provenance Capture Plan"]
  D --> UP["Human Interaction Plan"]

  CP --> CA["Context Runtime"]
  CA --> CM["Context Manifest"]

  RP --> ER["Execution Orchestrator"]
  HP --> ER
  UP --> ER
  CM --> ER

  ER --> LLM["LLM"]
  ER --> TOOL["Tools"]
  ER --> HUMAN["Human"]

  LLM --> RESULT["成果物・判断・状態変更"]
  TOOL --> RESULT
  HUMAN --> RESULT

  RESULT --> VERIFY["Contract Conformance Verification"]
  VP --> VERIFY
  PP --> PROV["Provenance Store"]
  CA --> PROV
  ER --> PROV
  VERIFY --> PROV

  VERIFY -->|未充足・矛盾| CA
  VERIFY -->|Contract不備| B
  VERIFY -->|完了| OUT["検証済み成果物"]
```

Task Contractは、コンテキスト、レビュー、ハーネス、Provenanceを個別に管理するための追加文書ではない。これらを系統的に導出するための**共通制御面（control plane）**として機能する。

## 3. 各層の役割

### 3.1 要求・ユーザ意図

最上位には、自然言語で表現された要求またはユーザ意図が存在する。

例：

- この変更が認証要件を満たすかレビューしたい
- 関連研究を網羅的に調査したい
- 実験結果を解析して次の実験を提案してほしい

この段階の情報は曖昧であり、そのままでは実行責務、必要なコンテキスト、完了条件を一意に決定できない。

### 3.2 構造化された要件

自然言語の要求・意図を、Task Contractへ写像可能な中間表現へ変換する。

構造化要件には、例えば以下を含める。

- 目的
- 対象
- 制約
- ステークホルダー
- 期待する成果
- 品質条件
- 既知の前提
- 不明点
- 優先度
- 根拠となる要求
- 要求間の依存関係

構造化要件は、大域的な要求整合性を保持する。一方、Task Contractは、そこから局所的かつ実行可能な責務を切り出す。

### 3.3 Task Contract

Task Contractは本アーキテクチャの中心概念であり、次のように定義する。


$$
TC =
\langle
R, B, P, CO, C, O, A, V, E
\rangle
$$
ここで、

- (R)：Responsibility
- (B)：Responsibility Boundary
- (P)：Preconditions
- (CO)：Context Obligations
- (C)：Allowed Capabilities
- (O)：Expected Outputs
- (A)：Acceptance Criteria
- (V)：Provenance Obligations
- (E)：Escalation Policy

である。

代表的な構造は次のとおりである。

```
TaskContract
├── Identity
│   ├── taskContractId
│   ├── version
│   └── sourceRequirements
├── Responsibility
│   ├── goal
│   ├── obligations
│   ├── inScope
│   ├── outOfScope
│   └── prohibitedEffects
├── Preconditions
│   ├── requiredState
│   ├── assumptions
│   └── dependencies
├── ContextObligations
│   ├── requiredEvidence
│   ├── authoritativeSources
│   ├── freshness
│   ├── trust
│   └── confidentiality
├── Capabilities
│   ├── allowedTools
│   ├── permissions
│   └── resourceBudget
├── Deliverables
│   ├── outputSchema
│   ├── expectedArtifacts
│   └── allowedSideEffects
├── Verification
│   ├── acceptanceCriteria
│   ├── reviewCriteria
│   └── completionConditions
├── ProvenanceObligations
│   ├── requiredTraceability
│   ├── evidenceRetention
│   └── executionRecording
└── Escalation
    ├── humanApprovalPoints
    ├── unresolvedCondition
    └── failurePolicy
```

責務境界には、何を行うかだけでなく、何を行わないか、どの依存関係まで確認するか、どの副作用を禁止するかを含める。

### 3.4 実行ランタイム

実行ランタイムはTask Contractを解釈し、実行可能な計画と環境を構成する。

実行ランタイムには以下を含む。

1. Task Contract Interpreter／Compiler
2. Context Runtime
3. Execution Orchestrator
4. Harness
5. Verification Runtime
6. Provenance Runtime
7. Human Interaction Runtime

実行ランタイムは、単にLLMを呼び出す機構ではない。Task Contractを満たすために必要なコンテキスト、能力、検証、証拠収集を統合的に制御する。

## 4. コンテキスト要求と動的コンテキスト構築

Task Contractから、実行に必要なContext Requirementsを導出する。
$$
ContextRequirements = Derive(TC,\ WorkflowState)
$$
各Context Requirementには、次の情報を含める。

- 対応するContract obligation
- 必要な情報の種類
- 情報源
- 対象範囲
- 必須／任意
- 鮮度
- 信頼性
- アクセス権限
- 情報量の上限
- 競合時の解決方針
- Provenance要件
- 充足判定条件

実行時には、Context Requirementsを現在の状態へ束縛する。
$$
ContextManifest =
Assemble(ContextRequirements,\ WorkflowState,\ Sources,\ Policy,\ Budget)
$$
Context Manifestには、LLMへ実際に提供された情報だけでなく、次を記録する。

- 選択されたコンテキスト
- 対応するContext Requirement
- 情報源とバージョン
- 要約・圧縮・統合などの変換
- 除外された候補
- 解消されていないContext Requirement
- 情報間の矛盾
- トークンおよび実行コスト

この仕組みにより、コンテキストは単なる関連文書の集合ではなく、Task Contractの責務を充足するために構成された実行時成果物となる。

## 5. Task Contractから導出される実行要素

```
Task Contract
↓ compile
├── Context Acquisition Plan
├── Review / Execution Plan
├── Tool and Permission Plan
├── Human Interaction Plan
├── Verification Plan
├── Provenance Capture Plan
└── Failure and Escalation Plan
```

| Task Contract要素      | 導出される実行要素                 |
| ---------------------- | ---------------------------------- |
| Responsibility         | LLMに与える実行目標                |
| In-scope               | 調査・レビュー・変更対象           |
| Out-of-scope           | 除外対象、境界逸脱の検出           |
| Context obligations    | 検索・取得・GraphRAG計画           |
| Preconditions          | 実行前チェック                     |
| Allowed tools          | 利用可能なツール群                 |
| Permissions            | ファイル、ネットワーク、API権限    |
| Output schema          | 構造化出力とバリデータ             |
| Acceptance criteria    | テスト、レビュー、終了判定         |
| Human approval         | Human-in-the-loopゲート            |
| Provenance obligations | ログ、証拠、引用、判断履歴         |
| Failure policy         | 再試行、代替手段、エスカレーション |

## 6. LLMの可用性を高める仕組み

ここでいう「LLMの可用性」は、システム稼働率としてのavailabilityだけを意味しない。LLMを実務上、制御可能かつ信頼可能な形で利用できる性質を意味する。

論文では、曖昧さを避けるため、以下のように分解することが望ましい。

- Task applicability：対象Taskへ適用できる
- Context adequacy：必要な情報が揃っている
- Controllability：権限と責務境界を制御できる
- Dependability：期待する成果を安定して生成できる
- Auditability：実行根拠を追跡できる
- Adaptability：状態変化へ対応できる
- Verifiability：成果を責務に対して検証できる

Task ContractはLLMそのものの能力を向上させるのではない。LLMが能力を発揮するための責務、情報、実行環境、検証条件を整えることで、LLMの**実務上の利用可能性と信頼性**を高める。

## 7. メリットと期待される効果

### 7.1 レビュー観点の明確化

Task Contractから、責務ごとのReview Obligationsを導出できる。

従来のレビュー：

```
このコードに問題がないかレビューする
```

Task Contractに基づくレビュー：

```
宣言された責務を満たしているか
責務境界を越えた変更がないか
禁止された副作用がないか
前提条件が維持されているか
必要な証拠が存在するか
Acceptance Criteriaを満たしているか
```

期待される効果は次のとおりである。

- 一般論的・表面的なレビュー指摘の削減
- 責務違反に関する検出率の向上
- 指摘と要求・仕様との対応付け
- 根拠を伴うレビュー結果
- 責務外変更や副作用の検出
- レビュー完了条件の明確化
- 人間によるレビュー判断の効率化

ただし、Contractが狭すぎると重大なContract外問題を見落とす危険がある。そのため、レビューは二層構造とする。

1. Contract-conformance review：Contractへの適合性を検証する
2. Contract-challenge review：Contract自体の欠落や境界の妥当性を検証する

### 7.2 コンテキスト特性の改善

Task Contract中心のコンテキスト構築は、意味的類似性だけに基づく検索とは異なる。

望ましいコンテキスト特性は次のとおりである。

| 特性              | 意味                                       |
| ----------------- | ------------------------------------------ |
| Relevant          | 責務と関係している                         |
| Sufficient        | 責務遂行に必要な情報を満たす               |
| Minimal           | 不要な情報を過剰に含まない                 |
| Fresh             | 必要な鮮度を満たす                         |
| Authoritative     | Contractが指定する信頼可能な情報源に基づく |
| Consistent        | 矛盾が検出・管理されている                 |
| Provenance-aware  | 出所と変換履歴を追跡できる                 |
| Permission-aware  | アクセス権限を満たす                       |
| Budget-aware      | トークン、時間、費用の制約を満たす         |
| Obligation-linked | 各情報がどの責務に必要か説明できる         |

期待される効果は次のとおりである。

- 不要なコンテキストの削減
- 必要証拠の欠落検出
- 古い情報や矛盾した情報の検出
- コンテキスト量の制御
- LLM出力の根拠明確化
- 同一Task Contractの状態変化への適応
- 「多くの情報」ではなく「責務を満たす情報」の提供

### 7.3 ハーネス構築の容易化

Task Contractは、実行ハーネスの構成仕様として利用できる。

Task Contractから以下を生成または設定する。

- LLMへの実行指示
- 利用可能なツール
- ファイル・API・ネットワーク権限
- コンテキスト取得機構
- 出力スキーマ
- バリデータ
- テスト
- Human approvalゲート
- 実行終了条件
- 再試行条件
- エスカレーション条件
- Provenance収集フック

これにより、ハーネスの設定根拠がTask Contractへ統一される。

期待される効果は次のとおりである。

- ハーネス構築時の手動設定削減
- Taskと実行環境の設定不整合削減
- Contract変更時の影響範囲特定
- ハーネス部品の再利用
- 最小権限によるツール利用
- 異なるLLM・ツールへの移植性
- 実行と検証の一体化

新規性としては「ハーネスが作りやすい」ことではなく、**Task Contractからハーネス構成を系統的に導出できること**が重要である。

### 7.4 Provenanceの意味的強化

従来のProvenanceは、使用したデータ、実行した処理、生成された成果物を記録する。

Task Contractを意味的アンカーとすることで、さらに以下を説明できる。

- なぜそのコンテキストが必要だったか
- どの責務を裏付ける証拠か
- なぜそのツールを実行したか
- 誰がどの判断を行ったか
- どのAcceptance Criterionを検証したか
- どの証拠に基づき責務を満たしたと判断したか

Task Contractから、Provenance Capture Planを導出する。
$$
ProvenanceRequirements = Derive(TC)
$$
実行後には、次の追跡関係を構築する。
$$
Requirement
\leftrightarrow
TaskContract
\leftrightarrow
Context
\leftrightarrow
Execution
\leftrightarrow
Result
\leftrightarrow
Evidence
$$
期待される効果は次のとおりである。

- Provenanceの収集範囲の明確化
- 必須Provenanceの欠落検出
- 要求から成果物までの双方向追跡
- LLM出力の説明可能性
- 人間判断の帰属可能性
- 監査効率の向上
- 要求変更時の影響分析
- 過去実行の再構成
- レビュー結果の根拠確認

新規性はProvenanceを保存することではなく、**Task Contractが要求するProvenanceを事前に規定し、責務単位でその完全性を検証すること**にある。

### 7.5 要求整合性と局所実行性の両立

構造化要件によってシステム全体の要求関係を保持し、Task Contractによって実行可能な責務へ分割する。

これにより、

- 仕様駆動開発の大域的整合性
- TDDの局所的な実行・検証単位
- LLMの動的コンテキスト構築
- ワークフローランタイムの状態管理

を接続できる。

テストはTask Contract全体ではなく、そのAcceptance CriteriaまたはEvidence Obligationを実行可能にした一つの実現形態として位置付ける。

### 7.6 Human-AI協調

Task Contractに人間へ問い合わせる条件を明示できる。

- 要件が曖昧な場合
- 必要なContextが取得できない場合
- 情報源が矛盾する場合
- 高リスクなツール実行が必要な場合
- Contractの責務境界を越える場合
- Acceptance Criteriaを自動判定できない場合

これにより、人間はすべての実行へ介入するのではなく、Contract上、人間判断が必要な箇所へ選択的に参加できる。

## 8. 二つのケーススタディへの適用

### 8.1 ReviewCompass

```
ソフトウェア要求
→ Task Contractへ写像可能な構造化要件
→ Review / Implementation Task Contract
→ 要件・設計・コード・テスト・履歴の収集
→ LLM・解析ツール・人間によるレビュー
→ Contract適合性とContract妥当性の検証
→ 根拠付きレビュー結果
```

Task Contractは、変更が果たすべき責務、責務境界、必要な設計情報、レビュー観点、テスト条件、禁止される副作用を定義する。

### 8.2 Scientific Concierge

```
研究者の意図
→ 構造化された研究要件
→ Research Task Contract
→ 論文・データ・実験履歴・ツール・専門家判断の収集
→ LLM・科学ツール・人間による実行
→ 成果物・引用・実験証拠の検証
```

Task Contractは、調査対象、採否基準、必要な一次資料、実験条件、利用可能なツール、Human approval、再現性・引用要件を定義する。

両ケースの違いは利用するコンテキストやツールであり、基本アーキテクチャは共通する。

## 9. 新規性の位置付け

個別には、以下の概念は既存研究に存在する。

- タスク固有の情報検索
- 動的コンテキスト構築
- Design by Contract
- Requirements Traceability
- ワークフロー実行
- Agent Harness
- Provenance記録
- Human-in-the-loop
- テストによる検証

したがって、これらを個別の新規性として主張すべきではない。

本研究の新規性候補は、次の統合的な導出関係にある。
$$
TaskContract
\rightarrow
\begin{cases}
Context\ Requirements \
Review\ Obligations \
Harness\ Configuration \
Human\ Interaction\ Policy \
Verification\ Plan \
Provenance\ Obligations
\end{cases}
$$
すなわち、

> 明示的かつ機械解釈可能な責務境界を持つTask Contractを、要求、コンテキスト、レビュー、実行ハーネス、Human-AI協調、検証、Provenanceを接続する実行可能な中間表現として導入する。

ことが本質的なContributionとなる。

## 10. 研究仮説

- H1：Task Contractは、通常のタスク記述よりLLMによる責務違反の検出率を向上させる。
- H2：Task Contractから導出したコンテキストは、通常のRAGや全文投入より高いEvidence Coverageを達成する。
- H3：Task Contractは、レビューにおける一般論的・責務外の指摘を削減する。
- H4：Task Contractからのハーネス構成導出は、手動構築の工数と設定不整合を削減する。
- H5：Task Contractに基づくProvenanceは、要求から成果物までの追跡可能性と監査性を向上させる。
- H6：ワークフロー状態が変化しても、同一Task Contractから適切なContext Manifestを再構築できる。
- H7：Task Contractは、Human interventionを必要な箇所へ限定できる。

## 11. 評価指標

| 評価領域     | 指標                                                         |
| ------------ | ------------------------------------------------------------ |
| Task遂行     | 成功率、Acceptance Criteria充足率                            |
| レビュー     | 欠陥Recall、指摘Precision、採用率、責務外指摘率              |
| コンテキスト | Evidence Recall、Context Precision、トークン数、未充足要求数 |
| ハーネス     | 構築時間、手動設定数、自動導出率、設定不整合数               |
| Provenance   | Evidence Coverage、Provenance Completeness、追跡可能率       |
| Human-AI協調 | 問い合わせ数、承認負担、判断時間                             |
| 適応性       | 状態変更後の成功率、再構築時間                               |
| コスト       | トークン、ツール呼び出し、遅延、金銭コスト                   |

## 12. 研究のPositioning

本研究は、Prompt EngineeringやRAGの拡張だけではない。また、単なるAgent RuntimeやWorkflow Runtimeでもない。

本研究の位置付けは、次のように表現できる。

> Task-Contract-Centric Context Engineering is an architectural approach in which a machine-interpretable responsibility contract serves as the executable intermediate representation connecting structured requirements with dynamic context assembly, heterogeneous execution runtimes, verification, and provenance.

さらに簡潔には、次の表現が可能である。

> **Task Contract as the control and provenance plane for LLM-mediated workflows.**

このアーキテクチャの目的は、LLMへより多くの情報を与えることではない。Task Contractによって、LLMが果たすべき責務、必要な情報、許可された行為、完了条件、必要な証拠を明確にし、LLMを実際のソフトウェア開発および科学研究ワークフローで、制御可能・検証可能・追跡可能な形で利用できるようにすることである。