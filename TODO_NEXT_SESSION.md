# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：第2のTask Contract v3は採用済みで、案Cの実装準備と実装開始も利用者が承認した。製品コード着手前にTDD実装境界を確認する規則を現行開発方針へ追加し、現役チェックリストの参照値も更新した。次は契約の22受入条件を、一回の失敗確認と最小実装で扱える単位へ分ける。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_boundary_precheck_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：案CのTDD実装境界確認を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [安全保存Task Contract v3の採用判断](records/development/2026-08-15-session-artifact-safe-storage-task-contract-adoption-decision-v1.md) — SHA-256 `83e533ea40655bbedce4087abfe071ba3d9d63fb6f5764744886de82ba5a2ff2`
- [案Cの実装開始判断](records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md) — SHA-256 `f8c55611de59cd25946aa27bb4330ca66bbf1cf751baba6c5fe5c19a3ec1d45f`
- [TDD開始前の実装境界確認を含む現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `e3e3f904dff8b4e14a6557e794185db14b3d5acc581bb80bb4f4844886e4c7f8`
- [TDD実装境界確認の方針変更判断](records/development/2026-08-15-tdd-implementation-boundary-precheck-policy-decision-v1.md) — SHA-256 `5c844a835b272283eb7ac485e2f5e4be792b7ded6dcf4d600054934a1007edfd`

## 次に行う一作業

採用済み契約の22受入条件をTDDで扱える実装単位へ分け、案Cの小さい実装作業票を作成して独立開始前レビューを行う。

開始条件：

- 採用済み契約、実装開始判断、現行開発方針の内容識別値が実fileと一致する
- 各単位をfile数ではなく、利用者から見た意味のある状態変化と一つの主要な失敗理由で分ける
- 各単位へ入力・出力、先行する失敗試験、最小実装、先取りしない責務、完了状態、前後の依存、停止条件を対応付ける
- 未完成機能を配布用実行名へ接続せず、G26全体、G30、上流候補を範囲へ含めない

完了条件：

- 22受入条件の全てが一つ以上の実装単位または最終全体確認へ重複なく説明可能な形で対応する
- 一つの試験が複数の未実装責務だけを理由に失敗する単位と、意味のない過細分化が残らない
- 新しい独立担当が実装粒度、依存順、安全境界、製品入口への公開時点を反証し、開始可否を記録する
- 開始可以外なら製品コードを変更せず、原因を利用者へ戻す

後続作業：独立開始前レビューが開始可の場合だけ、最初の実装単位の試験を先に追加して失敗を確認する。

## blocker・Human判断待ち

- blocker：製品実装を止める既知の欠陥はないが、TDDで扱える実装境界の事前確認が未完了であるため、製品コード着手は停止中である。
- Human判断待ち：現時点で追加判断はない。実装境界を定められない場合、または契約・実装順序の変更が必要になった場合だけ利用者へ戻す。

## stale・deferred

- stale：方針変更前のSHA-256を現行開発方針として使わない。過去の作業票と記録にある旧値は当時の固定材料として保持する。
- deferred：開始前レビュー合格まで、失敗試験、製品コード、設定、配布入口を変更しない。G26・G30・上流候補の正式化、探索、複数記録処理、外部送信、環境値解決、自動削除も開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：開発方針変更後、現役チェックリストの既存参照検査19件が成功した。製品コード・試験・設定は変更していないため、製品試験は再実行していない。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功、失敗・error・skip 0、終了コード0を確認した。その後は文書と記録だけが追加され、製品コード・試験・設定・配布入口は変更していないため再実行していない。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
