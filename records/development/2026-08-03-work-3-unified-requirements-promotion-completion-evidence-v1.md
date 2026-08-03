# Work 3 Unified Requirements Promotion Completion Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-UNIFIED-REQUIREMENTS-PROMOTION-COMPLETION-2026-08-03-V1`
- recorded at：`2026-08-03T22:23:30+09:00`
- stage／work：`initial-development / Work 3`
- status：`verified / completed`

## Human Decision

- Human instruction：統一50 Requirement candidateを「承認する」
- Decision：`records/requirements/decisions/dec-requirements-unified-50-2026-08-03-v1.json`
- file SHA-256：`dd8b5dd15197da0a3463b3981d607da6edcb8318e17d91038786de7edc9eff27`
- record digest：`b8cce324d5693a2bf4c8e5b9acb8adbf023f726069407e137faebcaa765442d8`
- class／outcome／authority：`requirements_promotion / approved / human`

承認はcandidate file SHA-256
`c82144375fecc22c088d06d510d9e041fe9c607a0d6e4eb353b034467654ca16`、candidate digest
`cc4ba8f872973f8035b798042f4a5335005394cca339ec6f0121cf16c8c533b4`、Evidence digest
`5b42979ab79699b2da950bae4788f582b023211c5c919571209a7f43bb5492fe`へ束縛した。要件本文、Acceptance truth、
Plan、製品実装、NFR／deferred判断は承認範囲外である。

## Promoted Authority

- authority bundle：`records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json`
- file SHA-256：`760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`
- bundle digest：`79a69d921bb00eb2b321e3d1adb073b88a527eb938398d1813567009255bd688`
- status：`effective`
- definition refs：50
- legacy authority bindings：0
- supersedes：authority bundle v1

同じ生成入力で2回目は`written 0 / unchanged 2`となり、Decisionとauthority bundleの決定的再生成を確認した。
v1とv2のeffective Requirement IDは50件で差分0、旧37件のsemantic field不一致0だった。

## Verification

- RED Evidence：`records/development/2026-08-03-work-3-unified-requirements-promotion-red-evidence-v1.md`
- implementation：`tools/requirements/unified_migration.py`、SHA-256
  `06dd73faced0722a15edcce556d5ad80d02475929c26adcac4edb6c26ed852b5`
- Test：`tests/test_requirements_unified_migration.py`、SHA-256
  `947137c9599eb0cd5a2d42744166f031fd3285de22243ec6dba3642d8ef3a7f4`
- negative RED Evidence：
  `records/development/2026-08-03-work-3-unified-requirements-promotion-negative-red-evidence-v1.md`、SHA-256
  `8e37fbf275e04cf8606817d33933309494e5f8530c8f3e0d1844199241cb84eb`
- GREEN receipt：`records/development/2026-08-03-work-3-unified-requirements-promotion-green-test-receipt-v2.json`
  - SHA-256：`2d01d4b4f9e8c3cd4c8a31a51d87fc9e1d54b3f6206e272c3bdad25f4ef2ed27`
  - result：`470 passed in 2.34s`
  - fallback：`false`
- GREEN receipt v1は負例追加前stateのためstaleな経過記録として保持する。
- independent JSON Schema：`passed artifacts=54`
- authority chain：`effective / requirements=50`

## Stale Closure

- revalidation Evidence：
  `records/development/2026-08-03-work-3-unified-requirements-revalidation-evidence-v1.md`
- SHA-256：`933af699185c27df4a7e4ea80fd15153c5ae9927df4fbdb98e10ae66a8523108`
- NFR候補：既承認内容、authority scope、Acceptance truthの変更0を確認しfreshへ復旧
- deferred候補：新authority v2とcurrent Planへ再検証済み、Human判断待ちを維持

## Result

統一50 Requirement promotionは`verified / completed`である。現行Requirement authorityは50 definitionだけを
持つv2となり、旧v1とlegacy bindingは履歴として保持する。次の一作業は、再検証済みdeferred scope候補に対する
Human判断である。
