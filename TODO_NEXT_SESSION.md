# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：候補3のG24について、契約候補v3はCodex限定再確認で開始可（blocking 0件）となり、利用者が縮小境界・契約v3採用・案C実装開始を承認した。Claudeが契約§13の順（失敗試験の固定→最小実装）で「一件の要求候補整合検査」を実装する。G24全体の作成責務は未完了のまま後続に残る。
- Task Contract：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005 / v3 / adopted_implementation_started`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者による縮小境界・契約v3採用・案C実装開始の承認](records/development/2026-08-15-one-requirement-candidate-consistency-check-adoption-decision-v1.md) — SHA-256 `35eb9a0b34d6ecf3e7d503498ca0a0f04234fd4519c33eecee3b816cf8dd5c41`
- [Codexによる契約候補v3限定再確認・開始可判定](records/development/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3-limited-rereview-v1.md) — SHA-256 `94f2650b0a5a96b273370c15e07097f5fc5675a700ad2597ab4165cb7809678b`
- [採用された一件の要求候補整合検査契約v3](records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md) — SHA-256 `7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- [利用者が条件20を満たしたG08製品受入判断](records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md) — SHA-256 `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

Claudeが契約v3の対象試験`tests/test_one_requirement_feature_source.py`を受入条件1〜22に対応する失敗試験として先に固定し、
期待どおり失敗することを確認してから、検査核`tools/requirements/one_requirement_feature_source.py`、
入口`tools/requirements/one_requirement_feature_source_entry.py`、`pyproject.toml`の実行名一件の最小実装で合格させる。

開始条件：

- 採用判断record、本TODOが意味単位commitへ固定され、作業treeがcleanである
- 変更は契約§12の上限（検査核・入口・実行名・対象試験・作業票／Evidence／TODO）に限定する
- §6の固定部品・保護10 path、要求schema、現行50要求、他製品処理を変更しない

完了条件：

- 対象試験が受入条件1〜22を覆い、失敗確認を経て最小実装で全件成功する（各単独command・終了コード0）
- G24関連59件、要求資料関連21件、G08対象107件、保護10 path差分0が退行しない
- 正規全試験の単独成功後、独立完了レビューと利用者受入（受入条件21〜23）へ進む

後続作業：独立完了レビューをCodexへ依頼し、合格後に利用者の製品受入（受入条件23）を求める。

## blocker・Human判断待ち

- blocker：技術blockerなし
- Human判断待ち：なし。実装完了後の独立完了レビュー合格まで、段完了・製品受入の判断を求めない

## stale・deferred

- stale：契約候補v2系の表示、v3の再確認待ち表示、Codex起動待ち表示はstale
- deferred：G24の要求作成責務、現行要求変更、候補4以降、外部送信、実利用者要求資料の使用は後続境界まで対象外。`.gitignore`のclaude-to-codex無視規則とrecord正本方式の食い違いは本線の区切りで改善候補として登録する

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
