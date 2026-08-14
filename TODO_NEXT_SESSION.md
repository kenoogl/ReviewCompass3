# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、内部とClaudeの独立全体レビュー、第5段完了判断まで完了した。
- 現在作業：立て直し計画v5は完了した。次の製品作業候補は、一件のSession記録と伏字化結果を安全な別領域へ保存して再読込みする範囲について、二つ目のTask Contract候補の定義挑戦を行うことである。開始判断は未実施で、保存機能の実装は未承認である。
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001 / completed_product_accepted_stable_stage5_completed`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：立て直し計画v5の完了と次のTask Contract候補の開始判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済み立て直し計画v5](docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md) — SHA-256 `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c`
- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [第5段完了候補の内部独立全体レビュー](records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-independent-overall-review-v1.md) — SHA-256 `0ff20a88464ad6b7121842a21194c073034f5396bd59de7250e1b1f3b685eda4`
- [Claudeによる第5段完了候補の全体レビュー結果](records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-claude-overall-review-result-v1.md) — SHA-256 `4a2a8d91e978447f4356cc4da87261074d0c07237bf93aa2cf5aa7015d7bda9e`
- [G25最初のTask Contract](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`

## 次に行う一作業

一件のSession記録と伏字化結果を安全な別領域へ保存して再読込みする範囲について、二つ目のTask Contract候補の定義挑戦を開始するかを利用者が判断する。

開始条件：

- 第5段完了判断と最初のTask Contractの内容識別値が実fileと一致する
- 開始対象を二つ目のTask Contract候補の定義と独立した定義挑戦だけに限定する
- G26の既知反例を未解消として維持し、G26・暫定計画・暫定要求・保存機能を自動的に正式化または実装しない

完了条件：

- 利用者が定義挑戦を開始するかを明示する
- 開始する場合は定義対象、対象外、三案比較、停止条件、独立レビュー範囲を別作業票へ固定する
- 開始しない場合は最初の製品入口を正式・安定のまま維持し、次候補を未開始として残す

後続作業：開始が承認された場合にだけ、二つ目のTask Contract候補を作成して独立した定義挑戦を行う。実装開始は契約の意味とレビュー結果を確認した後に別判断とする。

## blocker・Human判断待ち

- blocker：コード上のblockerはない。二つ目のTask Contract候補の定義挑戦を開始する利用者判断が未実施である。
- Human判断待ち：二つ目のTask Contract候補の定義挑戦を開始するか。定義挑戦と保存機能の実装開始は分けて判断する。

## stale・deferred

- stale：第5段完了候補の判断待ち表示は第5段完了判断によりstaleである。最初の実装Evidenceにある絶対path一般化、状態識別値4251a948...の結び付きと、それに依存した判定もstaleのまま現在根拠へ戻さない。
- deferred：利用者の別承認前に、二つ目のTask Contract作成、G26、G30、他142 path、上流9文書、保存、探索、外部送信、環境値解決、不可逆操作、権限変更、使用停止Issue処理は開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：正式・安定表示への独立レビューで、新入口12件とG25直接関連55件が成功し、昇格前後の同じ合成入力に対する出力がバイト単位で一致した。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を履歴付き複製で確認した。その後の製品コード・試験・設定・配布入口の差分0件を内部全体レビューで確認し、再実行せず結果を利用した。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
