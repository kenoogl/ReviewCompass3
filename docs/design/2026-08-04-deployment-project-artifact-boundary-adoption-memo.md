---
lifecycle: approved_corrective_in_progress
normative_status: non-normative-adopted-design
implementation_status: boundary_recording_started
related_layout_baseline: ../../records/development/2026-08-03-layout-baseline-v1.json
approval_record: ../../records/development/2026-08-04-deployment-project-artifact-boundary-decision.json
---

# デプロイパッケージとProject Artifact境界の採用メモ

## 1. 目的

ReviewCompass3のIssue Resolution早期Pilotより先に、交換可能なデプロイパッケージと、移動させない
Project Artifactの境界を固定する。詳細設計が後から判明するたびにIssue、Plan、Decision、Evidenceを
別directoryへ移す運用を避け、デプロイ時の大規模migrationを通常の解決手段にしない。

本メモはHumanが2026-08-04に承認した設計方向を記録する。現行Layout Baseline v1をin-place変更せず、
後続のv2候補、Test、再検証、Human承認へ渡す。Work 7A／7Bのinstall、更新、rollback全体を前倒しして
実装するものではない。

## 2. 判断に用いた固定source

| role | artifact | SHA-256 |
|---|---|---|
| predecessor deployment observation | `records/sources/2026-08-04-predecessor-deployment-package-observation.md` | `8ebd0bc13be4c6175cafc651d2950e7445267c8093756a6d398ea1963db800c2` |
| deployment topology discussion | `records/sources/2026-08-02-deployment-topology-discussion.md` | `95209eadae62ec80ef98cd23182266d657540576f6f542fdbc136f3c5d01c67b` |
| current Layout Baseline v1 | `records/development/2026-08-03-layout-baseline-v1.json` | `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2` |
| Work 1A Evidence v1 | `records/development/2026-08-03-work-1a-layout-evidence-v1.md` | `5d54c7de759388ae81c1fefebcc50c817c0b38ae2bcdc65444f47aa48cc8e899` |
| approved early Pilot memo | `docs/design/2026-08-04-reviewcompass2-issue-path-adoption-pilot-memo.md` | `e0a1a140ad76a06c00e08244314a00d866e92efb0a377773358c00d5c0f4f4ef` |
| TODO routing revision memo | `docs/design/2026-08-04-todo-rework-candidate-routing-revision-memo.md` | `e156a3b055b19b70bfb9bbe77d1af444ee30ecfcfbf47a7d436096dddcb571b3` |

固定済みの先行PilotメモとDecisionは書き換えない。本メモと後続Decisionで、先行Pilotメモ6節の
development専用暫定配置を、artifact作成前に置き換える。

## 3. 問題

現行Layout Baselineはcode、project、runtime data、state、log、cache、sensitive、evaluationの境界を
固定しているが、Issue、Plan、Triage／Approval Decision、Challenge、Verdictの恒久的な上位rootを
Project Manifestへ持っていない。

先行Pilotメモは`records/development/issue-resolution-pilot/`を暫定配置としていた。この場所へ実recordを
作ってから製品向け`.reviewcompass/`へ移すと、次が必要になる。

- file移動と参照の書換え
- ID、version、Digest、Decision bindingの再照合
- 古い配置と新しい配置を読む期間の二重処理
- rollbackとstale閉包
- migration tool自体の正しさを保証する追加Evidence

機械処理にしても、移動対象と参照が増えれば作業量と検証範囲は大きい。したがって、詳細schemaが未確定でも、
動かさない上位境界だけはPilot前に決める。

## 4. 採用する配置モデル

```text
development source checkout
  │
  │ Deployment Manifest allowlistからbuild
  ▼
version付きstable deployment package
  │
  │ Integration Manifest／Project Bindingで接続
  ▼
target project checkout
  └─ .reviewcompass/
       └─ workflow/                  ← 移動させないProject Artifact root
            ├─ improvement-candidates/
            ├─ issues/
            ├─ triage-decisions/
            ├─ resolution-plans/
            ├─ plan-challenges/
            ├─ resolution-verdicts/
            └─ evidence/             ← Evidence本体または耐久参照

project外logical roots
  ├─ data_root
  ├─ state_root
  ├─ log_root
  ├─ cache_root
  ├─ sensitive_root
  └─ evaluation_root
```

固定するProject Manifest上の単位は`workflow` artifact rootとする。下位のrecord kindが増えても
`artifact_roots`を増殖させず、既存recordを移動しない。下位directory名と正式schemaはPilotで検証するが、
既に作成したrecord kindを別kindへ改名して移動することは通常変更として認めない。

## 5. 配布パッケージの規則

- Deployment Manifestはallowlistとする。
- packageに含めるのは、確認済みcode、schema、template、prompt、規律、設定既定値など、再生成可能な
  配布物だけとする。
- 対象projectの`.reviewcompass/workflow/`、runtime data、state、log、cache、sensitive、evaluationを
  packageへ含めない。
- stable packageはSource Snapshot、build Run、Verification、version、Digestへ束縛する。
- 更新は新packageをstagingして検証後に参照を原子的に切り替える。旧packageはrollback可能期間だけ保持する。
- packageの更新または削除はProject Artifactの移動、書換えまたは削除を要求しない。

## 6. Project Artifactの不変条件

### 6.1 IssueからPlanへfileを移動しない

Issue RecordとIssue Resolution Planは別identityである。IssueをPlanへ変換または移動せず、新しいPlanを作り、
対象IssueのID、version、Digestを参照する。Triage Decision、Plan Challenge、Resolution Verdictも別recordとする。

### 6.2 関係はpathだけに依存させない

record間の結線は少なくともID、version、content Digest、relation kindを持つ。directory名は探索補助であり、
正本性、承認対象またはstale判定をdirectory名だけから決めない。

### 6.3 一覧と分類変更はprojectionで扱う

open Issue一覧、kind別一覧、現在状態、TODO表示はrecordとeventから機械生成する。分類方法が変わった場合は
indexまたはprojectionを再生成し、canonical recordを並べ替えない。

### 6.4 migrationを例外にする

通常のpackage更新、分類変更、index変更ではProject Artifact migrationを行わない。schemaまたは保存形式の
変更でsemantic migrationが避けられない場合だけ、次を満たす独立Workとする。

- Human承認
- 旧readerまたはrollback経路
- dry-runと影響閉包
- source／target Digest照合
- 全参照とDecision bindingの再検証
- 旧配置を消す前の復旧Evidence

## 7. 自己適用

ReviewCompass3 repository自身をtarget projectとして扱うことはできる。ただし、development source checkoutを
stable deploymentとして直接使わない。承認済みsnapshotからstable packageを生成し、development package、
state、dataと分離する。

stable側は共有Project Artifactをread-onlyで参照し、development candidateがstableのstateまたはdataへ
cross-writeすることを拒否する。development candidate自身だけでstable昇格を裁定しない。

## 8. 既存Layout Baselineへの影響

Layout Baseline v1とWork 1A Evidence v1は、当時の検証済み履歴として保持する。本メモだけでは現行baselineを
切り替えない。後続でv2候補を新規作成し、少なくとも次を追加する。

- Project Manifestの`artifact_roots.workflow`
- `canonical_project_artifact_move: prohibited`
- `deployment_package_replaceable: true`
- `runtime_projection_rebuildable: true`
- `semantic_data_migration: exceptional_human_approved`
- package、project、runtime dataの非重複検査

v2候補を採用する場合は、validatorまたは入力前提の変更としてv1の現行合格をstaleにし、正常例、負例、
境界例と独立oracleを再実行する。v1 recordまたはEvidenceをin-place更新しない。

## 9. Test-firstで固定するAcceptance

1. Manifest allowlistからpackageを構築できる。
2. `.reviewcompass/workflow/`またはproject固有recordがpackageへ混入すると拒否する。
3. package versionを切り替えてもIssue、Plan、Decision、EvidenceのpathとDigestが変わらない。
4. Issue作成後にPlanを追加してもIssue fileを移動または書換えない。
5. target project checkoutを移動した場合、Project IDを保ちBindingだけを更新できる。
6. stableとdevelopmentのcode、state、dataが分離され、cross-writeを拒否する。
7. indexとTODO projectionを削除してもcanonical recordから再生成できる。
8. package切替失敗時に旧packageへ戻り、Project Artifactへ副作用を残さない。

最初にfixtureと失敗するTestを固定し、その後にLayout validatorとpackage boundaryの最小実装を行う。

## 10. Issue Resolution早期Pilotへの補正

- 先行Pilotメモ6節の`records/development/issue-resolution-pilot/`は、artifact未作成のまま採用を取り消す。
- 設計メモ、Decision、Test Evidenceは引き続き`docs/design/`と`records/development/`へ置く。
- 実際のImprovement Candidate、Issue、Plan、Challenge、Verdictは、v2 Layout候補とTestが承認されるまで
  作成しない。
- Pilot recordの作成先はProject Artifact root `.reviewcompass/workflow/`とする。
- Pilotで正式製品schemaやWorkflow permitを確定しないという既存のscope制限は維持する。

## 11. 対応順序

1. 前身実装の観測記録を固定する。`完了`
2. 本採用メモとHuman Decisionを固定する。`進行中`
3. Layout Baseline v2候補にworkflow rootと不変条件を追加する。`未実施`
4. 正常、負例、境界fixtureとRED Testを作る。`未実施`
5. validatorの最小変更でTestをgreenにする。`未実施`
6. v2候補を再検証し、Human承認を得る。`未実施`
7. 早期Pilotの最初のImprovement CandidateとTriage Decisionを作る。`未実施`
8. package生成、原子的切替、rollbackの製品実装をWork 7A／7Bへ接続する。`未実施`

## 12. 現在の停止点

本メモ作成時点では、Project Artifact directory、schema、package builder、migration toolを作っていない。
次の実装単位はLayout Baseline v2候補と、その期待を固定するTestである。
