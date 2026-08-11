# 無工具Claude疎通 完了レビュー・秘密値修復 範囲固定 v1

- 日付：2026-08-11
- Human判断：`CB-REVIEW-F-001〜002`の修復を承認
- risk：`high`
- 外部送信：禁止

## 1. 対象

次の2件だけを修復する。

- `CB-REVIEW-F-001`：完了レビュー記録がなくても送信処理へ進める。
- `CB-REVIEW-F-002`：固定外の秘密値が子プロセスへ継承される。

旧v6範囲試験、実際のClaude起動、認証、通信、送信、一般的な秘密検出機能は対象外とする。

## 2. 完了レビューの結び付け

送信承認記録は、固定path
`records/development/claude-bootstrap-completion-review-v1.json`にある完了レビュー記録の
識別子、SHA-256、対象commitを持つ。

完了レビュー記録は次を完全一致で持つ。

- `schema_version: 1`
- `record_kind: claude_bootstrap_completion_review`
- 固有の`review_id`
- `status: verified`
- 対象`target_commit`
- 固定送信目録の`manifest_sha256`
- 固定二文の`ordered_payload_sha256`
- `blocking_finding_count: 0`

プログラムは、記録が通常fileであること、Gitへ記録済みであること、SHA-256、識別子、状態、対象commit、
目録との結び付けを確認する。対象commitは現在の`HEAD`の祖先であり、対象commitから`HEAD`までの変更は
完了レビュー記録と送信承認記録だけでなければならない。どれか一つでも違えば、外部プロセス作成前に
`completion_review_invalid`で停止する。

## 3. 子プロセスの環境

親プロセスの環境をほぼそのまま渡す方式を廃止する。子プロセスへ渡せる名前を次に固定する。

- `HOME`
- `PATH`
- `TMPDIR`
- `LANG`
- `LC_ALL`
- `LC_CTYPE`
- `TERM`
- `NO_COLOR`

親環境に存在する項目だけを渡す。上記以外は、名前や値を推測して判定せず、すべて渡さない。

## 4. 受入条件

- `CB-RR-001`：完了レビュー記録の欠落、未記録、識別子不一致、SHA-256不一致、`verified`以外、
  対象commit不一致を、外部プロセス作成前に拒否する。
- `CB-RR-002`：送信承認記録が完了レビューの識別子、SHA-256、対象commitへ結び付く。
- `CB-RR-003`：許可一覧外の`AWS_SECRET_ACCESS_KEY`その他の秘密値が、子プロセス環境と公開結果へ
  現れない。
- `CB-RR-004`：既存の固定32試験、既存Pilot・egress試験、公式全試験に新しい回帰を作らない。
- `CB-RR-005`：理由付きRED対応表v2が、収集失敗ではなく予定した2理由との一致を確認する。

## 5. 変更可能path

- `tools/development/claude_bootstrap.py`
- `tests/test_claude_bootstrap_adversarial.py`
- `tests/fixtures/claude_bootstrap/helpers.py`
- `records/development/2026-08-11-claude-bootstrap-manifests/review-repair-*`
- `records/development/2026-08-11-claude-bootstrap-review-repair-*`

既存の試験関数の期待、`tools/egress/`、既存Pilot、CLI入口、Workflow台帳は変更しない。

## 6. 作業順序

1. fixtureと新規受入試験を先に変更する。
2. 理由付きRED対応表v2を実行し、予定した2理由で失敗することを確認する。
3. 試験と範囲固定をコミットする。
4. 試験を変更せずproductionを実装する。
5. 関連試験と公式全試験を実行し、結果を記録してコミットする。
