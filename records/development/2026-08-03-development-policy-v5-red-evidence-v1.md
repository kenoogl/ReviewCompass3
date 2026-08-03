# Development Policy V5 RED Evidence V1

## Identity

- Evidence ID：`RC3-DEVELOPMENT-POLICY-V5-RED-2026-08-03-V1`
- scope：LLM／machine責務境界、手作業由来の手戻り報告
- status：`verified / red`

## Fixed Test

- path：`tests/test_development_policy.py`
- SHA-256：`2920252103af27ef905269de38ccab554cce7e51bf111d28f51371deb10b453a`

## Machine Receipt

- temporary receipt SHA-256：`fc61d05fdef1a4232f6fd5f8270f27a6843ec6b0caebe6206ec079e091d0ebfe`
- command：policy Test runner full suite
- result：`5 failed, 462 passed in 2.33s`

新規5件は全件`tools.development.policy.evaluate_operation`未実装だけを理由に失敗した。既存462件はgreenで、
既存機能の偶発的な失敗をREDへ混入していない。
