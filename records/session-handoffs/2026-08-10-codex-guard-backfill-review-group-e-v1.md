# 守り役後追い独立レビュー #6第2単位 group E 判定 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：implementation（既存の守り役codeに対する後追いレビュー）
- 本作業単位のrisk：`low`（Human確定済み）
- 対象codeの既定risk：`high`（承認関門、外部送信、機微情報、改変拒否を扱うため）
- 総合判定：`reported_unverified`
- Finding：blocking 7件、non-blocking 0件、defer 0件

## 1. 固定対象と開始状態

- 範囲固定：
  `records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-high-reviews-scope-v1.md`
  （commit `bedf986408156e661c4a15c6886a4e9558d514ec`、SHA-256
  `6b587a7eedf77380aadf5b41ab90edd148bdcd6f69b850447dc684591737f8e9`）
- 判定基準：`docs/development/work-review-protocol.md` §3、§4.7、§11
- Human承認：2026-08-10「#6第2単位 risk lowを確定、着手を承認する」
- 許可範囲：指定のgroup E判定record 1件の新規作成と単独commit、読取り、
  一時領域での反証
- 禁止範囲：code、test、既存record、実ログ、実設定、repository内既存fileの変更、
  実際の外部送信、Findingの修正、TODO反映、push、履歴書換え
- 停止条件：固定入力Digest不一致、許可path外の変更が必要、外部操作が必要

【実測】開始branchは`main`、開始HEADは
`e0e5d3343460a8a1793a41b62a21503323009d63`、開始時の
`git status --short`は出力なしだった。範囲固定後のcommit列はgroup A〜Dの判定record
4件だけであり、`git diff --name-status bedf986..HEAD`も次の4件の追加だけだった。

- `17613d26b9b334934a5d717b1954ab573d320043`：group A
- `46f246525c4a2714d5067e45e048ff47e72ea150`：group B
- `f02c32cb74263a6db60b3eac8144ce2adcde0c66`：group C
- `e0e5d3343460a8a1793a41b62a21503323009d63`：group D

【実測】固定入力のSHA-256を内容から再計算し、範囲固定record §3の値と全件一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| Human裁定 | `d73f51a17ef20fa6a5abb531c30119384582cec9c299102e518088e3bb51afa7` |
| 対象一覧 | `77b6ba9fc0bfd7ea17e071dc4e4df59e12f84f4a7d23798dedafe58b6ea6571e` |
| 共通レビュー基準 | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| `TODO_NEXT_SESSION.md` | `6de9d6d8b4f0ebc93f59e7fbe1ee6e192f5aba27e7b94e4e5dfe673e65b6205a` |

【実測】確定pathへの`git check-ignore --no-index`は終了コード1で、ignore対象外だった。
作成前の`test ! -e`は終了コード0で、同名fileが存在しないnew-only状態だった。

## 2. 実装、上流、既存testの読取り

【実測】対象7 module、直接・関連test、出口設計v4、出口設計Human判断Decision、
段階1 GREEN Evidence、Session Logの上流Requirementと既存完了Evidenceを再読込みした。
対象moduleのSHA-256は次のとおり。

- `docs/design/2026-08-07-external-egress-gate-proposal-v4.md`
- `records/development/2026-08-07-egress-gate-v3-judgments-decision-v1.md`
- `records/development/2026-08-07-egress-stage1-green-evidence-v1.md`
- `records/requirements/definitions/req-session-002--v1.json`
- `records/requirements/definitions/req-portable-004--v1.json`
- `records/development/2026-08-03-session-transcript-source-formats-completion-evidence-v1.md`

| 対象 | SHA-256 |
| --- | --- |
| `tools/egress/approval.py` | `40ccdf83cfad4008dfdf574dde63ca8b255f26ee22842f0611a4e125cc868693` |
| `tools/egress/gate.py` | `98a8626a9decfbfebedf880de9854b07c5ed1dd267a8f99ccae0ff6071b953a1` |
| `tools/egress/payload.py` | `979543576982440221bc6b9887f49c6ccab1b5d7a3d14bf85d415df1801971ab` |
| `tools/egress/prefilter.py` | `90fb298a38e0f7ea5dfd205cf99f05bf5122b514bda338007b2f84e751a7ce8e` |
| `tools/egress/sender.py` | `c8f58564a65f840f2b6f7f22d2cdc974557528d623dc53ec593c288e7b176992` |
| `tools/session_logs/preservation.py` | `1bf5b19e0a75b162945ef82424e6905de8684f675149fb42fd175fcfc4d75bf9` |
| `tools/session_logs/private_validation.py` | `b06ac88722c79cb3671d9aa5a46188a118a5c8ec4250e2e36103214d499481fc` |

【実測】直接・関連testとして次を読んだ。

- `tests/test_egress_approval.py`
- `tests/test_egress_gate.py`
- `tests/test_egress_payload.py`
- `tests/test_egress_prefilter.py`
- `tests/test_egress_dry_run.py`
- `tests/test_egress_adversarial.py`
- `tests/test_session_log_preservation.py`
- `tests/test_session_log_private_validation.py`

【記録】出口設計v4は、Humanが送信物の実物一覧を目視し、見た物、承認した物、
送られる物を一字単位で一致させる。送信可能な材料はsource行から機械切出ししたcode断片、
許可一覧にある数値・列挙値、承認済み定型文の3種だけである。承認recordの実在とpayloadの
結線、現在時刻での有効期限、秘密値走査、送信直前関門の単一実装も必須である。

【記録】同設計は、事前分類の閾値0.85／0.45と重み0.6／0.2／0.2の変更を
Human承認事項とする。段階1〜3は実際の送信を承認せず、段階1の送信係は関門合格後も
送信不能でなければならない。

【記録】Session Logの上流Requirementは、生ログ原本を共有隔離保存境界で保全し、
改変を検出すること、値を含まない診断を通常の機微値と分離することを求める。

【実測】既存testは、承認recordの各値の一項目差替え、通常のpayload改変、上位fieldの追加、
通常のsource変更、既知4形式の秘密値・個人識別子、閾値の通常値override、送信係の最終例外、
非追記source変更、復元直前のbackup単独改変、通常の値なし出力を覆う。一方、今回試した
承認record自体の偽造、`consumed`欠落、比較時刻の逆行、型fieldと送信JSONの分離、
入れ子fieldへの自由文混入、別形式の資格情報、非有限閾値、伏字化callbackの副作用、
保全処理を挟んだ改変の正当化、raw／backup rootのsymlink脱出、機微値をpathと本文の両方へ
入れる値漏えい反証は既存fixtureになかった。

## 3. 既存testと公式全Testの独立再実行

【実測】次の単独commandは終了コード0、`73 passed in 0.19s`だった。

```text
env PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS=-p\ no:cacheprovider .venv/bin/python3 -m pytest -q tests/test_egress_approval.py tests/test_egress_gate.py tests/test_egress_payload.py tests/test_egress_prefilter.py tests/test_egress_dry_run.py tests/test_egress_adversarial.py tests/test_session_log_preservation.py tests/test_session_log_private_validation.py
```

【実測】公式全Testは、元repositoryへ書かないため一時領域
`/private/tmp/codex-group-e-full-tree-v1`へ`git clone --no-hardlinks`で複製した。
複製内の`.venv/`だけを元環境の`bin`、`include`、`lib`、`pyvenv.cfg`へのsymlinkで
構成した。実行前後の複製側`git status --short --branch`はbranch行だけで、tracked・
untracked差分はなかった。対象7 moduleのDigestは元repositoryと一致した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/codex-group-e-official-isolated-receipt-v1.json
```

【実測】終了コード0、status `passed`、`1381 passed`、failed 0、errors 0、
skip・xfail・xpass 0、Python 3.9.6、pytest 8.4.2、fallback falseだった。
receipt SHA-256は
`35c513cc03b5fa5854c8bc74ab8f3bbae44c03fb405908ec3b1b27f869421826`である。

## 4. 既存fixtureにない反証

### 4.1 実行環境と終了コードの意味

【実測】反証はPython 3.9.6、pytest 8.4.2、
`macOS-26.5.1-arm64-arm-64bit`で実行した。反証を自動実行する一時scriptは
`/private/tmp/codex_group_e_adversarial.py`だけに置き、SHA-256は
`7906a65a20cb70ee56640ee01165927faa879d07bc8d96fbdac0309aa78c7c79`だった。
各source、承認入力、marker、Git repository、生ログ、backup、台帳、証拠fileは
caseごとの`TemporaryDirectory(dir="/private/tmp")`だけに作成し、case終了時に消去した。

【実測】反証scriptと`tools/egress/`に`socket`、HTTP client、URL取得、送信APIの
import・呼出しはなかった。`sender_callback_side_effect`は外部送信の代わりに、一時markerへの
書込みだけで任意の副作用が停止前に実行されることを確認した。実際の外部送信は行っていない。

以下の終了コード1はscript異常ではない。「偽造、混入、境界脱出、副作用を安全側で拒否する」
という独立判定に反して対象moduleが受理したことを表す。終了コード0は反証を拒否した、または
値を漏らさず安全側の期待を満たしたことを表す。

### 4.2 反証の実行一覧

各commandの`<case>`は、共通command末尾のcase名である。

```text
env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_e_adversarial.py <case>
```

| ID | `<case>` | 結果 | 終了コード |
| --- | --- | --- | --- |
| A1 | `approval_forged_record` | 永続record pathもHuman receiptもない辞書が承認済みとして合格 | `1` |
| A2 | `approval_missing_consumed` | 一回性を表す`consumed`が欠落しても合格 | `1` |
| A3 | `approval_backdated_now` | 2026-08-10時点で期限切れのrecordが、caller指定の過去時刻では合格 | `1` |
| P1 | `payload_detached_fragment` | sourceと異なる`CodeFragment.content`が、元のDigest fieldを残すと由来検証に合格 | `1` |
| G1 | `gate_nested_fragment_smuggling` | JSON内`fragment_a`を自由文だけの辞書へ置換しても関門が`allowed=true` | `1` |
| G2 | `gate_allowlisted_key_text_smuggling` | 許可field名`line_count`の値を自由文へ置換しても関門が`allowed=true` | `1` |
| G3 | `gate_secret_format_miss` | 合成AWS access key、GitHub token、PEM秘密鍵headerを走査0件で見逃し、関門が`allowed=true` | `1` |
| F1 | `prefilter_nonfinite_policy` | 本文・名前・特徴が同一の組を、NaN重みで`ambiguous`へ分類 | `1` |
| S1 | `sender_callback_side_effect` | 送信不可例外の前に、注入した伏字化callbackが一時markerを書込 | `1` |
| R1 | `preservation_ledger_launder` | backup改変後の再保全が台帳を改変値へ更新し、その値を正当な復元元として復元 | `1` |
| R2 | `preservation_symlink_escape` | raw root外を読取り、backup root外へ書込む2種のsymlink脱出が成立 | `1` |
| V1 | `private_validation_value_probe` | 機微値をraw root名と本文へ入れてもEvidence・標準出力へ漏れず、status `passed` | `0` |

### 4.3 代表的な機械出力

【実測】A1〜A3は、Human由来の証拠なし、必須field欠落、期限切れをそれぞれ持つ入力を
受理した。

```json
{"accepted": true, "case": "approval_forged_record", "durable_record_path_supplied": false, "human_receipt_supplied": false}
{"accepted": true, "case": "approval_missing_consumed", "consumed_present": false}
{"accepted": true, "actually_expired_at_review_time": true, "case": "approval_backdated_now", "supplied_now": "2026-08-07T12:00:00+09:00"}
```

【実測】P1、G1、G2は、dataclass（項目を固定した構造体）のfieldと送信JSON本文を分離すると、
source外文字列と数値fieldに見せかけた自由文を受理した。

```json
{"accepted": true, "case": "payload_detached_fragment", "content_matches_source": false, "digest_field_unchanged": true}
{"allowed": true, "case": "gate_nested_fragment_smuggling", "reasons": []}
{"allowed": true, "case": "gate_allowlisted_key_text_smuggling", "reasons": []}
```

【実測】R1では、改変backupを検出せず`action=preserved`としてそのDigestを台帳へ書き、
source削除後の復元で改変値を復元した。

```json
{"case": "preservation_ledger_launder", "ledger_rewritten_to_tamper": true, "preserve_action_after_tamper": "preserved", "restore_action": "restored", "restored_tampered_value": true}
```

【実測】V1は、1件のClaude形式rawを合格させ、出力は固定件数と状態だけで、入力値を含まなかった。

```json
{"case": "private_validation_value_probe", "cli_exit": 0, "counts": {"claude": 1, "codex_exec_json": 0, "codex_rollout": 0, "failed": 0, "ignored": 0, "unsupported": 0}, "marker_leaked": false, "status": "passed"}
```

### 4.4 反証作成時の手戻り

【実測】最初のG1、G2、G3、S1では、安全な合成payload自体が電話番号検出で拒否された。
対象操作は構造混入・秘密値見逃し・callback副作用の反証、期待executorと実executorはいずれも
同じ一時scriptだった。調査commandは、code断片のSHA-256内の数字列
`6414070778863`を電話番号として検出していることを終了コード0で示した。これは対象反証へ
到達する前の、走査器による別の誤拒否だった。

【判断】手作業理由は、狙った境界だけを独立に評価するためである。一時scriptを、両code断片の
Digestが変わるsaltを機械生成し、基準payloadの走査結果が0件のものだけを使う形へ直した。
修正後のG1〜G3、S1を上表の最終Evidenceとした。元repositoryは変更していない。

【実測】V1の最初のmarker名はpipeline側で失敗入力に分類されたため、値なし失敗経路しか
確認できなかった。成功経路の出力も確認するため、機微性を保つ中立な固有文字列
`ZqxjVioletMarblePhrase`へ変え、CLI終了コード0・status `passed`で漏えい0を再確認した。

【提案】同種の反証を反復する場合、既知走査に偶然一致しない基準payloadと、成功・失敗の
両経路を作るfixture生成を一時harness側で決定的に行う。routeは本レビュー内の一時harness修正で
完了しており、製品codeの改善候補にはしていない。

## 5. moduleごとの判定（§4.7）

| module | 判定 | Evidenceと理由 |
| --- | --- | --- |
| `tools/egress/approval.py` | `reported_unverified` | 通常の一項目差替えは拒否したが、A1〜A3でHuman由来のないrecord、`consumed`欠落、過去時刻指定を合格させ、G3で3種の資格情報形式を見逃した。F-E1・F-E3により`verified`にできない |
| `tools/egress/gate.py` | `reported_unverified` | 通常の上位field追加とdigest不一致は拒否したが、G1・G2でJSON内の入れ子構造・値型の偽装を合格させ、G3で資格情報を含む送信物を`allowed=true`にした。F-E2・F-E3により`verified`にできない |
| `tools/egress/payload.py` | `reported_unverified` | builderの通常出力は3種だけだったが、P1でsourceと異なる断片本文を由来検証が合格させた。F-E2により`verified`にできない |
| `tools/egress/prefilter.py` | `reported_unverified` | 既定閾値と通常3帯分類は既存testどおりだったが、F1で非有限値を拒否せず同一組を曖昧帯へ移した。F-E4により`verified`にできない |
| `tools/egress/sender.py` | `reported_unverified` | 関門合格後は既存testどおり送信不可例外になったが、S1でその停止前に任意callbackの副作用が実行された。F-E5により`verified`にできない |
| `tools/session_logs/preservation.py` | `reported_unverified` | 通常の追記、非追記変更の保全、復元直前の単独改変拒否は合格したが、R1で保全処理が改変を台帳へ正当化し、R2でroot外読書きが成立した。F-E6・F-E7により`verified`にできない |
| `tools/session_logs/private_validation.py` | `verified` | 既存testとV1が合格し、repository外の明示ログ1件について、本文・raw root名の固有値をEvidenceとCLI出力へ漏らさず、repositoryのGit状態を変えなかった。今回の範囲で反証成立なし |

【判断】6 moduleにblocking Findingが対応するため、group Eの総合判定は
`reported_unverified`である。§6が定める再現条件不足ではなく、§11.1類型1〜4の機械反証を
根拠とする。固定された完了報告と事後状態の競合はないため`report_execution_mismatch`ではない。
範囲固定§8.3はblocking検出を停止条件にせずrecordへ固定してgroupを完了させるため、
`blocked`でもない。

## 6. Finding（§11）

### F-E1 blocking／implementation／§11.1類型2・3・4

対象：`tools/egress/approval.py`、`tools/egress/gate.py`、`tools/egress/sender.py`

【実測】A1では、永続record path、Human receipt、署名のいずれもない一時辞書へ
`approved_by: user`等を書くだけで承認検証が合格した。実装の公開呼出し列を検索した結果、
gateとstage-one runnerはこの辞書を直接受け取り、Humanが作ったrecord fileの読込み、file identity、
Digest、receiptへ束縛する経路はなかった。

【実測】A2では一回性を表す`consumed`を削除しても、`record.get("consumed") is True`ではないため
未消費として合格した。A3では、レビュー日時点で期限切れのrecordも、callerが過去の`now`を渡すと
合格した。stage-one runnerも`now`をcallerから受け取る。

【記録】出口設計v4 §4はHumanによる実物一覧承認と一回性を要求し、§5条件5はHuman承認recordの
実在とpayloadとの結線を要求する。有効期限も7照合項目の一つである。

【判断】Human由来のない辞書を承認と扱うため類型2、必要field欠落・期限切れを誤って合格させるため
類型3、承認recordの実在・schema・時刻境界を破るため類型4のblockingとする。Human identity、
一回性、時間軸の同類型を本周回で一括確認した。

### F-E2 blocking／implementation／§11.1類型3・4

対象：`tools/egress/payload.py`、`tools/egress/gate.py`

【実測】P1では、`CodeFragment.content`だけをsource外文字列へ変え、
`content_sha256`を元sourceのまま残すと、`verify_fragment_provenance`が合格した。G1では、
EgressPayload側の安全なfragment fieldを残したまま、実際に送るJSONの`fragment_a`を
`{"free_text": ...}`へ置換し、本文Digestと承認一覧を自己整合させると関門が合格した。
G2では、JSONの許可field名`line_count`の値を整数でなく自由文にしても合格した。

【記録】出口設計v4 §3・§5条件1〜2は、送信物をsource行からのcode断片、許可された数値・列挙値、
定型文の3種だけに閉じ、code断片の由来を現在sourceへ解決することを要求する。

【判断】由来検証が断片本文を再切出し結果へ結ばず、gateが送信JSONの入れ子schemaと
EgressPayloadのfieldを相互照合しない。このためsource外自由文と型偽装を3種構成として
誤って合格させる類型3、payload schema・source行範囲境界を破る類型4のblockingとする。
code断片、機械特徴量の2種を同じ周回で確認した。

### F-E3 blocking／implementation／§11.1類型3

対象：`tools/egress/approval.py`、`tools/egress/gate.py`

【実測】G3では実在しない合成値だけを用い、AWS access key形式、GitHub token形式、
PEM秘密鍵headerの3変種をcode断片へ入れた。`scan_outbound_text`は0件を返し、他条件を満たした
gateは`allowed=true`を返した。

【実測】反対方向では、秘密値・個人識別子のない通常payload内のSHA-256に偶然含まれた13桁の
数字列を電話番号として検出し、gateが拒否した。既存の正例はこのDigest表現を踏んでいなかった。

【記録】出口設計v4 §4の材料方針は秘密値走査を必須、資格情報と個人識別子を禁止し、§5は
全条件合格時だけ送信を許す。

【判断】代表的な資格情報3形式を誤って安全とし、構造上不可避なDigest文字列を個人識別子と
誤認し得る。秘密値走査の偽陰性と偽陽性を機械実証した類型3のblockingとする。

### F-E4 blocking／implementation／§11.1類型1・3

対象：`tools/egress/prefilter.py`

【実測】F1では、`body_weight=NaN`を持つ`Thresholds`を渡すと、本文、名前、特徴が全て同一の組でも
合成類似度がNaNになった。Pythonの比較は`>= same_min`と`<= diff_max`の双方をfalseにし、結果は
`ambiguous`になった。閾値・重みの有限性、範囲、合計、大小関係を検証する処理はなかった。

【記録】出口設計v4 §3.1とHuman Decisionは、閾値と重みを承認済み初期値へ固定し、変更を
Human承認事項とする。

【判断】Human承認のない非有限値で既定分類を迂回できるため類型1、同一組を送信候補帯へ
誤分類するため類型3のblockingとする。将来の閾値設計は提案せず、現行固定値の検証だけを扱う。

### F-E5 blocking／implementation／§11.1類型4

対象：`tools/egress/gate.py`、`tools/egress/sender.py`

【実測】S1では、`redaction_hook`へ一時markerを書いて入力をそのまま返すcallbackを渡した。
stage-one runnerはcallbackを実行してmarkerを作った後、`EgressSendingNotApproved`で停止した。
hookのidentity、許可実装、無副作用性を検証する処理はなかった。

【記録】出口設計v4 §8が承認した段階1は実際の送信機能を持たず、GREEN Evidenceは
「送信は型として不可能」と報告する。伏字化は適用対象だが、合格の根拠にはしない。

【判断】停止例外より前にcaller注入の任意処理を実行するため、「段階1では外部副作用が型として
不可能」という境界になっていない。本反証は安全な一時file書込みだけだが、callbackに許可操作を
限定する型・検証がないことを機械実証した。未承認の段階4へ通じる任意callbackを段階1へ
注入できるため、段階境界を破る類型4のblockingとする。実際の外部送信は試していない。

### F-E6 blocking／implementation／§11.1類型3

対象：`tools/session_logs/preservation.py`

【実測】R1では、初回保全と台帳作成後にbackupだけを改変し、sourceを元のまま再保全した。
実装は不一致を`action=preserved`とした後、改変backupのDigestで台帳entryを上書きした。
sourceを削除して復元すると、改変値が台帳照合に合格して復元された。

【記録】Session Logの上流Requirementとmodule契約は、生ログの追記専用保全、改変検出、
完全性台帳による安全な復元を求める。

【判断】既存backupを台帳へ照合する前に台帳をそのbackupへ更新し、改変を正当化する。
復元直前の単独改変は既存testが拒否するが、保全処理を1回挟むと改変値を正本として合格させるため、
類型3のblockingとする。上書き、非追記、復元の同類型を一続きで確認した。

### F-E7 blocking／implementation／§11.1類型3・4

対象：`tools/session_logs/preservation.py`

【実測】R2前半では、raw root内の相対pathをroot外fileへのsymlinkにすると、その値を読み、
backupへ保全した。後半では、backup root内の親directoryをroot外directoryへのsymlinkにすると、
root外へ`session.jsonl`を作成した。全て一時領域内で確認した。

【判断】`raw_log.relative_to(raw_root)`は字句上の相対関係だけを検査し、raw、backup、各祖先を
解決後rootへ束縛しない。root外の値を正規rawとして合格させる類型3、隔離保存・読書きscopeを
破る類型4のblockingとする。読取り側と書込み側のsymlink変種を本周回で一括確認した。

### non-blocking／defer

【判断】non-blocking Findingは0件、defer Findingは0件である。今回の成立反証は全て、
上流authority、Human境界、誤った合格・拒否、またはscope・schema境界のいずれかを機械実証し、
§11.1の閉じた類型内だった。新しい送信段階、payload種別、保存schemaは提案していない。

## 7. Human境界、禁止事項、未実施

【実測】反証・既存test・公式全Testの前後で、元repositoryの
`git status --short --branch`はbranch行だけだった。反証は一時領域だけを使い、対象code、test、
既存record、実ログ、実設定、利用者環境を変更していない。実際の外部送信、push、tag、amend、
rebase、reset、履歴書換えも行っていない。

【判断】Findingの修正、TODO反映、段完了、Findingのrisk受容は未実施であり、Human境界を維持した。
本recordは修正開始の承認でも、group E対象codeの完了根拠でもない。

## 8. 結論と次の一作業

【判断】group Eは1 module `verified`、6 module `reported_unverified`、blocking 7件である。
公式全Testと既存testの合格は維持されたが、新作反証が現行fixtureの外で誤った合格・拒否と
境界脱出を実証したため、group全体を`verified`にはしない。

【提案】次の一作業は、Pilotが本recordを再読込みして鮮度・単独commit・禁止path不変を照合し、
Humanへblocking 7件を集約して「いま別単位で対処／候補として後回し／本線へ戻る」の判断を求める
ことである。修正着手とCloserのTODO反映は本commitに含めない。
