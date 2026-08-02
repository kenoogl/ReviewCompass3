---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
related_assessment: 2026-08-03-large-complex-software-design-assessment.md
related_plan: ../current/reviewcompass3-plan-current.md
---

# 並行作業modelの導入時期に関する検討メモ

## 1. 背景

[大規模・複雑なソフトウェア開発を前提とした設計評価](2026-08-03-large-complex-software-design-assessment.md)
において、現行の単一`active leaf`方式は安全な初期既定である一方、独立したTask Contractを
複数のAI実行主体が扱う場合も直列化するため、大規模開発では不足する可能性があると評価した。

この評価を受け、並行作業modelはReviewCompass3の設計へ反映する。ただし、設計への反映と
Runtimeでの実並行有効化を同時には行わず、段階的に導入する。

## 2. 合意した方針

並行作業modelは、設計上の前提を現在のRequirements・Design差分へ取り込む。最初のvertical
sliceは`single_active_leaf`で実行し、直列のWork Item lifecycle、依存、循環、stale、復旧、
Integration、Provenanceが安定した後に`bounded_parallel`を有効化する。

要点は次のとおりである。

- 並行可能なschema、identity、state境界、拡張点は初期設計で固定する。
- 初期Runtimeのscheduler policyは`single_active_leaf`とする。
- 初期実装中から、並行可能だったWork Item、競合理由、待ち時間を観測可能にする。
- shadow評価で効果と競合判定精度を確認してから実並行Pilotへ進む。
- 実並行Pilotは`local_integrated`、単一project、最大2 Work Item、low riskに限定する。
- 競合の有無を安全に確定できない場合は並行実行せず、直列へfallbackする。
- 汎用分散schedulerまたは新Featureを先行実装しない。

## 3. 初期設計で固定する事項

[Work 3：Requirements差分](../current/reviewcompass3-plan-current.md#work-3requirements差分)と
[Work 4：Design差分と最初のslice選定](../current/reviewcompass3-plan-current.md#work-4design差分と最初のslice選定)
で、少なくとも次を定義する。

- scheduler policy：`single_active_leaf | bounded_parallel`
- Work Itemのowner、lease、期限
- 固定source snapshotまたはbase commit
- 並行性判定に使うconflict domain
- 並行実行可否の判定結果と理由
- integration checkpoint
- mergeまたはbase変更後のfreshnessとstale再判定
- 一方のWork Itemが失敗、停止、中止した場合の他方への影響
- 並行実行中のProvenance relationと順序

単一active leafをstate modelの不変条件として埋め込まず、scheduler policyの初期値として扱う。
これにより、初期挙動の安全性を維持しながら、後続の並行化でWorkflow、state store、Provenanceを
全面移行する事態を避ける。

## 4. 段階的な導入順序

```text
Work 3
  並行性の安全義務をRequirements差分へ追加
  ↓
Work 4
  scheduler policy、lease、conflict domain、stale規則を設計
  ↓
Work 5A
  single_active_leafで最小E2Eを成立させる
  ↓
Work 6A
  並行性のnegative fixtureをDeferred Acceptance Catalogへ登録
  ↓
Work 7A
  durable state、process境界、crash再開を確認
  ↓
Work 8
  shadow schedulerで並行候補、競合精度、待ち時間を測定
  ↓
bounded_parallel Pilot
  local_integrated、単一project、max_parallel=2、low riskに限定
  ↓
Work 7B
  並行Work Itemを含むupdate、migration、rollback、復旧を検証
```

### 4.1 初期vertical slice

[Work 5A](../current/reviewcompass3-plan-current.md#work-5a最小review-task-contract-happy-path)では、
実並行を有効化しない。先に次を一つのWork Itemで確立する。

- Work Itemの状態遷移
- dependencyとcycle検出
- stale propagation
- crash後の再開
- side effectの重複防止
- Cross-Contract Integration
- Provenanceの完全性

### 4.2 negative fixture

[Work 6A](../current/reviewcompass3-plan-current.md#work-6a初期sliceのnegative-path)では、次を
Deferred Acceptance Catalogへ登録する。実並行機能が初期slice外であっても、将来必要となる
安全義務を失わない。

- 同じconflict domainを持つ二作業を同時開始しない。
- source snapshot変更後に旧Evidenceを再利用しない。
- lease切れまたはworker停止後に二重実行しない。
- 一方の失敗を理由なく他方のacceptedへ伝播させない。
- merge後に必要なIntegration Testを再実行する。
- crash再開時にside effectを重複させない。
- conflict domainを確定できない場合は直列化する。

### 4.3 shadow評価

[Work 8](../current/reviewcompass3-plan-current.md#work-8evaluation-pilot)では実行を直列のまま維持し、
schedulerだけに並行候補を判定させる。次を観測する。

- 並行実行可能と判定されたWork Item
- 競合と判定した対象と理由
- 並行化により削減可能な待ち時間
- 後から判明した未検出競合
- 並行化によって増えるstaleと再検証
- conflict domainを計算する費用

shadow評価は並行化の利益だけでなく、安全に直列化すべき不確実なcaseを識別できるかを確認する。

### 4.4 実並行Pilot

実並行PilotはWork 8の後、[Work 7B](../current/reviewcompass3-plan-current.md#work-7blifecycle-deployment-e2e)
より前に独立Workとして行う。初期条件は次とする。

```text
deployment_profile: local_integrated
project_count: 1
max_parallel: 2
risk: low
conflict_domain: disjoint
external_or_irreversible_side_effect: forbidden
decision_authority: human
```

このPilotで並行Work Itemを含むdurable restart、integration checkpoint、stale再判定、Provenanceを
確認する。その後のWork 7Bで、並行状態を保持するRuntimeのupdate、migration、rollbackを検証する。

## 5. 実並行を有効化する前提条件

次を満たすまで`bounded_parallel`を有効化しない。

- 直列Work Item lifecycleがgreenである。
- dependencyとcycle検出がgreenである。
- source、変更集合、commitのidentityが固定されている。
- stale propagationがgreenである。
- crash recoveryとidempotencyがgreenである。
- 二つ以上の関連Contractを直列にacceptedし、Integrationがgreenである。
- conflict domainを決定的に計算できる。
- 並行実行の判断、実行順序、結果をProvenanceから再構成できる。
- 不確実なcaseを安全に`single_active_leaf`へfallbackできる。

これらは正式導入の開始条件であり、設計への反映を遅らせる条件ではない。

## 6. Pilotの評価項目

実並行Pilotでは、少なくとも次を評価する。

- 重複または競合writeが発生しない。
- base変更とmergeによるstaleを漏れなく検出する。
- worker停止とlease切れからside effectを重複せず復旧する。
- 直列実行と並行実行でaccepted成果の意味が一致する。
- Integration Verdictが並行作業の両方を固定入力としている。
- Provenanceに判断、owner、lease、source identity、実行順序、統合結果が残る。
- lead time短縮が、追加された競合判定・再検証費用を上回る。

効果が確認できない、競合を安全に予測できない、またはProvenanceと復旧が不完全な場合は、
`single_active_leaf`を維持する。並行化をreleaseの完了条件にしない。

## 7. 結論

並行作業modelは、後から設計へ追加する機能ではなく、初期のRequirementsとDesignで拡張可能な
境界を固定する。ただし、実行機能は最初の直列E2Eへ含めず、直列lifecycle、durable state、
stale、Integration、Provenanceが成立した後に、shadow評価と最大2 Work ItemのPilotを経て導入する。

この順序により、単一active leafの仮定が実装全体へ固定されることを避けながら、並行処理固有の
複雑性によって初期E2Eの原因分析が困難になることも防ぐ。
