# 正式コード検索の確定コミット事前確認 判断 v1

- Decision ID：`DEC-COMMITTED-SOURCE-FORMAL-SEARCH-PRECHECK-2026-08-15-V1`
- 判断日：2026-08-15
- 判断主体：利用者
- 対象：実装前コード管理の正式検索
- 先行判断：`DEC-GIT-DERIVED-CODE-SEARCH-SOURCE-2026-08-15-V1`
- 判断：`require_clean_local_commit_for_formal_search / do_not_require_push`

## 1. 利用者判断

【記録】利用者は、検索元を現在のGit管理コードから生成する訂正後、外部repositoryとの差、ローカルcommitの
要否、commit確認の機械化を順に確認した。判断は次のとおりである。

- 正式な実装前検索では、再現可能なローカルcommitを必須にする。
- pushと外部repositoryとの一致は必須にしない。
- commit済み状態の確認を、コード管理側の機械処理へ含める。
- TDD開始前の実装境界確認とは別機能・別判定のままにする。

## 2. 修正前の実測

【実測】`tools/development/work4a_rebuild_v3.py`の既存`capture_observation`は、`head`を呼出し側から
受け取り、観測記録へ格納するだけだった。Gitが返す現在commitとの一致、未commit変更、追加登録、未登録file、
commit内のコード集合との一致を確認していなかった。したがって、機械生成された観測でも、正式検索へ使える
確定commit状態かどうかは別の手順に依存していた。

【実測】既存の`tools/development/work_unit_transition.py`には、repository rootの一致、通常の未commit差分、
追加登録、未登録file、表示を隠した追跡fileのbytes差を読取り専用で確認する処理がある。

## 3. 三案比較

| 案 | 内容 | 単純さ | 処理時間・メモリ | 頑健さ | 変更範囲 | 保守・戻しやすさ | 採否 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Work 4Aへ正式観測入口を追加し、既存の作業遷移確認を再利用する | 既存二処理の接続だけ | Gitの読取りと151 path程度の比較で小さい | 呼出し忘れを正式入口の境界で防ぎ、未commit状態と集合不一致を停止できる | 開発支援コード、関連試験、方針 | 独立した一関数で外しやすい | **採用** |
| B | commit確認専用の別commandを作る | 機能は明確 | 小さい | 別commandの実行忘れを残す | 新command、試験、導線 | 入口が増え保守が増える | 不採用 |
| C | 文書へ確認commandだけを書く | 最も小さい | 小さい | 人の実行・転記漏れを防げない | 文書だけ | 戻しやすいが目的を満たさない | 不採用 |

【判断】案Aを採用する。正式検索は`capture_committed_observation`から開始する。従来の
`capture_observation`はGit外の試験環境や予備調査のため残すが、正式な実装開始判断には使わない。

## 4. 正式入口の境界

【判断】正式入口は次を一回の処理で行う。

1. 要求されたproject rootがGit repository rootそのものであることを確認する。
2. 未commit変更、追加登録、未登録file、表示を隠した追跡fileのbytes差がないことを確認する。
3. `HEAD`のcommit識別値をGitから直接取得する。呼出し側からは受け取らない。
4. `HEAD`に含まれるsource universe対象pathをGitから生成する。
5. 作業場所で観測する対象pathと完全一致することを確認する。無視指定された未登録コードもここで止める。
6. 導出したcommit識別値を既存観測記録の`head`へ、fileとSHA-256を既存`files`へ固定する。

【判断】失敗時は自動commit、追加登録、変更破棄、push、network、外部repository照合を行わない。固定理由だけを
返して正式検索を停止する。外部より進んだローカルcommit、分岐名を持たないcommit、外部repositoryを持たない
commitも、上記条件を満たせば使用できる。

## 5. 版と記録

【判断】source universe v5とfreshness policy v8を追加する理由は、コードfileの追加ではなく、本Decisionで
正式検索の開始条件と検証結果語彙を変更したためである。今後もコード追加だけでは版を更新しない。

- 開発方針SHA-256：`9d550502038bf8d2ff230b98f4bed9c0378d925a00bbbdd54026b1b3cb7fae7a`
- source universe v5内容識別値：`67f0f6f3f1b19f4674a1791c973172ebeea4155ed68e15130908f7707b0209dc`
- freshness policy v8内容識別値：`7aab227c63f459efe7206dd23a724527faa8900b75dcc664cddb8c7d3a9a3c00`

## 6. 承認範囲と未実施

【判断】本Decisionは、開発支援コードの正式観測入口、関連試験、開発方針、参照する構造化方針、実施Evidence、
TODOの更新を承認する。製品コード、安全保存Task Contract、製品試験、製品設定、TDD実装境界は変更しない。

【未実施】自動commit、push、外部送信、network、外部repositoryとの同期、中央コード一覧、ライフサイクル中央
台帳、TDD境界確認との統合、G26・G30・上流候補の正式化は行わない。
