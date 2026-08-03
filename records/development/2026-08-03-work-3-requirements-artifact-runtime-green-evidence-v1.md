---
evidence_id: RC3-WORK3-REQUIREMENTS-ARTIFACT-RUNTIME-GREEN-2026-08-03-V1
recorded_at: 2026-08-03T18:34:18+09:00
stage: initial-development
work: Work 3
status: verified_green
workflow_state: completion_candidate
confidentiality_class: project-internal
---

# Work 3 Requirements Artifact Runtime GREEN Evidence V1

## 1. 結果

RED時点のTestとfixtureを変更せず、承認済みRequirements directory、最小artifact schema、標準ライブラリだけを
使うvalidator、authority chain検査、既存37 Requirementのlegacy binding inventoryを実装した。

targeted Testは`12 passed`、既存Requirements関連を含むTestは`71 passed`、全Testは`448 passed`となった。
追加13 Requirement definitionは作成せず、既存37 Requirementも移動または書換えしていない。

## 2. 固定TestとRED

| artifact | SHA-256 |
|---|---|
| `tests/test_requirements_artifact_layout.py` | `49df58714f901cf83c11594a9ac0f5f77567ac445e3977f81a1c756d9325a6a9` |
| `tests/fixtures/requirements/artifact-layout/valid-artifacts.json` | `8d063195352ac6b376b16cea32fc4bcb7584ac98a52ada83f50979dbb5b4c59c` |
| `records/development/2026-08-03-work-3-requirements-artifact-runtime-red-evidence-v1.md` | `9c6ec0d66f3bda56deee59e1a410694dd5c60a0ad2dd30fc68125c6efb97d373` |

REDは`12 errors in 0.07s`で、全件がvalidator module未実装による
`ModuleNotFoundError: tools.requirements.artifact_layout`だった。GREEN後もTestとfixtureのDigestはRED時点と
一致する。

## 3. 実装

| artifact | SHA-256／role |
|---|---|
| `tools/requirements/artifact_layout.py` | `8e96086c9a6cb9aee7d8db87377afffb8a8cd41092aa49967a65b5b9fd350ac2`／schema subset、Digest、locator、authority、legacy validator |
| `schemas/requirements/rc3-requirement-artifacts--v1.schema.json` | `cd8d5f69565b17c9ec2753dadab841ca2dd58cb7f401b3223bea61ef73b035ff`／5 artifact kindと共通refのschema |
| `records/requirements/README.md` | `f88dc4d5595e39377dce8736b12fc5847624078d26250cdc4e1f87463f505e4b`／directoryはauthorityでない旨の入口 |
| `records/requirements/authority/rc3-legacy-requirements-37--v1.json` | `8daec571041b8a70dab3055922b05fab58be49f270ad63438397dfda47a0e792`／既存37 ID、6 sourceのbinding |

`definitions/`、`candidates/`、`decisions/`、`evidence/`、`authority/`、`schemas/requirements/`を承認済みpathへ
用意した。空の将来配置には`.gitkeep`だけを置き、承認済みRequirementが存在するとは表示しない。

## 4. Verification

```text
targeted: 12 passed in 0.02s
Requirements related: 71 passed in 0.11s
full: 448 passed in 2.04s
independent JSON Schema: INDEPENDENT_JSON_SCHEMA_OK artifacts=6
compile: compile_ok
JSON reload: passed
git diff --check: passed
```

独立oracleとして環境のDraft 2020-12 validatorでschema自体を検査し、definition、candidate、Decision、
Evidence、authority bundle、legacy inventoryの6 artifactを再検証した。

## 5. 初回GREEN試行で検出した不一致

最初の実装後Testは`10 passed, 2 failed`だった。

- READMEの`Directory`が大文字で、固定した非authority表示文と一致しなかった。
- 共通artifact refのID patternがRequirement record IDの`@v1`に含まれる小文字`v`を許可していなかった。

Testとfixtureは変更せず、READMEを固定句へ合わせ、schemaでversion suffixの小文字`v`だけを明示許可した。
再実行後は`12 passed`となり、独立JSON Schema検査にも合格した。

## 6. Negative／boundary coverage

- 必須statement欠落、unknown field、self Digest不一致を拒否する。
- Requirement IDとversionから導くrecord ID不一致を拒否する。
- 承認済み命名と違うlocatorを拒否する。
- directoryまたはdefinition単独ではauthorityを成立させない。
- candidate／Evidence／Decision Digestのstaleな結線を拒否する。
- 同じRequirement ID・versionの異なるDigestを拒否する。
- legacy sourceの実Digest変更、37 IDの欠落・重複、Human source未収録を拒否する。

## 7. Authorityと未実施

本実装は追加13 Requirementを安全に構造化する入口であり、追加13 Requirement自体のdefinition、candidate、
Decision、Evidence、50 Requirement authority bundleは未作成である。既存37 Requirementはlegacy bindingの
参照対象であり、内容と既存pathを変更していない。Work 3後続項目、Work 3全体完了、commit、pushも
本Evidenceだけでは完了しない。
