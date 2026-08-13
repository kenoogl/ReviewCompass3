# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段と第2段、および第3段の前提接続は完了した。第3段では401件を16意味群へ分け、現在保証と履歴固定を区別して群単位で整理している。
- 現在作業：Work 5B契約と現役試験の役割再評価を完了した。独立レビューはverifiedで、契約試験file一件・六試験だけを現役集合から外し、契約v1・v2と過去Decision・Evidenceを履歴として無変更で残す案Cの利用者承認を待つ。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / Work 5B役割再評価verified / 案C承認待ち`、影響：完了済みの歴史契約を現在試験fileのbytesへ束縛する六試験が、正当な後続変更を不合格にし、固定値更新を繰り返している。六試験を外しても現在の直接試験22件が安全境界を維持することを独立確認した、次：利用者が案Cの実施と履歴record無変更を承認するか判断する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`
- [Work 5B役割再評価 作業票](docs/development/2026-08-14-work5b-contract-lifecycle-reassessment-bootstrap-work-ticket-v1.md) — SHA-256 `be6e705587c0bba6c65d91ea365b803bab5fbad1b31a428166cf4b65af6aae49`
- [Work 5B役割再評価Evidence](records/development/2026-08-14-work5b-contract-lifecycle-reassessment-evidence-v1.md) — SHA-256 `7710fc40c1eb275bd4ba286686209149ca2cced272c8c2b0e18f7833182361a9`
- [Work 5B役割再評価 独立完了レビュー](records/development/2026-08-14-work5b-contract-lifecycle-reassessment-independent-completion-review-v1.md) — SHA-256 `471fda706322a31919a5b6bca1f3c611b2731dbdec25bb0a91dbbdeacb49a87f`

## 次に行う一作業

利用者が案Cを採用するか判断する。案Cはtests/test_work5b_contract.py一件・六試験だけを削除する。Work 5B契約v1・v2、固定source Decision・Evidence、初期開発チェックリスト、現在の検査コードと直接試験は変更せず、v2の自己内容識別値不一致も追加訂正しない。

開始条件：

- 役割再評価Evidenceと独立完了レビューがcommit済みで判定verifiedである
- 案C模擬で現在の直接試験22件が成功し、常時許可・常時拒否の欠陥を既存直接試験が検出済みである
- 利用者が案C、試験file一件・六試験の削除、履歴record無変更を承認する

完了条件：

- 承認前は試験、契約、Decision、Evidenceを変更しない
- 承認時は変更範囲を試験file一件の削除と実施Evidenceに限定した作業票を固定する
- 実施後は現在の直接試験22件、公式全試験、Gitからの履歴回復を独立完了レビューで確認する

後続作業：案Cを実施・独立完了レビューした後、既に承認済みのG06案Bへ戻る。Claude手動確認は第3段完了前の一回を残す。

## blocker・Human判断待ち

- blocker：技術的な停止要因はないが、既存試験六件の削除と履歴recordを追加訂正しない裁定はHuman承認を要する。
- Human判断待ち：案C、tests/test_work5b_contract.py一件・六試験の削除、v1・v2等を無変更で残しv2不一致を追加訂正しないことを承認するか。操縦役と独立レビューは案Cを推奨する。

## stale・deferred

- stale：v2の固定SHA-256を現在値へ再更新すれば恒久解消するという見方、後継v3を作る必要があるという見方、六試験が現在製品の固有保証を持つという見方は採用しない。
- deferred：承認済みG06案B、IC-PROCESS-INVENTORY-SAFETY-CLAIM-001、G11三試験と専用補助処理、他の未評価意味群、Work 8の全体変異検査。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：現在の契約試験は5件成功・1件失敗。案C模擬では現在処理を直接守る22件が成功し、常時許可・常時拒否の二変異を既存直接試験が検出した。
- 直近の全Test：読み取り再評価とリポジトリ外模擬だけのため再実行しない。案C実施後に正規入口から実行する。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
