# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存Task Contract候補v2を作成し、先行指摘だけの独立変更点レビューを完了した。相対path除外、固定fileの途中状態、削除再試行、値受渡し、macOS権限は解消したが、一時fileが保持・削除対象へ未接続のため判定はcorrection_required／実装開始不可である。修正の修正となるため自動継続せず、v3の一点訂正を行うかが利用者判断待ちである。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / candidate_v2_correction_required_not_approved`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：安全保存Task Contract候補の訂正判断を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [立て直し計画v5第5段完了判断](records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md) — SHA-256 `4c50bdf643c12e3c4fb02c78d3fe47de20885efab4b8b9b34dbd946c763da3b0`
- [安全保存Task Contract候補v1の独立定義挑戦](records/development/2026-08-14-session-artifact-safe-storage-task-contract-definition-challenge-v1.md) — SHA-256 `cce6fb9a94da7cfe81541ebdccf8d0707eb07041f775b3c59969f5e8b937fd65`
- [安全保存Task Contract候補v2](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v2.md) — SHA-256 `c42c36a1ec389409892cf990116055bee301a29008c44f4e9fed9d03d4811163`
- [安全保存Task Contract候補v2の変更点限定レビュー](records/development/2026-08-15-session-artifact-safe-storage-task-contract-definition-correction-review-v1.md) — SHA-256 `6408d28e92fed3ebb62a2d8ea716d2b4af5d273a362b6d6437c15bd290f8cbb7`

## 次に行う一作業

一時fileだけを契約の固定対象へ接続する候補v3の一点訂正へ進むかを利用者が判断する。

開始条件：

- 候補v2と変更点限定レビューの内容識別値が実fileと一致する
- 訂正を、各一時fileの決定的な名前、operation.jsonの期待値、incomplete・保持期限・plan-delete・deleteへの接続、および権限対象を各保存rootと明記する一点に限定する
- 製品コード、試験、設定、既存契約、G26、上流候補を変更または正式化しない

完了条件：

- 利用者が修正の修正となる候補v3の一点訂正へ進むかを明示する
- 進む場合は契約候補v3だけを作成し、一時fileの接続だけを一回確認する
- 進まない場合は候補v2を未承認・実装開始不可のまま維持する

後続作業：候補v3の一点確認が合格した場合だけ、契約採否と実装開始を別々の利用者判断へ戻す。

## blocker・Human判断待ち

- blocker：書込み途中の一時fileが固定file一覧、保持期限、削除計画、削除対象へ含まれず、中断後に一記録だけを安全に片付ける経路が閉じていない。
- Human判断待ち：一時fileの決定的な名前と期待する内容識別値をoperation.jsonへ固定し、incomplete判定、保持期限、plan-delete、deleteへ含める候補v3の一点訂正へ進むか。これは契約採用、実装開始、製品コード変更の承認ではない。

## stale・deferred

- stale：候補v2は独立変更点レビューでcorrection_requiredとなり、契約採用・実装開始の根拠に使わない。v2で解消済みの相対path、削除再試行、値受渡し、macOS権限の確認結果は、一時fileの一点訂正で変更しない限り有効である。
- deferred：利用者の判断前に候補v3を作成せず、別承認前に保存機能の実装、G26、G30、上流候補、探索、外部送信、環境値解決、不可逆操作、権限変更を開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：候補v2の変更点限定レビューは契約文の反証に限定し、製品試験を再実行していない。製品コード・試験・設定は変更していない。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を確認した。その後は文書と記録だけが追加され、製品コード・試験・設定・配布入口は変更していないため再実行していない。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
