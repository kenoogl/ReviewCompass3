---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
related_plan: ../current/reviewcompass3-plan-current.md
related_checklist: ../development/2026-08-03-initial-development-checklist.md
---

# 手作業自己適用からの改善候補を計画改定へ送る経路の検討メモ

## 1. 目的

ReviewCompass3は、初期段階では計画とchecklistを人とAIが手作業で自己適用し、実際の開発で得た問題、
不足、改善案を計画へ反映しながら方式を練り上げる。この方法は実測に基づく設計改善に有効だが、
実装中の合否基準を随時書き換えると、TDDの判定可能性、履歴、Evidence、開発速度を失う。

本メモは、自己適用から生じた候補を、実行中のDeliveryと混ぜずに記録、分類、route、改定、評価する
方法を定める。また、どこまで機械処理でき、どこからHuman判断が必要かを整理する。本メモは
Issue Resolution PathとUpstream Revisionの前段を補助する非規範案であり、新しい大域Stage、製品Feature、
Issue engineまたは正式schemaを追加しない。

## 2. 基本原則

1. 知見の記録を推奨するが、知見を得た瞬間に実行中の合否基準を書き換えない。
2. Delivery、Learning、Revisionを別identityとEvidenceで扱う。
3. 実装不良を上流変更で通さず、上流不良を実装patchだけで隠さない。
4. blocking候補だけを現在Workへ割り込み、それ以外はcheckpointでまとめて判断する。
5. 機械は検査、候補分類、route提案、影響候補を生成できるが、意味的採否と計画変更を確定しない。
6. 採用、延期、却下、重複をすべて記録し、成功した案だけを残さない。
7. 候補recordの存在を完了にせず、消費先と後続Outcomeまで結ぶ。

## 3. 三つのloop

```text
Delivery loop
  Task Contract → red → implementation → green → verified
                         ↓ observation

Learning loop
  candidate capture → validation → classification → hypothesis / evidence
                         ↓ disposition proposal

Revision loop
  revision proposal → challenge → Human decision → new version
                    → impact / stale closure → resume → outcome evaluation
```

Delivery loopのContract、Test、Plan bundleは固定する。Learning loopで候補を記録しただけでは、
Deliveryの期待、permit、Testを変更しない。Revisionが承認された場合だけ、新versionとstale閉包を作って
Deliveryを再開する。

## 4. 改善候補の分類

初期の分類候補は次である。閉じた正式enumはPilot後に決める。

| 分類候補 | 典型例 | 既定route | 現Workへの効果 |
|---|---|---|---|
| `implementation_defect` | 固定Testを満たさないcode | 現Delivery Work Item | Testを変えず修正 |
| `test_or_oracle_defect` | TestがRequirementと異なる | Test revision候補 | 期待の真偽が変わるならpause |
| `contract_defect` | 責任、境界、受入、依存が不正 | Task Contract revision | 関連Workをpause |
| `requirement_defect` | 上流義務の不足、矛盾、実現不能 | Upstream Revision | 影響Workをpause |
| `intent_conflict` | 製品目的、利用者、非目標と競合 | Human authority | scopeを停止 |
| `external_blocker` | Tool、権限、外部system、依存待ち | Dependency／pause | 再開条件まで停止 |
| `process_improvement` | 手順負担、見落とし、復元時間 | checkpoint queue | 原則継続 |
| `product_idea` | 新しい能力、UI、分析 | checkpoint／defer | 原則継続 |

分類は原因の仮説であり、候補を記録した主体が自由に上流不良を確定するものではない。複数候補がある
場合は、断定せず`classification_uncertain`としてHuman triageへ送る。

## 5. 最小Candidate Record

手作業Pilotでは、次を一件の候補として記録する。形式はMarkdown表またはYAMLでよく、正式製品schemaへ
先行昇格しない。

```yaml
candidate_id: IC-...
observed_at: ...
origin:
  stage: ...
  work: ...
  task_contract: ...
  work_item: ...
  source_snapshot: ...
summary: ...
evidence_refs: [...]
classification_candidates: [...]
affected_authority: [...]
acceptance_truth_changed: unknown
safety_or_security_impact: unknown
authority_impact: unknown
provenance_reconstructability_impact: unknown
current_work_can_continue: unknown
suggested_route: ...
route_reason: ...
duplicate_of: null
checkpoint: ...
human_decision: pending
consumer_refs: []
outcome_ref: null
```

必須なのは候補ID、発生元、固定source、要約、Evidence、影響候補、継続可否、提案routeである。
自由文だけの「後で直す」は受け付けない。一方、初期から詳細なcost、全relation、全品質属性を必須にして
記録負担を増やさない。

## 6. 機械的な受付と経路提案

### 6.1 受付検査

機械的に次を検査できる。

- candidate IDの一意性
- origin Stage／Work／Contract／Work Itemの存在
- Source SnapshotとEvidence参照の存在、Digest、freshness
- 必須fieldの欠落
- 同じ対象、分類、Evidence Digestを持つ重複候補
- active Workと候補が指すsource identityの一致
- 既にclosed、rejected、supersededになった候補とのrelation

不足時は候補を削除せず`needs_information`相当として、不足fieldと取得先をtext表示する。

### 6.2 blocking提案

次のいずれかへ影響する可能性がEvidence付きで示された候補は、機械が`pause_and_triage`を提案する。

- safety、security、privacy
- Decision Authorityまたはpermission
- Acceptance Criteriaの真偽
- 必須Provenanceの再構築可能性
- source identity、Test／Verdictの対象一致
- 不可逆または外部side effect
- 現在のWorkflow permitを成立させる必須条件

影響fieldが`unknown`の場合、機械は安全と推測しない。現在Workを止める意味判断はHumanまたは既存の
決定的Policyが行う。表示器、任意metric、表現改善だけの問題を自動blockingにしない。

### 6.3 route決定表

初期のrule tableは次の優先順で提案を生成できる。

```text
intent conflict
  → stop scope / Human decision

requirement defect or acceptance truth change
  → pause / Upstream Revision / stale closure

contract defect
  → pause affected Work / Contract revision / Definition Challenge

test or oracle defect
  → pause TDD / new Test version / acceptance meaning review

implementation defect with fixed valid expectation
  → current Work / keep Test fixed / repair implementation

external blocker
  → dependency record / pause or defer / explicit resume condition

process improvement or product idea
  → checkpoint queue / no current permit effect

insufficient or conflicting classification
  → Human triage / no automatic plan change
```

決定表の出力は`route proposal`であり、Decision Recordではない。Plan、Requirement、Contract、Test、
checklistを自動編集しない。

## 7. 概念上の状態遷移

```text
captured
  → validated
  → triage_required
  → routed
      ├─ current_work
      ├─ revision_proposed
      ├─ checkpoint_queue
      ├─ deferred
      ├─ rejected
      └─ duplicate
  → decided
  → consumed
  → evaluated
  → closed
```

この状態名は検討用であり、初期製品schemaへ固定しない。重要なのは、候補をrouteしただけで閉じず、
次のいずれかへ必ず接続することである。

- 修正したWork ItemとVerification Evidence
- Upstream Revisionと後継Requirement／Contract／Test
- Issue RecordとIssue Resolution Plan
- deferの着手条件とcheckpoint
- reject／duplicateの理由とDecision
- 後続Outcomeと評価

## 8. 既存経路との接続

本候補経路は既存ownerを置き換えない。

```text
Improvement Candidate
  ├─ local implementation defect → current Delivery Work Item
  ├─ upstream defect             → Upstream Revision
  ├─ dependency / blocker        → Dependency Discovery / pause
  ├─ accepted cross-cutting issue→ Issue Resolution Path
  └─ non-blocking idea           → checkpoint / deferred
```

Issue候補へ昇格するのは、独立して追跡する価値、複数Workへの影響、計画challenge、別ownerまたは後続実行が
必要な場合である。局所的な実装不良をすべてIssue化せず、単なるアイデアを自動的に製品Requirementへ
変換しない。

## 9. Human authorityを残す範囲

初期は次をHumanが判断する。

- 意味的な分類の確定
- 現Workをpauseまたは続行する判断
- Requirement、Intent、Architecture Policy、Contract期待の変更
- Issueへの昇格、優先度、scope、defer、reject
- known riskの受入
- 改定後の再開、Stage完了、release

AIは分類候補、反証、route候補、影響閉包、必要Evidenceを提案できる。AIまたは機械が自分の提案を
根拠にPlanを変更し、そのPlanで自分を合格させる循環を許可しない。

## 10. 候補増殖と収束

候補の存在自体を現在Workのblockerにしない。候補は少なくとも次へ分ける。

- `blocking_now`
- `schedule_at_checkpoint`
- `defer_until_evidence`
- `reject`
- `duplicate`

checkpointはWork Item受入後、Stage移行前、release評価前など既存関門へ置き、新しい常設Stageを作らない。
候補数、重複率、未分類期間、blocking誤判定、処理時間を観測し、captureがDeliveryより大きな負担に
なった場合はfield、頻度、対象を減らす。

## 11. 段階的な機械化

### 11.1 手作業Pilot

- Candidate Recordを手作業で作る。
- 分類とroute提案をchecklistの判断材料として記録する。
- Humanがpause、続行、Issue昇格、defer、rejectを判断する。
- 必須field、分類の曖昧さ、重複、処理時間、未消費候補を観測する。

この段階で製品schema、Workflow permit、Plan自動編集を作らない。

### 11.2 development tooling

手作業で反復する決定的検査が明らかになった場合、固定fixtureを持つ小さなvalidatorとして実装できる。

- record completeness
- identity／Digest／source一致
- rule tableによるroute proposal
- duplicate candidate
- missing consumer、stale candidate、checkpoint超過
- Current Work Projectionへのpending／blocking候補表示

toolingは提案と検査に限定し、候補からIssue、Requirement、Plan、permitを自動生成・確定しない。

### 11.3 正式automation

現行計画どおり、Work 8のIssue Resolution手作業Pilotでfield、owner、停止、stale、費用を確認した後、
別Task ContractでHumanが着手を判断する。`REQ-WORKFLOW-010`／`011`の正式化、threat model、negative Test、
rollback、Provenanceを経ずにRuntimeへ昇格しない。

## 12. Current Work Projectionとの接続

現在位置textには、全候補の詳細ではなく次だけを投影する。

- `blocking_now`件数と対象Work
- Human triage待ち
- checkpointで判断する候補件数
- staleになった候補またはroute proposal
- 次に必要な判断またはEvidence取得

TODOへ候補全文を複製せず、candidate IDと次の一作業だけを載せる。表示は候補のauthorityではなく、
Candidate RecordとDecisionへ戻れる派生viewとする。

## 13. 評価

Pilotでは次を測る。

- 候補から分類・routeまでの時間
- 正しいowner／上流層へ届いた割合
- 実装不良を上流改定で通した件数
- blocking候補の見逃しと非blocking候補の誤停止
- duplicate、未分類、未消費、期限超過候補
- 計画改定後のstale閉包漏れ
- Candidate Record作成とreviewの負担
- 採用、defer、reject後のOutcome

自動分類率やIssue数の増加だけを成功指標にしない。Delivery停止時間、誤った基準変更、状況復元時間を
減らし、E2E到達を妨げないことを確認する。

## 14. 代表的な失敗と防止

| 失敗 | 防止 |
|---|---|
| 実装が難しいためRequirementを弱める | 固定Test、分類、Human改定判断 |
| 結果を見て過去Planを書き換える | immutable旧versionとDigest |
| アイデアをすべてIssue／Feature化する | checkpoint、defer、reject、昇格条件 |
| 候補recordを作って放置する | consumer closureとOutcome |
| AIが分類からPlan変更まで確定する | route proposalとHuman authorityの分離 |
| 手作業分類が揺れる | 固定fixture、決定表、uncertain route |
| 自動化自体が開発を止める | Pilot、development tooling、正式automationの分離 |
| TODOやchecklistが第二正本になる | ID／Evidenceへのlinkだけを表示 |

## 15. 現行文書へ反映する場合の最小候補

本メモの確認後、必要なら現行計画とchecklistへ次だけを反映する。

1. 自己適用中のObservationをImprovement Candidateとして固定する入口。
2. candidate分類とblocking／checkpointのroute判断。
3. 改善候補から既存のcurrent Work、Upstream Revision、Issue Resolution、deferへの接続。
4. 機械処理はvalidatorとroute proposalに限定し、計画変更はHuman判断とする境界。
5. Work 8の手作業Pilot後だけ正式automationを検討する順序。

新Feature、独立Stage、正式schema、UI、自動Plan編集は、本メモだけを根拠に追加しない。
