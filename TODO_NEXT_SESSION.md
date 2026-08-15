# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：候補3のG24について、契約候補v2のClaude独立再確認は停止原因1件で修正要となり、最小修正(a)で契約候補v3を作成した。v3の限定再確認だけを作成者以外のCodexへ依頼する（Claudeがcodex execで起動するrecord正本方式。判定後の後続はClaudeが実施）。製品実装は未開始で、G24全体の作成責務は未完了である。
- Task Contract：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005 / v3 / limited_independent_rereview_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者が条件20を満たしたG08製品受入判断](records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md) — SHA-256 `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86`
- [CodexへのG24契約候補v3限定再確認依頼record](records/session-handoffs/2026-08-15-g24-contract-v3-limited-rereview-codex-request-v1.md) — SHA-256 `47ae10f6ef13e990a0d10a1bd5e292d2849129c4c5267402029f95169a7dc712`
- [G24契約候補v2を停止原因1件で修正要としたClaude独立再確認](records/development/2026-08-15-one-requirement-candidate-consistency-check-contract-v2-independent-rereview-v1.md) — SHA-256 `270505d0f073fb59daf4d963824ca0eb9e2c854c580ed46dde2f63181242eb38`
- [最小修正(a)を限定適用した一件の要求候補整合検査契約候補v3](records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md) — SHA-256 `7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

Claudeが依頼recordを対象にcodex execでCodexを起動し、Codexは契約候補v3の限定再確認（訂正1点の閉鎖と退行の有無だけ）を
行い、判定record 1件を単独commitして停止する。

開始条件：

- 依頼record、本TODOが意味単位commitへ固定され、作業treeがcleanである
- 起動は利用者の指示を受けてClaudeが行い、Codexは依頼record§3の鮮度検査に合格してから動く
- Codexは製品コード、既存試験、G08、既存G24を変更せず、判定record 1件だけを作成する

完了条件：

- §6.2と受入条件13の照合対象がfile内容識別値・公開関数2名・既定pattern件数5だけになり、後決め要素がないことを再反証する
- G24関連59件、要求資料関連21件、G08対象107件、保護10 path差分0を各単独commandで確認する
- 判定recordに開始可または修正要を根拠、未接続条件、最小修正とともに書き、単独commitして停止する
- Claudeが判定recordの鮮度・変更path 1件・判定内容を機械照合する

後続作業（Claudeが実施）：開始可なら利用者へ『G24全体ではない最初の整合検査縦切り』の採用と案Cの実装開始を一判断として求め、修正要なら契約だけを次版へ訂正する。

## blocker・Human判断待ち

- blocker：技術blockerなし。利用者指示により限定再確認の担当をCodex、起動と後続をClaudeとする
- Human判断待ち：Codex起動の指示。起動後、Codexの限定再確認が開始可になるまで、縮小境界の採用と実装開始判断を求めない

## stale・deferred

- stale：契約候補v2の独立再確認待ち、v2の規則内容識別値固定、v2からの実装開始、G24全体を本縦切りで完了できる表示、旧引継ぎメモ（Human運搬前提・後続をCodexへ割り当てた記述）はstale
- deferred：契約候補v3の採用・製品実装、G24の要求作成責務、現行要求変更、候補4以降、外部送信、実利用者要求資料の使用は後続境界まで対象外

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G24既存関連59件、要求artifact関連21件、G08対象107件が各単独成功、終了コード0
- 直近の全Test：禁止認証環境6件を除く隔離条件で正規全試験2,127件成功、終了コード0。通常host環境の既存executor安全拒否はG08独立確認で退行なしと判断済み
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
