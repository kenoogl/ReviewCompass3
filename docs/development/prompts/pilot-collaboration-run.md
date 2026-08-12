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

合成リポジトリの確認運転では、Humanが承認候補のSHA-256を承認した後、次の一括入口を使う。

```text
reviewcompass3-claude-confirmation run-approved \
  --output-root <準備結果の保存場所の絶対パス> \
  --candidate-sha256 <承認済み候補のSHA-256>
```

この入口は、保存済み準備結果から対象リポジトリ、実行識別子、承認識別子、開始設定、モデル、送信文、
許可パスを読み取る。信頼済み入口の確認、承認票の有効化、第1ターン、機械検証、第2ターン、機械検証、
`ready_for_review`確認までを固定順で一度だけ行う。途中で停止した場合は第2ターンへ進まず、同じ外部処理を
自動再試行しない。送信後に応答解析だけが停止した場合は、改変されていない保存済み応答を外部送信なしで
再検証し、承認済みの残りターンだけを続行できる。操作者が各ターンの引数や承認票を手で組み立ててはならない。

未加工応答は全体を保存するが、通知名の完全一致を合否条件にしない。機械判定は、実際に有効だった道具・
外部接続・追加機能・権限方式、応答モデル、道具使用、権限拒否、自動再試行、最終結果、実ファイル差分、
試験結果という必要な証拠だけを使う。操作を伴わない未知の付随情報や警告は保存するが、停止理由にしない。

別の一回限りHuman送信承認tokenが用意された後だけ、管理者が配置した信頼済み入口から各ターンを起動する。

```text
trusted-review-send claude-implementation-execute \
  --workspace-root <ReviewCompass3作業場所の絶対パス> \
  --repository <対象リポジトリの絶対パス> \
  --private-root <保護された保存場所の絶対パス> \
  --run-id <実行識別子> \
  --turn <testまたはimplementation> \
  --approval-id <一回限りHuman送信承認の識別子>
```

tokenは開始設定全体のSHA-256、実行識別子、保存場所、期限へ結び付く。第1ターン開始時にclaimし、
第2ターン終了時または外部処理後の停止時にconsumeする。token不在・不一致・期限切れ・再利用では、
Claudeのprocessを作る前に停止する。

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

`claude-implementation-record`は保存済み結果を中核の取込み処理へ渡すだけであり、Claudeを起動しない。
`claude-implementation-execute`も、失敗時に別モデル、別認証、別経路へ切り替えず、同じ処理を自動再試行しない。

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
