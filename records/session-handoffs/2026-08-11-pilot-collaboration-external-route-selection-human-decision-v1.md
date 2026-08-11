# 操縦者別連携 外部実行経路 選択Human裁定 v1

- 日付：2026-08-11
- 裁定者：Human
- 裁定文言：`候補1`
- 裁定文言の出典：本作業の会話
- 選択対象：外部実行経路の接続
- 裁定：`select_external_execution_route`

## 1. 選択の意味

第1機械処理縦切りの次作業として、Codex主担当からClaude Codeを安全に起動し、送信前検査、Human承認、
未加工結果保存、失敗時停止を通る外部実行経路の接続を選ぶ。

この選択は、範囲設計と事前確認の開始を認める。次は別の承認とする。

- Claudeへの実payload送信。
- Claude Codeの認証操作。
- repository内容の送信。
- Claudeへファイル読書き、command実行、外部機能などの道具を許可すること。
- 凍結中の既存出口関門を変更すること。

## 2. 現在の実測

- Claude Code version：`2.1.220`
- Claude Code実行file SHA-256：`8addc857f3fe64d5a0368af9ee50321b50afb4a6918ba3ef018ab84f5dbbe081`
- API認証・接続先上書き環境変数を除外した認証状態：`loggedIn: false`、`authMethod: none`、
  `apiProvider: firstParty`、認証確認command終了コード1
- Claudeへのprompt送信とsession生成：未実施
- repository変更：本裁定recordとTODO更新以外は未実施

## 3. 先行範囲の扱い

先行する外部送信範囲v1は独立レビューで`reported_unverified`となり、次の4点が未解消である。

1. 新しい送信用途と凍結中の出口関門を変更するauthorityが未確定。
2. 単一の送信前検査、伏字化信号、復旧手順、材料方針、内容指紋付き目録の条件が不足。
3. 汎用command実行経路を含む迂回検査の定義が不十分。
4. repository外の状態を差し替えると同じ承認を再利用できる一回性の欠陥。

したがって先行範囲v1を実装根拠にせず、次versionで解消する。

## 4. 次のHuman選択

外部実行経路には次の二段階がある。権限と送信内容が異なるため、一つの承認へまとめない。

1. 無工具の疎通確認：固定した非機密payloadだけを送り、Claudeの全道具を無効にしてsession継続を確認する。
2. 実装委譲経路：コミット済み依頼を渡し、限定したrepository読書きとtest実行をClaudeへ許可する。

安全境界を先に確立するため、1を先に行うことを推奨する。いずれの場合も、現在の未認証状態を解消し、
送信対象と権限へ束縛したHuman承認を得るまで外部processを起動しない。
