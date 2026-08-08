# Codex → Claude：伏字化規則の設定登録と保全経路への接続

## 1. 役割と作業単位

- Humanは、`TODO_NEXT_SESSION.md`の「伏字化規則の設定登録と保全経路への接続」に
  着手し、`docs/development/codex-claude-collaboration.md`に従ってClaudeへ委譲することを
  指示した。
- Codexは、固定入力、受入条件、変更可能path、禁止事項、停止条件をこの指示書へ
  固定する。
- Claudeは、以下の**1つの小さなE2E縦切り**だけをTDDで実装する。
  1. 承認済みのpattern規則5件とenvironment reference規則3件を、セッションログ設定に
     宣言値のまま登録する。
  2. 設定から読み込んだ両種類の規則を`eventual_preservation`の伏字化派生物作成経路へ
     渡し、実際にマスクが適用されることを合成fixtureで固定する。
  3. 解決した環境値が設定、伏字化派生物、Provenance digest入力、診断のどこにも
     漏れないことを固定する。
- 完了後は指定のClaude→Codex報告を作り、Codexの独立確認まで次の作業へ進まない。

## 2. 開始状態と固定入力

- branch：`main`
- base commit：`32a8ac7af3817674f470a2d47adf1c6e891b34fd`
- 開始時worktree：clean

| role | path | SHA-256 |
| --- | --- | --- |
| 共同作業手順 | `docs/development/codex-claude-collaboration.md` | `beab9d2cf0db4f31a869ae2d597dff8265ace9a022d83bba2d03b810a984cc49` |
| 作業レビュー手順 | `docs/development/work-review-protocol.md` | `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `77fc5867de82f52716dadcf6930ae7be06ef296fa68ca38b3125894b1782b3dd` |
| 実施順序Decision | `records/development/2026-08-07-confidentiality-work-order-decision-v1.md` | `ca5c4a89adb6ab2807887bb7834c4778f4e8658a697deb9f64617893dd67de09` |
| 承認済み規則設計 | `docs/design/2026-08-07-redaction-rules-design-proposal.md` | `d6e1b15309e52aa5875176bfc9fcfaa1a7253b7be1d842fdc337c977bd79321a` |
| 規則実装GREEN Evidence | `records/development/2026-08-07-redaction-environment-rules-green-evidence-v1.md` | `9dae5c2df9d39be08a63e22f47936fb27336d42c9032d8b5442bca8d7df68f85` |
| 現行設定loader | `tools/session_logs/config.py` | `0b7c970e63ad7ad0b9f268b26ecea0425e95f81e4a503143229594c0c4a78989` |
| 承認済み規則実装 | `tools/session_logs/redaction.py` | `aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd` |
| 現行保全経路 | `tools/session_logs/eventual_preservation.py` | `2c186bbc8af591108ff91a3698f5dc4b3e3ce2bd318e23a838a8d30ae03900d7` |
| 設定境界Test | `tests/test_session_log_config_boundaries.py` | `cd43f9e2fec4c36c74dab9a2a82936d9fea1267d5b6f1e904c7a3457017b7a55` |
| 規則Test | `tests/test_redaction_environment_rules.py` | `8d532047203779622b5df6e1168ba04e6dbf2297c91ffb4775896806e14662e2` |
| 保全経路Test | `tests/test_session_log_eventual_preservation.py` | `a4f704c4ac267e983c0831b2f1a6a97a64c6db335b8eae9d3efa032e897b3999` |

作業開始時にbase commit、branch、worktree、表のSHA-256を機械確認する。不一致、先行commit、
別executorの未コミット差分がある場合は差分の帰属を推測せず停止する。

## 3. 固定する設定契約

### 3.1 登録内容

承認済みの次の8宣言だけを登録する。規則の追加、削除、pattern変更、role変更はしない。

- pattern：`email`、`bearer_token`、`api_key_assignment`、`private_key_block`、
  `aws_access_key_id`
- environment reference：`home_directory`、`user_name`、`host_name`

`tools/session_logs/redaction.py`の`default_pattern_rules()`と`environment_reference_rules()`を
唯一の宣言sourceとし、patternを別moduleへ重複記載しない。

### 3.2 JSON表現とload後の型

- 既存top-level key `redaction_rules`を維持する。新しいtop-level schemaを作らない。
- pattern宣言は既存形式`{"label": <label>, "pattern": <pattern>}`とする。
- environment reference宣言は承認済み形式
  `{"label": <label>, "environment_role": <role>}`とする。実値や解決後patternを書かない。
- loaderはpattern宣言を`Rule`、environment reference宣言を`EnvironmentRule`として
  区別して保持する。`Config.redaction_rules`は既存consumer互換のためpattern規則だけを保持し、
  environment referenceは意味が明確な新しいfieldへ保持する。
- `pattern`と`environment_role`を同時に持つ項目、どちらも持たない項目、未知roleは
  `ConfigError`でfail-closedにする。例外文に入力値を含めない。
- 既存のpattern-only configの読込みと明示的な空listの意味は壊さない。

### 3.3 ポータブル設定への登録

`tools/session_logs/portable_config.py`が生成する通常の新規設定に、上記8宣言を明示的に
シリアライズする。合成fixture以外のhost固有値を設定に書かない。

既存の`build_portable_config(..., redaction_rules=...)`呼出しの互換性は維持する。互換性を保つには
承認済み契約を変える必要があると判明した場合、推測で新schemaを追加せず停止する。

## 4. 保全経路の受入条件

`tools/session_logs/eventual_preservation.py`の既存のraw先行保全、境界、lock、cursor、冪等性は
変えず、伏字化派生物の作成部分だけを次のように接続する。

1. `collect_source`と`reconcile_source_root`は、既存のpattern規則に加えて
   environment reference宣言を受け取れる。既存の引数と呼出しの互換性を保つ。
2. 規則が明示的に渡された保全経路は`redact_with_environment(..., strict=True)`を使い、
   environment reference（長い値から）→pattern（登録順）→現行high-entropy検査の順を保つ。
3. Provenanceの`redaction_rules_sha256`は、解決後patternではなく、environment reference宣言と
   pattern宣言から決定的に算出する。役割名は入っても解決値は入らない。
4. 合成config→`load_config`→実collectorという受入Testで、次を確認する。
   - 合成したhome directory、user name、host name、email、tokenが伏字化派生物に残らない。
   - 置換先は`[REDACTED:<label>]`であり、実値を含まない。
   - rawとverbatimは従来どおりprivate rootに保全され、対象の変造や削除をしない。
   - redacted artifactとProvenanceは存在し、Provenanceと実fileのSHA-256が一致する。
   - 同じ固定入力の再実行は同じ伏字化結果と規則digestを生み、既存の冪等性を壊さない。
5. patternで消えない高entropy合成値が残った場合はfail-closedとし、伏字化派生物、
   Provenance、cursorの成功状態を作らない。例外と診断に該当値を出さない。raw先行保全の
   従来契約は維持する。
6. `redaction_rules is None`の既存の明示的な「伏字化派生物を作らない」契約は
   互換性のため維持する。通常の新規設定経路が承認済み規則を渡すことで、実行経路を
   伏字化有りにする。

テストでは実在の秘密、実在の保全データ、hostの実際のhome、user、hostnameを記録しない。
`monkeypatch`と`tmp_path`による合成値だけを使い、失敗出力にも値を出さない。

## 5. TDDとcommit境界

### Commit 1：RED Testだけ

- 原則として新規`tests/test_redaction_registration_preservation_path.py`だけに受入Testを書く。
  既存Testへの追記が必要な場合は、同じRED commitへ含めてよい。
- 実装前に対象Testを**単独command**で実行し、今回の未実装による期待した失敗だけが
  出ることとexit code `1`を確認する。
- 既存実装でGREENになるTest、fixture不備、実在値の露出で失敗するTestはRED根拠にしない。
- `git diff --check`後、Test pathだけを明示stageし、RED Testだけの意味単位commitを作る。

### Commit 2：GREEN実装とEvidence

- RED commit後は、要求誤解が判明しない限りTestを変更せず、実装側を修正して通す。
- 対象Test、関連回帰、公式全Testをそれぞれ単独commandで実行し、exit codeで合否を判定する。
- 公式全Testは次を使う。receiptのpathは固定する。

  `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-redaction-registration-preservation-green-test-receipt-v1.json`

- `records/development/2026-08-08-redaction-registration-preservation-green-evidence-v1.md`を作り、
  次を記録する。
  - baseとRED commit SHA
  - RED command、失敗数、期待失敗の理由、exit code
  - 設定登録の8宣言と、設定→loader→collectorの実行経路
  - targeted、関連回帰、公式全Testのcommand、結果、exit code
  - 実装とTestのSHA-256、公式receiptのSHA-256
  - 解決値非漏洩、fail-closed、raw先行保全、冪等性の結果
  - 未実施範囲とHuman境界
- `git diff --check`、公式receiptの再読込み、Evidenceの参照とDigestを機械照合する。
- 実装、Test、GREEN Evidence、公式receiptだけを明示stageし、緑の意味単位commitを作る。
- コミット後に`python3 -m tools.development.work_unit_transition --work-status completed`を実行し、
  `completed_work_unit_uncommitted`でないことを確認する。

## 6. 変更可能path

### 実装とTest

- `tools/session_logs/config.py`
- `tools/session_logs/portable_config.py`
- `tools/session_logs/eventual_preservation.py`
- `tests/test_redaction_registration_preservation_path.py`（新規）
- 必要な場合だけ：
  - `tests/test_session_log_config_boundaries.py`
  - `tests/test_session_log_portable_config.py`
  - `tests/test_session_log_eventual_preservation.py`

### Evidence

- `records/development/2026-08-08-redaction-registration-preservation-green-evidence-v1.md`
- `records/development/2026-08-08-redaction-registration-preservation-green-test-receipt-v1.json`

上記以外の変更が必要な場合は実装せず停止する。とくに`tools/session_logs/redaction.py`は今回の
固定入力であり、変更しない。ファイルのローカルなインデントと既存styleを保ち、無関係な一括整形を
しない。

## 7. 禁止事項

- 既存の保全済みデータ、`SENSITIVE_ROOT`、hostの実session logを読まない、伏字化しない、
  書き換えない、削除しない。実在データへの遡及適用は別のHuman判断である。
- C（内部の未公開情報）とD（会話に混入した外部データ）の定義や扱いを変えない。
- high-entropy検査のpattern、長さ、entropy閾値、allow pattern、位置づけを変えない。
- 外部送信、egress関門、APIレビュー、hook、watcher、scheduler、background service、
  deploymentを実行・変更しない。
- `TODO_NEXT_SESSION.md`、initial checklist、Decision、Issue、Candidate、workflow台帳、
  既存Evidenceを変更しない。TODOとchecklistの完了反映はCodexの独立確認後に行う。
- 新しい外部依存、schema version、Task Contract、Workflow permit、Human Decisionを作らない。
- `git add -A`、`git add .`、amend、rebase、reset、push、tag、PR、履歴書換えを行わない。

## 8. 停止条件

次のいずれかに該当したら、範囲を広げたり既存Testを書き換えたりせず停止する。

1. base、固定入力Digest、開始時worktreeが不一致。
2. 上記変更可能path以外、とくに`redaction.py`、pipeline全体、deploymentの変更が必要。
3. 既存top-level `redaction_rules`で両種類を表現できず、新schemaまたは新しい意味的裁定が必要。
4. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
5. GREENで受入条件を満たすために、規則のpattern・role、entropy網、既存raw保全契約、
   storage boundaryを変更する必要がある。
6. 対象Test、関連回帰、公式全Test、`git diff --check`、receipt再読込み、Digest照合のいずれかが不合格。
7. 実在の秘密、host固有値、既存保全データの読取りや記録が必要。

停止時も、停止理由、再現command、exit code、実施済みと未実施を完了報告へ書く。

## 9. ClaudeからCodexへの完了報告

完了または停止後、次を作成し、**commitに含めず**停止する。

`records/session-handoffs/2026-08-08-claude-to-codex-redaction-registration-preservation-path.md`

報告には次を含める。

- 判定：`completed_claim` または `blocked_claim`
- base、RED commit、GREEN commitのSHAと各commitの変更path
- RED、targeted GREEN、関連回帰、公式全Test、`git diff --check`のcommand、結果、exit code
- 設定→loader→collectorの実測結果、規則digest、Evidenceとreceiptのpath・SHA-256
- 解決値非漏洩、fail-closed、raw先行保全、冪等性の確認結果
- 禁止path変更、実在データ読取り、外部操作、pushが未実施であること
- 停止条件の発生有無と未実施範囲

Claudeの報告はClaimであり、完了Evidenceそのものではない。Codexがbaseからのcommit列、diff、
読み戻し、Digest、Test、禁止境界を独立確認する。本作業は`high`であるため、CodexはClaudeの
fixtureに無い新しい反証を最低1件機械実行し、その後にHumanへ判定を返す。
