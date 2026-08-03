---
evidence_id: RC3-WORK3-REQUIREMENTS-ARTIFACT-LAYOUT-EVIDENCE-2026-08-03-V1
recorded_at: 2026-08-03T17:49:00+09:00
stage: initial-development
work: Work 3
status: verified_candidate
workflow_state: human_decision_pending
completion_authority: human
confidentiality_class: project-internal
---

# Work 3 Requirements Artifact Layout Candidate Evidence V1

## 1. 結果

追加13 Requirementを構造化する前に、Requirement本体、候補、Human Decision、Evidence、schema、
authority bundleの配置、命名、identity、version、Digest、stale、legacy移行境界をHuman判断候補へ固定した。

候補は、ディレクトリ名だけで正本性を決めない。構造化Requirementが有効になるには、definitionの
ID・version・Digest、candidate manifest、検証Evidence、Human Decision、authority bundleの対象がすべて
一致し、supersede／revokeまたはstaleがないことを要求する。

本成果は配置規則の候補であり、現行Requirements／Plan本文、既存37 Requirementまたは追加13 Requirementを
変更していない。提案したディレクトリもHuman承認前には作成していない。

## 2. 発生した問題と処置

現在は人向け本文が`docs/requirements/`、構造化recordが`records/requirements/`に存在する。しかし、
Requirement本体、候補、Decision、Evidence、schemaの共通配置規則と、どの結線が正本性を成立させるかが
一つの固定sourceにない。

このまま追加13要件を構造化すると、次の問題が起こり得る。

- `approved`または`current`に見えるpathやfilenameを正本と誤認する。
- Humanが確認した候補と、後で利用するRequirement definitionの内容が異なる。
- schema、sourceまたはEvidence変更後も古いDecisionを再利用する。
- 既存37要件と追加13要件のauthorityが混在し、50要件の有効集合を一意に解決できない。

処置として、既存37要件を移動せずlegacy bindingとして維持し、新規構造化要件から適用する配置、命名、
authority解決、stale閉包、将来migrationの規則候補を作成した。

## 3. 候補

| artifact | SHA-256／state |
|---|---|
| `records/development/2026-08-03-work-3-requirements-artifact-layout-candidate-v1.json` | `154a4f40487bc52537e87575d063f0c3e0e72b19fa13d2cdcee0e4fc0339e6ed`／`human_decision_candidate` |

候補は固定source 10件のpathとDigestへ束縛した。全件を再計算し、Digest不一致は0だった。

## 4. 提案する配置

| artifact class | proposed directory | authority上の役割 |
|---|---|---|
| 人向けRequirement source | `docs/requirements/` | source、説明またはprojection。置くだけではnormativeにならない |
| 構造化Requirement definition | `records/requirements/definitions/` | 不変の機械可読Requirement本体。外部Decisionで有効性を解決する |
| candidate manifest | `records/requirements/candidates/` | 判断対象のdefinition ID・version・Digest集合を固定する |
| Decision Record | `records/requirements/decisions/` | candidate・Evidence DigestへのHuman判断を保存する |
| Evidence Record | `records/requirements/evidence/` | validation、review、coverage、post-write結果を保存する |
| Requirement schema | `schemas/requirements/` | record形状と閉じた値の機械正本。Acceptanceの真偽は所有しない |
| authority bundle | `records/requirements/authority/` | 有効なdefinition、Decision、legacy bindingの派生mapを固定する |

filenameはlocatorであり、埋込みIDを正とする。Requirement definitionは
`<requirement-id-lowercase>--v<requirement-version>.json`、schemaは
`<schema-id-lowercase>--v<schema-version>.schema.json`とする。参照済みfileはin-place変更またはrenameせず、
新versionと`supersedes`関係を作る。

## 5. Authority境界

構造化Requirementは次の全条件が揃った場合だけ有効とする。

1. definitionが記録済みschema ID・version・Digestに適合する。
2. candidate manifestがdefinitionのID・version・Digestを列挙する。
3. Humanの`requirements_promotion` DecisionがcandidateとEvidenceのDigestを承認する。
4. authority bundleがdefinition、Decision、既存legacy bindingを競合なく列挙する。
5. 後続のsupersede／revokeがなく、source、schema、Evidenceがstaleでない。

ディレクトリ名、filename、埋込みstatus、Evidenceのpassだけでは承認にならない。同一Requirement ID・versionに
異なるDigestがある場合は`authority_inconsistent`としてpromotionと下流compileを停止する。

## 6. Legacy移行境界

- 既存37 Requirementの本文とrecordは今回移動または書換えしない。
- 既存stage-four Approval、Completion、固定source Digestを`legacy_authority_bindings`として明示参照する。
- 追加13 Requirementは本候補承認と最小schema固定後に初めてdefinition化する。
- 50 Requirementを有効にする前に、既存37 bindingと追加13 definition／Decisionを一つのauthority bundleへ
  列挙する。
- 既存37 Requirementの新形式への移行は、別candidate、検証、Human Decision、stale閉包を必要とする。

## 7. 機械監査

```text
candidate_sha256=154a4f40487bc52537e87575d063f0c3e0e72b19fa13d2cdcee0e4fc0339e6ed
artifact_classes=7 fixed_sources=10 stale_rules=5
LAYOUT_AUTHORITY_AUDIT_OK
```

- artifact class 7件の欠落、重複、余剰は0。
- 各classにdirectory、filename pattern、role、必須identityがある。
- proposed directoryの重複は0。
- authority成立条件6件、非成立条件4件、stale規則5件を確認した。
- legacy migrationの現状維持、binding、追加13、mixed bundle、将来移行の5境界を確認した。
- fixed source 10件のDigest不一致は0。
- candidateは`proposed_only`、承認前の効果は`none`である。

現行配置の観測結果は次のとおりである。

```text
docs_requirement_files=4
record_root_json=14
review_directories=4
proposed_directories=not_created
```

## 8. Authorityと判断対象

- 承認対象は候補Digestに固定した7 artifact class、命名、version、authority解決、stale、legacy移行規則である。
- 承認はディレクトリ作成、schema実装、追加13要件の構造化、既存37要件の移動を含まない。
- 現行identity／stale候補は別のHuman判断対象であり、この候補が黙示的に承認しない。

Human判断候補は次の二択とする。

1. 現行候補を承認し、Work 3の配置・authority規則を`verified / completed`とする。
2. 変更が必要なdirectory、filename、authority、version、staleまたはmigration規則を指定する。
