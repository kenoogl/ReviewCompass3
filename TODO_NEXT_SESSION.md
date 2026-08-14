# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存案Cの実装前コード管理について、検索時点のGit管理コードから対象集合を毎回生成し、Work 4A観測集合との完全一致を開始条件にする方針訂正まで完了した。ライフサイクル区分は別のDecisionから導き、固定pathを中央一覧にしない。次は別機能であるTDD開始前の実装境界確認を行う。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_git_derived_code_search_completed_boundary_precheck_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：TDD実装境界の確認を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [案Cの実装開始判断](records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md) — SHA-256 `f8c55611de59cd25946aa27bb4330ca66bbf1cf751baba6c5fe5c19a3ec1d45f`
- [コード管理とTDD境界確認を分離した現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `befdd34e7051bab35314a485290da9bbddb54c0460576835a2706711cd4923b0`
- [Git起点のコード検索元生成の訂正判断](records/development/2026-08-15-git-derived-code-search-source-correction-decision-v1.md) — SHA-256 `5d25da0636def98d245030175168f1871ba96b3d62eea17941676d14646a3440`
- [実装前コード管理の導線Evidence](records/development/2026-08-15-safe-storage-preimplementation-code-management-routing-evidence-v1.md) — SHA-256 `56fd0603cc2eec478e72834c109c209ca08a3c48c6c79a76488e56b03a2f14b2`
- [実装前コード管理検索の実施Evidence](records/development/2026-08-15-safe-storage-preimplementation-code-management-search-evidence-v1.md) — SHA-256 `bcc7e604201784f5030a7da9ca1b3ed6ac8b64fe05d2bd7864eb3d5b1a0614eb`
- [正式コード検索記録の証明書](records/development/2026-08-15-safe-storage-formal-code-reuse-search-attestation-v1.json) — SHA-256 `a2bfec07d52ef87605645d710dc85980badf99269d65262f68de0a05700dcdb7`
- [保留G26検索記録の証明書](records/development/2026-08-15-safe-storage-provisional-g26-reuse-search-attestation-v1.json) — SHA-256 `d9e81d7abf20f633399ed92902eafb3a0808f2a3d015cd5a70aa186944f54ade`

## 次に行う一作業

コード管理とは別に、TDD開始前の実装境界確認の導線と機械化可能範囲を証跡へ固定し、採用済み契約の22受入条件を意味のある実装単位へ分ける。

開始条件：

- 採用済み契約、実装開始判断、現行開発方針、Git起点の検索元訂正判断、コード管理検索Evidenceの内容識別値が実fileと一致する
- コード管理検索とTDD境界確認を別機能・別判定として扱う
- 機械処理は22条件の対応、必須欄、依存順、公開時点など決定的な照合に限定し、境界の意味判断を自動化しない
- 新しい包括的な台帳、検査器、関門を先に作らず、既存の作業票とレビュー手順へ接続する

完了条件：

- TDD境界確認の入口、機械処理、人の意味判断、独立レビューの役割が別証跡で明確になる
- 22受入条件の全てが一つ以上の実装単位または最終全体確認へ対応し、対応漏れ・重複と必須欄を機械照合できる
- 一つの試験が複数の未実装責務だけを理由に失敗する単位と、利用者価値を持たない過細分化が残らない
- コード管理検索との合否を統合せず、製品コードを変更しない

後続作業：TDD境界の別作業が完了した後、その結果を案Cの小さい実装作業票へ固定し、新規の独立担当による開始前レビューを行う。開始可の場合だけ最初の失敗試験へ進む。

## blocker・Human判断待ち

- blocker：製品実装を止める既知の欠陥はない。Git起点の実装前コード管理検索は完了したが、TDD実装境界の導線と機械確認が未完了であるため製品コード着手は停止中である。
- Human判断待ち：現時点で追加判断はない。TDD境界を定められない場合、契約・実装順序の変更が必要な場合、または保留中G26の個別処理を正式依存へ採用する必要がある場合だけ利用者へ戻す。

## stale・deferred

- stale：2026-08-05の1,003処理一覧と現行方針へ結び付かないsource universe v2・freshness policy v5を開始根拠に使わない。正式11 file・G26九fileの先行検索は観測commit時点の証拠として有効だが、将来の全コード検索元または中央ライフサイクル一覧とみなす解釈は使わない。
- deferred：TDD境界の別作業と独立開始前レビューが合格するまで、失敗試験、製品コード、製品設定、配布入口を変更しない。Work 4A内部のGit列挙化、正式なコード管理用の一操作入口、G26・G30・上流候補の正式化、探索、複数記録処理、外部送信、環境値解決、自動削除も開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Git起点の検索元訂正後、構造化方針2件のschema・方針参照が合格し、権威参照とWork 4A関連56件が成功した。現在のGit管理対象は151 fileで、先行観測集合151 fileと一致する。
- 直近の全Test：正式・安定表示への独立レビューで正規全試験1,740件成功を確認した。その後、製品コード・試験・設定・配布入口の変更はないため再実行していない。件数は観測値である。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
