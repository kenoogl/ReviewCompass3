# 契約013採用と実装開始のHuman判断record v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contract候補の採用と実装開始（契約013・自由文類型）

## 1. 承認文言【記録】

> 推奨案で進める

（2026-08-17 chat。Claudeの推奨「所見を反映した候補v3を作成し、採用する。採用record→実装開始
（RED→実装→試験）まで進めて」の全文承認）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 採用する契約013候補v3（cr-013-001所見反映済み） | `records/task-contract/2026-08-17-free-text-request-type-candidate-v3.md` | `73a287c137a73c617e25655c35377b88a7ffc033b89e4be68d63d3b0ce245ffc` |
| 独立確認判定record（cr-013-001・verified_with_findings・blocking 0件・機械転記） | `records/session-handoffs/2026-08-17-free-text-request-type-contract-review-verdict-v1.md` | `dcfffbec261db38ba7c58dc8b92b9c5fa3b4d708940198abedaade29ae7112a6` |
| 起草側自己レビュー（SR-C13-1〜3） | `records/development/2026-08-17-free-text-request-type-v1-self-review-v1.md` | `7d52ce6eb8794de412def5dea9cf62f3d49ef27d35f26cd3154709983da0cb8f` |
| 事前走査v1（範囲整理の利用者了解を含む） | `records/development/2026-08-17-free-text-request-type-prescan-v1.md` | `aad68904a58f8ac79a8d99b1075636e1691684fde911fc83e15edc30437d9b55` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-FREE-TEXT-REQUEST-TYPE-013`は**候補v3を採用**し、状態を
   `adopted_implementation_started`とする。
2. 独立確認cr-013-001の非blocking所見2件の扱い：`scale-moderation-risk`は候補の残余risk 3の記載
   どおり（運用注意・fail-closed）。`prompt-injection-risk`は候補v3 §7.4残余risk 5として明文化済み。
3. 実装はRED先行（失敗試験の固定→期待どおりの失敗確認→最小実装）で開始する。既存2類型の互換は
   golden固定試験（生成結果SHA-256の試験定数固定）で機械証明する。
4. §9-5実運用E2E・§9-7完了レビューの起動、§9-8製品受入は、それぞれ利用者の明示指示・判断による
   （本判断に含まれない）。

## 4. 未実施

- 実装（RED→最小実装→試験）、実運用E2E、完了レビュー、製品受入、TODO更新。
