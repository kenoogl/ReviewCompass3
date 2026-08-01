---
lifecycle: provisional
normative_status: current-plan-candidate
promotion_required: true
---

# Task Contract中心化によるReviewCompass3再計画

## 1. 目的

Task Contractを構造化RequirementsとRuntimeの間に置き、ReviewCompass3の開発段階を
大域的仕様形成と局所的TDD Deliveryへ再構成する。既存成果を捨てず、変更影響を
差分で扱い、最小E2Eで有効性と配置可能性を実測する。

## 2. 固定baseline

次を履歴baselineとして保持し、上書きしない。

- 2026-07-27 intent承認成果
- Feature Partitioningと37 requirements
- 2026-07-28第5段designと適合性監査候補
- 第0段から第2段の実装、テスト、Evidence
- 2026-08-02開発方針改定
- Task Contract centered engineeringの外部議論文書とDigest

第5段候補の状態は`awaiting_human_approval`である。本再計画は第5段完了を承認せず、
Task Contract差分を反映するための再開理由になる。

## 3. 新しい標準ステージ

今後のReviewCompass3開発は次を標準とする。

```text
Stage A: Intent
Stage B: Feature Partitioning
Stage C: Requirements
Stage D: Task Contract Portfolio
Stage E: Task Contract TDD Delivery
Stage F: Cross-Contract Integration
Stage G: Release Evaluation
```

### Stage A: Intent

目的、利用者、成功、非目標、原則、優先順位を確定する。実装方法と特定Runtime構造を
過剰に固定しない。ただしTask ContractをRequirementsとRuntimeの実行可能な中間表現
とする製品方針はintentへ置く。

### Stage B: Feature Partitioning

大域的責務、所有境界、依存、共有境界を分ける。Task Contract Controlを新Featureと
して追加し、既存componentの状態所有を維持する。

### Stage C: Requirements

外部から観測できる義務、入力、出力、停止、復旧、保存、受け入れ、対象外を定義する。
Task Contractへ写像可能なatomic obligationと由来を保持する。

### Stage D: Task Contract Portfolio

全Requirementの受け先、Contract間依存、risk、cross-contract acceptanceを固定する。
実行予定のないContractまで詳細化せず、未被覆と競合を検出できる最小定義にする。

### Stage E: Task Contract TDD Delivery

各Contractを`draft → challenged → approved → compiled → red → green → verified →
accepted`で進める。Design、旧Task記述、Implementationを全体段階にせず、Contractの
実現成果として作る。green後は同一Contract versionとAcceptance Testを維持して
refactorし、green再確認後にverifiedへ進む。

### Stage F: Cross-Contract Integration

accepted Contract間のinterface、共有状態、E2E、failure propagation、配置、update、
uninstallを検証する。局所Contractがすべて成功しても全体Intentを満たさない場合、
Portfolio、RequirementsまたはIntentへ戻す。版付きIntegration Plan、E2E Evidence、
failure propagation Evidence、Integration Verdictを成果とする。

### Stage G: Release Evaluation

supported-platform matrix、配布物、migration、データ保護、Provenance完全性、
Evaluation Profile、既存方式との比較結果を確認し、release可否をHumanが判断する。

## 4. フィードバック

ステージは一方向に凍結しない。戻り条件を明示する。

- Contract challengeで上位欠落を検出：Requirementsへ戻る
- 複数Featureの責務競合：Feature Partitioningへ戻る
- 成功条件または非目標の競合：Intentへ戻る
- compile不能：Contract、Policy、Capability Catalogの該当箇所へ戻る
- red testを定義不能：ContractまたはRequirementへ戻る
- E2E不成立：Contract Portfolioまたはcross-contract interfaceへ戻る
- 評価不能：Capture PlanまたはEvaluation Profileへ戻る
- deploy不能：Portable RequirementまたはArchitecture Policyへ戻る

戻る場合は旧成果を削除せず、新versionと変更理由を結ぶ。

## 5. 現在地からの移行作業

### Work 1: 方針と固定入力

- 外部議論文書のDigestを固定する。
- 保存可能な原文はrepository内の不変snapshotへ保持し、source ID、capture日時、
  confidentiality、retention、artifact pathを記録する。保存しない場合は理由と
  `non_reconstructable`を明記する。
- 採用した議論をdecision ID、指示、意味、採否理由へ結ぶ。
- Task Contractの適用範囲をReview Task Contractへ限定する。
- 旧第5段候補をbaselineとして凍結する。
- 本改定文書群のsource、関係、statusを記録する。

完了条件：入力Digest、適用範囲、非目標、旧候補状態が一意である。

### Work 2: intent差分

- Task Contractのcontrol and provenance planeを追加する。
- 汎用Agent Runtime化を除外する。
- 二層review、最小権限、stale、配置非依存、評価可能性を追加する。

完了条件：旧intentの維持事項と置換事項が競合なく区別され、Human判断候補になる。

### Work 3: requirements差分

- `FEAT-TASK-CONTRACT-CONTROL`を追加する。
- `REQ-CONTRACT-001`〜`007`を確定する。
- Architecture Policyのidentity、競合、優先順位、stale伝播を`001`〜`003`へ組み込む。
- Definition ChallengeとFinal Contract Challengeを`004`で分離する。
- Cross-Contract IntegrationとIntegration Verdictを`007`で定義する。
- 既存37 requirementsを`preserve / adapt / replace / defer`へ全件分類する。
- 新旧Requirementとatomic obligationの順逆被覆を検査する。

完了条件：未被覆、重複所有、未定義interface、未解決停止条件がない。

### Work 4: design差分

- Contract schema、Portfolio、Compiler、Plan bundleを設計する。
- Architecture Policy schemaと決定的なPolicy解決を設計する。
- 既存Context、Workflow、Harness、Triage、Trace、Portable、Evaluationへ接続する。
- Contract lifecycleとfailure propagationを状態機械へ追加する。
- Provenanceの型付き複数関係、Evaluation trial identity、Deployment Manifest、安定した
  Project Identity、Bindingを設計する。
- Integration Plan、E2E Evidence、Integration Verdictを設計する。

完了条件：全新Requirementに受け先、interface、状態、acceptance testがある。

### Work 5: 最小Task Contract E2E

小さな仕様変更一件を対象に、次の一本を通す。

```text
Requirement
  → Review Task Contract
  → compile
  → Context Manifest
  → stub reviewer
  → Contract Conformance
  → Final Contract Challenge
  → Human decision
  → Provenance verdict
  → accepted artifact
```

初期実装では一Contract type、一Compiler version、一実行トポロジに限定する。
汎用DSL、plugin system、任意Task orchestrationを先に作らない。

### Work 6: TDD negative path

- Contract obligation欠落
- source Requirement未解決
- Plan被覆欠落
- Context不足
- capabilityまたはpermission過剰
- Contract変更後のstale
- crash後の再開
- 必須Provenance event欠落
- optional Evaluation observation欠落
- Contract適合だがRequirement欠落

各負例をredとして確認し、同じContract versionのAcceptance Criteriaを変更せず実装を
修正してgreenにする。green後はAcceptance Testを変更せずrefactorし、greenを再確認する。
RequirementまたはContract期待が誤っていた場合は新versionへ移り、Test変更理由を
記録する。

### Work 7: deployment E2E

- source checkoutとinstalled codeを分離する。
- target projectとruntime rootを別配置にする。
- OS標準配置、環境設定、明示overrideの優先順位を検証する。
- Project BindingとIntegration Manifestを検証する。
- project移動、update、migration、uninstallを検証する。
- sensitive storeの権限とretentionを検証する。
- project内容変更で`project_id`が変わらないこと、同一projectの複数checkoutを異なる
  Bindingとして扱えることを検証する。

### Work 8: evaluation Pilot

既存Review Task方式とTask Contract方式を、同じ対象、source universe、model、Tool、
budgetで比較する。

各試行はevaluation case、condition、pair、trial、実行順序、model・Tool・budget設定、
label作成者、評価者、confidenceへ結ぶ。無作為化、盲検化、反復数はProfileで指定し、
初期Pilotで未指定の場合も未指定であることを記録する。

初期評価領域は次に限定する。

- Context obligation充足とContext量
- Finding Precision、Recall、責務外指摘率
- RequirementからEvidenceまでの追跡可能率
- Contract作成からacceptedまでの時間と再作業
- Human介入回数と判断時間
- Tool、token、費用、保存量

Pilot完了条件は優位性の確定ではなく、必要eventの取得、指標再計算、欠測、privacy、
比較可能性、記録負担を確認できることである。

## 6. 最初のTask Contract

最初のContractは、ReviewCompass3自身の小さな文書変更を対象とするReview Task
Contractとする。Implementation Task Contractを初回から正式Runtime対象にしない。

最初のContractへ含める最小責務は次である。

- 固定Requirementと変更Targetの適合性をレビューする
- source universeとScopeを固定する
- 必須Contextを構築する
- stub reviewerで決定的なFindingを得る
- ConformanceとChallengeを分離する
- Human判断を対象Digestへ束縛する
- Requirementからaccepted artifactまでをProvenanceで結ぶ

## 7. Designの扱い

独立した全体Design段階は廃止するが、設計判断は次に分けて保持する。

### Architecture Policy

複数Contractへ共通する制約を版付きで保持する。

- 原理Aの責務分担
- component state ownership
- ID、Digest、Schema
- securityとpermission
- external send
- Human decision
- storageとdeployment
- cross-contract interface

各Policyは`policy_id`、version、digest、owner、適用範囲、rule ID、優先順位、
supersedes関係、競合解決を持つ。未解決または同順位競合のPolicyはcompile入力にしない。

### Design Decision

一Contractまたは少数Contractに局所的な実現判断を保持する。

- 対象Contractとobligation
- alternatives
- selected design
- rationale
- affected TestとImplementation
- rollbackまたはreplacement条件

## 8. リスクベースTDD

既存開発方針を維持する。

- low：関連自動テスト
- medium：関連テストと全テスト
- high：全テスト、fault injection、代表データ、独立review

保存、削除、機微情報、権限、状態遷移、外部送信、migration、uninstall、Provenance
完全性は原則highとする。

赤テストだけのcommitは必須にしない。統合対象commitは原則greenにする。文書、調査、
Contract候補探索には形式的なred-greenを強制しない。

## 9. Provenanceと評価の運用

各RunはCapture Planに従って一次eventを追記する。metricはeventを変更せず再計算する。

eventのappend順序は`previous_event_id`、意味的依存は閉じた語彙の複数`relations`で
記録する。比較評価に必要なcase、condition、pair、trial、実行条件、評価者も一次event
または参照先へ固定する。

- Operational Provenance欠落：Runをverifiedまたはacceptedにしない
- optional評価観測欠落：成果を保ち評価状態だけを下げる
- Outcome Label不足：Recallなど該当metricを計算しない
- metric変更：旧projectionを残して新versionで再計算する
- 改善反映：固定比較とHuman承認後だけ次周期へ適用する

## 10. デプロイを最初から扱う規則

各Task Contractは、必要なlogical root、allowed read / write、integration、機密性、
retentionを宣言する。CompilerはDeployment Manifestへ解決できないContractを
`not_compilable`にする。

`project_id`はProject Manifestに保存した安定IDとし、内容digest、repository root、
checkoutごとのBindingから分離する。project移動と通常の内容変更ではBindingまたは
artifact digestだけを更新する。

実装中も開発checkoutのimportや相対配置だけで成功扱いにしない。少なくとも
distribution testでは別install root、別project root、別runtime rootを使用する。

## 11. 停止条件

- Task Contractの適用範囲が汎用Agent Runtimeへ暗黙拡大した
- source RequirementまたはContract obligationの被覆が不明である
- Compilerが未対応obligationを黙って落とす
- Challenge Reviewの固定材料と完了条件がない
- Definition ChallengeとFinal Contract Challengeを区別できない
- Architecture Policyのidentity、適用範囲、優先順位または競合解決がない
- accepted Contract間のIntegration Verdictを生成できない
- 必須Provenanceを保存できない
- 評価値とOperational verdictを混同する
- 開発checkoutまたは特定アプリ配置がruntime必須条件になる
- sensitive dataの分類、権限、retentionがない
- 第5段旧候補を変更後設計の承認証拠として再利用する

## 12. 新しい第5段相当の完了条件

- Task Contract中心intentがHuman判断済みである。
- 新requirementsと既存37 requirementsの差分被覆が完了している。
- Contract schema、Compiler、Plan、state、interface、deployment、evaluationが設計済みで
  ある。
- Architecture Policy、型付きProvenance関係、Project Binding、Integration Verdictが
  設計済みである。
- 新旧設計の`preserve / adapt / replace / defer`監査が完了している。
- 最小E2Eと負例のAcceptance Testが確定している。
- 未解決review Findingがない。
- 新しい承認候補が旧候補、変更理由、全Evidenceへ結ばれている。

## 13. 実装へ進む条件

新しい第5段相当の設計全体を巨大な基盤として先に実装しない。Humanが方向と最小
Contractを承認した後、Work 5の一本に必要な薄いvertical sliceから実装する。

E2Eで実測されていない汎用化、追加Schema、Contract type、adapter、評価指標はbacklogへ
置き、具体的な不足が確認されるまで必須化しない。
