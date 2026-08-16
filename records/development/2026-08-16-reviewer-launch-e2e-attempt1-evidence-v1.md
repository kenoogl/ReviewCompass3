# 契約010 実E2E第1試行（e2e-010-001）Evidence v1

- 記録日：2026-08-16
- 記録者：Claude
- 実施根拠：利用者の明示指示「実E2Eを実施して。private rootは
  /Users/keno/.reviewcompass3-private/reviewer-launch で」（2026-08-16 chat）
- 結果：**停止（`response_model_unobserved`・終了コード2）。§9-8は未成立のまま**。停止の設計
  （raw保存・自動再試行なし）は仕様どおり機能した

## 1. 実施と停止【実測】

- 起動：`reviewcompass3-reviewer-launch launch`（対象＝完了レビュー依頼record、期待SHA-256
  `29819b3f…ddb13c`、run-id `e2e-010-001`）。
- 停止出力：`{"reason":"response_model_unobserved","source":"launch","status":"stopped"}`・終了コード2。
- 起動record（私有領域`e2e-010-001/launch.json`）：agyのprocess終了コード0、渡した環境変数は
  `HOME`・`LC_CTYPE`・`PATH`の3種のみ、`models_observed: []`、未加工出力SHA-256
  `bb4ed533400f84007a14bcf6ac3da1dec8c81ca919572546a74b2eae6d918c77`。

## 2. 診断【実測】

1. 保存済み未加工出力はstream-jsonではなく**日本語の平文2行**で、モデルは
   「`--output-format` についてのご質問でしょうか？」と聞き返していた。
2. 仮説：agyの`--print`は真偽旗ではなく**値（prompt本文）を取る旗**であり、直後の文字列
   `--output-format`がprompt本文として消費され、旗解析が最初の位置引数で停止し、末尾に置いた
   本来のpromptは捨てられた（Go標準flag形式の挙動）。
3. 局所検証（promptを送らない旗解析エラーの確認）：`agy --print`単独実行が
   `flag needs an argument: -print`で即時失敗し、値旗であることを確認。`--output-format`も同様。
4. 送出内容の確認：モデルへ実際に渡ったのは旗文字列（`--output-format`等）だけで、依頼recordの
   内容・repository情報は送られていない。応答も聞き返し2行で、危害・漏えい・大量課金はない。

## 3. 訂正【実測】

- `tools/reviewer_launch/core.py`の`build_arguments`を**全旗`--旗=値`形式・位置引数なし**へ訂正
  （promptは`--print=<本文>`。真偽旗`--disable-slash-commands`のみ単独形）。契約§7.1が固定する
  旗の集合・値（stream-json・schema・許可model・timeout 600s・禁止旗の不使用）は不変であり、
  引数の受け渡し形式だけの訂正である。
- 対象試験`test_fixed_arguments_exact`を厳密一致（全引数列の完全一致＋禁止旗の不在）へ更新。
  試験変更の理由：E2E実測による要求の誤解（旗形式）の訂正。
- 検証：対象試験32件単独緑、禁止認証隔離条件の正規全試験2,407件成功・終了コード0。

## 4. 残り

- §9-8実E2Eは未成立。再実施は**新しい試行識別子`e2e-010-002`**で利用者指示を得て行う
  （同一識別子の再利用は保存境界が拒否する設計）。
- 次回も停止し得る未知（stream-json内のmodel表記の形・result eventの形）は残る。停止の都度、
  保存済みrawで診断→訂正→利用者承認→新識別子で再起動の順を守る。
