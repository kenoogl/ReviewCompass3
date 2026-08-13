# 第3段 処理呼出し目録の役割再評価 軽量作業票 v1

- 作成日：2026-08-13
- 基準commit：`43167fb`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 危険度案：低
- 作業担当：操縦役
- 完了レビュー担当：新規サブエージェント一者
- 外部モデル確認：行わない。第3段完了前の一回を残す

## 1. 目的

G04に残る処理呼出し目録の生成コード、基準資料、固定試験について、現在の利用者と正本との接続を再確認し、
現在保証、履歴資料、両方、役割終了のどれに当たるかを判定する。呼出し元がないことだけで不要と判断せず、
正規入口、現行の受入条件、過去に現在比較を外した経緯を合わせて確認する。

## 2. 入力と根拠

- `tools/development/process_call_inventory.py`
- `records/development/2026-08-11-claude-bootstrap-manifests/process-call-baseline-v1.json`
- `tests/test_claude_bootstrap_entrypoints.py::test_process_inventory_baseline_matches_fixed_commit`
- `records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v3.md`
- `docs/development/prompts/claude-bootstrap-run.md`
- `records/development/2026-08-12-stage2-official-test-entry-restoration-evidence-v1.md`
- `records/development/2026-08-12-stage2-official-test-entry-restoration-completion-review-v1.md`
- `records/development/2026-08-13-stage3-g04-role-classification-evidence-v2.md`

履歴上の主要commitは、RED固定`8cdac45`、実装`d58ac5f`、現在比較の除去`354c57e`とする。

## 3. 作業範囲と対象外

次を読み取りと機械照合だけで行う。

- Pythonコード、設定、案内、正本、試験、記録から、三対象の現在参照を列挙する。
- 三commitの差分と当時のEvidenceを読み、作成目的と現在比較を外した理由を確認する。
- 現在の目録生成と比較処理を、リポジトリを書き換えない形で実行し、保証範囲を確認する。
- 維持、試験だけ整理、コードと試験を同じ単位で整理の三案を比較する。

コード、試験、設定、基準JSON、正本、案内、TODOは変更しない。削除、統合、新しい検査器・試験・台帳・入口、
全試験、外部送信、Claude確認、第3段完了判断は対象外とする。

## 4. 期待する成果

一件の再評価Evidenceに、現在参照、正本との関係、履歴、実測した保証範囲、四分類、三案比較、利用者が判断する
必要がある点、未実施をまとめる。削除案が現在の正本変更を要する場合は、削除可能と断定せず停止条件として示す。

## 5. 機械で確認する事実と正規入口

- `rg`とPython構文木でimport、関数呼出し、文字列参照を列挙する。
- `git show`、`git diff`、`git log`で三commitと現在の差を確認する。
- 現在の対象試験は単独で実行し、終了コードを確認する。
- `generate_process_call_inventory`と`compare_process_call_inventories`を読取り専用で実行し、現在入力に対する結果を確認する。
- 成果物はSHA-256、再読込み、参照照合、`git diff --check`で確認する。

## 6. レビューで判断する事項

- 通常の呼出し元がないことと、現行正本が受入条件として参照することを両方扱っているか。
- 過去の一作業だけの現在差分検査と、現在も意味を持つ保証を分けているか。
- 基準再生成試験を恒久とした2026年8月12日の判断が、現在も有効かを再検討しているか。
- 三案比較が本質から外れた新機構や過剰な修正を含まないか。
- 利用者の意味判断が必要な変更を、技術的な削除候補として先取りしていないか。

## 7. 停止条件と完了条件

停止条件：

- 現行正本、現在安全、外部送信境界に影響する変更が必要になる。
- コード、試験、設定、基準資料、案内、TODOの変更が必要になる。
- 対象外の欠陥修正、別群調査、新しい検査機構へ連鎖する。

完了条件：

- 三対象の現在参照と履歴が機械照合される。
- 現在の生成・比較処理と対象試験の実測結果が記録される。
- 四分類と三案比較が根拠付きで示される。
- 一回の独立完了レビューが結果を確認する。
- 実施や意味変更は利用者判断へ分離される。
