# レビュー対象分類・工程分離の機械接続 実装開始判断 v1

- 判断日：2026-08-13
- 状態：`implementation_approved`
- 基準作業票：`docs/development/2026-08-13-review-target-process-connection-bootstrap-work-ticket-v1.md`
- 基準作業票SHA-256：`486a70f1d02833cf14ac571001bb94476c8ac716d8555d0e619c85967ca62f04`
- 修正作業票：`docs/development/2026-08-13-review-target-process-connection-bootstrap-work-ticket-v2.md`
- 修正作業票SHA-256：`4ada59c4d7f8bdecfdfc9622e83e15ac936bbfd1797bf3bd35dc756a7f825536`
- Codex修正後確認：`records/development/2026-08-13-review-target-process-connection-bootstrap-correction-review-v1.md`
- Claude修正後確認：`records/session-handoffs/2026-08-13-claude-review-target-process-connection-correction-review-result-v1.md`

## 1. 利用者判断

【記録】Codexと、利用者が手動で受け渡したClaudeの修正後確認は、ともに`開始可`、先行指摘解消、
止める指摘0件、報告不一致0件だった。主担当は次の三点を実装開始前の判断対象として提示し、
利用者は「承認」と回答した。

【判断】次の三点を採用し、実装開始を承認する。

1. 案Cを採用する。変更pathと対象種別を一つの構造化入力で対応付け、実際のGit差分と照合する。
2. 未分類、余分、未知種別は警告に留める。読めない入力、重複path、安全でないpath、型不正は
   入力不正とする。既存の利用者承認条件は変えない。
3. 作業票§3.1の4 path以内で、先に失敗を確認する試験を作り、その試験を変えずに実装を通す。
   第3段の試験整理、開発方針評価、設定体系の変更は混ぜない。

## 2. 実装中の境界

- 試験だけの失敗確認と、試験を変えない実装を別の意味単位として固定する。
- `config/development-policy.json`と`tools/development/policy.py`は変更しない。
- 新しい永続台帳、状態機械、強制関門、レビュー周回を追加しない。
- 警告は開発作業を一律停止するために使わない。
- 作業票の停止条件に該当した場合は、実装を広げず利用者へ返す。
- 第3段の398件分類、試験削減、外部送信、履歴書換え、段完了判断は行わない。

## 3. 次の作業

【判断】`tests/test_review_plan.py`に作業票§5.1の受入条件を追加し、現行実装で意図した理由により
失敗することを確認する。失敗確認を固定した後は試験を変更せず、許可された実装pathだけを変更する。
