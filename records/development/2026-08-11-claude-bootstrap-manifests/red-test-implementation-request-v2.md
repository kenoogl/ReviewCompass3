# Codex Pilot 無工具Claude疎通 RED受入試験 作成依頼 v2

- 日付：2026-08-11
- 方式：`pilot_specific_claude_codex`
- 操縦者：Codex主担当
- 操縦者モデル：`gpt-5.6-sol`
- 実装担当：Codex実装用サブエージェント
- 実装担当モデル：`gpt-5.6-sol`
- 指示文監査・判定・レビュー担当モデル：`gpt-5.6-terra`
- 危険度：`high`
- 作業段階：`RED`。実装が無ければ失敗する受入試験と基準目録だけを作る
- 作業開始commit：本書をcommitしたcommit
- process基準commit：`e54fcdaec38ab4b755f67371dbbdd20604447b95`
- 範囲固定commit：`32ab8950428650500a9b4d9b23d318c1f7de240c`
- 範囲固定SHA-256：`02a4f6786875a9eeb87165e387ac1e65d520423930bf3849cb967249639861a7`
- 独立範囲レビューSHA-256：`3e0a6af442b7461858dfee94ac4dbd50687d5ca64778a03d1cad9b378b567189`
- RED開始Human裁定SHA-256：`7b0e7959df8acd589135ddf48406e8d57d0d59dafb3a601427879a63da317158`
- round 1所見Human裁定SHA-256：`6bb5ddc7455e0734664e2c04f7e2f6f710a01645b27d6435410a61dd09175778`
- Claude応答形式記録SHA-256：`73f871aea0b65cdb6ebe4e0b66ba18038c7102c0533a2046ebfd33bffc962e52`
- 指示文品質確認：round 2 / 2
- 実装・レビュー往復の上限：2
- 実行段階台帳の機械保証：`specified_only`

本書はround 1の`PA-CB-RED-001〜004`をHumanが全件採用した結果を反映した、RED段階の単一指示書である。
要求の正本は範囲固定v3だけとする。v1、過去の範囲固定、過去のレビュー依頼、旧実装案を指示として併用しない。
外部送信は一切伴わない。

## 1. 一作業の目的

範囲固定v3の`AC-CB-001〜013`、`NG-CB-001〜007`、`ST-CB-001〜007`、`OUT-CB-001〜005`を、
実装前の受入試験へ一対一で対応付ける。4つの試験fileを収集可能な状態にし、各fileで未実装由来の失敗を
一件以上確認する。実装前から成立する境界確認だけは合格してよい。

production codeと既存testは変更しない。試験を合格させる実装は次のGREEN段階へ残す。

## 2. 固定入力と開始前停止

### 2.1 範囲固定v3 §3の12件

範囲固定v3を対象commit `32ab8950428650500a9b4d9b23d318c1f7de240c`のGit blobから読み、§3の表を
機械抽出する。列は`identity | path | SHA-256`、行数は12、identityとpathの重複は0件でなければならない。

抽出した12件を、同じ対象commitのGit blob、現在file、表中SHA-256で全件照合する。一件でも欠落、不一致、
未commit、symbolic link、通常file以外なら、fileを変更せず`stale_input`で停止する。12件を本書へ重複転記せず、
範囲固定v3の表を一つの正本として扱う。

### 2.2 追加固定材料

次の8件も、本書をcommitしたcommitのGit blob、現在file、記載SHA-256で機械照合する。

1. 範囲固定v3：
   `records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v3.md`、
   SHA-256 `02a4f6786875a9eeb87165e387ac1e65d520423930bf3849cb967249639861a7`。
2. 独立範囲レビューv2：
   `records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-v2.md`、
   SHA-256 `3e0a6af442b7461858dfee94ac4dbd50687d5ca64778a03d1cad9b378b567189`。
3. RED開始Human裁定v1：
   `records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-v3-red-start-human-decision-v1.md`、
   SHA-256 `7b0e7959df8acd589135ddf48406e8d57d0d59dafb3a601427879a63da317158`。
4. round 1品質確認：
   `records/development/2026-08-11-claude-bootstrap-manifests/red-test-prompt-quality-round-1-v1.md`、
   SHA-256 `18cbbc9240bb0fb5c72ee3b175841817e8013bf8a0d4aa05379c91f7ec0e143b`。
5. round 1所見Human裁定：
   `records/development/2026-08-11-claude-bootstrap-manifests/red-test-prompt-finding-human-decision-v1.md`、
   SHA-256 `6bb5ddc7455e0734664e2c04f7e2f6f710a01645b27d6435410a61dd09175778`。
6. Claude 2.1.220応答形式記録：
   `records/development/2026-08-11-claude-bootstrap-manifests/claude-2.1.220-result-schema-v1.json`、
   SHA-256 `73f871aea0b65cdb6ebe4e0b66ba18038c7102c0533a2046ebfd33bffc962e52`。
7. 宣言対応表検査器：`tools/development/declaration_red_map_check.py`、
   SHA-256 `151d2ef80a3ebb0dad6999dc1db63c0790541575ef0e7d7efd9da9ac7a507a61`。
8. 入口設定：`pyproject.toml`、
   SHA-256 `6a0744e8a8ab4150e2c8309f410f5dcc079810198e72066c245b0b6362c7369e`。

本書自身も、作業開始commitのGit blob、現在file、指示時に渡されたSHA-256で照合する。§2.1、§2.2、本書の
全照合が終わるまでfileを変更しない。作業開始HEADとworktreeを記録し、既存の利用者差分があれば帰属を推測せず
停止する。

## 3. 変更可能pathと成果物

変更できるのは次の新規pathだけである。

- `tests/test_claude_bootstrap.py`
- `tests/test_claude_bootstrap_cli.py`
- `tests/test_claude_bootstrap_adversarial.py`
- `tests/test_claude_bootstrap_entrypoints.py`
- `tests/fixtures/claude_bootstrap/`配下
- `records/development/2026-08-11-claude-bootstrap-manifests/process-call-baseline-v1.json`
- `records/development/2026-08-11-claude-bootstrap-manifests/declaration-red-map-v1.json`
- `records/development/2026-08-11-claude-bootstrap-manifests/red-evidence-v1.md`

本書、固定材料、既存file、production code、`tools/egress/`、`pyproject.toml`、TODO、Workflow台帳は変更しない。
新規の試験補助処理はtest fileまたはfixture内だけへ置く。production側へfake runner、test hook、設定入口を
追加しない。

## 4. 試験が固定する公開契約

### 4.1 Python入口

将来の`tools.development.claude_bootstrap`から公開関数
`run_approved_no_tool_bootstrap(manifest_digest, approval_id)`だけを呼ぶ。callerがprompt、file、model、provider、
Claude実行path、argv、session ID、runtime root、保存先、環境変数、runnerを渡せる形を認めない。

作業repositoryは現在作業directoryから解決する。testは一時Git repositoryへ移動し、`Path.home()`を一時
directoryへ差し替えて既定stateと秘密保存場所を隔離する。processは標準ライブラリ`subprocess.run`をtest側で
置き換えて観測し、production引数へrunnerを注入しない。

### 4.2 CLI入口

`reviewcompass3-pilot bootstrap --manifest-digest <sha256> --approval-id <id>`だけを公開形とする。未知option、
重複option、欠落、追加位置引数を拒否する。標準出力は改行で終わるJSON一行だけ、標準エラーは空とし、
成功0、内部失敗1、安全停止2を区別する。

停止JSONは少なくとも`schema_version`、`result`、`stop_code`、`payload_process_count`、
`preflight_process_count`、`approval_state`、`recovery`を一回ずつ持ち、秘密値を含まない。

### 4.3 Claude外側JSONの版固定fixture

Claude processは起動しない。正本は§2.2の
`claude-2.1.220-result-schema-v1.json`とし、同記録の実行file SHA-256、build Git SHA、静的schema断片
1,644 byte、そのSHA-256、開始・失敗・終了markerの一意性をtest fixtureの由来へ固定する。

成功fixtureは応答形式記録の`success.required`を全件持ち、任意keyを全件省略し、`is_error: false`、
`permission_denials: []`、`modelUsage: {}`とする。成功required keyは次の14件である。

`type`、`subtype`、`duration_ms`、`duration_api_ms`、`is_error`、`num_turns`、`result`、`stop_reason`、
`total_cost_usd`、`usage`、`modelUsage`、`permission_denials`、`uuid`、`session_id`。

成功の任意keyは次の15件である。

`ttft_ms`、`ttft_stream_ms`、`time_to_request_ms`、`user_message_uuid`、`request_sent_wall_ms`、
`time_to_request_from_spawn_ms`、`warm_spare_claimed`、`time_origin_ms`、`api_error_status`、
`structured_output`、`deferred_tool_use`、`terminal_reason`、`fast_mode_state`、`fast_mode_disabled_reason`、`origin`。

失敗fixtureは応答形式記録の`error.required`を全件持ち、任意keyを全件省略する。次の4 subtypeを各一件作る。

- `error_during_execution`
- `error_max_turns`
- `error_max_budget_usd`
- `error_max_structured_output_retries`

失敗required keyは成功と共通の`result`以外の13件に`errors`を加えた14件であり、`is_error: true`とする。
失敗の任意keyは`terminal_reason`、`fast_mode_state`、`fast_mode_disabled_reason`、`origin`の4件である。

未知の外側key、必須key欠落、成功の`is_error: true`、permission denial、失敗subtype、道具利用を成功扱いに
しない。fixture由来記録へ利用者固有絶対path、実応答、認証値、秘密値を書かない。

## 5. test fileごとの責務

### 5.1 `tests/test_claude_bootstrap.py`

- 範囲固定v3 §5の二payload、byte数、各SHA-256、順序JSON、ordered digestを機械転記し、1 byte、順序、件数、
  末尾改行の変化を拒否する。
- 目録、Human Decision、承認token、store identity、期限、provider、model、実行file Digest、材料方針3項を
  完全一致で検査する。
- 伏字化で一文字でも変わる入力、秘密らしい文字列、email、電話番号をprocess作成前に拒否する。
- version、実行file Digest、認証3項、環境変数除外、repository外の既存空directory、保存枠を検査する。
- 成功、1回目停止、2回目停止、外側・内側JSON、session、nonce、道具不使用、終了コード、保存結果を検査する。
- raw、実行仕様、receiptの排他的作成と再読込を確認し、raw本文をGitへ書かない。

### 5.2 `tests/test_claude_bootstrap_cli.py`

- 公開optionを二つへ閉じ、成功・停止・内部失敗の終了コードとJSON一行出力を検査する。
- stdout以外への秘密漏洩、traceback、余分な自由文を拒否する。
- 既存prepare、ingest、statusを壊さず、bootstrapだけを薄く接続する契約を固定する。

### 5.3 `tests/test_claude_bootstrap_adversarial.py`

- tokenの逐次二重使用、並行claim、状態重複、store欠落、store identity置換、symbolic link、未知file、
  広すぎる権限を拒否する。
- root上書き環境変数、repository・親・内部・symlink経由・空でない作業directoryを拒否する。
- manifest、Git blob、payload、順序、approval、binary、auth、raw保存先の改竄をprocess作成前に拒否する。
- 子processからAPI認証、接続先上書き、全`REVIEWCOMPASS3_*_ROOT`を除外し、値を公開出力へ出さない。
- 1回目失敗後の2回目、retry、fallback、別model、別provider、別binary、shell、既存汎用runnerへの迂回が0件で
  あることを確認する。
- 補助関数を特定例へ過剰適合させず、後続レビューがfixture外の反証を追加できる形にする。

### 5.4 `tests/test_claude_bootstrap_entrypoints.py`

- 公開入口が既存`reviewcompass3-pilot`の`bootstrap`一つだけであることを確認する。
- `AGENTS.md`、`CLAUDE.md`、共通promptの発見経路を確認し、規則本文の複製を拒否する。
- productionで新規process作成が将来
  `tools/development/claude_bootstrap.py:run_approved_no_tool_bootstrap`から到達する固定一関数だけにある契約を
  構文木で検査する。
- `structured_argv_executor.subprocess_runner`、shell、動的import、`eval`、`exec`、任意argv入口、productionへ
  注入できるfake runnerを拒否する。
- `tools/egress/`と既存testがprocess基準commitから不変であることを確認する。後続recordやTODOのcommitを
  範囲外変更と誤判定せず、固定禁止path自体のGit blobを照合する。

全4 fileは単独で収集に成功し、各fileに少なくとも一つ未実装由来の失敗を持つ。module importはtest関数内または
遅延helperで行い、未実装moduleによる収集errorへ全件をまとめない。

## 6. process基準目録

基準commit `e54fcdaec38ab4b755f67371dbbdd20604447b95`の`tools/**/*.py`を、Git blobからPython構文木で
機械走査する。次を列挙する。

- `subprocess`のimport、alias、属性参照、呼出し。
- `os.exec*`、`os.spawn*`、`pty`、`asyncio.create_subprocess*`、`multiprocessing`のprocess作成参照。
- `tools.development.structured_argv_executor.subprocess_runner`の定義、import、参照。
- 動的import、`eval`、`exec`のうちprocess起動へ到達し得る参照。

目録JSONは`schema_version`、`record_kind`、`base_commit`、`roots`、`entries`、`inventory_sha256`を持つ。
各entryは`path`、`line`、`column`、`call_kind`、`qualified_name`、`file_sha256`を持つ。entryはこの順序で
整列する。`inventory_sha256`は同keyを除く正規JSON bytesのSHA-256とする。生成後に再読込し、同じ入力から
同じbytesを再生成できることを確認する。

一時生成処理はrepository外へ置く。RED段階で`tools/development/process_call_inventory.py`を作らない。
新規testは、将来の同moduleが基準目録と同じ結果を生成し、GREEN後の差分規則を満たすことを要求して失敗する。

## 7. 要求ごとの試験宣言

`declaration-red-map-v1.json`は次の32件を完全な宣言集合として一回ずつ持つ。各要求は少なくとも一つの固有testへ
結び、同じtestを複数要求へ使い回さない。詳細は範囲固定v3を正とする。

### `AC-CB-001`
公開入口一つ、入力二項目、Python公開関数一つを固定する。
### `AC-CB-002`
目録、二payload、各Digest、順序、ordered digestの完全一致だけを合格にする。
### `AC-CB-003`
Human承認の全束縛、材料方針、期限、未消費状態を完全照合する。
### `AC-CB-004`
単一の送信前検査がprocess直前に全前提を閉じる。
### `AC-CB-005`
認証、接続先、repository情報、秘密値を子processと公開出力へ伝えない。
### `AC-CB-006`
Claude道具、MCP、技能、plugin、hook、Chrome、別agentを無効にする固定argvだけを作る。
### `AC-CB-007`
payload processを最大二つ順番に実行し、失敗後の後続と自動再試行を禁止する。
### `AC-CB-008`
承認tokenを逐次・並行の双方で一回だけclaimし、root・store変更で再利用可能にしない。
### `AC-CB-009`
版固定の外側JSON、内側JSON、session、nonce、道具不使用、終了コードを完全照合する。
### `AC-CB-010`
raw、実行仕様、receiptをrepository外へ不変保存し、保存不能時はprocessを作らない。
### `AC-CB-011`
全停止応答が理由、二種類のprocess件数、approval状態、復旧手順をJSON一行で返す。
### `AC-CB-012`
process基準目録比較と新経路の起動箇所・汎用runner非接続を固定する。
### `AC-CB-013`
既存pilot、egress 6 file、公式全testの回帰を分離して確認する。
### `NG-CB-001`
`tools/egress/`、既存authority、Workflow台帳、既存testの期待値を変更しない。
### `NG-CB-002`
試験、実装、レビュー中にClaude process、外部送信、認証、実model確認を行わない。
### `NG-CB-003`
任意prompt、file、repository内容、model、provider、binary、argv、rootを入力にしない。
### `NG-CB-004`
shell、API key、接続先上書き、Desktop、browser、MCP、plugin、hook、Claude道具、別agent、fallback、retryを使わない。
### `NG-CB-005`
tokenをpendingへ戻さず、別markerを作らず、store欠落時に初期化しない。
### `NG-CB-006`
raw、認証値、利用者固有絶対pathをGit管理対象へ保存しない。
### `NG-CB-007`
本経路を実装委譲、一般対話、旧用途の外部判定へ拡張しない。
### `ST-CB-001`
範囲レビュー合格、Human RED承認、§2の全固定入力を開始前に確認する。
### `ST-CB-002`
固定入力、目録、payload、順序、Claude版・Digest、外側JSON仕様を固定できなければ停止する。
### `ST-CB-003`
認証が`claude.ai`／`firstParty`以外、未認証、追加課金・API key要求なら停止する。
### `ST-CB-004`
一回性、迂回検査、安全な外部保存をfake processで実証できなければ停止する。
### `ST-CB-005`
許可path外変更、既存schema破壊、既存testの意味変更が必要なら停止する。
### `ST-CB-006`
完了レビュー合格と送信実物へ束縛した別Human承認が無ければ実送信しない。
### `ST-CB-007`
host安全審査がprocess作成を拒否した場合、別経路へ切り替えず停止する。
### `OUT-CB-001`
正本32要求ID集合との完全一致、固有test対応、単独RED結果、目録DigestをEvidenceへ残す。
### `OUT-CB-002`
GREEN用の変更・検査欄をREDでは未実施として区別する。
### `OUT-CB-003`
CLIが成功・停止・内部失敗を区別するJSON一行だけを返し、秘密を含めない。
### `OUT-CB-004`
完了レビュー用に上流導出、独立反証、閉じた4類型を要求する入口を残す。
### `OUT-CB-005`
別途承認された実Run receiptの必須項目をtestで固定し、実Run自体は行わない。

## 8. 宣言からREDへの対応表

`declaration-red-map-v1.json`は`scope.kind: complete`とする。4 test fileに実在する全`test_`関数を一回ずつ
列挙し、宣言の無いtest、testの無い宣言、共有testを0件にする。

次を、`declaration_red_map_check`の通常検査とは別の固有test
`test_declaration_map_keys_equal_scope_requirement_ids`で機械確認する。

- 宣言key集合が`AC-CB-001〜013`、`NG-CB-001〜007`、`ST-CB-001〜007`、`OUT-CB-001〜005`の32件と
  完全一致する。
- 件数32、欠落0、重複0、未知参照0である。

この固有testは`OUT-CB-001`だけへ対応付け、他要求へ共有しない。

未実装機能に依存するtestは`red_now: true`とする。実装前から成立する固定入力、既存path不変、fixture schemaの
境界testだけを`red_now: false`にでき、その理由を`boundary_reason`へ記録する。

commit前に`check_declaration_red_map`を`verify_red=True`で単独実行し、`status: passed`、
`mismatched: 0`、`unknown: 0`を確認する。全test fileの収集errorは0件でなければならない。

## 9. 必須の機械確認

実装担当は次をそれぞれ単独commandで実行し、終了コードをRED Evidenceへ記録する。

1. 4 test fileの`--collect-only`。期待は終了0。
2. 4 test fileを一つずつ実行。各fileに一件以上REDがあり、期待は終了1。
3. 4 test fileをまとめて実行。期待は終了1。
4. 正本32要求ID集合との完全一致test。期待は終了0。
5. 宣言対応表の静的検査。期待は終了0、`status: passed`。
6. 同対応表の`verify_red=True`照合。期待は終了0、`mismatched: 0`、`unknown: 0`。
7. 新規4 fileを除外した既存全test。期待は終了0。
8. 既存pilot acceptance testとegress 6 file。期待は終了0、既存件数と一致。
9. process基準目録の同一入力二回生成。期待はbytesとDigestが一致。
10. Claude応答形式記録の静的schema断片Digest・marker一意性とfixture完全性。期待は終了0。
11. `git diff --check`。期待は終了0。
12. 変更pathが§3の新規pathだけで、production、既存test、`tools/egress/`に差分がないこと。

失敗は未実装の公開module、入口、応答、保存、token、目録生成へ帰属させる。構文誤り、fixture欠落、helper不具合、
収集error、環境依存、偶然の外部process拒否をRED根拠にしない。

## 10. RED Evidenceと実装担当の報告

`red-evidence-v1.md`へ実施、結果、判断、未実施、手戻りを分けて記録する。作成path、全commandと終了コード、
収集件数、合格・失敗件数、宣言32件の照合、各file Digest、process目録Digest、schema記録Digestを含める。

production実装、既存test変更、Claude起動、認証、外部送信、実Run、raw保存は未実施として明記する。

成果物を再読込し、明示pathだけをstageし、差分検査後にRED成果だけを一つの意味単位でcommitする。終了応答は
commit SHA、変更path、各Digest、全要求IDの結果、全commandと終了コード、未解決事項、未実施を含める。
push、履歴書換え、production実装、TODO更新は行わない。

## 11. 禁止事項と停止条件

- 固定入力不一致、既存利用者差分、許可path外変更の必要、応答schemaを静的根拠へ固定不能、外部processが必要、
  対応表の不一致・不明、既存test不合格のいずれかで停止する。
- 停止時はproductionを作らず、試験を弱めず、別model、別担当、Claude、外部API、browser、networkへ切り替えない。
- 意味上の新しい所見、要求変更、schema変更、既存testの期待値変更が必要なら自動修正せずHuman判断へ戻す。
- 調査中の範囲外発見はその場で直さず、候補として報告する。
