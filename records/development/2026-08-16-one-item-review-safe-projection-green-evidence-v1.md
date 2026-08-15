# 一件レビュー安全投影 実装成功Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-SAFE-PROJECTION-007 / v2`（採用済み）
- 採用判断：`records/development/2026-08-16-one-item-review-safe-projection-adoption-decision-v1.md`、
  SHA-256 `17b4f4f522810db3a851b1bc8dd1ab65bb90fb9ce5df2276ae60a42fcb19ec99`、commit `1d245fc`
- 実装担当：Claude
- 方式：テスト駆動（失敗試験の固定→最小実装）

## 1. 失敗試験の固定（RED）

【実測】対象試験へprepare操作の8試験を追加し、単独実行で7件が実装未存在により失敗、1件（入力key過不足の
既存停止）は既存動作で成立を確認した（`7 failed, 68 passed`）。commit `23be5e0`（試験1 fileのみ）へ固定した。

## 2. 最小実装（GREEN）

【実測】契約§8の変更上限内で、実行核`tools/operations/operation_contract_run.py`だけを変更した。

1. registryへ`one_item_review_prepare`を追加（操作名は§8.2手順3bの除外対象）。
2. G02核2関数`read_input_files`→`prepare_material`の直接呼出し（この順・一度ずつ）。
3. §7.2の固定allowlist投影（`material.content`、`review_spec.goal`・`criteria`・`constraints`を写さない）。
4. §7.1の固定変換：閉じた8理由だけを`part_stopped`（`part_source: none`、sensitiveのみ部品コード3）へ転記し、
   集合外（`stale_material`を含む）は`internal_failure`。
5. `part_result_sha256`は投影の正準JSON digest（部品出力bytesは投影から構成）。

入口・`pyproject.toml`・G02本体は変更なし（保護基準commit `a052312`から差分0を機械確認）。

## 3. 機械確認（各単独command・終了コード個別判定）

【実測】

- 対象試験：75件成功、終了コード0（投影のallowlist完全一致、自由文4種の非出現、束縛不一致、
  機微・絶対path・schema停止の変換、集合外理由の`internal_failure`反証を含む）
- G02対象158件・G08対象107件・G24対象111件・G30基盤e2e 38件：各単独成功、終了コード0
- 保護path（基準commit `a052312`からの差分）：差分0、終了コード0
- 正規全試験（既存の禁止認証隔離条件）：2,313件成功、終了コード0
- `git diff --check`：終了コード0

## 4. 合成一件E2E（受入条件10・関連）

【実測】正式実行名`reviewcompass3-operation-run`をrepository外の現在位置`/private/tmp/g02-e2e/outside`から実行した。
終了コード0、標準エラー0 bytes。

- 運用契約：`OC-E2E-G02`、操作`one_item_review_prepare`
- 実行記録が着地し、標準出力と完全一致（`stdout==file: True`）
- 束縛照合：material（生bytes digest）・review_spec（正準digest）とも一致
- 投影root keys：`external_send_approved`、`material`、`material_package_sha256`、`result_schema`、
  `review_spec`、`schema_version`、`status`（allowlistどおり）
- 自由文（資料本文・目的・基準文）の漏えい：0件を機械確認
- 実行記録内容識別値：`f2e8f982d29f8ee9a06779284b124aabdf508b66c1fceecc3975749f4cba6371`

## 5. 未実施

- 独立完了レビュー（受入条件11、Codex）
- 利用者の製品受入（受入条件12）
- G02のorganize操作、連鎖、保存統合（後続縦切り）
