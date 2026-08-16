# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合、G20の外部送信2契約（008・009）の製品受入と3 provider実環境確認が完了。『レビュー実行体制の正式ツール化』縦Bの契約010は、実装・実E2E（7試行目で成功）・独立完了レビュー相当（判定verified・findings 0件）まで完了した。
- 現在作業：契約010の最終段＝製品受入（§9-11）のHuman判断待ち。受入対象は§2承認境界（起動の起点は利用者chat指示・起動ごと追加承認なし）と§7.4残余risk 3点の最終受容。E2Eはe2e-010-007で成立：起動→読取り→構造化判定→判定record機械転記→単独commit→事後照合4点合格をHuman運搬0回で完走（backend agy・gemini-3.1-pro-high・Tier 1）。外部APIレビュー（API直接送信経路）はpendingのまま。
- Task Contract：`TC-RC3-PRODUCT-REVIEWER-LAUNCH-ADAPTER-010 / v2`＝`adopted_implementation_started`（実E2E・独立完了レビュー相当まで済み。製品受入待ち）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：契約010の受入判断を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [契約010実E2E成功Evidence（第7試行・7試行の訂正連鎖表）](records/development/2026-08-17-reviewer-launch-e2e-attempt7-success-evidence-v1.md) — SHA-256 `eca7ae8f534a467e4e16bf094416bc742aeebd85231558c2fca98033e6b15711`
- [完了レビュー判定record（機械転記・verified）](records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-verdict-v1.md) — SHA-256 `68757e8b8583199dab95ffb6f5f9a43609f94fcb7acde04b53ec6bfff0233a3a`
- [完了レビュー依頼record（headless起動対象）](records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-request-v1.md) — SHA-256 `29819b3fd33b934ed51ced3b4f4d3982939e9b5498ed3a5fd43c0c079fddb13c`
- [読取り恒久許可の発見とproject束縛Evidence](records/development/2026-08-17-reviewer-launch-permission-grant-discovery-v1.md) — SHA-256 `db1562fadd60aa3f444fbeb29c892fd278e012a7c0898d2046dbcc48e8aaa0d5`
- [契約010実装Evidence（RED→緑・導線・手戻り記録）](records/development/2026-08-16-reviewer-launch-adapter-implementation-evidence-v1.md) — SHA-256 `9c7863e10f6fae2b654c85b17b0edb7493e47412f19218ae28ed5ee5d7ff58c5`
- [契約010採用と実装開始のHuman判断record](records/development/2026-08-16-reviewer-launch-adapter-contract-adoption-decision-v1.md) — SHA-256 `351e57108293255989d345a9936cbdb122cc4f6695df7c52b4ff2856ded0a983`
- [許可model一覧の利用者承認record（gemini-3.1-pro-high 1件）](records/development/2026-08-16-reviewer-launch-allowed-models-approval-v1.md) — SHA-256 `24377cd11ceae6e8182949dddd3dff3cd499e9bb1142b2746c3c5065c1b5e7b5`
- [採用中の契約010候補v2](records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md) — SHA-256 `7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a`
- [契約候補v2独立確認判定record（Gemini・開始可）](records/development/2026-08-16-reviewer-launch-adapter-v2-independent-review-v1.md) — SHA-256 `b2c37c97ca4d6fb1989b8bd07be0cdee94c0e819f5b0fca20e1bbad7e13724e3`
- [レビュー実行体制の正式ツール化 統合検討v1（agy訂正済み）](records/development/2026-08-16-review-tooling-formalization-study-v1.md) — SHA-256 `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が契約010の製品受入（§9-11）を判断する。受入対象：(1) §2承認境界（起動の起点は利用者のchat指示。
起動ごとの追加承認手続きなし。「起動ごと承認」への厳格化も選べる）、(2) §7.4残余risk 3点（repository
読取り＝Googleへの内容送出〔読取りはagyの機械層でrepository配下に限定されることを実測済み〕・agy仕様
変更への追随risk・Tier 1でも残るmodel依存〔work-review-protocol §5の機械反証併用は不変〕）。

開始条件：

- E2E成功Evidenceと本TODOが意味単位commitへ固定され、作業treeがcleanである

完了条件：

- 製品受入（または保留・条件付き受入）の文言がchatで得られる

後続作業：受入後は第2縦切り（claude-subagent backend・Tier 2／3の宣言とHuman受容機構）、縦A（依頼組み
立て器）、縦C（品質gate）の順序選択をHumanへ諮る。暫定手動体制はfallbackとして残る。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇により、codex exec起動によるレビューは停止中（本契約の受入後はagy経由のheadlessレビューが機械代替になる）
- Human判断待ち：契約010の製品受入（§2承認境界と§7.4残余riskの最終受容）

## stale・deferred

- stale：契約008・009の進行中表示（両契約とも受入完了）。E2E第1〜6試行の停止事象（第7試行の成功と各Evidenceの訂正で解消済み）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。対象：応答解析・監査自動化・旧egress設計統合・複数送信・API経路への運搬移行判断・external_send_approved表示の観測登録。送信路自体は受入済みで利用可能なまま。再開は利用者指示による）。契約010の範囲外の後続＝claude-subagent／codex-cli backend・Tier 2／3受容機構・Reviewer書込み方式・縦A依頼組み立て器・縦C品質gate。Reviewer側digest実計算のための特定command許可（shasum等）は将来の契約改定候補。5手順事前走査の手順書化は改善候補のまま

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約010対象35件（`tests/test_reviewer_launch.py`）、G30運用契約実行75件、layout 13件——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,410件成功・終了コード0（E2E成功・判定record着地後の再実行）。通常host環境の既存executor安全拒否12件は既知事象で退行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
