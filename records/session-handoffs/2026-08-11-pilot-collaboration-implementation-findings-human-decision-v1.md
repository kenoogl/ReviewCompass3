# 操縦者別連携 production実装所見 Human裁定 v1

- 日付：2026-08-11
- 裁定者：Human
- 裁定文言：`IR-PC-001〜004を全件採用する`
- 裁定文言の出典：本作業の会話
- 対象所見：`IR-PC-001`、`IR-PC-002`、`IR-PC-003`、`IR-PC-004`
- 対象レビュー：`records/session-handoffs/2026-08-11-pilot-collaboration-implementation-review-v1.md`
- 対象レビューSHA-256：`ddb97a5f8a28f10533ebf025f4b359985a90dc593a4250ca7bdfe006ea20cd2e`
- 対象実装commit：`0974769d2ce91210dfb62a7a9a6179fd98e7f614`
- 裁定：`accept_all_for_reimplementation`

## 裁定内容

4件を一つの再実装単位として扱い、次を行う。

1. 親directoryのsymlinkを経由したrepository内private rootを拒否する。
2. `launch/`、`raw/`、`parsed/`の孤児・余剰・参照欠落を`status`で拒否する。
3. current sourceの差異と保存物不整合が同時にある場合、`stale_input`を優先する。
4. CLIが把握済みのrun IDを安全停止応答へ保持する。

production修正前に4件の反証testを追加して失敗を確認し、そのtestを固定したまま実装を修正する。修正後は
固定済み73件を含む対象test、既存bootstrap review test、公式全test、差分検査を再実行し、別の新しい
会話状態による独立再レビューを行う。外部CLI起動と外部送信は行わない。
