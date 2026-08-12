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

## 立て直し計画

開発停滞の原因、立て直しの原則、ブートストラップから製品本線へ戻る五段階は、次の採用済み計画を読む。

- `plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- `../records/development/2026-08-12-project-stall-recovery-plan-v5-adoption-decision-v1.md`（採用判断）

v1からv4は同じ`plan/`配下に旧版として保持し、最新版から先行版の内容識別値をたどれる。

## 当面の開発入口

立て直し期間の開発作業は、採用済み立て直し計画を開始入口とする。既存のoperational checklistは、
現在位置とEvidenceを確認する入力として使う。

- `plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- `development/2026-08-03-initial-development-checklist.md`
- `../TODO_NEXT_SESSION.md`（session更新・引き継ぎメモ）
- `development/templates/TODO_NEXT_SESSION.template.md`（TODO新規作成・構造復元用）
- `../records/session-handoffs/2026-07-28-todo-next-session-snapshot.md`（過去snapshot）

checklistはIntent、Requirements、計画を置き換えず、立て直し前の作業順、確認項目、完了Evidenceを一つの
操作viewへまとめた資料として使う。立て直し中の作業順は採用済み計画に従い、checkboxだけを完了根拠にせず、
参照するauthorityと固定Evidenceを確認する。
ルートTODOも状態正本ではなく、最新状況と次作業からauthority／Evidenceへ移るための人向け入口とする。
過去内容はTODOへ累積せず、独立保持する価値があるmilestoneだけ`records/session-handoffs/`へ保存する。

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
- `design/2026-08-03-current-work-projection-memo.md`
- `design/2026-08-03-self-application-improvement-routing-memo.md`
- `design/2026-08-03-execution-claim-verification-memo.md`

特に`overdesign-boundaries`は、6 Plan、Challenge、関数台帳、Provenanceについて、意味上の分離を
維持しながら独立artifact、service、Human gate、無期限captureへ過剰展開しない設計判断を保持する。
`current-work-projection`は、現在位置を第二の状態正本にせず、Provenance等からtextへ導出し、
実測後の画面UIへ同じstructured projectionを渡す設計判断を保持する。
`self-application-improvement-routing`は、自己適用中の問題・アイデアを実行中の合否基準と混ぜず、
既存のcurrent Work、Upstream Revision、Issue Resolution、checkpointへ機械的なroute候補を出す境界を保持する。
`execution-claim-verification`は、会話上の実施報告を完了Evidenceとみなさず、実施・結果・判断Claimを
固定Evidenceと観測した事後状態へ照合し、不一致時に進行を停止する規律を保持する。

## 単独文書の現在位置

2026-08-13に`docs/`配下の文書を機械照合し、ほかの文書から参照されていなかった4件を次のように分類した。
参照がないことだけを理由に現役入口へ追加せず、内容が現在も有効かと、後続の利用者決定を先に確認した。

| 文書 | 判定 | 現在の参照先 |
| --- | --- | --- |
| `design/2026-08-04-project-first-runtime-root-memo.md` | `一部だけ有効`。project-first配置、開発用と実行用の分離、必要なrootだけの作成は現役。原文全体は非正本で、Windowsの利用者限定権限などは後続扱い | `../records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json`と、その承認対象`../records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json` |
| `design/2026-08-04-work-4a-v2-start-condition-specification.md` | `置換済み`。Work 4A v3設計がv2を置き換えたため履歴として保持 | `design/2026-08-04-work-4a-rebuild-design-v3-proposal.md`と`../records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md` |
| `development/2026-08-04-work-4a-v3-shared-context-for-codex.md` | `履歴のみ`。作成時点の引き継ぎ資料であり、文書自身が非正本と明記 | `development/2026-08-03-initial-development-checklist.md`のWork 4A現在位置と、同欄が示す設計・決定記録 |
| `design/2026-08-08-consolidation-evaluation2-proposal.md` | `置換済み`。利用者指摘を反映したv2へ差し替え済み | `design/2026-08-08-consolidation-evaluation2-proposal-v2.md`と`../records/development/2026-08-08-consolidation-eval2-approval-decision-v1.md` |

配置メモの中核が現在も有効であることは、Layout Baseline v3の承認記録、現在の配置処理、関連する19試験の
成功で照合した。古い文書の未採用部分を現行保証へ広げない。

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
- `../records/development/development-policy-v3.json`
- `../records/development/development-policy-v4.json`

## 適用関係

- 2026-07-27から2026-07-28のintent、concept、requirements、design、planは固定済みの
  baselineであり、過去の承認と監査証拠の参照先として保持する。
- 2026-08-02のTask Contract文書群は、それらを上書きしない差分・後継候補である。
- 2026-08-02の開発方針と2026-08-03の改定は、リスクベースのテストファースト、段階的自己適用、
  自己適用で得た改善候補の記録・分類・停止判定・route、Human判断範囲を定める。改善候補は
  Work 8まで手作業規律として運用し、機械強制済みとは扱わない。また、会話上の実施報告を
  固定Evidenceと事後状態へ照合し、報告だけを完了根拠にしない。
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
