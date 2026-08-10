# Codex PilotによるClaudeセッション確立・停止Evidence v1

- 日付：2026-08-11
- work item：`codex-pilot-claude-session-bootstrap`
- 範囲固定：
  `records/session-handoffs/2026-08-11-codex-pilot-claude-session-bootstrap-scope-v1.md`
- 範囲固定commit：`531432b9e8c2493abef4c530368882c37707226e`
- verdict：`blocked`

## 1. 実施

【実測】公式installerを`https://claude.ai/install.sh`から取得し、SHA-256
`cde4f1702d3b1695f92b73d26888364e17bca476e17f0fd676484c951d36c125`の内容を確認してから
Claude Code安定版を導入した。

【実測】導入結果はversion `2.1.220`、配置先は`/Users/keno/.local/bin/claude`である。

【実測】`ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、
`CLAUDE_CODE_OAUTH_TOKEN`を子processの環境から除外してClaude契約プランへログインした。
通常環境での`claude auth status`は次の3条件を満たした。

```json
{
  "loggedIn": true,
  "authMethod": "claude.ai",
  "apiProvider": "firstParty"
}
```

【記録】Humanは、ReviewCompass3の承認済み送信経路を通さず、Claude Code CLIから
AnthropicのFableへ、範囲固定§4の非機密payload 2件だけを送ることを明示承認した。
同時に、repository内容とAPIキーを送らず、Claudeの全toolを無効にする条件を固定した。

## 2. 結果

【実測】1回目payloadの送信commandは2回試みたが、どちらもClaude Codeを起動する前の
安全審査で拒否された。

1. 初回：承認済み`trusted-review-send`経路外から、未登録の外部宛先・modelへ送る操作として拒否。
2. Humanの具体的な再承認後：再承認を認識したうえで、同経路外の送信は安全方針上の
   明示拒否に該当するとして再度拒否。

【実測】拒否は`CreateProcess`前に発生しており、Claude Codeのprocessは開始されていない。
したがって、§4のpayload、repository内容、APIキーのいずれもClaudeへ送信されていない。

【実測】予定したsession ID
`394745ba-c4c1-42f4-8752-bf48c692a732`およびnonce
`RC3-CPC-20260811-A`を`/Users/keno/.claude/projects`配下から検索した結果は0件、
`rg`のexit codeは`1`であった。Claude側のsession transcriptは生成されていない。

## 3. 判断

【判断】範囲固定§6の受入条件は満たしていない。CodexをPilotとするClaudeセッションは
確立していないため、verdictは`blocked`とする。

【記録】現行の`tools/egress/sender.py`は段階1の関門だけを実装し、関門合格後も
`EgressSendingNotApproved`で必ず停止する。実送信は段階4として別のHuman承認を必要とする。
このため、現在のrepositoryに本payloadを実送信できる承認済み経路はない。

## 4. 手戻り

- 対象操作：Codex PilotからClaude Reviewerへの最初の非機密payload送信
- 期待executor：Claude Code CLI `2.1.220`
- 実executor：起動前の安全審査。Claude Codeは未起動
- 手作業理由：なし。Human中継への切替や別経路の迂回は行っていない
- 事象とEvidence：本record §2、2回の`CreateProcess`拒否、session検索0件
- 機械処理候補：Claude CLIを承認済み送信経路として登録するか、実送信を持つ関門の段階4を
  独立作業として設計・承認する
- route：Human判断待ち

## 5. 未実施

- Claudeへの1回目payload送信
- 同じClaude sessionの再開
- Claude応答JSONの機械照合
- Codex PilotとClaude Reviewerの対話成立
- 既存authorityの改定
- 実作業のClaude委譲

安全審査が明示した禁止に従い、同じcommandの再試行、別のshell経路、Claude Desktop、
API、Human中継による迂回は実施しない。
