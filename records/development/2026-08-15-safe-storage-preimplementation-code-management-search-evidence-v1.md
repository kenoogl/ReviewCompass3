# 安全保存機能 実装前コード管理検索 実施Evidence v1

- 実施日：2026-08-15
- 観測commit：`9eb044a2876e31a2205e4ce0f9b5be13281c6881`
- 対象契約：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002` version 3
- 導線Evidence：`records/development/2026-08-15-safe-storage-preimplementation-code-management-routing-evidence-v1.md`
- 判定：`code_management_search_completed / tdd_boundary_not_started`

## 1. 実施した機械処理

【実測】既存の`tools/development/work4a_rebuild_v3.py`と
`tools/development/reuse_search_record.py`だけを使い、観測commitの`tools/**/*.py`から次を生成した。

1. source observation（現在の対象fileとSHA-256）。
2. Routine Profile v3（現在の処理一覧）。
3. Comparison Discovery（構造、直接呼出し、直接試験参照等による比較候補）。
4. 正式採用済み11 fileの再利用検索記録。
5. 保留中G26九fileの再利用検索記録。
6. 二検索記録の外部保存と、project内の証明書。
7. 責務名による横断候補検索。ただし開始許可には使用しない。

【実測】外部送信、network、製品コード、試験、製品設定、Task Contractの変更は行っていない。大きい
機械生成物は既存のローカル開発データ領域へ置き、Gitには証明書と本Evidenceだけを置く。

## 2. 検索元の現在性

| 項目 | 値 |
| --- | --- |
| data root | `/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data` |
| source universe | v3、内容識別値`3a9c13c27f69e428c057b67e3db5c51dac44ee6af5cd2b4e37d90da9548fb534` |
| freshness policy | v6、内容識別値`b718f6ce9dc00ac588e3bf365a6f28b156d148978f0b6d6dd8a7725a44223134` |
| source content ID | `c8880cb4dee72e73264e342b8a5b249b8e971c45ce3dcb8294aec6c06edefcf6` |
| observation ID | `c50ba7c45714034ba8caed2f81eed910106a91688b0ab467961b00024004edbe` |
| Profile ID | `4227caa1eb155f067549434a04550b741d55dd88f7f85f08e9f8f3def5147b58` |
| Discovery ID | `2221b9bfa688744464faa88caf9d3853912678f01f9ea5beab8d7fb448808568` |
| 処理数 | 1,580 |
| 比較群数 | 1,031 |

【実測】source universe v3とfreshness policy v6は、現行開発方針SHA-256
`beda23f02aa15c7a1ff76504c240ffa8d28d056435db64cf881be6e552172e91`を参照する。旧版は変更していない。

## 3. 正式採用済みコードの検索

- 対象：G25の正式採用済み10 fileと、正式な読取り専用入口1 file。
- 検索record内容識別値：`2ca470ce38a01f8d1675350b1e204c08db375b2fea0e1d816984fa05176cae66`
- 外部record byte SHA-256：`88f1670f922da6a94c8f03fa2f114ffb5c1d9ec3eb22a95fd041715263a389b8`
- 証明書：`records/development/2026-08-15-safe-storage-formal-code-reuse-search-attestation-v1.json`
- 証明書SHA-256：`a2bfec07d52ef87605645d710dc85980badf99269d65262f68de0a05700dcdb7`
- 結果：一意処理105件、hit 669行、比較群260。
- 鮮度：変更0、追加0、欠落0、再生成一致、`start_allowed: true`。

【判断】`start_allowed`は、この検索記録が現在の対象fileと検索元へ正しく結び付き、検索を再現できるという
コード管理上の判定である。製品実装、TDD境界、G26採用の開始許可ではない。

【判断】正式入口`tools/session_logs/read_only_entry.py`は、契約が指定する値受渡し関数の**拡張候補**とする。
G25の解析、伏字化、要約、来歴生成は既存の正式経路を再利用し、新しい保存処理へ複製しない。

## 4. 保留中G26の検索

- 対象：G26の保留中9 file。
- 検索record内容識別値：`f326a6e3ac37331fcdaf9f00402355671755410099bd5119dc5927d5c5458ffe`
- 外部record byte SHA-256：`55bc09e3804fadcb89ea517f96dad25dd8dd9053f68ce62ff08ff4ea5df90154`
- 証明書：`records/development/2026-08-15-safe-storage-provisional-g26-reuse-search-attestation-v1.json`
- 証明書SHA-256：`d9e81d7abf20f633399ed92902eafb3a0808f2a3d015cd5a70aa186944f54ade`
- 結果：一意処理172件、hit 1,942行、比較群445。
- 鮮度：変更0、追加0、欠落0、再生成一致、`start_allowed: true`。

【判断】この`start_allowed`も検索記録の現在性だけを示す。G26は保留中であり、一括再利用または正式化を
許可しない。類似する原子的書込み、root境界、ロック、保存処理は、現在契約のsymlink非追跡、所有者限定mode、
二rootの状態遷移、削除確認値と再試行への適合を処理単位で確認した場合だけ再利用候補にできる。

## 5. 責務名による横断検索

【実測】同じProfileとDiscoveryへ、`canonical`、`commit`、`delete`、`digest`、`load`、`manifest`、
`mode`、`nofollow`、`operation`、`permission`、`record`、`retention`、`root`、`safe`、`sha256`、
`store`、`write`を検索語として適用した。

- record内容識別値：`c91d5dc1e2e441624f07599de135e21924bac6c33a5e97dde9bebd711232d0aa`
- 名前の直接一致：263件。
- 近接処理と比較群を含む一意処理：673件、hit 4,250行、比較群761。

【判断】この検索は候補発見だけに使う。対象pathを空にした責務名検索は将来のfile変更を鮮度確認できず、
既存gateが通っても実装開始根拠に使えない。この制約を隠すための新しい検査器は作らず、正式・G26の
対象path付き検索と、人による限定確認を正規の判断材料にする。

## 6. 実装前の処置候補

| 対象 | 現在の扱い | 理由 |
| --- | --- | --- |
| 正式な`read_only_entry.py` | 拡張候補 | 契約自身が、標準出力なしで安全結果を値として返す関数の追加先に指定している |
| 正式G25の解析・伏字化・要約・来歴 | 再利用 | 現在の正式入口と同じ処理経路であり、複製は不要 |
| G26九file | 一括再利用しない | 保留中で既知反例があり、現在契約の安全な開閉・二root状態・削除再試行を保証しない |
| G26の個別処理 | 必要時だけ再評価 | 現在契約を満たす処理単位だけを選び、満たさなければ理由を付けて分離する |
| `tools/common/digests.py`等の横断候補 | 自動採用しない | 名前は一致するが暫定表示であり、正式製品コードの依存にできるか別判断が必要 |

【判断】以上をコード管理側の実装前判断として固定する。TDD実装境界側では、この検索をやり直す代わりに、
各実装単位が上記の処置候補と矛盾していないことだけを別項目として参照する。両確認の合否は統合しない。

## 7. 残る限界と後続

【実測】既存処理には、処理一覧生成から検索証明書作成までを一操作で呼ぶ正式な入口がない。今回は既存関数を
一時的な機械実行で順番に呼んだ。決定的な抽出・照合自体は機械化できたが、起動手順はまだ正式実装ではない。

【判断】この不足のために安全保存機能の本線を止めて新しい包括的入口を先に作らない。本作業の検索記録を
実装開始条件へ接続し、正式なコード管理機能では、一操作入口と対象宣言の恒久形式を後続候補として扱う。

次の別作業は、TDD開始前の実装境界確認について、独自の導線と機械化可能範囲を確認することである。

## 8. 未実施

【未実施】TDD実装境界、22受入条件の分割、実装作業票、失敗試験、製品コード、製品試験、製品設定、
配布入口、G26の正式化、個別G26処理の採用、正式なコード管理用CLIの実装は行っていない。外部送信、network、
push、tag、amend、rebase、reset、履歴書換えも行っていない。
