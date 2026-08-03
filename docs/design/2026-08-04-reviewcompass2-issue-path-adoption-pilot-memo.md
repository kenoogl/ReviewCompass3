---
lifecycle: approved_pilot_not_started
normative_status: non-normative-pilot-design
promotion_required: true
implementation_status: human_hold
related_plan: ../current/reviewcompass3-plan-current.md
fixed_predecessor_evidence: ../../records/sources/2026-08-02-reviewcompass2-issue-plan-path.md
approval_record: ../../records/development/2026-08-04-reviewcompass2-issue-path-early-pilot-decision.json
---

# ReviewCompass2 Issue→Plan経路のReviewCompass3早期採用Pilotメモ

## 1. 目的

ReviewCompass2で運用したIssue→Plan経路を、ReviewCompass3の開発中に見つかった手戻り候補の耐久保存と
TODO縮小へ限定して早期Pilotする。ReviewCompass2の運用をそのまま複製せず、ReviewCompass3で既に定めた
Issue Record、Triage Decision、Issue Resolution Plan、Plan Challenge、Task Contract／Work Item、
Resolution Verdictのidentity分離へ合わせる。

本メモはPilotの実装方法を定める非規範設計である。早期PilotのHuman承認は別Decisionへ記録する。
製品Requirement、正式schema、Workflow permit、UI、外部trackerを確定するauthorityは持たない。

## 2. 固定source

| role | artifact | SHA-256 |
|---|---|---|
| predecessor Evidence | `records/sources/2026-08-02-reviewcompass2-issue-plan-path.md` | `d28234ca17b2f2308bad9a63ed551f21caf4b3e4527416f4627bf05d1b5a84f7` |
| current Plan | `docs/current/reviewcompass3-plan-current.md` | `911d0c49d1646f308a733e45d0af6071cd7206dd80b31e123369e921b0b490db` |
| current Glossary | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` |
| improvement routing memo | `docs/design/2026-08-03-self-application-improvement-routing-memo.md` | `0ee336ac2da20e78df00cc096eceb9dc4907a096835f7e579050072478b5d14f` |
| development policy | `docs/development/2026-08-02-development-policy.md` | `444898d51e1190458de000fbc3d6499a5bacee5dce2353a07e723e1b4546dc5e` |

前身Evidenceは固定commit、Git blob、Digestに基づく観測記録であり、本Pilotの採用判断を理由に書き換えない。
ReviewCompass3での追加判断、修正、実測は本メモ、Decision、Pilot artifact、Evidenceへ分離する。

## 3. 採用する経路

```text
Observed problem / rework
  → Improvement Candidate
  → Human Triage Decision
  → Issue Record
  → Issue Resolution Plan
  → Plan Challenge
  → Task Contract／Delivery Work Item
  → Verification Evidence
  → Resolution Verdict
```

- Observationは発生事実、Improvement Candidateは未裁定候補、Issue RecordはHumanが独立追跡を採用した
  問題として区別する。
- Issueを起票しただけでPlan、Task Contract、Work Itemまたは開始permitを生成しない。
- Plan Challengeのblocking Findingが残る間は実装へ進まない。
- Plan承認、green Test、commitまたはWork Item完了だけでIssueをclosedにしない。固定Acceptance Evidenceへ
  Resolution Verdictを接続して閉じる。
- TODOはIssueのauthorityにせず、現在作業に影響するIssue ID、状態projection、次の操作だけを表示する。

## 4. ReviewCompass2から修正して採用する点

### 4.1 状態をIssue本文へ上書きしない

ReviewCompass2の`status: open | completed`を一つのYAMLへ上書きする方式は採用しない。Issue Record、
Triage Decision、Resolution Plan、Work Item、Resolution Verdictを別identityとversionで保持し、現在状態は
有効なrecordとeventから機械導出する。旧versionと却下Decisionを消さない。

### 4.2 Issue本文をEvidence倉庫にしない

Issue Recordへ保持するのは問題、動機、発生元、Evidence参照、影響、scope、non-scope、関係、owner候補、
route候補に限定する。調査全文、会話逐語録、Test出力、実装diff、Decision本文を追記せず、別artifactの
identityとDigestを参照する。

### 4.3 laneを二軸へ分解する

ReviewCompass2の`sdd | maintenance | reopen`をそのまま移植しない。ReviewCompass3の
`work_origin: new_development | maintenance`と`continuation_mode: fresh | reopen`へ分ける。Issue分類、
上流改定、実行方法を一つのlane値へ畳み込まない。

### 4.4 IssueとPlan bundleを分ける

Issue Resolution Planは意味的な対処と作業分解を所有する。Task Contractから決定的にcompileされる6つの
Plan bundleとは別identityである。Issue Resolution PlanからTask Contractへrouteするとき、scope、non-scope、
禁止事項、expected outcome、oracle、rollbackが失われていないことをPlan Challengeで確認する。

### 4.5 全手戻りをIssue化しない

同じ作業内で恒久対策とVerificationまで完了した局所的手戻りはCompletion Evidenceへ残す。未解決、再発、
複数Workへの影響、別owner、独立Plan、後続実行が必要な候補だけをHuman判断でIssueへ昇格する。

## 5. 早期Pilotの位置付け

現行Planは正式なIssue Resolution schemaとautomationをWork 8の手作業Pilot後へdeferしている。本Pilotは
その正式化を前倒ししない。TODO巨大化という実在問題に一件だけ適用するdevelopment-process bootstrapである。

早期実施によって変更するのはPilotの観測時期だけである。次は変更しない。

- `REQ-WORKFLOW-010`／`011`は要件候補のまま維持する。
- 製品schema、正式state machine、Workflow permit、UI、外部tracker同期を実装しない。
- Work 8で行う正式Pilot、評価、Requirement昇格判断を代替しない。
- 現行Work 4の製品DesignをIssue Pilotへ吸収しない。

## 6. Pilot artifactの暫定配置

実装開始が明示された後、次のdevelopment専用rootを候補とする。

```text
records/development/issue-resolution-pilot/
  issue-records/
  triage-decisions/
  resolution-plans/
  plan-challenges/
  resolution-verdicts/
  evidence/
```

この配置は製品Runtimeまたは正式Issue authorityではない。`records/issues/`または
`.reviewcompass/backlog/issues/`を先行作成せず、Pilot後にfield、分量、参照、state導出、運用費用を評価して
正式配置をHuman判断する。

## 7. Pilot artifactの最小形状

### Issue Record

- `issue_id`、`version`、`created_at`
- `problem`、`motivation`
- `source_work`、`source_identity`、`evidence_refs`
- `impact`、`scope`、`non_scope`
- `related_files`、`related_units`
- `owner_candidate`、`route_candidate`
- content Digest

mutableな`current_status`、実装手順全文、解決済み宣言は持たない。

### Triage Decision

- candidateとIssue identity
- `promote | current_work | upstream_revision | dependency | checkpoint | defer | reject | duplicate`
- blocking判定、理由、Human actor、決定時刻
- 選択したconsumerと次の操作

### Issue Resolution Plan

- 対象Issue versionとDigest
- scope、non-scope、禁止事項
- 作業項目、依存、expected outcome
- Acceptance、oracle、Test、review
- risk、deployment、rollback、recovery
- Task Contract／Work Item route候補

### Plan Challenge

- Issue obligation coverage
- 作業粒度と単独判定可能性
- TDD closure
- 禁止事項とnon-scopeの移送
- 実現可能性、依存、oracle
- blocking Findingとstale binding

### Resolution Verdict

- Issue、Plan、Task Contract／Work Item identity
- Acceptance Evidenceと固定Digest
- side effect、未処理、残余risk
- `resolved | unresolved | partially_resolved | superseded | duplicate`
- Human判断が必要な終了class

## 8. 最初の一件

最初のIssue候補は、ルート`TODO_NEXT_SESSION.md`へ過去sessionのClaimと手戻り履歴を累積し、現行handoffが
669行、約61 KB、詳細Claim 94件になった問題とする。

Pilot実装時の範囲は次に限定する。

1. 巨大化の観測Evidenceと固定TODO Digestを作る。
2. Improvement CandidateとHuman Triage DecisionをIssue Recordへ接続する。
3. 現行TODOを一度だけmilestone snapshotへ保存するPlanを作る。
4. root TODOを現在位置、最新Evidence、active work、blocker、Human判断、次の一作業、最新Test、
   現在作業に影響するIssue IDへ縮小する。
5. TODOの容量、Claim数、解決済み手戻り残留、Issue参照を検査するvalidator拡張をPlanへ含める。
6. 短い共通TODO更新promptをCodex／Claudeのrepository instructionから参照する。
7. Plan Challenge後に実装し、Resolution Verdictで縮小と再発防止を確認する。

他の過去手戻り候補を一括Issue化しない。最初の一件を閉じ、記録費用とfield不足を評価してから次を判断する。

## 9. TODOとの境界

TODOへIssue本文、全Decision、全Evidence、解決済みIssue履歴を複製しない。表示候補は次に限定する。

```markdown
## 現在作業に影響するIssue

- `<issue_id>`：`<derived state>`、次：`<one action>`
```

現在作業に影響するopen Issueがなければ`なし`とする。Issue総数、open／closed件数、全backlog一覧は
machine projectionまたは専用inventoryから取得し、root TODOへ固定しない。

## 10. LLMと機械処理

LLMは問題、動機、scope、non-scope、Plan、Challenge Finding、Verdict理由の文章化と意味分析を担う。
machineはID、version、Digest、必須field、参照、重複候補、状態導出、stale、件数、TODO上限、Issue参照、
post-write再読込を担う。machineまたはLLMはHumanのIssue昇格、blocking裁定、Plan承認、Resolution Verdictを
代行しない。

## 11. Acceptanceと評価

Pilotは少なくとも次をEvidenceで評価する。

- 前身Evidenceを変更せずReviewCompass3のPilot artifactへ結線できた。
- Issue、Decision、Plan、Challenge、Work、Verdictのidentityが混ざらない。
- TODOから過去Claimと解決済み手戻り詳細を除いてもEvidenceへ到達できる。
- Plan Challengeが粒度不足、Acceptance欠落、禁止事項脱落を検出できる。
- Issue昇格からVerdictまでの時間、記録byte数、Human判断数、手戻り数を計測できる。
- TODO validatorが正常例、負例、境界例で累積再発を検出する。
- Work 8正式Pilotで維持、修正、破棄すべきfieldを列挙できる。

## 12. 停止条件

- Pilot artifactが製品正本または正式Requirementのように扱われる。
- Issue作成だけでPlanまたは実装開始permitが発生する。
- Human判断なしに改善候補がIssueへ昇格する。
- predecessor Evidence、現行Plan、Requirement、TestをPilot都合でin-place変更する。
- TODO削減時に唯一のEvidenceまたは未解決義務が失われる。
- Plan Challenge前にTODO削減またはvalidator実装へ着手する。

## 13. 実装順序

明示的な再開指示後に次の順で進める。

1. Task ContractとPilot固定sourceを作る。
2. artifact配置、最小field、命名、version、Digest規則をDecision候補へ固定する。
3. 正常、負例、境界fixtureを先に作る。
4. 最初のIssue RecordとTriage Decisionを作る。
5. Issue Resolution Planを作り、独立Plan Challengeを通す。
6. milestone snapshot、TODO縮小、prompt、validatorを実装する。
7. post-write verificationとResolution Verdictを作る。
8. Pilot評価をWork 8の正式判断材料へ接続する。

## 14. 現在の実施状態

- 早期Pilotの設計方向：Human承認済み。別Decisionへ固定する。
- 実装開始：保留。Humanの明示的な再開指示が必要。
- Pilot directory、schema、Issue Record、Plan、validator拡張、TODO縮小：未実施。
- commit、push：未実施。
