# 契約012（claude-subagent第2 backend）採用と実装開始のHuman判断record v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contractの採用（縮小境界の確定）と実装開始の一判断

## 1. 承認文言【記録】

> 契約012を採用する。実装を開始して

（2026-08-17 chat。Claudeが提示した推奨文言と同一）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 契約012候補v2（採用対象） | `records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md` | `f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d` |
| 独立確認判定record（cr-012-001・verified・blocking 0） | `records/session-handoffs/2026-08-17-claude-subagent-backend-contract-review-verdict-v1.md` | `ae78da140e9b72576700437569f91aa67cdce2be237ae0a0cf48829b3d1676c3` |
| 起草側自己レビュー（SR-C12-1〜3） | `records/development/2026-08-17-claude-subagent-backend-v1-self-review-v1.md` | `092bfc37997c1a6cd723cbfbe47364f5936fee615f2cbe09dacee72fdaa913bc` |
| 正式再利用検索の証明書（start_allowed: true） | `records/development/2026-08-17-claude-subagent-backend-reuse-search-attestation-v1.json` | `bc37a5be2e2e182cd76985114f5ae9156039e5475282b1f2adf35c41feba230b` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-CLAUDE-SUBAGENT-BACKEND-012`（v2）を採用する。状態は
   `candidate_pending_independent_review`から`adopted_implementation_started`へ進む。
2. 実装を開始する。順序は契約§9のとおりRED（失敗試験の先行固定・外部起動なし）から行う。
3. **subagent許可modelの値の確定（利用者承認record）と、subagentの実起動（契約§9-8のE2E・
   `--accept-tier 3`と受容根拠の明示つき）は本判断に含まれない**。それぞれ別途の利用者承認・
   明示指示を得てから行う。
4. 残余risk（契約§7.4の4点）の最終受容は本判断に含まれない。製品受入（契約§9-11）で判断する。

## 4. 未実施

- 実装、subagent許可modelの承認、実E2E、完了レビュー、製品受入、TODO更新（handoff時）。
