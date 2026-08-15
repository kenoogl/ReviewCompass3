# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：候補3のG24について、契約候補v2のClaude独立再確認は停止原因1件（機微情報規則の規則内容識別値が計算方法未定義）で修正要となった。利用者指示の最小修正(a)により、規則内容識別値の固定を撤回しfile内容識別値・公開関数・既定pattern件数の照合へ限定した契約候補v3を作成した。製品実装は未開始で、G24全体の作成責務は未完了である。
- Task Contract：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005 / v3 / limited_independent_rereview_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者が条件20を満たしたG08製品受入判断](records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md) — SHA-256 `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86`
- [G24契約候補v2を停止原因1件で修正要としたClaude独立再確認](records/development/2026-08-15-one-requirement-candidate-consistency-check-contract-v2-independent-rereview-v1.md) — SHA-256 `270505d0f073fb59daf4d963824ca0eb9e2c854c580ed46dde2f63181242eb38`
- [最小修正(a)を限定適用した一件の要求候補整合検査契約候補v3](records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md) — SHA-256 `7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- [4原因を限定訂正した一件の要求候補整合検査契約候補v2](records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v2.md) — SHA-256 `a4d544e29d877ac45dca65b748557387bd1b04f58adda59ffacf91fc47a216bb`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

契約候補v3の作成を担当しなかった別担当が、固定されたv3を成果物変更なしで読み、v2の停止原因1件（規則内容識別値の
計算方法未定義）が閉じたことと、v2で閉じた他境界に退行がないことだけを限定再確認する。

開始条件：

- v2再確認記録、契約候補v3、本TODOが一つの意味単位commitへ固定され、作業treeがcleanである
- 担当はAGENTS.md、TODO、v2再確認記録を読み、Pythonは.venv/bin/python3だけを使う
- 製品コード、既存試験、G08、既存G24を変更せず読取り専用で確認する

完了条件：

- §6.2と受入条件13の照合対象がfile内容識別値・公開関数2名・既定pattern件数5だけになり、後決め要素がないことを再反証する
- G24関連59件、要求資料関連21件、G08対象107件、保護10 path差分0を各単独commandで確認する
- 成果物を変更せず、開始可または修正要を根拠、未接続条件、最小修正とともに返す

後続作業：開始可なら利用者へ『G24全体ではない最初の整合検査縦切り』の採用と案Cの実装開始を一判断として求め、修正要なら契約だけを次版へ訂正する。

## blocker・Human判断待ち

- blocker：技術blockerなし
- Human判断待ち：契約候補v3の限定再確認の担当指定（v3作成はClaudeのため、Claude以外を推奨）。再確認が開始可になるまで、縮小境界の採用と実装開始判断を求めない

## stale・deferred

- stale：契約候補v2の独立再確認待ち、v2の規則内容識別値固定、v2からの実装開始、G24全体を本縦切りで完了できる表示はstale
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
