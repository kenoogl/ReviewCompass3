# 必要な働きから導くコード再利用検索 実装Evidence v1

- 実施日：2026-08-15
- Work ID：`WORK-CAPABILITY-DERIVED-CODE-REUSE-SEARCH-2026-08-15-V1`
- 利用者判断：案A
- 判定：`implementation_verified / current_capability_search_pending`

## 1. 実装した機能と用途

【実測】既存の正式コード再利用検索へ、作業ごとの必要な働きを入力にする計画schema 2と
`search_required_capabilities`を追加した。機能は、現在のGit管理コード全体から作った同じ処理一覧と比較群を使い、
必要な働きごとに次を返す。

- 既知の参考path・処理・処理名の手掛かりに一致した処理。
- その直接の呼出し先・呼出し元。
- 比較群に属する別file・別機能名の全member。
- 必要な構文副作用を持つ処理。
- 禁止副作用との衝突。
- source自身に明記された`stable`、`provisional`、`stopped`または未宣言。
- 候補がない必要な働き。

【判断】用途は、機能名や固定file一覧だけでは見落とす共通内部部品を実装前に見つけ、重複実装を避けること
である。自然文から責務を自動推測せず、必要な働きは作業ごとにHumanが確認する。

## 2. TDD実装境界とREDからGREEN

【実測】実装前の試験は9件中4件失敗、5件成功、終了コード1だった。失敗は次の二境界に対応した。

1. `search_required_capabilities`がなく、働き別候補、禁止副作用、成熟度、未対応を返せない三件。
2. 一操作入口が計画schema 2を拒否する一件。

【実測】試験を変更せず境界1と境界2を最小実装し、同じ9件は全件成功、終了コード0へ移行した。その後、
新しいコードがGit検索範囲へ入った場合に既存証明書を`profile_stale`として停止する一件、必要・禁止の
副作用を同時指定する誤入力を拒否する一件、実行時間を検索内容識別値から分離して報告する一件を追加し、関連46件は
全件成功、終了コード0だった。方針・権威参照の関連29件も全件成功、終了コード0だった。

【実測】実行時間の計測追加後、正規全試験は1,758件成功、失敗・error・skip 0、終了コード0だった。
Python 3.13.14、pytest 8.4.2、runner版2、fallbackなし。リポジトリ外の受領記録SHA-256は
`5dfc010e31873da2639d0bb1c8e61a583b1f63d9c8d55485c7ee1ea9b2ef92e2`である。

## 3. 実行時間の報告

【実測】一操作入口は単調時計で、コード観測、処理一覧、比較候補、各検索、検索全体の経過秒を測り、
最終結果の`timing`と各検索の`elapsed_seconds`へ返す。時間は外部検索正本、証明書、検索内容識別値へ
含めないため、同じコード状態の検索identityを実行環境の速度で変えない。

## 4. 作業別入力と固定一覧の分離

【実測】安全保存用計画schema 2は八つの必要な働きを持つ。

1. 正式入口から安全な値を渡す。
2. 内容識別値を計算する。
3. 保存rootと権限の境界を守る。
4. 一時fileから完全な記録だけを確定する。
5. 中断した操作を安全に再開する。
6. 確定記録を検証して再読込みする。
7. 再試行可能な順序で削除する。
8. 同じ記録への更新を排他する。

- plan SHA-256：`f652448f72e306fcac57ab05bf88200fce352994afb48017db04a3c5e13f1421`
- plan内容識別値：`c35d1f2abc97e7fbd665f5b428092532dd12a5553d7c41886776cb4b73c1fe1f`

【判断】参考path・処理は今回の働きを調べる時点入力であり、将来作業の検索元や中央一覧にしない。検索元は
source universe v7の規則に従い、実行時のGit管理コードから毎回作る。

## 5. 機械処理とHuman判断の境界

【実測】新record schema 3は`human_adjudication_required: true`を必須とし、再利用方法を出力しない。
成熟度はsourceのmodule docstringに明記された表示だけを観測し、Decisionから使用停止や正式化を推測しない。

【判断】候補が見つかることと、採用できることは別である。入力、出力、失敗、安全条件が一致するかをHumanが
確認し、採用、不採用、修正利用を別の判断として記録する。

## 6. 内容識別値

- `tools/development/reuse_search_record.py` SHA-256：`02a95cec88c37a990597cc397703b3b541f8cd2ef99e40730bb9bbaddd0f0311`
- `tools/development/formal_code_reuse_search.py` SHA-256：`496b8e7f868a588c5f197534235afcffe40f1e323ec2e056698e4c3cf9b5fa9b`
- `tests/test_capability_reuse_search.py` SHA-256：`6390bf954a6bf9b834d8556592e42da2aca839b3d8f5c643c297f7baa530932e`
- `tests/test_formal_code_reuse_search.py` SHA-256：`afa364190c524a66b7ec006c009b3db8270e88f5f2113847abbb25521d6fa796`
- 開発方針SHA-256：`3453626fd168ac014d5e929017dbfb654bea6425164cfa3aa02bbfdf4aaa1c56`
- source universe v7内容識別値：`f5e02f65077df0aeecd804aad7383f6e248fa2d02f1f28796f4a5d160f7e4e69`
- freshness policy v10内容識別値：`e6ec332021c85c2b80dbc260f7783a573062d4347eae1ab2a7baf3e54449506a`

## 7. 未実施

【未実施】現在repositoryについて安全保存の八つの働きを正式検索する処理、候補の採否、保留G26の正式化、
使用停止Decisionの自動解釈、製品コード、製品試験、製品設定、Task Contract、製品TDD境界、自動commit、push、
外部送信は実行・変更していない。正式検索は本実装をcommitし、作業場所を変更なしにした後に一回実行する。
