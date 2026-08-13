# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：G07の追加8試験を再評価し、7件は固有の現在保証、1件は入力分離不足と独立確認した。現行レビュー手順が旧方式を許し、試験準備の失敗を期待どおりの赤として誤合格できる接続漏れも確認した。既存の安全な版2へ接続する案Aの利用者判断を待つ。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 最初の整理単位完了 / G07再評価verified / 案A承認待ち`、影響：試験準備の失敗を予定した機能不足と取り違えて赤試験を誤承認でき、空宣言の拒否条件を壊しても既存試験が検出しない、次：利用者が、現行レビュー手順を既存版2へ接続し、既存一試験内で二つの空条件を分ける案Aを開始するか判断する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [G07再評価 作業票](docs/development/2026-08-13-stage3-g07-declaration-red-contract-reassessment-bootstrap-work-ticket-v1.md) — SHA-256 `a9b95a250ea3f48a49474fabad2fe03a78b95f7741420b55de77cee0e1976193`
- [G07再評価Evidence](records/development/2026-08-13-stage3-g07-declaration-red-contract-reassessment-evidence-v1.md) — SHA-256 `2f9441bdc684fa02b15c839bc3d91cc773ba2f688c747b4818831f12ed96a172`
- [G07再評価 独立完了レビュー](records/development/2026-08-13-stage3-g07-declaration-red-contract-reassessment-independent-completion-review-v1.md) — SHA-256 `225aab836892ddea8ccd576bdd9444186e72e0ae513ef11cab9e5b9d0805e4dc`
- [処理目録安全問題の後回し判断](.reviewcompass/workflow/triage-decisions-v4/dec-ic-process-inventory-safety-claim-001--v1.json) — SHA-256 `19c730b299cb0eb2d3bd9098427fbc0b138d5cbe8ac1ad80dffd39f87a081f01`

## 次に行う一作業

利用者が案Aを開始するか判断する。案Aは、現行レビュー手順で対応表版2、予定失敗理由、最低版2を必須にし、既存の空宣言試験一件の中で「宣言だけ空」と「試験file一覧だけ空」を別々に確認する。新しい試験、検査器、台帳は追加しない。

開始条件：

- G07再評価Evidenceと独立完了レビューがcommit済みで判定verifiedである
- 旧方式の誤合格と空宣言条件の見逃しが別入力・別複製で再現済みである
- 方針変更と試験の意味変更について利用者が案Aを承認する

完了条件：

- 承認前は現行レビュー手順、試験、検査処理を変更しない
- 承認時は変更範囲を現行レビュー手順一件と既存試験file一件に限定した作業票を固定する
- G07追加8件を削除せず、新しい試験件数を増やさない
- 修正後は対象試験、旧方式の誤合格反例、新方式の拒否、二つの空条件を独立確認する

後続作業：案Aを実施・独立完了レビューした後、第3段の次の意味群へ戻る。承認しない場合は、保証を失わない別案を利用者判断へ戻す。

## blocker・Human判断待ち

- blocker：技術的な実施方法は既存機能で確定しているが、現行レビュー手順の意味変更を含むため利用者承認が必要。
- Human判断待ち：案Aを開始し、G07追加8件を維持するか。操縦役と独立レビューは案Aを推奨する。

## stale・deferred

- stale：G07追加8件を履歴固定または重複として削除する案、旧方式のverify_redだけで赤試験を安全に照合できるという見方、空宣言試験が二つの空条件を個別に保証するという見方は採用しない。
- deferred：IC-PROCESS-INVENTORY-SAFETY-CLAIM-001（外部送信入口の再利用前にHuman裁定）、G11三試験と専用補助処理、他の未評価意味群、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G07追加8件、専用四file 22件、混在二fileの関連7件はすべて成功。独立変異では7条件を各一件が検出し、空宣言条件だけは追加8件と関連22件が見逃した。
- 直近の全Test：読み取りと記録だけのため再実行しない。直前の試験整理単位では正規入口から1,737件成功、失敗・エラー・除外0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
