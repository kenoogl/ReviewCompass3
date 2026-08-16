# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合、G20の外部送信2契約（008・009）の製品受入と3 provider実環境確認が完了。新規取組『レビュー実行体制の正式ツール化』は、縦B（Reviewer起動アダプタ）の契約010を採用し、実装（RED→緑・導線配備・保護対象差分0）まで完了した。
- 現在作業：契約010の残り受入条件を進める。§9-8実E2E（前提：許可model一覧の利用者承認と定数固定。現状は空一覧のため起動は安全側で停止する）→§9-10独立完了レビュー（暫定体制）→§9-11製品受入。Gemini CLIは2026-06-18提供終了・後継agy 1.1.13導入済み（統合検討はagyへ訂正済み）。外部APIレビュー（API直接送信経路）はpendingのまま。
- Task Contract：`TC-RC3-PRODUCT-REVIEWER-LAUNCH-ADAPTER-010 / v2`＝`adopted_implementation_started`（採用判断record参照）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在の契約010実装を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [契約010採用と実装開始のHuman判断record](records/development/2026-08-16-reviewer-launch-adapter-contract-adoption-decision-v1.md) — SHA-256 `351e57108293255989d345a9936cbdb122cc4f6695df7c52b4ff2856ded0a983`
- [契約010実装Evidence（RED→緑・導線・手戻り記録）](records/development/2026-08-16-reviewer-launch-adapter-implementation-evidence-v1.md) — SHA-256 `9c7863e10f6fae2b654c85b17b0edb7493e47412f19218ae28ed5ee5d7ff58c5`
- [契約候補v2独立確認判定record（Gemini・開始可）](records/development/2026-08-16-reviewer-launch-adapter-v2-independent-review-v1.md) — SHA-256 `b2c37c97ca4d6fb1989b8bd07be0cdee94c0e819f5b0fca20e1bbad7e13724e3`
- [採用中の契約010候補v2](records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md) — SHA-256 `7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a`
- [契約候補v2のGemini依頼record](records/session-handoffs/2026-08-16-reviewer-launch-adapter-v2-review-gemini-request-v1.md) — SHA-256 `390bc32868a2ee99f11e68d6bb9489826681674786d64b93ea207592399ac995`
- [契約候補v1自己レビュー（SR-C10-1〜4）](records/development/2026-08-16-reviewer-launch-adapter-v1-self-review-v1.md) — SHA-256 `3fadb74967e52fb6bc9a19b3099db12324b2e52c983fc60207b7587534b8cd8f`
- [レビュー実行体制の正式ツール化 統合検討v1（agy訂正済み）](records/development/2026-08-16-review-tooling-formalization-study-v1.md) — SHA-256 `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0`
- [縦B事前走査v1](records/development/2026-08-16-vertical-b-reviewer-launch-adapter-prescan-v1.md) — SHA-256 `736b9d58227cdb8b66f41abe9b6b0ab1b54515f415e5ccb69170c97bab7cb33a`
- [縦B事前走査追補v1（agy実測）](records/development/2026-08-16-vertical-b-prescan-agy-addendum-v1.md) — SHA-256 `2f5cdec3c2470ed54cd0df58cd46afa47353c6d159ba97c7494b19f65bf760f8`
- [暫定レビュー体制の決定（Gemini手動利用・Human中継）](records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md) — SHA-256 `1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が契約010の実E2E（§9-8）の実施を判断する：(1) 許可model一覧に載せるagyのmodel名を利用者が提示・
承認し、Claudeが直書き定数へ固定する（空一覧の間は`allowed_models_unfixed`で起動前停止）。(2) 実E2Eの
対象依頼record 1件（commit済み）を利用者が指定し、実施を明示指示する。実施後は独立完了レビュー
（暫定体制）→製品受入へ進む。

開始条件：

- 実装Evidenceと本TODOが意味単位commitへ固定され、作業treeがcleanである

完了条件：

- 許可model一覧の承認と実E2E実施指示（または保留の判断）がchatで得られる

後続作業：実E2E→§9-9残余確認→独立完了レビュー→製品受入→第2縦切り（claude-subagent・Tier 2／3受容）。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇により、codex exec起動によるレビューは停止（暫定Gemini体制で代替中）。旧Gemini CLIは2026-06-18提供終了（後継agyへ移行済み・アダプタ実装済み）
- Human判断待ち：許可model一覧の承認と、実E2E（初回の実起動）の実施指示

## stale・deferred

- stale：契約008・009の進行中表示（両契約とも受入完了）。縦B事前走査v1 §7の論点1・3（追補v1で差し替え済み）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。対象：応答解析・監査自動化・旧egress設計統合・複数送信・API経路への運搬移行判断・external_send_approved表示の観測登録。送信路自体は受入済みで利用可能なまま。再開は利用者指示による）。契約010の範囲外の後続＝claude-subagent／codex-cli backend・Tier 2／3受容機構・Reviewer書込み方式・縦A依頼組み立て器・縦C品質gate。5手順事前走査の手順書化は改善候補のまま

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約010対象31件（`tests/test_reviewer_launch.py`）、G30運用契約実行75件、layout 13件——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,406件成功・終了コード0（契約010実装とTODO参照digest更新後の再実行）。通常host環境の既存executor安全拒否12件は既知事象で退行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
