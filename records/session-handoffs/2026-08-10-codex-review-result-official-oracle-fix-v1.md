# group B 公式検証oracle修正 完了レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion
- risk：`high`
- 対象：`records/session-handoffs/2026-08-10-claude-pilot-official-oracle-fix-review-request-v1.md`
  （commit `c5d7db364a199f94caea2fffb4ad10fca854995f`）
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`
- 総合判定：`report_execution_mismatch`（要修正）
- 停止類型：`report_execution_mismatch`
- Finding：blocking 2件、non-blocking 1件、defer 0件

## 1. 判定と停止根拠

判定：`report_execution_mismatch`（要修正）。`verified`ではない。

【記録】レビュー依頼§3は、F-B5について、porcelainが空でもHEADとのbytes差があれば停止し、
別Git rootへの差し替えを拒否するとClaimしている。Evidence §6.1はP1〜P3・S1〜S2・
D1〜D3・W1〜W2の10反証がすべて拒否または`failed`になったとClaimしている。

【実測】W1とW2を使い捨てGit repositoryで再実行すると、どちらも現在実装で
`status=passed`、`next_work_allowed=true`となった。したがって、上記Claimと
commit `c5d7db3`の事後状態は競合する。

停止根拠は次の2件である。

1. W1：`skip-worktree`で追跡fileの変更をGit表示から隠すと、作業bytesはHEADと異なるのに
   `git status --porcelain`と`git diff --name-only HEAD --`が共に空となり、完了関門が合格する。
2. W2：dirtyな対象repositoryの代わりに別のclean Git repositoryを`project_root`へ渡すと、
   そのrootの`rev-parse --show-toplevel`は要求root自身を返すため、identity検査を通過して合格する。

【判断】これは`work-review-protocol.md` §4.7・§6・§11.1が定める、競合Evidenceを列挙した
`report_execution_mismatch`である。影響を受けるレビュー依頼§3のF-B5 Claim、Evidence §6.1、
F-B1〜F-B5をすべて解消したという完了Claimはstaleである。公式全Testの合格Claimは、§4の独立実行で
一致しており、それ自体はstaleにしない。

## 2. 固定対象、開始状態、commit列

- base：`271826a544e40db6b66640be785444204d9930f5`
- 対象HEAD：`c5d7db364a199f94caea2fffb4ad10fca854995f`
- branch：`main`
- 開始時worktreeとindex：clean
- 許可範囲：読取り、一時領域での反証と隔離実行、本record 1件の新規作成と単独commit
- 禁止範囲：code、test、既存record、config、schema、上流設計、TODO、checklistの恒久変更、
  外部送信、push、tag、履歴書換え、Closer作業

【実測】commit列は次の直線であり、親SHAも連続していた。

| commit | 役割 | 変更pathの実測 |
| --- | --- | --- |
| `c5cd440` | SCOPE v1 | scope v1 1件の追加だけ |
| `134fed4` | 範囲レビュー | 範囲レビューrecord 1件の追加だけ |
| `34e8a59` | RED | 許可されたtest 4件だけ。299行追加、削除0 |
| `4fda1a6` | SCOPE v2 | scope v2 1件の追加だけ |
| `e07183d` | 修正RED | `tests/test_work_unit_transition.py` 1件だけ |
| `f8c01b5` | GREEN | 実装4件、`conftest.py`、新規Evidence、receiptに加え、既存契約v2を変更 |
| `c5d7db3` | review request | レビュー依頼record 1件の追加だけ |

【実測】各commitに対する単独の`git diff --check <parent> <commit>`は7／7で終了コード0だった。

## 3. 反証10件の逐一照合

反証用harnessは`/private/tmp`だけへ置き、各fixtureは
`TemporaryDirectory(dir="/private/tmp")`でcaseごとに作成・消去した。harness SHA-256は
`03d35dfb4e8bf7e5b6fc85fc2bb3b3a395b49a770d9ac3a3718dbec92500bfa0`。
次表のharness終了コードは、`0`が反証不成立、`1`が反証成立を表す。

| ID | 同じ危険入力の独立結果 | harness終了コード | 照合 |
| --- | --- | ---: | --- |
| P1 | 実行前から在る`999 passed`のsummaryを`test_summary_stale`で拒否。receiptなし | 0 | 不成立 |
| P2 | skip・xfailだけでpassed 0のsuiteを`test_summary_inconsistent`で拒否。receiptなし | 0 | 不成立 |
| P3 | 既存`.py`をreceipt先にすると`receipt_path_invalid`で拒否。source bytes不変 | 0 | 不成立 |
| S1 | 同じnodeid・call report 2件を`passed=1,total=1`と集計 | 0 | 不成立 |
| S2 | 収集errorでpytest終了コード2、`errors=1,total=1` | 0 | 不成立 |
| D1 | 空のcomplete対応表を2 findingつき`failed` | 0 | 不成立 |
| D2 | 文字列`"false"`を`red_now_not_boolean`で検出し`failed` | 0 | 不成立 |
| D3 | `../outside.py`を`test_file_outside_project_root`で検出し`failed` | 0 | 不成立 |
| W1 | `skip-worktree`後にbytesを変更しても`passed`、`next_work_allowed=true` | 1 | **成立** |
| W2 | dirtyなactual rootは`blocked`だが、cleanなdecoy rootは`passed` | 1 | **成立** |

【判断】10件中8件は不成立、2件は成立である。「すべて不成立」という受入条件1を満たさない。

### high riskの追加反証

【実測】Pilot fixtureにない同類型の変種として、追跡fileへ`assume-unchanged`を設定してから
bytesを変更した。porcelainとHEAD diffは共に空となり、現在実装は`passed`、
`next_work_allowed=true`を返した。harness終了コードは1で、反証は成立した。

【判断】W1と同じ「Gitの表示から作業bytes差を隠す」類型は、`skip-worktree`だけに閉じず
`assume-unchanged`でも残る。

## 4. 正例、対象Test、公式全Test

### 4.1 対象Test

【実測】次の単独commandは終了コード0、`48 passed in 1.70s`だった。

```text
env PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' .venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py tests/test_policy_test_runner_summary.py tests/test_policy_test_runner_receipt_identity.py tests/test_declaration_red_map_check.py tests/test_declaration_red_verification.py tests/test_work_unit_transition.py
```

【判断】対象Testが全件合格してもW1・W2の実入力は合格するため、この48件だけではF-B5の
受入条件を検査できていない。

### 4.2 公式全Testと独立件数

【実測】元repositoryを汚さないよう、HEAD `c5d7db3`を`/private/tmp`へlocal cloneし、
`.venv`だけをcloneのGit内部除外へ登録して公式runを実行した。追加の環境変数を付けない最終runは
終了コード0、status `passed`、`1465 passed`、failed 0、errors 0、skipped 0、total 1465だった。
一時receipt SHA-256は`ec76f43c40e8bdcd753f7c8653ae88746161f17d09de1db8671757be8677c1d7`。
cloneの`git status --short`は実行前後とも空だった。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt <一時領域>/official-receipt.json
```

【実測】別の一時pluginでpytestの`session.items`を数えた収集runは、終了コード0、
`independent_collected=1465`だった。公式receiptの`passed=1465,total=1465`と一致した。

【判断】`conftest.py`への収集error結線は、正常runの件数を歪めていない。受入条件2の正例側と
公式全Test合格は成立する。

【記録】隔離方法を確定する前の2 runは最終判定に使っていない。1回目はcloneの`.venv` symlinkが
未追跡となり作業木検査1件が失敗、2回目は呼出し側の`PYTHONDONTWRITEBYTECODE=1`を継承して
cache契約Test 1件が失敗し、いずれも`1 failed, 1464 passed`、終了コード1だった。原因を除いた
上記最終runだけを公式全Testの判定に使った。

## 5. REDと検査性質

RED／GREENのcheckoutはrepositoryを直接切り替えず、各commitの`git archive`を
`/private/tmp`へ展開して行った。展開領域は実行後に消去した。再現harness SHA-256は
`bfa01bcfb7797f4a10732d1f185a0835b4d1e97edc63a52ee1d3b0d8cb637ff4`。

【実測】RED commit `34e8a59`の対象6 fileは終了コード1、`13 failed, 35 passed`だった。

【実測】修正RED `e07183d`の
`test_preflight_reads_git_state_mechanically`は、修正前実装Digest
`de131c00baef55799b6222aec578c2ad4e960b5e56df8a0b97fcdabd998d434e`で終了コード1、`1 failed`。
GREEN `f8c01b5`の修正後実装Digest
`91726ff02cc7f86318c139913ec75d464521d2d7f389ed26cc227a45c88cb97e`で終了コード0、`1 passed`だった。
両runのtest SHA-256は同じ
`d4b4f63af8b820d06cfcbdf101b71d26f49bfe265fe4d739aa00ebe0c857ea40`だった。

【判断】修正REDの既存testは、修正前後を区別し、「Git状態を機械的に読み、変更があればblockedを
返す」という従来の検査性質を保持している。ただし、追加されたF-B5 testは`head_difference`を
文字列で直接注入し、repository identity testも要求rootとGit top-levelの不一致だけを作るため、
元のW1・W2実入力を再現していない。

## 6. 事故痕跡、契約pin、Digest

### 6.1 Evidence §2.1の事故痕跡

【実測】現在の`tools/development/policy_test_runner.py`のSHA-256は
`0f7072ab8a7c4ab9093f394858c7629e2f60c1d2b774d5fd3b640622998e5b24`で、レビュー依頼値と一致した。
`134fed4..e07183d`の同path差分は空で、対象列ではGREEN `f8c01b5`だけが同pathを変更していた。
AST構文解析、対象Test、公式全Testも合格した。

【判断】RED作成中にreceipt JSONで上書きされた事故はcommitされておらず、現在成果物に
上書き痕跡を残していない。

### 6.2 契約pin

【実測】`e07183d`と`f8c01b5`の契約v2 JSONを構造比較すると、差は
`.fixed_sources[5].sha256`の
`901a4ea1…`から`b2e42d3f…`への1値だけだった。`goal`、`acceptance`、`work_items`は不変。
契約v1もbytes不変で、SHA-256は
`89c92ae260bfb1efd201d414e0235b66ebb270b457942c59ef5fccfc9cfa5387`だった。

【判断】Evidence §5の「v2の1箇所だけで、契約本文・受入条件・v1は不変」というClaimは一致する。

### 6.3 成果物Digest

【実測】レビュー依頼§4の7件は全件再計算一致した。

| file | 再計算SHA-256 |
| --- | --- |
| `tools/development/policy_test_runner.py` | `0f7072ab8a7c4ab9093f394858c7629e2f60c1d2b774d5fd3b640622998e5b24` |
| `tools/development/pytest_summary.py` | `febbdc68d64048c2351a343f83e121b2d06823515741d33ee1216203533d22b4` |
| `tools/development/declaration_red_map_check.py` | `151d2ef80a3ebb0dad6999dc1db63c0790541575ef0e7d7efd9da9ac7a507a61` |
| `tools/development/work_unit_transition.py` | `91726ff02cc7f86318c139913ec75d464521d2d7f389ed26cc227a45c88cb97e` |
| `conftest.py` | `1705384a41206185c38bda731706bf3ada2a024dec6f6ba3eb9f207e2350bc16` |
| Evidence | `fe3c8a82e153eb2f23b83c95073bee98b28a676ec3104a025e8c55bddf044121` |
| 固定公式receipt | `e3bf3347bdb094fde6831dff51eeda04dd64d4b2fe1e34a6db09c2e4a1c9cd3e` |

【実測】固定公式receipt自体はstatus `passed`、exit 0、`1465 passed,total=1465`である。
ただし、その`source_state_digest`記載値`432a3a8f…`は、`f8c01b5` treeからreceiptとsummaryを
除いて再計算した`ca50aa18…`とは一致しなかった。現在HEADに対する独立公式runは§4.2で合格済みである。

## 7. 変更範囲、禁止事項、Human境界

【実測】`271826a..c5d7db3`でconfig、schema、設計文書の変更は0件だった。対象4実装、許可test、
`conftest.py`、新規Evidence／receipt／handoff以外の変更は、既存の
`records/development/2026-08-07-work5b-implementation-task-contract-v2.json` 1件だった。

【記録】Evidence §5とレビュー依頼§1は、Humanが契約recordの照合値1箇所の更新を承認したと記録する。
一方、scope v1 §7は既存recordを変更禁止とし、scope v2は`conftest.py`と既存test 1件だけを
変更可能pathへ追加した。`role-neutral-pilot-review-collaboration.md` §4は、範囲変更が必要なら
次versionを新規commitするよう定める。契約recordを追加したscope v3は存在しない。

【判断】Humanによる内容変更の承認は記録されているため、§11類型2の承認欠落とはしない。
しかし、GREEN `f8c01b5`は固定済み変更file境界を守っておらず、§11類型4に該当する。

【実測】外部送信、push、tag、amend、rebase、reset、履歴書換え、TODO・checklist・Closer変更は
対象commit列にない。レビュー用一時fileと隔離cloneは消去済みで、判定record作成前の元repositoryはcleanだった。

## 8. Finding（§11）

### F-C1 blocking／completion／§11.1類型3

対象：`tools/development/work_unit_transition.py`、関連Test、レビュー依頼§3、Evidence §6.1。

【実測】W1・W2と追加反証`assume-unchanged`が、完了済みの未コミット変更またはdirtyな対象rootを
残したまま合格した。対象Test 48件はすべて合格した。

【判断】完了関門の「誤った合格」を機械実証した受入条件・検証の欠陥であり、類型3のblocking。
同じ周回でGit表示の非表示指定2種とclean decoy rootを確認した。

### F-C2 blocking／completion／§11.1類型4

対象：GREEN `f8c01b5`、scope v1 `c5cd440`、scope v2 `4fda1a6`。

【実測】GREENは、v1で禁止されv2でも追加されていない既存契約recordを変更した。

【判断】Humanによるpin値更新の承認とは別に、committed scopeの変更file境界を破っているため、
類型4のblocking。

### N-C1 non-blocking／completion／§11.1閉じた4類型の列挙外

【実測】固定公式receiptのfile SHA-256と件数は申告どおりだが、その`source_state_digest`は
GREEN commit treeから再生成一致しなかった。

【判断】現在HEADの公式全Testと独立収集件数を本レビューで再実行して一致を確認したため、
この完了レビューのTest合格を未検証にはしない。類型1〜4のblocking根拠には追加せずnon-blockingとする。

defer Findingは0件。実装方式の好みに基づく指摘は行っていない。

## 9. Human境界、未実施、次

Human境界：維持。完了レビューでblockingが出た後のcode・test修正は、包括承認record §2により
Human承認待ちである。

未実施：F-C1・F-C2の修正、既存recordの訂正、TODO・checklist反映、Closer作業、group C・D、
外部操作、push、履歴書換え。

次：Humanが本recordをPilotへ渡し、F-C1・F-C2を対象とする修正開始の可否を判断する。
