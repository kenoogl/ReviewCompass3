# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：候補3のG24について、既存5実装・5試験、旧37要求と現行50要求の権限差、3反例を固定し、一件の要求・機能区分・出典対応のTask Contract候補v1を作成した。固定commit後の独立定義確認へ進む。
- Task Contract：`TC-RC3-PRODUCT-ONE-REQUIREMENT-FEATURE-SOURCE-005 / v1 / independent_definition_review_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者が条件20を満たしたG08製品受入判断](records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md) — SHA-256 `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86`
- [G24一件処理の目的、上流不一致、3反例、3案比較を固定した契約定義証拠](records/development/2026-08-15-one-requirement-feature-source-contract-definition-evidence-v1.md) — SHA-256 `9d35dc70f5d96eb497bd8530ced4a1b32d5d838a6c0503f24668d8be719987c6`
- [独立定義確認待ちのG24作業契約候補v1](records/task-contract/2026-08-15-one-requirement-feature-source-candidate-v1.md) — SHA-256 `19702df3b5414b4e271ba30e6fb84ec285c887a98e189ed9bfd88e8ad2df6a25`
- [G24を候補3とした次製品作業候補](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [現行50要求を解決する要求権限束v2](records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json) — SHA-256 `760e33ea2ecf6937f56d7bf8d2bd703b18b47dbd2bd6b2bd5919e0dd556d9dae`

## 次に行う一作業

G24契約定義証拠と作業契約候補v1を意味単位commitへ固定し、別担当へ読取り専用の定義反証を委譲する。

開始条件：

- 契約定義証拠、作業契約候補v1、本TODOの参照内容識別値が一致する
- 関連59試験、要求artifact関連21試験、git diff --checkが各単独成功する
- 明示3pathだけをcommitし、commit後の作業treeがcleanである

完了条件：

- 別担当が目的、上流不一致、二入力、全採否、全義務対応、未昇格を反証する
- 安全読取り、安全表示、変更上限、21受入条件の未固定または誤合格余地を確認する
- 成果物を変更せず開始可または修正要と根拠付きで返す

後続作業：開始可なら利用者へ契約採用と案Cの実装開始を一判断として求め、修正要なら候補を訂正して同じ担当へ再確認する。

## blocker・Human判断待ち

- blocker：なし。固定commit後に独立定義確認を開始できる
- Human判断待ち：なし。独立確認が開始可になるまで契約採用・実装開始判断を求めない

## stale・deferred

- stale：G24契約定義証拠作成待ち、上流資料不一致の調査待ち、関連試験未実施の表示はstale
- deferred：G24契約の採用・製品実装、現行要求変更、候補4以降、外部送信、実利用者要求資料の使用は後続境界まで対象外

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G24既存関連59件、要求artifact関連21件が各単独成功、終了コード0
- 直近の全Test：禁止認証環境6件を除く隔離条件で正規全試験2,127件成功、終了コード0。通常host環境の既存executor安全拒否はG08独立確認で退行なしと判断済み
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
