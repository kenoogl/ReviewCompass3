# Codex Pilot用・承認済みClaude送信経路の範囲固定 v1

- 状態：実装前の範囲固定
- 日付：2026-08-11
- collaboration_mode：`role_neutral_pilot_review`
- pilot：Codex
- reviewer：Claude
- closer：Codex
- work_item：`approved-claude-send-path`
- risk提案：`high`
- risk根拠：Human承認、秘密情報の除外、承認の一回消費、外部送信を判定・実行する守り役code
- 固定入力の出自：判断選定（Pilotが既存の出口設計、連携正本、停止Evidence、実装を選定）

## 1. Humanの指示、承認、未確定境界

Humanは次を明示承認した。

> ReviewCompass3の承認済み送信経路を通さず、Claude Code CLIからAnthropicのFableへ、
> 範囲固定record §4の非機密payload 2件だけを送信することを承認する。リポジトリ内容と
> APIキーは送信せず、Claudeの全toolを無効にする。

その試行が送信前の安全審査で停止した後、Humanは承認済み送信経路の作成可否を確認し、
作成可能であること、守り役codeと外部送信を扱うため`high` riskで進めること、実装前独立レビューと
再開承認を置くことの説明に対して「進めて」と指示した。

本指示により、この範囲固定recordの作成と独立範囲レビューの依頼までは承認済みとする。
`high` riskの実装開始は、Claudeによる範囲レビュー結果をHumanが確認し、riskと再開を明示承認するまで
未承認とする。実送信は、実装の独立完了レビューが`verified`となり、§4のpayload list digestに
束縛した有効なHuman承認recordを送信時に機械検証できる場合だけ実施する。

## 2. 開始状態

- base commit：`7f58333aa5bc1f275f59bc672fc1f0722fc813da`
- branch：`main`
- worktree：clean
- Claude Code version：`2.1.220`
- Claude Code executable SHA-256：
  `8addc857f3fe64d5a0368af9ee50321b50afb4a6918ba3ef018ab84f5dbbe081`
- installer script SHA-256：
  `cde4f1702d3b1695f92b73d26888364e17bca476e17f0fd676484c951d36c125`
- 認証実測：API key等を子process環境から除外した通常環境で`loggedIn: true`、
  `authMethod: claude.ai`、`apiProvider: firstParty`
- 前回試行：Claude Codeのprocess作成前に安全審査で停止し、外部送信、Claude session生成、
  repository変更はいずれも0件

## 3. 固定入力

| identity | version | repository-relative path | SHA-256 |
| --- | --- | --- | --- |
| role-neutral Pilot／Review連携 | 試行版 | `docs/development/role-neutral-pilot-review-collaboration.md` | `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e` |
| 作業レビュープロトコル | 運用メモ | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| Initial Development Checklist | 現行 | `docs/development/2026-08-03-initial-development-checklist.md` | `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c` |
| 現行TODO | 現行 | `TODO_NEXT_SESSION.md` | `c361baee7b84de372383249534e1890deb06638931e455006b35ae9eae59bc77` |
| 外部送信の出口設計 | v4 | `docs/design/2026-08-07-external-egress-gate-proposal-v4.md` | `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd` |
| 旧用途の出口方式Decision | v1 | `records/development/2026-08-08-egress-method-conclusion-decision-v1.md` | `d9228be3ec17db82fbed694e7a6bf05b8a5d6fae52ff2353aad39aeac27dc6fc` |
| 先行するClaude疎通範囲 | v1 | `records/session-handoffs/2026-08-11-codex-pilot-claude-session-bootstrap-scope-v1.md` | `3aa8a86e014b4513fe2426e94f53348998544293d877df3effca2d96d9c35c39` |
| 先行試行の停止Evidence | v1 | `records/development/2026-08-11-codex-pilot-claude-session-bootstrap-blocked-evidence-v1.md` | `ee222ca69b86a3fc5100c8b1bac5237fb8c69a75d6212e0f6a3727625431302b` |
| 既存承認検証 | 現行 | `tools/egress/approval.py` | `cb8f97e1d2b05f0ec7e9bad9e045c80b8378a03167be2d623f13853c3236b243` |
| 既存出口関門 | 現行 | `tools/egress/gate.py` | `ec611dfa65c0ff8f8ccf586ed491e944430cf80952a797861ea3b06a7f1de0c1` |
| 既存段階1 sender | 現行 | `tools/egress/sender.py` | `05286fe21ee5baf264c80fe8518eccef3602de1c7ada6041e121dd4a2b5bbef8` |
| 既存旧用途payload | 現行 | `tools/egress/payload.py` | `daeb48b1ef3c00f7ae14ba1debfaba7efe564387808e505d57e4c15a14d34a1f` |
| raw応答の不変保存 | 現行 | `tools/bootstrap/raw_review_store.py` | `32f4202e82d2971ff936773e509e80a520052bd54187205d6863b9edda1559af` |
| project-first runtime配置 | 現行 | `tools/layout/baseline.py` | `6d00c3053da820cd694a0c4b47d5e5f1b632f00d83e81691f99060626bc94cb7` |

固定入力のDigestが独立範囲レビュー前に不一致ならレビューを開始しない。範囲レビュー後、RED開始前に
不一致となった場合は本scopeをstaleとして停止する。

## 4. 新用途と固定payload

本作業は出口設計v4 §8が実送信の前提とした「段階4の別提案」に相当する。ただし、旧用途
`implementation_sameness_judgment`を再開せず、新用途`claude_session_bootstrap`だけを追加する。
既存の`EgressPayload`、既存の質問template、旧用途のHuman Decision、段階1 senderを緩和、転用、
または実送信可能に変更しない。

payload 1は次の1行のUTF-8文字列に固定する。末尾改行はpayloadに含めない。

```text
あなたはClaude Reviewerです。Codex Pilotからの疎通確認です。ツールを使わず、他のエージェントを起動せず、次のJSONだけを返してください。{"protocol":"codex-pilot-claude-bootstrap-v1","role":"reviewer","nonce":"RC3-CPC-20260811-A","reinvoke":false}
```

- SHA-256：`18059aa0f32b93bae5b117092a45fbf4e985381546b8c64507168f0226f4ad64`

payload 2は次の1行のUTF-8文字列に固定する。末尾改行はpayloadに含めない。

```text
同じセッションの継続確認です。前回のnonceを使い、次のJSONだけを返してください。{"protocol":"codex-pilot-claude-bootstrap-v1","continued":true,"nonce":"<前回のnonce>","reinvoke":false}
```

- SHA-256：`c2309f2624ba0d0f36fd00894dcbc67ccd66e83429960c4083f4e10b2f18982a`

上記順序のDigest列を既存`payload_list_digest`と同じ規則で計算した値は
`967e9410e0cf3bb722fca084b7ffa91b1d282c6f02674843362bd6893a25bf89`である。
送信時のHuman承認はこのlist digest、purpose、provider、model、期限へ束縛する。

providerはClaude Code CLIのfirst-party接続を表す固定識別子、modelは`fable`とする。providerの
識別子文字列は実装前独立レビューで既存命名規則との整合を確認し、Human承認recordの作成前に一つへ
固定する。識別子変更を承認済み送信先の変更に使ってはならない。

## 5. 今回の最小E2E

1. content-addressedな目録から§4の2 payloadだけを読み、Digest、順序、list digestを検証する。
2. Human承認recordをpurpose、provider、model、payload list digest、期限、未消費状態まで検証する。
3. Claude executableのversionとDigest、`claude.ai`／`firstParty`認証、送信先modelを検証する。
4. 一回限りの承認を排他的かつfail-closedに消費し、receipt保存先を確保する。
5. API認証・接続先上書きの環境変数を子processから除外し、Claudeの全tool、MCP、slash command、
   Chrome連携を無効にした構造化argvでpayload 1を送る。
6. 応答、終了code、tool不使用、protocol、role、nonce、`reinvoke:false`を検証してrawを不変保存する。
7. 同じClaude session IDだけをresumeしてpayload 2を送り、`continued:true`、同じnonce、
   `reinvoke:false`を検証してrawを不変保存する。
8. 2送信の正確なpayload Digest、raw Digest、session ID、provider、model、認証方式、時刻、
   approval identity、承認消費結果、各終了codeをreceiptへ固定する。

一つのHuman承認はこの2送信を順番に行う一つの操作だけに対応する。payload 1が失敗または不一致なら
payload 2を開始しない。process作成後の失敗、無応答、保存失敗を含め、自動再試行しない。
承認は送信前に消費済みへ確定し、失敗時も未消費へ戻さない。再実行には新しいHuman承認を要求する。

## 6. 安全境界

### 6.1 実行時検証

- Claude executableはversion `2.1.220`かつ§2のSHA-256と一致させる。実行時pathはcaller入力とし、
  user固有の絶対pathをrepositoryへ保存しない。
- 子process環境から少なくとも`ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、
  `ANTHROPIC_BASE_URL`、`CLAUDE_CODE_OAUTH_TOKEN`を除外する。値はlog、error、receiptへ出力しない。
- 送信前auth statusは`loggedIn: true`、`authMethod: claude.ai`、`apiProvider: firstParty`以外を拒否する。
- Claude起動argvには`--print`、`--safe-mode`、`--tools ""`、`--disallowedTools "*"`、
  `--strict-mcp-config`、`--disable-slash-commands`、`--no-chrome`、`--max-turns 1`、
  `--output-format json`と、固定model／session引数だけを許す。
- shell、文字列command、PATH探索、stdin以外の動的payload、任意の追加引数、任意環境変数上書き、
  hook／plugin／project設定を有効化する引数を禁止する。
- session IDは実装が新規UUIDとして生成し、2回目はその同一値だけをresumeする。callerが既存sessionを
  指定する経路を作らない。
- 応答はClaude CLI JSON envelopeと固定JSON本文を機械解析する。tool use、追加turn、session不一致、
  schema外field、nonce不一致を拒否する。

### 6.2 承認、保存、復旧

- 承認recordはHumanが明示作成したnew-onlyの機械可読recordとし、対象identityとlist digestを持つ。
- 承認claim、消費、送信の競合を一つの排他境界で扱う。同一承認の並行実行は一方だけが送信可能とする。
- 送信前に消費済みmarkerとattempt用directoryを原子的に確保できない場合、外部processを作成しない。
- stateとraw応答は`tools/layout/baseline.py`のproject-first runtime解決を使う。承認消費markerとreceiptは
  development profileの`STATE_ROOT`、raw応答は`SENSITIVE_ROOT`へ置く。要求したrootだけを作成する。
- raw応答の不変保存は`tools/bootstrap/raw_review_store.py`を再利用する。既存保存処理を複製しない。
- 応答raw、session transcript、auth出力をGit管理対象へ入れない。
- 送信後の保存失敗では承認を消費済みのまま保ち、残存するprocess結果とstateから
  `reported_unverified`としてHumanへ停止報告する。重複送信で証跡を補わない。
- timeoutまたは無応答はfail-closedで停止し、Humanへ非応答escalationを出す。別model、API、Desktop、
  Human中継へ自動fallbackしない。

## 7. 受入条件

1. §4以外の自由文、payload、file、stdin、repository内容を外部送信できない。
2. purpose、provider、model、2 payloadの各Digest、順序、list digest、期限、Human承認のいずれかが
   不一致ならClaude processを作成しない。
3. executable version／Digestまたは`claude.ai`／`firstParty`認証が不一致なら送信しない。
4. API key等の値が子process環境、stdout、stderr、exception、receiptへ伝播しない。
5. Claudeのtool、MCP、slash command、Chrome連携、別agent起動を可能にするargvを構成できない。
6. §5の2送信だけが同一の新規sessionで順番に行われ、1回目の不合格時は2回目が0件となる。
7. 承認は並行実行を含め一回だけ消費でき、送信開始後の失敗でも再利用できない。
8. 2つの応答が固定schema、protocol、nonce、session、tool不使用条件を満たさない限り成功receiptを作らない。
9. raw応答は`SENSITIVE_ROOT`へ不変保存され、Git管理対象に出現しない。receiptだけでpayloadとrawのDigest、
   provider、model、時刻、approval、session、終了状態を追跡できる。
10. 既存の旧用途payload、出口関門、段階1 sender、旧Decisionの意味と挙動が変わらず、既存testが合格する。
11. actual outbound processを作成できるproduction moduleは今回のtrusted入口一つだけであり、ASTまたは
    module inventoryの独立検査で他の迂回経路がないことを確認できる。
12. command入口はcontent-addressedな固定目録とHuman承認recordだけを受け取り、自由文、任意file、
    任意model、任意追加引数をCLI optionとして受け取らない。

## 8. 変更可能path

範囲レビュー合格後のPilotは、次のpathだけを新規作成または必要最小限で変更できる。

- `tools/egress/claude_session.py`：固定payload目録、応答、session、receiptの型と純粋検証
- `tools/egress/trusted_claude_send.py`：唯一の実process起動、環境除外、承認消費、保存の統合入口
- `tools/egress/approval.py`：新purposeと二送信一操作のfail-closedな一回消費に必要な最小変更だけ
- `tests/test_trusted_claude_send.py`：正常系、停止系、RED／GREEN
- `tests/test_trusted_claude_send_adversarial.py`：秘密情報、改竄、競合、迂回の反証
- `records/development/2026-08-11-approved-claude-send-path/`：固定payload目録、payload、Human承認、
  RED／GREEN／実RunのEvidenceとreceipt参照
- `records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-review-request-v1.md`
- reviewerが作る範囲レビューおよび完了レビューの同work item handoff record

実装中に既存approval schemaの互換性を保ったまま§7を満たせない場合、既存schemaを拡張せず、
Claude専用approval moduleを新規pathとして提案する新scopeへ改版してHuman判断を得る。

## 9. 禁止path、禁止操作、未実施範囲

禁止pathは§8以外の全pathとする。特に次を変更しない。

- `docs/design/2026-08-07-external-egress-gate-proposal-v4.md`
- `records/development/2026-08-08-egress-method-conclusion-decision-v1.md`
- `tools/egress/payload.py`
- `tools/egress/gate.py`
- `tools/egress/sender.py`
- `.reviewcompass/workflow/`配下
- `TODO_NEXT_SESSION.md`およびInitial Development Checklist

禁止操作：範囲レビュー前のtest／実装、完了レビュー前の実送信、承認なしの再送、直接Claude CLI、
別shell／Desktop／API／UI経路、payloadの追加・編集、providerまたはmodelのfallback、repository内容の
送信、API keyの使用・表示・保存、hook／plugin／MCP／Claude toolの有効化、既存承認の再利用、
push、履歴書換え、sandboxまたはhost安全審査の迂回。

今回実施しない範囲：一般用途の外部送信、任意promptによる継続対話、実作業のClaude委譲、
ClaudeからCodexの再起動、課金方式の比較、既存authorityの恒久改定、旧用途scene 1の再開、
別provider／model対応、安定版への昇格、TODO／checklistの段完了projection。

## 10. TDD、検証、独立oracle

範囲レビューとHuman再開承認後、振る舞いを変える前にtestを追加し、実装がなければ失敗することを
単独commandのexit codeで確認する。Testを弱めずに実装を進め、対象test、全egress test、全testを
それぞれ単独commandで合格確認する。実装変更と無関係な既存testの書換えを行わない。

最低限のRED／GREEN宣言は次とする。

- exact 2 payload、各Digest、順序、list digestだけが通る
- 自由文、任意file、改竄、追加payload、model／provider差替えをprocess作成前に拒否する
- auth、binary version／Digest、承認、期限、消費状態の不一致をprocess作成前に拒否する
- child environmentからAPI認証・接続先変数を除き、秘密値を全出力から除外する
- 固定no-tool argvを構造化引数で実行し、shellと動的追加引数を使わない
- 応答schema、nonce、session、tool use、終了code、timeoutをfail-closedに扱う
- 1回目の失敗が2回目を停止し、自動retryしない
- 同一承認の逐次再利用と並行競合の双方で外部process作成が合計1操作以下となる
- state／sensitive保存が送信前に利用不能なら送信しない。送信後保存失敗は成功扱いにしない
- productionのactual outbound process起動箇所がtrusted入口一つだけである
- 既存egress挙動に回帰がない

`high`の完了レビューでは、Reviewerが上流authorityから受入条件を独立導出し、Pilotのfixtureにない
反証を最低1件新作して機械実行する。誤った合格の反証は、payload表現差、承認競合、環境変数漏洩、
session差替え、process起動箇所の増加を優先候補とする。Claude自身への実送信を反証目的で重複実行せず、
fake runnerと保存先fixtureで守り役codeを検証する。

## 11. 停止条件

- 独立範囲レビューが`verified`以外、またはblocking Findingがある
- Humanが`high` riskとRED開始を明示承認していない
- 固定入力、payload、binary、approvalのidentityまたはDigestが不一致
- 受入条件を満たすために§8外の変更、既存schemaの互換性破壊、既存testの意味変更が必要
- Claude CLIのflagまたはFableのmodel指定が実測と一致せず、安全設定を固定できない
- `claude.ai`／`firstParty`認証を確認できない、追加課金またはAPI keyを要求される
- raw／stateの安全な保存、排他的な一回消費、非応答停止のいずれかを実装・検証できない
- 完了レビューが`verified`になる前、または送信時Human承認を機械検証できない
- host安全審査が承認済みtrusted入口として認識せず、process作成前に拒否する
- repositoryに範囲外変更または既存利用者差分が生じる

停止時は別経路へ迂回せず、事象、終了code、外部process作成数、承認消費状態、未実施範囲をEvidenceへ
固定してHumanへ返す。

## 12. 意味単位のcommit境界

1. `SCOPE`：本recordだけを単独commitし、Claudeの独立範囲レビューへ渡して停止する。
2. `SCOPE REVIEW`：Claudeが上流authorityから独立導出し、範囲レビューrecordだけを単独commitして停止する。
3. `RED`：Humanのrisk・再開承認後、失敗するtestとRED Evidenceを意味単位commitする。
4. `GREEN`：testを変更せず実装し、GREEN Evidenceと実装を意味単位commitする。
5. `REVIEW REQUEST`：PilotのClaimとEvidenceを固定したreview requestだけを単独commitして停止する。
6. `COMPLETION REVIEW`：Claudeが独立oracleと新作反証を実行し、review resultだけを単独commitして停止する。
7. `REAL RUN`：Human承認recordを機械検証し、trusted入口から§5の一操作だけを実行する。rawはruntimeへ、
   Git管理するEvidenceが必要なら秘密を含まないreceipt参照だけを別commitに固定する。

範囲変更、blocking Finding、設計変更、test前提変更が生じた場合は既存recordを編集せず、次versionの
scopeを新規commitしてHuman判断へ戻す。
