# 無工具Claude疎通 修復範囲訂正 v2

- 日付：2026-08-11
- Human指示：`正せ。`
- 差替え対象：`2026-08-11-claude-bootstrap-review-repair-scope-v1.md` §2の履歴制限
- 外部送信：禁止

## 訂正理由

v1は、レビュー対象commitから現在までの変更を、完了レビュー記録と送信承認記録の2件だけに制限した。
この規則は、正規手順で必要なレビュー計画の記録まで拒否するため過剰である。

## 残す検査

- 完了レビュー記録が固定pathにあり、Gitへ記録済みである。
- 完了レビュー記録の識別子とSHA-256が送信承認記録と一致する。
- 完了レビュー記録が`verified`で、blocking所見が0件である。
- 完了レビュー記録の対象commit、固定送信目録のSHA-256、固定二文の順序SHA-256が記録されている。
- 子processへ渡す環境変数は固定した許可一覧だけである。

## 削除する検査

- レビュー対象commitが現在の`HEAD`の祖先かを送信時に再判定する処理。
- レビュー対象commit以後の変更pathを全列挙する処理。
- 変更pathが完了レビュー記録と送信承認記録の2件だけかを判定する処理。
- レビュー対象commit時点の送信目録をGit履歴から再読込する処理。

固定送信目録の現在内容、完了レビュー記録、送信承認記録の結び付けは従来どおり検査する。

## 受入条件

- `CB-RC-001`：レビュー対象commit後に機械生成したレビュー計画を記録しても、正しい承認処理は停止しない。
- `CB-RC-002`：既存の完了レビュー不一致5例と秘密値4例は引き続き拒否する。
- `CB-RC-003`：既存の固定試験と公式全試験に新しい回帰を作らない。

## 変更可能path

- `tools/development/claude_bootstrap.py`
- `tests/test_claude_bootstrap_adversarial.py`
- `records/development/2026-08-11-claude-bootstrap-manifests/review-repair-correction-*`
- `records/development/2026-08-11-claude-bootstrap-review-repair-*`

新しい監視機能、schema、停止code、外部入口は追加しない。
