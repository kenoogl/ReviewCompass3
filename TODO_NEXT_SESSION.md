# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：G20『外部レビュア一回送信』は実送信E2E一回（受入条件13）を完了した。1回目は資料file名への高乱雑性誤検知で送信前に安全停止（構造問題を観測record・改善候補`IC-EGRESS-SENSITIVE-SCAN-FALSE-POSITIVE-001`として登録）。利用者裁定(2)の下、検査合格の確認用文書で再実行し、gemini-3.1-pro-previewへの一回送信・未加工応答保存・台帳3 record着地・計数1件・鍵非出現を実環境確認した。残るは製品受入（受入条件14）の利用者判断だけである。
- Task Contract：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5 / live_e2e_done_awaiting_product_acceptance`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [G20実送信E2E Evidence（初回承認済み外部送信）](records/development/2026-08-16-external-reviewer-single-send-live-e2e-evidence-v1.md) — SHA-256 `42f47236a79b04944d84504d837149cbc193637d5a34d405995fd49e7809d95f`
- [機微検査誤検知の観測record](records/development/2026-08-16-egress-sensitive-scan-false-positive-observation-v1.json) — SHA-256 `e6ffac53245501a57555a19b17225c4715ac394bdf37ef1c6cb025446adfb1b4`
- [G20訂正の限定再確認・verified判定（Gemini・Human中継）](records/development/2026-08-16-external-reviewer-single-send-correction-rereview-v1.md) — SHA-256 `c2b518f86792bebbe51352543da1b13ea8f2b33c55268c38ceac4996ab297596`
- [G20訂正の限定再確認依頼record](records/session-handoffs/2026-08-16-g20-single-send-correction-rereview-gemini-request-v1.md) — SHA-256 `f4b761d34993f95c6c71b92aa834db0f37d34511dd2fa17114f19a8e3d4138ae`
- [G20完了レビュー指摘3件の訂正Evidence](records/development/2026-08-16-external-reviewer-single-send-correction-evidence-v1.md) — SHA-256 `1f10f9c37350bb1acd0173a6753d917b1baddfd670cba66baa546df28b153262`
- [G20独立完了レビュー・修正要判定（Gemini・Human中継）](records/development/2026-08-16-external-reviewer-single-send-completion-review-v1.md) — SHA-256 `e429f167e57883aae04a72ad85a82416a7aa5801ec4bfc108facdf61a0d12aa9`
- [G20独立完了レビュー依頼record v2（Gemini直接読取り・Human中継）](records/session-handoffs/2026-08-16-g20-single-send-completion-review-gemini-request-v2.md) — SHA-256 `4888796d5ce5c9242400065a85d2043a8cc00c67b13a07cd3ef3b73019013936`
- [G20実装の起草側自己レビューと文脈整理](records/development/2026-08-16-external-reviewer-single-send-impl-self-review-v1.md) — SHA-256 `899f0697b5124850273dea442f68cd28ac52bd2aa95d1be8410d1e7b3a46dbfe`
- [G20実装成功Evidence（RED・v5訂正・GREEN・退行確認・判定系列E2E）](records/development/2026-08-16-external-reviewer-single-send-green-evidence-v1.md) — SHA-256 `51bd4d40e8d6fd3424bae6dac16ca1bc6006e86f95e37c66c93e3465b74cfd9a`
- [契約v5軽微訂正の直接承認・実装再開の利用者判断](records/development/2026-08-16-external-reviewer-single-send-v5-adoption-decision-v1.md) — SHA-256 `0d80690cb5f71150701d2f6d8613a205c9e5b37a1865e74bd6db377d4e13811f`
- [採用中の置き場所矛盾を訂正した契約v5](records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v5.md) — SHA-256 `6fc7b37b07f65519e78353df23fc7277c1c9265956320e46d5e6e35608e9d165`
- [縮小境界・契約v4採用・実装開始の利用者判断](records/development/2026-08-16-external-reviewer-single-send-adoption-decision-v1.md) — SHA-256 `dc525b5ed752103f454008f04c7df58665c85788ca041ea2b9293a29ad7fb201`
- [契約候補v4を開始可としたGemini限定再確認（Human中継）](records/development/2026-08-16-external-reviewer-single-send-v4-limited-rereview-v1.md) — SHA-256 `75d483ca65c27ac6ece1363f4a708153912447f58254c997ad760aa06b90bc84`
- [契約候補v2の起草側自己レビューと文脈整理](records/development/2026-08-16-external-reviewer-single-send-v2-self-review-v1.md) — SHA-256 `65dd817a2b49b4769d7ed9743fc3d5331c6e0720f3c00123753cf24b3f350d71`
- [暫定レビュー体制の決定（Gemini手動利用・Human中継）](records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md) — SHA-256 `1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792`
- [利用者の受入済み部品運用化目標](records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md) — SHA-256 `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a`
- [外部レビュー準備・実施の機械化目標](records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md) — SHA-256 `46a415eb630266e23a87562e6083f873e2fe9790acd34a6699f59b30aee0b45e`
- [利用者によるG02安全投影の製品受入判断](records/development/2026-08-16-one-item-review-safe-projection-product-acceptance-decision-v1.md) — SHA-256 `2cea891bb43fa83b15259310d97a459b6f446898bdedf79630cd2e945d8008cc`
- [次製品作業の候補一覧（8候補・推奨順）](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が製品受入（受入条件14）を判断する。提示済みの限界：(1)G20全体ではない最初の送信縦切りで、
応答解析・監査自動化・旧設計統合は後続、(2)機微検査の現水準では長い連結名・digest記載を含む実用文書が
誤検知で送信不能（改善候補`IC-EGRESS-SENSITIVE-SCAN-FALSE-POSITIVE-001`登録済み。精密化は後続契約）。
受入後はTODOを次候補選択の状態へ更新する。

開始条件：

- 実送信E2E Evidence・観測record・改善候補・本TODOが意味単位commitへ固定され、作業treeがcleanである

完了条件：

- 利用者の受入判断がchatで得られ、Decision recordへ固定される

後続作業：受入後、候補6以降の次作業選択、または区切り作業（5段手続きの手順書化・`.gitignore`仕分け・
機微検査精密化の契約候補作成）をHumanが選ぶ。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇により、codex exec起動によるレビューは停止（暫定Gemini体制で代替中）
- Human判断待ち：製品受入（受入条件14）の判断。改善候補`IC-EGRESS-SENSITIVE-SCAN-FALSE-POSITIVE-001`の仕分けは受入後の区切りで扱う

## stale・deferred

- stale：契約候補v5の判断待ち表示、stash退避中の表示はstale（v5承認済み・stash復元済み）
- deferred：G24の要求作成責務、G02 organize・G25・安全保存との統合、既存G30基盤の正式化、候補6以降、実利用者資料の使用は後続境界まで対象外。外部レビュー準備の機械化（依頼組み立て器・prompt品質gate・判定取り込み）は目標record固定済みで契約008完了後の縦切り。5段手続きの手順書化は本線の区切りで実施。`.gitignore`食い違いは`IC-HANDOFF-GITIGNORE-RECORD-CANONICAL-001`として登録済み、Human仕分け待ち

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G20対象49件、egress関連107件（敵対試験の不変条件回復を含む）、G02 158件、G08 107件、G24 111件、実行器75件、G30基盤e2e 38件——各単独終了コード0。保護path差分0（基準は契約v5 §6.2の保護基準commit）
- 直近の全Test：禁止認証隔離条件の正規全試験2,362件成功・終了コード0（G20 GREEN時点。前回2,313件＋対象49件）。通常host環境の既存executor安全拒否12件は既知事象で退行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
