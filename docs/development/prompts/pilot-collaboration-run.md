# Pilot collaboration run

実装指示の正本は
`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md`
である。LLMと機械処理の分担、`prompt_payload_bytes`、外部送信、Human承認を含む規則は正本を参照し、
この入口には複製しない。

共通コマンドの場所は次のとおり。

- `reviewcompass3-pilot prepare`
- `reviewcompass3-pilot ingest`
- `reviewcompass3-pilot status`

## Claude実装委譲

`pilot: codex`でClaudeを実装担当にする場合は、次の共通入口を使う。

- `reviewcompass3-claude-implementation prepare`
- `reviewcompass3-claude-implementation record-turn`
- `reviewcompass3-claude-implementation status`

各コマンドは、現在の作業ディレクトリを対象リポジトリとして扱う。パスには絶対パスを渡す。

準備は次の形で行う。

```text
reviewcompass3-claude-implementation prepare \
  --config <開始設定の絶対パス> \
  --private-root <保護された保存場所の絶対パス>
```

準備は、一時作業ツリーと固定された起動依頼を作るだけである。Claudeを起動せず、外部へ送信しない。
Claudeの起動と送信には、対象、モデル、起動依頼、材料、期限へ結び付いた別のHuman承認が必要である。

Claudeの一回の処理が終わった後、機械処理が起動記録と未加工応答を取り込む。

```text
reviewcompass3-claude-implementation record-turn \
  --private-root <保護された保存場所の絶対パス> \
  --run-id <実行識別子> \
  --turn <testまたはimplementation> \
  --launch <起動記録の絶対パス> \
  --raw <未加工応答の絶対パス>
```

管理者が配置した信頼済み入口を使う場合、結果取込みは次の形に固定する。

```text
trusted-review-send claude-implementation-record \
  --workspace-root <ReviewCompass3作業場所の絶対パス> \
  --repository <対象リポジトリの絶対パス> \
  --private-root <保護された保存場所の絶対パス> \
  --run-id <実行識別子> \
  --turn <testまたはimplementation> \
  --launch-record <起動記録の絶対パス> \
  --raw-file <未加工応答の絶対パス>
```

信頼済み入口も、保存済み結果を中核の取込み処理へ渡すだけである。Claudeを起動せず、外部へ送信せず、
失敗時に別モデル、別認証、別経路へ切り替えず、同じ処理を自動再試行しない。

現在状態は次の形で確認する。

```text
reviewcompass3-claude-implementation status \
  --private-root <保護された保存場所の絶対パス> \
  --run-id <実行識別子>
```

三つの共通コマンドは、標準出力へJSONを一行だけ返す。終了コードは、成功が`0`、予期しない内部失敗が
`1`、入力不備または安全境界による停止が`2`である。Claudeの報告だけで試験結果や完了を決めず、
中核処理が固定試験、変更範囲、保存物を機械確認する。`ready_for_review`は独立レビュー待ちを意味し、
Humanの段完了承認までは完了ではない。

固定二payloadによる無工具Claude疎通は、用途を限定した
`docs/development/prompts/claude-bootstrap-run.md`を入口とする。

レビューの対象、確認項目、担当数、最大周回数を機械生成する場合は、
`docs/development/prompts/review-plan-run.md`を入口とする。
