# Work 3 Unified Requirements Promotion Negative RED Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-UNIFIED-REQUIREMENTS-PROMOTION-NEGATIVE-RED-2026-08-03-V1`
- recorded at：`2026-08-03T22:20:08+09:00`
- stage／work：`initial-development / Work 3`
- status：`verified / expected_red`

## Risk Boundary

authority昇格では、schema-validでも`result=failed`のEvidence、または別candidate Digestを指すEvidenceを
Human Decisionへ束縛してはならない。正常系実装後のpost-write reviewでこの負例を追加した。

## RED Result

- Test：`tests/test_requirements_unified_migration.py`
- Test SHA-256：`947137c9599eb0cd5a2d42744166f031fd3285de22243ec6dba3642d8ef3a7f4`
- command：`python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt <temporary-receipt>`
- temporary receipt SHA-256：`723244130a14e7c2e789b39570c832d0542d5bac76d8d8b15b44a0f1bb1d71a3`
- source state digest：`08047f125f83c4cbcd9c33a0ad2b8e98b48d6b4c49e951f55ad893a6774b2050`
- result：`2 failed, 468 passed in 2.38s`
- failure：2件とも`Failed: DID NOT RAISE RequirementMigrationError`

既存468件はgreenであり、新規負例2件だけがEvidence resultとcandidate bindingの拒否条件未実装を理由に失敗した。
実装では、`result=passed`とexact candidate ID、version、path、Digestの一致をpromotion前の必須関門にした。
