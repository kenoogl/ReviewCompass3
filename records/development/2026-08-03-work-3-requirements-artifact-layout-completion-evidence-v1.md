---
evidence_id: RC3-WORK3-REQUIREMENTS-ARTIFACT-LAYOUT-COMPLETION-2026-08-03-V1
recorded_at: 2026-08-03T18:19:21+09:00
stage: initial-development
work: Work 3
checklist_item: requirements-artifact-placement-naming-and-authority
status: verified
workflow_state: completed
completion_authority: human
confidentiality_class: project-internal
---

# Work 3 Requirements Artifact Layout Completion Evidence V1

## 1. 結果

Humanが`A1、B1`の`B1`として、監査済みのRequirements配置・authority候補を明示承認した。人向けsource、
構造化definition、candidate manifest、Decision、Evidence、schema、authority bundleの7 artifact classと、
filename、ID、version、Digest、Decision、stale、legacy migrationの規則を固定している。

Work 3の「Requirement本体、候補、Decision、Evidence、schemaの配置、命名、authority結線」項目を
`verified / completed`とする。

## 2. 固定入力とDecision

| role | artifact | SHA-256／state |
|---|---|---|
| Candidate | `records/development/2026-08-03-work-3-requirements-artifact-layout-candidate-v1.json` | `154a4f40487bc52537e87575d063f0c3e0e72b19fa13d2cdcee0e4fc0339e6ed`／approved snapshot |
| Candidate Evidence | `records/development/2026-08-03-work-3-requirements-artifact-layout-evidence-v1.md` | `25c7a61e99f04b78ab2732ef70bf507ec161f859085238579f6d0fcb09285871`／verified candidate |
| Human Decision | `records/development/2026-08-03-work-3-requirements-artifact-layout-decision.json` | `516caf5214bd9bfe840d96a7f1249593c2844da26b511432a8cee12ff91e336e`／approved and effective |

Decisionは候補と監査EvidenceのDigestへ束縛され、B1の承認対象と除外対象を分離している。

## 3. 完了関門

| check | result |
|---|---|
| artifact class | 7 / 7 |
| fixed source Digest | 10 / 10一致 |
| stale rule | 5 / 5 |
| legacy migration boundary | 5 / 5 |
| directory重複／Digest不一致 | 0 / 0 |
| authority成立 | definition、candidate、Evidence、Human Decision、authority bundleの対象一致が必須 |
| path単独のauthority | 禁止 |
| audit | `LAYOUT_AUTHORITY_AUDIT_OK` |

## 4. 承認した配置

| role | directory |
|---|---|
| 人向けsource | `docs/requirements/` |
| 構造化definition | `records/requirements/definitions/` |
| candidate manifest | `records/requirements/candidates/` |
| Decision | `records/requirements/decisions/` |
| Evidence | `records/requirements/evidence/` |
| schema | `schemas/requirements/` |
| authority bundle | `records/requirements/authority/` |

## 5. Authority境界

本DecisionとEvidenceが完了させるのは配置、命名、authority規則の確定だけである。提案directoryとschemaは
まだ作成していない。追加13 Requirementは構造化または承認しておらず、既存37 Requirementも移動または
書換えしていない。50 Requirement authority bundle、現行Plan改定、後続Work 3項目、Work 3全体完了、
commit、pushも承認範囲外である。

## 6. 次作業

承認済み配置に必要なdirectory、最小Requirement schema、validator／fixture、既存37 Requirementの
legacy binding inventoryをtest-firstで作成し、追加13 Requirement構造化の開始関門を満たす。
