---
evidence_id: RC3-WORK3-REQUIREMENTS-ARTIFACT-RUNTIME-RED-2026-08-03-V1
recorded_at: 2026-08-03T18:27:52+09:00
stage: initial-development
work: Work 3
status: verified_red
workflow_state: active
confidentiality_class: project-internal
---

# Work 3 Requirements Artifact Runtime RED Evidence V1

## 1. 結果

承認済みRequirements配置、最小schema、artifact validator、authority結線、既存37 Requirementのlegacy
binding inventoryについて、正常、負例、境界例を12件のAcceptance Testへ固定した。実装前に実行し、
12件すべてが期待する未実装理由でerrorになった。

## 2. 固定Testとfixture

| artifact | SHA-256 |
|---|---|
| `tests/test_requirements_artifact_layout.py` | `49df58714f901cf83c11594a9ac0f5f77567ac445e3977f81a1c756d9325a6a9` |
| `tests/fixtures/requirements/artifact-layout/valid-artifacts.json` | `8d063195352ac6b376b16cea32fc4bcb7584ac98a52ada83f50979dbb5b4c59c` |

Test sourceは生成物を書かない`compile()`で`compile_ok`を確認した。

## 3. RED

```text
12 errors in 0.07s
ModuleNotFoundError: No module named 'tools.requirements.artifact_layout'
```

12件のerrorはすべてpytest fixtureのmodule import時に発生した。schema、directory、legacy inventoryの
中途半端な実装または既存Testの回帰ではなく、validator moduleがまだ存在しないことだけが原因である。

最初の構文確認では`py_compile`がmacOSのproject外user cacheへbytecodeを書こうとしてsandboxに拒否された。
Test内容の問題ではないため、同じsourceをwriteなしの`compile()`で確認し、RED実行を継続した。

## 4. 実装中の固定境界

- greenになるまで本Testとfixtureの期待を変更しない。
- 外部JSON Schema dependencyを追加せず、承認済みschemaの必要部分を標準ライブラリで検査する。
- 追加13 Requirementのdefinitionは作らない。
- 既存37 Requirementを移動または書換えしない。
- directory名だけでauthorityを成立させない。
