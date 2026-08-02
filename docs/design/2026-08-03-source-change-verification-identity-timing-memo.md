---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
related_assessment: 2026-08-03-large-complex-software-design-assessment.md
related_parallel_memo: 2026-08-03-parallel-work-introduction-timing-memo.md
related_plan: ../current/reviewcompass3-plan-current.md
---

# Source・変更集合・Verification identityの導入時期に関する検討メモ

## 1. 背景

[大規模・複雑なソフトウェア開発を前提とした設計評価](2026-08-03-large-complex-software-design-assessment.md)
において、Git、CI、変更集合の識別が現行計画では十分に明示されていないと評価した。

ReviewCompass3は固定source tree、Context identity、stale、Test Evidence、commit、Project Bindingを
既に扱う。また、並行作業modelでは固定source identityとconflict domainを安全条件にする。しかし、
Test、review、判断、統合、releaseが実際にどのsource内容を対象としたかを共通のidentityで結ばなければ、
古いEvidenceの再利用、別commitに対するCI結果の採用、並行変更の競合見逃しが発生する。

この問題を解決するため、Git固有の操作機能ではなく、SCM非依存のsource、変更集合、Verification、
artifact identityを設計する。初期adapterはlocal Gitのread-only取得に限定し、CI製品連携とGit hosting
操作は必要性を確認してから段階導入する。

## 2. 必要性

### 2.1 Testとreviewの対象を確定する

commit SHAだけでは、実際にTestまたはreviewした内容を常に表せない。commit後の変更、stage済み変更、
untracked file、別worktree、未commitの文書変更を含む場合があるためである。

ReviewCompass3は、commitとは別に、対象となった内容全体のmanifestとDigestを持つSource Snapshotを
必要とする。Test、review、Decision RecordはこのSnapshotへ束縛し、実行後に内容が変われば旧Evidenceを
staleにする。

### 2.2 Evidenceの誤再利用を防ぐ

次の場合、過去のgreenまたはreview合格をそのまま利用してはならない。

- base commitまたはdependencyが変わった。
- Test後にsourceが変更された。
- snapshotへ含めるべきuntracked fileが除外された。
- merge結果がTest対象と異なる。
- CIがaccepted対象とは別のcommitを検証した。
- tool、workflowまたは実行環境の意味が変わった。

Source Snapshot、Change Set、Verification Runを分離し、各Evidenceがどのidentityに対して有効かを
明示する必要がある。

### 2.3 並行作業の安全性を保証する

`bounded_parallel`では、各Work Itemのbase、変更対象、実変更、作業領域、統合結果を識別しなければ
conflict domainを計算できない。したがって、Source SnapshotとChange Setの識別は実並行Pilotの
前提条件である。

branch名は移動可能な参照であり、固定identityとして扱わない。固定commit、作業treeのcontent
manifest、Change Set、merge結果をそれぞれ識別する。

### 2.4 CI結果を正しい成果へ結ぶ

CI Runはprovider上の表示名またはgreen表示だけで採用しない。workflow version、Run、Attempt、
source、Test selection、environment、raw result、artifactを結ぶ必要がある。retryまたはrerunも旧結果を
上書きせず別Attemptとして保持する。

CIをacceptance oracleとして使わないprojectでは、CI adapterを初期releaseの必須能力にしない。

### 2.5 release artifactを再構成する

releaseまたはdeployment時には、次を再構成できる必要がある。

```text
Requirement
  → Task Contract
  → Change Set
  → Source Snapshot
  → Verification Run
  → Build Artifact
  → Release
```

この連鎖はrollback、再現可能性、将来のAs-Built projectionにも必要になる。

## 3. 論理identity

次は論理的に分けるが、独立serviceまたは独立Runtime componentを意味しない。一つのrecord bundleの
sectionとして実装できる。

### 3.1 Repository Binding

ReviewCompass3 projectとrepository、checkoutまたはworktreeの対応を表す。

- `project_id`
- `repository_id`
- `binding_id`
- SCM kind
- repository root
- checkoutまたはworktree

### 3.2 Source Snapshot

review、Test、実装判断が対象とした内容全体を表す。

- base commitとHEAD
- indexの状態
- tracked change
- 対象となるuntracked file
- content manifestとDigest
- dependency lock identity
- capture時刻

snapshot対象外にしたfileがある場合は、除外規則と理由を記録する。dirtyな作業treeをcleanとみなさない。

### 3.3 Change Set

固定baseからcandidateまでの意味のある変更集合を表す。

- base Snapshotとcandidate Snapshot
- add、modify、delete、rename
- 変更fileとsymbol
- Work ItemとTask Contract
- change semantics
- merge、split、supersedes関係

### 3.4 Verification Run

local TestとCI Testを共通に扱う。

- provider：`local | ci`
- RunとAttempt
- Source Snapshot
- Test selection
- commandまたはworkflow identity
- environment identity
- result、raw output、Evidence Digest

### 3.5 Build Artifact

deploymentまたはrelease対象を表す。

- artifact identityとcontent Digest
- Source Snapshot
- build Runとtoolchain
- target platform
- Verification結果
- promotionとrollback関係

## 4. 責務配置

新Featureを追加せず、既存ownerへ次のように割り当てる。

- Project Binding：repository、checkout、worktreeとの対応
- Context Runtime：review対象Source Snapshotの採否とContext identity
- Workflow：Change SetとWork Item、base変更、merge、staleの進行制御
- Harness：local command、CI Run、Attempt、raw capture
- Semantic Trace：Snapshot、Change Set、Test、Decision、commit、artifact間の関係
- Portable Lifecycle：Build Artifact、promotion、update、rollback

Git adapterはidentityを取得するが、Contract、accepted state、Decisionを所有しない。CI adapterも外部結果を
取得・検証するだけで、green表示をReviewCompass3のacceptanceへ直接変換しない。

## 5. 段階的な導入順序

```text
Work 1・1A
  repository、固定commit、checkout、dirty状態をbaselineへ記録
  ↓
Work 3
  Source Snapshot、Change Set、Verification、staleの義務をRequirements化
  ↓
Work 4
  SCM非依存identity、owner、relation、保存、staleを設計
  ↓
Work 4A
  Source Symbol Indexを固定Source Snapshotへ束縛
  ↓
Work 5A・6A
  read-only local Git取得とnegative fixture
  ↓
Work 7A
  identityの保存、復元、checkout移動、複数checkoutをE2E検証
  ↓
必要な場合のみCI取込みPilot
  ↓
Work 8A前
  branch、worktree、Change Set、merge結果の識別を完成
  ↓
Work 7B
  Build Artifact、promotion、rollbackを検証
```

### 5.1 Work 1・Work 1A

製品機能を作らず、既存Evidenceのrepository、固定commit、checkout、dirty状態と、Git管理対象・
project外dataの境界を記録する。

### 5.2 Work 3・Work 4

Work 3でsource、変更集合、Verificationの識別義務とstale条件を定める。Work 4ではSCM非依存の
record、owner、relationを設計する。GitHub、GitLab、特定CI providerをRequirementへ固定しない。

この設計はWork 4Aより前に必要である。Source Symbol IndexとReusable Routine Ledgerがどのsource
内容を対象としたかを確定するためである。

### 5.3 Work 5A・Work 6A

最初のvertical sliceではread-only local Git取得だけを実装する。

- repository、HEAD、base commit
- tracked changeとindex状態
- 対象untracked file
- content manifest
- Change Set Digest

次をnegative fixtureにする。

- Test後にsourceが変わった。
- TestまたはCI結果が別commitを対象にしている。
- 対象untracked fileをsnapshotから落とした。
- baseが移動した。
- dirty workspaceをcleanとして記録した。
- result commitとaccepted Change Setが一致しない。

### 5.4 Work 7A後のCI取込みPilot

local E2Eとdurable stateが成立した後、実対象projectがCIを使う場合だけ実施する。最初はCIを起動・
制御せず、既存Runのworkflow identity、Run、Attempt、source、Test結果、artifact Digestをread-onlyで
取り込む。

CI結果をReviewCompass3のacceptanceへ利用する場合は、対象sourceとの一致、raw capture、validation、
stale、retryを別Task Contractで確認する。

### 5.5 Work 8A前

実並行Pilotを行う場合は、Work Itemごとのbase Snapshot、worktreeまたは隔離作業領域、Change Set、
merge結果、統合後Snapshot、base変更後のstaleを識別できなければならない。CI連携自体は、local
Verificationが受入条件を満たす場合には必須ではない。

### 5.6 Work 7B

update、migration、rollbackの対象となるBuild Artifactを、source、build Run、Verification、target
platformへ束縛する。artifactのpromotionとrollbackはこの段階で扱う。

## 6. 過剰設計を避ける境界

初期実装ではSCMまたはCIの管理製品を作らない。

- SCM非依存のidentityとrelationは設計する。
- adapterはread-only local Git一種類から始める。
- CIは既存結果の取込みから始める。
- push、pull request作成、自動merge、merge queueを実装しない。
- GitHub、GitLab、CI providerごとの管理UIを作らない。
- branch名を耐久identityまたはauthorityにしない。
- Git操作の自動化とEvidence識別を分離する。
- 論理recordを独立componentまたはserviceへ分割しない。

特定provider連携、SCMへのwrite、CI起動、PR／merge管理は、実対象projectで必要性が確認され、権限、
failure、retry、外部side effect、rollbackを別Task Contractで定義した後に扱う。

## 7. 結論

Source SnapshotとChange Setの識別は、最初のImplementation Task ContractとWork 4Aの台帳baselineより
前に設計し、最初のvertical sliceではread-only local Git取得として最小実装する。branch、worktree、
merge結果の識別は`bounded_parallel`実並行Pilotより前に完成させる。

CI adapterはlocal deployment E2E後、CIを利用する実対象projectに限って導入し、Build Artifact identityは
release lifecycleを扱うWork 7Bで導入する。この順序により、Evidenceの対象を早期に固定しながら、
Git hosting、CI制御、PR管理を初期範囲へ持ち込まない。
