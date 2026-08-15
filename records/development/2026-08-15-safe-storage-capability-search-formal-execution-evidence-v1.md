# 安全保存・必要な働きによる正式コード検索 実行Evidence v1

- 日付：2026-08-15
- Work ID：`WORK-SAFE-STORAGE-CAPABILITY-SEARCH-FORMAL-EXECUTION-2026-08-15-V1`
- 対象commit：`0d676e9b78b70579809d6aa0940dbd5927aa56af`
- 判定：`completed / freshness_verified / human_adjudication_required`
- 製品実装：未開始

## 1. 機能と用途

【実測】現在のGit管理下にあるPythonコード152 file、1,600処理を機械的に観測し、安全保存に必要な八つの働きについて、
直接確認対象、検索上の手掛かり、既存の比較集団を分けて一回で検索した。検索は、固定した中央一覧を更新する方式ではなく、
実行時点の確定commitから検索元を作る。このため、今後追加されたGit管理コードも次回検索では自動的に対象へ入る。

【判断】用途は、製品実装前に既存部品の重複と再利用可能性を確認することである。検索処理は、再利用、修正利用、不採用、
新規実装を自動決定しない。正式、暫定、使用停止の区分も結果へ表示するだけで、Human裁定を代行しない。

## 2. 固定入力と実行結果

【実測】次の確定材料を使った。

- plan：`records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v4.json`
- plan file SHA-256：`1c9fef66370e3a067500ea0d6c1ecce9b77e0a9a107b51ad52c99519aab6ac45`
- plan内容識別値：`e817da66c2e58373c57701b9169696f6855a96c00b9c9be27113755cbc6a4ec6`
- source universe v7 file SHA-256：`1f6c1d7bf327f8398225c6ebbebb3fb17d098ca689c19a7f7f505e570a3a6dc3`
- source universe内容識別値：`f5e02f65077df0aeecd804aad7383f6e248fa2d02f1f28796f4a5d160f7e4e69`
- freshness policy v10 file SHA-256：`b6e57a5d04a41027e0be8a56320e479f6dd100440f9d3396affca54ff2025d77`
- freshness policy内容識別値：`e6ec332021c85c2b80dbc260f7783a573062d4347eae1ab2a7baf3e54449506a`

【実測】正式入口は終了コード0、`status: completed`を返した。push、remote照合、network、外部送信、自動commitは
行っていない。外部開発データ領域へ観測・処理一覧・比較・検索正本を作り、project内へnew-onlyの証明書一件を作った。

- source content ID：`9549891507936fbc03aebe3bf96a0ddbf76db9753600227569eee6edbff5ae9f`
- observation snapshot ID：`96bb5a6cd46db60113c274e45000848be2e98cab24c2a12cf7fc0f304c8e897f`
- routine profile run ID：`0f4eef7114d362ba1eb4184e7d30e91abc8f04b479932774df76626aef68777b`
- comparison discovery run ID：`54a5e00598209b6a9663ce2dc446b2af048f24f89725f72073b745513d1e25bf`
- 比較集団：1,048件

## 3. 所要時間

【実測】単調増加時計で測った一回の観測値は次である。時間は検索結果の合否や内容識別値へ含めていない。

| 工程 | 秒 |
| --- | ---: |
| Git管理コードの観測 | 0.270766 |
| 1,600処理の一覧作成 | 2.895783 |
| 比較集団の生成 | 0.068061 |
| 八つの働きの検索 | 0.217537 |
| 合計 | 3.468781 |

【判断】現在規模では実行時間は隘路ではない。ただし時間短縮は検索範囲を狭める理由にしない。

## 4. 八つの働きの検索結果

【実測】延べ件数は、直接確認対象119件、手掛かり1,223件、比較集団1,177件だった。手掛かりと比較集団は、
再利用できる処理の件数ではない。比較の入口と外部全件記録への参照である。

| 必要な働き | 直接 | 手掛かり | 比較集団 | 機械表示 |
| --- | ---: | ---: | ---: | --- |
| 正式入口から安全な値を渡す | 18 | 28 | 99 | `direct_matches_found` |
| 内容識別値 | 32 | 47 | 114 | `direct_matches_found` |
| 保存root・権限境界 | 13 | 318 | 162 | `direct_matches_found` |
| 原子的な記録確定 | 7 | 165 | 209 | `direct_matches_found` |
| 中断後の復旧 | 21 | 97 | 73 | `direct_matches_found` |
| 検証付き再読込み | 19 | 420 | 469 | `direct_matches_found` |
| 再試行可能な削除 | 0 | 140 | 0 | `search_hints_found` |
| 同時更新の排他 | 9 | 8 | 51 | `direct_matches_found` |

【実測】計画で明示したpathと処理は全件存在し、欠落参照は0件だった。再試行可能な削除には、計画どおり直接対応する
既存処理を指定していない。処理名や本文の削除語による140件は低水準の手掛かりであり、契約が求める再試行可能な削除が
実装済みであるとは表示していない。

## 5. ライフサイクルと再利用方法の候補

【実測】計画で明示した処理のうち、正式・安定表示は
`tools/session_logs/read_only_entry.py:_safe_result`一件だけだった。その他の明示処理はすべて暫定表示だった。
禁止したnetworkと外部process起動の衝突は、明示処理では0件だった。

【提案】Human裁定へ返す最小候補は次である。これは採用Decisionではない。

1. 安全な値の受渡し：`_safe_result`の許可項目選択は再利用候補。現行の正式入口は画面へ出して終了コードを返すため、
   保存処理へ値を返す接続は新しい小境界として必要である。
2. 内容識別値：`canonical_json_bytes`と`sha256_hex`は限定再利用候補。来歴照合は`verify_provenance`を参考にする。
   いずれも明示処理の成熟度は暫定なので、新製品境界の試験で契約適合を確認する。
3. 保存root・権限境界：G28とG26の処理は修正利用候補。別の場所を指すリンク、所有者、アクセス制御一覧、二保存rootを
   現契約どおり閉じるまでは、そのまま採用しない。
4. 原子的な記録確定：既存の一時fileからの置換は低水準部品候補。二保存rootの状態確定は新しく定義する。
5. 中断後の復旧：G28の確認値と再実行処理は参考候補。今回のoperation状態機械とは同一でない。
6. 検証付き再読込み：既存の来歴・ledger・cursor照合は部品候補。今回の固定file集合全体の照合は別途必要である。
7. 再試行可能な削除：直接対応する既存処理なし。低水準の削除操作だけを参考にし、状態遷移は新規実装候補とする。
8. 同時更新の排他：`exclusive_lock`は修正利用候補。保存rootと権限の保証は別に確認する。

【判断】暫定file全体の正式化や丸ごとの再利用は推奨しない。採用する場合も、必要な関数と安全条件だけへ限定する。

## 6. 過大検索の訂正確認

【実測】旧v3検索は1,598処理中1,023処理を平らな候補一覧にし、人の判断材料として過大だった。今回のschema 4は、
直接確認対象、手掛かり、比較集団を別欄にし、比較集団の全構成員を後段結果へ複写していない。比較集団は既存Work 4Aの
根拠、限界、件数、大きさ区分、代表最大三件、外部全件記録への参照として残した。

【実測】既存の検証処理で証明書と外部正本を再照合し、
`start_allowed: true / reuse_search_record_verified / assessed_fresh`を確認した。

- 証明書：`records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-attestation-v3.json`
- 証明書SHA-256：`de06acf8367b99b84ab0643652a05058065cd381798a2bc32d1990281f446322`
- 証明書内容識別値：`1bde543ad68198f18e2f5857fab1009403d3a62a3e188421769a85f74ab97dbb`
- 外部検索正本の相対path：`work4b/reuse-searches/263e4f14a9fb786b91178379b6aebe4e24db58d2deafc93b7a87cb0137ead053.json`
- 外部検索正本のbyte SHA-256：`2149b7999dc96b506b23246b003ccd366f1fc0a8deeafccf72acac4eb38396d5`

## 7. 未実施

候補の採用・不採用・修正利用のHuman裁定、暫定処理の正式化、製品TDD境界、失敗試験、製品コード、製品試験、
製品設定、Task Contractは変更していない。中央一覧、追加の検索機構、push、外部送信、履歴書換えは行っていない。

次の作業は、八つの働きについて上記の再利用方法をHumanが裁定し、その裁定だけを入力に、別機能である製品TDDの
実装境界事前確認へ戻ることである。
