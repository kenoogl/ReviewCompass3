---
evidence_id: RC3-WORK3-SOURCE-IDENTITY-STALE-COMPLETION-2026-08-03-V1
recorded_at: 2026-08-03T18:19:21+09:00
stage: initial-development
work: Work 3
checklist_item: source-change-verification-artifact-identity-and-stale
status: verified
workflow_state: completed
completion_authority: human
confidentiality_class: project-internal
---

# Work 3 Source Identity and Stale Completion Evidence V1

## 1. 結果

Humanが`A1、B1`の`A1`として、監査済みのsource identity／stale候補を明示承認した。Repository Binding、
Source Snapshot、Change Set、Verification Run、Build Artifactの5 entityと、Test、review、Decision、commit、
releaseの5 gateを、ID、stale、復旧、受入、対象外へ接続している。

Work 3の「source、Change Set、Test／CI／Build Artifactのidentityとstale規則」項目を
`verified / completed`とする。

## 2. 固定入力とDecision

| role | artifact | SHA-256／state |
|---|---|---|
| Candidate | `records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json` | `e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc`／approved snapshot |
| Candidate Evidence | `records/development/2026-08-03-work-3-source-identity-stale-evidence-v1.md` | `3d04943d0174c323d9b5f1feb605eb70ff3e4dc3a779e681bf179d810db16812`／verified candidate |
| Human Decision | `records/development/2026-08-03-work-3-source-identity-stale-decision.json` | `1eba4807e9b1e5d5ff4fa38e8617e768c27cfe02c553572d91c86cd67366bae9`／approved and effective |

Decisionは候補と監査EvidenceのDigestへ束縛され、A1の承認対象と除外対象を分離している。

## 3. 完了関門

| check | result |
|---|---|
| identity entity | 5 / 5 |
| target consistency gate | 5 / 5 |
| fixed source Digest | 6 / 6一致 |
| RequirementからReleaseのrelation | 7 / 7段階 |
| 未知参照／Digest不一致 | 0 / 0 |
| initial scope | SCM非依存、read-only local Git、local Verification |
| deferred scope | CI adapter、Build Artifact実装、provider操作 |
| audit | `AUDIT_OK` |

## 4. Authority境界

本DecisionとEvidenceが完了させるのはsource identity／stale規則のchecklist項目だけである。CI adapter、
Build Artifact、CI起動、push、PR、merge queueを実装または実行していない。Requirements／Plan本文、
後続Work 3項目、Work 3全体完了、commit、pushも承認範囲外である。

## 5. 次作業

同じHuman instructionのB1で承認されたRequirements配置規則を完了Evidenceへ接続し、その後、承認済みの
配置へ最小schemaとlegacy binding inventoryを実装する。
