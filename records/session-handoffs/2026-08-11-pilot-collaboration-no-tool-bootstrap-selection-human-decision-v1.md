# 操縦者別連携 無工具疎通確認 選択Human裁定 v1

- 日付：2026-08-11
- 裁定者：Human
- 裁定文言：`無工具の疎通から`
- 裁定文言の出典：本作業の会話
- 先行裁定：`records/session-handoffs/2026-08-11-pilot-collaboration-external-route-selection-human-decision-v1.md`
- 裁定：`select_no_tool_claude_bootstrap_scope`

## 1. 選択した段階

外部実行経路の最初の段階には、固定した非機密の文だけをClaude Codeへ渡す無工具の疎通確認を選ぶ。
Claudeへrepositoryの読取り、file変更、command実行、MCP、plugin、hook、別agent起動を許可しない。

この段階では、次の二往復だけを対象とする。

1. 新しいClaude sessionを開始し、固定JSONを返せることを確認する。
2. 同じsessionを再開し、最初のnonceを保持していることを確認する。

実装委譲に必要なrepositoryの発見性と限定道具は、無工具の経路が成立した後の別段階とする。無工具の
疎通確認では、repository外の空directoryをClaudeの作業directoryに使い、物理的にもrepositoryを
発見しにくくする。この限定は後続の実装委譲方式へ一般化しない。

## 2. 本裁定が認める範囲

本裁定は、先行範囲レビューのF1〜F4を解消した範囲固定v2の作成、機械検証、独立範囲レビュー依頼までを
認める。新用途名は`claude_session_bootstrap`とする。

凍結している`tools/egress/`は変更せず、用途の異なる既存の出口機構を転用しない。既存機構が持つ安全条件は、
新用途へ必要な条件としてv2に明示して採否をHumanが確認できる形にする。

## 3. 本裁定が認めない範囲

次は別のHuman承認を要する。

- `high` riskのREDテスト作成と実装開始。
- Claude Codeの認証操作。
- Claude Codeのprocess起動とAnthropicへの実payload送信。
- repository内容、利用者情報、秘密情報、API keyの送信。
- Claudeの道具、MCP、plugin、hook、Chrome連携、別agent起動の有効化。
- 凍結している`tools/egress/`の変更。
- 実装委譲経路、任意prompt、任意model、他providerへの拡張。

実送信の承認は、送信する二つの文面、順序、送信先、model、期限、Claude実行fileの指紋、未消費の
一回限り承認へ束縛し、実装完了レビューが`verified`となった後に別途取得する。

## 4. 現在の停止状態

【記録】認証情報と接続先上書き環境変数を除外した直近の認証状態は`loggedIn: false`、
`authMethod: none`、`apiProvider: firstParty`である。

【実測】本裁定record作成までにClaudeへのprompt送信、Claude session生成、認証操作、外部process起動、
repository内容の送信は行っていない。

したがって、範囲固定v2の作成とレビューより後へは進まず、認証状態を理由に別の認証方式やAPI keyへ
自動で切り替えない。
