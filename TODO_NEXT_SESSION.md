# TODO_NEXT_SESSION

更新日：2026-08-15

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：立て直し計画v5の第1段から第5段を完了した。最初のTask Contractに基づくG25読取り専用入口は、利用者受入、正式・安定表示、第5段完了判断まで完了した。
- 現在作業：安全保存案Cの実装前コード管理について、一操作の正式入口を実装し、commit 0a02b51の152コードから正式11 pathと保留G26九pathを同一identityで再検索した。両証明書は鮮度確認に合格し、候補採否はHuman裁定待ちとして保持した。
- Task Contract：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002 / version_3_adopted_implementation_start_approved_code_search_complete_tdd_boundary_precheck_pending`

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
- [一操作による現在検索Evidence](records/development/2026-08-15-safe-storage-formal-code-reuse-search-one-operation-execution-evidence-v1.md) — SHA-256 `2b9dffc209a730609a8c3ee8c031c7695db5188245390122f4a21be8c82f55d0`
- [正式11 pathの現行検索証明書](records/development/2026-08-15-safe-storage-formal-code-reuse-search-attestation-v2.json) — SHA-256 `709d72b7a79c1412e25208b7a405f6354059493240daa50e9552346ae5fc01bd`
- [保留G26九pathの現行検索証明書](records/development/2026-08-15-safe-storage-provisional-g26-reuse-search-attestation-v2.json) — SHA-256 `05259d87ec6c2a4b93cda21775bfbbc34994df56c839e9c6c43f5f6ac5e298e8`

## 次に行う一作業

コード管理とは別の作業単位として、安全保存Task Contract v3をTDDで扱える小さいRED／GREEN境界へ分けられるかを実装前に確認する。

開始条件：

- 採用済みTask Contract v3、案C実装開始判断、現行検索Evidence、二つの現行証明書を固定入力として読む
- 製品コードと試験を書き始めず、契約の状態遷移・失敗境界・許可pathを意味的に完結した小単位へ分ける
- 現行検索候補のうち実装依存として採用する処理があれば、正式・暫定・使用停止と再利用方法を明示してHumanへ戻す
- コード管理入口とTDD境界確認を一つの機能へ統合しない

完了条件：

- 各実装境界が一つの観測可能な振る舞いと対応するRED／GREENで完結し、前後の途中状態を不整合にしない
- 最初に実装する最小の縦切り、許可変更path、各境界の停止条件と独立確認方法が明示される
- 再利用候補の採否未決がある境界は実装開始可とせず、正式コードの重複実装を防ぐ
- 製品コード、製品試験、製品設定、Task Contractを変更せず、開始可否を利用者へ返す

後続作業：TDD境界確認と独立開始前レビューが合格し、必要な再利用裁定をHumanが行った後だけ、最初のREDへ進む。

## blocker・Human判断待ち

- blocker：コード管理入口と現行検索にはblockerがない。安全保存の製品実装は、TDD境界確認と必要な再利用候補のHuman裁定が終わるまで開始しない。
- Human判断待ち：現時点で追加判断はない。TDD境界確認で保留G26または他候補を正式依存へ採用する必要が判明した場合だけ、正式・暫定・使用停止と再利用方法を利用者へ戻す。

## stale・deferred

- stale：旧一時手順による検索とv1証明書は過去観測として保持し、現在の根拠にはcommit 0a02b51へ結び付いたv2証明書だけを使う。作業別計画を将来の検索元または中央一覧にしない。
- deferred：TDD境界の独立確認が終わるまで、失敗試験、製品コード、製品設定、配布入口を変更しない。ライフサイクル自動裁定、再利用方法の自動裁定、中央一覧、自動commit、push、外部送信も開始しない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：一操作入口の新規5件と、確定commit確認、Work 4A、Work 4B、権威参照の関連115件が成功した。module入口の起動確認と、生成後の二証明書の独立鮮度照合も成功した。
- 直近の全Test：一操作入口と試験を含む正規全試験は1,751件成功、失敗・error・skip 0、終了コード0だった。Python 3.13.14、pytest 8.4.2、runner版2、fallbackなし。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
