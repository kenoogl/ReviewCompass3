# 最小運用契約実行 契約候補v3 限定再確認依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v3の訂正担当）
- 依頼先：Codex（レビュー専任）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式
- レビュー種別：訂正1点と退行の有無だけの限定再確認（読取り専用）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担

- **Codexが行うのは§4の限定再確認と、判定record 1件の作成・単独commitだけ**である。全面再走査をしない。
- 判定後の後続はClaudeが実施する。

## 2. 対象と前提

- 対象契約候補v3：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v3.md`
  - SHA-256：`d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85`
  - 固定commit：`8351622efb8c66b018fe1ccd7e3e69f905c50a3b`
- 訂正根拠（v2限定再確認、判定`修正要`・停止原因1件）：
  `records/development/2026-08-16-minimal-operation-contract-execution-v2-limited-rereview-v1.md`
  - SHA-256：`1926cfa2f4ebbb45d500813348e61cebc9f25018eae22194d28afaaa5aec005d`
- 直前版契約v2：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v2.md`
  - SHA-256：`927965f9502c0762c0ba289968d37d16237ae0ef433f15c2ac53cc8dacd94090`
- v3の訂正は1点だけである：§7手順3のhard link成功を「公開の確定点」と定義し、手順5（公開後の清掃）を追加、
  確定点後の一時名削除失敗を`partial_cleanup_failed`（source `output`・終了コード6・空stderr）で停止し、
  最終名は公開済み正本として残存、一時名は同一inodeで残存、回復境界は利用者の一時名削除、再実行は
  `invalid_output_root`で停止と一意化した。§11の一般規則と表、§13.16・16b・16c、§14、§15を同じ定義へ
  合わせた。見出し（版・supersedes・訂正根拠・訂正範囲）も更新した。これ以外の本文は変更していない。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の3 fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致・宛先違い・前提不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 限定再確認の内容

契約候補v3を成果物変更なしで読み、次の2点だけを確認する。

1. **訂正1点が閉じたか**：v2停止原因（公開確定後の一時名削除失敗の未定義）が、確定点の定義と
   `partial_cleanup_failed`の一意な状態・終了コード・残留・回復境界で閉じたか。書込み経路の全失敗位置
   （作成・書込み・照合・hard link作成・公開前回収・公開後削除）が§7・§11で漏れなく一意に定義され、
   実装者の後決め要素が残っていないか。
2. **退行がないか**：v2とv3の全文差分が§2記載の訂正範囲に限定され、v2で開始可とされた境界
   （registry縮小、目的縮小の固定、§8.2機微検査、§10.2束縛照合位置4件、固定内容識別値、基準commit）に
   退行がないか。

必須の機械確認（各単独command・終了コード個別判定）：

- §6.1の再利用4 file、§6.2の1 file、§6.3の保護10 pathの内容識別値の一致
- `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
- `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`
- `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`
- `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py`

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-minimal-operation-contract-execution-v3-limited-rereview-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`開始可`または`修正要`とし、根拠、未接続条件、`修正要`の場合は最小数の停止原因と最小修正案を書く。
   事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. §4の各commandの結果（件数と終了コード）を記載する。
5. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`8351622efb8c66b018fe1ccd7e3e69f905c50a3b`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
