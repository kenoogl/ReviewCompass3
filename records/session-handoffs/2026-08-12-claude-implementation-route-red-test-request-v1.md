# Claude実装委譲経路 第1縦切り RED受入試験作成依頼 v1

- 状態：`fixed_request`
- 実装担当：新しい会話状態の`gpt-5.6-sol` Codex実装用サブエージェント
- 対象基準commit：この依頼を含むcommit
- 変更可能path：`tests/test_claude_implementation_route.py`だけ
- 製品実装：禁止
- Claude起動、外部送信：禁止

## 1. 固定入力

- 範囲固定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v3.md`
- 範囲固定SHA-256：`063d4299e78c11c2060b012ff7f09d7feaa2eca318e879e35bd418a7015e689f`
- RED開始裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-red-start-human-decision-v1.md`
- 権限裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-permission-finding-human-decision-v1.md`
- v3監査：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-audit-raw-v3.json`
- v3判定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-judgment-raw-v3.json`
- v3独立範囲レビュー：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-review-raw-v3.json`
- 既存入口：`tools/development/pilot_collaboration.py`、`tools/development/pilot_collaboration_cli.py`
- 共通不変保存：`tools/bootstrap/immutable_result_store.py`
- 信頼済み配置：`tools/deployment/trusted_claude_transport.py`

## 2. 今回の最小縦切り

一つの合成Git repositoryと偽のClaude応答を使い、次の公開入口を期待する受入試験を作る。公開名は試験内で
次に固定する。

- module：`tools.development.claude_implementation_route`
- `prepare(repository, config_path, private_root)`：固定入力とHuman承認を検査し、repository外の一時worktreeと
  第1ターンの固定起動情報を作る。
- `record_turn(repository, private_root, run_id, turn, launch_path, raw_path)`：未加工結果と道具使用を不変保存し、
  全変更pathを機械照合し、`test`ターンでは機械処理だけが固定試験commandを実行してREDを確認する。
  `implementation`ターンでは固定済み試験指紋を確認して同じcommandのGREENを確認する。
- `status(repository, private_root, run_id)`：保存物を再検査し、状態を導出する。

今回の試験は実際のClaude、認証、管理者配置、外部networkを使わない。Claude processの代わりに、起動記録、
未加工応答、道具使用一覧、変更済み合成worktreeをfixtureとして渡す。Gitと固定試験commandだけは製品側の
機械処理が配列引数で実行する想定にする。

## 3. 必須受入試験

一つの試験fileへ、重複を避けて次を実装する。

1. 正常系：`prepare`→試験ターンRED→試験指紋固定→実装ターンGREEN→変更一覧→`ready_for_review`。
2. 開始前停止：未承認、対象SHA不一致、`ready_for_executor`でない、古い入力、使用済み承認では、worktreeと
   Claude起動記録を作らない。
3. 能力設定：Claude用起動情報の道具は`Read,Glob,Grep,Edit,Write`だけで、`Bash`、Web、MCP、agent、hook、
   plugin、skill、Chrome、背景実行、fallbackを含まない。権限方式は`dontAsk`、空MCP、safe modeとする。
4. 変更境界：試験ターンは指定試験pathだけ、実装ターンはproduction pathだけを許す。symlink、未追跡の
   余剰file、主作業ツリー変更、試験指紋変更を拒否する。
5. 機械試験：固定command以外、文字列shell、Claude報告だけのRED／GREEN判定を拒否する。終了コードが
   第1ターンで非0、第2ターンで0の場合だけ進む。
6. 保存：起動記録、未加工応答、道具使用、試験結果、変更一覧を上書きせず保存し、欠落・余剰・改竄を
   `status`で拒否する。
7. 後続境界：ClaudeへGit操作をさせず、機械commit前後を区別し、独立レビューとHuman段完了承認なしに
   完了状態へ進まない。
8. 確認運転境界：ReviewCompass3の実repositoryをproof対象にする設定、秘密・利用者情報を含む材料、
   無工具疎通承認の流用を開始前に拒否する。
9. 要求対応：25要求すべてを少なくとも1試験へ対応付け、対応先の試験関数が実在することを機械確認する。

## 4. 試験作成規則

- 既存製品code、既存試験、文書、record、設定を変更しない。
- 試験内の補助関数で合成repository、承認、設定、偽のターン結果を決定的に作る。
- 実Claudeや外部commandは絶対に起動しない。試験自身が使うGitは配列引数の`subprocess.run`だけとする。
- 期待する停止理由と、停止前に作られてはならない成果物を確認する。
- 同じ欠陥の表現違いを大量に列挙せず、各境界の代表例へ絞る。
- 実装moduleが存在しないため失敗することを、対象試験file単独の終了コードで確認する。
- collection（試験収集）は終了0、対象試験実行は終了1でなければ停止する。
- 新規試験を除く既存全試験を一度実行し、既知の無関係な古い範囲guardだけを明示除外して終了0を確認する。
- 作業完了時に変更path、試験件数、単独終了コード、代表失敗理由、既存試験結果を報告し、コミットしない。

## 5. 停止条件

- 固定入力のSHA-256不一致、要求集合不一致、変更可能path外の差分。
- 製品側を変えなければ失敗しない試験、実Claude起動、外部送信。
- 既存試験の不合格が今回の新規試験と無関係であることを確認できない。
- 既存試験またはscopeの修正が必要になった場合。
