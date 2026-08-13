# Work 5B契約試験整理 Evidence v1

- 記録日：2026-08-14
- 状態：`implemented_pending_independent_review`
- 作業票：`docs/development/2026-08-14-work5b-contract-test-cleanup-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`336eb49a9d3ac70d566f67b5b4178d7c3d1f7f3e0c65f92617a3e4aead636163`
- 基準commit：`b609d86`
- 作業票commit：`e7c91b2`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- Human承認：2026-08-14、案C、試験file一件・六試験の削除、履歴資料無変更

## 1. 実施

【実測】`tests/test_work5b_contract.py`一file・六試験だけを削除した。削除前SHA-256は
`9630b087d400dd13eb36c519a5d916755626ebcb15ffb6942ad6ce87cb05d9d0`である。

【実測】次の履歴資料は変更していない。

- Work 5B契約v1：`89c92ae260bfb1efd201d414e0235b66ebb270b457942c59ef5fccfc9cfa5387`
- Work 5B契約v2：`5123b778cb12b8cf23f353d9725c0598f9214fdcf66d625f9385ef2ebd8a20f0`

固定source DecisionとEvidenceも基準commitから差分0である。

【判断】削除した六件は完了済みWork 5Bの履歴固定五件と現在保証に重複する一件であり、現在処理の固有保証を持たない。
契約v1・v2、過去Decision・Evidence、初期開発チェックリストを残すため、履歴・監査資料は失われない。

## 2. 現在保証と参照

【実測】六試験名と`tests/test_work5b_contract.py`を、製品コード、検査コード、設定、他試験から検索し、参照0件だった。

【実測】現在の宣言対応表検査と再利用検索を直接守る次の三fileは22件成功、終了コード0だった。

- `tests/test_declaration_red_map_check.py`
- `tests/test_reuse_search_externalization.py`
- `tests/test_adversarial_remedy_batch1.py`

【記録】先行の独立再評価は、再利用検索処理を常時許可・常時拒否へ変える二つの欠陥を、六試験を外した状態でも
既存の直接試験が検出することを確認済みである。本実施はその確認済み境界を変更していない。

## 3. 正規全試験

【実測】次の正規入口を単独実行した。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-work5b-contract-test-cleanup-full-receipt.json
```

- 結果：`passed`
- 終了コード：`0`
- 成功：`1,731`
- 失敗・エラー・除外：`0`
- Python：`3.13.14`
- pytest：`8.4.2`
- 代替実行：`false`
- 受領記録SHA-256：`9fc9cc48a7458040e507935eb274fef6c035d073a09369d1be82145ce6965a21`
- 状態識別値：`ce4d243590f094bfda1c02f59a796d89af594cf721d02435149a50b446738439`

【実測】削除前1,737件から六件減の1,731件で、作業票の期待件数と一致した。受領記録は本Evidence追加前の
削除状態に対応する。独立完了レビューは結果commit全体について再確認する。

## 4. 履歴回復

【実測】作業票commit `e7c91b2`から削除前fileをGit物体として読み出し、SHA-256が削除前値と一致した。

【実測】commit `c0acdcd`をリポジトリ外へ展開し、当時の契約v2と契約試験を回復した。当時のv2は、
標準JSON・SHA-256による自己内容識別値の再計算と一致した。当時の契約試験は六件成功、終了コード0だった。

【判断】現在の試験集合から外しても、作業時点の契約と試験はGitからbyte単位で回復できる。v2の現在の自己内容識別値
不一致は先行停止Evidenceと役割再評価Evidenceに原因付きで残しており、履歴recordを現在値へ追加訂正していない。

## 5. 変更範囲、判断、未実施

【実測】成果の変更範囲は、削除した試験file一件と本Evidence一件だけである。`git diff --check`は指摘0件だった。

【判断】案Cは、現在保証を直接試験へ残し、履歴資料を無変更で保存し、正当な後続変更のたびに固定値を更新する手戻りを
解消した。新しい契約、検査器、台帳、試験、強制関門は増やしていない。

【未実施】契約v1・v2、固定source Decision・Evidence、初期開発チェックリスト、現在の検査コード、他試験、設定、
正本、TODO、v2内容識別値の変更、後継契約、新しい検査器・台帳・試験、G06案B、外部送信、履歴書換え、
第3段完了判断は行っていない。
