# 契約011（依頼組み立て器）採用と実装開始のHuman判断record v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contractの採用（縮小境界の確定）と実装開始の一判断

## 1. 承認文言【記録】

> 契約011を採用する。実装を開始して

（2026-08-17 chat。Claudeが提示した推奨文言と同一。先行して「所見3件を採用する。v3へ反映して
採用判断の材料を出して」の指示によりcr-011-001所見3件が候補v3へ反映済み）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 契約011候補v3（採用対象） | `records/task-contract/2026-08-17-request-builder-candidate-v3.md` | `146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1` |
| 独立確認判定record（cr-011-001・verified_with_findings・blocking 0件） | `records/session-handoffs/2026-08-17-request-builder-v2-review-verdict-v1.md` | `f8a719f74f880eac80b95582073a12aff2d481b097add45c38dbaf17b996e51a` |
| 起草側自己レビュー（SR-C11-1〜3） | `records/development/2026-08-17-request-builder-v1-self-review-v1.md` | `7fef594b4bd4048fc4efdfa5368cb74e88d5be073a4526357827a0c1302030f3` |
| 正式再利用検索の証明書（start_allowed: true） | `records/development/2026-08-17-vertical-a-request-builder-reuse-search-attestation-v1.json` | `b081e9fa6243f46c653cd2870fc439c22f46cd903f7df21aa23f9f815e35c344` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-REQUEST-BUILDER-011`（v3）を採用する。状態は
   `candidate_pending_independent_review`から`adopted_implementation_started`へ進む。
2. v3はcr-011-001の所見3件（利用者採用）を逐語反映しており、v3への再レビューは行っていない
   （変更がReviewer提案の逐語反映であるため。利用者は本判断でこの扱いを含めて採用した）。
3. 実装を開始する。順序は契約§9のとおりRED（失敗試験の先行固定・外部起動なし）から行う。
4. **実運用E2E（契約§9-8：組み立てた依頼recordの縦B起動）は本判断に含まれない**。利用者の別途の
   明示指示を得てから行う。
5. 残余risk（契約§7.4の4点）の最終受容は本判断に含まれない。製品受入（契約§9-11）で判断する。

## 4. 未実施

- 実装、実運用E2E、完了レビュー、製品受入、TODO更新（handoff時）。
