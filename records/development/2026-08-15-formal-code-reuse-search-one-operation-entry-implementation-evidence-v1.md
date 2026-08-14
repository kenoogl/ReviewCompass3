# 正式コード再利用検索 一操作入口 実装Evidence v1

- 実施日：2026-08-15
- Work ID：`WORK-FORMAL-CODE-REUSE-SEARCH-ONE-OPERATION-ENTRY-2026-08-15-V1`
- 利用者判断：推奨案Aを実施
- 判定：`implementation_verified / current_search_execution_pending`

## 1. 実装した機能と用途

【実測】`tools/development/formal_code_reuse_search.py`を追加した。この開発支援入口は、一つの変更なし
ローカルcommitと作業別検索計画を入力に、既存のcommit確認、コード観測、処理一覧、比較候補、複数の
再利用検索、外部記録、project内証明書、最終結果を一回で生成する。

【判断】用途は、新しい製品コードの実装前に、現在の全コードから既存処理の再利用候補を漏れなく検索し、
同じcommitと内容識別値へ結び付けることである。ライフサイクルと再利用方法は人の裁定待ちとして返す。

## 2. TDDの失敗から成功

【実測】実装前に`tests/test_formal_code_reuse_search.py`の5件を実行し、全件がmodule不存在を理由に失敗、
終了コード1だった。試験を変更せず入口を実装し、同じ5件は全件成功、終了コード0へ移行した。

確認した例は次のとおりである。

- 外部repositoryを持たない変更なしcommitから、二検索を一回で完了する。
- 未commit変更を停止する。
- 対象pathが空の計画を停止する。
- 既存の証明書出力先を上書きせず停止する。
- Git repositoryでない作業場所を停止する。

## 3. 処理順と停止境界

【実測】入口は計画のschema、内容識別値、検索宣言、出力先を全て先に確認してから、次を順番に呼ぶ。

1. `capture_committed_observation`
2. `build_routine_profile_v3`
3. `build_comparison_discovery`
4. 宣言ごとの`search_existing_routines`
5. 宣言ごとの`externalize_reuse_search_record`
6. 宣言ごとの`gate_check_attested`

【実測】入口のGit処理は先行commit確認が使う読取り操作だけであり、add、commit、push、fetch、network、
外部repository照合はない。自動的なライフサイクル裁定、再利用方法の裁定、TDD境界判定もない。

## 4. 作業別計画と中央一覧の分離

【実測】安全保存用計画
`records/development/2026-08-15-safe-storage-formal-code-reuse-search-plan-v1.json`は、正式11 pathと保留G26九pathの
二検索を同じcommitから行う作業時点入力である。計画file SHA-256は
`cdecd40cfecf4c945dcf55f0a48de97170caf7858093adb80cb73e04cd796bd5`、内容識別値は
`f2762eb20161e23174ad52ce245b840edfb92e619d55dc7a5e66ecc559657261`である。

【判断】この計画は将来のコード検索元、全コード一覧、ライフサイクル中央一覧にしない。検索元は実行時の
Git管理コードから毎回生成し、計画はその検索で確認する作業固有範囲だけを宣言する。

## 5. 関連確認と内容識別値

【実測】新規5件、確定commit事前確認、Work 4A v3からv3.3、Work 4B検索記録・鮮度・外部化、権威参照の
関連115件は全件成功、終了コード0だった。module入口の`--help`も終了コード0だった。

【実測】TODO参照更新後の正規全試験は1,751件成功、失敗・error・skip 0、終了コード0だった。
Python 3.13.14、pytest 8.4.2、runner版2、fallbackなし。リポジトリ外の受領記録SHA-256は
`ddb47a8583537aab73f3a4a6dfad2203d6f0bd7f811c062edf87d6740c05d7cd`である。

- 実装file SHA-256：`12327a7b6019e13343df309879b1aacf953f1dfc26ef7d0a3924d2bdab8c47e5`
- 試験file SHA-256：`ddd7b00efe158780e211042c27846852a8bac72d555cd867195f9c4f96a059ec`
- 開発方針SHA-256：`14e70e875990c51351b30175c800449f8942117822fd85dd3457baab19aba823`
- source universe v6内容識別値：`a87816987937eceebaddfbe786dd568b4db8c661584399247ccdeb97963f3230`
- freshness policy v9内容識別値：`0f1c5eb3c85bccf9fc3107fadbdf788c3e3072df14f530d7a2e39c80579e5c52`

## 6. 未実施

【未実施】現在repositoryの安全保存二検索、検索結果のHuman裁定、製品コード、製品試験、製品設定、
安全保存Task Contract、TDD実装境界、中央一覧、自動commit、push、外部送信は変更・実行していない。
現在検索は本実装をcommitして作業場所を変更なしにした後、同入口から一回実行する。
