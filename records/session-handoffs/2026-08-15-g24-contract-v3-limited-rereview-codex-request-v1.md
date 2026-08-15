# G24契約候補v3 限定再確認依頼record v1（Claude→Codex）

- 作成日：2026-08-15
- 依頼元：Claude（操縦・契約候補v3の作成担当）
- 依頼先：Codex（レビュー専任。v3の作成を担当していない）
- 受け渡し方式：`docs/development/pilot-driven-record-handoff.md`のrecord正本方式。Claudeが`codex exec`で起動し、Humanは運搬しない
- supersedes：`records/session-handoffs/2026-08-15-g24-contract-v3-codex-handoff-v1.md`、SHA-256 `1b966f1fdcd51f6ed46e3b9bb83c6f3049cff9975ac29bbc1e95a2336c913fe4`
- supersedes理由：旧メモは（1）HumanがCodexへ運搬する廃止方向の旧方式を前提にし、（2）判定後の後続作業までCodexへ割り当てていた。本recordで受け渡し方式と役割分担を訂正する

「限定再確認」は、直前版で閉じた境界を全面再走査せず、訂正1点と退行の有無だけを読取り専用で確認する作業である。
「内容識別値」は、内容の変化を機械検出するSHA-256値である。

## 1. 役割分担（本依頼の境界）

- **Codexが行うのは本record§4の限定再確認と、判定record 1件の作成・単独commitだけ**である。
- 判定後の後続——`開始可`の場合の利用者への一判断提示、`修正要`の場合の契約次版への訂正、その後の実装——は
  **すべてClaudeが実施**する。Codexは判定recordをcommitして停止し、後続作業に着手しない。
- 利用者との会話接点はClaudeのみである。Codexは利用者への質問・提案を判定recordへ書かず、判定と根拠だけを書く。

## 2. 対象と前提

- 対象契約：`records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md`
  - SHA-256：`7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
  - 固定commit：`2935825df00274d7c6b782687305b8e0c171eb44`
- 訂正根拠（v2独立再確認）：`records/development/2026-08-15-one-requirement-candidate-consistency-check-contract-v2-independent-rereview-v1.md`
  - SHA-256：`270505d0f073fb59daf4d963824ca0eb9e2c854c580ed46dde2f63181242eb38`
  - 判定：`correction_required`（停止原因1件：§6.2の機微情報規則の「規則内容識別値」が計算方法未定義のまま固定され、実装者の後決めになる）
- 直前版契約（v2）：`records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v2.md`
  - SHA-256：`a4d544e29d877ac45dca65b748557387bd1b04f58adda59ffacf91fc47a216bb`
- v3の訂正は最小修正(a)：§6.2の規則内容識別値の固定を撤回し「規則の変更はfile内容識別値の不一致として検出する」へ変更、
  受入条件13の照合対象をfileの内容識別値・公開関数`default_pattern_rules`と`find_high_entropy`の存在・既定pattern件数5へ限定、
  見出し（契約版・supersedes・訂正根拠・訂正範囲・利用者判断）と§15の次作業文の更新。これ以外の本文は変更していない。
- 製品コード：未実装。外部送信：未実施・禁止継続。

## 3. 開始時の確認（Codexの鮮度検査）

1. 自分宛の最新依頼recordが本recordであることをGit履歴から機械特定する。
2. `git status --short`が空であることを確認する。
3. §2の3 fileの内容識別値を機械計算し、本record記載値と一致することを確認する。
4. 不一致・宛先違い・前提不一致の場合は、作業せずその旨を判定recordへ書いて停止する。
5. Python実行は常に`.venv/bin/python3`を使う。

## 4. 限定再確認の内容

契約候補v3を成果物変更なしで読み、次の2点だけを確認する。製品コードを作らない。全面再走査をしない。

1. **訂正1点が閉じたか**：契約§6.2と受入条件13の照合対象がfile内容識別値・公開関数2名・既定pattern件数5だけになり、
   計算方法や基準値を実装者が後決めする要素が残っていないか。各照合対象が現物（`tools/session_logs/redaction.py`、
   SHA-256 `aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`、公開2関数、既定pattern 5件）と一致するか。
2. **退行がないか**：v2とv3の全文差分が§2記載の訂正範囲に限定され、v2で閉じた3系統（目的縮小、識別子の機微漏えい、
   正常・停止形式の非一意性）と契約§6.1・§6.3の固定基準に退行がないか。

次はそれぞれ単独commandとして実行し、終了コードを個別に判定する。

`.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`

直近結果：59件成功、終了コード0。

`.venv/bin/python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py`

直近結果：21件成功、終了コード0。

`.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`

直近結果：107件成功、終了コード0。

`git diff --exit-code 0583863e4612f7f14b5db131beb627677b99017a -- tools/requirements/boundary_relations.py tools/requirements/feature_partition.py tools/requirements/fixed_inputs.py tools/requirements/requirement_batch.py tools/requirements/source_trace.py tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`

期待：終了コード0、差分0。

参考：v2再確認記録§5に停止原因へ数えない観測2件（高乱雑性検査が24文字以上のID形式でも停止し得ること、実装pathと
契約IDが旧名のままであること）がある。これらは本限定再確認の合否に含めない。

## 5. 判定recordの作成と停止（Codexの成果物）

1. 判定recordを次のpathへ作成する。
   `records/development/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3-limited-rereview-v1.md`
2. recordの冒頭に、Reviewerのmodel名とreasoning effort（起動時に表示された値）を記載する。
3. 判定は`開始可`または`修正要`とし、根拠、未接続条件、`修正要`の場合は同じ原因の変種をまとめた最小数の停止原因と
   最小修正案を書く。事実の主張には【実測】【記録】【推測】のラベルを付ける。
4. §4の各commandの結果（件数と終了コード）を記載する。
5. **そのrecord 1件だけをstageして単独commitし、停止する。** record以外のfileを変更しない。TODO更新、契約訂正、
   利用者への提案、後続作業への着手を行わない。

## 6. Claudeの事後照合（参考）

Claudeは応答後に、(a) 判定recordのcommitが対象commit`2935825df00274d7c6b782687305b8e0c171eb44`より後にあること、
(b) 変更pathが判定record 1件だけであること、(c) 判定内容、を機械照合してから後続へ進む。

## 7. 依頼完了条件

本recordと更新済み`TODO_NEXT_SESSION.md`を一つの意味単位commitへ固定し、`git status --short`が空であること、
TODO検査と`git diff --check`が終了コード0であることを確認する。Codexの起動は本record固定後、利用者の指示を受けて行う。
