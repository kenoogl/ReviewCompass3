# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：G06再評価後にWork 5B契約v2の内容識別値訂正を開始したが、G07の承認済み試験変更により別の固定参照が外れ、関連試験が既に一件失敗していることを確認した。一値訂正は取り消し、関連成果物群の再評価を開始するか利用者が判断する段階である。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / G06再評価verified / Work 5B限定訂正停止 / Human判断待ち`、影響：完了済みの歴史契約が後から正当に変更された現在試験fileのbytesを不変として照合し、同じ固定値更新の手戻りを繰り返している。G07変更後の現在状態では契約試験が一件失敗する、次：利用者が案Cの読み取り再評価を開始するか判断する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [Work 5B限定訂正 作業票](docs/development/2026-08-13-work5b-contract-v2-content-digest-correction-bootstrap-work-ticket-v1.md) — SHA-256 `f2aaf3f67f7f75372c7c5a47740d6d83158bc82230358e6c3499e91df4a5267f`
- [Work 5B限定訂正 停止Evidence](records/development/2026-08-13-work5b-contract-v2-content-digest-correction-stopped-evidence-v1.md) — SHA-256 `160f894ceac081c02c3ba738d4c67385022cb4c3540c8254b5112f7dcdfec275`
- [G06再評価 限定修正後確認](records/development/2026-08-13-stage3-g06-common-guards-reassessment-correction-review-v1.md) — SHA-256 `e0613030767c04d38014e9842388c2b302cc071f0a1c5b463bb3914bf6d7d36a`

## 次に行う一作業

利用者が案Cを開始するか判断する。案Cでは、Work 5B契約v1・v2、固定参照のDecision、現在の契約試験六件、G07で変更した試験file、現在利用者、Git履歴を一群として読み取り再評価する。コード、試験、契約recordは変更しない。

開始条件：

- 限定訂正の一時変更が取り消され、対象recordが基準commitと同じbytesである
- 関連試験一件の失敗が内容識別値ではなくG07変更後の固定source指紋差で再現済みである
- 利用者が案Cの読み取り再評価を承認する

完了条件：

- 関連成果物を現在保証、履歴・監査資料、両方、役割終了へ分類する
- 固定値の再追随、後継契約、現役試験整理を簡潔さ、頑健さ、将来の保守・回復費用で比較する
- 一回の独立完了レビュー後、意味変更候補を利用者判断へ戻す

後続作業：案Cの裁定後に選ばれた修復を一作業として完了し、その後に承認済みG06案Bへ戻る。Claude手動確認は第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：内容識別値一値だけの訂正では関連試験が成功しない。契約の意味または現在試験の責務を変える可能性があり、追加のHuman判断が必要。
- Human判断待ち：同じ固定値更新を繰り返さず、案Cの読み取り再評価を開始するか。操縦役は案Cを推奨する。

## stale・deferred

- stale：Work 5B契約v2の自己内容識別値だけを直せば現在不整合が閉じるという見方、G07変更前の全試験1,737件成功を現在状態へ適用する見方、固定SHA-256を都度更新すれば恒久解消するという見方は採用しない。
- deferred：承認済みG06案B、IC-PROCESS-INVENTORY-SAFETY-CLAIM-001（外部送信入口の再利用前にHuman裁定）、G11三試験と専用補助処理、他の未評価意味群、Work 8の全体変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：tests/test_work5b_contract.pyは内容識別値訂正前後とも5件成功・1件失敗、終了コード1。失敗はG07で変更された試験fileの固定SHA-256差である。
- 直近の全Test：現在状態では関連試験の失敗を直接確認済みのため実行しない。G07変更前の1,737件成功は現在状態には適用しない。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
