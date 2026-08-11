# Codex Pilot用・無工具Claude疎通経路の範囲固定 v2

- 状態：`scope_review_pending`
- 日付：2026-08-11
- collaboration_method：`pilot_specific_claude_codex`
- pilot：Codex主担当
- implementer候補：Codex実装用サブエージェント
- reviewer：Codexレビュー用サブエージェント
- work_item：`codex-pilot-no-tool-claude-bootstrap`
- risk提案：`high`
- base commit：`07b62593e776925cd500e249ec8fdc1389a7ffe9`
- 差替え対象：`records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v1.md`

## 1. 目的、authority、現在のHuman境界

目的は、Codex主担当がClaude Codeを安全な固定入口から起動し、固定した非機密の二つの文だけで、新規
sessionと同一sessionの再開を確認できるようにすることである。これは実装委譲ではなく、外部経路の最小
疎通確認である。

Humanは次を順に選択した。

1. 第1機械処理縦切りの後続として、外部実行経路を接続する。
2. その最初の段階を、Claudeの全道具を無効にした無工具の疎通確認とする。

選択の正本は次の二件である。

- `records/session-handoffs/2026-08-11-pilot-collaboration-external-route-selection-human-decision-v1.md`
- `records/session-handoffs/2026-08-11-pilot-collaboration-no-tool-bootstrap-selection-human-decision-v1.md`

このHuman選択は、本書の作成、検証、独立範囲レビュー依頼までを認める。次はまだ認めない。

- `high` riskのREDテスト作成と実装。
- Claudeの認証操作。
- Claude processの作成と実payload送信。
- repository内容または秘密情報の送信。
- Claudeの道具の有効化。

独立範囲レビューが`verified`となり、Humanが本書のrisk、要求、変更範囲、RED開始を明示承認するまで
実装しない。実装完了レビューが`verified`となった後も、実送信は送信時の一回限りHuman承認を別に要求する。

## 2. 先行v1からの修正

先行範囲レビュー
`records/session-handoffs/2026-08-11-claude-scope-review-approved-claude-send-path-v1.md`
はF1〜F4をblockingとした。本v2では次のように修正する。

| 所見 | v2での修正 |
| --- | --- |
| F1：新用途と凍結資産のauthority不足 | Humanの段階選択を新用途の範囲設計authorityとして固定する。`tools/egress/`は変更も転用もしない。実装authorityは範囲レビュー後のHuman再開承認へ残す |
| F2：既存の安全条件の欠落 | 単一の送信前検査、伏字化変化時停止、材料方針3項、内容指紋付き目録、復旧手順、raw保存をACへ明記する |
| F3：迂回検査が機械判定不能 | 新経路から到達できるprocess起動を定義し、基準commitのrepository全体のprocess起動一覧と実装後一覧をASTで比較する。既存の汎用argv実行器を新経路から使うことを禁止する |
| F4：承認recordと消費markerの分離 | 外部固定store内の一つの承認token自体を`pending`から`claimed`、`consumed`へ原子的に移動する。別markerを正本にせず、root変更・欠落時は再初期化せず停止する |

`docs/design/2026-08-07-external-egress-gate-proposal-v4.md`を本用途のauthorityとはしない。同文書でHumanが
既に選んだ安全条件を、本用途にも採用する提案として本書へ書き直し、本書へのHuman再開承認によって
新用途の条件として確定させる。

## 3. 固定入力

範囲レビューは次のpathとSHA-256を照合してから開始する。一件でも不一致なら本書を`stale`として停止する。

| identity | path | SHA-256 |
| --- | --- | --- |
| Intent | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` |
| 用語集 | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` |
| 計画 | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| 開発方針 | `docs/development/2026-08-02-development-policy.md` | `08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c` |
| 開発入口 | `docs/development/2026-08-03-initial-development-checklist.md` | `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c` |
| 操縦者別連携 | `docs/development/pilot-specific-claude-codex-collaboration.md` | `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d` |
| 共通レビュー | `docs/development/work-review-protocol.md` | `b7eb8f08c7b3f585d64d163a7a2f93e758e57e830bb973cc2441bfadbc98a3df` |
| 外部経路選択 | `records/session-handoffs/2026-08-11-pilot-collaboration-external-route-selection-human-decision-v1.md` | `58d7809b547b339c3641f336cc23b2729aca6e09d7d50a109ed4c7f984de7983` |
| 先行v1 | `records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v1.md` | `22860ffddb23ad35d511b4e7590a0d17f37827782059bd4344b66a0583e0250d` |
| 先行範囲レビュー | `records/session-handoffs/2026-08-11-claude-scope-review-approved-claude-send-path-v1.md` | `402b2f7af1b2b28c9dac497ec2624e6078e361cebf55730b12f8ee8784c1e1ff` |

本書と無工具段階選択recordのSHA-256は、両fileを作成したcommitの後にレビュー依頼へ固定する。自己Digestを
本書へ書き戻す追加commitは作らない。

## 4. 実測済みの外部実行条件

【実測】Claude Codeはversion `2.1.220`、実行fileのSHA-256は
`8addc857f3fe64d5a0368af9ee50321b50afb4a6918ba3ef018ab84f5dbbe081`である。

【実測】同versionの`claude --help`には次が明記されている。

- `--tools ""`：全ての組込み道具を無効にする。
- `--safe-mode`：CLAUDE.md、技能、plugin、hook、MCP、独自command、agentなどの利用者設定を無効にする。
- `--strict-mcp-config`：明示したMCP設定以外を無視する。
- `--disable-slash-commands`：技能を無効にする。
- `--no-chrome`：Chrome連携を無効にする。
- `--print`と`--output-format json`：非対話で単一結果を得る。
- `--session-id`と`--resume`：指定sessionの開始と再開を行う。

先行v1に書かれた`--max-turns`は現versionに存在しないため使用しない。`--bare`は契約認証を読まずAPI keyを
要求するため使用しない。modelは`fable`、provider識別子はClaude Codeのfirst-party接続を表す
`claude-code-first-party`に固定し、自動fallbackを指定しない。

【記録】認証情報と接続先上書き環境変数を除外した直近の認証状態は`loggedIn: false`、
`authMethod: none`、`apiProvider: firstParty`である。認証済みとの報告に使わず、実送信の停止条件とする。

## 5. 固定payloadと順序

payload 1は次の一行のUTF-8文字列とし、末尾改行を含めない。

```text
あなたはClaude Reviewerです。Codex Pilotからの疎通確認です。ツールを使わず、他のエージェントを起動せず、次のJSONだけを返してください。{"protocol":"codex-pilot-claude-bootstrap-v1","role":"reviewer","nonce":"RC3-CPC-20260811-A","reinvoke":false}
```

- byte数：296
- SHA-256：`18059aa0f32b93bae5b117092a45fbf4e985381546b8c64507168f0226f4ad64`

payload 2は次の一行のUTF-8文字列とし、末尾改行を含めない。

```text
同じセッションの継続確認です。前回のnonceを使い、次のJSONだけを返してください。{"protocol":"codex-pilot-claude-bootstrap-v1","continued":true,"nonce":"<前回のnonce>","reinvoke":false}
```

- byte数：221
- SHA-256：`c2309f2624ba0d0f36fd00894dcbc67ccd66e83429960c4083f4e10b2f18982a`

順序の指紋は、各要素を`ordinal`と`sha256`だけのobjectとするJSON配列を、key順、空白なし、UTF-8、末尾
改行なしで直列化してSHA-256を計算する。正規化した計算対象と結果は次のとおりである。

```json
[{"ordinal":1,"sha256":"18059aa0f32b93bae5b117092a45fbf4e985381546b8c64507168f0226f4ad64"},{"ordinal":2,"sha256":"c2309f2624ba0d0f36fd00894dcbc67ccd66e83429960c4083f4e10b2f18982a"}]
```

- ordered payload digest：`26933d4f45ed497f9d1d9f5fdc741aca87b0ad37c3ed3c35fd99ebff6b2bd8a0`

既存の`payload_list_digest`は順序を表さないため、本用途では承認や実行順の根拠に使わない。

## 6. 最小E2E

E2E（入口から結果確認までを通す試験）は、次の一操作、payloadを持つprocessは最大二つとする。
version確認と認証状態確認のprocessはpayloadを持たない事前検査として別に数え、receiptでは両方の件数を
分けて記録する。

1. 内容指紋付き目録、Human承認、承認token、Claude実行file、認証、保存先、空の作業directoryを検証する。
2. 承認tokenを`pending`から`claimed`へ原子的に移し、これ以降は失敗しても再利用可能状態へ戻さない。
3. 固定argvとpayload 1で新しいUUIDのsessionを開始する。
4. 終了code、Claude出力の外側JSON、内側の固定JSON、session ID、道具不使用を検証し、rawを不変保存する。
5. 4が全て合格した場合だけ、同じsession IDを`--resume`へ渡してpayload 2を送る。
6. 2回目も同様に検証し、同じnonceと`continued:true`を確認してrawを不変保存する。
7. 承認tokenを`claimed`から`consumed`へ原子的に移し、成功または停止receiptを保存する。

payload 1のprocess作成後は、いかなる失敗でも自動再試行しない。payload 1が不合格ならpayload 2のprocessを
作成しない。`claimed`のまま異常終了した承認も消費済み相当とし、新しいHuman承認なしに復旧送信しない。

## 7. 単一の送信前検査と実行入口

新経路の公開入口は一つとする。

```text
reviewcompass3-pilot bootstrap --manifest-digest <sha256> --approval-id <id>
```

入口は目録のSHA-256と承認IDだけを受け取る。prompt、file path、model、provider、Claude実行path、追加argv、
session ID、runtime root、保存先、環境変数を引数として受け取らない。

production codeでは、公開関数`run_approved_no_tool_bootstrap`だけが送信前検査、承認claim、最大二processの
実行、raw保存、receipt保存を順番に統合する。この関数より下流へ「検証済み」を表す公開booleanや、callerが
組み立てられるargvを渡さない。process起動の直前に別の検査実装を置かず、本関数内の一つの検査結果だけを
使う。

検査は少なくとも次を一度に確認し、一件でも不合格ならprocessを作成せず、停止理由と実行可能な復旧手順を
単一JSONで返す。自動修正、自動切詰め、別model、別認証、別経路へのfallbackは行わない。

1. 目録file名、現在bytes、Git blobのSHA-256が全て`--manifest-digest`と一致する。
2. 目録のschema、purpose、provider、model、二payload、各Digest、順序、ordered digestが§5と一致する。
3. payloadへ伏字化を適用し、文字が一つでも変わったら混入の兆候として停止する。変化なしを安全の証明にしない。
4. 資格情報、秘密らしい文字列、email、電話番号の走査結果が0件である。
5. Human承認が`approved_by: user`、purpose、provider、model、目録Digest、ordered digest、実行file Digest、
   有効期限、未消費状態、材料方針3項に一致する。
6. 材料方針の`require_secret_scan`、`forbid_credentials`、`forbid_personal_identifiers`が全て`true`である。
7. Claude Codeのversionと実行file SHA-256が§4に一致する。標準installの入口symbolic linkは許すが、
   解決後の対象が通常fileであり、別versionへの多段linkやrepository内へのlinkではないことを確認する。
8. 認証状態が`loggedIn: true`、`authMethod: claude.ai`、`apiProvider: firstParty`である。
9. API認証や接続先上書きの環境変数を子processから除外し、その値をどの出力にも含めない。
10. repository外に実体がある既存の空directoryを作業directoryとし、repository、その親、その内部、
    symbolic link経由、既存entryを拒否する。
11. rawとreceiptの排他的な保存枠をprocess作成前に確保し、repository外の機密保存先へ不変保存できる。
12. 承認tokenの固定store identity、状態、排他的な移動が§9を満たす。

## 8. 固定argv、環境、応答

argvは構造化配列としてcode内で組み立て、shellを使わない。第1processには次のoptionだけをこの順で使う。

```text
claude --print --safe-mode --tools "" --disallowedTools "*" --strict-mcp-config --mcp-config '{"mcpServers":{}}' --disable-slash-commands --no-chrome --output-format json --model fable --session-id <generated-uuid> <payload-1>
```

第2processは`--session-id <generated-uuid>`を`--resume <same-uuid>`へ置き換え、末尾をpayload 2にする。
`--continue`、`--fork-session`、`--fallback-model`、`--add-dir`、`--file`、`--settings`、
`--setting-sources`、`--plugin-dir`、`--plugin-url`、`--agent`、`--agents`、`--allow-dangerously-skip-permissions`、
`--dangerously-skip-permissions`、`--chrome`、`--ide`、`--worktree`、stdin入力は使わない。

子processの環境から最低限、`ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_BASE_URL`、
`CLAUDE_CODE_OAUTH_TOKEN`、`CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_VERTEX`、
`CLAUDE_CODE_USE_FOUNDRY`、全`REVIEWCOMPASS3_*_ROOT`を除外する。値をlog、error、raw以外のrecord、
receiptへ出さない。環境変数名の追加は、認証statusとClaudeの公式helpから機械導出し、固定testへ加える。

終了codeは両processとも0だけを合格とする。Claudeの外側JSONからsession ID、結果、error状態、利用した
道具を機械抽出する。未知の形式、session不一致、道具利用、permission denial、追加turn、結果外の自由文を
成功扱いにしない。内側の結果は§5のJSONと完全一致させ、意味が近いだけの応答を合格にしない。

外側JSONの正確なschemaはClaudeを実送信して推測せず、実装前に利用可能な公式仕様またはversion固定fixtureへ
束縛する。仕様を固定できない場合はRED開始後もprocessを作成せずHumanへ停止報告する。

## 9. 一回限り承認の正本

Humanの承認内容の正本は、GitへcommitしたHuman Decision recordとする。実行可能かどうかの正本は、その
Decision Digestへ束縛した一つの承認tokenの所在とする。承認tokenとは、一度だけ送信開始権を表すJSON fileで
あり、別の消費markerを作らない。

承認storeはproject-first development profileの既定`state` rootの下に固定し、caller指定pathと
`REVIEWCOMPASS3_RUNTIME_ROOT`等の上書きを受け付けない。storeは次を満たす。

1. `store.json`にランダムなstore identityを持ち、送信入口は自動作成や再初期化をしない。
2. Human Decision recordがstore identity、approval ID、目録Digest、ordered digest、provider、model、purpose、
   実行file Digest、期限を固定する。
3. tokenの現在状態は、同じfileが`pending`、`claimed`、`consumed`のどの固定directoryに存在するかだけで表す。
4. 送信直前に同一filesystem内の原子的renameで`pending`から`claimed`へ移す。並行する二つ目は
   `pending`が無いためprocess作成前に停止する。
5. 正常終了または処理できた停止では`claimed`から`consumed`へ移す。異常終了で`claimed`に残っても再利用を
   禁止する。
6. 三directoryの複数に同じapproval IDがある、未知fileがある、symbolic linkがある、権限が広い、store
   identityが違う場合は停止する。
7. storeまたは`store.json`が欠落、削除、別identityへ置換された場合は自動で作り直さず停止する。同じ承認IDを
   新しいstoreへ移さず、新しいHuman Decisionを要求する。

この保証は、正規入口の逐次実行、並行実行、root指定変更、store欠落・通常の置換を対象とする。端末所有者が
過去のfilesystem全体を同一bytesへ意図的に巻き戻す攻撃は、local CLIだけでは原理的に検出できない。この
限界を成功receiptへ記載し、local端末所有者を攻撃者と仮定した暗号学的な一回性を主張しない。

## 10. process迂回の機械検査

本書でいう「新経路の外部process」とは、`reviewcompass3-pilot bootstrap`から到達するproduction moduleが
作成するprocessをいう。端末利用者が直接shellを使うことや、用途の異なる既存commandが持つprocess起動まで
消滅させるとは主張しない。

RED時に、base commitの`tools/`全体をPythonの構文木（プログラムの構造を表す機械データ）で走査し、
`subprocess`、`os.exec*`、`os.spawn*`、`pty`、既知の汎用argv実行器の定義と参照を全列挙した基準目録を作る。
目録は対象commit、全path、行番号、呼出し種別、各file Digest、目録自身のDigestを持つ。

GREEN後に同じ検査器で再生成し、次を機械確認する。

- 基準目録にある既存起動箇所は、本作業の許可path外で一件も追加、削除、変更されていない。
- 新規の実process作成は`tools/development/claude_bootstrap.py`の固定した一関数内だけにある。
- CLIからその関数までのimport先に、`structured_argv_executor.subprocess_runner`その他の汎用argv実行器、
  `shell=True`、動的import、`eval`、`exec`、shell command文字列が無い。
- test用fake runnerはtest pathだけにあり、production引数やCLI optionとして注入できない。
- Claude実行file名、prompt、model、argvを受け取る別の新規公開関数がない。

基準目録の許可listをtest内へ手書きで隠さず、base commitからの機械生成物と現在再生成物を比較する。
repository全体の直接shell利用を防ぐ保証ではなく、「本作業が新しい迂回を増やさず、新しい入口自身が
既存汎用runnerへ接続しない」保証である。

## 11. 受入条件

- `AC-CB-001`：公開入口が§7の一つだけで、入力が目録Digestと承認IDだけに閉じている。
- `AC-CB-002`：内容指紋付き目録、二payload、各Digest、順序、ordered digestの完全一致だけが合格する。
- `AC-CB-003`：Human承認の全束縛、材料方針3項、期限、未消費状態の完全一致だけが合格する。
- `AC-CB-004`：単一の送信前検査が伏字化変化、秘密走査、Claude実行file、認証、保存先、空作業directory、
  固定argvをprocess作成直前にfail-closedで確認する。
- `AC-CB-005`：API認証、接続先上書き、repository root情報、秘密値が子processと公開出力へ伝播しない。
- `AC-CB-006`：Claudeの組込み道具、MCP、技能、plugin、hook、Chrome、別agentを利用可能にするargvを
  構成できず、repository外の空directoryでだけ起動する。
- `AC-CB-007`：一つの承認tokenでpayloadを持つprocessを最大二つ順番に実行し、1回目の不合格時は2回目を
  作成せず、自動再試行しない。payloadを持たないversion・認証確認processと件数を混同しない。
- `AC-CB-008`：承認tokenは逐次・並行の双方で一回だけclaimでき、root上書き、store欠落・別identity置換で
  再利用可能状態にならない。
- `AC-CB-009`：外側・内側の応答、session、nonce、道具不使用、終了codeが完全一致した場合だけ成功とする。
- `AC-CB-010`：raw、実行仕様、receiptをrepository外へ不変保存し、保存枠を確保できなければprocessを
  作成せず、送信後保存失敗を成功扱いしない。
- `AC-CB-011`：全停止応答は理由、payloadを持つprocess作成数、事前検査process作成数、approval状態、
  実行可能な復旧手順を単一JSONで返す。
- `AC-CB-012`：§10の基準目録比較が合格し、新経路が汎用argv実行器や別process起動入口へ接続しない。
- `AC-CB-013`：既存`reviewcompass3-pilot prepare/ingest/status`、既存egress 65 test、公式全testが回帰しない。

## 12. 禁止事項、停止条件、出力要件

### 禁止事項

- `NG-CB-001`：`tools/egress/`、既存authority、`.reviewcompass/workflow/`、既存testの期待値を変更しない。
- `NG-CB-002`：実装・完了レビュー中にClaude process、外部送信、認証操作、実model応答確認を行わない。
- `NG-CB-003`：任意prompt、任意file、repository内容、任意model、provider、binary、argv、rootを入力にしない。
- `NG-CB-004`：shell、API key、接続先上書き、Desktop、browser、MCP、plugin、hook、Claude道具、別agent、
  自動fallback、自動retryを使わない。
- `NG-CB-005`：承認tokenを`pending`へ戻さず、消費markerを別fileに作らず、store欠落時に自動初期化しない。
- `NG-CB-006`：raw応答、認証値、利用者固有の絶対pathをGit管理対象へ保存しない。
- `NG-CB-007`：本経路を実装委譲、一般のClaude対話、旧用途の外部判定へ拡張しない。

### 停止条件

- `ST-CB-001`：独立範囲レビューが`verified`以外、blocking所見がある、またはHumanが`high` riskとRED開始を
  明示承認していない。
- `ST-CB-002`：固定入力、目録、payload、順序、Claude version・Digest、公式の応答仕様のいずれかを固定
  できない。
- `ST-CB-003`：現在の認証が`claude.ai`／`firstParty`でない、未認証、追加課金やAPI keyを要求される。
- `ST-CB-004`：§9の一回性、§10の迂回検査、repository外の安全な保存をfake runnerで実証できない。
- `ST-CB-005`：受入条件を満たすために許可path外の変更、既存schemaの破壊、既存testの意味変更が必要になる。
- `ST-CB-006`：完了レビューが`verified`でない、または送信時の完全に束縛されたHuman承認がない。
- `ST-CB-007`：hostの安全審査が正規入口を拒否する。別経路へ迂回せず停止Evidenceを作る。

### 出力要件

- `OUT-CB-001`：REDでは要求IDごとのtest対応表、単独REDのcommand・exit code、基準process目録Digestを残す。
- `OUT-CB-002`：GREENでは変更全path・各Digest、対象test、既存pilot test、egress test、公式全test、
  故障注入の単独command・exit codeを残す。
- `OUT-CB-003`：CLIは成功、停止、内部失敗を区別する一行JSONをstdoutへ一つだけ返し、秘密値を含めない。
- `OUT-CB-004`：完了レビューは上流から受入条件を独立導出し、実装fixtureにない反証を最低一件作り、
  blocking所見を共通レビュープロトコルの閉じた4類型へ対応付ける。
- `OUT-CB-005`：実Runを別途承認された場合、各processのpayload Digest、raw Digest、session ID、provider、
  model、認証方式、時刻、approval ID・状態、終了code、保存結果をreceiptへ固定する。

## 13. TDDと変更可能path

Humanの`high` risk・RED開始承認後、実装担当は先にtestだけを作り、production実装が無ければ要求どおり失敗
することを単独commandのexit codeで確認する。REDを固定してから、testを弱めずproductionを実装する。

変更可能pathは次だけとする。括弧内は予定する役割であり、同名fileの存在を先に機械確認する。

- `tools/development/claude_bootstrap.py`：単一の送信前検査、承認claim、固定argv、実行、保存。
- `tools/development/claude_bootstrap_cli.py`：一行JSON応答の薄いCLI変換。
- `tools/development/pilot_collaboration_cli.py`：`bootstrap`を上記CLIへ接続する最小変更。
- `tools/development/process_call_inventory.py`：§10の決定的な構文木目録生成。
- `tools/bootstrap/immutable_result_store.py`：既存契約を壊さない接続が必要な場合の最小変更だけ。
- `tests/test_claude_bootstrap.py`：正常系と停止系。
- `tests/test_claude_bootstrap_cli.py`：CLI契約。
- `tests/test_claude_bootstrap_adversarial.py`：改竄、競合、root置換、秘密漏洩、迂回の反証。
- `tests/test_claude_bootstrap_entrypoints.py`：入口と許可path。
- `tests/fixtures/claude_bootstrap/`：外部送信しないversion固定fixture。
- `records/development/2026-08-11-claude-bootstrap-manifests/`：内容指紋付き目録、Human Decision参照、
  process基準目録、RED／GREEN Evidence。rawは置かない。
- `docs/development/prompts/claude-bootstrap-run.md`：人が発見できる共通入口。
- `docs/development/prompts/pilot-collaboration-run.md`：上記入口への一リンク。
- `pyproject.toml`：既存の`reviewcompass3-pilot`入口を維持した接続だけ。
- 本work itemのreview request、review result、Human裁定、TODO projection。

`tools/egress/`は全pathを禁止する。既存pilot acceptance testとegress testは変更せず、回帰testとして実行する。
変更可能pathを増やす必要が判明した時点で実装を止め、新しいscopeとHuman判断を要求する。

## 14. 独立レビューと意味単位

本作業は`pilot: codex`である。実装担当はCodex実装用サブエージェント、範囲と完了のレビュー担当は主担当と
反対側のモデルを使うCodexレビュー用サブエージェントを候補とする。実際の担当とモデルは開始前の機械検査で
`docs/development/pilot-specific-claude-codex-collaboration.md`の対応表へ照合する。対応modelを利用できなければ
黙って代替せず停止する。

意味単位は次の順とし、後段を前倒ししない。

1. `SCOPE`：本書、無工具段階選択record、TODO projectionをcommitする。
2. `SCOPE REVIEW`：実装を変更しない独立範囲レビューをcommitする。
3. `HUMAN RESUME`：Humanが所見の採否、`high` risk、要求、変更範囲、RED開始を裁定する。
4. `RED`：testと基準目録だけを作り、期待どおりの失敗を固定する。
5. `GREEN`：testを変更せず実装し、fake runnerだけで全受入を合格させる。
6. `COMPLETION REVIEW`：独立oracleと新作反証で実装を確認する。
7. `HUMAN SEND APPROVAL`：送信実物と一回限りtokenへ束縛した別のHuman承認を作る。
8. `REAL RUN`：正規入口から一操作だけ実行する。

本書作成時点では1だけを行う。範囲レビューの指示文も、既存の指示文品質関門を通す必要がある場合は先に
その機械処理へ接続し、合格した指示だけをレビュー担当へ渡す。

## 15. 今回の未実施

本書作成時点で次は行っていない。

- test追加、production実装、既存code変更。
- Claude Codeの認証、process作成、prompt送信、session生成。
- Anthropicその他への外部送信。
- raw、token、approval storeの作成。
- repository内容、API key、利用者情報の送信。
- `tools/egress/`、Workflow台帳、既存authorityの変更。
- 実装担当またはレビュー担当の起動。
