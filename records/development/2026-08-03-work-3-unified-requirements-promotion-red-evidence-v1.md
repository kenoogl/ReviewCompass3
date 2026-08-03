# Work 3 Unified Requirements Promotion RED Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-UNIFIED-REQUIREMENTS-PROMOTION-RED-2026-08-03-V1`
- recorded at：`2026-08-03T22:11:33+09:00`
- stage／work：`initial-development / Work 3`
- status：`verified / expected_red`

## Human Decision Boundary

Humanは、file SHA-256
`c82144375fecc22c088d06d510d9e041fe9c607a0d6e4eb353b034467654ca16`、candidate digest
`cc4ba8f872973f8035b798042f4a5335005394cca339ec6f0121cf16c8c533b4`、Evidence digest
`5b42979ab79699b2da950bae4788f582b023211c5c919571209a7f43bb5492fe`の統一50 Requirement candidateを
「承認する」と判断した。

## Fixed Test

- Test：`tests/test_requirements_unified_migration.py`
- Test SHA-256：`380825fb26a4410816dbc9aa5d43273d1fc500f8313d9484cd60d82c5687915a`
- 期待：exact candidate／Evidenceに束縛したHuman Decisionと、50 `definition_refs`だけを持つauthority
  bundle v2を決定的に生成し、同じ入力で再生成差分0になる。

## RED Result

- command：`python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt <temporary-receipt>`
- temporary receipt SHA-256：`4a478c9f712bde4b7db1199f9fa6c71d44d84ac3d3aa513464e4f41c32571ce3`
- source state digest：`388d703b65e5d592f71d6b0e6d01ad881972b8098c8444f1c32bb142d67e965c`
- result：`1 failed, 467 passed in 2.31s`
- failure：`AttributeError: module 'tools.requirements.unified_migration' has no attribute 'build_approved_promotion'`

既存467件はgreenであり、新規1件だけがpromotion生成機能の未実装を理由に失敗した。Human Decision、
authority bundle v2、既存Requirement本文はRED時点では未作成・未変更だった。
