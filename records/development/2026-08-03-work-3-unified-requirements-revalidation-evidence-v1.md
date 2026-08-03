# Work 3 Unified Requirements Revalidation Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-UNIFIED-REQUIREMENTS-REVALIDATION-2026-08-03-V1`
- recorded at：`2026-08-03T22:16:10+09:00`
- stage／work：`initial-development / Work 3`
- status：`verified / passed`

## Current Authority

- authority bundle v2：`records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json`
  - file SHA-256：`760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`
  - bundle digest：`79a69d921bb00eb2b321e3d1adb073b88a527eb938398d1813567009255bd688`
  - status：`effective`
  - definition refs：50
  - legacy authority bindings：0
- superseded authority bundle v1：file SHA-256
  `fc6d945a6bef1ebea0c4ef22705d70fac6177a8c561be0f992ca94474a8a7509`、bundle digest
  `497bcc4374e3224acbfbb08e38c7d9f3d4e5373f59df505179b6a19bc035a02c`

v1とv2を同じmachine readerで解決し、effective Requirement IDは双方50件、差分0、重複0だった。旧37件は
9 semantic field不一致0、`acceptance_truth_changed=true` 0件であり、追加13件は既承認definitionを変更していない。

## Plan Identity

- current Plan：`docs/current/reviewcompass3-plan-current.md`
- current SHA-256：`911d0c49d1646f308a733e45d0af6071cd7206dd80b31e123369e921b0b490db`
- prior comparison target：commit `f9adef4`の同Plan
- body comparison：`unchanged`

Plan差分はfrontmatterのdevelopment policy参照をv5へ更新した部分だけであり、NFR Profile、deferred scope、
Work 3〜releaseに関係する本文はbyte一致した。

## NFR Candidate Revalidation

- candidate SHA-256：`08d5159a483d16507c5652857e5245993b42559ed3bcc24c9434e70b0d5c2381`
- candidate digest：`c93f9336790fc8641f3f89687f94fcff3baa23254936545ed9cb85c15c25d3a6`
- prior Human Decision SHA-256：`6cdb1f74c8b92bcc7257bf8087158f78e8c980428d1b0fa725a20e2dd8e96373`
- Decision binding：`matched`
- Profile：19
- unknown Requirement refs：0
- effective Requirement集合差分：0
- approved target content／authority scope／Acceptance truth変更：0

したがって、既承認NFR Profile接続のHuman Decisionは再承認を要求せずfreshへ戻せる。Architecture Policy、
数値閾値、deployment scopeの承認状態は変更していない。

## Deferred Candidate Revalidation

- candidate SHA-256：`01da1ea0c6c4f6adad8fdcd09085f97b387ea4639d01b0811b80dc5957916210`
- candidate digest：`8993a6e4671679ab8cfe665322efdaf862cf085a8f1fab7d500d15f5fd7deb84`
- deferred capability：13
- unknown Requirement refs：0
- unknown Profile refs：0
- initial consumer：9
- scope leak：0
- release blocker：0

候補の意味内容は変更せず、新authority v2とcurrent Planに対して同じ監査結果を再確認した。このEvidenceは候補を
自動承認しない。deferred候補は引き続き`human_decision_pending`である。

## Result

authority representationとPlan frontmatterのidentity変更によるstale閉包を再検証した。NFR候補は既承認範囲を
維持してfresh、deferred候補は現行sourceに対してverifiedだが未承認である。次のHuman判断対象はdeferred候補の
owner、成果、配置、有効化条件、初期非依存境界である。
