# 守り役後追い独立レビュー #6第2単位 group B 判定 v1

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
- Finding：blocking 5件、non-blocking 0件、defer 0件

## 1. 固定対象と開始状態

- 範囲固定：
  `records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-high-reviews-scope-v1.md`
  （commit `bedf986408156e661c4a15c6886a4e9558d514ec`、SHA-256
  `6b587a7eedf77380aadf5b41ab90edd148bdcd6f69b850447dc684591737f8e9`）
- 判定基準：`docs/development/work-review-protocol.md`（§3・§4.7・§11、SHA-256
  `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`）
- レビュー開始時HEAD：`17613d26b9b334934a5d717b1954ab573d320043`
- branch：`main`
- 先行：group A判定recordのcommit `17613d2`は完了済み。group Aの修正は本scope外
- 対象：`tools/development/policy_test_runner.py`、
  `tools/development/pytest_summary.py`、
  `tools/development/declaration_red_map_check.py`、
  `tools/development/work_unit_transition.py`
- 許可範囲：対象と既存testの読取り、一時領域での反証、本判定recordの新規作成と単独commit
- 禁止範囲：code、test、既存record、実台帳、実設定、利用者環境の変更、外部操作、
  Findingの修正、TODO・checklist反映、group A修正
- 期待成果：moduleごとの§4.7判定、§11区分のFinding、反証のcommand・結果・終了コード、
  model来歴を持つ本record 1件と、その単独commit
- 停止条件：固定入力Digest不一致、許可path外の変更が必要な場合

【記録】Humanは2026-08-10に「#6第2単位 risk lowを確定、着手を承認する」と明示した。

【実測】開始時のworktreeとindexはcleanだった。HEADは範囲固定commit後の先行group A単独commit
`17613d2`である。`git diff --name-status bedf986 -- <group B 4 module> tests`は出力なしで、
group Bの実装とtestが範囲固定後に変わっていないことを確認した。

【実測】範囲固定§3の固定入力4件は、`shasum -a 256`による再計算で全件一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| Human裁定 | `d73f51a17ef20fa6a5abb531c30119384582cec9c299102e518088e3bb51afa7` |
| 対象一覧 | `77b6ba9fc0bfd7ea17e071dc4e4df59e12f84f4a7d23798dedafe58b6ea6571e` |
| 共通レビュー基準 | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| `TODO_NEXT_SESSION.md` | `6de9d6d8b4f0ebc93f59e7fbe1ee6e192f5aba27e7b94e4e5dfe673e65b6205a` |

【実測】確定pathへの`git check-ignore --no-index`は終了コード1で、ignore対象外だった。
作成前の`test ! -e`は終了コード0で、同名fileが存在しないnew-only状態だった。

## 2. 実装と既存testの読取り

【実測】対象4 moduleと直接・結線・既往反証の既存testを再読込みした。対象bytesのSHA-256は
次のとおり。

| 対象 | SHA-256 |
| --- | --- |
| `tools/development/policy_test_runner.py` | `64724e0ff1aed80953dd48054218c2765c905a1a207ed43ef9ddfe8056e2cd82` |
| `tools/development/pytest_summary.py` | `b70c4fb7cc6840509a9b16f683a3f2286396df7ebbfd9ba5daa4d1d71ecacebe` |
| `tools/development/declaration_red_map_check.py` | `fee17b2161cb07268cb05fd954cf5d57c29c9824add4d59ef05fc08def64e73d` |
| `tools/development/work_unit_transition.py` | `de131c00baef55799b6222aec578c2ad4e960b5e56df8a0b97fcdabd998d434e` |
| `tests/test_policy_test_runner.py` | `9ac58195519428cc2b7d1e3202e7b531a37000646e9c48dfdcce1daf5082be64` |
| `tests/test_policy_test_runner_receipt_identity.py` | `bc97e02ad06ebfda098f05056c2d0e6184fca7f66daf15186b32160f2a0c7fbf` |
| `tests/test_policy_test_runner_summary.py` | `8f0dbfc2e51691d4cdb1b9de946802ba3247d9f724f2a08e64b0fc72b4acb129` |
| `tests/test_declaration_red_map_check.py` | `901a4ea19a9945a615f3328122f9a759820eea1bd126cf4a29e410e94a23fe42` |
| `tests/test_declaration_red_verification.py` | `9fd15c8e38cce1ca05e1a50cde8c2366daa72a719f96d490557e2e55b62e5b49` |
| `tests/test_red_verification_collection_error.py` | `856eea001f39a40522e7291a0aade998291d12ed338e60af8e4b5e7b56f18164` |
| `tests/test_work_unit_transition.py` | `9b488d4e348316a8c3a98d27321e5176ccb55a8b7e341c029a9f583a71b8f986` |

【記録】`policy_test_runner.py`と`pytest_summary.py`は、pytestの機械的なreport objectから
公式Test receiptの件数を作り、stdout文字列から件数を抽出しない契約である。
`declaration_red_map_check.py`は、宣言、列挙test、実在testの対応と`red_now`主張を
fail-closedで検査する。`docs/development/2026-08-02-development-policy.md`の
「作業単位終端のcommit reminder Pilot」は、`completed`かつdirtyなら次作業を停止する。

【実測】既存testは、通常の合格・失敗、summary欠落とfield不整合、setup error、skip、
xfail、xpass、対応表のfile内双方向不一致、収集errorのRED扱い、通常のtracked・untracked dirtyを
覆う。一方、今回使った実行前から残る正しい形式のsummary、receipt出力先とsource fileの同一化、
同じnode idの重複report、pytest自体の収集error集計、空のcomplete対応表、偽boolean、root外test、
`skip-worktree`、別Git rootへの差替えは既存fixtureになかった。

## 3. 既存testと公式全Testの独立再実行

【実測】次の単独commandは終了コード0、`46 passed in 1.32s`だった。

```text
env PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' .venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py tests/test_policy_test_runner_receipt_identity.py tests/test_policy_test_runner_summary.py tests/test_declaration_red_map_check.py tests/test_declaration_red_verification.py tests/test_red_verification_collection_error.py tests/test_work_unit_transition.py tests/test_adversarial_remedy_batch1.py
```

【実測】公式全Testは元repositoryを書き換えないため、一時領域
`/private/tmp/codex-group-b-full-tree-v1`へworktreeと`.git`を複製し、`.venv`だけを元環境へ
symlinkして実行した。隔離copyの`git status --short`は実行前に空で、対象4 moduleのDigestは上表と
一致した。receiptはproject root外へ置いた。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/codex-group-b-official-isolated-receipt-v1.json
```

結果は終了コード0、status `passed`、`1381 passed`、failed 0、errors 0、skip・xfail・xpass 0、
Python 3.9.6、pytest 8.4.2、fallback falseだった。receipt SHA-256は
`bebc61a5a66ea52d8631a48b0a037fe36d7fd32cb1578e537e09a3a94179b7e7`である。

【実測】隔離方法の確定前に、元repositoryへ書かないための環境変数を付けた2回と、`.git`を除いた
隔離copyで1回実行した。前2回は対象外のcache環境契約testが各1件失敗して`1 failed, 1380 passed`
（終了コード1）、後1回は履歴参照test 17件が失敗して`17 failed, 1364 passed`（終了コード1）だった。
原因を切り分け、環境変数を外し`.git`も一時copyへ含めた上記最終runだけを全Test判定に使った。

## 4. 既存fixtureにない反証

### 4.1 実行環境と一時領域

【実測】反証はPython 3.9.6、`macOS-26.5.1-arm64-arm-64bit`で実行した。
反証harnessは`/private/tmp/codex_group_b_adversarial.py`だけに置き、そのSHA-256は
`73efaa400ac09051ad017668ece3aef41c09f30b5008c65dee3f5de9a89b1b7a`だった。
fixture、Git repository、receipt、summaryは各caseの`TemporaryDirectory(dir="/private/tmp")`だけへ
作成し、case終了時に消去した。repository内、実台帳、実設定、利用者環境への書込みは行っていない。

以下の終了コード1は、harness異常ではなく「安全側なら拒否または不一致を検出する」という独立oracleに
反して対象moduleが合格したことを表す。終了コード0は期待どおりの切分け結果である。

### 4.2 実行一覧

各commandの`<case>`は、同一command末尾のcase名である。

| ID | command | 結果 | 終了コード |
| --- | --- | --- | --- |
| P1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py policy_stale_summary` | 実際は`1 passed`だが、実行前から残した正しい形式のsummaryを再利用し、receiptは`999 passed`、status `passed` | `1` |
| P2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py policy_nonpass_outcomes` | 失敗するassertだけをskip 1件・xfail 1件にすると、passed 0のまま公式status `passed` | `1` |
| P3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py policy_receipt_overwrite` | receipt先を`tests/test_only.py`にすると、Test合格後にsourceをreceiptで置換し、そのpathを`source_state_digest`から除外したままstatus `passed` | `1` |
| S1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py summary_duplicate_nodeid` | 同じ`nodeid`の同一call reportを2回渡すと、unique node 1件を`passed=2,total=2`と確定 | `1` |
| S2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py summary_collection_error` | pytest収集errorでpytest終了コード2だが、summaryは`errors=0,total=0` | `1` |
| S3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py summary_outcomes` | setup skip、xfail、xpass、teardown errorをそれぞれ1件へ分離して`skipped=1,xfailed=1,xpassed=1,errors=1,total=4` | `0` |
| D1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py declaration_empty_complete` | project内に未列挙の失敗testがあっても、空の`complete` map（宣言0・file 0）をstatus `passed` | `1` |
| D2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py declaration_invalid_red_type` | JSON文字列`"false"`をbooleanとして拒否せずtruthyへ変換し、実際に失敗するtestを`verified=1`、status `passed` | `1` |
| D3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py declaration_path_escape` | `../outside.py`をtest fileと宣言したroot外参照をstatus `passed` | `1` |
| W1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py transition_skip_worktree` | HEADとbytesが違うtracked fileへ`skip-worktree`を付けるとporcelainは空になり、status `passed`、`next_work_allowed=true` | `1` |
| W2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py transition_wrong_root` | actual rootはdirtyでstatus `blocked`だが、引数を別のclean Git rootへ差し替えるとstatus `passed` | `1` |
| W3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_b_adversarial.py transition_receipt_agnostic` | fake・stale receiptは関数入力でなく、clean Git rootのstatusは`passed`のまま | `0` |

### 4.3 代表的な機械出力

【実測】P1は次を出力した。

```json
{"actual_test_files": 1, "pytest_stdout": ". [100%]\n1 passed in 0.00s", "receipt_passed": 999, "runner_exit_code": 0, "runner_status": "passed"}
```

【実測】P2の`test_summary`は次だった。

```json
{"errors": 0, "failed": 0, "passed": 0, "skipped": 1, "total": 2, "xfailed": 1, "xpassed": 0}
```

【実測】D1はfindingなしで次を返した。

```json
{"findings": [], "machine_count": {"declarations": 0, "declarations_without_tests": 0, "listed_tests_missing_in_file": 0, "tests_unmapped_to_declarations": 0}, "status": "passed"}
```

【実測】W1は次を返した。

```json
{"gate_status": "passed", "next_work_allowed": true, "porcelain": "", "working_bytes_differ_from_head": true}
```

## 5. moduleごとの判定（§4.7）

| module | 判定 | Evidenceと理由 |
| --- | --- | --- |
| `tools/development/policy_test_runner.py` | `reported_unverified` | 通常の公式全Testは合格したが、P1で古いsummaryを現在runの件数として受理し、P2でpassed 0のskip・xfailだけのsuiteを公式合格とし、P3でsourceとreceipt出力先の同一化を拒否しなかった。F-B1・F-B2により`verified`にできない |
| `tools/development/pytest_summary.py` | `reported_unverified` | S3の通常分類はdocstringどおりだったが、S1で同一nodeを重複計上し、S2で収集errorを0件とした。F-B3により`verified`にできない |
| `tools/development/declaration_red_map_check.py` | `reported_unverified` | 既存のfile内双方向検査とRED実行照合は合格したが、D1〜D3でcomplete範囲の全省略、偽boolean、project root脱出をすべて合格させた。F-B4により`verified`にできない |
| `tools/development/work_unit_transition.py` | `reported_unverified` | 通常dirtyは停止したが、W1でHEADと異なるtracked bytesをcleanとし、W2で検査rootを差し替えてdirtyな対象rootを迂回できた。F-B5により`verified`にできない |

【判断】4 moduleすべてにblocking Findingが対応するため、group Bの総合判定は
`reported_unverified`である。§6が定める再現条件不足ではなく、§11.1類型3または4の機械反証を
根拠とする。固定された完了報告と事後状態の競合はないため`report_execution_mismatch`ではない。
範囲固定§8.3はblocking検出を停止条件にせずrecordへ固定してgroupを完了させるため、`blocked`でもない。

## 6. Finding（§11）

### F-B1 blocking／implementation／§11.1類型3

対象：`tools/development/policy_test_runner.py`

【実測】P1では現在runが1件だけ合格したにもかかわらず、実行前からsummary出力pathに置いた
構造上正しい`999 passed`を現在runの集計として受理し、公式status `passed`のreceiptを作った。
P2では失敗するassert 2件をskip・xfailにしたsuiteが、実合格0件でも公式status `passed`になった。

【判断】summaryをrun開始前にnew-onlyへせず、現在runが書いたことも束縛しないため、古い件数を
現在の公式Evidenceとして誤って合格させる。さらに「失敗またはerrorが0」だけを合格側の整合条件とし、
実合格0件を拒否しない。公式Test receiptに誤った合格を作れる§11.1類型3のblockingとする。
同じ「非合格結果だけで公式合格」の変種としてskipとxfailを本周回で確認した。error・収集errorは
pytest終了コードが非0となりrunner status自体は`failed`だった。

### F-B2 blocking／implementation／§11.1類型3・4

対象：`tools/development/policy_test_runner.py`

【実測】P3ではreceipt出力先を実行対象のtest sourceそのものに指定できた。runnerはそのsourceを
`source_state_digest`から除外してTestを実行し、合格後にsourceをreceipt JSONへ置換した。

【判断】receipt pathを許可領域またはsource外へ制限せず、sourceと同一でも除外するため、receiptが
表す入力同一性から実行sourceを欠落させたまま公式合格を作れる。またsource fileを書換えるpath境界を
許す。誤った合格の類型3とscope境界破りの類型4に該当するblockingとする。

### F-B3 blocking／implementation／§11.1類型3

対象：`tools/development/pytest_summary.py`

【実測】S1では`nodeid`を一切参照せず、同一testの同一call report 2件を2 passedとして確定した。
S2ではpytestの収集errorで終了コード2だったが、hook対象が`pytest_runtest_logreport`だけのため
summaryを`errors=0,total=0`として確定した。

【判断】receiptの構造検証は内訳合計だけを確認するため、重複計上と収集error欠落の両方を正しい件数
として受理する。実行件数の公式Evidenceを誤って合格させる§11.1類型3のblockingとする。
同じ集計類型のsetup、teardown、skip、xfail、xpassはS3で期待どおり分離された。

### F-B4 blocking／implementation／§11.1類型3・4

対象：`tools/development/declaration_red_map_check.py`

【実測】D1では`scope.kind=complete`でも`test_files`と`declarations`を共に空にすると、project内の
失敗testを一切検査せずstatus `passed`となった。D2ではbooleanでない`"false"`を拒否せず、
`bool("false") == True`として実際の失敗と一致させた。D3ではproject root外の`../outside.py`を読み、
対応表の対象として合格させた。

【判断】検査対象集合を対応表自身からだけ作るため、宣言とfileを同時に省略する偽装を検出できない。
また`red_now`の型とtest fileのroot内境界を閉じていない。TDD対応表を誤って合格させる類型3と
project scope境界を破る類型4のblockingとする。同じ宣言逃れの変種として全省略、型偽装、path脱出を
本周回で一括掃討した。

### F-B5 blocking／implementation／§11.1類型3

対象：`tools/development/work_unit_transition.py`

【実測】W1ではtracked fileのbytesがHEADと異なるにもかかわらず、Git indexの`skip-worktree`により
porcelain出力が空となり、`next_work_allowed=true`になった。W2ではdirtyなactual rootへの同関数結果は
`blocked`だったが、引数を別のclean Git rootへ差し替えると`passed`になった。

【記録】上流方針とRED Evidenceは「`completed`かつdirtyなら次作業を停止する」としている。

【判断】porcelain文字列以外にHEADとのbytes差や対象repository identityを束縛しないため、完了済みの
未コミット変更があっても遷移を合格させられる。commit関門の偽陰性を機械実証した§11.1類型3の
blockingとする。同じ迂回類型のindex非表示とroot差替えを本周回で確認した。

### non-blocking／defer

【判断】non-blocking Findingは0件、defer Findingは0件である。fake・stale receiptは
`work_unit_transition.py`の入力ではなく、このmoduleの現契約はTest鮮度を主張しないため、W3を
同moduleのFindingにはしない。receipt生成後の改竄検出も、現行のGit・固定SHAによる事後照合と分け、
本moduleだけへ未承認の新しいreceipt schemaを要求しない。

## 7. Human境界、禁止事項、未実施

【実測】反証・公式全Testの前後で元repositoryの`git status --short`は空だった。反証は一時領域だけを
使い、対象code、test、既存record、実台帳、実設定、利用者環境を変更していない。外部送信、不可逆操作、
push、tag、履歴書換えも行っていない。

未実施：F-B1〜F-B5の修正、新規test作成、既存test変更、TODO・checklist反映、group A修正、
group C以降のレビュー、Closer作業、外部操作。

【判断】risk `low`は成果物が本レビューrecord 1件だけであることに対するHuman確定であり維持した。
守り役code自体の判定では、依頼どおり既存fixture外の独立反証と隔離した公式全Testを追加した。

## 8. 判定と次のHuman判断

判定：`reported_unverified`。

【判断】レビュー作業と本recordは完了したが、対象4 moduleはF-B1〜F-B5により`verified`ではない。
blockingを修正せず、禁止された実装変更を未実施のまま保持した。

次：Humanが本Findingを確認し、現行Plan上で次のいずれかを選ぶ。

1. いま対処：F-B1〜F-B5を、守り役code修正の別`high` risk作業単位として範囲固定する。
2. 候補として後回し：Findingを未解消のまま保持し、修正候補へrouteする。
3. 本線へ戻る：本groupの修正には着手せず、固定済み第2単位のgroup Cレビューへ進む。
