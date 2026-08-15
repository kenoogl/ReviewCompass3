# 一件レビュー安全投影操作の追加 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-SAFE-PROJECTION-007`
- 契約版：1
- 契約種別：製品処理・受入済み『最小運用契約実行』への操作追加縦切り（運用化目標の後続）
- 状態：`candidate_pending_independent_review_and_human_approval`
- 作成日：2026-08-16
- 直前の製品契約：`TC-RC3-PRODUCT-MINIMAL-OPERATION-CONTRACT-EXECUTION-006 / v4`（受入済み）
- 利用者判断：2026-08-16の運用化目標、G30縦切りの製品受入、「#4はG02の安全投影から進める」選択
- 実装状態：未開始
- 危険度：高
- 危険の理由：自由文を含む部品結果を扱い、投影の誤りが機微情報・自由文の実行記録への漏えいになる
- 内容識別値：本候補固定後、独立確認と利用者判断記録から参照する

「安全投影」は、部品結果から自由文を含まない固定の項目だけを写した、実行記録へ埋め込むためのJSON objectである。
他の用語（作業契約、運用契約、実行記録、正準JSON）は契約006 v4の定義を引き継ぐ。

## 1. 位置と縮小境界

【記録】受入済みの実行器（契約006 v4、`reviewcompass3-operation-run`）はG08・G24の2操作を持つ。G02一件レビューは、
部品結果に入力自由文が入る・入口署名が共通形と異なる・停止結果に停止元がないため、006のregistryから除外された
（006 v1独立確認の停止原因1、その最小修正）。

【判断】本契約は、その除外を閉じる後続縦切りである。**実行器のregistryへ`one_item_review_prepare`一操作を、
核関数の直接呼出し・安全投影・停止の固定変換で追加する**ことだけを行う。

- G02の`organize`操作、複数操作の連鎖、実行計画、保存統合、既存G30基盤の正式化は本契約で行わない。
- 本契約の受入だけでは候補4（G30）と運用化目標の全体を完了にしない。
- この縮小境界を採るかは、独立確認後に利用者が契約採用と同時に判断する。

## 2. 目的

承認済み運用契約一件（操作`one_item_review_prepare`）について、次を決定的に行う。

1. G02の安全読取り`read_input_files`と材料固定`prepare_material`を同一process内で直接呼び出す。
2. 部品結果から§7.2の固定allowlistだけを写した安全投影を作り、自由文を実行記録へ入れない。
3. 部品結果が報告する内容識別値と運用契約の束縛宣言を照合する。
4. 契約006 v4の実行記録形式・書込み境界のまま、実行記録一件を着地させる。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 利用者の運用化目標 | `records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md` | `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a` |
| 基底契約006 v4 | `records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v4.md` | `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1` |
| 006の製品受入判断（G02を後続とする境界を含む） | `records/development/2026-08-16-minimal-operation-contract-execution-product-acceptance-decision-v1.md` | `8386ee089ff54b0fde80fca4592a58d8e660e71cd11cb9687e676ca3f824e808` |
| 006 v1独立確認（G02除外の根拠） | `records/development/2026-08-16-minimal-operation-contract-execution-v1-independent-review-v1.md` | `3eb9eba738171ac0f66572de1da5454377684f5ab4d4c110e85397c86657e5ca` |

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A G02入口のstdout捕捉 | 既存entryをstdout差し替えで呼ぶ | 署名が共通形でなく、プロセス全域のstdout差し替えは他部品へ波及する。不採用 |
| B G02入口の改修 | entryへ`output`引数と停止元を追加する | 受入済みG02の変更は保護境界を破る。不採用 |
| C 核関数の直接呼出し＋固定投影 | `read_input_files`→`prepare_material`を直接呼び、固定allowlist投影と停止変換を実行器側に持つ | G02無変更・出力一意。推奨 |

## 5. 範囲

### 5.1 範囲内

- 実行器registryへの`one_item_review_prepare`の追加（運用契約の`operation`enumへ同名を追加）。
- 入力key・束縛keyは`material`、`review_spec`の2件。値は絶対path（契約006 §8の共通規則のまま）。
- G02核の直接呼出し、安全投影の作成、束縛照合、実行記録の着地（006 §7の書込み境界のまま）。

### 5.2 範囲外

- G02の`organize`操作、G02入口・核・試験の変更、既存2操作の意味変更。
- 投影への自由文・採否理由・絶対path・例外本文の追加。
- 連鎖、実行計画、保存統合、既存G30基盤、外部送信、G02 material本文の保存。

## 6. 固定再利用部品と保護基準

### 6.1 変更対象の基準（実装で変更してよい2 file）

| path | 現在のSHA-256 |
| --- | --- |
| `tools/operations/operation_contract_run.py` | `a0fdc2eacaa6ce6d5baafc54daa133f215dc3b0285772af7f16f7d0f94b8c689` |
| `tests/test_operation_contract_run.py` | `1d96fb6ff03326a2febfb47963ab1c2560fc35f6cac7f08c1d340dd9921005b5` |

### 6.2 再利用（呼び出すだけで変更しない）

`tools/reviews/one_item_review.py`（SHA-256 `de658b6e96b804af393d106cbc11c39d7452e9cb54c24c5157853bc5dcd9ad57`）の
公開`read_input_files`と`prepare_material`だけを再利用する。呼出し順はこの2関数一度ずつ、この順だけとする。

【実測】`read_input_files(*, input_root, material, review_spec)`は2 fileを非追跡・同一性検査付きで読み
（上限：material 262,144 bytes、review_spec 65,536 bytes）、`{"material": bytes, "review_spec": bytes}`を返す。
`prepare_material(material_bytes, review_spec_bytes)`はUTF-8復号、NUL検査、機微・絶対path検査
（`sensitive_data_remaining`／`absolute_path_remaining`）、review仕様の固定schema検査を行い、結果objectを返す。
停止は全て`ReviewStop(reason)`で、停止元を持たない。

### 6.3 保護対象

保護基準commitを`a052312645328d7272f65aededdb74152e157c41`とする。§6.2のG02核、
`tools/reviews/one_item_review_entry.py`（`92a770583b14728b5f6606a851357efb27a19fdba11d07fecd12d941f633c390`）、
`tools/operations/operation_contract_run_entry.py`（`06c01aefbff568f80ff0919af398dfff2fabc405927419fe0acd5e52a1a88abb`）、
`pyproject.toml`（`bea8151c9c055d9fe696672013b64e566579d9a7365f3c753b9eedae7885d5ef`）、機微情報規則file
（`aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`）、G08・G24の再利用4 file、
`tools/task_contract/`5 file、`tests/test_one_item_review.py`、`tests/test_one_design_acceptance.py`、
`tests/test_one_requirement_feature_source.py`、`tests/test_first_review_task_contract_e2e.py`を変更しない。

## 7. 実行方法の固定

### 7.1 呼出しと停止の固定変換

運用契約の検査・機微検査・出力先事前検査・書込み境界は契約006 v4 §7〜§11のまま変更しない。
`operation: one_item_review_prepare`のとき、部品実行段階を次へ固定する。

1. `read_input_files(input_root=<input_root>, material=<inputs.material>, review_spec=<inputs.review_spec>)`を呼ぶ。
2. 返った bytes 対で`prepare_material(material_bytes, review_spec_bytes)`を呼ぶ。
3. いずれかが`ReviewStop(reason)`で停止した場合、`part_stopped`（source `part`・終了コード5）とし、
   `part_reason`へ理由をそのまま転記、`part_source`は固定値`none`、`part_exit_code`は
   理由が`sensitive_data_remaining`のとき`3`、それ以外`2`とする。理由は§6.2の8種
   （`invalid_arguments`、`invalid_path`、`invalid_schema`、`invalid_utf8`、`sensitive_data_remaining`、
   `size_limit_exceeded`、`unreadable_input`、`absolute_path_remaining`、および`stale_material`を含む固定集合）だけを
   転記し、他は`internal_failure`とする。
4. `ReviewStop`以外の例外は`internal_failure`とする。

### 7.2 安全投影（固定allowlist）

部品結果から次の項目**だけ**を写した安全投影を`part_result`へ埋め込む。列挙外の項目（`material.content`、
`review_spec.goal`、`review_spec.criteria`、`review_spec.constraints`を含む）は写さない。

- `external_send_approved`（固定`false`）
- `material`：`content_sha256`、`identifier`、`line_count`だけ
- `result_schema`：`grouping_basis`、`schema_version`、`semantic_deduplication_performed`の全項目
- `review_spec`：`sha256`だけ
- `schema_version`、`status`、`material_package_sha256`

`part_result_sha256`は安全投影の正準JSON bytesのSHA-256とする（他操作の「標準出力bytes由来」と計算対象が
異なることを実行記録の一意な形として固定する）。実行記録の他の項目・書込みは006 §10のまま。

### 7.3 束縛照合表（追加行）

| 操作 | 入力名 | 部品結果内の照合位置 |
| --- | --- | --- |
| `one_item_review_prepare` | `material` | `material.content_sha256`（入力fileの生bytesのSHA-256） |
| `one_item_review_prepare` | `review_spec` | `review_spec.sha256`（正規化済みreview仕様の正準JSON SHA-256） |

## 8. 変更上限

1. 実行核`tools/operations/operation_contract_run.py`（registry追加・呼出し・投影・変換だけ）。
2. 対象試験`tests/test_operation_contract_run.py`への追加。
3. Evidence、独立確認、受入判断、TODO更新。

入口・`pyproject.toml`・G02・既存2操作の定義・§6.3保護対象を変更しない。必要なら契約改定へ戻る。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. prepare正例で、実行記録の着地、標準出力とfileの完全一致、束縛2件の一致を示す。
2. 実行記録に資料本文・goal・criteria本文・constraints本文・絶対pathが現れないことを、投影のallowlist完全一致と
   固定自由文の非出現の両方で確認する。
3. `part_result_sha256`（投影の正準JSON digest）、`contract_sha256`、`record_sha256`を独立oracleで再計算する。
4. 束縛宣言の一値変更で`binding_mismatch`となり、fileが作られない。
5. §7.1の変換表どおり：G02の機微停止（材料に機微情報候補）が`part_stopped`・`part_reason:
   sensitive_data_remaining`・`part_source: none`・`part_exit_code: 3`・実行器終了コード5となる。
   `absolute_path_remaining`（材料に絶対path）と`invalid_schema`の各変換も確認する。
6. 操作名`one_item_review_prepare`（23文字）が§8.2手順3bの除外対象であり、正例が機微停止しない。
7. 既存2操作の全試験が退行しない（既存67件相当が成功のまま）。
8. G02核2関数の呼出しがこの2関数一度ずつ・固定順だけで、G02のfile内容識別値が§6.2と一致する。
9. 未知操作・入力key過不足など006の停止表が3操作目でも同じ形で成立する。
10. 配布後の正式実行名を別の現在位置から実行しても同じbytesを返す。
11. 対象、関連（G02 158件・G08 107件・G24 111件・G30基盤38件）、正規全試験を各単独終了コード0で成功させ、
    固定commitを別担当が誤合格・未接続・禁止作用・上位目的への悪影響0件として確認する。
12. 利用者が「G02のprepare一操作の追加であり、organize・連鎖・保存統合は後続に残る」限界と実装結果を確認して
    製品処理を受け入れる。

## 10. 停止条件

- 安全投影のallowlistで自由文の遮断を一意に確認できない。
- G02核・入口・既存2操作・§6.3保護対象の変更が必要になる。
- 停止変換を固定規則から一意に決められない。
- 通信、外部process、保存追加、環境値解決、時刻取得が必要になる。
- 対象、関連、正規全試験または独立確認が不合格になる。

## 11. 影響、未実施、次作業

【判断】受入後は、レビュー中核部品（G02材料固定）が運用契約の導線に載り、材料の固定を一commandで実行記録へ
着地できる。自由文は投影で遮断され、実行記録の安全表示は3操作で一貫する。

【未実施】契約採用、縮小境界の利用者判断、実装、既存成果物変更、外部送信は行っていない。

次は本候補を固定commitへ記録し、本候補の作成を担当しなかった別担当が定義反証（投影の遮断・変換の一意性・
束縛位置の現物一致・保護基準）を成果物変更なしで確認する。`開始可`になった後、利用者へ縮小境界の採用と
実装開始を一判断として求める（新契約のため条件付き事前承認は引き継がない）。
