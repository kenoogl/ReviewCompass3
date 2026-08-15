# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段、G25読取り専用入口、一件用安全保存、一件レビュー材料作成・結果整理、G08一件設計・受入条件照合の製品受入が完了した。残る6候補を順に実行中である。
- 現在作業：候補2のG08は利用者判断により正式受入となった。候補3のG24について、要求固定・機能分割・由来追跡の既存5fileと関連試験、上流文書候補の不一致、利用者価値境界を実測し、Task Contract候補の根拠を作る。
- Task Contract：`G24 / requirement_fixing_feature_partition_source_trace / contract_definition_evidence_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：現在のG24契約定義を妨げず、立て直し計画を未完了へ戻さない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [利用者が条件20を満たしたG08製品受入判断](records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md) — SHA-256 `7e3eb626474f72ebcd3a3d5ec2646cf004ba192606f03684a50ae6f0b251ce86`
- [G08の条件1〜19をverifiedとした独立再確認](records/development/2026-08-15-one-design-acceptance-independent-correction-rereview-v1.md) — SHA-256 `8a4793e617f9d0ce3204ba6c2bc85ce309afb75df0d7add988a8bcb270eda7bc`
- [G24を候補3とした次製品作業候補](records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md) — SHA-256 `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba`
- [G24の既存5fileと5試験fileを示す製品候補目録](records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md) — SHA-256 `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559`

## 次に行う一作業

G24の既存5実装file・5試験file、参照する上流要求資料、現行入口と副作用を機械抽出し、目的・使える部分・危険・最小製品境界を一件の契約定義Evidenceへ固定する。

開始条件：

- G08製品受入Decisionと本TODOが意味単位commitへ固定される
- G24の既存成果物を変更せず読取り専用で実測する
- 暫定文書を正式要求へ自動昇格せず、上流不一致を先に列挙する

完了条件：

- 5実装file・5試験fileの存在、内容識別値、公開関数、作用、関連試験結果を固定する
- 上流資料候補の一致・不一致と、採用せず保留する入力を示す
- 異なる3実装案を比較し、最小製品境界をTask Contract候補へ接続する

後続作業：G24のTask Contract候補を別担当の定義確認へ渡し、開始可の場合だけ利用者へ採用・実装開始判断を求める。

## blocker・Human判断待ち

- blocker：なし。G24の上流資料不一致は本調査で確定する
- Human判断待ち：なし。G08製品受入は完了し、G24は契約候補作成まで承認済みの自律実行範囲

## stale・deferred

- stale：G08の製品受入待ち、独立再確認待ち、形式検査修正待ちの表示はstale
- deferred：G24契約の採用・製品実装、候補4以降、外部送信、実利用者要求資料の使用は後続境界まで対象外

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：G08対象107件、既存G08関連31件が各単独成功、終了コード0。G24関連試験は契約定義Evidence作成時に単独実行する
- 直近の全Test：禁止認証環境6件を除く隔離条件で正規全試験2,127件成功、終了コード0。通常host環境の既存executor安全拒否はG08独立確認で退行なしと判断済み
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
