# デプロイ構成検討の参照記録

## 1. 目的

過去に議論したTask Runtime、review application、Task Package、ローカル・共有server・hybrid
配置、stable／development分離を、Task Contract中心のReviewCompass3へ適合させるための固定
参照として記録する。元文書は対話形式の検討資料であり、全提案を承認済み設計として扱わない。

## 2. 固定source

- source：`/Users/keno/LLMsession/デプロイ方法の検討.md`
- SHA-256：`fa48a9a74cee52b19167c714c61b57bd69ae7af697b4de586c0533f1d2edcb91`
- 行数：692
- source内の出典表示：なし

主な検討範囲は、local／shared／hybridの段階、APIとWorker、data保存、配布単位、stable版による
自己開発、Task Package、Registry、定型・動的Workflow、Control Plane／Execution Planeである。

## 3. 採用する内容

- 論理component境界と物理deployment topologyを分ける。
- 最初はlocal profileで小さく動かし、shared runtimeとdistributed hybridは実測後に進める。
- 制御、durable state、Policy、ProvenanceをControl Plane責務、実作業をExecution Plane責務とする。
- WorkerまたはExecution Agentはauthorityを持つ状態をローカル一時領域だけに保持せず、再起動後に
  durable checkpointとProvenanceから再開できるようにする。
- shared runtimeがlocal file、Git、commandへ無制限にアクセスせず、Local Execution Agentと
  version付きpermissionを介する。
- stable deploymentを使ってdevelopment candidateをreviewし、未検証candidateを自分自身の
  合否判定に使わない。
- Runtime、integration client、execution adapter、project側Contract／Policyを別の配布・更新単位と
  して識別する。
- Project側のTask ContractとPortfolioはRuntime codeの再deployなしに追加・更新できる。

## 4. 修正して採用する内容

| 元の案 | ReviewCompass3での適合 |
|---|---|
| Middleware APIとReview App | Task Contract Control／Workflow／HarnessとCLI・IDE integrationの論理interfaceとして定義し、初期process分割は固定しない |
| Task Registry | Task Contract PortfolioとProject Manifestを定義登録先とし、実行codeの無検査動的loadは許可しない |
| Task Package | project側のContract／Policy／Prompt等と、installed code側の検証済みCapability Adapterを分離する |
| Review Domain Package | 初期ReviewCompass3 profileとして扱い、汎用domain package platformにはしない |
| Dynamic Workflow | accepted ContractとPortfolioからcompileできる範囲に限定し、任意agent orchestrationへ拡張しない |
| Runtime Worker | Harnessed ExecutionのExecution Planeとして扱い、state ownerとしない |
| Local Agent | shared profileでのみ導入する最小権限Execution Agentとし、初期local profileへ先行実装しない |
| Docker Compose | local profileを再現する候補implementationとし、product requirementにはしない |

## 5. 採用しない内容

- PostgreSQL、Object Storage、GraphRAG、Docker、Kubernetesを必須技術に固定すること。
- 任意Task、任意plugin、任意domain applicationを無検査で登録・実行する汎用Runtime。
- ConciergeがTaskを自由生成し、Requirements、Contract、Policyのauthorityを迂回すること。
- 初期releaseでshared server、worker pool、HPC、複数tenantを実装すること。
- Runtime Coreの更新とproject側Contract更新を同じlifecycleまたは同じidentityで扱うこと。

## 6. 初期範囲と後続範囲

初期範囲は`local_integrated` profileとする。同一machine、単一利用者、最小vertical sliceでよいが、
code、project、runtime data、sensitive dataを分け、論理Control／Execution境界、structured I/O、
crash再開、stable／development分離を検証する。

`shared_runtime`はlocal profileの実測後、Local Execution Agent、remote boundary、認証、通信障害、
offline、permission、data localityのRequirementsとthreat modelを別Task Contractで定義してから
着手する。`distributed_hybrid`は複数worker、scheduler、HPC、scaleの必要性が実測された後に
検討する。

## 7. 制約

この記録はsourceと適合判断のEvidenceであり、Requirementsまたは設計の正本ではない。採用事項は
現行Requirements差分、設計改定、統合計画、用語集へ反映して初めて現行候補となる。
