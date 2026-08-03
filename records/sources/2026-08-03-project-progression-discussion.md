---
source_id: SRC-PROJECT-PROGRESSION-DISCUSSION-001
captured_at: 2026-08-03
source_kind: user-provided-project-progression-discussion
normative_status: source-evidence
confidentiality_class: project-internal
raw_snapshot_retained: false
source_reconstructability: digest-only
---

# プロジェクト進行検討から採用する知見

## 1. 目的と位置付け

過去に検討したコンシェルジュ型Task Runtimeのプロジェクト進行案から、ReviewCompass3の
Task Contract中心設計に必要な知見だけを抽出し、現行概念へ読み替える。本書は出典と採否判断を
保持するEvidenceであり、Intent、Requirementsまたは計画の正本ではない。

元資料はReviewCompass3より広い製品を想定している。このため、元のcomponent構成やroadmapを
そのまま移植せず、ReviewCompass3の代表的な開発経路を検証する方法として利用する。

## 2. 固定source

- source：`/Users/keno/LLMsession/プロジェクト進行.md`
- SHA-256：`9a5c4fa66c3fd1637ec6e08be40d8c9cbb153908d0d74b622207a652bbfbbc98`
- 行数：793
- source内の出典表示：なし

元資料の全文はrepositoryへ複製しない。本書は上記identityで観測したsourceからの要約と、
2026-08-03時点のReviewCompass3への適合判断だけを保持する。元ファイルを失った場合は本書から
全文を再構築できない。

## 3. 採用する知見

### 3.1 代表シナリオからの縦断検証

個別Requirementの被覆だけでなく、利用者の要求から受入までの経路を代表シナリオで通す。
ReviewCompass3では、少なくとも次を確認対象とする。

1. `new_development / fresh`：RequirementからTask Contract、TDD、review、Human判断、受入へ進む。
2. `maintenance / reopen`：既存成果と先行Evidenceを引き継ぎ、変更影響とstaleを処理する。
3. 上流改定と問題対応：実装中の不整合を分類し、必要な最下位上流層を改定して再開する。
4. 依存、循環、中止：依存追加、cycle、pause、cancel、close-scopeをEvidence付きで処理する。
5. 配置とlifecycle：別root、project移動、update、migration、rollback後もidentityとProvenanceを保つ。
6. 条件付き並行：独立なlow-risk Work Itemだけを並行化し、integration checkpointで再検証する。

この一覧を新しいFeature、開発lane、Runtime schemaまたは独立gateにしない。Design、Acceptance Test、
E2E fixture、Evaluationを同じ利用経路へ接続する確認軸として使う。最初は一つのvertical sliceを
端から端まで成立させ、他のシナリオは必要なnegative pathまたは後続Workで追加する。

### 3.2 シナリオ被覆の確認観点

各代表シナリオについて、次が途中で切れずに接続されるかを確認する。

- IntentとRequirementの対象範囲
- Task Contractの責任、境界、依存と受入条件
- Context ObligationsとCapability／permission
- Humanの判断点、authority、escalation
- Run、state、pause、resume、retry、terminationと復旧
- Test、Verdict、Provenance、Decision、accepted artifact
- security、再現性、配置、resource budget

この確認はRequirement coverageを置き換えない。原子的要件が全件割り当てられていても、一つの
利用経路として実行不能な欠落を検出する補助表とする。表自体を製品artifactとして先行実装せず、
Work 4の設計確認とWork 8のEvaluation材料から始める。

### 3.3 Task Contractの粒度

Task Contractを分けるのは、次を満たす境界がある場合とする。

- 一つの説明可能な責任とaccountable ownerを持つ。
- 独立して観測可能なExpected OutputとAcceptance Criteriaを持つ。
- 必要な場合にretry、checkpoint、terminationまたはHuman escalationの単位になる。
- side effectとその所有範囲が明確である。
- 再利用、依存管理またはProvenance追跡のために独立identityを持つ価値がある。

独立して受理、復旧または追跡できない内部手順は、Contractを増やすためだけに分割しない。
逆に、異なるauthority、risk、lifecycle、side effectまたはfailure recoveryを一つのContractへ
埋め込まない。文書、調査、試作には形式的TDDやretry可能性を一律に要求せず、Contract typeに
適した観測可能な受入と停止条件を使う。

### 3.4 部分side effectからの回復

長時間処理または外部side effectを持つContractでは、単なるretryだけでは部分成功を安全に扱えない。
適用されるContractまたはPolicyは、次を明確にする。

- timeoutまたはdeadline
- cancellation可能範囲
- idempotency identityと重複検出
- compensation、または外部状態と期待状態を照合して修復するreconciliation
- 自動回復できない操作とHuman escalation

すべてのContractへ汎用job controlを実装しない。外部または回復を要するside effectがscopeへ入った
時点で必要なPlan、Test、Provenanceを有効にする。不可逆操作は補償可能と仮定せず、事前Human gateと
影響制限を優先する。

### 3.5 自己適用後の外部project検証

ReviewCompass3自身のvertical sliceと`local_integrated` E2Eが成立した後、異なるsoftware repository
一件で、Repository Binding、impact slice、maintenance／reopen、配置独立性、Provenance移植性を
検証する。これは汎用middleware化や別domain applicationの開発ではなく、自己開発固有の仮定を
検出するportability pilotである。

初期vertical sliceをblockせず、自己適用から得た固定interfaceと観測項目が揃った後の条件付きWorkと
する。検証結果から共通責務を確認し、二つ目の対象を支援するためだけの抽象化は追加しない。

## 4. 条件付きで後続へ送る知見

元資料はRequester、Contributor、Reviewer、Decision Maker、Approver、AdministratorなどのHuman roleを
分けている。現行Intentの主対象は一人の開発者であるため、初期実装ではHuman Interaction Planの
論理的な判断classとauthorityで区別し、一人が複数roleを担えるようにする。複数利用者のRBAC、
assignment、Administratorは`shared_runtime`の具体的必要性とthreat modelが得られた後に検討する。

## 5. 既に現行計画へ反映されている知見

- Human、AI、決定論的validator／Toolの役割分担
- 最小vertical sliceから開始する開発順
- Context、Capability、permission、security境界
- Provenance、Decision Record、評価、失敗Evidence
- pause、cancel、retry、checkpoint、crash再開、idempotency
- local profileを先行し、shared／distributedを実測後へ送る配置方針
- cost、resource budget、version、negative path、失敗事例の観測
- 高度な意味検索を初期実装の前提にしない方針

これらは本資料を理由に重複したFeature、Requirement、componentまたはWorkとして追加しない。

## 6. 採用しない知見

- ReviewCompass3を汎用ConciergeまたはGoal／Workflow Managerへ拡張すること
- 任意Taskを登録・検索・合成する汎用Task Registry
- Task plugin platformと無検査の動的load
- 論文作成、研究調査、実験支援など別domain applicationの同時開発
- Model Gateway、Runtime Server、GraphRAGを独立componentまたは必須roadmapにすること
- modular monolith、microservice、monorepoなどの物理構成を実測前に固定すること

これらは現行Intentの非目標または過剰実装境界と競合する。将来必要性が生じても、本資料だけを
根拠に復活させず、IntentまたはRequirementsの明示的な改定から始める。

## 7. 現行計画へ渡す最小差分

現行計画へは次だけを渡す。

1. Work 4で代表シナリオと端から端の被覆を設計確認軸にする。
2. Definition ChallengeへTask Contract粒度の判断基準を加える。
3. 外部side effectがある場合のcompensation／reconciliation義務をContractまたはPolicyへ置く。
4. 自己適用E2E後の外部software project一件によるportability pilotをDeferred Workへ置く。

詳細な採否理由とシナリオ一覧は本書を参照し、現行計画へ元資料の広いcomponent構成を転記しない。
