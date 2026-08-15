# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：候補3のG24の最初の縦切り「一件の要求候補整合検査」は、Codex独立完了レビュー`verified`（blocking 0件）を経て利用者が製品受入した。候補3全体は未完了で、要求文・機能区分・出典対応の「作成」責務が後続に残る。次はG24残り責務の継続か候補4（G30最小作業契約実行)への移行かの利用者選択である。
- Task Contract：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005 / v3 / accepted`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者による一件の要求候補整合検査の製品受入判断](records/development/2026-08-16-one-requirement-candidate-consistency-check-product-acceptance-decision-v1.md) — SHA-256 `dd9edcfd5895c143f7c83c05dcc2df986d36d066030782a5577d534071866fd8`
- [Codex独立完了レビュー・verified判定](records/development/2026-08-16-one-requirement-candidate-consistency-check-independent-completion-review-v1.md) — SHA-256 `ab78ec0cb391ecaa1413275cf8a27a746039f42c6fdce95a794050947a14a50c`
- [実装成功Evidence（RED・GREEN・全試験・合成E2E）](records/development/2026-08-16-one-requirement-candidate-consistency-check-green-evidence-v1.md) — SHA-256 `50386e4a981e039e21af3bcec1fb3c37ba078739ff506b9afa19d63d806be6d2`
- [採用された一件の要求候補整合検査契約v3](records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md) — SHA-256 `7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- [次製品作業の候補一覧（8候補・推奨順）](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が次の一件を選択する：(A) 候補3の残り責務（G24の要求文・機能区分・出典対応の「作成」縦切り）の契約定義へ進む、
(B) 候補4（G30最小作業契約実行）の契約定義へ進む。選択後、Claudeが同じ手順（契約候補→独立確認→採用→
失敗試験→最小実装→独立完了レビュー→受入）で進める。

開始条件：

- 受入判断record、本TODOが意味単位commitへ固定され、作業treeがcleanである
- 選択前に契約定義・実装を開始しない

完了条件：

- 利用者の選択がchat文言で得られ、対応する契約候補の定義作業へ引き継がれる

後続作業：なし（改善候補の登録は完了済み。仕分けはHuman裁定待ちの持ち越し）。

## blocker・Human判断待ち

- blocker：技術blockerなし
- Human判断待ち：次の一件の選択（A：G24作成責務の継続、B：候補4のG30へ移行）

## stale・deferred

- stale：v3の実装中・レビュー待ち・受入待ちの表示はstale
- deferred：G24の要求作成責務（選択Aまで）、現行要求変更、候補5以降、外部送信、実利用者要求資料の使用は後続境界まで対象外。`.gitignore`食い違いは`IC-HANDOFF-GITIGNORE-RECORD-CANONICAL-001`として登録済み、Human仕分け待ち

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：対象111件、G24既存関連59件、要求artifact関連21件、G08対象107件が各単独成功、終了コード0
- 直近の全Test：禁止認証環境6件を除く隔離条件で正規全試験2,238件成功、終了コード0。通常host環境の既存executor安全拒否12件は実装前cleanなHEADの一時worktreeで同一再現し退行なしと確認済み
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
