# TODO_NEXT_SESSION

更新日：2026-08-17

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合、G20の外部送信2契約（008・009）、そして『正式ツール化』縦Bの契約010（Reviewer起動アダプタ・第1 backend＝agy）の**製品受入が完了**した。headless機械起動によるレビュー一往復（起動→読取り→構造化判定→判定record機械転記→単独commit→事後照合）が正式経路となり、暫定手動体制はfallbackへ移行した。
- 現在作業：後続の縦切りの順序選択のHuman判断待ち。候補：(a) 縦A依頼組み立て器（依頼promptの機械組み立て＋機械検査。作成時の内容機微検査を論点に含める）、(b) 第2縦切りclaude-subagent backend（Tier 2／3の宣言・Human受容機構。2 oracle化の近道）、(c) 縦C品質gate・合議（判定record比較の上位層。A・Bの後が自然）、(d) 外部API直接送信経路のpending解除。設計原則は設計方針メモ（利用者裁定2件）に固定済み。
- Task Contract：なし（契約010はaccepted済み。次契約は順序選択後に定義する）

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：後続の縦切り定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者による契約010の製品受入判断（§2承認境界・残余risk受容）](records/development/2026-08-17-reviewer-launch-adapter-product-acceptance-decision-v1.md) — SHA-256 `78adb15fc84be82acf8a934a1673370d1ccd45c69805d12ed924e6320288d516`
- [レビュー経路の設計方針メモ（利用者裁定2件）](records/development/2026-08-17-review-path-design-principles-memo-v1.md) — SHA-256 `8e6a3668107b6bef114c2073c445092be1c54919decc65484e9a3def4b20648e`
- [契約010実E2E成功Evidence（第7試行・訂正連鎖表）](records/development/2026-08-17-reviewer-launch-e2e-attempt7-success-evidence-v1.md) — SHA-256 `eca7ae8f534a467e4e16bf094416bc742aeebd85231558c2fca98033e6b15711`
- [完了レビュー判定record（機械転記・verified）](records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-verdict-v1.md) — SHA-256 `68757e8b8583199dab95ffb6f5f9a43609f94fcb7acde04b53ec6bfff0233a3a`
- [契約010実装Evidence（RED→緑・導線・手戻り記録）](records/development/2026-08-16-reviewer-launch-adapter-implementation-evidence-v1.md) — SHA-256 `9c7863e10f6fae2b654c85b17b0edb7493e47412f19218ae28ed5ee5d7ff58c5`
- [契約010採用と実装開始のHuman判断record](records/development/2026-08-16-reviewer-launch-adapter-contract-adoption-decision-v1.md) — SHA-256 `351e57108293255989d345a9936cbdb122cc4f6695df7c52b4ff2856ded0a983`
- [受入済みの契約010候補v2](records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md) — SHA-256 `7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a`
- [レビュー実行体制の正式ツール化 統合検討v1（agy訂正済み）](records/development/2026-08-16-review-tooling-formalization-study-v1.md) — SHA-256 `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0`
- [暫定レビュー体制の決定（fallbackとして残置）](records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md) — SHA-256 `1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

利用者が後続の縦切りの順序を選ぶ：**縦A（依頼組み立て器）**＝依頼promptの機械組み立て・機械検査
（作成時の内容機微検査を論点に含む。全レビューの品質と省力化）、**第2縦切り（claude-subagent backend）**＝
Tier 2／3の宣言・Human受容機構（2 oracle化・突き合わせの近道）、**縦C（合議）**＝判定record比較の上位層、
**API pending解除**のいずれか。選択後、Claudeが事前走査（5手順）→契約候補作成→5段手続き→独立確認
（正式経路：agy headless起動）→採用判断の順で進める。

開始条件：

- 受入判断record・設計方針メモと本TODOが意味単位commitへ固定され、作業treeがcleanである

完了条件：

- 後続順序の利用者選択がchatで得られる

後続作業：選択された縦の事前走査→契約候補作成→独立確認→採用→RED→実装→レビュー→受入。

## blocker・Human判断待ち

- blocker：codexCLIのトークン枯渇は継続（第3 backend候補として疎通回復待ち）。レビュー実行は契約010のagy headless経路が正式経路であり、実務上のblockerは解消
- Human判断待ち：後続の縦切りの順序選択（縦A／claude-subagent／縦C／API pending解除）

## stale・deferred

- stale：契約008・009・010の進行中表示（三契約とも受入完了）。E2E第1〜6試行の停止事象（第7試行成功と各Evidenceで解消）。「独立確認＝Gemini手動・Human中継」の表示（正式経路はadapter起動。手動体制はfallback）
- deferred：**外部API直接送信経路の後続はpending**（2026-08-16。対象：応答解析・監査自動化・旧egress設計統合・複数送信・API経路への運搬移行判断・external_send_approved表示の観測登録。送信路自体は受入済みで利用可能なまま。再開は利用者指示による。統合する場合もbackend合流でなく判定record規約への準拠とする——設計方針メモ§3）。Reviewer側digest実計算のための特定command許可（shasum等）は将来の契約改定候補。5手順事前走査の手順書化は改善候補のまま

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約010対象35件（`tests/test_reviewer_launch.py`）、G30運用契約実行75件、layout 13件——各単独終了コード0
- 直近の全Test：禁止認証隔離条件の正規全試験2,410件成功・終了コード0（受入record・設計方針メモ・TODO更新後の再実行）。通常host環境の既存executor安全拒否12件は既知事象で退行なし
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
