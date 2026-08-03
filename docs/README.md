# ReviewCompass3文書索引

## 統合最新版

現在の全体像は、次の3文書を順に読む。

1. `current/reviewcompass3-intent-current.md`
2. `current/reviewcompass3-glossary-current.md`
3. `current/reviewcompass3-plan-current.md`

Intent統合最新版は製品目的、利用者、原則、非目標、成功基準を独立して保持する。計画統合
最新版はFeature、Requirements、Task Contract設計、TDD、Workflow、Provenance、配置、
初期Work、Deferred Workを現在有効な形へ解決する。統合用語集は両文書で使うdomain固有語の
日本語表示名、canonical token、意味、旧語の読み替えを保持する。3文書はHuman承認前の
successor候補であり、front matterの生成元pathとDigestから詳細と変更Evidenceへ戻れる。

## 生成元の更新候補

Task Contract中心化に関する詳細な生成元は次の順に読む。

1. `concepts/2026-08-02-task-contract-centered-engineering.md`
2. `intent/2026-08-02-task-contract-centered-intent-amendment.md`
3. `requirements/2026-08-02-task-contract-requirements-delta.md`
4. `design/2026-08-02-task-contract-design-amendment.md`
5. `design/2026-08-02-stage-five-to-task-contract-inheritance.md`
6. `plan/2026-08-02-task-contract-centered-replan.md`
7. `development/2026-08-02-development-policy.md`

## 重要な設計判断メモ

大規模・複雑なsoftwareへの適用と、Task Contract設計の実装境界は次を参照する。

- `design/2026-08-03-large-complex-software-design-assessment.md`
- `design/2026-08-03-parallel-work-introduction-timing-memo.md`
- `design/2026-08-03-source-change-verification-identity-timing-memo.md`
- `design/2026-08-03-non-functional-requirements-verification-profile-memo.md`
- `design/2026-08-03-overdesign-boundaries-memo.md`

特に`overdesign-boundaries`は、6 Plan、Challenge、関数台帳、Provenanceについて、意味上の分離を
維持しながら独立artifact、service、Human gate、無期限captureへ過剰展開しない設計判断を保持する。

議論の固定原文と変更判断は次へ保持する。

- `../records/sources/2026-08-02-source-catalog.json`
- `../records/sources/2026-08-02-task-contract-source.md`
- `../records/sources/2026-08-02-llmgp-hybrid-experiment.md`
- `../records/sources/2026-08-02-reviewcompass2-shared-routine-ledger.md`
- `../records/sources/2026-08-02-reviewcompass2-issue-plan-path.md`
- `../records/sources/2026-08-02-reviewcompass-conformance-evaluation.md`
- `../records/sources/2026-08-02-reviewcompass2-terminology-control.md`
- `../records/sources/2026-08-02-deployment-topology-discussion.md`
- `../records/sources/2026-08-02-reviewcompass2-change-scaled-review-input.md`
- `../records/sources/2026-08-02-reviewcompass2-cross-cutting-lessons.md`
- `../records/sources/2026-08-03-project-progression-discussion.md`
- `../records/task-contract/task-contract-centered-documentation-v1.json`
- `../records/task-contract/task-contract-centered-documentation-v2.json`
- `../records/task-contract/task-contract-centered-documentation-v3.json`
- `../records/task-contract/task-contract-centered-documentation-v4.json`
- `../records/task-contract/task-contract-centered-documentation-v5.json`
- `../records/task-contract/task-contract-centered-documentation-v6.json`
- `../records/task-contract/task-contract-centered-documentation-v7.json`
- `../records/task-contract/task-contract-centered-documentation-v8.json`
- `../records/task-contract/task-contract-centered-documentation-v9.json`
- `../records/task-contract/task-contract-centered-documentation-v10.json`
- `../records/task-contract/task-contract-centered-documentation-v11.json`
- `../records/task-contract/task-contract-centered-documentation-v12.json`
- `../records/task-contract/task-contract-centered-documentation-v13.json`
- `../records/task-contract/task-contract-centered-documentation-v14.json`
- `../records/task-contract/task-contract-centered-documentation-v15.json`
- `../records/task-contract/2026-08-02-documentation-reconstructability-audit.json`
- `../records/task-contract/task-contract-centered-documentation-v16.json`
- `../records/development/development-policy-v2.json`

## 適用関係

- 2026-07-27から2026-07-28のintent、concept、requirements、design、planは固定済みの
  baselineであり、過去の承認と監査証拠の参照先として保持する。
- 2026-08-02のTask Contract文書群は、それらを上書きしない差分・後継候補である。
- 2026-08-02の開発方針は、リスクベースのテストファースト、段階的自己適用、
  Human判断範囲を定める。
- Task Contract文書群は第5段完了承認を代替しない。構造化requirements、design、
  acceptance test、差分監査を経て新しい承認候補を生成する必要がある。
- Task Contract requirements差分は`REQ-CONTRACT-001`〜`008`を対象とする。`007`でaccepted
  Delivery Work Itemに束縛されたContract間のIntegration Verdictを定義し、`008`で
  Provenanceからの実装文書projectionを後続開発として定義する。`008`は初期開発へ入れない。
- Workflow requirements差分は`REQ-WORKFLOW-005`〜`009`を追加し、new developmentと
  maintenanceのrouting、reopen、上流改定、依存・循環、制御終了、実装前の共通ルーチン
  照合を定義する。
- SDD workflow、maintenance、reopenは三つの独立engineにせず、二つのwork originと
  fresh / reopenのcontinuation modeを共通Task Contract Deliveryへrouteする。
- LLMGPのSDD/TDD折衷試行は先行実験Evidenceとして扱い、受入条件の真偽を基準とする
  reopen分類、変更のstate effect、risk別review、Project Policy Overlayを明示的に採用する。
- 旧第5段の9 design、29 interface、8 state machine、14 protocol、37 acceptance testは
  継承matrixで`preserve / adapt / replace`へ全件分類する。replaceは旧表現の廃止であり、
  安全性義務、failure verdict、successor owner、後継testの削除を意味しない。
- ReviewCompass2のP-5と共通ルーチン台帳を前身方針として継承する。実コードから生成する
  Source Symbol Indexと意味判断を保持するReusable Routine Ledgerを分離し、red確認後の
  green実装前に`reuse / extend / merge / split_with_rationale`を判断する。
- 初回実装前にLayout Baselineを固定し、空の配置fixtureでproject移動後の参照を検査する。その
  直後にSession Log Bootstrapを準備してWork 2以降の議論、判断、調査、変更を保全する。その配置を
  基準に全関数・methodのSource Symbol Indexと、共有・high-risk・重複・retired・影響範囲を対象にした
  Reusable Routine Ledgerの初期baselineを整備する。全symbolは機械Indexへ収録し、Humanは生成規則、
  coverage、freshness、対象routine、重複候補、retired routineを確認してから最小E2Eへ進む。
- ReviewCompass2のIssue→Plan経路を継承し、横断的なIssue Resolution Pathとして計画する。
  Issue Resolution Planをcompiled Plan bundleから分離する。最初はWork 8で手作業Pilotし、
  必須fieldと停止条件を確認した後のDeferred Workでだけschemaと開始permitを実装する。
- ReviewCompassのconformance-evaluationは、実装由来差分、draft-only更新候補、reopen
  handoffを継承する。管理下codeの通常経路はProvenanceからのAs-Built projectionへ置換し、
  旧code-only推定は後続のlegacy reconstructionへdeferする。
- ReviewCompass2の登録制用語集を修正継承する。旧6段SDD、3 lane、単一状態台帳、代理判定は
  現行設計へ置換し、統合用語集を人向けの意味正本候補、schemaとPolicyを閉じた値の機械正本と
  して分離する。Runtimeでの用語強制は、初期の手作業運用で不足を確認した後にRequirements化する。
- 過去のデプロイ検討から、論理／物理配置の分離、local／shared／hybrid profile、Control／
  Execution Plane、durable worker再開、stable／development分離、distribution unitを修正継承する。
  初期は`local_integrated`だけを実装し、具体middleware技術と汎用Task Registryは固定しない。
- ReviewCompass2の変更規模比例review入力を継承し、変更単位からの影響閉包、Evidence抜粋、
  Contract必須材料で既定の`impact_slice`を構成する。無関係な文書総量ではpayloadを増やさず、
  局所化できない場合だけ理由付き`expanded_scope`または独立した`full_consistency`へrouteする。
- ReviewCompass2のfreeze原因と実装Evidenceから、Evidence Extraction Contract、Consumption
  Closure、Assurance Obligation Matrix、Validator Assurance Profile、Review Quality Contract、
  post-write verification、session source復元検証を修正継承する。旧Intent、旧lane、固定reviewer数・
  round数・容量値、provider固有pathは継承しない。新要件IDや第7 Planは追加せず既存50要件と6 Planを
  横断強化する。
- 過去のプロジェクト進行検討から、代表シナリオによる縦断被覆、Task Contractの粒度基準、
  部分side effectの補償／調停、自己適用後の外部software project検証を修正継承する。汎用Concierge、
  Task Registry、plugin platform、別domain applicationは継承しない。

## 固定baseline

- `intent/2026-07-27-reviewcompass3-intent-draft.md`
- `concepts/2026-07-27-task-runtime-concept.md`
- `requirements/review-context-requirements.md`
- `requirements/remaining-feature-requirements.md`
- `design/2026-07-28-reviewcompass3-design.md`
- `plan/2026-07-27-reviewcompass3-rebuild-plan.md`
- `plan/2026-08-02-development-policy-amendment.md`

固定baselineの内容を更新する必要がある場合、現在のパスを直接書き換えず、改定文書、
source Digest、置換範囲、変更理由を記録する。
