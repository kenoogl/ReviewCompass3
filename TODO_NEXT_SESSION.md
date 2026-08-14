# TODO_NEXT_SESSION

更新日：2026-08-14

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：二つ目のTask Contract候補v1を作成し、独立した定義挑戦を完了した。判定はcorrection_required／実装開始不可である。保存内容、二つの保存領域にまたがる途中状態、削除再試行、正式入口からの値受渡しを契約v2で閉じるかが利用者判断待ちであり、保存機能の実装は未承認である。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / candidate_correction_required_not_approved`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：立て直し計画v5の完了と二つ目のTask Contract訂正判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [G25最初のTask Contract](records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md) — SHA-256 `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- [安全保存Task Contract候補v1](records/task-contract/2026-08-14-session-artifact-safe-storage-candidate-v1.md) — SHA-256 `6d0f4984b3144d840b69544c70a71a48a29fe11bcdeeaa0075bddc9e8027a57a`
- [安全保存Task Contract候補v1の独立定義挑戦](records/development/2026-08-14-session-artifact-safe-storage-task-contract-definition-challenge-v1.md) — SHA-256 `cce6fb9a94da7cfe81541ebdccf8d0707eb07041f775b3c59969f5e8b937fd65`

## 次に行う一作業

独立定義挑戦が示した四点だけを反映するTask Contract候補v2を作成するかを利用者が判断する。

開始条件：

- 候補v1と独立定義挑戦の内容識別値が実fileと一致する
- 訂正範囲を、保存用派生物からsource_pathを除くこと、一記録の途中状態と削除再試行を固定fileだけで閉じること、現行表示を変えない値受渡し境界、macOSのdirectory 0700・file 0600相当とsymlinkを追わない開閉の四点に限定する
- 製品コード、試験、設定、G26、G30、上流候補を変更または正式化しない

完了条件：

- 利用者が四点の限定訂正へ進むかを明示する
- 進む場合は契約候補v2だけを作成し、先行指摘だけの一回限り変更点レビューを行う
- 進まない場合は候補v1を未承認・実装開始不可のまま維持する

後続作業：契約候補v2が変更点レビューに合格した場合だけ、契約採否と実装開始を別々の利用者判断へ戻す。

## blocker・Human判断待ち

- blocker：候補v1は永続保存する一記録の内容と全状態遷移が閉じておらず、独立レビューで実装開始不可と判定された。
- Human判断待ち：保存用派生物からsource_pathを除くこと、途中状態の中止・削除と削除再試行を当該record_idの固定fileだけで閉じること、現行の画面出力と終了区分を変えず値受渡し境界を定めること、macOSの所有者限定権限とsymlink非追跡を具体化することの四点を契約候補v2へ限定反映するか。これは契約採用や実装開始の承認ではない。

## stale・deferred

- stale：二つ目のTask Contract候補の定義挑戦開始判断待ちは、利用者の候補1選択と独立定義挑戦完了によりstaleである。候補v1は独立レビューでcorrection_requiredとなり、契約採用・実装開始の根拠に使わない。
- deferred：利用者の訂正判断前に契約候補v2を作成せず、別承認前に保存機能の実装、G26、G30、上流候補、探索、外部送信、環境値解決、不可逆操作、権限変更を開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：独立定義挑戦で正式な読取り専用入口の対象試験3件が成功し、正常結果にprovenance.source_pathが含まれる現在仕様を確認した。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を確認した。その後は文書と記録だけが追加され、製品コード・試験・設定・配布入口は変更していないため再実行していない。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
