# 無工具Claude疎通 過剰監視訂正 GREEN Evidence v1

- 日付：2026-08-11
- 範囲：`records/development/2026-08-11-claude-bootstrap-review-repair-scope-v2.md`
- RED commit：`376ee7dc6b0b3db8ebfc4957ea82935fb8c360c9`
- 変更production：`tools/development/claude_bootstrap.py`
- production SHA-256：`cda8ba1dcb6a4a648d680af1724e56825de3e2031744ead82f954fe098791cce`

## 訂正結果

- レビュー対象commit以後の全変更pathを列挙する処理を削除した。
- 変更pathを完了レビュー記録と送信承認記録の2件だけに限定する処理を削除した。
- Git履歴上の祖先判定と、過去commitからの送信目録再読込を削除した。
- 完了レビュー記録のGit記録、識別子、SHA-256、`verified`状態、対象commit、blocking所見0件、
  現在の固定送信目録との一致は維持した。
- 固定外の秘密値を除外する環境変数許可一覧は維持した。

## 試験結果

- 正規レビュー計画追加の正常系：終了0、1件合格。
- 固定4試験file：終了0、35件合格。
- 既存Pilot・egress試験：終了1、184件合格、既知の旧v6範囲試験1件不合格。
- 公式全試験：終了1、1604件合格、既知の旧v6範囲試験1件不合格。
- `git diff --check`：終了0。

既知の不合格は
`tests/test_pilot_collaboration_entrypoints.py::test_change_scope_contains_only_v6_allowlisted_paths`であり、
本訂正では変更していない。

## 未実施

Claude Code CLIの起動、認証、通信、payload送信、実Run、旧v6範囲試験の修正は行っていない。
