# 守り役後追い独立レビュー #6第2単位 group C 判定 v1

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
- レビュー開始時HEAD：`46f246525c4a2714d5067e45e048ff47e72ea150`
- branch：`main`
- 先行：group A `17613d2`、group B `46f2465`は完了済み。両groupの修正は本scope外
- 対象：`tools/development/todo_handoff.py`、
  `tools/development/todo_update_path.py`
- 許可範囲：対象と既存testの読取り、一時領域での反証、本判定recordの新規作成と単独commit
- 禁止範囲：code、test、既存record、実TODO、実台帳、実設定、利用者環境の変更、外部操作、
  Findingの修正、TODO・checklist反映、先行groupの修正
- 期待成果：moduleごとの§4.7判定、§11区分のFinding、反証のcommand・結果・終了コード、
  model来歴を持つ本record 1件と、その単独commit
- 停止条件：固定入力Digest不一致、許可path外の変更が必要な場合

【記録】Humanは2026-08-10に「#6第2単位 risk lowを確定、着手を承認する」と明示した。

【実測】開始時のworktreeとindexはcleanだった。HEADは範囲固定commitと先行group Aの後にある
group B単独commit `46f2465`である。`git diff --name-status bedf986 -- <group C 2 moduleと直接test>`は
出力なしで、対象実装と直接testが範囲固定後に変わっていないことを確認した。

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

【実測】対象2 module、直接test、TODO共通手順、Git欄安定化Decision、TODO生成Plan承認Decisionを
再読込みした。対象bytesのSHA-256は次のとおり。

| 対象 | SHA-256 |
| --- | --- |
| `tools/development/todo_handoff.py` | `fbc6279b6471913f490b604940c14ef792b139e35819c951a0e4406ce5994d61` |
| `tools/development/todo_update_path.py` | `3396e9d8131c8059661a7a264503faafe7ad1d5b8af96b09d9483385e873bd31` |
| `tests/test_todo_handoff_git_state.py` | `c4f6ff744c442536c6e83f9d476092b9f82d0f308a02e64920e7eeaeb2d3d426` |
| `tests/test_todo_update_path.py` | `220d68e5bd2a3c8c1b1900d1393cbccded943062fefc307a1dafff85fc6004f1` |

【記録】`RC3-COMMIT-HANDOFF-STABILITY-DECISION-2026-08-04-V1`は、TODOを含むcommit自身のSHA、
数値付きahead／behind、push済否、一時的な未コミット状態をGit欄へ保存せず、不安定なGit欄を
決定的validatorで拒否する。TODO共通手順は、branchを含む状態導出、Digest、件数、Git確認を
機械処理にし、`todo_handoff`をcommit安定Git欄を含む単一検証入口としている。

【記録】`DEC-RECORD-GENERATION-PLAN-001`は、公式Test receipt（受領証）の構造化集計からTODOを
更新し、二段確認の不一致または更新失敗では原状復帰する。`todo_update_path.py`の契約は、
一時receiptによる候補の書込み・検証後に公式全Testを再実行し、二つの集計、suite、Python版、
pytest版、fallback、statusを完全一致させる。自由文、link、順序など非機械管理部分は変えない。

【実測】既存testは、7文字以上の小文字SHA、完全一致するGit見出しの欠落・重複、欄外のcommit
Evidence、通常の二段一致、集計・版の不一致、候補書込み後のread-back不一致、validator失敗、
第1・第2実行の例外、危険な引数path、原状復帰を覆う。一方、今回試した4文字SHA、大文字SHA、
実branchとの不一致、末尾空白付き見出し、欄外の可変Git snapshot、全角空白、無効な第2receipt、
同一receipt再利用、第2実行中のTODO差替え、CRLF改行は既存fixtureになかった。

## 3. 既存testと公式全Testの独立再実行

【実測】次の単独commandは終了コード0、`33 passed in 0.07s`だった。

```text
env PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS=-p\ no:cacheprovider .venv/bin/python3 -m pytest -q tests/test_todo_handoff_git_state.py tests/test_todo_update_path.py
```

【実測】公式全Testは元repositoryへ書かないため、一時領域
`/private/tmp/codex-group-c-full-tree-v1`へ`.venv`を除くworktreeと`.git`を複製し、複製内の
`.venv/`だけを元環境の4要素へのsymlinkで構成して実行した。実行前後の複製側
`git status --short --branch`はbranch行だけで、tracked・untracked差分はなかった。対象2 moduleの
Digestは元repositoryと一致した。receiptはproject root外へ置いた。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/codex-group-c-official-isolated-receipt-v1.json
```

結果は終了コード0、status `passed`、`1381 passed`、failed 0、errors 0、skip・xfail・xpass 0、
Python 3.9.6、pytest 8.4.2、fallback falseだった。receipt SHA-256は
`d440654707fc5458376eea76159da762637271f70ea14e3b52e5f0b8593a8335`である。

## 4. 既存fixtureにない反証

### 4.1 実行環境と一時領域

【実測】反証はPython 3.9.6、pytest 8.4.2、`macOS-26.5.1-arm64-arm-64bit`で実行した。
反証harness（反証を自動実行する一時スクリプト）は`/private/tmp/codex_group_c_adversarial.py`だけに
置き、最終版SHA-256は`7d206760ad433e026d98c7f3e59087e33eda104ffdbbe05534a15efd366197a0`
だった。各TODO、Issue record、参照file、Git repository、receiptはcaseごとの
`TemporaryDirectory(dir="/private/tmp")`だけに作成し、case終了時に消去した。

以下の終了コード1は、harness異常ではなく「安全側なら拒否または不一致を検出する」という独立oracle
に反して対象moduleが合格したことを表す。H6はBOM・CRLF・順序入替えの対照結果も同時に記録した。

### 4.2 有効な反証の実行一覧

各commandの`<case>`は、同一command末尾のcase名である。

| ID | command | 結果 | 終了コード |
| --- | --- | --- | --- |
| H1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py handoff_short_sha` | GitがHEADとして解決する4文字SHA `46f2`をGit欄へ置いても単一入口が`passed` | `1` |
| H2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py handoff_uppercase_sha` | Gitが同じHEADへ解決する40文字大文字SHAをGit欄へ置いても`passed` | `1` |
| H3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py handoff_branch_mismatch` | 一時Git repositoryの実branchは`main`だが、存在しないbranch名の記載を`passed`。実Gitを作るよう強化した再実行も同じ結果 | `1` |
| H4 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py handoff_alias_duplicate` | 正規見出しに加え、末尾空白付き`## Git・Test `へHEAD、push済み、ahead／behind 0を置いても`passed` | `1` |
| H5 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py handoff_outside_snapshot` | `## 補足Git状態`へHEAD、push済み、ahead／behind 0を置いても`passed` | `1` |
| H6 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py handoff_boundary_controls` | BOM、CRLF、必須3行の順序入替えは`passed`。worktree必須文の前を全角空白にしてbullet外へ出しても`passed` | `1` |
| U1 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py update_second_identity_forgery` | 第2receiptを未知kind・偽runner・exit 9・浮動小数件数・fallback 0にしても更新成功。独立receipt validatorは拒否 | `1` |
| U2 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py update_same_receipt_replay` | CLI引数は別receipt pathだがexecutorが両段で第1receiptを返すと終了コード0。最終receipt fileは存在しないまま`status=updated` | `1` |
| U3 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py update_second_phase_swap` | 第2Test中に検証済みTODOを不正bytesへ差し替えても関数は成功を返し、返却候補と実TODOが不一致。独立TODO validatorは拒否 | `1` |
| U4 | `env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 /private/tmp/codex_group_c_adversarial.py update_crlf_preservation` | CRLF 22個のTODOを更新するとCRLF 0個、LF 22個へ全面変換し、非機械管理部分のbytesも変えたまま成功 | `1` |

### 4.3 harness準備失敗と訂正

【実測】最初の並列実行ではH1〜H3が上表の欠陥を再現した一方、H4〜H6・U1〜U4の7 commandは、
一時harnessの`_workspace()`が既定行の変数名を取り違え、対象moduleへ到達する前に
`TypeError: Value after * must be an iterable, not NoneType`で終了コード1となった。この7結果は
反証Evidenceに数えていない。一時harness内だけで`*git_lines`を`*lines`へ訂正し、同じ7 commandを
再実行した結果が§4.2である。H3は一時project自身をGit repositoryにする強化後にも再実行し、
終了コード1で同じ偽陰性を確認した。

### 4.4 代表的な機械出力

【実測】H3は次を出力した。

```json
{"actual_branch": "main", "claimed_branch": "branch-that-does-not-exist", "status": "passed"}
```

【実測】U1では`todo_update_path`が未知kindとexit code 9を受理した一方、独立validatorは拒否した。

```json
{"accepted_exit_code": 9, "accepted_receipt_kind": "forged_receipt", "independent_validator": {"error": "receipt_invalid: forged_receipt", "status": "rejected"}, "todo_changed": true}
```

【実測】U2は実在しない最終receiptを成功出力へ記載した。

```json
{"cli_exit_code": 0, "cli_output": {"final_receipt": "records/development/final.json", "first_receipt": "records/development/first.json", "status": "updated", "test_summary": {"errors": 0, "failed": 0, "passed": 7, "skipped": 0, "total": 7, "xfailed": 0, "xpassed": 0}}, "final_receipt_exists": false}
```

【実測】U3は成功返却後の実TODOを独立validatorが`git_section_missing`で拒否した。

```json
{"calls": ["first", "second"], "function_returned": true, "independent_validator": {"error": "todo_verification_failed: git_section_missing", "status": "rejected"}, "returned_bytes_match_actual": false}
```

## 5. moduleごとの判定（§4.7）

| module | 判定 | Evidenceと理由 |
| --- | --- | --- |
| `tools/development/todo_handoff.py` | `reported_unverified` | 既存testと通常形式は合格したが、H1〜H2でGitが解決できる禁止SHA表現、H3で実branchと異なる現在地、H4〜H6で別表現・別節の可変Git状態をすべて合格させた。F-C1・F-C2により`verified`にできない |
| `tools/development/todo_update_path.py` | `reported_unverified` | 通常の二段一致・不一致・復帰は既存testどおりだったが、U1〜U2で無効・再利用receiptを最終確認として合格させ、U3で第2実行中の差替え後も成功し、U4で非機械管理bytesを変えた。F-C3〜F-C5により`verified`にできない |

【判断】2 moduleすべてにblocking Findingが対応するため、group Cの総合判定は
`reported_unverified`である。§6が定める再現条件不足ではなく、§11.1類型3または4の機械反証を
根拠とする。固定された完了報告と事後状態の競合はないため`report_execution_mismatch`ではない。
範囲固定§8.3はblocking検出を停止条件にせずrecordへ固定してgroupを完了させるため、`blocked`でもない。

## 6. Finding（§11）

### F-C1 blocking／implementation／§11.1類型3

対象：`tools/development/todo_handoff.py`

【実測】H1ではGitが現在HEADへ解決する4文字SHA、H2では同じHEADへ解決する40文字大文字SHAを
Git欄へ保存しても合格した。H3では一時Git repositoryの実branchが`main`であるのに、存在しない
`branch-that-does-not-exist`を記載しても合格した。

【判断】SHA検出を7〜40文字の小文字だけに限定し、branch記載を実Gitへ照合しないため、禁止された
自己SHA snapshotと誤った現在branchを正しいGit欄として合格させる。commit安定Git欄と現在地の
誤った合格を実証した§11.1類型3のblockingとする。同じGit偽装類型の短縮形・大文字形・branch差替えを
本周回で一括確認した。

### F-C2 blocking／implementation／§11.1類型3・4

対象：`tools/development/todo_handoff.py`

【実測】H4では末尾空白付きの別名Git見出しに禁止snapshotを置き、H5では別のGit状態節へ同じ内容を
置いても合格した。H6ではworktree必須文を全角空白でbullet外へ出しても、節内substringとして合格した。

【判断】完全一致する見出しだけを対象節として数え、必須文は行構造でなく部分文字列で探すため、
意味上の重複欄、欄外へ逃がした可変Git状態、非正規行を検査範囲外にできる。単一Git欄の誤った合格を
作る類型3と、検査scope境界を別表現で破る類型4のblockingとする。同じ欄境界逃れの見出し末尾、
別見出し、Unicode空白を本周回で確認した。

### F-C3 blocking／implementation／§11.1類型3

対象：`tools/development/todo_update_path.py`

【実測】U1では第2receiptを未知kind、偽runner、exit code 9、浮動小数の件数、整数0のfallbackへ
変えても二段更新が成功した。第1receiptだけは候補生成時に検証されるが、第2receiptは独立validatorが
`receipt_invalid`で拒否する内容だった。U2ではCLI引数の2 pathが異なっていても、executorが両段で
同じ第1receipt pathを返すと、最終receipt fileが無いまま終了コード0と`status=updated`になった。

【判断】第2receiptの構造・実行結果・identityを検証せず、比較fieldではPythonの`False == 0`や
整数と同値の浮動小数も一致とする。また要求pathとexecutorが返した実pathを束縛しないため、無効receipt
または第1receiptの再利用を「二度目の公式実行」として合格させられる。数値と実状態を誤って合格させる
§11.1類型3のblockingとする。同じ二段確認迂回の内容偽造・型偽装・path再利用を本周回で確認した。

### F-C4 blocking／implementation／§11.1類型3・4

対象：`tools/development/todo_update_path.py`

【実測】U3では候補のread-backとvalidatorが終わった後、第2公式Test callback内でTODOを
`tampered after verification`へ差し替えた。二つのreceiptが一致すると関数は成功を返し、返却した
`todo_bytes`と実TODOは不一致、実TODOは独立validatorで拒否された。

【判断】第2実行後にTODOのread-back・再検証・候補bytesとの同一性確認がないため、確認途中の差替えや
並行更新を未検証のまま確定できる。二段確認の誤った合格である類型3とtransaction境界破りの類型4に
該当するblockingとする。途中差替えと並行更新は同じ最終同一性欠落へ収束するため、本反証で同周回の
変種を代表させる。

### F-C5 blocking／implementation／§11.1類型4

対象：`tools/development/todo_update_path.py`

【実測】U4ではCRLF改行22個を持つTODOを正常二段更新すると、成功した候補はCRLF 0個、LF 22個に
なった。機械管理対象の全Test行だけでなく、自由文、見出し、linkを含む全行の改行bytesが変わった。

【記録】同moduleの契約は、自由文、link label、link path、順序を変えず、非機械管理部分の既存bytesを
そのまま保つとしている。

【判断】`Path.read_text()`の改行変換後に全文を再encodeするため、機械管理外bytesまで書き換える。
許可された更新範囲を越える§11.1類型4のblockingとする。BOM付きUTF-8はH6の読取り検証で合格し、
全角空白はF-C2として分離した。

### non-blocking／defer

【判断】non-blocking Findingは0件、defer Findingは0件である。必須3行の順序入替えは上流が固定順を
受入条件にしていないためFindingにしない。BOMとCRLFの読取り合格自体もFindingにせず、CRLF更新時の
scope外bytes変更だけをF-C5とした。確認tokenは現契約に存在しないため、新しいtoken設計は要求せず、
既存のreceipt identityと二つの実pathの束縛欠落をF-C3として判定した。

## 7. Human境界、禁止事項、未実施

【実測】反証・公式全Testの前後で元repositoryの`git status --short`は空だった。反証は一時領域だけを
使い、対象code、test、既存record、実TODO、実台帳、実設定、利用者環境を変更していない。外部送信、
push、tag、amend、rebase、reset、履歴書換えも行っていない。

未実施：F-C1〜F-C5の修正、新規test作成、既存test変更、TODO・checklist反映、先行group修正、
group D以降のレビュー、Closer作業、外部操作。

【判断】risk `low`は成果物が本レビューrecord 1件だけであることに対するHuman確定であり維持した。
守り役code自体の判定では、依頼どおり既存fixture外の独立反証と隔離した公式全Testを追加した。

## 8. 判定と次のHuman判断

判定：`reported_unverified`。

【判断】レビュー作業と本recordは完了したが、対象2 moduleはF-C1〜F-C5により`verified`ではない。
blockingを修正せず、禁止された実装変更を未実施のまま保持した。

次：Humanが本Findingを確認し、現行Plan上で次のいずれかを選ぶ。

1. いま対処：F-C1〜F-C5を、守り役code修正の別`high` risk作業単位として範囲固定する。
2. 候補として後回し：Findingを未解消のまま保持し、修正候補へrouteする。
3. 本線へ戻る：本groupの修正には着手せず、固定済み第2単位のgroup Dレビューへ進む。
