---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
related_assessment: 2026-08-03-large-complex-software-design-assessment.md
related_plan: ../current/reviewcompass3-plan-current.md
---

# 非機能要件とVerification Profileの接続に関する検討メモ

## 1. 背景

[大規模・複雑なソフトウェア開発を前提とした設計評価](2026-08-03-large-complex-software-design-assessment.md)
において、性能、規模上限、信頼性、費用、互換性、security・privacy、maintainabilityなどの
非機能要件を、RequirementまたはArchitecture PolicyからVerification Profileへ接続する必要があると
評価した。

Task Contractごとの機能Testがすべてgreenでも、処理に長時間を要する、保存量が増え続ける、障害から
復旧できない、既存dataを壊す、機密情報を漏らすなど、製品として受け入れられない状態は発生する。
このため、「機能が正しく動くこと」と「実際に使用でき、安全に運用できること」を分けて検証する。

## 2. 三層の役割

### 2.1 Requirement

利用者または外部から見て、何を満たさなければならないかを定める。

例は次のとおりである。

- 指定規模のprojectで影響範囲計算を許容時間内に完了する。
- worker停止後にside effectを重複させず再開できる。
- support対象の旧versionからdataを移行できる。
- raw sessionを通常data領域へ保存しない。

Requirementは入力、出力だけでなく、停止、復旧、保存、受入、対象外をatomic obligationとして持つ。
数値、対象規模、support範囲が製品またはproject固有の外部義務である場合はRequirementへ置く。

### 2.2 Architecture Policy

複数のRequirementまたはTask Contractへ共通する制約を定める。

例は次のとおりである。

- sensitive dataは許可したroot以外へ保存しない。
- authority stateの更新は原子的かつdurableに行う。
- 外部送信には対象、送信先、permissionの確認を必要とする。
- Indexと意味graphは増分更新可能な境界を持つ。
- Test結果は固定Source Snapshotへ束縛する。

横断制約を各Task Contractへ複製すると、版、閾値、例外、適用範囲がContractごとにずれる。このため、
共通制約は版付きArchitecture Policyへ置き、Task Contractは適用するPolicy identityを参照する。

### 2.3 Verification Profile

RequirementまたはArchitecture Policyの義務を、実際に確認できる方法へ変換する。

```yaml
source_obligation: NFR-PERF-001
applicable_profile: local_integrated
workload:
  symbol_count: 100000
metric: elapsed_seconds
threshold: 30
environment: reference_local_machine
samples: 5
failure_verdict: performance_requirement_failed
evidence:
  - workload_digest
  - environment_identity
  - raw_measurements
  - summary
```

Verification Profileは新しい要求を発明しない。上流義務をworkload、fixture、環境、測定値、閾値、
判定、Evidenceへ変換する。Profileだけに合格基準を書き、RequirementまたはPolicyに由来しない基準を
事実上の製品要求にしない。

## 3. 接続が必要な理由

### 3.1 非機能要件の宣言だけを防ぐ

「高速であること」「安全であること」と記述しても、測定方法と合格基準がなければ受入判断には
使えない。上流義務とVerification Profileを接続し、少なくとも次を確定する必要がある。

- どのRequirementまたはPolicy ruleを検証するか
- 何を、どの条件で測定するか
- どの閾値またはinvariantをoracleにするか
- 失敗時に何を停止し、どのVerdictを出すか
- どのEvidenceを保存するか
- いつ再検証が必要になるか

対応するProfileを生成できない必須義務は、Compilerが`not_compilable`として開始を拒否できる必要がある。

### 3.2 Testが独自の正本になることを防ぐ

Testに書かれた閾値だけを基準にすると、Testが上流Requirementを置き換える。Requirementが30秒以内を
要求し、Testが60秒以内を合格としている場合、そのTestがgreenでもRequirementは未達である。

authorityは次の順にする。

```text
Requirement / Architecture Policy
  → Task Contract obligation
  → Verification Profile
  → Test / measurement
  → Evidence
  → Verdict
```

上流義務の意味が変わる場合はRequirementまたはPolicyの新versionへ戻る。実装またはTestの都合で
Profileの閾値だけを弱めない。

### 3.3 Task Contractの局所最適を防ぐ

Task Contract方式では仕事を小さく分けてTDDを行うが、非機能要件は複数Contractを横断する場合が
多い。各Contractの処理時間が個別には許容範囲でも、全体の合計が製品Requirementを超えることがある。

```text
Context取得       5秒
意味graph計算    20秒
review実行       40秒
Provenance保存   10秒
────────────────
全体             75秒
```

全体Requirementが60秒以内であれば、各局所Testがgreenでも製品は不合格である。個別Task Contractでは
割当budgetと局所invariantを検証し、Stage FまたはRelease Evaluationではend-to-endの品質属性を検証する。

### 3.4 risk-based verificationを具体化する

low、medium、highのrisk分類だけでは、性能Testのworkload、compatibility matrix、failure injection、
privacy検査の内容は決まらない。品質属性をVerification Profileへ接続し、変更の意味とriskに応じて
実行する検証を具体化する。

例は次のとおりである。

- performance変更：代表規模のbenchmark
- storage変更：容量増加、quota、retention、cleanup
- state変更：crash recovery、retry、idempotency
- migration変更：旧version fixtureからの移行とrollback
- external send変更：送信先、permission、機微情報検査
- shared routine変更：dependency境界、重複候補、利用箇所

### 3.5 条件変更時にEvidenceをstaleにする

非機能Testの結果はsourceだけでなく、環境、workload、tool、policyにも依存する。

- support対象OSが変わった。
- 最大project規模が増えた。
- model、Tool、workflowが変わった。
- retention期間が変わった。
- threat modelが変わった。
- token単価または費用上限が変わった。

Requirement、Policy、Verification Profile、RunをidentityとDigestで結ぶことで、条件変更時に影響を受ける
EvidenceとVerdictをstaleにできる。接続がなければ、古い環境または古い安全条件で得た合格結果を
利用し続ける可能性がある。

### 3.6 観測値と合格基準を区別する

lead time、token、Tool、費用、storage量を観測しても、許容基準がなければ合否は決まらない。

```text
Evaluation Observation: 一回のreviewで50万tokenを使用した
Requirement:             一Work Item当たり10万token以下
Verification Verdict:    requirement failed
```

Evaluation Observationは事実を保存し、RequirementまたはPolicyは許容範囲を定め、Verification Profileが
比較方法を定める。評価metricが存在するだけで品質義務を満たしたと扱わない。

## 4. 品質属性ごとの必要性

| 品質属性 | 機能Testだけでは分からない問題 | Verification例 |
|---|---|---|
| 性能 | 結果は正しいが遅すぎる | latency、throughput、影響計算時間 |
| 規模上限 | 小さいfixtureでは動くが実projectで破綻する | symbol数、Contract数、Provenance量別Test |
| 信頼性 | 通常実行は成功するが障害後に壊れる | crash、retry、途中停止、重複side effect |
| 費用 | 高性能だがtoken・storage費用が無制限になる | token、Tool、保存量、外部service費用 |
| 互換性 | 新規環境では動くが既存dataを壊す | platform matrix、旧schema、migration、rollback |
| security・privacy | 機能は動くが過剰権限または情報漏洩がある | permission、external send、retention、伏字化 |
| maintainability | 現時点では動くが重複、循環、密結合が増える | dependency境界、重複候補、台帳、変更影響 |

maintainabilityは単一metricで自動合否にしない。dependency invariant、重複、循環、public boundaryなど
機械判定できる項目と、Design DecisionおよびHuman reviewを組み合わせる。複雑度の数値だけを目的化しない。

## 5. ReviewCompass3の初期範囲

### 5.1 初期から必要な品質義務

`local_integrated`の最初のsliceに直接関係する次を優先する。

- crash後の再開とside effect重複防止
- sensitive data、外部送信、permission、retention
- support対象platform
- migrationとrollback
- review payload、token、実行時間、保存量の観測
- Source SnapshotとEvidenceの一致
- component state ownershipと再利用方針

安全性、data保護、復旧のinvariantは初期から合否を持つ。一方、性能、規模、費用は、根拠のある閾値が
未確定なら、まず観測と欠測検出を行う。

### 5.2 実測後に基準を決める項目

次は測定方法とEvidenceを先に用意し、Work 8のPilotでbaselineを得てからHumanが許容範囲を決める。

- 最大project規模
- 最大symbol数
- 許容latency
- tokenと費用上限
- Provenance保存量
- 同時Work Item数
- CI待ち時間

根拠のない数値を初期Requirementへ固定しない。baseline測定値をそのまま許容上限にせず、利用目的、
運用余裕、失敗時の影響、改善費用を考慮して判断する。

### 5.3 後続範囲

次は`shared_runtime`または`distributed_hybrid`を導入する場合の後続Requirementとする。

- shared runtimeのavailability
- tenant間の性能とdata分離
- distributed workerのscaleと重複実行
- 高負荷時の自動scale
- 複数地域の可用性

初期`local_integrated`の暗黙要件またはrelease blockerにしない。

## 6. 最小構造

新Featureまたは新componentを追加せず、既存のRequirement、Architecture Policy、Compiler、Verification、
Provenanceへ次の情報を持たせる。

```text
Requirement / Architecture Policy
  ├─ quality attribute
  ├─ applicability
  ├─ expected threshold or invariant
  └─ failure consequence
        ↓
Verification Profile
  ├─ workload / fixture
  ├─ environment
  ├─ measurement
  ├─ threshold / oracle
  ├─ sampling and tolerance
  ├─ failure verdict
  └─ required Evidence
        ↓
Verification Run
        ↓
Evidence + Verdict
```

複数Contractへ同じProfile全文を複製せず、版付きProfileを参照する。すべての品質属性について全環境と
全規模の組合せを作らず、deployment profile、risk、変更影響に応じた代表fixtureとrelease checkpointを
選ぶ。適用外の場合も暗黙に省略せず、対象外理由を記録する。

## 7. 結論

Requirementは「何を満たすか」、Architecture Policyは「複数Contractで共通して守る制約」、
Verification Profileは「どの条件で、どのように確認するか」を担当する。三者を接続することで、
非機能要件を宣言だけでなく、Task Contractの開始、完了、統合、release判断に実際に作用する義務にできる。

初期開発では安全性、data保護、復旧、compatibilityの必須invariantを優先し、性能、規模、費用は測定方法を
先に確立して実測後に閾値を決める。sharedまたはdistributed環境固有のavailabilityとscaleを初期範囲へ
入れず、既存ownerと版付きProfileを使って過剰設計を避ける。
