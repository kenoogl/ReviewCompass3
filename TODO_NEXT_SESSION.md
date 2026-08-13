# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：G04の最初の整理単位を完了し、処理目録一式は混在単位として維持した。判明した安全保証の食い違いは未解決の改善候補へ固定し、外部送信入口の再利用前に裁定する条件で後回しにした。次はG07の赤試験宣言契約を意味群として再評価する。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 16意味群分類完了 / 最初の整理単位完了 / 処理目録安全問題はdefer / G07再評価待ち`、影響：増加した試験を行数や一件単位で処分せず、現在保証・履歴固定・役割終了を意味的に分離して保守負債を減らす、次：G07の追加8 node IDだけでなく、対応する三試験file、製品処理、現役正本、履歴資料を一群として読み取り、現在の役割を裁定前まで整理する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [第3段 意味群分類Evidence](records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-evidence-v1.md) — SHA-256 `cc77c218bc4baefc5e734ad7310824235900f32c122bd5f3c5ecdb786cb9399e`
- [処理目録の役割再評価 独立完了レビュー](records/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-independent-completion-review-v1.md) — SHA-256 `34fc8dedbea2a1be5164977244a6d2799785e574e496ea6e42e5f958657a0934`
- [処理目録安全問題の観測](records/development/2026-08-13-process-inventory-safety-claim-observation-v1.json) — SHA-256 `5cb7208c1a0ffe40b3d2afffeae1fcb7fdd091207dfecf746de09246ac59a443`
- [処理目録安全問題の改善候補](.reviewcompass/workflow/improvement-candidates/ic-process-inventory-safety-claim-001--v1.json) — SHA-256 `2a9704bfbbaa3a677351c76490a7a73a3cd2291443efd1121bf5600e501c0394`
- [処理目録安全問題の後回し判断](.reviewcompass/workflow/triage-decisions-v4/dec-ic-process-inventory-safety-claim-001--v1.json) — SHA-256 `19c730b299cb0eb2d3bd9098427fbc0b138d5cbe8ac1ad80dffd39f87a081f01`

## 次に行う一作業

G07「赤試験宣言契約」を意味的に完結する一群として読み取り再評価する。401件中の追加8 node IDを入口にするが、対象をその8試験だけへ狭めず、関連する三試験file、宣言map・実行処理、現役の正本と利用者、履歴資料を照合する。コード、試験、設定、正本は変更しない。

開始条件：

- 処理目録安全問題の観測、改善候補、後回し判断がcommit済みである
- 外部送信入口の再利用前に同問題を裁定する条件を維持する
- G07の追加8 node IDと三試験fileを機械列挙し、試験件数だけを採否根拠にしない

完了条件：

- 試験、製品処理、設定・正本、履歴資料を対象種別ごとの工程で確認する
- 現在の動作保証、履歴・監査資料、両方、役割終了へ意味単位で分類し、境界と利用者を示す
- 代表的な正常例・異常例・境界例または反証を機械で確認し、削除・維持・修正の裁定はHumanへ返す
- 比較のためだけの新しい試験、検査器、台帳を作らない

後続作業：独立レビューで分類境界と反証を確認した後、意味的な変更候補がある場合だけ利用者へ三案比較と裁定点を示す。Claude手動確認は追加せず、第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：なし。G07は読み取り再評価から開始できる。
- Human判断待ち：G07の読み取り再評価後に、意味的な削除・維持・修正候補が生じた場合だけ求める。現時点ではなし。

## stale・deferred

- stale：G04処理目録一式を単純な未使用処理として結合削除する案、v1のG11三試験を役割終了として削除する案、分類ごとのClaude手動確認、一件ずつの削除は採用しない。
- deferred：IC-PROCESS-INVENTORY-SAFETY-CLAIM-001（外部送信入口の再利用前にHuman裁定）、G11三試験と専用補助処理、他の未評価意味群、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：処理目録の基準再生成試験と現在の汎用実行器到達禁止試験は独立確認で各一件成功、終了コード0。後回し記録は候補検証とV4判断台帳検証に合格。
- 直近の全Test：後回し記録はコード・試験・設定を変更しないため再実行しない。直前の試験整理単位では正規入口から1,737件成功、失敗・エラー・除外0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
