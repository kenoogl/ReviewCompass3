# レビュー対象分類・工程分離の機械接続 実施証跡 v1

- 実施日：2026-08-13
- 実装開始判断commit：`f254cfec48455ab6c317343633e97b81903d1ba3`
- 失敗確認commit：`4d3dc9417738f8d2dd3f590e4ad06dfacf256fbb`
- 実装commit：`61fd0c5c34bd9bf9bbc36bd5029e7c046fa22593`
- 状態：`completion_review_pending`
- 外部送信：未実施
- 第3段：未開始

## 1. 変更範囲

【実測】失敗確認commitは`tests/test_review_plan.py`一件だけを変更した。実装commitは、次の三件だけを
変更した。

- `tools/development/review_plan.py`
- `tools/development/review_plan_cli.py`
- `docs/development/prompts/review-plan-run.md`

【実測】`tests/test_review_plan.py`のGit物体識別値は、失敗確認commitと実装commitでともに
`7cc0623c5e100e5ca3f24035032ee42f5404c62f`である。実装中に試験を変更していない。
`config/development-policy.json`、`tools/development/policy.py`、第3段の試験群と台帳は変更していない。

## 2. 失敗確認と実装後確認

各試験指令は単独で実行し、終了コードを確認した。

| 状態 | 指令 | 終了コード | 結果 |
| --- | --- | ---: | --- |
| 現行作業ツリーでの失敗確認 | `.venv/bin/python3 -B -m pytest tests/test_review_plan.py` | 1 | 9件失敗。分類入力と対象別工程が未実装であることを検出 |
| `4d3dc94`の使い捨て複製での再現 | `.venv/bin/python3 -B -m pytest tests/test_review_plan.py -q` | 1 | 9件失敗。同じ未実装理由を履歴から再現 |
| 実装後の対象試験 | `.venv/bin/python3 -B -m pytest tests/test_review_plan.py` | 0 | 9件成功 |
| 関連試験 | `.venv/bin/python3 -B -m pytest tests/test_review_plan.py tests/test_development_policy.py` | 0 | 34件成功 |

## 3. 公式全試験

【実測】公式入口は`.venv/bin/python3 -B -m tools.development.policy_test_runner --suite full --receipt <path>`を
使い、代替実行は行っていない。

最初に結果を受け取れる実行は、1,738件成功、1件失敗、終了コード1だった。失敗は
`tests/test_claude_bootstrap_adversarial.py::test_token_claim_is_once_only_for_sequential_and_parallel_calls`で、
並行処理の一方が承認fileを移動した直後に、他方が同じfileを参照して`FileNotFoundError`になった。
受領証は`/private/tmp/review-target-process-connection-full-receipt-v3.json`、SHA-256は
`f7b0be4b171d51277c72d55de5488af8f26ad0b9207b3087c6b7fea5f5d6007a`である。

【実測】当該既存試験だけを単独再実行すると1件成功、終了コード0だった。成果物を変更せず公式入口を
再実行し、1,739件成功、失敗・エラー・除外0、終了コード0となった。合格受領証は
`/private/tmp/review-target-process-connection-full-receipt-v4.json`、SHA-256は
`44acb3bc31f70adcc39d61450e88645f19780489c8b8798010da0870e874ab70`、状態識別値は
`6453617083199599d9dd5ef0509b924f7c0d9aed2d2c8b342d57d31b8a8616ff`である。

【判断】最初の不合格を隠さず残す。今回の変更と無関係な並行処理試験の偶発失敗であり、単独再実行と
変更なしの公式全試験再実行がともに成功したため、今回の実装を不合格とする根拠にはしない。

## 4. 欠陥投入

実装commitの使い捨て複製をリポジトリ外に四つ作り、各複製へ一種類だけ欠陥を入れた。
対象試験はすべて不合格となり、誤った実装を合格にしなかった。

| 欠陥 | 対象試験の終了コード | 検出結果 |
| --- | ---: | --- |
| `validator_code`を文書変更へ誤対応 | 1 | 1件失敗。検査器用の欠陥投入確認が消えたことを検出 |
| Git差分の先頭pathを一件落とす | 1 | 3件失敗。変更一覧、対象群、余分pathの不一致を検出 |
| 未分類・余分・未知種別の警告を空にする | 1 | 1件失敗。警告付き完了が通常完了になる誤りを検出 |
| 分類入力SHA-256を計画識別値の計算から外す | 1 | 1件失敗。独立再計算した識別値との不一致を検出 |

## 5. 独立した別計算

【実測】`/private/tmp/review_target_process_oracle.py`（SHA-256
`4c1ba9cf37fc9a9c0bfbf6ee15b9e91d79c0ef14b7cd28c218aa67c4e10292f9`）は、使い捨てGitリポジトリで
六種類の対象を作り、製品の群分け処理を使わずにGit差分と既存方針評価から期待値を計算した。

終了コード0で、変更path 6件、対象群6件、各群の確認項目、利用者承認待ち、警告0件、計画識別値の
一致を確認した。一時処理はリポジトリ外であり、成果物へ含めていない。

## 6. 手戻りの記録

### 6.1 長時間実行の待受け

- 対象操作：公式全試験
- 期待する実行役：機械
- 実際の実行役：機械
- 手作業理由：なし
- 事象：最初の二回は30秒の待受けが終了し、結果と受領証を取得できなかったため合否不明とした
- 根拠：指定した`v1`、`v2`の受領証が存在しないことを確認
- 機械処理候補：長時間指令は開始後に同じ端末実行を継続して待ち受ける
- 経路：同じ公式入口を継続待受け付きで再実行し、`v3`と`v4`の受領証を取得して解消

### 6.2 既存並行処理試験の偶発失敗

- 対象操作：公式全試験
- 期待する実行役：機械
- 実際の実行役：機械
- 手作業理由：なし
- 事象：既存並行処理試験1件がfile移動と参照の競合で一度失敗
- 根拠：不合格受領証`v3`と、同試験単独成功、変更なしの合格受領証`v4`
- 機械処理候補：当該並行処理試験の安定性評価は今回の実装範囲外の候補とする
- 経路：現在作業では修正せず、失敗と再確認結果を完了レビューへ渡す

## 7. 未実施

【未実施】新しい永続台帳、状態機械、強制関門、方針評価器、レビュー周回は追加していない。
第3段の398件分類、試験削減、外部送信、push、履歴書換え、段完了判断は行っていない。
完了レビューと利用者への完了報告は未実施である。
