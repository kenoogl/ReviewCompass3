# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存Task Contract候補v3を、第2のTask Contractとして利用者が採用した。採用判断は対象契約と独立レビューの内容識別値へ結び付けて固定した。保存機能の案Cと実装開始は未承認であり、別の利用者判断へ戻す段階である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_not_approved`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：安全保存Task Contractの案Cと実装開始判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [候補v3の一時file一点限定レビュー](records/development/2026-08-15-session-artifact-safe-storage-task-contract-temporary-file-correction-review-v1.md) — SHA-256 `22ae12fd33d147cdb873bfb81ac786f096a2fccbb00ece4fcc9419d60ee1ab84`
- [安全保存Task Contract v3の採用判断](records/development/2026-08-15-session-artifact-safe-storage-task-contract-adoption-decision-v1.md) — SHA-256 `83e533ea40655bbedce4087abfe071ba3d9d63fb6f5764744886de82ba5a2ff2`

## 次に行う一作業

案Cの実装準備と実装開始へ進むかを、利用者が別に判断する。

開始条件：

- 採用済み契約v3と採用判断の内容識別値が実fileと一致する
- 案Cが、正式な読取り専用入口から安全な結果を値で受け、一件専用の保存処理と保存入口を追加して、保存・再読込み・期限後拒否・明示削除を行う機能だと理解する
- 実装前に変更pathを小さい作業票へ固定し、失敗確認、最小実装、関連試験、通常の全試験、高危険度境界の反証、独立完了レビューの順で進める
- G26全体、G30、上流候補、探索、複数記録処理、外部送信を実装範囲へ含めない

完了条件：

- 利用者が案Cの実装準備と実装開始を承認するか、承認せず停止するかを明示する
- 承認する場合は変更path、失敗確認、停止条件を実装前の小さい作業票へ固定し、独立開始前レビューを行う
- 承認しない場合は採用済み契約を保持し、製品コード・試験・設定を変更しない

後続作業：実装開始が承認された場合だけ、三案比較済みの案Cを小さい作業票へ具体化し、独立開始前レビューへ進む。承認だけで直ちにコードを書かない。

## blocker・Human判断待ち

- blocker：技術的な止める指摘はない。採用済み契約に従う案Cの実装開始が、利用者の別判断待ちである。
- Human判断待ち：案Cの実装準備と実装開始を承認するか。案Cは、一件だけを明示した二領域へ安全に保存し、派生結果だけを再読込みし、期限後は拒否し、確認後に一件だけ削除する専用機能を作る案である。

## stale・deferred

- stale：候補v1・v2は契約採用・実装開始の現役根拠に使わない。候補v3先頭の作成時状態は履歴表示であり、現在の採用状態は採用判断記録を正本とする。
- deferred：別承認前に、保存機能の実装、コード・試験・設定・配布入口の変更、G26・G30・上流候補の正式化、探索、複数記録処理、外部送信、環境値解決、自動削除を開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：契約採用は文書上の意味的判断であり、製品コード・試験・設定を変更していないため製品試験を再実行していない。候補v3の一点限定レビューはverified、止める指摘0件である。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を確認した。その後は文書と記録だけが追加され、製品コード・試験・設定・配布入口は変更していないため再実行していない。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
