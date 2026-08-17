> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
reviewed_intent: ../current/reviewcompass3-intent-current.md
reviewed_plan: ../current/reviewcompass3-plan-current.md
---

# 大規模・複雑なソフトウェア開発を前提とした設計評価

## 1. 目的

ある程度規模が大きく、複雑なソフトウェアの開発へReviewCompass3を適用することを想定し、
現行Intentと計画について、必要な機能が盛り込まれているか、また過剰な設計になっていないかを
評価する。

本書は評価結果を固定する非規範文書である。現行Intent、Requirements、計画を直接変更せず、
採用する補強または簡素化は、別途Humanが判断して規範文書へ反映する。

## 2. 評価対象と前提

評価対象は次の統合最新版とする。

- [ReviewCompass3 Intent統合最新版](../current/reviewcompass3-intent-current.md)
- [ReviewCompass3計画統合最新版](../current/reviewcompass3-plan-current.md)

現行Intentが定める主な利用者は、AIの支援を受けながら一人でソフトウェアを開発・保守する
開発者である。このため、本評価では「一人の開発者が、複数のAI実行主体を利用し、大規模で
複雑なコードベースを扱う」範囲を主対象とする。複数組織、複数team、複数repositoryを横断する
enterprise開発は、必要性を確認する対象ではあるが、現行Intentの必須範囲とはみなさない。

## 3. 総合評価

現在の設計は、主対象に必要な機能を概ね網羅している。Task Contract、TDD、上流改定、依存と
循環、変更規模に応じたreview入力、Provenance、配置、復旧、関数再利用、Issue Resolution、
段階的なAI委譲を一つの開発方式として接続しており、単純なhappy pathだけを扱う設計ではない。

一方で、大規模コードベースへ継続適用するには、次の4点を補強する必要がある。

1. 独立作業を安全に並行実行する方式
2. Git、CI、build成果をTask Contractと結ぶ識別
3. 非機能要件を検証へ接続するQuality Attribute Profile
4. Index、意味graph、Test、Provenanceの増分処理と資源予算

また、6種類のPlan、複数Challenge、関数台帳、詳細なProvenanceを、それぞれ独立した機構として
一律に実装すると過剰になる。概念上の責務分離は維持しつつ、一つのPlan bundle、risk別の
verification、機械Indexと限定的Human確認、Provenance profileとして軽量に実装する必要がある。

## 4. 優先度の高い不足

### 4.1 並行作業model

現行計画では、schedulerは未解決blocking辺を持たない単一の`active leaf`だけを選ぶ。この方式は、
依存の発散、循環、同時変更の衝突を防ぐ安全な初期既定として妥当である。

しかし、互いに独立したContractを複数のAI実行主体が処理できる場合も直列化されるため、大規模な
開発では処理待ちが増える。後続で次を扱える必要がある。

- 競合領域が重ならないContractの並行実行
- Work Itemのowner、lease、期限
- 同一file、symbol、Requirement、state ownerへの競合検出
- 並行作業を統合する時点でのfreshnessとstale再判定
- merge後のIntegration Verdictと再検証

初期実装では`single_active_leaf`を維持する。並行性の必要性を実測した後、Workflowのscheduler
policyとして`bounded_parallel`を追加し、新Featureまたは汎用分散schedulerを先行実装しない。

### 4.2 Git、CI、変更集合の識別

現行計画はcommitをTDD成果およびProvenanceへ関連付けるが、次の識別と状態遷移を明示的な
設計対象にしていない。

- base commit、変更後commit、変更集合
- branch、worktree、checkout
- merge、rebase、競合解決
- CI Run、実行環境、Test結果
- build artifactとsource、Test、Contractの対応
- merge後またはbase変更後に再利用できるEvidenceの条件

これらは独立Featureとして追加せず、Project Binding、Workflow、Verification、Operational
Provenanceへ分担する。Task ContractとPlan bundleは固定source identityを入力とし、baseまたは
統合結果が変わった場合に、影響を受けるContext、Test Evidence、Verdictをstaleにする必要がある。

### 4.3 非機能要件

現行Requirementsは、外部義務、入力、出力、停止、復旧、保存、受入、対象外を定義するが、複雑な
製品で必要となる品質属性を、project単位でまとめて検証へ渡す方式が明示されていない。

最低限、次の品質属性を扱う必要がある。

- 性能と処理時間
- 規模上限とresource使用量
- reliabilityとavailability
- token、storage、外部service費用
- compatibilityとmigration期間
- securityとprivacy
- maintainability

一律の数値や新Featureを追加するのではなく、RequirementまたはArchitecture Policyから参照する
版付き`Quality Attribute Profile`として定義し、Verification Plan、Release Evaluation、
Provenanceへ接続するのが適切である。

### 4.4 大規模化に対する増分処理

`impact_slice`によりreview入力を変更規模へ比例させる方針は適切である。一方、medium riskで
関連Testと全Test、high riskで全Testを実行する現在の規則は、Test数が大きくなると継続的な
開発を止める可能性がある。

次を補強する必要がある。

- Source Symbol Indexと意味graphの増分更新
- affected-test selection
- input、tool、environment、結果Digestによる安全なEvidence再利用
- 定期、integration、release時のfull suite
- Index、Provenance、logのquota、rotation、compaction、retention
- 処理または入力budgetを超えた場合の分割、scope拡大、停止

high riskの全Testは維持する。medium riskは、影響Testと必要なcross-contract Testを変更ごとに実行し、
full suiteを定期またはintegration checkpointで実行する方式を検討する。

## 5. 対象に応じて必要になる機能

次の機能は複雑な製品では必要になり得るが、すべてを初期実装の必須範囲にはしない。

- package依存、lock file、脆弱性、license、SBOM、再現可能build
- Provenance、Workflow state、Project Artifactsのbackup、export、restore
- monorepoまたは複数repositoryを横断するContractと変更集合
- release artifactのversion、署名、promotion、rollback

実際の対象projectで必要性が確認されたものを、既存Featureの別Task Contractとして追加する。
複数repositoryや複数組織への対応を、現在の`local_integrated`初期sliceへ含めない。

## 6. 過剰になり得る設計

本節の4項目について、維持する意味、過剰化する条件、推奨する物理実装、分離を認める条件は
[Task Contract設計の過剰実装を避ける境界に関するメモ](2026-08-03-overdesign-boundaries-memo.md)
に詳述する。本節は総合評価上の要約として保持する。

### 6.1 6種類のPlan

6種類のPlanは、Contract obligationを実行時の責務へ投影し、欠落と不整合を検出する観点として
有効である。ただし、6個の独立文書、独立state machine、独立serviceとして実装すると過剰になる。

初期実装では、一つのcompiled Plan bundleに6つのsectionまたはviewを持たせる。各Planを別の
永続aggregateまたはRuntime componentへ分割するのは、独立したlifecycleまたはscale要件が
実測された場合に限る。

### 6.2 Challengeとgateの多重化

Definition Challenge、Conformance、Final Challengeは、Contract定義、実行結果、上位目的との
整合性という異なる失敗を検出するため、意味上の分離は維持する。

ただし、すべてのContractで同じreviewer数、round数、検証負担を要求しない。

- low risk：決定的validatorと関連Testを中心とする
- medium risk：必要な独立reviewを追加する
- high risk：三つのChallengeと独立reviewを明示的に実施する

Challengeの意味は分離し、実行回数と実行主体をVerification Profileで構成する。

### 6.3 関数台帳のHuman確認範囲

全関数とmethodを機械的なSource Symbol Indexへ収録する方針は、重複候補の発見と影響分析のために
妥当である。一方、Index、Reusable Routine Ledger、実codeの全件を、変更ごとにHumanが確認する
方式は拡張できない。

Human確認は次へ限定する。

- public API
- 共有routine
- cross-component routine
- high-risk routine
- 今回の影響閉包に含まれるroutine
- 重複候補とretired routine

全件Indexは機械的に生成・検査し、全体Human auditはbaseline作成時または定期checkpointで行う。

### 6.4 Provenanceの粒度

現在のevent fieldと型付きrelationは、判断、権限、上流改定、依存、再利用、評価を後から再構成する
ために十分である。ただし、すべてのeventへすべてのfieldとrelationを要求すると、保存量、検証時間、
実装負担が増える。

共通の最小必須event setを固定し、Contract type、risk、side effect、decision classに応じて
Provenance Capture Profileを追加する。projectionに利用する一次eventは保持しつつ、raw capture、
派生index、集計値には別々のretentionと再生成規則を持たせる。

## 7. 現行設計で十分に扱われている事項

次は大規模で複雑な開発にも必要であり、現時点で過剰とは判断しない。

- 不整合の種類に応じて変更が必要な最下位層へ戻るrevision経路
- dependency、cycle、pause、cancel、close-scope
- Requirement変更と実装不良の区別
- 変更規模に応じたreview入力と理由付きscope拡大
- TDDとContract、Test version、Evidenceの固定
- 開発開始前の配置baseline
- stable deploymentとdevelopment candidateの分離
- crash後の再開とside effectの重複防止
- Session Evidence Sourceとraw、派生物の分離
- Source Symbol IndexとReusable Routine Ledgerによる再利用判断
- Issue Resolution Pathの手作業Pilot
- AI判断委譲、As-Built projection、shared deployment、Issue自動化のDeferred化

特に、実測前に汎用Task orchestration、plugin system、分散scheduler、Issue管理UIを作らない方針は、
過剰実装を抑えるうえで妥当である。

## 8. 推奨する適用判断

大規模コードベースを使った最初のPilot前に、次を既存計画へ補強する。

1. `single_active_leaf`を初期既定とし、将来の競合domainと`bounded_parallel`の拡張点を定義する
2. source、変更集合、CI Run、build artifactのidentityとstale規則を定義する
3. project別Quality Attribute ProfileをRequirementsとVerificationへ接続する
4. Index、意味graph、Test、Provenanceの増分処理とbudgetを定義する

同時に、初期実装では次の簡素化を守る。

1. 6 Planを一つのPlan bundle内のviewとして扱う
2. Challengeの実行負担をrisk別に構成する
3. 全symbolを機械Index化し、Human確認を共有、高risk、影響範囲へ限定する
4. Provenanceを最小必須event setと追加profileに分ける

これらの補強と簡素化は、新Featureまたは新componentを追加せず、既存のWorkflow、Project Binding、
Verification、Semantic Trace、Operational Provenanceへ割り当てる。これにより、現在のTask Contract
中心設計を維持しながら、大規模化に必要な能力と初期実装の現実性を両立できる。

## 9. 結論

現行設計の機能被覆は良好であり、主対象である単一開発者とAIによる複雑なソフトウェア開発へ
適用できる骨格を持つ。全面的な再設計またはFeature追加は不要である。

ただし、並行作業、SCM／CI identity、非機能要件、増分処理の4点を補強せずに大規模codebaseへ
適用すると、直列化、Evidenceの誤再利用、品質基準の曖昧化、Test・Index・Provenance費用の増大が
発生する可能性がある。一方、Plan、Challenge、台帳、Provenanceをすべて独立機構として実装すると
過剰になる。既存ownerへ能力を追加し、riskと規模に応じて処理を構成する方針を採用すべきである。
