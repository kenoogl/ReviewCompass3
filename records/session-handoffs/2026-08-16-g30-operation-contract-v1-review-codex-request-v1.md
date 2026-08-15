# 最小運用契約実行 契約候補v1 独立確認依頼record v1（Claude→Codex）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v1の作成担当）
- 依頼先：Codex（レビュー専任。本契約候補の作成を担当していない）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式。Claudeが`codex exec`で起動し、Humanは運搬しない
- レビュー種別：実装開始前の契約定義反証（読取り専用）
- 共通手順：`docs/development/work-review-protocol.md`

## 1. 役割分担（本依頼の境界）

- **Codexが行うのは本record§4の定義反証と、判定record 1件の作成・単独commitだけ**である。
- 判定後の後続——開始可の場合の実装開始、修正要の場合の契約次版への訂正——は**Claudeが実施**する。
- 利用者との会話接点はClaudeのみである。Codexは判定と根拠だけを判定recordへ書く。

## 2. 対象と前提

- 対象契約候補：`records/task-contract/2026-08-16-minimal-operation-contract-execution-candidate-v1.md`
  - SHA-256：`1ed92a89a96550fe1ea5df74fc40fd74102694e8bfefa07b5ec0c9d09df1bb6d`
  - 固定commit：`93fa28dee6850d71279f599735b69108ea91f200`
- 利用者の運用化目標：`records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md`
  - SHA-256：`c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a`
- 参考（同種契約の先例）：G24契約はv1が4原因（目的縮小の不明示、識別子の機微漏えい、正常・停止形式の非一意性、
  再利用・保護基準の未固定）、v2が1原因（計算方法未定義の識別値固定）で修正要となった。本候補v1は同種の穴を
  避ける意図で作成されている。
- 製品実装：未開始。外部送信：未実施・禁止継続。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の2 fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致・宛先違い・前提不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 定義反証の内容

契約候補v1を成果物変更なしで読み、次を反証する。製品コードを作らない。

1. **目的縮小の固定**：G30全体ではなく「承認済み運用契約一件による一部品実行と実行記録の着地」という縦切りで
   あること、既存G30基盤5 fileを変更しないこと、候補4を完了にしないこと、縮小採用が利用者判断に残ることが、
   誤解なく固定されているか。
2. **機微情報の遮断**：§8.2の検査順で、契約の全文字列key・値が既定5 patternと高乱雑性検査の対象になり、
   `expected_bindings`の正規SHA-256値だけが除外されるか。実行記録・停止結果へ自由文・絶対path・例外本文が
   漏れない形になっているか。
3. **正常・停止形式の一意性**：同じ入力から実行記録bytes、`contract_sha256`・`part_result_sha256`・
   `record_sha256`、停止結果が一意に定まるか。§10.2の束縛照合表が部品の実際の結果形式
   （`tools/reviews/one_item_review.py`のprepare結果、G08結果、G24結果）と一致するか。
4. **再利用・保護基準と書込み境界**：§6の再利用6 file・保護8 path・機微規則の内容識別値が現物と一致するか
   （機械計算で確認する）。file書込みが「実行記録一件・新規作成専用・停止時無作成・書込み後再読込一致」に
   閉じており、実装者が後決めできる要素（計算方法未定義の固定値、基準commit欠落、試験command欠落）が残って
   いないか。

必須の機械確認（各単独command・終了コード個別判定）：

- §6.1の6 file、§6.2の1 file、§6.3の8 pathの内容識別値の一致
- `.venv/bin/python3 -m pytest -q tests/test_one_item_review.py`
- `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
- `.venv/bin/python3 -m pytest -q tests/test_one_requirement_feature_source.py`
- `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py`

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-16-minimal-operation-contract-execution-v1-independent-review-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`開始可`または`修正要`とし、根拠、未接続条件、`修正要`の場合は同じ原因の変種をまとめた最小数の
   停止原因と最小修正案を書く。事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. §4の各commandの結果（件数と終了コード）を記載する。
5. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`93fa28dee6850d71279f599735b69108ea91f200`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordを意味単位commitへ固定し、`git status --short`が空であること、`git diff --check`が終了コード0であることを
確認する。
