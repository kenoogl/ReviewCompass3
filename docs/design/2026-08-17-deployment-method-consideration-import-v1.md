# デプロイ方法の検討（repo外検討メモの取り込み） v1

- 取り込み日：2026-08-17
- 取り込み者：Claude（利用者指示「案2で進める。メモ取り込み→事前走査→論点整理の提示まで」）
- 出自：`/Users/keno/LLMsession/RC3/デプロイ方法の検討.md`（利用者と外部LLMの検討記録。
  原文SHA-256 `fa48a9a74cee52b19167c714c61b57bd69ae7af697b4de586c0533f1d2edcb91`・31,966 bytes）
- 性格：**時点検討の記録**（作成から時間が経過しており、現実体と乖離がありうる——利用者申告）。
  デプロイ方針再検討（2026-08-17開始の作業単位）の固定入力。正本のRC3概念は
  `docs/concepts/2026-07-27-task-runtime-concept.md`
- 以下は原文のverbatim転記（無改変）

---


デプロイ方法を検討しておく必要がある

そうですね。今回のミドルウェアは、単体アプリとして配布するのか、複数の研究支援アプリから共通利用する基盤として運用するのかで、設計がかなり変わります。現時点では、**「ローカル実行を基本としつつ、将来はサーバ型へ移行できる構成」**にしておくのがよいと思います。

## 基本方針

まずは、次の3層に分けて考えると整理しやすいです。

```
研究者向けアプリケーション  ├─ ReviewCompass  ├─ 論文作成支援  ├─ 実験・解析支援  └─ 研究コンシェルジュ          ↓ Task Runtime Middleware  ├─ Workflow Runtime  ├─ Task State Manager  ├─ Context Builder  ├─ Tool / MCP Gateway  ├─ Human Interaction  ├─ Provenance / Event Log  └─ Policy / Model Router          ↓ 外部サービス・計算資源  ├─ LLM API / Local LLM  ├─ MCP Server  ├─ GraphRAG / Vector DB  ├─ Git / File System  ├─ HPC / Job Scheduler  └─ External APIs
```

重要なのは、アプリケーションからミドルウェアを直接ライブラリ呼び出しするだけでなく、**API経由でも利用できるようにすること**です。

## 推奨するデプロイ形態

### 1. 初期段階：ローカル単体型

最初は、研究者のPCまたは開発マシン上で、すべてをDocker Composeで起動します。

```
Developer PC  ├─ Application  ├─ Task Runtime API  ├─ Runtime Worker  ├─ PostgreSQL  ├─ Object / File Storage  └─ MCP Servers
```

これは現在のReviewCompassのような自己適用・開発検証に向いています。

利点は、開発が簡単で、ファイルシステム、Git、ローカルLLM、MCPツールへのアクセスが容易なことです。研究データを外部に出さずに済む点も大きいです。

ただし、アプリケーションとRuntimeを同一プロセスに埋め込むのではなく、最低限、

```
Application → HTTP API → Task Runtime
```

という境界は設けておいた方がよいです。

### 2. 研究室内運用：共有サーバ型

次の段階では、研究室内サーバにRuntimeの中核を置きます。

```
研究者PC  └─ Web UI / Desktop Client          ↓ Lab Server  ├─ API Gateway  ├─ Task Runtime  ├─ Worker Pool  ├─ PostgreSQL  ├─ Artifact Storage  ├─ GraphRAG  └─ Local LLM Server          ↓ HPC / GPU Server / External API
```

この形では、ワークフロー定義、実行履歴、レビュー記録、provenanceを共有できます。

一方で、各研究者のローカルファイルやGitリポジトリにアクセスする必要があります。そのため、中央サーバだけで完結させるのではなく、研究者PC側に小さな実行エージェントを置く構成が有効です。

```
Central Runtime      ↓ task request Local Execution Agent  ├─ Local files  ├─ Git  ├─ Local commands  └─ Local MCP servers
```

中央Runtimeが判断し、実際のローカル操作はLocal Agentが行います。これは、研究コンシェルジュ用途ではかなり重要になると思います。

### 3. 将来形：分散・ハイブリッド型

将来的には、Task RuntimeをControl PlaneとExecution Planeに分けるのが自然です。

```
Control Plane  ├─ Workflow definitions  ├─ Task state  ├─ Scheduling  ├─ Context requirements  ├─ Policy  └─ Provenance index Execution Plane  ├─ LLM Worker  ├─ Local Tool Agent  ├─ HPC Agent  ├─ GraphRAG Worker  └─ External Service Worker
```

Control Planeは「何を、どの状態で、どこに実行させるか」を管理し、Execution Planeが実作業を担当します。

これはHarness Engineeringの観点とも整合します。LLM自体を中央に置くのではなく、LLM、ツール、人間、データ、評価器を取り巻く実行環境をControl Planeが統制する形です。

## コンテナの分割単位

初期実装では、細かくマイクロサービス化しすぎない方がよいです。まずは以下の5コンポーネント程度で十分です。

```
1. runtime-api   ワークフロー受付、状態取得、Human応答受付 2. runtime-worker   Task実行、Context構築、LLM呼び出し、ツール実行 3. runtime-db   Workflow、Task、状態、イベント、provenance 4. artifact-store   入出力ファイル、プロンプト、LLM応答、レビュー結果 5. tool-gateway   MCP、ローカルコマンド、外部API、HPCへの接続
```

GraphRAGは最初からRuntime本体へ埋め込まず、外部Context Providerとして接続するのがよいです。

```
Context Builder  ├─ File Context Provider  ├─ Git Context Provider  ├─ Review History Provider  ├─ GraphRAG Provider  └─ Human Query Provider
```

これなら、GraphRAGが未実装でもRuntime開発を進められます。

## データ保存の考え方

最低限、以下を分けて保存する必要があります。

| 種類                | 保存先                     |
| ------------------- | -------------------------- |
| Workflow定義        | GitまたはDB                |
| 現在状態            | PostgreSQL                 |
| Task実行履歴        | PostgreSQL                 |
| イベントログ        | PostgreSQLまたは追記型ログ |
| プロンプト・LLM応答 | Artifact Store             |
| 入出力成果物        | ファイル/Object Storage    |
| provenance関係      | DB、将来はGraph DBも可     |
| 秘密情報            | Secret Store / 環境変数    |

特に重要なのは、成果物そのものと、その成果物を生成した履歴を分離することです。

```
Artifact  ├─ content  ├─ version  ├─ producer task  ├─ source artifacts  ├─ prompt  ├─ model  ├─ tool invocation  └─ human decisions
```

この構造があれば、後からGraphRAGや意味論的provenanceへ発展させられます。

## 配布方法

利用者の種類ごとに、入口を分けるのがよいでしょう。

開発者向けには、

```
docker compose up
```

で一式起動できる形にします。

アプリケーション開発者向けには、REST APIまたはPython SDKを提供します。

```
runtime.start_workflow(    workflow="post_write_review",    inputs={"target": "paper.tex"} )
```

一般の研究者向けには、Web UI、デスクトップアプリ、またはChat UIを提供します。

つまり、配布物は一つではなく、

```
Runtime Server Python SDK CLI Web UI Local Agent Workflow Packages
```

に分かれます。

## まず決めるべきデプロイ上の責務境界

今の段階で、特に次の点は仕様化しておいた方がよいです。

### Runtimeが保持するもの

- WorkflowとTaskの状態
- 実行履歴
- Context要求
- Human問い合わせの状態
- Tool実行要求
- provenance
- 再実行・中断・再開情報

### Workerが保持しないもの

Workerは原則ステートレスにします。処理中に障害が起きても、DBとArtifact Storeから再開できるようにします。

### アプリケーションが保持するもの

- 画面
- ドメイン固有のワークフロー
- ドメイン固有のレビュー観点
- ドメイン固有のContext Provider
- 利用者向けの説明

## 現実的な開発順序

デプロイを考慮すると、次の順序がよいです。

1. 単一マシン上でRuntime APIとWorkerを分離する
2. PostgreSQLによるTask状態永続化を実装する
3. Artifactとprovenanceの保存形式を決める
4. Docker Composeで再現可能な実行環境を作る
5. ReviewCompassを最初のクライアントとして接続する
6. Local Agentを追加し、ローカルファイル操作を分離する
7. 共有サーバへ配置する
8. GraphRAG、HPC、複数Workerを追加する
9. Kubernetes等への対応を検討する

Kubernetesは最初から導入する必要はありません。まずDocker Composeで責務境界を固め、Workerの水平追加が必要になった段階で移行すれば十分です。

## 推奨する当面の形

当面は、次の構成が最もバランスがよいと思います。

```
Docker Compose  ├─ Task Runtime API  ├─ Task Worker  ├─ PostgreSQL  ├─ Artifact Storage  └─ MCP / Tool Gateway Host OS  ├─ Git repositories  ├─ Research files  ├─ Local LLM  └─ Local tools
```

その上で、Runtime API、Worker、Context Provider、Tool Adapterを明確に分けます。

これにより、現在はローカルPC上で動かしながら、将来はほぼ同じ設計のまま、

```
ローカル型 → 研究室サーバ型 → 分散ハイブリッド型
```

へ移行できます。

デプロイ方法は後処理ではなく、**Task Runtimeにおける状態の所在、実行権限、データ境界、障害回復を決める設計問題**として、ミドルウェア設計と並行して詰めるべきです。

ミドルウェアとその上で動くレビューアプリという構成の場合，ミドルウェアをデプロイし，それを使ってレビューアプリを作成，あｓらにそのレビューアプリをデプロイして，コーディングするという構造になるかも

はい、その理解でほぼ合っています。ただし、素直に実装すると、

```
ミドルウェアを開発 → ミドルウェアをデプロイ → レビューアプリを開発 → レビューアプリをデプロイ → レビューアプリを使ってコーディング
```

という多段構造になり、開発時の更新がかなり重くなります。

したがって、**論理構造と物理的なデプロイ構造を分けて考える**のがよいです。

## 論理的には三層構造

```
対象プロジェクト  └─ コード・仕様・設計文書          ↑ レビューアプリ  ├─ レビュー用ワークフロー  ├─ レビュー観点  ├─ UI / CLI  └─ ReviewCompass固有機能          ↑ ワークフローミドルウェア  ├─ Task Runtime  ├─ Context Builder  ├─ Human Interaction  ├─ Tool Execution  ├─ Provenance  └─ Workflow State
```

この意味では、

1. ミドルウェアを構築する
2. ミドルウェア上にレビューアプリを構築する
3. レビューアプリを用いて対象プロジェクトを開発・レビューする

という関係です。

これは正しいです。

ただし、毎回それぞれを独立したサーバにデプロイする必要はありません。

## 開発初期は一体的に起動する

現実的には、ミドルウェアとレビューアプリを一つの開発環境として起動します。

```
docker compose up  ├─ middleware-api  ├─ middleware-worker  ├─ review-app  ├─ database  └─ artifact-store
```

レビューアプリは内部でミドルウェアAPIを使います。

```
Developer   ↓ Review App   ↓ Middleware API   ↓ LLM / MCP / Git / Files / Tests
```

つまり、論理的には別製品ですが、開発時には一括して起動できます。

この形であれば、

```
ミドルウェア変更 → コンテナ再ビルド → レビューアプリから即利用
```

となり、毎回本番デプロイする必要はありません。

## 問題は「何をレビューするのか」

レビューアプリ自身を開発するときには、少し循環構造が生じます。

```
Middleware    ↓ Review App    ↓ Review App自身のコードをレビュー
```

これは自己適用です。

さらに、ミドルウェアのコードもレビューアプリでレビューするなら、

```
Middleware    ↓ Review App    ↓ Middlewareのコードをレビュー
```

という構造になります。

論理的には循環していますが、実行時には問題ありません。すでに動作している安定版を使って、次の版をレビューすればよいからです。

```
Middleware v1 + Review App v1             ↓ Middleware v2を開発・レビュー             ↓ Review App v2を開発・レビュー
```

これはコンパイラが新しいコンパイラをコンパイルするブートストラップに近い構造です。

## 安定版と開発版を分ける

重要なのは、現在使用中の環境と、開発中の環境を分けることです。

```
Stable Environment  ├─ Middleware v1  └─ Review App v1          ↓ Development Environment  ├─ Middleware v2 source  └─ Review App v2 source
```

Stable版のレビューアプリを使って、Development版をレビューします。

開発版をそのまま自分自身のレビューに使うと、バグがレビュー結果にも影響するため危険です。

そのため、少なくとも次の2系統を持つのが安全です。

```
stable development
```

あるいは、

```
production staging
```

です。

## ミドルウェアの提供形態

ミドルウェアは、単なるサーバだけでなく、次の組み合わせにすると使いやすくなります。

```
Middleware Server  実行状態、Workflow、Context、provenanceを管理 Middleware SDK  レビューアプリから簡単に呼び出す Workflow Definition Package  Taskや状態遷移を記述する CLI  開発・テスト・運用に使う
```

レビューアプリ側では、例えば次のように利用します。

```
review = runtime.start(    workflow="post_write_verification",    inputs={        "repository": repository_path,        "target_files": changed_files,    }, )
```

ミドルウェアの内部実装をレビューアプリが直接参照するのではなく、APIまたはSDKを通す形です。

## レビューアプリの位置づけ

レビューアプリは、単なる画面ではありません。

ミドルウェア上に載るドメインアプリケーションとして、以下を持ちます。

```
Review Application  ├─ レビューWorkflow定義  ├─ レビューTask定義  ├─ Context Provider  ├─ レビュー観点  ├─ モデル選択方針  ├─ 判定・エスカレーション規則  ├─ Git連携  └─ UI / CLI
```

一方、以下はミドルウェア側です。

```
Middleware  ├─ Taskの開始・停止・再開  ├─ 状態管理  ├─ Contextの収集機構  ├─ LLM呼び出し  ├─ Tool実行  ├─ Human問い合わせ  ├─ Artifact保存  └─ Provenance記録
```

この境界を保てば、同じミドルウェア上に別のアプリも載せられます。

```
Middleware  ├─ Review Application  ├─ Paper Writing Application  ├─ Experiment Application  └─ Research Concierge
```

## 実際のコーディング時の構造

対象プロジェクトをコーディングするときは、次のようになります。

```
IDE / Coding Agent      ↓ コード変更      ↓ Review App      ↓ Middleware      ├─ 仕様取得      ├─ 設計文書取得      ├─ Git差分取得      ├─ テスト実行      ├─ LLMレビュー      └─ Human問い合わせ      ↓ レビュー結果      ↓ コード修正
```

レビューアプリは、IDEと並んで使う外部ツールでもよいですし、将来的にはIDE拡張やCoding Agentに統合してもよいでしょう。

## 最初から完全分離しすぎない

初期段階で、

```
Middleware専用サーバ Review App専用サーバ Local Agent Gateway Workflow Registry Context Service
```

まで全部分けると、実装とデバッグが重くなります。

当面はモノレポまたは近接したリポジトリ構成が現実的です。

```
platform/  ├─ middleware/  ├─ sdk/  ├─ review-app/  ├─ workflows/  ├─ adapters/  └─ docker-compose.yml
```

デプロイ単位は分けても、開発環境は一括管理できます。

## 推奨する段階構成

### 第1段階

```
単一リポジトリ 単一docker-compose ミドルウェアとレビューアプリは別プロセス
```

API境界は作るが、デプロイは一括です。

### 第2段階

```
ミドルウェアを共通サーバ化 レビューアプリを独立配布
```

別のアプリケーションからもミドルウェアを利用できるようにします。

### 第3段階

```
中央Middleware 複数Application 複数Local Execution Agent
```

研究室内や複数利用者向けの構成です。

## まとめると

おそらく想定される構造は、次のようになります。

```
ミドルウェアを作る      ↓ ミドルウェア上にレビューアプリを作る      ↓ レビューアプリを使って対象システムを開発する
```

ただし、運用上は、

```
ミドルウェアを毎回本番デプロイ → レビューアプリを毎回本番デプロイ → ようやくコーディング
```

とはしません。

実際には、

```
安定版Middleware + 安定版Review App                 ↓        次版のコードをレビュー
```

というブートストラップ構造にし、開発中はDocker Composeなどで一括起動するのがよいです。

この観点からは、最初に作るべき成果物は、ミドルウェア単体よりも、**最小ミドルウェアと最小レビューアプリを一緒に動かす縦切りの実装**です。ミドルウェアを完成させてからレビューアプリに進むより、レビューという具体的ユースケースを通して責務境界を確定する方が、設計を外しにくいと思います。

デプロイを再考する．15スレッドの議論を通過し，コンシェルジュ的な動作をすることを考えた．予め決まったワークフローもあれば，小さなタスクを動的に組み立てたワークフローも視野にはいる．このような使い方を考えると，小さなタスクを任意に登録でき，それらのタスクを自在に使えるようにする必要がある．このようなシステムでは，ミドルウェアをデプロイし，その上（中？）に小さなタスクを追加していくイメージか？

はい。その理解がかなり近いです。ただし、表現としては、**「ミドルウェアの中にタスクを実装して追加する」よりも、「デプロイされたミドルウェアに、独立したTask Packageを登録して利用可能にする」**と捉える方がよいと思います。

つまり、構造は次のようになります。

```
Task Runtime Platform ├─ Runtime Core ├─ Task Registry ├─ Workflow Registry ├─ Context / Tool / Human Interaction基盤 └─ Execution Workers        ↑        │ 登録・配布        │ Task Packages ├─ 文献検索Task ├─ Git差分取得Task ├─ コードレビューTask ├─ テスト実行Task ├─ 論文構成提案Task ├─ 人間への確認Task └─ 成果物保存Task
```

## ミドルウェアは「タスク実行プラットフォーム」になる

従来のイメージは、

```
Middleware    ↓ Review Application    ↓ Coding
```

でした。

しかし、コンシェルジュ型まで視野に入れると、より適切なのは次の構造です。

```
ユーザの意図    ↓ Concierge / Orchestrator    ↓ Task Runtime    ↓ Task Registryから必要なTaskを選択    ↓ Taskを組み合わせて実行
```

ここで、レビューアプリはミドルウェアの上に載る完全に独立した大きなアプリケーションというよりも、次の組み合わせになります。

```
Review Application = Review用UI・対話 + Review Workflow群 + Review用Task群 + Review用ポリシー
```

Task Runtimeは、それらを実行する共通基盤です。

## 予め決まったWorkflowと動的Workflow

両者は同じRuntime上で扱えます。

### 定型Workflow

例えば、現在のReviewCompassに近いものです。

```
変更検出  ↓ 関連仕様の収集  ↓ レビューコンテキスト構築  ↓ 複数モデルによるレビュー  ↓ トリアージ  ↓ 人間による承認  ↓ 結果保存
```

Workflow定義そのものが登録されています。

```
workflow: post-write-verification steps:  - detect_changes  - collect_related_specs  - build_review_context  - run_review  - triage_findings  - request_human_approval  - store_results
```

一方、コンシェルジュ型では、利用者の要求に応じてRuntimeがTaskを組み立てます。

```
「この変更が仕様と整合しているか確認し、 問題があれば修正案も作って」
```

という要求に対して、

```
intent理解   ↓ Task Registry検索   ↓ 必要Taskの選択   ↓ 依存関係を考慮した組み立て   ↓ 実行
```

となります。

例えば動的に、

```
Git差分取得  ↓ 関連仕様検索  ↓ 整合性レビュー  ↓ 問題箇所抽出  ↓ 修正案生成  ↓ 人間への確認
```

という一時的なWorkflowを構築します。

## Taskはミドルウェアの「中」か「上」か

ここは責務境界として重要です。

結論としては、

> Taskの実行機構はミドルウェアの中にあるが、個別Taskの定義・実装はミドルウェアの外から登録する。

という構造がよいです。

```
Middleware Core ├─ Taskのロード ├─ 入出力検証 ├─ 状態管理 ├─ Context構築 ├─ Tool呼び出し ├─ Human問い合わせ ├─ 再試行・中断・再開 └─ Provenance記録 Task Package ├─ Taskの目的 ├─ 入力・出力スキーマ ├─ 必要Context ├─ 実行ロジック ├─ 使用可能Tool ├─ 成功条件 └─ エラー・エスカレーション条件
```

個別Taskをミドルウェアのソースコードへ直接追加する設計にすると、Taskを一つ追加するたびにミドルウェア本体の再ビルドや再デプロイが必要になります。

それでは、自在にTaskを追加するという目的に合いません。

## Task Packageという単位

各Taskは、プラグインあるいはパッケージとして配布するのがよいでしょう。

例えば、

```
tasks/ ├─ git-diff/ │   ├─ task.yaml │   ├─ handler.py │   └─ schemas/ ├─ requirements-retrieval/ │   ├─ task.yaml │   ├─ handler.py │   └─ prompts/ └─ semantic-review/    ├─ task.yaml    ├─ handler.py    ├─ prompts/    └─ policies/
```

Taskのメタデータは、例えば次のように表現できます。

```
name: semantic-requirements-review version: 1.2.0 description: >  コードまたは設計変更が関連要件と整合しているかを検証する inputs:  target_artifact:    type: artifact  change_set:    type: git_diff outputs:  findings:    type: review_findings context_requirements:  - related_requirements  - related_design  - previous_review_findings capabilities:  - llm  - repository_read  - graph_retrieval human_interaction:  allowed: true success_criteria:  - all_changed_components_are_reviewed  - findings_have_evidence
```

Runtimeはこの記述を読み、Taskを利用可能にします。

## Taskの実装方式は一つに限定しない

小さなTaskには、性質の異なるものがあります。

```
Task ├─ Python関数 ├─ CLIコマンド ├─ REST API ├─ MCP Tool ├─ LLM Prompt ├─ Human Interaction ├─ 別Workflow └─ HPC Job
```

したがって、Task Runtimeは「すべてのTaskを同じプロセスで動かす」のではなく、共通のTaskインターフェースを提供するべきです。

```
Task Runtime    ↓ Task Adapter ├─ Python Adapter ├─ Container Adapter ├─ MCP Adapter ├─ REST Adapter ├─ LLM Adapter ├─ Human Adapter └─ Workflow Adapter
```

これにより、例えば「文献検索Task」は外部API、「テスト実行Task」はローカルコンテナ、「レビューTask」はLLM、「承認Task」は人間との対話として実装できます。

## デプロイ後のTask追加

理想的な運用は次のようになります。

```
1. Runtime Platformをデプロイ 2. Task Packageを作成 3. Task Registryへ登録 4. RuntimeがTaskを検証 5. Taskを有効化 6. 定型Workflowまたは動的Workflowから利用
```

例えばCLIでは、

```
runtime task install ./tasks/semantic-review runtime task validate semantic-review runtime task enable semantic-review
```

あるいはコンテナとして、

```
runtime task register \  --name test-runner \  --image reviewcompass/test-runner:1.0
```

のような形です。

Task登録だけで済むなら、Runtime Coreそのものを再デプロイする必要はありません。

## Task Registryが重要になる

このシステムでは、単にTask一覧を保存するだけでは不十分です。

コンシェルジュがTaskを選択するためには、Task Registryが次の情報を持つ必要があります。

| 情報          | 用途                       |
| ------------- | -------------------------- |
| Taskの目的    | 何ができるか               |
| 入力型        | 何を与えれば動くか         |
| 出力型        | 何が生成されるか           |
| 前提条件      | いつ実行可能か             |
| 必要Context   | 何を収集すべきか           |
| 使用Tool      | 権限・実行場所の決定       |
| コスト・時間  | 実行計画の選択             |
| 信頼度        | Task選択・再検証           |
| 副作用        | ファイル更新やメール送信等 |
| Human承認要否 | 安全な実行                 |
| provenance    | バージョンと実行根拠       |

つまりTask Registryは、単なる関数カタログではなく、**Taskの意味と実行条件を記述した能力カタログ**になります。

この意味情報がないと、コンシェルジュは「どのTaskを、なぜ、どの順番で使うか」を判断できません。

## Workflowも登録可能なTaskとして扱える

TaskとWorkflowを完全に別物にしない方が、構成しやすくなります。

例えば、

```
atomic task  Git差分を取得する composite task  変更後レビューを実行する
```

とし、複合Taskの内部にWorkflowを持たせます。

```
Task ├─ Atomic Task └─ Composite Task      └─ Sub-workflow
```

そうすると、従来考えていた具体的なTask Runtimeは、コンシェルジュから見ると再利用可能なComposite Taskになります。

例えば、

```
Concierge Runtime  ↓ 「変更後レビュー」Composite Task  ↓ Review Task Runtime / Sub-workflow  ├─ Context収集  ├─ Human問い合わせ  ├─ Tool実行  └─ LLMレビュー
```

これは、15スレッドで議論した抽象度の拡張とよく対応します。

## レビューアプリの再定義

この構造では、レビューアプリは単独の巨大なアプリというより、レビュー領域のTask群とWorkflow群を提供する**ドメインパッケージ**として整理できます。

```
Review Domain Package ├─ Review Tasks │   ├─ change_detection │   ├─ context_collection │   ├─ requirements_alignment_review │   ├─ design_review │   ├─ code_review │   └─ finding_triage ├─ Review Workflows │   ├─ post_write_verification │   ├─ pre_merge_review │   └─ specification_review ├─ Review Policies ├─ Review Prompts ├─ Review Context Providers └─ Review UI
```

UIを除けば、これらはRuntimeに登録されるTask・Workflow・Policyの集合です。

したがって、

```
ミドルウェアをデプロイ ↓ レビューアプリを別サーバとしてデプロイ
```

だけが唯一の構成ではありません。

次の構成も可能です。

```
Task Runtime Platform ├─ Review Domain Package ├─ Paper Writing Domain Package ├─ Experiment Domain Package └─ Literature Survey Domain Package
```

ユーザは同じコンシェルジュを通して、それらを横断的に使えます。

## 推奨する全体像

```
┌─────────────────────────────────────────────┐ │ User Interface / Concierge                  │ │ 意図理解・対話・実行計画・結果説明          │ └─────────────────────┬───────────────────────┘                      │ ┌─────────────────────▼───────────────────────┐ │ Task Runtime Control Plane                  │ │ 状態管理・計画・権限・Context・Provenance   │ └───────────┬──────────────────┬──────────────┘            │                  │ ┌───────────▼──────────┐  ┌────▼─────────────┐ │ Task / Workflow      │  │ Execution Plane  │ │ Registry             │  │ Worker / Agent   │ │                      │  │                  │ │ Atomic Tasks         │  │ Local            │ │ Composite Tasks      │  │ Container        │ │ Fixed Workflows      │  │ MCP              │ │ Policies             │  │ LLM / HPC        │ └───────────▲──────────┘  └──────────────────┘            │ ┌───────────┴─────────────────────────────────┐ │ Domain Packages                             │ │ Review / Writing / Experiment / Survey ... │ └─────────────────────────────────────────────┘
```

## デプロイ単位として整理すると

最終的には、少なくとも次の4種類があります。

### 1. Runtime Platform

長期間動作する共通基盤です。

```
API Task State Registry Scheduler Context Manager Provenance Policy
```

### 2. Task Worker

Taskを実際に実行する環境です。中央サーバ、ローカルPC、GPUサーバ、HPCなどに配置します。

### 3. Task / Domain Package

後から追加・更新できる機能群です。Runtime本体とは別にバージョン管理・配布します。

### 4. Client / Concierge UI

ユーザが要求を入力し、進行状況を確認し、人間判断を返す入口です。

したがって、イメージとしては、

> ミドルウェアを一度デプロイし、その中にTaskをハードコードして増築する

ではなく、

> Task Runtime Platformをデプロイし、そこへTask PackageおよびWorkflow Packageを継続的に登録・更新する

が適切です。

そしてレビューアプリは、**レビュー用Task Package群・Workflow群・UIをまとめた最初のドメインアプリケーション**になります。

この構造にすれば、ReviewCompassから始めながら、後に論文作成、文献調査、実験実行などのTaskを追加し、コンシェルジュがそれらを横断的に組み合わせる形へ自然に発展できます。

ソース

ソースはまだありません