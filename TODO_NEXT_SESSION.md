# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段・第2段は完了し、第3段は完了候補の実施・独立確認・手動全体確認まで終えた。残るのは利用者による段完了判断である。
- 現在作業：Claudeによる第3段完了前の全体確認はverified、止める指摘0件、報告不一致0件だった。返答を証跡へ保存し、固定材料10件と主要な差分主張を操縦役が再照合した。
- Task Contract：`none（ブートストラップ立て直し中のため未導入）`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了のHuman判断待ち`、影響：第3段の誤拒否確認は完了候補になったが、宣言file化と変異検査を将来扱う元Issueの未解決範囲は残る、次：第3段完了を承認するか利用者が判断し、承認時もIssueはregisteredのままWork 8へ残す

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [試験増加・状態固定Issueの現在有効性判断](records/development/2026-08-13-test-growth-state-pinning-current-validity-decision-v1.md) — SHA-256 `1609dfdd76b25c86b38bd105f4199cbbc1636614c5f68256fdee61879c3bddac`
- [正しい実装例による方法への修正判断](records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-decision-v1.md) — SHA-256 `76aa813046a07176650e0bc5db5d5308f569a8e51011f15cd2c21341852e0d2f`
- [既知の正しい現在状態による独立完了レビュー](records/development/2026-08-14-stage3-known-correct-state-witness-independent-completion-review-v1.md) — SHA-256 `623095ce50005400977749fa323e6bea00213db46b9487651ea42e01337afd97`
- [成果物ライフサイクル整理の独立完了レビュー](records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-independent-completion-review-v1.md) — SHA-256 `ea06bdb6566bc7e9f5653fa8a45e573b2966aed12e2e70fcd6de0a482a1544c8`
- [第3段完了候補](records/development/2026-08-14-stage3-completion-candidate-v1.md) — SHA-256 `ab9fe71622c435a8e01bf1385d682ae66814f77928edaf648fd3b3355eb6b1e4`
- [Claudeによる第3段完了前全体レビュー結果](records/development/2026-08-14-stage3-completion-claude-overall-review-result-v1.md) — SHA-256 `289e804b1aae736503aaea5ae8efe2b11c309feb8595e2bac8d7c70d514b9ef9`

## 次に行う一作業

利用者が第3段完了を承認するか判断する。承認前に完了Decision、Issue状態変更、第4段開始を行わない。

開始条件：

- 第3段完了候補、二つの独立完了レビュー、Claude全体レビュー結果のSHA-256が実fileと一致する
- Claude全体レビューがverified、止める指摘0件、報告不一致0件で固定されている
- ISSUE-TEST-GROWTH-STATE-PINNING-001がregisteredであり、段完了とIssue解決を混同しない

完了条件：

- 利用者が第3段完了の可否を明示する
- 承認の場合、二確認点への限定、三種類のWork 8等への分離、1,728件を恒久値にしないことを完了Decisionへ引き継ぐ
- 承認の場合も対象Issueをregisteredのまま維持し、状態更新処理を自己適用しない
- 不承認の場合、中心判断を崩す一原因と最小訂正範囲だけを別作業として固定する

後続作業：第3段完了承認を記録し現在位置を更新した後、立て直し計画v5の第4段へ進む。

## blocker・Human判断待ち

- blocker：技術的blockerはない。第3段完了のHuman判断だけが残る。
- Human判断待ち：第3段完了を承認するか。推奨は、対象Issueをregisteredのまま維持する条件付きで承認すること。

## stale・deferred

- stale：参照文字列による17件候補・495参照、全試験の詳細人手確認、試験数削減、実行時間短縮は第3段の現役入力・完了条件にしない。
- deferred：誤った実装の受理、守れない保証表示、安全方針に反する副作用の見逃し、状態固定の宣言file化、変異検査は必要時のWork 8または通常開発へ残す。ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001と暫定issue_resolution_v4.pyも使用停止のまま維持する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：正しい現在状態の独立確認は1,728件成功、失敗0。成果物分類は127 path、未分類0、重複0、役割終了0。Claude全体レビューもverified。
- 直近の全Test：履歴付き一時複製で正規全試験1,728件成功、失敗・error・skip 0、終了コード0。観測commit以後のtests・tools・config・pyproject・conftest差分0を再確認した。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
