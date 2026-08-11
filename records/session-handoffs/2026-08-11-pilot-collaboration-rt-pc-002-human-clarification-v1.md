# 操縦者別連携 RT-PC-002 Human補足裁定 v1

- 日付：2026-08-11
- 裁定者：Human
- 裁定文言：`RT-PC-002はv6どおり保存前停止とする。raw・launch・eventは作らずraw_digest_mismatchで停止し、裁定記録の「保存」はaudit_digest_mismatchだけに適用する。`
- 裁定文言の出典：本作業の会話
- 対象所見：`RT-PC-002`
- 対象再レビュー：`records/session-handoffs/2026-08-11-pilot-collaboration-red-test-rereview-v2.md`
- 対象再レビューSHA-256：`914c3d6a466fe439f50e000407fe3a2f0a5d70ace9616e86ed36ed18239553d2`
- 先行裁定：`records/session-handoffs/2026-08-11-pilot-collaboration-red-test-findings-human-decision-v1.md`
- 先行裁定SHA-256：`d350bb7d21b0a427b3306fb878c2044f75ccb9a7d0eb19438b8c68c965042e7a`
- 実装指示：`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md`
- 実装指示SHA-256：`5ab9474b425162df9c192124c7558754b4b371402d2e4d67adfab448cbbb3b5d`
- 裁定：`pre_store_stop`

## 補足裁定内容

1. launch記録に含まれるraw SHA-256の不一致は、v6どおり保存前検査とする。
2. 不一致時はrun raw、launch記録、eventを一切作らず、`raw_digest_mismatch`で停止する。
3. 先行裁定の「保存」は、判定rawの`audit_parsed_sha256`不一致で停止する
   `audit_digest_mismatch`だけに適用する。
4. この補足裁定は先行裁定のRT-PC-002部分を限定し、RT-PC-001、003、004の採用判断は変更しない。

したがってv6の変更は行わず、現行testの保存前停止境界を維持する。RT-PC-001と004の不足を同じ
test-only作業単位で修正し、独立再レビューが`verified`になるまでproduction実装へ進まない。
