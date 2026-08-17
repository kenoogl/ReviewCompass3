> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
related_assessment: 2026-08-03-large-complex-software-design-assessment.md
related_design: 2026-08-02-task-contract-design-amendment.md
related_plan: ../current/reviewcompass3-plan-current.md
---

# Task Contract設計の過剰実装を避ける境界に関するメモ

## 1. 目的

ReviewCompass3の大規模適用評価で、次の4点は必要な責務を持つ一方、意味上の区別をそのまま独立文書、
独立component、独立state machine、毎回のHuman作業へ変換すると過剰になると判断した。

1. 6種類のPlan
2. Definition Challenge、Conformance、Final Challenge
3. Source Symbol IndexとReusable Routine Ledger
4. Operational Provenance

本メモは、各概念を削除せずに、何を維持し、何を統合し、どの条件で初めて物理分離を認めるかを
固定する。共通原則は次である。

> 意味上の責務は分離するが、保存・実行・確認の単位は、独立したauthority、lifecycle、security、
> scale上の根拠がない限り統合する。

## 2. 6種類のPlan

### 2.1 維持する理由

Task Contractから導出する六つのPlan観点は、それぞれ別の欠落を検出する。

- Context Acquisition：必要な材料、選択、freshness
- Review / Execution：実施内容と成果
- Harness and Capability：Tool、permission、実行条件
- Verification：Test、oracle、failure verdict
- Provenance Capture：保存すべきEvidenceと関係
- Human Interaction：Human判断とescalation

例えばVerificationが定義されても、Context Acquisitionが不足すれば正しい材料でTestできない。
六つの観点とobligation coverageは維持する。

### 2.2 過剰になる条件

次の実装は避ける。

- 六つを独立ファイルとして毎回生成・保存する。
- 各Planに独立したversion、approval、lifecycle、state machineを持たせる。
- 利用者が導出Planを手作業で編集する。
- 共通fieldを各Planへ複製する。
- Plan間整合性を全組合せのpoint-to-point検査として実装する。
- 六つを別serviceまたは別databaseへ先行分割する。

Contract数に比例して管理artifactとreview差分が6倍になり、同じrisk、source、permissionが複数Planで
不一致になる。Plan管理がTask Contractの実施より大きな作業になる場合、設計目的を損なう。

### 2.3 推奨する形

Task Contractと固定Policyをauthorityとし、一つのimmutable Plan bundleに六つのtyped viewを持たせる。

```text
Plan Bundle
  ├─ context
  ├─ execution
  ├─ harness
  ├─ verification
  ├─ provenance
  └─ human_interaction
```

- bundle全体に一つのidentity、version、Digest、compile verdictを持たせる。
- 六つのviewは安定したkeyで参照できるが、独立したapprovalとlifecycleを持たない。
- 共通情報はbundle共通部へ一度だけ保存する。
- consumerには必要なviewだけを決定的にprojectionする。
- 利用者はTask ContractまたはPolicyを変更し、導出viewを直接編集しない。
- 共通の中間modelから全viewを生成し、pairwiseな整合性protocolを作らない。
- 不要なviewを別artifactとしてmaterializeせず、空または既定値もbundle内で表す。

### 2.4 物理分離を認める条件

次のいずれかが実測された場合に限り、特定viewの独立保存またはprocess分離を検討する。

- ownerと更新周期が異なる。
- securityまたはpermission境界が異なる。
- retentionが異なる。
- 独立したretry、failure recoveryが必要である。
- scale上、同一processまたはstoreでは要求を満たせない。

分離してもTask Contractからの導出関係、bundle identity、coverageを失わない。

## 3. Challengeとgate

### 3.1 維持する理由

三つのVerdictは異なる問いを扱う。

- Definition Challenge：Task Contract自体が上位Requirement、Policy、隣接Contractに照らして妥当か
- Conformance：成果がTask ContractのExpected OutputとAcceptance Criteriaへ適合するか
- Final Challenge：Contract適合でもIntent、Requirement、全体品質を損なっていないか

誤ったContractへ完全適合した成果はConformanceだけでは検出できないため、三つのVerdict identityと
failure routeは分離する。

### 3.2 過剰になる条件

次の実行方法は避ける。

- low riskの小変更でも三つを別Run、複数model、複数roundで実行する。
- 各state transitionで全Challengeを再実行する。
- 三つへ同じ材料と質問を渡し、重複Findingを個別処理する。
- 全変更へ同じHuman gateを要求する。
- staleの影響外であるVerdictまで一律に再実行する。

review費用、待ち時間、重複Finding、誤停止が増え、利用者が重要なFindingを識別しにくくなる。

### 3.3 推奨する形

Verdictの意味とReview Run数を分離する。一つのRunが複数の型付きVerdictを生成しても、Verdict identity、
基準、failure routeは混ぜない。

- low risk：deterministic validatorを優先し、一つのRunから必要な三Verdictを生成できる。
- medium risk：DefinitionはContract version確定時に実行し、ConformanceとFinal Challengeは影響に応じて
  独立させる。
- high risk：三Verdictに加え、必要な実行主体、代表data、fault injection、Human gateも独立させる。

実行時期は次を既定とする。

- Definition Challenge：Contract versionごと
- Conformance：成果候補または成果versionごと
- Final Challenge：accept前、または上位・隣接影響が変わったとき
- stale後の再実行：影響を受けたVerdictだけ

共有材料、deterministic validation、Finding候補は一度生成して再利用し、同じFindingをVerdictごとに
複製しない。再利用したEvidenceと各Verdictの独立した判断をProvenanceで区別する。

### 3.4 実行分離を認める条件

次の場合は別Runまたは独立reviewerを要求する。

- high riskまたは外部・不可逆side effectを持つ。
- Definitionを作成した主体の自己確認だけでは独立性を満たさない。
- Contract適合と上位目的の評価で異なる専門性が必要である。
- failureの影響が大きく、共通mode failureを避ける必要がある。

## 4. Source Symbol IndexとReusable Routine Ledger

### 4.1 維持する理由

Source Symbol Indexは実codeに何が存在するかを機械的に把握し、Reusable Routine Ledgerは共有責務、
alias、統廃合、retirementなどの意味判断を保持する。事実層と意味層を分離することで、台帳だけに存在する
routine、codeに存在するが未帰属のroutine、重複実装を検出できる。

### 4.2 過剰になる条件

次の運用は避ける。

- 全private helper、getter、lambda、Test helper、generated codeへHumanが意味entryを作る。
- 全symbolの責務、入出力、side effect、類似候補を変更ごとにHumanが再確認する。
- 全件Human確認が終わるまで大規模既存projectの実装を無期限に停止する。
- Source Symbol IndexとLedgerへ同じ事実を二重入力する。
- 変更影響外のroutineまで`implementation_ready`ごとに再確認する。

symbol数に比例してHuman作業が増え、baseline確認中にcodeが変わって台帳がstaleになる。品質gateが
開発停止の原因になる。

### 4.3 推奨する形

全symbolは機械的なSource Symbol Indexへ収録し、増分更新と定期全再生成でfreshnessを確認する。

Humanが確認するReusable Routine Ledgerと再利用判断は次へ限定する。

- public API
- 複数componentまたはmoduleから利用される共有routine
- cross-contract routine
- security、保存、権限、外部送信などのhigh-risk routine
- 重複候補
- retired routineと後継
- 今回の影響閉包に含まれるroutine
- 新規作成、共有化、統廃合の提案対象

baseline時にHumanが確認するのは、全symbolの意味ではなく次である。

- Index生成規則と対象外規則
- coverageとfreshnessの統計
- public、共有、high-risk symbolの抽出結果
- 重複候補とretired routine
- representative sample
- 未解決候補と処置

`implementation_ready`では今回の変更範囲、類似候補、retired verdictを確認する。全体Human auditは
baselineまたは定期checkpointで行い、毎変更には行わない。generated code、外部vendor、単純accessor
などは明示した規則でLedger対象外にできるが、Source Symbol Index上の存在を黙って消さない。

### 4.4 Human範囲を広げる条件

次の場合はimpact slice外へHuman確認を拡大する。

- 重複候補のconfidenceまたは機械判定根拠が不足する。
- public boundaryまたは共有責務が変わる。
- retired routineが再導入される。
- high-risk routineのside effectが変わる。
- 定期全再生成でIndexまたはLedgerのdriftを検出する。

## 5. Operational Provenance

### 5.1 維持する理由

ReviewCompass3は、Requirement、Contract、Plan、Context、Run、Test、Decision、authority、source、
side effect、acceptance、stale、中止、再開を後から再構成する必要がある。判断とEvidenceの因果関係を
失うと、Task Contract方式の完了判断、AI委譲、As-Built projectionを検証できない。

### 5.2 過剰になる条件

次のcaptureは避ける。

- file read、symbol検索、Test assertion、debug logなど全低水準操作を耐久eventにする。
- すべてのeventへ全共通fieldと全relationを要求する。
- raw response、session、diagnosticを無期限に通常Provenanceへ保存する。
- authoritative eventと再生成可能なindex・metricを同じ保存義務にする。
- すべてのeventを同期書込みし、診断記録の失敗で本体処理を停止する。
- 重要なDecision eventを大量の診断eventへ埋没させる。

保存量だけでなく、書込みlatency、schema変更、query、privacy、retentionの費用が増える。記録量が多い
こと自体は説明可能性を保証しない。

### 5.3 推奨する層

#### 必須・耐久event

失うとaccepted判断、authority、side effectまたは復旧を再構成できないものをimmutableに保存する。

- Requirement、Contract、Plan bundle、Context、Source Snapshot、Change Set
- Run、Attempt、Verification Evidence
- Decision Recordとauthority
- permit、state transition、acceptance、stale、invalidate、termination
- externalまたは不可逆side effect
- integration checkpoint、Build Artifact、release

欠落時は`provenance_incomplete`として`verified`または`accepted`を拒否する。

#### 運用event

retry、checkpoint、worker lease、cache、incremental update、scope expansionなど、障害解析と再開に必要な
eventである。riskと実行経路に応じたCapture Profile、quota、retentionを適用する。

#### 診断・raw data

debug log、詳細trace、raw response、session raw、performance sampleなどである。通常Provenanceから物理的・
権限的に分離し、sampling、rotation、期限付きretentionを許可する。判断、外部送信、不可逆操作をsampling
してはならない。

#### 派生物

query index、集計metric、dashboard、graph cache、As-Built候補など、一次eventから再生成できるものは
削除・再生成可能とする。一次eventと同じretentionを要求しない。

### 5.4 event schema

共通envelopeを小さくし、event type固有fieldをpayloadへ置く。

```text
Common Event Envelope
  - event_id / event_type / schema_version / occurred_at
  - actor
  - project / work / run identity
  - input / output refs and digests
  - confidentiality / retention class
  - causal predecessor / typed relations

Type-specific Payload
  - decision and authority
  - state transition and permit
  - verification and metric
  - scheduler and lease
  - side effect
  - duration / resource / cost
```

すべてのeventへ空のdecision、state、verification、cost fieldを持たせない。relationはevent typeごとの
許可集合を使い、内容はcontent-addressed artifactへの参照とDigestで共有する。

authority変更または外部side effectの直前に必要なeventはwrite-aheadで耐久化する。運用・診断eventは
安全性義務を損なわない範囲でbatchまたは非同期保存できる。

### 5.5 Capture Profileを拡張する条件

次の場合は必須eventまたはretentionを追加する。

- acceptanceまたは復旧を既存eventから再構成できない。
- 新しいside effectまたはauthority classを導入する。
- As-BuiltまたはEvaluationで必要なrelationが欠落する。
- 実障害の原因が現在の運用eventから判定できない。

過去に存在しなかった事実を推測して補完せず、追加後のevent versionから取得する。必要性が確認されない
低水準eventを将来用途だけを理由に無制限収集しない。

## 6. 設計判断のまとめ

| 対象 | 維持するもの | 統合・限定するもの |
|---|---|---|
| 6 Plan | 六つの責務viewとobligation coverage | 一つのbundle identity、共通保存、consumer projection |
| Challenge | 三Verdictの意味、基準、failure route | risk別にRun、reviewer、round、Human gateを構成 |
| 関数台帳 | 全symbolの機械Index、共有責務のLedger | Human確認を共有・high-risk・影響範囲へ限定 |
| Provenance | 判断、authority、Evidence、state、side effectの因果 | 運用、raw、派生dataのCapture Profileとretention |

次の根拠がない分離は行わない。

- 独立したauthority
- 独立したlifecycle
- 独立したsecurityまたはretention境界
- 独立したfailure recovery
- 実測されたscale要件

初期vertical sliceでは、意味上の被覆とfailure verdictを保った最小bundle、risk別Challenge、機械Indexと
限定Human確認、必須Provenance eventを実装する。独立service、全変更の多重review、全symbolの意味台帳、
全低水準eventの無期限保存を初期完了条件にしない。
