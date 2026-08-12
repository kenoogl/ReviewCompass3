# Claude実装委譲経路 合成リポジトリ確認運転 指示書 v1

- 状態：`prepared_not_approved`
- 日付：2026-08-12
- 用途：`claude_implementation_executor_confirmation`
- 操縦者：Codex
- 実装担当：Claude
- 要求モデル：`claude-fable-5`
- 許容実応答モデル：`claude-fable-5`、`claude-opus-5`、`claude-opus-4-8`
- 実送信承認：未取得
- 実Claude起動：未実施

根拠とする範囲は
`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v3.md`、SHA-256
`063d4299e78c11c2060b012ff7f09d7feaa2eca318e879e35bd418a7015e689f`である。
モデル名と許容集合はHumanが指定したFable 5の選択を使うが、無工具疎通の承認、用途、payloadは流用しない。
本確認運転には、別の一回限り送信承認を必要とする。

## 1. 目的

ReviewCompass3本体とは別の、機密を含まない小さな合成Gitリポジトリで、次の一連の処理を確認する。

1. Codexが固定済みの作業を準備する。
2. 同じClaudeセッションの第1ターンで、Claudeが受入試験だけを作る。
3. 機械処理が試験を実行し、意図した不合格を確認して試験の指紋を固定する。
4. 第2ターンで、Claudeが製品コードだけを実装する。
5. 機械処理が同じ試験を実行し、合格、変更範囲、保存物を確認する。
6. Codexの別モデルが独立レビューできる状態で停止する。

本確認運転は、ReviewCompass3本体をClaudeへ読ませない。実運用、段完了、管理者配置、外部送信の一般承認を
目的としない。

## 2. 合成リポジトリ

実行時に新しく作る一時リポジトリは、最初のコミットに次の3ファイルだけを持つ。

### `README.md`

```text
Synthetic repository for the ReviewCompass3 Claude delegation confirmation.
```

### `instructions/implementation.md`

```text
Create a deterministic function named double.
The function accepts one number and returns that number multiplied by two.
```

### `materials/requirements.md`

```text
double(4) must return 8.
The implementation must not read files, environment variables, network resources, or time.
```

初期コミットに`tests/test_feature.py`と`src/feature.py`を含めない。実行時に作るリポジトリ、作業ツリー、
保存場所は、いずれもReviewCompass3本体の外に置く。

## 3. Claudeへ渡す文章

### 第1ターン：受入試験

次の文章だけを、合成リポジトリを作業場所とするClaudeへ渡す。

```text
このリポジトリは機密を含まない確認運転用の合成リポジトリです。
instructions/implementation.mdとmaterials/requirements.mdを読み、要求を確認してください。

このターンではtests/test_feature.pyだけを新規作成してください。
src/feature.pyを含む他のファイルは変更しないでください。
試験はsrc.featureのdoubleを読み込み、double(4)が8になることを確認してください。

コマンドを実行せず、ネットワークを使わず、Git操作をしないでください。
作業が終わったら、変更したパスだけを短く報告してください。
```

### 第2ターン：製品実装

第1ターンを機械処理が受理した場合だけ、同じClaudeセッションへ次の文章を渡す。

```text
機械処理が受入試験の不合格と試験ファイルの固定を確認しました。

このターンではsrc/feature.pyだけを新規作成し、instructions/implementation.mdと
materials/requirements.mdの要求を満たしてください。
tests/test_feature.pyを含む他のファイルは変更しないでください。

コマンドを実行せず、ネットワークを使わず、Git操作をしないでください。
作業が終わったら、変更したパスだけを短く報告してください。
```

Claudeの報告は合否根拠に使わない。変更パスと試験結果は機械処理が確認する。

## 4. 機械だけが使う固定条件

- Claudeへ見せる道具：`Read`、`Glob`、`Grep`、`Edit`、`Write`だけ。
- Claudeへ見せない機能：`Bash`、Web、MCP、別エージェント、フック、プラグイン、スキル、Chrome、
  背景実行。
- 権限方式：`dontAsk`。
- MCP設定：空。
- 自動再試行：なし。
- 別モデル、別認証、別経路、別送信先への自動切替：なし。
- 第1ターンの変更可能パス：`tests/test_feature.py`だけ。
- 第2ターンの変更可能パス：`src/feature.py`だけ。
- 固定試験コマンド：実行時に作るPython環境の絶対パスを先頭にした、
  `python -m pytest -q tests/test_feature.py`相当の配列引数。
- 試験実行者：ReviewCompass3の機械処理だけ。固定試験コマンドをClaudeへ渡さない。
- 第1ターンの期待終了コード：0以外。
- 第2ターンの期待終了コード：0。
- 独立レビュー担当：Codex主担当が`gpt-5.6-sol`の場合は`gpt-5.6-terra`。

要求モデルと許容実応答モデルは別に記録する。要求モデルがFable 5でも、実応答モデルが上記の閉じた許容集合
に含まれる場合は受理できる。許容集合外、空、または機械的に特定できない場合は停止する。

## 5. 開始前に固定する値

次の値を開始設定と一回限り承認へSHA-256で結び付ける。

- 合成リポジトリの基準コミット。
- 本指示書。
- 範囲固定v3の`AC-CD-001`〜`007`、`NG-CD-001`〜`007`、`ST-CD-001`〜`006`、
  `OUT-CD-001`〜`005`から成る25件の要求集合。
- `instructions/implementation.md`と`materials/requirements.md`。
- 要求集合。
- 第1ターンと第2ターンの文章。
- 変更可能パス。
- 固定試験コマンド。
- 能力設定。
- 要求モデルと許容実応答モデル。
- Claude Codeの版と実行ファイルの指紋。
- 認証が`claude.ai`かつ`firstParty`で、APIキー由来でないこと。
- 保存場所、期限、用途、実行回数1回。

一つでも不一致、古い状態、未承認、使用済みであれば、Claudeの処理を作る前に停止する。

## 6. 実行順序

1. 合成リポジトリと開始設定を機械的に作る。
2. `reviewcompass3-claude-implementation prepare`で一時作業ツリーと第1ターンの起動依頼を作る。
3. 別途固定した起動処理が、第1ターンの文章と起動依頼を使ってClaudeを1回だけ処理する。
4. 信頼済み入口が起動記録と未加工応答を第1ターンの取込み処理へ渡す。
5. 状態が`ready_for_implementation_turn`の場合だけ、第2ターンを同じセッションで1回処理する。
6. 信頼済み入口が第2ターンの起動記録と未加工応答を取込み処理へ渡す。
7. `reviewcompass3-claude-implementation status`で`ready_for_review`を確認する。
8. `gpt-5.6-terra`の別実行単位が、固定要求、差分、保存物、試験結果を独立レビューする。
9. 技術的合格後もHumanの段完了承認待ちで停止する。

同じ失敗処理を自動再試行しない。失敗後の再開には、新しい試行識別子とHuman判断を必要とする。

## 7. 合格条件

- 第1ターンでは`tests/test_feature.py`だけが追加され、機械試験が不合格になる。
- 第1ターン後の試験指紋が固定される。
- 第2ターンでは`src/feature.py`だけが追加され、試験ファイルが変わらない。
- 第2ターン後の同じ機械試験が合格する。
- 主作業ツリー、ReviewCompass3本体、管理者配置に変更がない。
- 禁止道具、禁止パス、秘密情報、利用者情報、余剰ファイルがない。
- 起動記録、未加工応答、道具使用、試験結果、変更一覧が上書きされず保存される。
- 実応答モデルが許容集合内で、要求モデルと分けて記録される。
- 状態は`ready_for_review`で止まり、独立レビューとHuman段完了承認を飛ばさない。

## 8. 現時点の停止事項

本指示書を作成・コミットしても、次は承認されない。

- Claudeの起動、認証操作、外部送信。
- 管理者領域への実配置。
- ReviewCompass3本体をClaudeへ見せること。
- 一回限り承認の発行または消費。
- 確認運転の成功、独立レビュー合格、段完了の宣言。

また、実際のClaude Codeを固定能力で起動し、その応答から中核処理が受け付ける起動記録と取込み用JSONを
作る処理は、現時点では未実装である。この起動・変換処理を試験先行で実装し、独立レビューに合格させた後、
本指示書と全入力へ結び付いた一回限りのHuman送信承認を別に得る必要がある。
