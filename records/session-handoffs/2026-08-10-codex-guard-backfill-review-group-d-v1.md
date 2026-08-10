# 守り役後追い独立レビュー #6第2単位 group D 判定 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：implementation（既存の守り役codeに対する後追いレビュー）
- risk：`low`（Human確定済み）
- 総合判定：`reported_unverified`
- Finding：blocking 7件、non-blocking 0件、defer 0件

## 1. 固定対象と開始状態

- 範囲固定：
  `records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-high-reviews-scope-v1.md`
  （commit `bedf986408156e661c4a15c6886a4e9558d514ec`、SHA-256
  `6b587a7eedf77380aadf5b41ab90edd148bdcd6f69b850447dc684591737f8e9`）
- 判定基準：`docs/development/work-review-protocol.md`（§3・§4.7・§11、SHA-256
  `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`）
- レビュー開始時HEAD：`f02c32cb74263a6db60b3eac8144ce2adcde0c66`
- branch：`main`
- 先行：group A `17613d2`、group B `46f2465`、group C `f02c32c`は完了済み。
  各commitは対応する判定record 1件だけを追加しており、修正は本scope外
- 対象：`tools/development/structured_argv_executor.py`、
  `tools/development/issue_intake_v4.py`、`tools/layout/baseline.py`
- 許可範囲：対象と既存testの読取り、一時領域での反証、本判定recordの新規作成と単独commit
- 禁止範囲：code、test、既存record、実台帳、実設定、利用者環境の変更、外部操作、
  Findingの修正、TODO・checklist反映、先行groupの修正
- 期待成果：moduleごとの§4.7判定、§11区分のFinding、反証のcommand・結果・終了コード、
  model来歴を持つ本record 1件と、その単独commit
- 停止条件：固定入力Digest不一致、許可path外の変更が必要な場合

【記録】Humanは2026-08-10に「#6第2単位 risk lowを確定、着手を承認する」と明示した。

【実測】開始時のworktreeとindexはcleanだった。HEADは先行group Cの単独commit `f02c32c`である。
`git diff --name-status bedf986 -- <group D 3 moduleと直接test>`は出力なしで、対象実装と
直接testが範囲固定後に変わっていないことを確認した。

【実測】範囲固定§3の固定入力4件は、`shasum -a 256`による再計算で全件一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| Human裁定 | `d73f51a17ef20fa6a5abb531c30119384582cec9c299102e518088e3bb51afa7` |
| 対象一覧 | `77b6ba9fc0bfd7ea17e071dc4e4df59e12f84f4a7d23798dedafe58b6ea6571e` |
| 共通レビュー基準 | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| `TODO_NEXT_SESSION.md` | `6de9d6d8b4f0ebc93f59e7fbe1ee6e192f5aba27e7b94e4e5dfe673e65b6205a` |

【実測】確定pathへの`git check-ignore --no-index`は終了コード1で、ignore対象外だった。
作成前の`test ! -e`は終了コード0で、同名fileが存在しないnew-only状態だった。

## 2. 実装、上流、既存testの読取り

【実測】対象3 module、直接・関連test、Layout Baseline v1〜v3、Issue Intake V4の設計・
GREEN Evidence、argv executorの承認・GREEN Evidenceを再読込みした。対象moduleのSHA-256は
次のとおり。

| 対象 | SHA-256 |
| --- | --- |
| `tools/development/structured_argv_executor.py` | `ffe09cdc619ffe71235b1c4182d7ec1d7b5246fe231c8f990c082a401bcb1a1c` |
| `tools/development/issue_intake_v4.py` | `42b797ad9e1aef81620a94a08c279a99c8daa7924329b44a54da1024cc9f4fde` |
| `tools/layout/baseline.py` | `6d00c3053da820cd694a0c4b47d5e5f1b632f00d83e81691f99060626bc94cb7` |

【実測】直接・関連testとして次を読んだ。

- `tests/test_structured_argv_executor.py`
- `tests/test_verification_boundary_layer2.py`
- `tests/test_issue_intake_v4.py`
- `tests/test_issue_intake_v4_single_candidate.py`
- `tests/test_adversarial_remedy_i4.py`
- `tests/test_verification_boundary_layer1.py`
- `tests/test_layout_baseline.py`
- `tests/test_project_runtime_layout.py`

【記録】argv executorは、全操作が`read_only`であり、argvが
`git status --porcelain`と任意のpathspecに一致する場合だけ実行する。shellを介さず、Git metadata、
project成果物、外部操作への書込みを起動しない契約である。

【記録】Issue Intake V4は、候補、Human裁定、Issueをpath、file SHA-256、内容Digest、ID、版で
束縛し、裁定集合の競合を拒否する。後継裁定の版と時刻の前後矛盾は
`check_decision_time_monotonicity`で拒否することが層1 GREEN Evidenceに記録されている。

【記録】Layout Baselineは、相対pathのproject root外脱出、stable／development間のcross-write、
管理対象pathの通常移動を拒否し、project-first runtime rootを物理分離する。ここでsymlinkは、
別の場所を指す特殊なfileである。

【実測】既存testは、argvの文字列化・既知option形・字句上のpath脱出・開始時点のcwd symlink、
参照指紋の一項目改変、裁定rootの競合、Issue本文改変、通常の相対path脱出、通常のroot初期化を
覆う。一方、今回試した実行file探索の環境すり替え、Git環境変数による別worktree参照、
自己整合させた偽Digest、candidate pathのsymlink脱出、裁定後継の時刻逆転・別ID化、
Layout解決後のsymlink差替え、Manifest自体のsymlink脱出、固定方針値の複合改変は
既存fixtureになかった。

## 3. 既存testと公式全Testの独立再実行

【実測】次の単独commandは終了コード0、`104 passed in 0.24s`だった。

```text
env PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS=-p\ no:cacheprovider .venv/bin/python3 -m pytest -q tests/test_structured_argv_executor.py tests/test_verification_boundary_layer2.py tests/test_issue_intake_v4.py tests/test_issue_intake_v4_single_candidate.py tests/test_adversarial_remedy_i4.py tests/test_verification_boundary_layer1.py tests/test_layout_baseline.py tests/test_project_runtime_layout.py
```

【実測】公式全Testは元repositoryへ書かないため、一時領域
`/private/tmp/codex-group-d-full-tree-v1`へ`.venv`を除くworktreeと`.git`を複製し、複製内の
`.venv/`だけを元環境の4要素へのsymlinkで構成して実行した。実行前後の複製側
`git status --short --branch`はbranch行だけで、tracked・untracked差分はなかった。対象3 moduleの
Digestは元repositoryと一致した。receiptはproject root外へ置いた。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/codex-group-d-official-isolated-receipt-v2.json
```

結果は終了コード0、status `passed`、`1381 passed`、failed 0、errors 0、skip・xfail・xpass 0、
Python 3.9.6、pytest 8.4.2、fallback falseだった。receipt SHA-256は
`1d04fb38fc201979618c8b49fa7cd3c6f5f7d51c296a0de7956a3b8054f75ce7`である。

【実測】最初の隔離全Testでは、付加した`PYTHONDONTWRITEBYTECODE=1`が子processへ継承され、
bytecode cache作成を期待する`tests/test_task_python_cache.py` 1件だけが失敗した。commandは次で、
終了コード1、`1380 passed, 1 failed`だった。

```text
env PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS=-p\ no:cacheprovider .venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/codex-group-d-official-isolated-receipt-v1.json
```

【判断】これは対象moduleの失敗ではなくReviewerが加えた環境条件による手戻りである。期待executorは
公式policy runner、実executorも同じだが、手作業理由は元repositoryへのcache書込み回避だった。
公式Test自身が一時runtimeへcacheを書くため付加条件は不要だった。付加条件を外した上記v2を
合否根拠とし、v1は判定Evidenceに数えていない。機械処理候補は、隔離全Testの共通runnerが
公式環境条件を固定すること。routeは本レビュー外の改善候補であり、本線では扱わない。

## 4. 既存fixtureにない反証

### 4.1 実行環境と一時領域

【実測】反証はPython 3.9.6、pytest 8.4.2、`macOS-26.5.1-arm64-arm-64bit`で実行した。
反証harness（反証を自動実行する一時script）は`/private/tmp/codex_group_d_adversarial.py`だけに
置き、SHA-256は`253cf8b265751d60d0b9443f120d39c6c7e5554c2bfcd1b9eff2384b220a3f35`だった。
各project、Git repository、候補、裁定、Layout、markerはcaseごとの
`TemporaryDirectory(dir="/private/tmp")`だけに作成し、case終了時に消去した。

以下の終了コード1はharness異常ではなく、「安全側なら拒否し、境界外を読まず、境界外へ作らない」
という独立oracleに反して対象moduleが合格したことを表す。

### 4.2 反証の実行一覧

各commandの`<case>`は、同一command末尾のcase名である。

| ID | command | 結果 | 終了コード |
| --- | --- | --- | --- |
| E1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py executor_path_substitution` | 一時`PATH`先の偽`git`がmarkerを書き、receiptは`completed` | `1` |
| E2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py executor_git_environment_redirect` | `GIT_DIR`・`GIT_WORK_TREE`が指すproject外の一時worktreeを読み、receiptは`completed` | `1` |
| I1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py issue_candidate_digest_forgery` | 候補の宣言Digestは全0、再計算値は`a2c3fe3c...8a659`だがHuman裁定validatorが合格 | `1` |
| I2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py issue_candidate_symlink_escape` | project内の相対pathがproject外候補へのsymlinkでもHuman裁定validatorが合格 | `1` |
| I3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py decision_chain_time_reversal` | v2裁定の時刻をv1より1日前にしてもrepository validatorがv2を有効化 | `1` |
| I4 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py decision_chain_cross_identity` | `DEC-IC-CHAIN-001-ALT`が別IDの`DEC-IC-CHAIN-001`を後継化しても有効化 | `1` |
| L1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py layout_symlink_swap_write` | Layout解決後にruntime rootをsymlinkへ差し替えると、project外の一時directoryに`sensitive` rootを作成 | `1` |
| L2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py layout_manifest_symlink_escape` | 管理pathのManifest自体がproject外fileへのsymlinkでもproject bindingを合格 | `1` |
| L3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_d_adversarial.py layout_baseline_policy_tamper` | `escape=allow`、`cross_write=allow`、解決優先順の差替えを同時に含むBaselineを合格 | `1` |

### 4.3 代表的な機械出力

【実測】E1は次を出力した。

```json
{"case": "executor_path_substitution", "fake_executable_ran": true, "receipt_status": "completed"}
```

【実測】I3・I4では、時刻逆転と別IDへの連鎖をそれぞれ持つv2裁定が有効裁定になった。

```json
{"accepted": true, "case": "decision_chain_time_reversal", "first_decided_at": "2026-08-10T12:00:00+09:00", "first_decision_id": "DEC-IC-CHAIN-001", "second_decided_at": "2026-08-09T12:00:00+09:00", "second_decision_id": "DEC-IC-CHAIN-001", "violation_present": true}
{"accepted": true, "case": "decision_chain_cross_identity", "first_decided_at": "2026-08-10T12:00:00+09:00", "first_decision_id": "DEC-IC-CHAIN-001", "second_decided_at": "2026-08-11T12:00:00+09:00", "second_decision_id": "DEC-IC-CHAIN-001-ALT", "violation_present": true}
```

【実測】L1は次を出力した。表示pathはsymlinkの字句pathだが、実際に作成されたdirectoryは
一時領域内のproject外targetだった。

```json
{"case": "layout_symlink_swap_write", "created_path": "/private/tmp/.../runtime/projects/project-alpha/development/sensitive", "outside_target_created": true}
```

## 5. moduleごとの判定（§4.7）

| module | 判定 | Evidenceと理由 |
| --- | --- | --- |
| `tools/development/structured_argv_executor.py` | `reported_unverified` | 既存testと通常argvは合格したが、E1で許可した`git`とは別の実行fileが書込みを行い、E2で検証済みcwd外のGit状態を読んだ。F-D1により`verified`にできない |
| `tools/development/issue_intake_v4.py` | `reported_unverified` | 既存の一項目改変、競合root、通常の裁定連鎖は拒否したが、I1〜I4で自己整合したDigest偽造、symlink脱出、時刻逆転、別ID連鎖を合格させた。F-D2〜F-D4により`verified`にできない |
| `tools/layout/baseline.py` | `reported_unverified` | 通常の相対path脱出、開始時点のroot分離、固定実recordは既存testどおりだったが、L1〜L3で検証後symlink差替えによるproject外作成、管理Manifestのproject外参照、固定境界方針の改変を合格させた。F-D5〜F-D7により`verified`にできない |

【判断】3 moduleすべてにblocking Findingが対応するため、group Dの総合判定は
`reported_unverified`である。§6が定める再現条件不足ではなく、§11.1類型1、3、4の機械反証を
根拠とする。固定された完了報告と事後状態の競合はないため`report_execution_mismatch`ではない。
範囲固定§8.3はblocking検出を停止条件にせずrecordへ固定してgroupを完了させるため、`blocked`でもない。

## 6. Finding（§11）

### F-D1 blocking／implementation／§11.1類型3・4

対象：`tools/development/structured_argv_executor.py`

【実測】E1では、argvは許可templateのままだが、processの`PATH`先頭へ置いた偽`git`が一時markerを
書き、executorのreceiptは`completed`になった。E2では、実Gitを起動しても`GIT_DIR`と
`GIT_WORK_TREE`により検証済みproject root外の一時worktreeを読み、そのfile名をstatus出力に得た。

【判断】検査する文字列`git`を実行file identityへ束縛せず、Gitの対象repositoryを検証済みcwdへ
束縛しないため、許可外programの書込みとscope外repository参照を「読み取り専用の許可command」として
合格させる。誤った合格を実証した類型3、書込み禁止とproject scopeを破る類型4のblockingとする。
同じ環境すり替え類型の実行file探索とGit対象指定を本周回で一括確認した。

### F-D2 blocking／implementation／§11.1類型3

対象：`tools/development/issue_intake_v4.py`

【実測】I1では、候補recordの`content_digest`を全0にし、その不正bytesに合うfile SHA-256を
`candidate_ref`へ置いた。参照側と候補内の宣言値は自己整合するが、候補内容から再計算したDigestは
`a2c3fe3c...8a659`で異なる。それでもHuman裁定validatorは合格した。

【判断】単体候補のfile SHA-256と宣言Digestの参照一致は調べるが、候補自身の正準Digestを再計算しない。
このため、候補と参照を同時に偽造した入力を正しいProvenance（来歴）として合格させる類型3の
blockingとする。一項目だけのstale化は既存testが拒否するため、本周回では自己整合偽造を試した。

### F-D3 blocking／implementation／§11.1類型3・4

対象：`tools/development/issue_intake_v4.py`

【実測】I2では、`candidate_ref.record_path`は通常のproject相対pathだが、実fileをproject外の
一時候補へ向けるsymlinkにした。file SHA-256、ID、宣言Digestが合うとHuman裁定validatorは合格した。

【判断】pathを字句だけで検査し、解決後pathがproject root内であることとsymlink不使用を確認しない。
root外の台帳候補を正本参照として合格させる類型3、project scope境界を破る類型4のblockingとする。
候補bundle、裁定file、Issue fileにも同じpath解決関数群が使われるが、小出しを避けるため、同類型を
単体候補参照で代表して記録する。

### F-D4 blocking／implementation／§11.1類型3

対象：`tools/development/issue_intake_v4.py`

【実測】I3では同じIDのv2裁定をv1より1日前の`decided_at`にしてもrepository validatorがv2を
有効化した。I4では別ID `DEC-IC-CHAIN-001-ALT`のv2裁定が
`DEC-IC-CHAIN-001`のv1を`supersedes`で指しても有効化した。各recordのDigestは再計算済みである。

【記録】同moduleには時刻逆転と別IDを拒否する`check_decision_time_monotonicity`があり、層1 GREEN
Evidenceも後継版と時刻の矛盾を拒否するとしている。

【判断】裁定repositoryの有効版解決がこの検査を呼ばず、`supersedes`先と後継のdecision ID同一性も
直接確認しないため、偽造した裁定連鎖を有効なHuman判断として合格させる類型3のblockingとする。
同じ裁定連鎖類型の時間軸とidentity軸を本周回で一括確認した。

### F-D5 blocking／implementation／§11.1類型3・4

対象：`tools/layout/baseline.py`

【実測】L1では、副作用なしでruntime layoutを解決した後、作成前にruntime rootをproject外の一時
directoryへのsymlinkへ差し替えた。`initialize_project_runtime_layout`は拒否せず、symlink先へ
`projects/project-alpha/development/sensitive`を作成した。

【判断】解決時のpathだけを信頼し、書込み直前にrootと各祖先のsymlink・解決先を再検査しない。
許可root内の初期化と誤って合格させる類型3、配置・書込みscope境界を破る類型4のblockingとする。
runtime root本体、祖先component、要求rootの差替えは同じ最終同一性欠落へ収束するため、本反証で
代表させる。

### F-D6 blocking／implementation／§11.1類型3・4

対象：`tools/layout/baseline.py`

【実測】L2では、管理path `.reviewcompass/project-manifest.json`をproject外の一時Manifestへの
symlinkに置換した。Manifest内の相対pathがproject内へ解決できると、`validate_project_layout`は
project bindingを合格させた。

【判断】個々の宣言pathは解決後root内を検査するが、宣言正本であるManifest自身のsymlinkと解決先を
検査しない。project外の宣言をGit管理内の正本として合格させる類型3、管理対象pathとproject scopeを
破る類型4のblockingとする。読取り側symlinkの同類型はF-D3と本件で台帳・Layoutの両境界を確認した。

### F-D7 blocking／implementation／§11.1類型1・3

対象：`tools/layout/baseline.py`

【実測】L3では、v3 Baselineの`relative_path_policy.escape`と
`environment_isolation.cross_write`を`allow`へ、`resolution_precedence`を未知の1値へ同時に変えた。
top-level keyと版は維持したまま、`load_layout_baseline`は変更後recordを合格させた。

【記録】現行Baselineと既存testは、escapeとcross-writeを`reject`にし、解決優先順を
`explicit_cli`、versioned setting、許可環境変数、OS標準の順へ固定している。

【判断】loaderは一部の固定policyを完全一致で検査する一方、上記3境界値を検査しない。上流authorityと
反対の配置方針を有効Baselineとして受ける類型1、境界validatorの誤った合格である類型3のblockingと
する。同じ未検査方針値の脱出、cross-write、優先順を本周回で一括確認した。

### non-blocking／defer

【判断】non-blocking Findingは0件、defer Findingは0件である。今回の9反証はすべて、上流境界との
矛盾、誤った合格、またはscope・禁止事項の破りを機械実証したため、§11.1の閉じた類型内である。
新しいcommand種類、台帳schema、Layout設計は提案せず、現契約の境界だけを判定した。

## 7. Human境界、禁止事項、未実施

【実測】反証・既存test・公式全Testの前後で元repositoryの`git status --short --branch`はbranch行だけ
だった。反証は一時領域だけを使い、対象code、test、既存record、実台帳、実設定、利用者環境を
変更していない。外部送信、push、tag、amend、rebase、reset、履歴書換えも行っていない。

未実施：F-D1〜F-D7の修正、新規test作成、既存test変更、TODO・checklist反映、先行group修正、
group Eレビュー、Closer作業、外部操作。

【判断】risk `low`は成果物が本レビューrecord 1件だけであることに対するHuman確定であり維持した。
守り役code自体の判定では、依頼どおり既存fixture外の独立反証と隔離した公式全Testを追加した。

## 8. 判定と次のHuman判断

判定：`reported_unverified`。

【判断】レビュー作業と本recordは完了したが、対象3 moduleはF-D1〜F-D7により`verified`ではない。
blockingを修正せず、禁止された実装変更を未実施のまま保持した。

次：Humanが本Findingを確認し、現行Plan上で次のいずれかを一つ選ぶ。

1. いま対処：F-D1〜F-D7を、守り役code修正の別`high` risk作業単位として範囲固定する。
2. 候補として後回し：Findingを未解消のまま保持し、修正候補へrouteする。
3. 本線へ戻る：本groupの修正には着手せず、固定済み第2単位のgroup Eレビューへ進む。
