# 安全保存コード再利用検索・過去実装と検索境界の調査 v1

- 日付：2026-08-15
- 対象commit：`a5d82282594e41148e7bb008c19a1ecbcd799a9c`
- 対象：安全保存案Cの実装前コード再利用検索
- 判定：`investigation_complete / correction_required`
- 製品実装：未開始

## 1. 目的

【判断】現在のGit管理コード全体から、今回必要な働きと同じ内部部品を探す。ただし、機能名やfile名が違うだけで
探索対象から外さず、似ているという理由だけで再利用を自動決定しない。

本調査では、現在の検索結果が過大になった原因、前身ReviewCompass／ReviewCompass2と現在の保留コードにある
参考実装、八つの働きに対応する具体的な比較元、検索方法の修正案を読み取り専用で確認した。

## 2. 固定材料

| 材料 | 内容識別値またはcommit |
| --- | --- |
| 安全保存Task Contract v3 | `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac` |
| 能力別検索計画v3 | `7b385de1f1ae216b711daf29499afa86bea93fdc65d2d86890bc2d172f130a9e` |
| v3検索証明書 | `ee19058135c2a2fda3af896725fad5557a348de35c7cbde132acc742dc06fce9` |
| 検索本体 | `tools/development/reuse_search_record.py`、`f22afb8299eec3d542824e6595e13d2d5d355bbf4bf182090f9b945962316c32` |
| 一操作入口 | `tools/development/formal_code_reuse_search.py`、`496b8e7f868a588c5f197534235afcffe40f1e323ec2e056698e4c3cf9b5fa9b` |
| 前身ReviewCompass2リポジトリの固定commit | `d6bbb01500002872c713412bfbd63b702a291c99` |
| 前身ReviewCompassリポジトリの固定commit | `cab302d4b32af790628b811b3566f39d55781fa5` |
| ReviewCompass3保留保存処理 | `tools/session_logs/eventual_preservation.py`、`9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18` |

## 3. 現在の検索が過大になった原因

【実測】v3証明書は、観測した1,598処理中1,023処理を候補としている。八つの働きは全て
`candidates_found`となり、未対応は0件と表示された。しかし、候補集合は実装前の人の確認材料としてなお過大である。

`search_required_capabilities`を読み、原因を次の四点へ分けた。

1. `reference_paths`は、指定file内の全class・関数・methodを比較元にする。このため、`main`、例外class、表示補助まで
   同じ働きの比較元になる。
2. `required_effect_markers`は絞込み条件ではなく、その印を持つ全処理を候補へ加える条件である。例えば
   `file_write`だけで、責務の違う多数の処理が候補になる。
3. `symbol_terms`は処理名だけを調べる。関数本文で`unlink`を使うが関数名に削除語を持たない処理は見つからない。
4. 具体的な比較元からの展開は、直接の呼出し元・呼出し先と、限定された構造一致群だけである。別名・別構造で同じ
   内部処理を持つ場合は、全コードを観測していても候補へ上がらない。

【判断】検索対象を全コードにしていることと、全コードから同じ働きを実際に見つけられることは同じではない。
現在の不足は対象範囲ではなく、比較方法と結果区分にある。

## 4. 過去と現在の参考実装

### 4.1 ReviewCompass2の共通処理台帳

【実測】固定commitの`.reviewcompass/architecture/shared-routines.yaml`は、能力、正本module、正本関数、関連語、
`reuse | extend | merge | split_with_rationale`の判断履歴を持つ。ただし登録は二件で、この台帳を全コード検索へ
使う実行処理は固定commit内に見つからなかった。

【判断】判断語彙と履歴形式は参考になるが、検索処理としては再利用できない。中央の手作業一覧へ戻してはならない。

### 4.2 ReviewCompass2のSession取込み

【実測】`tools/session_capture/provenance.py`、`merge.py`、`verify.py`には、取り込んだ範囲のSHA-256、追記と
非追記変更の区別、来歴からの再生成、バイト一致確認がある。一方、
`.reviewcompass/backlog/issues/issue-2026-07-26-raw-session-log-preservation.yaml`は、生ログ保全が未実装であることを
open Issueとして残す。安全な保存、二領域の確定、保持期限後の再試行可能な削除は存在しない。

### 4.3 ReviewCompassの参考処理

【実測】`tools/check_workflow_action/preservation.py:_atomic_write_yaml`は、同一directoryの一時fileへ書き、flush、
`fsync`、`os.replace`を行う。原子的な書込みの参考にはなるが、今回の保存root、所有者、権限、二領域状態、削除再試行を
扱わない。固定commitの参照コードであり、現在の正式部品ではない。

### 4.4 ReviewCompass3の保留処理

【実測】`tools/session_logs/eventual_preservation.py`には次がある。

- `_validate_boundaries`：repositoryと保存領域の分離、source root内確認。
- `_secure_parent_chain`、`_secure_file`：directory 0700、file 0600の設定。
- `_write_atomic`：決定的な一時名からの置換。
- `_collect_locked`、`_checkpoint`、`_file_matches`：成果物後・cursor前の中断から再実行する材料。

このfileは第4段でG28、`製品／保留`と分類され、先頭表示も`provisional / non-normative /
promotion_required: true`である。現在の計画v3はこのfileを比較元へ含めていなかった。

【判断】上記は関数単位の修正利用候補である。ただし全構成要素で別の場所を指すリンク（シンボリックリンク）を
追わない開閉、所有者・アクセス制御一覧（ACL）の検査、二つの保存領域の状態確定、確認値付き削除は保証しない。
file全体の正式化や丸ごとの再利用はしない。

## 5. 八つの働きと具体的な比較元

| 必要な働き | 具体的な既存関数 | 現時点の判断 |
| --- | --- | --- |
| 正式入口から安全な値を渡す | `pipeline.prepare_artifact`、`read_only_entry._safe_result` | 一部参考。契約が求める値返却口は未実装 |
| 内容識別値 | `canonical_json_bytes`、`sha256_hex`、`verify_provenance` | 強い修正・再利用候補 |
| 保存root・権限境界 | G28の`_validate_boundaries`、`_secure_parent_chain`、`_secure_file`、G26の`_bind_inside_root` | 修正利用候補。現契約より境界が弱い |
| 原子的な記録確定 | G28／G26の`_write_atomic`、`storage._commit_outputs` | 部品候補。二root確定は未実装 |
| 中断後の復旧 | G28の`_checkpoint`、`_file_matches`、`_collect_locked` | 挙動の参考。今回の状態機械とは異なる |
| 検証付き再読込み | `verify_provenance`、`regenerate_artifact`、`_verify_ledger`、`_load_cursor` | 部品候補。今回の固定file全体照合は未実装 |
| 再試行可能な削除 | 直接対応する既存関数なし | 新規実装が必要。低水準の削除処理だけを参考にする |
| 同時更新の排他 | `locking.exclusive_lock` | 修正利用候補。保存境界と権限は別途必要 |

## 6. 読み取り専用の反証試算

### 6.1 具体的な比較元だけを現行検索へ渡す

【実測】参考file全体、処理名の手掛かり、読書き印を外し、上表の具体的な関数だけを比較元にして、同じ
1,598処理・同じComparison Discoveryへ現行検索をメモリ上で適用した。

- 一意候補：99件。
- 所要：0.068491秒。
- 働き別候補：18、32、14、8、21、19、0、9件。
- 再試行可能な削除は0件となった。

候補過大は大きく減ったが、結果の中心は比較元の呼出し元・呼出し先である。
`tools/development/issue_resolution_v4.py:_atomic_write`のような、別配置の原子的書込みは候補にならなかった。

### 6.2 2026-08-07の事前分類式を具体的な比較元へ適用する

【実測】関数本文の識別語重なり0.6、関数名0.2、引数・return・raise・例外・分岐・行数の一致0.2という当時の式を、
具体的な比較元と全1,598処理へ読み取り専用で適用した。全件詳細を保持しない試算は0.211959秒だった。

現行検索が見つけなかった主な例は次である。

- 内容識別：`claude_bootstrap._canonical_bytes`、`review_plan._canonical_bytes`、
  `immutable_result_store.canonical_json_bytes`。
- 保存境界：`private_validation._validate_boundaries`、`preservation_migration._secure_directory_chain`、複数の
  `_safe_relative_path`。
- 原子的書込み：`issue_resolution_v4._atomic_write`、`todo_update_path.atomic_write`、
  `todo_compaction._atomic_write`。

【実測】全比較結果を保持する形で計測器を付けた試算では11,165件だった。全結果を空白なしJSONへ変換した大きさは
2,868,125 bytes、Python内で追跡した最大メモリは21,127,634 bytes、所要0.853492秒だった。計測器自体の負担を
含むため、通常計算の0.211959秒とは分けて扱う。

【判断】現規模では全コード比較の処理時間とメモリは隘路ではない。ただし当時の重みと0.85／0.45境界は正解集合で
検証されておらず、これを候補の切捨てに使ってはならない。

### 6.3 比較元がない削除処理

【実測】関数本文を`delete | deleting | retention | unlink | remove | purge`で確認すると42処理が該当した。
配置解除、一時file掃除、lock解除が多く、今回の「削除計画を確認し、状態を残して再試行する」処理はなかった。

【判断】本文中の操作語は比較元がない働きの探索入口として有効だが、語の一致を責務一致とみなしてはならない。
42件は低水準部品または反例の確認対象であり、既存の再試行可能削除があるという結論ではない。

## 7. 修正三案

| 案 | 内容 | 簡潔さ | 処理時間・メモリ | 頑健さ | 変更範囲 | 戻しやすさ | 判断 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 計画だけを具体的な比較元へ直す | 最小 | 0.07秒、候補99件 | 別名・別構造の共通部品を見落とす | 作業別計画だけ | 高い | 不採用。全repository探索の目的を満たさない |
| 2 | 旧事前分類の重みと境界で候補を切る | 小さい | 約0.21秒 | 閾値未検証で偽陰性を作る | 検索処理・試験・計画 | 高い | 不採用。順位材料には使えるが切捨てに使えない |
| 3 | 現行一操作入口の中で、直接候補と全repository比較結果を分ける | 中 | 全件保持試算約2.9 MB、最大約21.1 MB | 全処理を確認した証拠を残し、直接候補と弱い手掛かりを混同しない | 既存検索処理・既存試験・schema・作業別計画 | 高い | **推奨** |

案3では、新しい中央索引や別入口を作らない。同じ観測commit、処理一覧、比較結果を使い、次を分ける。

1. `direct_candidates`：明示した比較元、直接の呼出し関係、強い構造一致。
2. `repository_comparisons`：全処理について、本文語、名前、構造特徴、禁止作用との衝突を観測した比較事実。
3. `uncovered`：比較元も、本文操作語による直接候補もなく、既存実装を確認できなかった働き。

全体比較に弱い値が付いた処理も外部正本から削除しない。人へ通常提示する優先順と、機械が確認した全件記録を分ける。
重みや境界は採否や未対応の自動決定に使わない。

## 8. 案3のTDD実装境界事前確認

### 境界1：直接候補と全体比較の分離

- 入力：具体的な比較元一件と、直接関係にないが本文・構造が近い別名関数一件。
- RED：現行処理は別名関数を返さないか、広い候補と直接候補を同じ一覧へ混ぜる。
- 最小GREEN：直接候補と全体比較事実を別欄に返し、採否を返さない。

### 境界2：比較元がない働き

- 入力：比較元なし、処理名に削除語なし、本文で`unlink`を使う関数一件。
- RED：現行処理は処理名しか見ないため未発見となる。
- 最小GREEN：本文の操作語一致として返し、責務一致とは表示しない。

### 境界3：全コードを確認した証拠

- 入力：同じ観測commitの全処理集合。
- RED：現行記録は候補だけを持ち、働きごとに全1,598処理を比較したかを結果から再現できない。
- 最小GREEN：比較した処理数、処理識別子集合の内容識別値、全件の比較事実を外部new-only正本へ残す。

【判断】三境界は別の製品機能ではなく、一つの開発支援検索の順序付き小単位である。製品の安全保存TDDとは分離する。

## 9. 判断と次の作業

【判断】計画だけの訂正では目的を満たさない。案3を採用する場合は、既存一操作入口と既存外部記録を拡張し、
直接候補と全体比較を分ける限定修正をTDDで行う。その後に具体的な比較元を持つ安全保存検索計画をnew-onlyで作り、
clean commitから正式検索をやり直す。

これは検索記録の意味を変えるため、実装開始前に利用者判断を要する。既存v1／v2証明書と外部記録は失敗観測として
書き換えず保持する。

## 10. 未実施

製品コード、製品試験、製品設定、安全保存Task Contract、製品TDD境界、正式検索計画、検索実装、検索schema、
TODO、既存Evidenceは変更していない。正式検索、候補の採否、G26／G28の正式化、外部送信、push、履歴書換えは
行っていない。読み取り専用試算の一時scriptはrepository外の`/private/tmp`に置き、正式根拠へ使わない。
