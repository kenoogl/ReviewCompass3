# G24契約候補v3 Codex引継ぎメモ v1

- 作成日：2026-08-15
- 引継ぎ理由：契約候補v3の作成をClaudeが担当したため、利用者指示により限定再確認を作成者以外のCodexへ依頼する
- 現在の作業：G24「要求固定・機能分割・由来追跡」の最初の縦切りに関する作業契約定義
- 製品コード：未実装
- 外部送信：未実施・禁止継続
- 次の担当：Codex

「作業契約」は、目的、入力、範囲、確認方法、停止条件を実装前に固定する約束である。
「内容識別値」は、内容の変化を機械検出するSHA-256値である。
「限定再確認」は、直前版で閉じた境界を全面再走査せず、訂正1点と退行の有無だけを読取り専用で確認する作業である。

## 1. 結論から見た現在地

【記録】契約候補v2のClaude独立再確認は`修正要`と判定した。v1の4停止原因のうち3系統（目的縮小、識別子の機微漏えい、
正常・停止形式の非一意性）は閉じ、残る停止原因は1件だった。

【実測】停止原因は、§6.2の機微情報規則の「規則内容識別値」が計算方法未定義のまま固定され、実装者の後決めになる
ことである。この値のrepository内の出現は契約v2の1箇所だけで、妥当と考えられる計算方法を三回の機械走査で
計106通り試しても一致0件だった。

【記録】利用者は最小修正(a)（規則内容識別値の固定を撤回し、照合対象をfile内容識別値・公開関数2名・
既定pattern件数5へ限定する）を選択し、契約候補v3の作成を指示した。

【実測】v3は作成済みでcommit`2935825df00274d7c6b782687305b8e0c171eb44`へ固定済みだが、限定再確認は未実施である。
したがって、実装開始不可である。

## 2. 今回の引継ぎ対象

### 2.1 v2独立再確認記録

- path：`records/development/2026-08-15-one-requirement-candidate-consistency-check-contract-v2-independent-rereview-v1.md`
- SHA-256：`270505d0f073fb59daf4d963824ca0eb9e2c854c580ed46dde2f63181242eb38`
- 判定：`correction_required`（停止原因1件）
- repository成果物変更：0件

### 2.2 訂正済み契約候補v3

- path：`records/task-contract/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3.md`
- SHA-256：`7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081`
- 状態：限定再確認待ち
- 実装：未開始

### 2.3 v3で行った訂正

【記録】訂正は最小修正(a)の範囲だけである。

- §6.2から規則内容識別値`3c736257…`を削除し、「規則の変更は上記file内容識別値の不一致として検出する」へ変更した。
- 受入条件13の照合対象を、§6.2のfileの内容識別値、公開関数`default_pattern_rules`と`find_high_entropy`の存在、
  既定pattern件数5へ限定した。
- 見出しの契約版、supersedes、訂正根拠、訂正範囲、利用者判断と、§15の次作業文を更新した。
- 上記以外の本文（§1〜§5、§6.1、§6.3、§7〜§12、受入条件13以外、§14）は1文字も変更していない。

## 3. Codexが最初に行う一作業

契約候補v3を成果物変更なしで読み取り、v2の停止原因1件が閉じたことと、v2で閉じた境界に退行がないことだけを
限定再確認する。製品コードを作らない。

### 3.1 開始時の確認

1. `AGENTS.md`と`TODO_NEXT_SESSION.md`を読む。
2. `git status --short`が空であることを確認する。
3. 本メモ、v2再確認記録、契約候補v3の内容識別値を機械計算し、本メモ記載値と一致することを確認する。
4. Python実行は常に`.venv/bin/python3`を使う。

### 3.2 再確認する2点

1. §6.2と受入条件13の照合対象がfile内容識別値・公開関数2名・既定pattern件数5だけになり、計算方法や基準値を
   実装者が後決めする要素が残っていないか。各照合対象が現物（`tools/session_logs/redaction.py`、SHA-256
   `aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`、公開2関数、既定pattern 5件）と一致するか。
2. v2とv3の全文差分が§2.3の訂正範囲に限定され、v2で閉じた3系統（目的縮小、機微漏えい、非一意性）と
   §6.1・§6.3の固定基準に退行がないか。

### 3.3 必須の機械確認

次はそれぞれ単独commandとして実行し、終了コードを個別に判定する。

`.venv/bin/python3 -m pytest -q tests/test_requirements_feature_partition.py tests/test_requirements_fixed_inputs.py tests/test_requirement_boundary_relations.py tests/test_requirements_source_trace.py tests/test_requirements_batch.py`

直近結果：59件成功、終了コード0。

`.venv/bin/python3 -m pytest -q tests/test_requirements_artifact_layout.py tests/test_requirements_unified_migration.py`

直近結果：21件成功、終了コード0。

`.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`

直近結果：107件成功、終了コード0。

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
- 訂正点と退行の有無を再確認してから利用者判断へ進む。

## 5. 参考の非停止観測

【記録】v2再確認記録§5に、停止原因に数えない観測2件（高乱雑性検査が24文字以上のID形式でも停止し得ること、
実装pathと契約IDが旧名`one_requirement_feature_source`のままであること）がある。これらの扱いは利用者の3択に
残してあり、本限定再確認の合否に含めない。

## 6. 未実施

- 契約候補v3の限定再確認。
- 利用者による縮小境界、契約採用、案C実装開始の判断。
- 対象試験の作成と失敗確認。
- 製品コード、正式入口、実行名の実装。
- 正規全試験、独立完了レビュー、製品受入。
- G24の要求作成責務。
- 候補4以降。
- 外部送信、実利用者資料の使用。

## 7. 引継ぎ完了条件

本メモと更新済み`TODO_NEXT_SESSION.md`を一つの意味単位commitへ固定し、`git status --short`が空であること、
TODO検査と`git diff --check`が終了コード0であることを確認する。
