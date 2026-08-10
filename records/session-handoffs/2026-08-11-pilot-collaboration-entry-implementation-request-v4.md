# 操縦者別連携の共通入口・指示文品質関門 最小実装依頼 v4

- 日付：2026-08-11
- 方式：`pilot_specific_claude_codex`
- 操縦者：Codex主担当
- 実装担当：Codex実装用サブエージェント
- 実装側モデル：`gpt-5.6-sol`
- 指示文監査・判定・実装後レビュー側モデル：`gpt-5.6-terra`
- 危険度：`high`
- Human開始指示：本作業の会話における「OK。進めて」
- Human所見裁定：`PA-PC-001〜006を全件採用する`
- Human統合裁定：`PA-PC-007を採用し、v2とv3を統合した単一v4指示書を作る`
- 開始時基準コミット：`4dcb0bc5c964b537eac0332794a3f84aec90f037`
- 対象コミット：本依頼を含むコミットを起動時に機械取得して固定する
- 旧依頼：`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v2.md`
- 旧追補：`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v3.md`
- Human統合裁定記録：`records/session-handoffs/2026-08-11-pilot-collaboration-pa-pc-007-human-decision-v1.md`
- 上流：`docs/development/pilot-specific-claude-codex-collaboration.md`
- 共通レビュー入口：`docs/development/work-review-protocol.md`
- 開発方針：`docs/development/2026-08-02-development-policy.md`

本書は旧依頼v2と旧追補v3を置き換える、自己完結した単一の実装依頼である。実装担当はv2とv3を指示として
併用せず、本書だけを実装指示の正本とする。v2、v3、品質確認記録、Human裁定は改訂理由の履歴としてだけ
参照する。開始設定の`instruction.path`と`instruction.sha256`は本書一件だけへ束縛する。

## 1. 一作業の目的

`pilot: codex`の最初の運用可能な縦切りとして、コミット済みの開始設定を受け取り、指示文の事前機械検査、
指示文監査と指示文判定の未加工結果保存、厳格解析、段階状態の導出までを、一つの共通コマンド入口へ接続する。

指示文監査と指示文判定の意味判断はLLMが行う。入力固定、Git照合、起動記録照合、保存、解析、全件照合、
状態導出、ファイル操作は機械処理とする。本実装ではLLMを実際に起動せず、模擬結果を取り込む境界までを作る。
group C・Dは保留を継続し、本作業へ含めない。

## 2. 共通の形式規則

本書で「完全形式」と記すJSON objectは、列挙したkeyをすべて一回ずつ持ち、それ以外のkeyを拒否する。
入れ子objectにも同じ規則を適用する。`integer`は真偽値を含まない整数、`text`は空でなくNULを含まない文字列、
`sha256`は小文字16進64文字とする。

識別子の形式は次で固定する。

- `run_id`、`attempt_id`、`execution_id`：`[a-z0-9][a-z0-9._-]*`
- 要求識別子：`(?:AC|NG|ST|OUT)-[A-Z0-9]+(?:-[A-Z0-9]+)*`
- 監査所見識別子：`PA-[A-Z0-9]+(?:-[A-Z0-9]+)*`
- Gitコミット：小文字16進40文字

正規JSON bytesは、Pythonの`json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)`を
UTF-8化したbytesとし、末尾改行を含めない。正規JSONのSHA-256はこのbytesから計算する。JSON fileへ保存する
場合だけ同じbytesへ改行1文字を加える。保存後に再読込し、書いたbytesと一致することを確認する。

配列は意味上の順序がない場合、保存前に固定識別子またはpathの昇順へ正規化する。入力の重複は正規化で
隠さず拒否する。

## 3. 受入条件

今回の要求集合は、受入条件9件、禁止事項7件、停止条件4件、出力要件6件の計26件とする。開始設定の
`requirement_ids`は、本書から抽出できるこの26件だけを一回ずつ持つ。それ以外の要求識別子を含む設定は
`requirement_mismatch`として拒否する。

### `AC-PC-001` 共通入口

`pyproject.toml`に一つのコマンド入口`reviewcompass3-pilot`を公開する。Codex用`AGENTS.md`とClaude用
`CLAUDE.md`は、同じ共通手順`docs/development/prompts/pilot-collaboration-run.md`をそれぞれ一回だけ参照する。
入口文書へ処理規則を複製せず、正本とコマンドの場所だけを案内する。

### `AC-PC-002` 開始設定の完全形式と事前機械検査

開始設定rootは次の19 keyを持つ。

| key | 型・許容値 |
| --- | --- |
| `schema_version` | integer `1` |
| `run_id` | 上記形式のtext |
| `collaboration_method` | `pilot_specific_claude_codex` |
| `request_kind` | 本縦切りでは`implementation`だけ |
| `pilot` | `codex`だけ |
| `implementer` | `claude`または`codex_implementation_subagent` |
| `pilot_model` | `gpt-5.6-sol`または`gpt-5.6-terra` |
| `reviewer_model` | `pilot_model`と反対側 |
| `instruction_quality_model` | `reviewer_model`と同値 |
| `source_commit` | Gitコミット形式 |
| `instruction` | 後述の完全形式object |
| `materials` | 後述の完全形式objectを1件以上持つarray |
| `fixed_input` | 後述の完全形式object |
| `requirement_ids` | 重複のない要求識別子array。4接頭辞を各1件以上含む |
| `result_contract_version` | `pilot-collaboration-prompt-quality-v1` |
| `instruction_quality_round` | 1以上のinteger |
| `instruction_quality_round_limit` | 1以上のinteger。round以上 |
| `implementation_review_round_limit` | 1以上のinteger |
| `mechanical_assurance_status` | 後述の完全形式object |

`instruction`は`path`と`sha256`の2 keyを持つ。`instruction.path`は本書のpath、`instruction.sha256`は
`source_commit`内にある本書blob bytesのSHA-256と一致しなければならない。`materials`の各要素も`path`と
`sha256`の2 keyを持ち、pathを重複させない。pathはrepository root基準の安全なPOSIX相対pathで、空、
絶対path、`.`、`..`、NULを拒否する。

`fixed_input`は次の7 keyを常に持つ。

| key | `machine_derived` | `judgment_selected` |
| --- | --- | --- |
| `origin` | `machine_derived` | `judgment_selected` |
| `count` | `materials`件数と同値 | `materials`件数と同値 |
| `derivation_argv` | 1件以上のtext array | `null` |
| `derivation_output_sha256` | sha256 | `null` |
| `selector` | `null` | text |
| `selection_basis` | `null` | text |
| `selected_paths_sha256` | materials pathを昇順に改行区切りしたUTF-8 bytesのsha256 | 同左 |

`mechanical_assurance_status`は、`instruction_preflight`、`stage_ledger`、`change_inventory`、
`raw_result_store`、`result_parser`、`reuse_guard`、`capability_preflight`の7 keyを持つ。本縦切りの開始設定では
すべて`specified_only`だけを受け付ける。`connected`への変更と能力の実在確認は後続作業へ明示的に移管する。

事前機械検査は、設定fileを解析するだけでなく次を検査する。

1. `source_commit`が現在repositoryのcommit objectである。
2. 指示書と全材料のpathが、`source_commit`のtree内にある通常blobである。
3. `git show <source_commit>:<path>`で得たblob bytesのSHA-256が設定値と一致する。
4. 現在のrepository内の同pathが通常fileでsymlinkではなく、現在bytesが固定blob bytesと一致する。
5. 指示書本文から抽出した要求識別子集合が`requirement_ids`集合と一致する。
6. private rootと設定fileの検査を含め、全検査が完了するまでrun directoryを書かない。

Git操作はshell文字列でなく引数arrayの`subprocess.run`を使う。終了コードと標準出力を直接判定し、pipeや
後段commandで合否を置き換えない。

### `AC-PC-003` 決定的な準備処理とfile配置

`prepare`は、同じ固定入力から同じ`manifest.json`、`prompt-audit-envelope.json`、最初の段階eventを生成する。
実行directoryは、既存する絶対private rootの直下`<private-root>/<run-id>/`へ排他的に作る。private rootは
repository root内、その親、symlinkのいずれも拒否する。候補directoryで全fileを書いて再読込した後、同じ
private root内で一回のrenameによりrun directoryを確定する。既存run IDを上書きしない。

run directoryの配置を次に固定する。

```text
<run-id>/
  manifest.json
  prompt-audit-envelope.json
  prompt-judgment-envelope.json       # 監査解析成功後だけ作成
  events/0001-prepared.json
  events/0002-prompt-audit-*.json      # ingest後だけ作成
  events/0003-prompt-judgment-*.json   # ingest後だけ作成
  launch/<attempt-id>.json
  raw/<attempt-id>.json
  parsed/<attempt-id>.json             # 解析成功時だけ作成
```

`manifest.json`は`schema_version`、`repository_root`、`config_raw_sha256`、`start_config`、
`manifest_sha256`の5 keyを持つ。`manifest_sha256`はそのkeyを除く4 keyの正規JSON SHA-256とする。
`repository_root`は実行時の絶対pathでありprivate保存だけに使い、Gitへ記録しない。

`prompt-audit-envelope.json`は`schema_version`、`result_kind`、`run_id`、`source_commit`、`instruction`、
`materials`、`fixed_input`、`requirement_ids`、`output_contract`、`envelope_sha256`の10 keyを持つ。
`result_kind`は`prompt_audit`、`instruction`は`path`、`sha256`、固定blobのUTF-8 `text`を持つ。
materialsはpathとsha256だけを持ち、本文を埋め込まない。`output_contract`は`pilot-prompt-audit-v1`とする。
`envelope_sha256`はそのkeyを除く9 keyの正規JSON SHA-256とする。これは発見力モードであり、参照範囲を
閉包したとは主張しない。

### `AC-PC-004` ingest入力、起動記録、未加工結果の不変保存

`ingest`は、絶対pathで指定されたUTF-8 raw fileと起動記録fileを読み、起動記録の検査後、意味上の解析より
先に両方を不変保存する。raw fileと起動記録は通常fileだけを受け付け、symlinkを拒否する。

起動記録は次の10 keyを持つ完全形式objectとする。

| key | 型・許容値 |
| --- | --- |
| `schema_version` | integer `1` |
| `execution_id` | 規定形式のtext |
| `run_id` | CLIのrun IDと同値 |
| `stage` | `prompt_audit`または`prompt_judgment`。CLI指定と同値 |
| `attempt_id` | CLIのattempt IDと同値 |
| `provider` | text。本縦切りの模擬入力では`fixture`を許す |
| `model` | manifestの`instruction_quality_model`と同値 |
| `status` | `succeeded`または`failed` |
| `commands` | 後述のcommand objectを1件以上持つarray |
| `material_observation` | 後述の完全形式object |

command objectは`argv`と`exit_code`の2 keyを持つ。`argv`は空でないtext array、`exit_code`はintegerとする。
起動不能を表す場合も、呼出しを試みたargvと観測済み終了コードを持てないため、本縦切りのingest対象にはせず、
`launch_record_invalid`で停止する。実起動不能の表現は実起動接続の後続作業へ移管する。

`material_observation`は`material_mode`、`extractable_count`、`unextractable_count`、`unique_count`、
`raw_sha256`の5 keyを持つ。`material_mode`は`discovery`、3件数は0以上のinteger、`unique_count`は
`extractable_count`以下、`raw_sha256`は入力raw bytesのSHA-256とする。

保存するlaunch documentは起動記録へ`launch_record_sha256`を追加した11 keyとし、追加keyを除く正規JSON
SHA-256を値とする。raw documentは`schema_version`、`run_id`、`stage`、`attempt_id`、
`input_envelope_sha256`、`launch_record_sha256`、`raw_sha256`、`raw_text`の8 keyを持つ。

未加工結果と起動記録は、解析成否にかかわらず先に保存する。同一run内でattempt IDを再利用せず、保存済み
file、parsed file、eventを上書きしない。

既存`tools/bootstrap/raw_review_store.py`と保存処理を二重実装しない。安全な相対path、排他的作成、正規JSON、
再読込を行う共通不変保存境界を`tools/bootstrap/immutable_result_store.py`へ抽出し、既存review保存と新しい
agent結果保存の双方から使う。既存の公開データ型、既存JSON保存形式、例外型、既存テストの互換性を保つ。

### `AC-PC-005` 指示文監査結果の完全形式と厳格解析

指示文監査rawは次の5 keyを持つJSON一文書だけを受け付ける。

| key | 型・許容値 |
| --- | --- |
| `schema_version` | integer `1` |
| `result_kind` | `prompt_audit` |
| `status` | `completed` |
| `findings` | finding object array。0件を許す |
| `requirement_results` | requirement result object array |

finding objectは`id`、`category`、`severity`、`requirement_ids`、`evidence`の5 keyを持つ。`id`は監査所見
識別子、`category`は`omission`、`leading`、`target_mismatch`、`insufficient_material`、`scope_deviation`の
いずれか、`severity`は`critical`、`high`、`medium`、`low`のいずれかとする。`requirement_ids`は1件以上で
重複がなく、開始設定の要求集合の部分集合とする。`evidence`はtextとする。finding IDを重複させない。

requirement result objectは`requirement_id`、`status`、`evidence`の3 keyを持つ。`status`は`checked`だけ、
`evidence`はtextとする。開始設定の全要求識別子を一回ずつ被覆し、欠落、重複、未知参照を拒否する。

解析後はfindingをID順、requirement resultを要求ID順に並べた同じ5 keyのobjectを正規化済み監査結果とする。
`audit_parsed_sha256`は、この正規化済み監査結果の正規JSON bytesに対するSHA-256である。raw bytes、raw保存
document、末尾改行付きfileのSHA-256ではない。

監査解析成功後、`prompt-judgment-envelope.json`を生成する。これは`schema_version`、`result_kind`、
`run_id`、`audit_parsed_sha256`、`audit_result`、`output_contract`、`envelope_sha256`の7 keyを持つ。
`result_kind`は`prompt_judgment`、`audit_result`は正規化済み監査結果、`output_contract`は
`pilot-prompt-judgment-v1`とする。`envelope_sha256`はそのkeyを除く6 keyの正規JSON SHA-256とする。

### `AC-PC-006` 指示文判定結果の完全形式と厳格解析

指示文判定rawは次の5 keyを持つJSON一文書だけを受け付ける。

| key | 型・許容値 |
| --- | --- |
| `schema_version` | integer `1` |
| `result_kind` | `prompt_judgment` |
| `status` | `completed` |
| `audit_parsed_sha256` | 対応する正規化済み監査結果のSHA-256と同値 |
| `recommendations` | recommendation object array |

recommendation objectは`finding_id`、`recommendation`、`rationale`の3 keyを持つ。`recommendation`は
`accept`、`reject`、`hold`のいずれか、`rationale`はtextとする。監査findingの全IDを一回ずつ被覆し、
findingが0件なら空arrayだけを受け付ける。判定結果はHumanの最終採否を含めない。

解析後はrecommendationをfinding ID順に並べた同じ5 keyのobjectを正規化済み判定結果とし、その正規JSON
SHA-256を判定解析結果の内容指紋とする。

### `AC-PC-007` 追記専用eventと段階状態の機械導出

eventは次の14 keyを持つ完全形式objectとする。

| key | 型・許容値 |
| --- | --- |
| `schema_version` | integer `1` |
| `event_id` | file名stemと同値 |
| `event_type` | 下表の値 |
| `run_id` | manifestと同値 |
| `request_kind` | `implementation` |
| `stage` | `prepare`、`prompt_audit`、`prompt_judgment` |
| `round` | manifestの`instruction_quality_round`と同値 |
| `previous_event_id` | 最初だけ`null`、以後は直前event ID |
| `previous_event_sha256` | 最初だけ`null`、以後は直前event正規JSON SHA-256 |
| `attempt_id` | prepareだけ`null`、以後はCLI指定値 |
| `input_sha256` | 入力configまたは対応envelopeのSHA-256 |
| `output_sha256` | 成功時はmanifestまたは解析結果SHA-256、解析失敗時はraw SHA-256 |
| `status` | `completed`または`failed` |
| `stop_code` | 成功時は`null`、失敗時は§3 `AC-PC-008`の対応code |

event file名、event type、合法な遷移、導出状態を次に固定する。

| file | event type | 前段 | 条件 | 導出状態 |
| --- | --- | --- | --- | --- |
| `0001-prepared.json` | `prepared` | なし | prepare成功 | `ready_for_prompt_audit` |
| `0002-prompt-audit-parsed.json` | `prompt_audit_parsed` | prepared | 監査解析成功 | `ready_for_prompt_judgment` |
| `0002-prompt-audit-parse-failed.json` | `prompt_audit_parse_failed` | prepared | raw保存後に監査解析失敗 | `blocked` |
| `0003-prompt-judgment-parsed.json` | `prompt_judgment_parsed` | audit parsed | 判定解析成功・findingあり | `human_decision_required` |
| 同上 | 同上 | audit parsed | 判定解析成功・findingなし | `ready_for_executor` |
| `0003-prompt-judgment-parse-failed.json` | `prompt_judgment_parse_failed` | audit parsed | raw保存後に判定解析失敗 | `blocked` |

`status`はmanifest、全event、launch、raw、parsed、固定commit blob、現在fileを再読込し、正規JSON、SHA-256、
前段、入力、出力、attempt IDを再照合して状態を導出する。固定commit blobと現在fileが異なる場合は、eventを
書き換えず`stale`を返す。未知event、番号欠落、合法表外の遷移、保存物改竄は`blocked`とする。

本縦切りは一runにつき指示文品質1周、各段階1試行だけを扱う。同一stageまたはattempt IDの再取込みを拒否し、
自動再試行しない。次周回は新しいrun IDと増加した`instruction_quality_round`を持つ新しい開始設定で行う。
複数runをまたぐ同形所見の意味判定と2周連続停止は、Human裁定・再監査を扱う第2縦切りへ移管する。本縦切りは
roundが上限を超える設定を機械拒否し、失敗回数を推測しない。

### `AC-PC-008` コマンド契約、応答、終了コード

コマンド文法を次で固定する。各path引数は絶対pathだけを受け付ける。

```text
reviewcompass3-pilot prepare --config <json-file> --private-root <existing-directory>
reviewcompass3-pilot ingest --private-root <existing-directory> --run-id <id> --stage <prompt_audit|prompt_judgment> --attempt-id <id> --raw-file <file> --launch-record <json-file>
reviewcompass3-pilot status --private-root <existing-directory> --run-id <id>
```

標準出力は次の8 keyを持つJSON一文書と改行だけにする。

| key | 型・許容値 |
| --- | --- |
| `schema_version` | integer `1` |
| `command` | `prepare`、`ingest`、`status` |
| `result` | `completed`、`stopped`、`failed` |
| `state` | §3 `AC-PC-007`の導出状態または`null` |
| `run_id` | 判明している場合はID、未解析なら`null` |
| `event_id` | 今回追加したevent ID。追加なしは`null` |
| `stop_code` | 停止code。成功時は`null` |
| `detail` | 機密値を含まない短い説明。不要時は`null` |

成功は終了コード0、安全停止は2、予期しない内部失敗は1とする。終了コード1では`result: failed`、
`stop_code: internal_error`とする。終了コード2で使用できるstop codeを次に限定する。

```text
config_invalid, repository_invalid, private_root_invalid, source_commit_invalid,
source_blob_invalid, source_digest_mismatch, requirement_mismatch, model_pair_invalid,
run_exists, run_invalid, stage_invalid, attempt_exists, launch_record_invalid,
raw_digest_mismatch, raw_parse_failed, coverage_incomplete, audit_digest_mismatch,
transition_invalid, stored_record_invalid, stale_input
```

未知引数、必須引数欠落、引数型違いは`config_invalid`または`stage_invalid`へ正規化して終了コード2とする。
標準エラーへ判定結果を分散させない。

### `AC-PC-009` 既存機能の非回帰

既存のbootstrap reviewの公開データ型、保存形式、コマンド、テストを壊さない。既存
`reviewcompass3-bootstrap-review`は置き換えず、今回の共通入口と役割を混同しない。

## 4. 禁止事項

- `NG-PC-001` 外部送信、Claude CLI、Codex CLI、Codexサブエージェントを実装コードから起動しない。
- `NG-PC-002` Human所見裁定、実装実行、実装後レビュー、再実装、完了反映を本縦切りへ含めない。
- `NG-PC-003` 未加工結果を解析前に捨てない。解析失敗を成功へ変換しない。
- `NG-PC-004` 段階状態、SHA-256、件数、参照集合をLLMの報告から手転記しない。
- `NG-PC-005` 既存の閉包型`review_pipeline`を発見力モードへ黙って読み替えない。
- `NG-PC-006` `.reviewcompass/workflow/`配下へ新しい台帳を手書きしない。
- `NG-PC-007` 関係のない整形、既存Python全体のインデント変更、既存テストの書換えを行わない。

## 5. 停止条件

- `ST-PC-001` 受入条件を満たすために本依頼外の設計変更、製品schema変更、既存テスト変更が必要になった。
- `ST-PC-002` 共通不変保存境界への抽出が既存保存形式の互換性を壊す。
- `ST-PC-003` private root、Git範囲、symlink、path traversalを安全に区別できない。
- `ST-PC-004` 指示文監査または判定の固定結果形式に意味上の不足が見つかった。

停止条件に達した場合はコードを広げず、事象、根拠、未実施範囲を主担当へ返す。

## 6. 出力要件

- `OUT-PC-001` 実装前に新規受入テストを作り、対象機能が無いため失敗することを単独コマンドで確認する。
- `OUT-PC-002` 実装中は、要求の誤りが判明しない限り固定した受入テストを変更しない。
- `OUT-PC-003` 正常例、負例、境界例に加え、SHA-256改竄、未加工結果上書き、要求被覆欠落、所見全件照合欠落、
  段階飛ばし、private root誤配置を故障注入で検出する。
- `OUT-PC-004` 実装後に対象テスト、既存bootstrap reviewテスト、公式全テスト、`git diff --check`をそれぞれ
  単独コマンドで実行し、終了コードを報告する。
- `OUT-PC-005` 実装結果は変更path、要求識別子ごとの根拠、実行コマンドと終了コード、未解決事項を含む。
- `OUT-PC-006` 実装担当は意味的に完結した変更をコミットして停止する。push、履歴書換え、外部送信は行わない。

## 7. 変更可能範囲

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

## 8. テストと実装の順序

1. 新規テストだけを作り、対象機能不在による失敗を確認する。
2. テストの期待が本依頼と一致することを確認する。
3. 実装を進め、固定したテストを合格させる。
4. 既存保存テストと既存reviewテストを合格させる。
5. 故障注入、実repositoryを使う確認運転、公式全テストを行う。
6. 実装結果をコミットし、主担当へ返す。

本実装が合格しても、`mechanical_assurance_status`を直ちに`connected`へ変更しない。外部実行経路への接続、
実運用での一連の確認、独立レビュー、Human段完了承認は後続境界である。

## 9. 第2縦切りへ移す必須要求

第2縦切りは、次を固定するまで実装を開始しない。

1. 前run ID、前attempt ID、前入力SHA-256、再開段階の参照形式。
2. 指示文所見を同形と数える分類規則。意味分類はLLMの提案、最終分類はHuman裁定とする。
3. Human裁定済み分類と連続回数を上書きせず保存する機械処理。
4. 同形所見が2周続いた場合、指示文修正を続けずHuman判断待ちへ停止する遷移。
5. 初回、異なる所見、同形2回、入力変更、古い結果、改竄の正常例・負例・境界テスト。

本節は第2縦切りの範囲固定で固定入力として参照し、後続の要求識別子へ割り当てる。今回の26件には含めない。
