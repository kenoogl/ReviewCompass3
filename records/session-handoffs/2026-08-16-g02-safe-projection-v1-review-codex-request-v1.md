# 一件レビュー安全投影 契約候補v1 独立確認依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v1の作成担当）
- 依頼先：Codex（レビュー専任。本契約候補の作成を担当していない）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：実装開始前の契約定義反証（読取り専用）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担

- **Codexが行うのは§4の定義反証と、判定record 1件の作成・単独commitだけ**である。
- 判定後の後続（開始可なら利用者への採用提示、修正要なら契約訂正）はClaudeが実施する。

## 2. 対象と前提

- 対象契約候補：`records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v1.md`
  - SHA-256：`b42232fd0f6a559a680c5447845502a0947b0d96caaaddae208c8bf0c94a2f9b`
  - 固定commit：`b82ccf30ada56f0cb763b0741a56bcb945f10481`
- 基底契約006 v4（受入済み）：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v4.md`
  - SHA-256：`d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1`
- G02除外の経緯（006 v1独立確認の停止原因1）：
  `records/development/2026-08-16-minimal-operation-contract-execution-v1-independent-review-v1.md`
  - SHA-256：`3eb9eba738171ac0f66572de1da5454377684f5ab4d4c110e85397c86657e5ca`
- 本候補は、受入済み実行器のregistryへ`one_item_review_prepare`を追加する縦切りである。中心は
  §7.2の固定allowlist投影（自由文遮断）、§7.1のReviewStop固定変換、§7.3の束縛照合位置である。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の3 fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 定義反証の内容

契約候補v1を成果物変更なしで読み、次を反証する。製品コードを作らない。反証の新作は一時領域のみ使用する。

1. **投影の遮断**：§7.2のallowlistが、G02現物`prepare_material`の結果形式（【実測】`material.content`、
   `review_spec.goal`・`criteria`・`constraints`が自由文）に対して自由文を漏らさず一意か。列挙項目が現物に
   実在するか（`material.content_sha256`・`identifier`・`line_count`、`result_schema`3項目、
   `review_spec.sha256`、`schema_version`、`status`、`material_package_sha256`）。
2. **変換の一意性**：§7.1のReviewStop変換（理由転記・`part_source: none`・sensitiveのみ3、他2、実行器5）が
   G02現物の停止形（`ReviewStop(reason)`のみ・停止元なし・理由8種）と整合し、後決め要素がないか。
3. **束縛位置の現物一致**：`material.content_sha256`が入力生bytesのSHA-256、`review_spec.sha256`が正規化済み
   仕様の正準JSON SHA-256であることを現物で機械照合する。
4. **基準の固定**：§6の変更対象2 file・再利用・保護対象の内容識別値が現物と一致するか。006 v4の停止表・
   書込み境界・機微検査（操作名23文字が手順3b除外対象）との整合に矛盾がないか。

必須の機械確認（各単独command・終了コード個別判定）：

- §6.1〜§6.3記載の全内容識別値の一致
- `.venv/bin/python3 -m pytest -q tests/test_operation_contract_run.py`（直近67件成功）
- `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`（直近158件成功）

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-one-item-review-safe-projection-v1-independent-review-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`開始可`または`修正要`とし、根拠、未接続条件、`修正要`の場合は最小数の停止原因と最小修正案を書く。
   事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`b82ccf30ada56f0cb763b0741a56bcb945f10481`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
