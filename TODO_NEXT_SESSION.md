# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存案Cの実装前コード管理について、確定ローカルcommitから観測・処理一覧・比較・複数検索・証明書・結果までを一回で生成する正式入口を実装した。次はこの実装をcommitし、同入口で現在の正式11 pathと保留G26九pathを再検索する。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_code_search_entry_green_current_search_pending`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：コード管理入口と現在検索を妨げない、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

## 最新のauthority／Evidence

- [採用済みの安全保存Task Contract v3](records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md) — SHA-256 `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- [案Cの実装開始判断](records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md) — SHA-256 `f8c55611de59cd25946aa27bb4330ca66bbf1cf751baba6c5fe5c19a3ec1d45f`
- [現行開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `14e70e875990c51351b30175c800449f8942117822fd85dd3457baab19aba823`
- [確定コミット事前確認判断](records/development/2026-08-15-committed-source-formal-search-precheck-decision-v1.md) — SHA-256 `8138c20dca1fb361781846c94f4300afc4ff208241f572510a76d5d801e36539`
- [一操作入口の実装計画](records/development/2026-08-15-formal-code-reuse-search-one-operation-entry-implementation-plan-v1.md) — SHA-256 `6f2c1174a89e99c33fe1180ef2f23ddab830ba306f8a4cc27fd6a52748a28978`
- [一操作入口の実装Evidence](records/development/2026-08-15-formal-code-reuse-search-one-operation-entry-implementation-evidence-v1.md) — SHA-256 `bbca763e7fb81e30ae890805ced42c6b49a773d91dbfb65555b1a3f2182dc46b`
- [安全保存用の作業別検索計画](records/development/2026-08-15-safe-storage-formal-code-reuse-search-plan-v1.json) — SHA-256 `cdecd40cfecf4c945dcf55f0a48de97170caf7858093adb80cb73e04cd796bd5`

## 次に行う一作業

一操作入口の実装を意味単位でcommitした後、変更なしの同commitから安全保存用二検索を一回実行し、新しい証明書と結果を固定する。

開始条件：

- 一操作入口、対象試験、検索計画、現行開発方針、source universe v6、freshness policy v9がcommitされ、作業場所に未commit変更がない
- 安全保存用計画の内容識別値と二つの証明書出力先が実状態と一致し、出力先が未作成である
- 一操作入口だけを使い、個別関数の手動実行や結果転記で代替しない
- ライフサイクルと再利用方法の裁定を自動化しない

完了条件：

- 正式11 pathと保留G26九pathの二検索が同じcommit・source content ID・Profile・Discoveryに結び付く
- 二つの証明書がnew-onlyで生成され、両方の鮮度判定が合格する
- 一回の機械結果が件数、内容識別値、証明書SHA-256、人の裁定待ちを返す
- 製品コード、製品試験、製品設定、Task Contract、TDD境界を変更しない

後続作業：現在検索の証跡とTODOを固定した後、コード管理とは別のTDD開始前実装境界確認へ進む。

## blocker・Human判断待ち

- blocker：製品実装を止める既知の欠陥はない。一操作入口は関連試験で成功したが、現在repositoryを対象にした正式検索は実装commit後でなければ開始条件を満たさない。
- Human判断待ち：現時点で追加判断はない。現在検索で保留G26の個別処理を正式依存へ採用する必要が判明した場合だけ利用者へ戻す。

## stale・deferred

- stale：旧一時手順による正式11 path・G26九path検索は観測commit時点の履歴として保持するが、現在実装の開始根拠には新しい一操作入口の結果を使う。作業別計画を将来の検索元または中央一覧にしない。
- deferred：現在検索とTDD境界の独立確認が終わるまで、失敗試験、製品コード、製品設定、配布入口を変更しない。ライフサイクル自動裁定、再利用方法の自動裁定、中央一覧、自動commit、push、外部送信も開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：一操作入口の新規5件と、確定commit確認、Work 4A、Work 4B、権威参照の関連115件が成功した。module入口の起動確認も成功した。
- 直近の全Test：一操作入口と試験を含む正規全試験は1,751件成功、失敗・error・skip 0、終了コード0だった。Python 3.13.14、pytest 8.4.2、runner版2、fallbackなし。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
