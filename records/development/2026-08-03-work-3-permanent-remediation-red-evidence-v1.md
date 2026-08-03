# Work 3 Permanent Remediation RED Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-PERMANENT-REMEDIATION-RED-2026-08-03-V1`
- recorded at：`2026-08-03T21:26:33+09:00`
- scope：Requirement格納形式の機械統一、policy準拠Test runner
- status：`verified / red`

## Fixed Tests

- `tests/test_requirements_artifact_layout.py`
  - SHA-256：`775f7f0caa6ecabf4537be8a369f8d3bd0337d3bf8e4b3e9fe0e09d8c0076775`
- `tests/test_requirements_unified_migration.py`
  - SHA-256：`54095cfd3be1103ace5c4fc210140b2ece449b30d6a0f35ef7a6579f658b3775`
- `tests/test_policy_test_runner.py`
  - SHA-256：`f46fec7dd348e1dab4f5970e4b3ef533e8949deb8b7de0b80f017082bc79a6f4`

## Command and Result

```text
python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py tests/test_policy_test_runner.py
```

結果：`2 failed, 12 passed, 8 errors in 0.09s`

- mixed authorityの共通reader 2件は`resolve_effective_requirement_ids`未実装で失敗した。
- Requirement機械移行4件は`tools.requirements.unified_migration`未実装でerrorとなった。
- policy Test runner 4件は`tools.development.policy_test_runner`未実装でerrorとなった。

## RED Validity

失敗理由は、固定した新しい振る舞いが未実装であることに限定される。既存12 Testはgreenであり、既存機能の
偶発的な失敗を新規REDへ混入していない。以後、上記3 Test fileを変更せず実装を進める。
