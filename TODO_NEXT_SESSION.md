# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段、第2段、第3段は完了した。次は第4段の範囲固定であり、第4段の実施と完了はまだ行っていない。
- 現在作業：利用者が第3段完了を承認した。完了範囲、三種類の再開条件、対象Issueをregisteredで維持する条件、第4段への引継ぎを完了Decisionへ固定した。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：第3段の完了は妨げない。状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する、次：Issue状態を変更せず、第4段の正式製品コード識別と最初の製品処理候補の範囲固定へ進む

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [第3段完了判断](records/development/2026-08-14-recovery-plan-v5-stage3-completion-decision-v1.md) — SHA-256 `88578d3160b046cb99c847aaaa6eb4d1ce7b6ee430d4708cfa23bc559edbe0f1`
- [三種類の確認条件と扱いの判断](records/development/2026-08-14-stage3-deferred-quality-concerns-trigger-and-routing-decision-v1.md) — SHA-256 `56ab15aa55c9eeb6775247269bd78827ff1030f4830d335a5d16c43fde57ef34`
- [第4段の正式製品コード識別の追補判断](records/development/2026-08-14-recovery-plan-v5-stage4-formal-product-code-identification-amendment-decision-v1.md) — SHA-256 `1e21e6af4be4898e98436206b950efed4e6cca825397fbc85a9030455e5e94e3`
- [第4段の軽量整理と製品機能候補を分ける追補判断](records/development/2026-08-14-recovery-plan-v5-stage4-lightweight-code-cleanup-boundary-amendment-decision-v1.md) — SHA-256 `d54a486c93a6d0f25411765f99a7fdb669edfb1db84c7a9298a2d9b5dfb8e70a`

## 次に行う一作業

第4段の最初の軽量作業票を作る。参照する上流文書、コードの母集合、用途と採否の二軸分類、最初の製品処理候補の選定基準、対象外、確認の深さ、停止条件を固定する。コード・試験・設定を変更せず、Task Contractの実装を始めない。

開始条件：

- 第3段完了Decisionと第4段の二つの追補判断のSHA-256が実fileと一致する
- 対象Issueがregistered、issue_resolution_v4.pyが暫定・使用停止のままである
- 第4段を読み取りと候補作成に限定し、最初のTask ContractやREQ-WORKFLOW-009の実装を前倒ししない

完了条件：

- 上流文書、コードの母集合、二軸分類語彙、選定基準、対象外、確認方法、停止条件を作業票へ固定する
- 製品、開発支援、共有、用途不明と、採用候補、保留、使用停止、履歴のみを混同しない
- 最初の製品処理から到達するコードだけを詳しく確認し、他のコードへ一律の詳細確認を課さない
- 作業担当と異なる新規サブエージェントの独立開始前レビューを行い、利用者へ開始判断を戻す

後続作業：開始可と利用者承認の後、Git実状態からコードを機械列挙し、意味的に完結する単位ごとに用途と今後の扱いを分類する。

## blocker・Human判断待ち

- blocker：なし。第3段は利用者承認により完了し、第4段の範囲固定へ進める。
- Human判断待ち：第4段の軽量作業票と独立開始前レビューを提示した時点で、固定範囲で開始するかを判断する。

## stale・deferred

- stale：第3段の17件候補・495参照、試験数削減、全試験の詳細人手確認は第4段の入力にしない。第3段完了候補のHuman判断待ちは第3段完了Decisionにより解消した。
- deferred：三種類の品質問題は具体的な開始条件が成立した範囲だけ扱う。ISSUE-TEST-GROWTH-STATE-PINNING-001はregistered、ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001とissue_resolution_v4.pyは使用停止のまま維持する。Work 8、最初のTask Contract、REQ-WORKFLOW-009の採用・実装は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：第3段の正しい現在状態確認は1,728件成功、失敗0。成果物分類は127 path、未分類0、重複0、役割終了0。Claude全体レビューはverified。第3段完了後のコード・試験変更はない。
- 直近の全Test：履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。観測commit以後のtests・tools・config・pyproject・conftest差分0を確認済み。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
