# 一件の要求・機能区分・出典対応 契約v1独立確認 v1

- 実施日：2026-08-15
- 対象commit：`0583863e4612f7f14b5db131beb627677b99017a`
- 対象契約：`records/task-contract/2026-08-15-one-requirement-feature-source-candidate-v1.md`
- 対象契約SHA-256：`19702df3b5414b4e271ba30e6fb84ec285c887a98e189ed9bfd88e8ad2df6a25`
- 定義証拠SHA-256：`9d35dc70f5d96eb497bd8530ced4a1b32d5d838a6c0503f24668d8be719987c6`
- 担当：契約作成と実装を担当しない別AI
- 方法：読取り専用の定義反証
- 判定：`correction_required`
- repository成果物変更：0件

## 1. 結論

【判断】固定commit`0583863`からの実装開始を止める。停止原因は、同じ原因の変種をまとめて4系統である。

1. 上位G24の作成責務を、説明なしに整合検査へ変えている。
2. 正常表示する識別子へ機微情報候補を入れられる。
3. 同じ入力から複数の正常bytesと内容識別値が契約適合になり得る。
4. 再利用部品と保護対象の固定基準が不足している。

## 2. 停止原因

### 2.1 作成から検査への目的変更

【記録】候補一覧は「固定した要求資料から、要求、機能区分、由来の対応を一件分作る」と定める。

【実測】契約v1は、要求文、機能区分、全出典の採否、全原子義務の対応を入力作成者へ要求する。正常出力にも機能名、
責務、要求文、採否理由を含めず、入力済み対応の検査結果と内容識別値だけを返す。

【判断】これはG24全体の完成ではなく「構造化済み要求候補一件の整合検査」という狭い縦切りである。狭い縦切り自体は
妥当だが、元の作成責務が未完了で残ることと、この縮小を人が採用する境界が固定されていない。

最小修正は、製品名と責務を整合検査へ直し、元G24の作成責務を未完了の後続として残し、この契約の受入だけでは
候補3を完了にしないことと、縮小採用を人の判断へ残すことである。

### 2.2 識別子からの機微情報漏えい

【実測】契約の識別子規則は`AKIA`に16個の大文字英数字を続けたAWSアクセスキー形式を受理する。同じ文字列は
既存の機微情報検査で`aws_access_key_id`に一致する。出典ID、候補ID、機能ID、要求ID、義務IDは正常結果へ表示される。

【判断】自由文だけを非表示にしても、秘密らしい値を識別子へ入れれば正常結果へ露出する。形式固定済みSHA-256欄を除く
全利用者入力文字列のkeyと値へ、固定した既定patternと高乱雑性検査を適用し、検出時は値を出さず停止する必要がある。

### 2.3 正常結果と内容識別値の非一意性

【実測】一時領域で契約文を満たし得る複数表現を作ると、次のように内容識別値が分かれた。

| 対象 | 表現1 | 表現2 |
| --- | --- | --- |
| `counts` | 平坦形式 `c7e937...aab148a` | 入れ子形式 `cb0187...10694` |
| `human_decision_queue` | 状態別集合 `121791...f701` | 項目別 `79a4e8...d416` |
| `trace_sha256` | 対応本体だけ `1d4f9b...bc0e9` | 版を含む包み全体 `782860...4383f` |

【判断】`counts`の完全な項目、`human_decision_queue`の形と順、`trace_sha256`の計算対象、候補・機能・要求の
各内容識別値へ含める項目、Unicode文字表現、違反から停止理由・停止元への対応が一意でない。受入条件8、9、13、20を
一意に判定できない。

最小修正は、正常結果の全入れ子構造、各内容識別値の正規化済みJSON、正準JSONの文字表現、全停止条件の
`違反 → reason → source → 終了コード`を固定することである。

### 2.4 再利用部品と退行基準の未固定

【実測】G08安全読取りの現行内容識別値は次である。

| path | SHA-256 |
| --- | --- |
| `tools/design/one_design_acceptance.py` | `b3af7fdf254b21e5d368f2a02cf2aba23a86233a67b4120e7c2b39a3fd4a5c14` |
| `tools/design/one_design_acceptance_entry.py` | `7535aa6652514c6ce4dfd31facd2640944a356ddc04802b0df8ae63a9bec9823` |
| `tests/test_one_design_acceptance.py` | `6adc44ad7c7c9dff37ad3e671abfc0e86d9c5afe53861f2edeafc7acd01e1542` |

【実測】受入済みG08製品commit`1fec2475dfd50898edd22cb28f866952b764d2e0`から対象commitまで、上記3 fileは差分0だった。
停止元`design`と`acceptance`を`catalog`と`candidate`へ変換する方針自体は妥当である。

【判断】契約v1はG08の固定commitと内容識別値を開始条件にしていない。既存G24の保護10 pathについても、
受入条件16の「基準commit」が指定されず、全内容識別値を固定していない。要求artifact関連21件の試験pathも列挙していない。

最小修正は、G08の受入済みcommitと再利用file、G24保護基準commitと10 path、59件と21件の完全な試験commandを
契約内へ固定することである。

## 3. 問題がなかった境界

【実測】【判断】次は契約意図と一致する。

- 上流権限不一致を隠さず`source_requirement_ids`を空にしている。
- 二入力、全出典の採否、全原子義務対応、採用出典の消費、機能ID一致を閉じている。
- 候補・履歴資料を正式要求へ自動昇格しない。
- 要求採用を人の判断として残す。
- G08安全読取りの再利用と停止元変換は実装可能である。
- 既存G24の5実装・5試験を変更しない上限は妥当である。
- 外部送信、保存、探索、外部処理を禁止している。

## 4. 機械確認

【実測】

- G24関連試験：59件成功、終了コード0。
- 要求artifact関連試験：21件成功、終了コード0。
- 要求権限束v2：`effective`、50件、重複0、内部内容識別値`79a69d921bb00eb2b321e3d1adb073b88a527eb938398d1813567009255bd688`。
- G24保護10 path：固定commitから差分0。
- `git diff --check`：終了コード0。
- 作業tree：clean。
- branch：`main`、観測時に`origin/main`より945 commit先行。
- 外部送信：なし。

G24保護10 pathの内容識別値は次である。

| path | SHA-256 |
| --- | --- |
| `tools/requirements/boundary_relations.py` | `31ae6b8edfde022300a817ec3d9d553ddb3f64d71a92a3d95c35e01a8e40e869` |
| `tools/requirements/feature_partition.py` | `0796d436b7f6c3e075b998f1d80451ea59d3cb3cc6b77e6ef3084f9ffbecec2a` |
| `tools/requirements/fixed_inputs.py` | `60cfdef9e5d506fcb9519a00a02e83ed379f87a290aa34a50051d716c0354c9b` |
| `tools/requirements/requirement_batch.py` | `2e91889620ae18e2b49b856939d07102429b9d07d24b707fcd9d4b1ecb6f3986` |
| `tools/requirements/source_trace.py` | `7919f0baac5eabac3bb937fbb9264193c4ad31735a78cba4b07207f52fd282b3` |
| `tests/test_requirements_feature_partition.py` | `ec7908934b15de8a65878a9172fddfe6684db0fd66b00b87f2930fb8c95854d5` |
| `tests/test_requirements_fixed_inputs.py` | `529b4ad7b985173845d2e0404dbd991542397a10617e6fe79dfd4feb809d3111` |
| `tests/test_requirement_boundary_relations.py` | `00cbd919baf8c98d295e45007b136b48dda13596d78daeace262b638c30fb50d` |
| `tests/test_requirements_source_trace.py` | `9f04b748882ade1626e125cc78700850d0f1eeeb92c6202e0234de06e0f978c5` |
| `tests/test_requirements_batch.py` | `43e6ba7815a7c839b611e0d9f49d317b82c60fd7d3eb588545cc2810f663934b` |

## 5. 次の判断

【提案】上記4原因だけを契約候補v2へ限定訂正し、同じ担当へ変更点確認を戻す。製品コード、既存試験、G08、
既存G24は変更しない。v2では狭い整合検査をG24全体と同一視せず、その縮小を採るかを人の判断へ残す。

【未実施】契約v2、契約採用、実装、既存成果物変更、要求昇格、外部送信は行っていない。
