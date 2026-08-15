# 能力別コード再利用検索・候補過大展開の訂正Evidence v1

- 日付：2026-08-15
- 対象実装commit：`af862aa872726671d0a50b6a84e76d4eb7598603`
- 対象plan：`records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v2.json`
- 対象attestation：`records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-attestation-v1.json`
- attestation SHA-256：`bfb5ea4ebb5ed39df9599364ad2808b7e816c0e38a7e3911776f75297de075b6`
- 判定：候補集合として不採用。実行時間の観測だけを有効とし、実装開始根拠へ使わない。

## 1. 機能と用途

能力別コード再利用検索は、作業ごとに必要な働きを宣言し、現在のGit管理下にあるコードから、直接関係する処理と別名の共通部品候補を探す開発支援処理である。人が採用、不採用、修正利用を決める前の検索材料を作るものであり、処置を自動決定しない。

## 2. 最初の実行で確認した事実

cleanな対象commitから正式入口を一回実行した。処理は終了コード0、`status: completed`、8能力すべて`candidates_found`、未発見能力0件だった。一方、解析対象1,598 routine中1,575件が候補になった。

実測時間は次のとおりだった。

| 工程 | 秒 |
|---|---:|
| Git管理下コードの観測 | 0.266076 |
| routine profile生成 | 2.862351 |
| comparison discovery生成 | 0.068466 |
| 8能力の検索 | 0.292518 |
| 合計 | 3.505985 |

計測は単調増加時計による観測値であり、検索record、attestation、検索内容識別値へ含めていない。

## 3. 問題と原因

候補数は能力別に1,154〜1,557件だった。各能力の候補のうち822〜1,315件は、直接参照、能力語、必要作用の一致を持たず、`comparison_group_member`だけで追加されていた。

原因は、参照処理と同じ比較群に入った全routineを候補へ展開したことである。Comparison Discoveryの「同じ引数形」「同じ例外名」「同じ直接呼出し先」「同じ試験参照」は比較の手掛かりであって同じ責務の結論ではない。これらの広い群を意味一致として全展開したため、検索のほぼ全routineが候補になった。

この結果は再現可能だが、人が再利用判断を行う材料として過大である。よってv1 attestationを実装開始の根拠へ使わない。外部のnew-only検索recordとproject内attestationは、失敗観測として書き換えず保持する。

## 4. 三案と選択

| 案 | 内容 | 簡潔さ | 処理時間・memory | 頑健さ | 変更範囲 | 戻しやすさ |
|---|---|---|---|---|---|---|
| A | 比較群展開を全廃し、直接参照と語・作用一致だけにする | 最小 | 最小 | 別名の近い実装を取りこぼす | 小 | 高い |
| B | 比較群の全展開を維持し、表示時だけ上位件数へ切る | 表面上小さい | 記録は大きいまま | 切捨て順が意味と無関係になり得る | 小 | 高い |
| C | 全コード検索を維持し、比較群からの追加だけを構造一致または呼出し近傍一致のfocused群へ限定する | 小さい | 過大全展開を避ける | 広い形だけの一致を候補と誤認せず、近い実装の手掛かりを残す | 検索処理1件・既存試験1件 | 高い |

案Cを採用した。Comparison Discovery自体や固定一覧を変更せず、能力検索が候補として採用する比較根拠だけを限定する。直接参照、完全一致symbol、能力語、必要作用、直接隣接、全Git source scope、Human裁定境界は維持する。

## 5. REDからGREEN

同じ引数形だけを持つ無関係な`show_status`を、参照処理と同じ`interface_shape_match`群へ入れた反例を既存試験へ追加した。

- RED：4件中1件失敗、終了コード1。無関係な`show_status`が候補へ入ることを検出した。
- GREEN：能力検索・正式入口・既存record・freshness・外部化の関連28件成功、終了コード0。
- 拡張関連確認：46件成功、終了コード0。
- 正規全試験：1,758件成功、失敗・error・skip 0、終了コード0、Python 3.13.14、pytest 8.4.2、runner版2、fallbackなし。
- 全試験receipt：`/private/tmp/reviewcompass3-capability-search-expansion-correction-full-receipt-v1.json`
- receipt SHA-256：`d07418821c629fec4f92af1d063ba85db191e6deb61572e7de37bf429ef293fc`
- 最初に誤って`--result-json`を指定した実行は、試験開始前にCLIが終了コード2で拒否した。正規入口の引数`--receipt`で単独再実行し、上記の成功を確認した。
- 実装：`tools/development/reuse_search_record.py`
- 実装SHA-256：`f22afb8299eec3d542824e6595e13d2d5d355bbf4bf182090f9b945962316c32`
- 試験：`tests/test_capability_reuse_search.py`
- 試験SHA-256：`18495b683cdd7f5425f853ef7ef650789c5aa88429aa8826536746bdc97a26a3`

## 6. 訂正後の再実行計画

元plan v2は書き換えず、同じ8能力と新しいattestation pathを持つplan v3を別fileで作成した。

- plan：`records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v3.json`
- plan file SHA-256：`7b385de1f1ae216b711daf29499afa86bea93fdc65d2d86890bc2d172f130a9e`
- plan content digest：`4ab75db51198552774843bb6b48930f6aaaf12e3d5728ee361600ceb7f5fac3b`
- 出力：`records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-attestation-v2.json`

訂正実装をclean commitへ固定した後、plan v3を一回だけ実行する。再実行でも工程別・検索別・合計時間を報告し、候補数と候補理由を確認する。候補がなお人の判断材料として過大なら、製品TDDへ進まず停止する。

## 7. 未実施

製品コード、安全保存機能、製品試験、製品設定、Task Contractは変更していない。候補の採用・不採用・修正利用、製品TDD境界の開始、push、外部送信は行っていない。
