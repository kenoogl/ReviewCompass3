# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存Task Contract候補v3を作成し、一時file境界だけの独立変更点レビューを完了した。判定はverified／開始可、止める指摘0件、報告不一致0件である。候補v3の採用と案Cの実装開始は未承認であり、二つを別々の利用者判断へ戻す段階である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / candidate_v3_verified_pending_human_adoption`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：安全保存Task Contract候補v3の採否判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [安全保存Task Contract候補v2の変更点限定レビュー](records/development/2026-08-15-session-artifact-safe-storage-task-contract-definition-correction-review-v1.md) — SHA-256 `6408d28e92fed3ebb62a2d8ea716d2b4af5d273a362b6d6437c15bd290f8cbb7`
- [安全保存Task Contract候補v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [候補v3の一時file一点限定レビュー](records/development/2026-08-15-session-artifact-safe-storage-task-contract-temporary-file-correction-review-v1.md) — SHA-256 `22ae12fd33d147cdb873bfb81ac786f096a2fccbb00ece4fcc9419d60ee1ab84`

## 次に行う一作業

候補v3を第2のTask Contractとして採用するかを利用者が判断する。

開始条件：

- 候補v3と一点限定レビューの内容識別値が実fileと一致する
- 契約の機能が、許可されたSession記録一件を機微情報用領域へ保存し、許可項目だけの派生成果物を別領域へ保存・再読込みし、期限超過を拒否し、明示確認付きで一記録を削除する範囲だと理解する
- 候補v3の採用には製品コード、試験、設定の変更や、G26・上流候補の正式化を含めない

完了条件：

- 利用者が候補v3を採用するか、採用せず停止するかを明示する
- 採用する場合は対象契約と限界をDecisionへ固定する
- 採用しない場合は保存機能の実装を開始しない

後続作業：候補v3が採用された場合だけ、案Cの実装開始を別のHuman判断として提示する。契約採用を実装承認として扱わない。

## blocker・Human判断待ち

- blocker：技術的な止める指摘はない。候補v3は独立確認済みだが、利用者による契約採用が未実施である。
- Human判断待ち：候補v3を第2のTask Contractとして採用するか。これは案Cの実装開始、製品コード変更、G26または上流候補の正式化の承認ではない。

## stale・deferred

- stale：候補v1・v2は各独立レビューでcorrection_requiredとなり、契約採用・実装開始の現役根拠に使わない。指摘と訂正の経緯は履歴Evidenceとして保持する。
- deferred：候補v3の採用前、および採用後の別承認前に、保存機能の実装、コード・試験・設定・配布入口の変更、G26・G30・上流候補の正式化、探索、外部送信、環境値解決、不可逆操作、権限変更を開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：候補v3の一点限定レビューは契約文の状態遷移と一時file境界の反証に限定し、製品試験を再実行していない。製品コード・試験・設定は変更していない。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を確認した。その後は文書と記録だけが追加され、製品コード・試験・設定・配布入口は変更していないため再実行していない。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
