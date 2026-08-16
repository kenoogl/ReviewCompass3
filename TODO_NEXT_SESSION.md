# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：G20『外部レビュア一回送信』は契約v4採用の下で実装に入り（RED 48件→最小実装で対象49件成功）、契約内矛盾を発見した：§11の置き場所`tools/egress/`と、§12.11が成功を要求する既存敵対試験の不変条件「egress配下に通信手段なし」が両立しない。既存試験の書換えはHuman承認事項のため停止し、置き場所だけを新package`tools/external_review/`へ変える契約候補v5を作成した。利用者の判断（軽微訂正として直接承認かGemini限定再確認へ運搬か）を待って停止中。実装fileは未commit。
- Task Contract：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5 / correction_pending_human_approval`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者の受入済み部品運用化目標](records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md) — SHA-256 `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a`
- [外部レビュー準備・実施の機械化目標](records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md) — SHA-256 `46a415eb630266e23a87562e6083f873e2fe9790acd34a6699f59b30aee0b45e`
- [置き場所矛盾を訂正した契約候補v5](records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v5.md) — SHA-256 `6fc7b37b07f65519e78353df23fc7277c1c9265956320e46d5e6e35608e9d165`
- [契約候補v4を開始可としたGemini限定再確認（Human中継）](records/development/2026-08-16-external-reviewer-single-send-v4-limited-rereview-v1.md) — SHA-256 `75d483ca65c27ac6ece1363f4a708153912447f58254c997ad760aa06b90bc84`
- [Gemini指摘3件を訂正した外部レビュア一回送信の契約候補v4](records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v4.md) — SHA-256 `e41acfdf0ceb1f8cff0c112d21181cd60a856345de6b38e90e89d3aafa161325`
- [契約候補v3を修正要としたGemini独立確認（Human中継）](records/development/2026-08-16-external-reviewer-single-send-v3-independent-review-v1.md) — SHA-256 `5198c5fff9a63820e603a613b8db9f4c5cf91ac00ffe2dd90e57fb4c001b9ac0`
- [契約候補v2の起草側自己レビューと文脈整理](records/development/2026-08-16-external-reviewer-single-send-v2-self-review-v1.md) — SHA-256 `65dd817a2b49b4769d7ed9743fc3d5331c6e0720f3c00123753cf24b3f350d71`
- [暫定レビュー体制の決定（Gemini手動利用・Human中継）](records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md) — SHA-256 `1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792`
- [利用者によるG02安全投影の製品受入判断](records/development/2026-08-16-one-item-review-safe-projection-product-acceptance-decision-v1.md) — SHA-256 `2cea891bb43fa83b15259310d97a459b6f446898bdedf79630cd2e945d8008cc`
- [Codex独立完了レビュー・verified判定](records/development/2026-08-16-one-item-review-safe-projection-independent-completion-review-v1.md) — SHA-256 `0152fb5ba32397ab651c29291f36e45d8c030f10188bc2ebf3f6f2bb2ce4a145`
- [実装成功Evidence（RED・GREEN・全試験・自由文遮断E2E）](records/development/2026-08-16-one-item-review-safe-projection-green-evidence-v1.md) — SHA-256 `6b9e6dbd7c43f1d34dc456f3fff6bc5e17c82103a8aa5db623f0b841be84fb63`
- [利用者による契約v2採用・実装開始の承認](records/development/2026-08-16-one-item-review-safe-projection-adoption-decision-v1.md) — SHA-256 `17b4f4f522810db3a851b1bc8dd1ab65bb90fb9ce5df2276ae60a42fcb19ec99`
- [契約候補v2を開始可としたCodex限定再確認](records/development/2026-08-16-one-item-review-safe-projection-v2-limited-rereview-v1.md) — SHA-256 `135f3a5e4daa3be2548831c6d2f97c5b77fba0b1e8e00611bafd6be9e9051afc`
- [停止理由集合を一意化したG02安全投影の契約候補v2](records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v2.md) — SHA-256 `9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603`
- [契約候補v1を停止原因1件で修正要としたCodex独立確認](records/development/2026-08-16-one-item-review-safe-projection-v1-independent-review-v1.md) — SHA-256 `b211626ba83409e9a892c202c0903e1363b535dc93b6f390627d42361ba3d33f`
- [利用者による最小運用契約実行の製品受入判断](records/development/2026-08-16-minimal-operation-contract-execution-product-acceptance-decision-v1.md) — SHA-256 `8386ee089ff54b0fde80fca4592a58d8e660e71cd11cb9687e676ca3f824e808`
- [Codex独立完了再レビュー・verified判定](records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-rereview-v1.md) — SHA-256 `00825b1fbce7a3ea91177d1493c9098bbfea6a7a76868e24f8f050b1f59dc927`
- [blocking 3件の訂正Evidence](records/development/2026-08-16-minimal-operation-contract-execution-correction-evidence-v1.md) — SHA-256 `c2a386c87e542a7f626e77b931bb24672fd6bf392fda71e216a5c19923959c30`
- [実装成功Evidence（RED・契約欠陥発見・GREEN・全試験・E2E）](records/development/2026-08-16-minimal-operation-contract-execution-green-evidence-v1.md) — SHA-256 `145f4938b7358acf301195901dfcacdf633b712927e60539c2db8e956c088336`
- [採用中の最小運用契約実行の契約v4](records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v4.md) — SHA-256 `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1`
- [条件付き事前承認の成立による契約v3採用judgment](records/development/2026-08-16-minimal-operation-contract-execution-adoption-decision-v1.md) — SHA-256 `5f8c9fab3e3512376359f4b58ca528b87adcb74d0d488e1e86af1af06f2b6614`
- [契約候補v3を開始可としたCodex限定再確認](records/development/2026-08-16-minimal-operation-contract-execution-v3-limited-rereview-v1.md) — SHA-256 `daa414658c2d6fc8ef712ceb47ae9b188cd787c1214be1ab826209795e97689e`
- [利用者による一件の要求候補整合検査の製品受入判断](records/development/2026-08-16-one-requirement-candidate-consistency-check-product-acceptance-decision-v1.md) — SHA-256 `dd9edcfd5895c143f7c83c05dcc2df986d36d066030782a5577d534071866fd8`
- [次製品作業の候補一覧（8候補・推奨順）](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が契約候補v5（置き場所だけの訂正：`tools/egress/`→新package`tools/external_review/`。安全境界・
schema・検査・台帳の定義は不変）の扱いを決める：(A)軽微訂正として直接承認し実装を再開する、
(B)Gemini限定再確認へ運搬してから採用判断する。

開始条件：

- 契約候補v5、本TODOが意味単位commitへ固定される（実装途中file 4件は未commitのまま作業treeに残す。Git・Test欄参照）
- 次sessionはAGENTS.md・本TODO・契約候補v5・v2自己レビュー（5段手続きの記録）を読んでから再開する

完了条件：

- 利用者の判断がchatで得られ、Decision recordへ固定される

後続作業：承認後、Claudeが実装file 2件を`tools/external_review/`へ再配置（`__init__.py`追加・試験のimport先
更新）して対象試験49件を全緑にし、退行確認（egress敵対試験の回復を含む）→GREEN commit→独立完了レビュー
（Gemini・Human中継、5段手続きの下ごしらえつき）→利用者指示による実送信E2E一回→製品受入提示の順で進める。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇により、codex exec起動によるレビューは停止（暫定Gemini体制で代替中）
- Human判断待ち：契約候補v5の扱い（直接承認かGemini再確認か）

## stale・deferred

- stale：候補3実行中の表示、次の一件の選択待ち表示はstale
- deferred：G24の要求作成責務、G02 organize・G25・安全保存との統合、既存G30基盤の正式化、候補6以降、実利用者資料の使用は後続境界まで対象外。外部レビュー準備の機械化（依頼組み立て器・prompt品質gate・判定取り込み）は目標record固定済みで契約008完了後の縦切り。5段手続きの手順書化は本線の区切りで実施。`.gitignore`食い違いは`IC-HANDOFF-GITIGNORE-RECORD-CANONICAL-001`として登録済み、Human仕分け待ち

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：**意図的に未commitの実装途中fileが4件残る**（契約v5のHuman判断待ちのため。`tools/egress/`配下に
  置いたままcommitすると既存敵対試験が不合格になるので、v5承認後に`tools/external_review/`へ再配置してから
  commitする）：`tools/egress/gemini_send.py`（新規・未追跡）、`tools/egress/gemini_send_entry.py`（新規・未追跡）、
  `pyproject.toml`（実行名1行追加の変更）、`tests/test_gemini_send.py`（opener試験の実態合わせ変更）。
  これらを消さずに次sessionで扱うこと
- 直近の関連Test：G20対象49件（worktreeの実装で成功）、G02 organize追加後の実行器75件、G02 158件、G08 107件、G24 111件、G30基盤38件、egress関連107件（うち敵対1件は上記の置き場所矛盾により実装file存在時のみ不合格）
- 直近の全Test：隔離条件の正規全試験2,313件成功（G02安全投影GREEN時点）。通常host環境の既存executor安全拒否12件は既知事象で退行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
