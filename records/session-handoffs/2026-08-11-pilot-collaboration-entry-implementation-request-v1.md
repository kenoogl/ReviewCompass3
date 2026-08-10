# 操縦者別連携の共通入口・指示文品質関門 最小実装依頼 v1

- 日付：2026-08-11
- 方式：`pilot_specific_claude_codex`
- 操縦者：Codex主担当
- 実装担当：Codex実装用サブエージェント
- 実装側モデル：`gpt-5.6-sol`
- 指示文監査・判定・実装後レビュー側モデル：`gpt-5.6-terra`
- 危険度：`high`
- Human指示：本作業の会話における「OK。進めて」
- 開始時HEAD：`4dcb0bc5c964b537eac0332794a3f84aec90f037`
- 対象コミット：本依頼を含むコミットを起動時に機械取得して固定する
- 上流：`docs/development/pilot-specific-claude-codex-collaboration.md`
- 共通レビュー入口：`docs/development/work-review-protocol.md`
- 開発方針：`docs/development/2026-08-02-development-policy.md`

## 1. 一作業の目的

`pilot: codex`の最初の運用可能な縦切りとして、コミット済みの開始設定を受け取り、指示文の事前機械検査、
指示文監査と指示文判定の未加工結果保存、厳格解析、段階状態の導出までを、一つの共通コマンド入口へ接続する。

指示文監査と指示文判定の実際の意味判断はLLMが行う。入力固定、起動記録照合、保存、解析、全件照合、
状態導出、ファイル操作は機械処理とする。本実装ではLLMを実際に起動せず、外部で得た模擬結果を取り込む
境界までを作る。

group C・Dは保留を継続し、本作業へ含めない。

## 2. 受入条件

### `AC-PC-001` 共通入口

`pyproject.toml`に一つのコマンド入口`reviewcompass3-pilot`を公開する。Codex用`AGENTS.md`とClaude用
`CLAUDE.md`は、同じ共通手順`docs/development/prompts/pilot-collaboration-run.md`をそれぞれ一回だけ参照する。
入口文書へ処理規則を複製せず、正本とコマンドの場所だけを案内する。

### `AC-PC-002` 開始設定と事前機械検査

版付きJSON開始設定を厳密に読み、未知項目、欠落、型違い、重複した要求識別子、未知の接頭辞、モデル対応違反、
Gitコミット不在、指示書または材料の不在・SHA-256不一致を拒否する。要求識別子は`AC-`、`NG-`、`ST-`、
`OUT-`の固定集合とし、指示書内の参照集合と一致させる。

開始設定は少なくとも、実行識別子、方式、操縦者、実装担当、操縦側モデル、レビュー側モデル、指示文品質側
モデル、固定コミット、指示書、固定材料、固定材料の出自、要求識別子集合、結果契約版を持つ。固定材料の
出自は`machine_derived`または`judgment_selected`とし、出自に応じた再現コマンドまたは選定者・選定基準・
件数を検査する。

### `AC-PC-003` 決定的な準備処理

`prepare`は、同じ固定入力から同じ実行manifest、指示文封筒、最初の段階eventを生成する。実行directoryは
Git管理範囲外の明示private root直下に排他的に作成し、既存実行を上書きしない。指示文封筒は発見力モードを
使い、固定指示文本文と材料のpath・SHA-256・出自を持つが、参照範囲を閉包したとは主張しない。

### `AC-PC-004` 未加工結果と起動記録の不変保存

`ingest`は、`prompt_audit`と`prompt_judgment`の未加工結果を解析前に保存する。起動記録には実行識別子、
終了状態、実行コマンド配列、`material_mode: discovery`、参照pathの抽出可能件数、抽出不能件数、重複除外件数を
持たせる。未加工結果と起動記録は内容のSHA-256で結び、一度保存した試行識別子を上書きしない。

既存`tools/bootstrap/raw_review_store.py`と保存処理を二重実装しない。安全な相対path、排他的作成、正規JSON、
再読込を行う共通の不変保存境界を抽出し、既存review保存と新しいagent結果保存の双方から再利用する。既存の
公開データ型と既存テストの互換性を保つ。

### `AC-PC-005` 指示文監査結果の厳格解析

指示文監査結果はJSON一文書とし、版、状態、所見、要求識別子ごとの確認結果だけを受け付ける。各所見は
固定識別子、分類、重大度、影響する要求識別子、根拠を持つ。所見識別子と要求結果は重複を禁止し、要求結果は
開始設定の全要求識別子を一回ずつ被覆する。未知項目、未知参照、欠落、解析不能を合格へ進めない。

### `AC-PC-006` 指示文判定結果の厳格解析

指示文判定結果はJSON一文書とし、版、状態、監査結果SHA-256、所見ごとの推奨だけを受け付ける。推奨は
`accept`、`reject`、`hold`のいずれかで、監査所見の全識別子を一回ずつ被覆し、理由を持つ。判定担当は
最終採否を決めない。監査結果SHA-256不一致、欠落、重複、未知所見を拒否する。

### `AC-PC-007` 段階状態の機械導出

段階eventは追記専用とし、手編集する現在状態ファイルを作らない。`status`はmanifest、event、不変結果、
解析結果を再読込して現在状態を導出する。準備後は`ready_for_prompt_audit`、監査合格後は
`ready_for_prompt_judgment`、判定完了時に所見があれば`human_decision_required`、所見がなければ
`ready_for_executor`とする。解析不能、改竄、段階飛ばしは`blocked`として成功へ昇格させない。

### `AC-PC-008` コマンドと終了コード

最低限、`prepare`、`ingest`、`status`を提供する。成功は終了コード0、入力不備または安全停止は終了コード2、
予期しない内部失敗は終了コード1とし、標準出力へ一つのJSON結果を出す。シェル文字列を組み立てず、Git確認は
引数配列で実行する。

### `AC-PC-009` 既存機能の非回帰

既存のbootstrap reviewの公開データ型、保存形式、コマンド、テストを壊さない。既存
`reviewcompass3-bootstrap-review`は置き換えず、今回の共通入口と役割を混同しない。

## 3. 禁止事項

- `NG-PC-001` 外部送信、Claude CLI、Codex CLI、Codexサブエージェントを実装コードから起動しない。
- `NG-PC-002` Human所見裁定、実装実行、実装後レビュー、再実装、完了反映を本縦切りへ含めない。
- `NG-PC-003` 未加工結果を解析前に捨てない。解析失敗を成功へ変換しない。
- `NG-PC-004` 段階状態、SHA-256、件数、参照集合をLLMの報告から手転記しない。
- `NG-PC-005` 既存の閉包型`review_pipeline`を発見力モードへ黙って読み替えない。
- `NG-PC-006` `.reviewcompass/workflow/`配下へ新しい台帳を手書きしない。
- `NG-PC-007` 関係のない整形、既存Python全体のインデント変更、既存テストの書換えを行わない。

## 4. 停止条件

- `ST-PC-001` 受入条件を満たすために本依頼外の設計変更、製品schema変更、既存テスト変更が必要になった。
- `ST-PC-002` 共通不変保存境界への抽出が既存保存形式の互換性を壊す。
- `ST-PC-003` private root、Git範囲、symlink、path traversalを安全に区別できない。
- `ST-PC-004` 指示文監査または判定の固定結果形式に意味上の不足が見つかった。
- `ST-PC-005` 同じ種類の実装失敗が二回続き、前提または作業分割の見直しが必要になった。

停止条件に達した場合はコードを広げず、事象、根拠、未実施範囲を主担当へ返す。

## 5. 出力要件

- `OUT-PC-001` 実装前に新規受入テストを作り、対象機能が無いため失敗することを単独コマンドで確認する。
- `OUT-PC-002` 実装中は、要求の誤りが判明しない限り固定した受入テストを変更しない。
- `OUT-PC-003` 正常例、負例、境界例に加え、SHA-256改竄、未加工結果上書き、要求被覆欠落、所見全件照合欠落、
  段階飛ばし、private root誤配置を故障注入で検出する。
- `OUT-PC-004` 実装後に対象テスト、既存bootstrap reviewテスト、公式全テスト、`git diff --check`をそれぞれ
  単独コマンドで実行し、終了コードを報告する。
- `OUT-PC-005` 実装結果は変更path、要求識別子ごとの根拠、実行コマンドと終了コード、未解決事項を含む。
- `OUT-PC-006` 実装担当は意味的に完結した変更をコミットして停止する。push、履歴書換え、外部送信は行わない。

## 6. 変更可能範囲

- `tools/development/pilot_collaboration.py`（新規）
- `tools/development/pilot_collaboration_cli.py`（新規）
- `tools/bootstrap/immutable_result_store.py`（新規）
- `tools/bootstrap/raw_review_store.py`（共通保存境界への接続だけ）
- `tests/test_pilot_collaboration.py`（新規）
- `tests/test_pilot_collaboration_cli.py`（新規）
- `tests/test_bootstrap_immutable_result_store.py`（新規）
- `docs/development/prompts/pilot-collaboration-run.md`（新規）
- `tests/test_pilot_collaboration_entrypoints.py`（新規）
- `AGENTS.md`（共通入口への参照一行だけ）
- `CLAUDE.md`（共通入口への参照一行だけ）
- `pyproject.toml`（コマンド入口一件だけ）

変更可能範囲を広げる必要がある場合は`ST-PC-001`として停止する。

## 7. テストと実装の順序

1. 新規テストだけを作り、対象機能不在による失敗を確認する。
2. テストの期待が本依頼と一致することを確認する。
3. 実装を進め、固定したテストを合格させる。
4. 既存保存テストと既存reviewテストを合格させる。
5. 故障注入、実リポジトリを使う確認運転、公式全テストを行う。
6. 実装結果をコミットし、主担当へ返す。

本実装が合格しても、`mechanical_assurance_status`を直ちに`connected`へ変更しない。外部実行経路への接続、
実運用での一連の確認、独立レビュー、Human段完了承認は後続境界である。
