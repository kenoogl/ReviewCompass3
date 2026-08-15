# TODO_NEXT_SESSION

更新日：2026-08-16

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：候補3のG24について、「一件の要求候補整合検査」の実装が完了した。対象試験111件・関連59＋21＋107件・隔離条件の正規全試験2,238件が各単独成功し、正式実行名の合成一件E2Eも成功した。次はCodexによる独立完了レビュー（受入条件21）である。G24全体の作成責務は未完了のまま後続に残る。
- Task Contract：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005 / v3 / implemented_independent_completion_review_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [実装成功Evidence（RED・GREEN・全試験・合成E2E）](records/development/2026-08-16-one-requirement-candidate-consistency-check-green-evidence-v1.md) — SHA-256 `50386e4a981e039e21af3bcec1fb3c37ba078739ff506b9afa19d63d806be6d2`
- [利用者による縮小境界・契約v3採用・案C実装開始の承認](records/development/2026-08-15-one-requirement-candidate-consistency-check-adoption-decision-v1.md) — SHA-256 `35eb9a0b34d6ecf3e7d503498ca0a0f04234fd4519c33eecee3b816cf8dd5c41`
- [Codexによる契約候補v3限定再確認・開始可判定](records/development/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3-limited-rereview-v1.md) — SHA-256 `94f2650b0a5a96b273370c15e07097f5fc5675a700ad2597ab4165cb7809678b`
- [採用された一件の要求候補整合検査契約v3](records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md) — SHA-256 `7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- [利用者が条件20を満たしたG08製品受入判断](records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md) — SHA-256 `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

Claudeが独立完了レビューの依頼recordを作成・commitし、codex execでCodexを起動する。Codexは実装済み製品を
成果物変更なしでレビューし（受入条件21：誤合格・未接続・禁止作用・上位目的への悪影響の反証）、判定record 1件を
単独commitして停止する。判定後の照合と利用者への受入提示はClaudeが実施する。

開始条件：

- 実装一式と成功Evidence、本TODOが意味単位commitへ固定され、作業treeがcleanである
- Codexは製品コード、既存試験、契約、G08、既存G24を変更せず、判定record 1件だけを作成する

完了条件：

- Codexが対象・関連・安全表示・正規全試験の各単独成功と、固定commitの誤合格・未接続・禁止作用・
  上位目的への悪影響0件を確認し、判定recordを単独commitする
- Claudeが判定recordの鮮度・変更path 1件・判定内容を機械照合する

後続作業（Claudeが実施）：レビュー合格なら利用者へ受入条件23の製品受入（G24全体ではない縦切りの限界と後続未完了の確認を含む）を一判断として求め、不合格なら指摘だけを最小修正して再レビューへ戻る。

## blocker・Human判断待ち

- blocker：技術blockerなし
- Human判断待ち：独立完了レビュー用のCodex起動指示。レビュー合格まで製品受入の判断を求めない

## stale・deferred

- stale：契約候補v2系の表示、v3の再確認待ち・実装開始待ちの表示はstale
- deferred：G24の要求作成責務、現行要求変更、候補4以降、外部送信、実利用者要求資料の使用は後続境界まで対象外。`.gitignore`のclaude-to-codex無視規則とrecord正本方式の食い違いは本線の区切りで改善候補として登録する

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
