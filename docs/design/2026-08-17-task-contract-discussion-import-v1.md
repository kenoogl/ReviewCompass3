# Task Contract議論メモ（repo外検討メモの取り込み） v1

- 取り込み日：2026-08-17
- 取り込み者：Claude（利用者指示「論文構想2文書もrepoへ取り込み」）
- 出自：`/Users/keno/LLMsession/RC3/TaskContract議論.md`（利用者と外部LLMの検討記録。
  原文SHA-256 `73b0ca9ce2684759ba652db517f5932f82fa4c3829da376332190961af29cbe9`・36,730 bytes）
- 性格：**研究構想の時点記録**（構造化要件→Task Contract→TDDの三層・Task-Centric Context
  Engineeringの統一・論文2本構成の議論）。評価データ取得計画
  （`docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md`）の固定入力
- 以下は原文のverbatim転記（無改変）

---


さいごに議論した内容をまとめてください．1）何が問題となっているか，2）どういう方法で問題を解決しようとしているのか，その着眼点は？，3）具体的な手続き，4）新規性と考える点，5）効果，動的ワークフローへの適用など．

今回の議論は、ReviewCompassやTask Runtimeから少し離れて、**「LLM時代の開発プロセスそのものはどうあるべきか」**という観点で整理できたと思います。途中でRuntimeやPlannerの話へ広がりそうになりましたが、最後には「開発プロセス」の議論に戻ったことで、かなり本質が見えてきました。

------

# 1. 問題意識

## 従来の仕様駆動開発の問題

仕様駆動開発では、

```
要求 ↓ 要件 ↓ 基本設計 ↓ 詳細設計 ↓ 実装
```

というトップダウンの流れになります。

しかし、

- 要件から設計へ進むにつれて文書量が爆発的に増える
- 一つの仕様書の中に要求・設計・実装方針が混在する
- レビュー対象が100ページ単位になる
- レビューの責任範囲が曖昧になる

という問題があります。

つまり、

> **仕様が正しいことを保証するためのレビューコストが非常に高い。**

------

## 一方、TDDの問題

TDDでは、

```
テスト ↓ 実装
```

という非常に小さい単位で開発できます。

そのため

- レビューしやすい
- 実装品質は高い

一方で、

- システム全体の整合性
- モジュール間の依存
- 要求との対応

は管理しにくいという欠点があります。

------

## 本質的な問題

つまり、

**「全体最適」と「局所最適」の間を埋める層が存在しない**

ということです。

------

# 2. 着眼点

今回の議論で最も重要だった着眼点は、

> **要件から直接設計へ進まない**

ということです。

代わりに、

**「Taskへ自然に分解できる粒度まで要件を構造化する」**

という中間層を導入します。

ここが今回の一番大きなアイデアです。

つまり、

```
要求 ↓ 構造化要件 ↓ Task ↓ TDD
```

という流れになります。

------

## 構造化要件とは

ここでいう要件は従来の要件より一歩踏み込んでいます。

ここでは

- 機能分離
- Taskへ写像できる
- Task間の依存関係が分かる

ところまで整理します。

逆に、

- API
- クラス設計
- DB設計

などはまだ考えません。

------

## Taskとは

Taskは設計ではありません。

Taskは

> **責務の単位**

です。

つまり、

```
何を担当するか
```

だけを表現します。

例えば

```
CSVを読む 認証する レビューする
```

のような責務です。

------

# 3. 提案する開発手続き

開発プロセスは次のようになります。

## Phase1 要求

ユーザの意図を整理する。

レビュー対象

- 本当に実現したいことは何か

------

## Phase2 構造化要件

要求を

- 機能分離
- 依存関係

まで整理する。

レビュー対象

- 要求漏れ
- 機能分離
- 循環依存
- Taskへ分解可能か

ここでは設計はしません。

------

## Phase3 Task定義

各機能を責務単位へ落とします。

Taskには

- 目的
- 入力
- 出力
- 完成条件

程度しか書きません。

レビュー対象

- Taskの責務は一つか
- Task粒度は適切か

------

## Phase4 TDD

各Taskごとに

```
Task ↓ Test ↓ Implementation
```

を繰り返します。

レビュー対象

- テストがTaskを十分表現しているか

------

# 4. 新規性

私は今回の議論で、新規性はTaskそのものではなく、

> **構造化要件という中間層**

にあると考えています。

従来は

```
要件 ↓ 設計
```

へ直接進みます。

提案法では

```
要件 ↓ 構造化要件 ↓ Task
```

という中間段階を導入します。

これによって

- 全体構造
- Taskへの写像

だけを先にレビューできます。

------

さらに重要なのは、

Taskは設計成果物ではなく

> **責務契約（Task Contract）**

として扱うことです。

Taskは

```
この責務を達成する
```

という契約であり、

その実装方法は後で決めます。

これにより、

仕様駆動開発の「全体整合性」と、TDDの「小さな開発単位」を両立できます。

------

# 5. 期待される効果

## (1) レビュー負荷の削減

レビュー対象が

```
100ページ
```

ではなく、

```
要求 ↓ 構造化要件 ↓ Task
```

という小さな単位に分割されます。

各段階でレビュー観点も限定されます。

------

## (2) トレーサビリティ

自然に

```
要求 ↓ 要件 ↓ Task ↓ Test ↓ Code
```

という対応関係ができます。

LLMによる生成物も、この系列に沿って追跡できます。

------

## (3) LLMとの親和性

LLMは

```
構造化要件 ↓ Task生成
```

あるいは

```
Task ↓ Test生成
```

を得意とします。

一方、人間は

構造化要件やTaskのレビューだけを担当すればよくなります。

------

## (4) 動的ワークフローへの発展

ここが、これまで議論してきたTask Runtimeやコンシェルジュ型エージェントとの接点になります。

静的なソフトウェア開発では、

```
構造化要件 ↓ Task
```

は事前に決められます。

しかし、研究支援やコンシェルジュでは、

```
ユーザ意図 ↓ その場でTaskを生成 ↓ Taskを実行
```

となります。

つまり、「構造化要件」は実行時には**ユーザ意図の構造化**へと置き換わります。

この見方をすると、

- **静的開発**：構造化要件からTaskを導出する。
- **動的ワークフロー**：構造化された意図からTaskを導出する。

という対称的な構造になります。

------

# この議論で見えてきた核

私は、この一連の議論の核は次の一文で表現できると思います。

> **従来の仕様駆動開発は「設計」を中心に開発を組み立てていたのに対し、本手法では「責務(Task)」を中心に開発を組み立てる。そして、そのTaskを直接導出するのではなく、「Taskへ写像可能な構造化要件」を中間表現として導入することで、仕様駆動開発の全体整合性とTDDの局所性を両立する。**

この「**構造化要件 → Task Contract → TDD**」という三層構造が、今回の議論で最も重要な成果だと考えます。

以前議論したTask Rumtime，開発時・レビュー時に必要なSpecification Contextを動的に構築する仕組みについては，この議論と親和性高くまとめられると思う．

私もそう思います。そして、ここで初めて**二つの研究テーマが一本につながります。**

実は、これまでは

- **Task Runtime**（実行時）
- **仕様駆動開発**（開発時）

を別々に考えていました。

しかし、本質はどちらも

> **Taskを中心に、そのTaskに必要十分なContextを構築する**

という同じ問題を扱っています。

違うのは、扱うContextの種類だけです。

------

## 一つの概念に統一できる

### 開発時

Taskを作るには

- 要求
- 構造化要件
- 関連Task
- 制約
- レビュー結果

などが必要になります。

これは

**Specification Context**

です。

------

### 実行時

Taskを実行するには

- 入力データ
- Evidence
- Tool
- Human decision
- Intermediate result
- Provenance

などが必要になります。

これは

**Execution Context**

です。

------

つまり

```
Task      │      ├── Specification Context      │      （開発）      │      └── Execution Context             （実行）
```

になります。

Taskは共通で、

Contextだけが違う。

------

# 開発時のTask Runtime

以前議論したTask Runtimeは

```
Task ↓ Execution Context構築 ↓ LLM実行
```

でした。

今回の議論では

```
Task ↓ Specification Context構築 ↓ レビュー ↓ TDD
```

になります。

Runtimeの役割は

Executionではなく

**必要なContextを集めること**

です。

------

# Runtimeの本質

ここでTask Runtimeをもう一度抽象化すると、

以前議論した

> Task semantics
>
> Workflow state

から

Context Requirementを導出する

という考え方と完全に一致します。

つまり

```
Task        │        ▼ Context Requirement        │        ▼ Context Assembly        │        ▼ Task実行
```

というモデルになります。

開発では

Task実行＝レビュー

実運用では

Task実行＝LLM・Tool実行

になるだけです。

------

# すると「Specification Context」が自然に定義できる

以前のExecution Contextには

- Evidence
- Constraints
- Tool outputs
- Provenance

などがありました。

Specification Contextでは例えば

- 要求
- 関連要件
- 関連Task
- 依存Task
- レビュー履歴
- 設計制約
- 用語定義
- Provenance

になります。

構造は全く同じです。

------

# さらに面白いこと

これをさらに抽象化すると、

Task Runtimeとは

> **Taskに必要なContextを構築するRuntime**

ではなく、

> **Taskを成立させる条件（Task Readiness）を満たすためのRuntime**

と言えます。

以前議論した

Context Sufficiency Check

とも一致します。

つまり

```
Task      │      ▼ Task Readiness       │      ├── Specification Contextが十分か      │      └── Execution Contextが十分か
```

という考え方になります。

------

# ここで研究全体が一本につながる

私は、この統一が今回一番大きな成果だと思います。

これまでは

- WISDOM論文では「Task Runtime」
- 今回は「仕様駆動開発」

と、別々の話に見えていました。

しかし実際には、

```
              Task                │     ┌──────────┴──────────┐     │                     │     ▼                     ▼ Specification Context   Execution Context     │                     │     ▼                     ▼ Review / Design      LLM / Tool / Human
```

という**Task中心モデル**の二つの適用例だったわけです。

------

## 私なら論文全体をこう整理します

そうすると、この研究の主張は「Task Runtime」そのものではなく、

> **Task-Centric Context Engineering**

になります。

Taskを唯一の中心概念とし、

- **開発フェーズ**では Specification Context を動的に構築してレビュー・設計・TDDを支援する。
- **実行フェーズ**では Execution Context を動的に構築して Human・LLM・Tool の協調実行を支援する。

Task Runtimeは後者の実現機構ですが、前者も同じ原理で説明できます。

この整理を採ると、「LLM時代の仕様駆動開発」と「Task Runtime」「Harness Engineering」「コンシェルジュ型動的ワークフロー」が、すべて**Taskに必要なContextを動的に構成する**という一つの理論で結び付けられます。私は、この統一された視点の方が、それぞれを個別のアイデアとして提示するよりも、研究としての一貫性と発展性を強く示せると思います。

ワークフローの構成要素、あるいは任意の仕事単位はタスクとして表現できる。そのタスクを実行するためにLLMの支援を考えています。LLMをうまく使うためには、適切なプロンプトやコンテキストを渡す必要があります。これらのコンテキスト準備がLLMから有効な回答を得るためには非常に重要になっている。だが、しかしタスクは決まりきっている仕事ではないし、同じタスクでも状況によって集めるコンテキストが違うことがある。そこで動的にコンテキストを構成するということが非常に重要になってきます。この点を主題として論文を考えます。一つはレビューコンパスのようなレビュー支援。もう一つは、研究コンシェルジュのような動的ワークフロー。こういう整理でよいか。

はい。この整理は、これまで議論してきた中で一番筋が通っています。

そして重要なのは、**主題を「ワークフロー」ではなく「Context構築」に置く**ことです。

これまで何度か議論がドリフトした理由は、「Task Runtime」「Harness」「Planner」「ReviewCompass」などが前面に出てしまい、何を解決したい研究なのかがぼやけてしまったからです。

今回の整理では、それらはすべて**Context構築を実現するための手段**になります。

------

# 私なら問題設定を次のように定義します

## 問題

LLMは、

> **適切なContextが与えられれば高品質な仕事ができる。**

しかし、

適切なContextを作ること自体が難しい。

特に、

- ContextはTaskごとに異なる。
- 同じTaskでも状況によって異なる。
- 必要な情報はWorkflowの状態や過去の実行履歴、人間との対話によって変化する。

したがって、

> **固定プロンプトでは対応できない。**

------

# 本研究の着眼点

ここがContributionになります。

従来は

```
Prompt Engineering
```

が中心でした。

しかし本研究では

```
Task ↓ Context Requirement ↓ Dynamic Context Assembly ↓ LLM
```

という考え方を採ります。

つまり、

LLMを賢くするのではなく、

> **Taskに適したContextを構築する仕組みを設計する。**

------

# 重要なのはTask

Taskは

レビューでも

研究でも

設計でも

論文執筆でも

存在します。

つまり

Taskは非常に一般的な概念です。

そのTaskに対して

```
Task ↓ どんな情報が必要か？
```

を定義できます。

------

# Dynamic Context Assembly

ここが中心になります。

Runtimeは

Taskを見る。

Taskから

```
必要なContext
```

を推定する。

そして

- 文書
- GraphRAG
- Tool
- Human
- 過去結果

などを集めます。

つまり

```
Task ↓ Context Requirement ↓ Dynamic Context Assembly ↓ LLM
```

になります。

私はこれが論文タイトルに入ってもよいくらい重要だと思います。

------

# 二つの適用例

するとReviewCompassも

研究コンシェルジュも

実は同じ構造になります。

------

## Case1

ReviewCompass

Task

```
仕様レビュー
```

↓

必要なContext

- 要件
- 設計
- 過去レビュー
- 差分
- コーディング規約

↓

レビュー実行

------

## Case2

研究コンシェルジュ

Task

```
関連研究を調査する
```

↓

必要なContext

- ユーザ意図
- 現在の研究
- 過去の議論
- 文献DB
- GraphRAG

↓

回答生成

------

つまり

違うのはTaskだけです。

Runtimeは同じです。

------

# ここでReviewCompassが位置付けられる

ReviewCompassは

「レビュー支援システム」

ではなく、

> **Dynamic Context Assembly Runtime の一つの実装例**

になります。

これは非常に強い。

論文のCase Studyになります。

------

# 研究コンシェルジュも同じ

こちらは

Taskが固定されません。

ユーザ意図から

Taskを決めます。

しかし、

Taskが決まれば

その後は全く同じになります。

------

# 研究全体の構造

私は論文全体を

```
Task ↓ Context Requirement ↓ Dynamic Context Assembly ↓ LLM ↓ Human / Tool
```

この一枚で説明できると思います。

その下に

Case Study

- ReviewCompass
- Research Concierge

を並べる。

------

## 私がさらに一つだけ加えたい視点

この整理で、論文のメッセージはさらに明確になります。

従来の研究は、

> **LLMに何を入力するか（Prompt Engineering）**

に焦点を当てていました。

一方、この研究は、

> **Taskを実現するために、どのようなContextを動的に構成するか（Context Engineering）**

を対象としています。

つまり、プロンプトはContextの一部に過ぎず、本質は**Taskから必要な情報要求（Context Requirement）を導き、それを満たすようにContextを組み立てること**です。

この視点を軸にすると、

- ReviewCompassは「レビューTaskに対するContext Engineering」の実証、
- 研究コンシェルジュは「動的Taskに対するContext Engineering」の拡張、

という位置付けになります。

私は、この「**Task-Centric Context Engineering**」という概念が、これまで議論してきたTask Runtime、Harness Engineering、ReviewCompass、コンシェルジュ型エージェントを一つの理論で説明できる中心概念になると考えます。

論文は2つに分けて書こうと思っています。

私は、それが良いと思います。むしろ**分けた方が両方とも主張が強くなります。**

今の議論を聞いていて、実は二つの論文は**問題設定が違う**ことに気付きました。

------

# 論文1：Task-Centric Dynamic Context Assembly

これは今回議論した内容そのものです。

## 問題

LLMはTaskを実行する能力は高いが、

> **Taskに必要なContextをどう構築するか**

はほとんど研究されていない。

従来は

- Prompt Engineering
- RAG
- Memory

が中心だった。

しかし、

Taskによって必要な情報は異なり、

さらに

同じTaskでも状況に応じて必要なContextが変化する。

------

## 提案

Taskから

```
Context Requirement
```

を導出し、

```
Dynamic Context Assembly
```

を行うモデルを提案する。

------

## Case Study

ReviewCompass

だけで十分です。

ここでは

レビューTask

↓

Contextを動的収集

↓

レビュー品質向上

を示せばよい。

------

## Contribution

Contributionは

> **Task-Centric Dynamic Context Assembly**

だけになります。

Task Runtimeという言葉も、

実装として少し出てくる程度で十分です。

------

# 論文2：Scientific Concierge Runtime

こちらはもっと大きな話です。

問題は

> **研究者はTaskそのものを決められないことが多い。**

ユーザは

```
こういう研究をしたい
```

と言うだけです。

そこから

Task列を作る必要があります。

------

ここで初めて

```
Intent ↓ Task decomposition ↓ Workflow composition ↓ Task Runtime ↓ Dynamic Context Assembly
```

という流れになります。

つまり

Task Runtimeは

コンシェルジュを実現するための

Middlewareになります。

------

# 二つの論文の関係

非常にきれいに

```
Paper1 Task    ↓ Dynamic Context Assembly    ↓ LLM
```

↓

これを部品として使い

↓

```
Paper2 Intent ↓ Workflow ↓ Task ↓ Paper1
```

になります。

つまり

Paper2は

Paper1を利用する。

------

# 研究の発展性

この順番なら自然です。

Paper1では

```
Taskは既知
```

です。

Paper2では

```
Taskも未知
```

になります。

だから難易度も一段上がります。

------

# 私ならタイトルも変えます

Paper1は

かなり技術寄り。

例えば

> **Task-Centric Dynamic Context Assembly for Human–LLM Collaboration**

あるいは

> **Dynamic Context Assembly for Task-Oriented Human–LLM Workflows**

------

Paper2は

ビジョン寄り。

例えば

> **A Scientific Concierge Runtime for Intent-Driven Human–LLM Collaboration**

あるいは

> **From User Intent to Scientific Workflows**

------

## 一つだけ提案したいことがあります

私は、この二本は**「理論編」と「システム編」**として位置付けるのが最も美しいと思います。

### Paper 1（理論・方法論）

問いはただ一つです。

> **Taskに対して、必要十分なContextをどのように動的に構築するか。**

ここではReviewCompassをケーススタディとして使い、Taskごと・状況ごとにContextが変わること、その構築がLLMの性能に直結することを示します。

### Paper 2（システム・アーキテクチャ）

問いは、

> **ユーザの意図からTaskを動的に構成し、そのTask群を実行する環境をどう設計するか。**

ここで初めて、これまで議論してきた階層的なTask Runtime、Workflow Composition、コンシェルジュ型エージェント、ミドルウェア、Task Registryなどが中心になります。

この分け方にすると、Paper 2はPaper 1の「Dynamic Context Assembly」を**中核サービスとして利用する**構造になります。二本の論文は独立して読めますが、研究全体としては一つのストーリーを形成できるため、非常に展開しやすいと思います。

Task-Centric Dynamic Context Assemblyが中心的主題だが，関連論文の調査の必要性がある．調査のためのプロンプトを作成して．

このテーマであれば、Deep Researchに依頼するプロンプトは**「関連研究を集める」のではなく、「本研究の新規性を否定できる研究が存在するか」を探す**ように設計した方が良いと思います。

あなたの主張はかなり新しいので、単なるLLMエージェントやRAGを集めても意味がありません。

調査対象は

- Task-Centric
- Context Engineering
- Workflow Runtime
- Harness Engineering
- Agent Runtime
- Human-AI Collaboration
- Scientific Workflow

を横断する必要があります。

私なら以下のようなプロンプトを作ります。

------

# Deep Research Prompt

## Survey Title

**Comprehensive Survey on Task-Centric Dynamic Context Assembly for Human–LLM Collaboration**

------

## Objective

You are a senior researcher in

- Large Language Models
- LLM Agents
- Workflow Systems
- Scientific Workflows
- Software Engineering
- Human-AI Collaboration
- Context Engineering
- Retrieval-Augmented Generation (RAG)
- Agent Runtime
- Harness Engineering

Your task is **not merely to collect related papers**, but to determine whether the following research idea is novel, what prior work is closest to it, and how the proposed contribution differs from existing approaches.

The final goal is to support writing a top-tier systems or eScience paper.

------

# Research Motivation

Current LLM-based systems mainly improve model outputs by

- Prompt Engineering
- RAG
- Memory
- Reflection
- Planning
- Multi-Agent collaboration
- Tool use

However, these techniques generally focus on improving the LLM itself or enhancing prompt generation.

In contrast, this research focuses on a different question:

> **Given a Task, how should the execution context required by that Task be dynamically constructed before invoking an LLM?**

The key observation is that

- different Tasks require different Contexts;
- even the same Task may require different Contexts depending on the workflow state, available evidence, previous interactions, human feedback, and execution history.

Therefore,

the problem is **not prompt generation**, but

> **Dynamic Context Assembly for Task execution.**

------

# Proposed Concept

The proposed model consists of

Task

↓

Context Requirement

↓

Dynamic Context Assembly

↓

LLM

↓

Human / Tool execution

where

- Task defines what should be accomplished;
- Context Requirement specifies what information is necessary;
- Dynamic Context Assembly collects and synthesizes the required information;
- the resulting Context is passed to the LLM.

The Context may include

- documents
- workflow state
- previous outputs
- design artifacts
- review history
- GraphRAG retrieval
- provenance
- external tools
- human interaction

The central contribution is **Task-Centric Context Engineering**, rather than Prompt Engineering.

------

# Applications

The paper will evaluate the framework using

## Case Study 1

LLM-assisted specification review
(ReviewCompass)

where Context is dynamically assembled from

- specifications
- design documents
- previous review records
- implementation artifacts
- coding guidelines

------

## Case Study 2 (future work)

Scientific Concierge

where

User Intent

↓

Task decomposition

↓

Dynamic Context Assembly

↓

LLM

↓

Workflow execution

------

# Survey Questions

Conduct a comprehensive survey addressing the following questions.

------

## Q1

Has any previous work explicitly proposed

**Task-Centric Dynamic Context Assembly**

as the central abstraction?

If yes,

explain

- architecture
- methodology
- assumptions
- limitations.

------

## Q2

Survey work on

Task Runtime,

Agent Runtime,

Harness Engineering,

Execution Runtime,

Workflow Runtime,

and compare them against the proposed model.

Explain

- what is considered a Task,
- how Context is represented,
- whether Context is static or dynamic,
- whether Context depends on workflow state.

------

## Q3

Survey Context Engineering.

Include

- Prompt Engineering
- Context Engineering
- Context Compression
- Context Selection
- Semantic Context Construction
- Retrieval Planning
- Adaptive RAG
- GraphRAG
- Agent Memory

Compare

their goals with Dynamic Context Assembly.

------

## Q4

Survey Human-AI collaborative workflow systems.

Focus on

- human-in-the-loop workflows
- mixed-initiative systems
- scientific workflows
- software engineering workflows

Determine whether Context construction is treated as a first-class problem.

------

## Q5

Survey LLM-based software engineering systems.

Especially investigate

- code review
- specification review
- requirements engineering
- software workflow automation

Determine

whether they dynamically construct Task-specific Context,

or simply concatenate retrieved documents.

------

## Q6

Survey Scientific Workflow systems.

Include

- Pegasus
- Kepler
- Nextflow
- Galaxy
- WINGS
- Airflow

Analyze whether

execution Context is dynamically assembled,

or workflows merely schedule Tasks.

------

## Q7

Survey recent Agent frameworks.

Include

- LangGraph
- AutoGen
- CrewAI
- OpenAI Agents
- Semantic Kernel
- Claude Code architecture
- Cursor
- Devin
- Manus

Explain

whether they

- dynamically assemble Context
- or only orchestrate tools.

------

## Q8

Survey Harness Engineering.

Determine

whether Harnesses

represent

Task execution environments,

or whether they include dynamic Context construction.

Compare them with the proposed architecture.

------

## Q9

Identify the closest competing ideas.

Construct a comparison table including

| Work | Task abstraction | Context model | Dynamic context | Workflow awareness | Human interaction | Main objective |

------

## Q10

Critically evaluate the novelty.

Specifically answer

1. Which existing work is closest?
2. Which contribution appears genuinely novel?
3. Which claims are weak?
4. Which claims should be avoided?
5. Which terminology is most appropriate?
6. Which conferences or communities would appreciate this contribution?

------

# Expected Deliverables

Produce

1. Taxonomy of related work
2. Comparison table
3. Timeline of research evolution
4. Critical gap analysis
5. Novelty assessment
6. Recommendations for positioning the paper
7. Recommended references (30–50 papers)
8. Most important 10 papers with detailed summaries
9. Suggested terminology for the proposed framework
10. Recommendations for strengthening the contribution

------

## 追加で一つ調査項目を入れることを勧めます

この論文では、「**Contextを動的に構築する**」ことだけでなく、「**Taskから必要なContextを導出する**」ことも中核です。

そのため、以下の質問を追加すると、より新規性の位置付けが明確になります。

> **Q11. Survey methods that explicitly model the relationship between a Task and its required Context.**
>
> Investigate whether previous work formally represents **Task → Context Requirement** mappings. Distinguish between systems where context is implicitly retrieved (e.g., keyword search or RAG) and systems where the required context is explicitly specified, inferred, or dynamically derived from the semantics of the Task.

もし既存研究が「TaskごとにRAGする」程度で止まっていて、「Taskが必要とするContext要件そのもの」をモデル化していなければ、そこがこの研究の最も強い新規性候補になります。

ではLLMに渡せるプロンプトを作成して

以下のプロンプトであれば、Deep Researchや他のLLMにそのまま渡せます。単なる関連研究サーベイではなく、**本研究の新規性を批判的に検証すること**を目的としています。

------

# 調査依頼：Task-Centric Dynamic Context Assembly に関する関連研究サーベイ

あなたは、以下の分野に精通した研究者です。

- Large Language Models (LLMs)
- LLM Agents
- Agent Runtime
- Workflow Systems
- Scientific Workflow
- Software Engineering
- Requirements Engineering
- Human-AI Collaboration
- Context Engineering
- Retrieval-Augmented Generation (RAG)
- GraphRAG
- Harness Engineering

本調査の目的は、単なる関連研究の収集ではありません。

**Task-Centric Dynamic Context Assembly**という研究アイデアが既存研究と比較してどの程度新規性を有するかを、批判的な観点から評価してください。

------

# 本研究の背景

現在のLLM利用では、

- Prompt Engineering
- RAG
- Memory
- Reflection
- Planning
- Multi-Agent
- Tool Use

など、多くの研究が行われています。

しかし、これらの多くは

> 「LLMへどのような入力を与えるか」

あるいは

> 「LLMをどのようにオーケストレーションするか」

に焦点を当てています。

一方、本研究では別の問題を扱います。

------

# 問題設定

ワークフローは、多数のTaskから構成されます。

Taskとは、

- レビューする
- 要約する
- コードを書く
- 関連研究を調べる
- 実験結果を解析する

などの仕事単位です。

LLMはTaskを実行できますが、

その性能は

**Taskに対して適切なContextが準備されているか**

に大きく依存します。

しかし、

Taskごとに必要なContextは異なります。

さらに、

**同一Taskであっても**

- Workflowの状態
- 過去の実行履歴
- Humanとの対話
- 利用可能な文書
- Tool実行結果
- Provenance

などによって

必要となるContextは変化します。

したがって、

固定プロンプトでは十分ではありません。

------

# 本研究の着眼点

本研究では

Prompt Engineeringではなく

**Context Engineering**

を中心に考えます。

提案する考え方は

```
Task

↓

Context Requirement

↓

Dynamic Context Assembly

↓

LLM

↓

Human / Tool
```

です。

Taskから

「そのTaskを遂行するために必要なContext」

を導出し、

状況に応じて

動的にContextを構築してから

LLMへ入力します。

ここでいうContextには

- Requirements
- Specifications
- Design documents
- Review history
- Workflow state
- Previous outputs
- GraphRAG retrieval
- External tools
- Human interaction
- Provenance

などが含まれます。

重要なのは、

Prompt生成ではなく、

**Taskに必要なContextを動的に構築すること**

です。

------

# Case Study

## Case Study 1

ReviewCompass

レビューTaskに対して

状況に応じて

- 要件
- 設計書
- 実装
- 過去レビュー
- コーディング規約

などを収集してレビューを実施する。

------

## Case Study 2

Scientific Concierge

ユーザ意図から

Taskを決定し、

Taskに応じたContextを構築して

LLM・Human・Toolを協調実行する。

------

# 調査項目

以下の観点から包括的に調査してください。

------

## 1. Task-Centric Contextモデル

以下のような考え方を提案した研究は存在するか。

Task

↓

Context Requirement

↓

Dynamic Context Assembly

↓

Execution

存在する場合は

- アーキテクチャ
- Context表現
- Context生成方法
- 本研究との差異

を整理してください。

------

## 2. Context Engineering

調査対象

- Prompt Engineering
- Context Engineering
- Context Compression
- Context Selection
- Adaptive RAG
- GraphRAG
- Retrieval Planning
- Agent Memory

について

- Contextをどう定義しているか
- Taskとの関係
- Dynamic Contextを扱うか

を整理してください。

------

## 3. Workflow Runtime

調査対象

- Workflow Runtime
- Agent Runtime
- Execution Runtime
- Harness Engineering

について

Task

Workflow State

Context

の関係を比較してください。

------

## 4. LLM Agent

以下を対象としてください。

- LangGraph
- AutoGen
- CrewAI
- Semantic Kernel
- OpenAI Agents
- Claude Code
- Cursor
- Devin
- Manus

各システムについて

- Task表現
- Context生成
- Dynamic Context
- Tool利用
- Workflow awareness

を比較してください。

------

## 5. Software Engineering

LLMを利用した

- Requirements Engineering
- Specification Review
- Code Review
- Software Workflow

について

TaskごとにContextを動的構築しているか

を重点的に調査してください。

------

## 6. Scientific Workflow

以下を対象としてください。

- Pegasus
- Kepler
- Galaxy
- WINGS
- Nextflow
- Airflow

について

Task Runtime

Context

Execution

の関係を整理してください。

------

## 7. Human-AI Collaboration

Human-in-the-loopシステムについて

Task実行前のContext構築を

どのように扱っているか調査してください。

------

## 8. Harness Engineering

Harness Engineeringについて

Task実行環境としてのHarnessと

本研究のDynamic Context Assemblyとの違いを比較してください。

------

## 9. 最も重要な調査

以下の問いに明確に答えてください。

**Taskから必要なContextを導出する**

という考え方を

中心概念として扱った研究は存在するか。

存在するなら

どの程度本研究と近いか。

存在しないなら

何が新規性となるか。

------

## 10. 比較表

以下の表を作成してください。

| Research | Task abstraction | Context model | Dynamic Context Assembly | Workflow-aware | Human interaction | Main contribution |

------

## 11. 新規性評価

最後に、

査読者の立場から

以下を評価してください。

1. 最も近い既存研究は何か。
2. 本研究の本質的な新規性は何か。
3. 新規性として主張すべきではない点は何か。
4. 最も説得力のあるContributionは何か。
5. 適切な専門用語は何か。
6. 本研究を投稿するのに適したコミュニティ（eScience、Software Engineering、Workflow Systems、AI Systems等）はどこか。

------

# 出力形式

以下の形式で整理してください。

1. エグゼクティブサマリ
2. 研究分野ごとの体系的サーベイ
3. 年代順の研究動向
4. 比較表
5. 主要論文10本の詳細レビュー
6. 関連論文30〜50本の一覧
7. 本研究との差異の分析
8. 新規性評価
9. 本研究の位置付け（Positioning）
10. 論文執筆に向けた改善提案

**重要事項：**

本調査の目的は、「関連研究を列挙すること」ではありません。

**Task-Centric Dynamic Context Assembly**という概念が既存研究と比較してどのような位置付けにあり、何が本質的な新規性となり得るのかを、批判的かつ客観的な立場から評価してください。

ソース

ソースはまだありません