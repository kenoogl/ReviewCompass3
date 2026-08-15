# 一件レビュー安全投影 契約候補v2 限定再確認依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v2の訂正担当）
- 依頼先：Codex（レビュー専任）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：訂正1点と退行の有無だけの限定再確認（読取り専用）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担

- **Codexが行うのは§4の限定再確認と、判定record 1件の作成・単独commitだけ**である。全面再走査をしない。
- 判定後の後続はClaudeが実施する。

## 2. 対象と前提

- 対象契約候補v2：`records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v2.md`
  - SHA-256：`9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603`
  - 固定commit：`14a74a5a00ac4e38412e1b27bb9ae7ee2b915952`
- 訂正根拠（v1独立確認、判定`修正要`・停止原因1件）：
  `records/development/2026-08-16-one-item-review-safe-projection-v1-independent-review-v1.md`
  - SHA-256：`b211626ba83409e9a892c202c0903e1363b535dc93b6f390627d42361ba3d33f`
- 直前版契約v1：`records/task-contract/2026-08-16-one-item-review-safe-projection-candidate-v1.md`
  - SHA-256：`b42232fd0f6a559a680c5447845502a0947b0d96caaaddae208c8bf0c94a2f9b`
- v2の訂正は1点だけである：§7.1の転記理由集合を、prepare経路の2関数が到達し得る閉じた8種
  （`invalid_arguments`、`invalid_path`、`invalid_schema`、`invalid_utf8`、`sensitive_data_remaining`、
  `size_limit_exceeded`、`unreadable_input`、`absolute_path_remaining`）だけへ一意化し、8種以外
  （organize経路専用の`stale_material`を含む）は`internal_failure`と明記した。§6.2へ現物の到達可能理由の
  注記、受入条件5へ集合外理由の`internal_failure`反証を追加した。見出しと§11の次作業文も更新した。
  これ以外の本文は変更していない。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の3 fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 限定再確認の内容

契約候補v2を成果物変更なしで読み、次の2点だけを確認する。

1. **訂正1点が閉じたか**：v1停止原因（8種の記載と9件の列挙の競合）が、閉じた8理由の列挙と集合外の
   `internal_failure`固定で一意になったか。8理由がprepare経路の現物到達可能集合と一致するか
   （v1確認の実測を引用してよい）。
2. **退行がないか**：v1とv2の全文差分が§2記載の訂正範囲に限定され、v1で問題なしとされた境界
   （投影allowlist、束縛照合位置、変更対象・保護基準、006整合）に退行がないか。

必須の機械確認（各単独command・終了コード個別判定）：

- §6.1〜§6.3記載の全内容識別値の一致

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-one-item-review-safe-projection-v2-limited-rereview-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`開始可`または`修正要`とし、根拠を書く。事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`14a74a5a00ac4e38412e1b27bb9ae7ee2b915952`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
