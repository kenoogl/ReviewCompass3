# 最小運用契約実行 契約候補v2 限定再確認依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v2の訂正担当）
- 依頼先：Codex（レビュー専任）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：訂正2点と退行の有無だけの限定再確認（読取り専用）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担

- **Codexが行うのは§4の限定再確認と、判定record 1件の作成・単独commitだけ**である。全面再走査をしない。
- 判定後の後続はClaudeが実施する。Codexは判定と根拠だけを判定recordへ書く。

## 2. 対象と前提

- 対象契約候補v2：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v2.md`
  - SHA-256：`927965f9502c0762c0ba289968d37d16237ae0ef433f15c2ac53cc8dacd94090`
  - 固定commit：`dd5375ab52eb787252d6c814a8a18378d8e3cabb`
- 訂正根拠（v1独立確認、判定`修正要`・2系統）：
  `records/development/2026-08-16-minimal-operation-contract-execution-v1-independent-review-v1.md`
  - SHA-256：`3eb9eba738171ac0f66572de1da5454377684f5ab4d4c110e85397c86657e5ca`
- 直前版契約v1：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v1.md`
  - SHA-256：`1ed92a89a96550fe1ea5df74fc40fd74102694e8bfefa07b5ec0c9d09df1bb6d`
- v2の訂正は2点だけである：(1) registryから`one_item_review_prepare`を除外しG08・G24の2操作へ縮小
  （G02の2 fileは§6.3保護対象へ移動、範囲外§5.2へ後続条件を明記）、(2) §7の書込みを「事前検査→一時成果
  （新規作成専用）→bytes照合→hard linkによる上書き不能な原子公開→一時成果削除、失敗時は自作一時成果だけを
  回収」の二段へ再定義し、§11の停止表・処理順・受入条件13・14・16・16b・18・19・21を整合させた。
  見出し（版・supersedes・訂正根拠・訂正範囲・利用者判断）と§15の次作業文も更新した。これ以外の本文は変更していない。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の3 fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致・宛先違い・前提不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 限定再確認の内容

契約候補v2を成果物変更なしで読み、次の2点だけを確認する。

1. **訂正1（registry縮小）が閉じたか**：v1停止原因1（一件レビュー部品の呼出し形式・自由文埋め込み・停止形式の
   現物不一致）が、2操作への縮小と§5.2の後続明記で閉じたか。残る2入口`tools.design.one_design_acceptance_entry.main`
   と`tools.requirements.one_requirement_feature_source_entry.main`が、契約§6.1の共通形（`main(arguments, *, output)`、
   停止結果に`reason`・`source`、正常・停止結果に自由文・絶対path・例外本文なし）と現物で一致するか（機械照合）。
2. **訂正2（書込み境界）が閉じたか**：v1停止原因2（停止時無作成と書込み後失敗の矛盾）が、一時成果＋hard link
   原子公開＋自作一時成果の回収で両立するか。作成後失敗の残留が「回収失敗時の一時名だけ・最終名は未作成」へ
   一意に限定され、実装者の後決め要素が残っていないか。§11の停止表・処理順が§7の二段書込みと矛盾しないか。

退行確認：v1で問題なしとされた境界（目的縮小の固定、§8.2機微検査、§10.2束縛照合位置4件、固定内容識別値、
基準commit、必須試験）に、v2の差分による退行がないか。v1とv2の全文差分が§2記載の訂正範囲に限定されているか。

必須の機械確認（各単独command・終了コード個別判定）：

- §6.1の再利用4 file、§6.2の1 file、§6.3の保護10 pathの内容識別値の一致
- `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
- `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`
- `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`
- `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py`

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-minimal-operation-contract-execution-v2-limited-rereview-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`開始可`または`修正要`とし、根拠、未接続条件、`修正要`の場合は最小数の停止原因と最小修正案を書く。
   事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. §4の各commandの結果（件数と終了コード）を記載する。
5. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`dd5375ab52eb787252d6c814a8a18378d8e3cabb`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
