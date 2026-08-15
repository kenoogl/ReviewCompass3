# G24契約候補v2 Claude引継ぎメモ v1

- 作成日：2026-08-15
- 引継ぎ理由：利用者の指示により、Codexの残り文脈量を理由として以後をClaudeへ移す
- 現在の作業：G24「要求固定・機能分割・由来追跡」の最初の縦切りに関する作業契約定義
- 製品コード：未実装
- 外部送信：未実施・禁止継続
- 次の担当：Claude

「作業契約」は、目的、入力、範囲、確認方法、停止条件を実装前に固定する約束である。
「内容識別値」は、内容の変化を機械検出するSHA-256値である。

## 1. 結論から見た現在地

【記録】G08「一件の設計・受入条件照合」は利用者に正式受入され、受入記録を含むcommit`25bed5c`まで完了している。

【実測】G24の契約候補v1はcommit`0583863e4612f7f14b5db131beb627677b99017a`へ固定済みである。別担当AIの
読み取り専用レビューは`修正要`と判定した。停止原因は次の4系統だった。

1. 上位G24の「作成」を、説明なしに「整合検査」へ縮めていた。
2. 正常表示する識別子へ秘密鍵らしい値を入れられた。
3. 件数、判断一覧、内容識別値、停止理由の形が一意でなかった。
4. 再利用するG08安全読取りと、保護するG24既存成果物の基準が不足していた。

【実測】4原因だけを訂正した契約候補v2は作成済みだが、独立再確認は未実施である。したがって、実装開始不可である。

## 2. 今回の引継ぎ対象

### 2.1 v1独立確認記録

- path：`records/development/2026-08-15-one-requirement-feature-source-contract-v1-independent-review-v1.md`
- SHA-256：`31d8227de940dc1aca264222cd25aad9870a0e6fb4fe16c954c109d11a6d7705`
- 判定：`correction_required`
- repository成果物変更：0件

### 2.2 訂正済み契約候補v2

- path：`records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v2.md`
- SHA-256：`a4d544e29d877ac45dca65b748557387bd1b04f58adda59ffacf91fc47a216bb`
- 状態：独立再確認待ち
- 実装：未開始

### 2.3 v2で行った訂正

【記録】

- 製品名を「一件の要求候補整合検査」へ変更した。
- これはG24全体ではなく最初の縦切りであり、G24の要求作成責務は未完了の後続として残すと明記した。
- この縦切りの受入だけでは候補3を完了にしないと明記した。
- 利用者入力のSHA-256欄を除く全文字列key・値へ、固定した機微情報候補検査を適用した。
- 正常結果の全項目、件数欄、判断一覧、並び順、5種類の内容識別値の計算対象を固定した。
- 全停止を`違反・理由・停止元・終了コード`の表へ固定した。
- 受入済みG08の3 file、G24既存10 path、機微情報規則fileの内容識別値を固定した。
- G24関連59件と要求資料関連21件の完全な試験commandを固定した。

## 3. Claudeが最初に行う一作業

契約候補v2を成果物変更なしで読み取り、v1の4停止原因だけが閉じたかを独立再確認する。製品コードを作らない。

### 3.1 開始時の確認

1. `AGENTS.md`と`TODO_NEXT_SESSION.md`を読む。
2. `git status --short`が空であることを確認する。
3. 引継ぎpackageを含むHEADと、本メモ、v1確認記録、v2契約の内容識別値を確認する。
4. Python実行は常に`.venv/bin/python3`を使う。

### 3.2 再確認する4点

1. 「整合検査」はG24全体ではなく未完了を残す縦切り、と誤解なく固定されているか。
2. AWS鍵形式、email、bearer token、API key代入、秘密鍵block、高乱雑性tokenをID・key・自由文で停止し、
   SHA-256の正規欄だけを誤停止しないか。
3. 同じ入力から正常JSON、件数、判断一覧、各内容識別値、停止結果が一意に定まるか。
4. G08固定3 file、G24保護10 path、機微情報規則、59件と21件の試験経路が実装者によって後決めできないか。

### 3.3 必須の機械確認

次はそれぞれ単独commandとして実行し、終了コードを個別に判定する。

`.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`

直近結果：59件成功、終了コード0。

`.venv/bin/python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py`

直近結果：21件成功、終了コード0。

`.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`

直近の受入済みG08結果：107件成功、終了コード0。本引継ぎ直前には再実行していないため、Claudeが再確認する。

`git diff --exit-code 0583863e4612f7f14b5db131beb627677b99017a -- tools/requirements/boundary_relations.py tools/requirements/feature_partition.py tools/requirements/fixed_inputs.py tools/requirements/requirement_batch.py tools/requirements/source_trace.py tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`

期待：終了コード0、差分0。

## 4. 再確認後の分岐

### 4.1 `開始可`の場合

利用者へ次の一判断だけを求める。

> G24全体ではなく、最初の縦切りとして「構造化済み要求候補一件の整合検査」を先に実装する。要求文・機能区分・
> 出典対応の作成は後続に残り、この受入だけでは候補3を完了にしない。この境界と案Cの実装開始を承認するか。

利用者の明示承認前に試験追加、製品実装、`pyproject.toml`変更を行わない。

### 4.2 `修正要`の場合

- 同じ原因の変種をまとめ、止める原因を最小数で報告する。
- 契約候補だけを新しい版へ訂正し、製品コード、既存G24、G08、要求資料を変更しない。
- 同じ4境界を再確認してから利用者判断へ進む。

## 5. 実装開始後も守る境界

- テスト駆動開発で、失敗試験を先に作り期待どおり失敗させる。
- 新規Pythonは4スペースで字下げする。
- 既存G24の5実装・5試験、受入済みG08、現行50要求、要求schemaを変更しない。
- 通信、外部送信、外部処理、環境値解決、入力外探索、file保存を追加しない。
- 完了した意味単位は明示pathだけをstageし、関連試験と`git diff --check`の成功後にコミットする。
- 実装完了後は別担当による独立完了レビューと、利用者による製品受入が必要である。

## 6. 上流の重要な不一致

【実測】旧第4段の37要求、9機能、由来対応は`provisional`かつ`non-normative`のままである。

【実測】2026-08-03の要求権限束v2は50要求を`effective`として解決するが、人の判断は要求本文と受入真偽を承認範囲外とする。

【判断】この不一致があるため、契約候補v2は`source_requirement_ids`を空にしている。旧37要求または現行50要求を、
G24製品の存在だけで正式要求へ再昇格しない。

## 7. 未実施

- 契約候補v2の独立再確認。
- 利用者による縮小境界、契約採用、案C実装開始の判断。
- 対象試験の作成と失敗確認。
- 製品コード、正式入口、実行名の実装。
- 正規全試験、独立完了レビュー、製品受入。
- G24の要求作成責務。
- 候補4以降。
- 外部送信、実利用者資料の使用。

## 8. 引継ぎ完了条件

本メモ、v1独立確認記録、契約候補v2、更新済み`TODO_NEXT_SESSION.md`を一つの意味単位commitへ固定し、
`git status --short`が空であること、TODO検査と`git diff --check`が終了コード0であることを確認する。
