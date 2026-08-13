# TODO_NEXT_SESSION

更新日：2026-08-13

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：G06の24件を再評価し、現在保証21件、役割終了候補3件、list再帰の見逃し、不一致のWork 5B契約v2記録を独立確認した。限定訂正後レビューはverifiedで、案Bと不一致記録のrouteを利用者が判断する段階である。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 最初の整理単位完了 / G06再評価verified / Human判断待ち`、影響：G06の現行24件にはlist再帰欠陥を見逃す入力と、固有保証のない3件が混在する。別に、現在試験が読むWork 5B契約v2の自己内容識別値が不一致である、次：利用者が案Bの試験整理と、Work 5B契約v2不一致のrouteを別々に判断する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [G06再評価 作業票](docs/development/2026-08-13-stage3-g06-common-guards-reassessment-bootstrap-work-ticket-v1.md) — SHA-256 `a10bd8a7b4e98ec5bc2afdfe5a8067302056a875e0e398e8c6b3cc235ce7b752`
- [G06再評価 訂正済みEvidence](records/development/2026-08-13-stage3-g06-common-guards-reassessment-evidence-v1.md) — SHA-256 `16e00c983c023167b11ebe64aaa6e0f2f32c55a59bc0e751b1c5e48e8422a9c1`
- [G06再評価 限定修正後確認](records/development/2026-08-13-stage3-g06-common-guards-reassessment-correction-review-v1.md) — SHA-256 `e0613030767c04d38014e9842388c2b302cc071f0a1c5b463bb3914bf6d7d36a`
- [処理目録安全問題の後回し判断](.reviewcompass/workflow/triage-decisions-v4/dec-ic-process-inventory-safety-claim-001--v1.json) — SHA-256 `19c730b299cb0eb2d3bd9098427fbc0b138d5cbe8ac1ad80dffd39f87a081f01`

## 次に行う一作業

利用者が二点を別々に判断する。第一に、G06案Bとして既存入力一件をlist内tupleへ置換し、固有保証のない衝突確認2件と不安定な実在記録走査1件を試験file一件から整理するか。第二に、Work 5B契約v2の自己内容識別値不一致を、いま別作業で限定訂正するか、候補として後回しにするか、本線へ戻るか。

開始条件：

- G06再評価Evidenceの事実誤記が限定訂正され、修正後確認がverifiedである
- 案Bはリポジトリ外模擬で21件・関連84件成功、list再帰欠陥で置換一件が失敗済みである
- 案BとWork 5B契約v2の訂正を同じ意味単位へ混ぜない

完了条件：

- 承認前は試験とWork 5B契約v2を変更しない
- 案Bを承認する場合は試験file一件だけの作業票、実施、独立完了レビューへ進む
- Work 5B契約v2は選択されたrouteを証跡化し、いま対処の場合だけ別作業票へ進む

後続作業：二判断のroute確定後、選ばれた一作業だけを完了し、第3段の次の意味群へ戻る。Claude手動確認は第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：技術的な案Bは成立しているが、既存試験の意味変更・削除と履歴記録の訂正routeはHuman判断を要する。
- Human判断待ち：案Bを開始するか。Work 5B契約v2不一致を、いま限定訂正／候補として後回し／本線へ戻る、のどれにするか。

## stale・deferred

- stale：G06の24件をすべて固有の現在保証とする見方、先頭200件の実在記録走査を全記録整合の保証とする見方、Work 5B契約v2を初期開発チェックリストも参照するという一次報告は採用しない。
- deferred：IC-PROCESS-INVENTORY-SAFETY-CLAIM-001（外部送信入口の再利用前にHuman裁定）、G11三試験と専用補助処理、他の未評価意味群、状態固定を宣言fileと共通検査へ置き換える作業、Work 8の全体変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G06現行24件・関連87件は成功。案B模擬は21件・関連84件成功。list再帰欠陥では現行24件が見逃し、案Bの置換一件が失敗。
- 直近の全Test：読み取り再評価とリポジトリ外模擬だけのため再実行しない。直前の試験整理単位では正規入口から1,737件成功、失敗・エラー・除外0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
