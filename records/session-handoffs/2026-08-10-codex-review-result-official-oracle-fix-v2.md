# 完了レビュー v2：group B — F-C1・F-C2修正後

- 作成日：2026-08-10
- collaboration mode：`role_neutral_pilot_review`
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- risk：`high`
- 判定：`verified`
- model来歴：`model = gpt-5.6-sol`、`reasoning effort = high`
  （`~/.codex/config.toml`の実効値）

## 1. 対象と固定境界

- 作業指示：
  `records/session-handoffs/2026-08-10-claude-pilot-official-oracle-fix-review-request-v2.md`
  （commit `b8563fd`、SHA-256
  `d9ebd0ad344f0d3ec1a49421aa5710adb17404630dc8e0a5c402790ddc7dd28f`）
- 先行判定：
  `records/session-handoffs/2026-08-10-codex-review-result-official-oracle-fix-v1.md`
  （commit `9c9d9a7`、SHA-256
  `fd9023716741502332e945d25df585bf97dd009a758b8c22ceff3431bde80195`）
- Human裁定：2026-08-10「F-C1とF-C2の修正を承認する」
- 範囲：scope v1 `c5cd440`、v2 `4fda1a6`、v3 `6ce4d03`。
  v3のSHA-256は
  `a069a6b842d094d39371b3607a434ced6e60976f84bae59c8abaff52dba61418`。
- 再レビュー開始：branch `main`、HEAD `b8563fd34b467007bfa98fe9555910aae6e38578`、
  作業treeと索引はclean。
- 許可範囲：読取り、一時領域での反証と隔離実行、本record 1件の新規作成と単独commit。
- 禁止範囲：code、test、既存record、config、schema、上流設計、TODO、checklistの
  恒久変更、外部送信、push、tag、履歴書換え、Closer作業。

## 2. Claimの分解と総合判定

- 実施Claim：F-C1の検出追加、F-C2のscope是正、修正RED 2件、修正GREEN、Evidence追記、
  receipt v2作成。
- 結果Claim：対象Test 13件と公式全Test 1469件の合格、公式status `passed`。
- 判断Claim：W2型の限界を明記し、指定rootとGit rootの食い違いは拒否する。
- 未実施Claim：group C・D、TODO・checklist反映、Closer作業、push、履歴書換え。

【判断】必須Evidenceを独立再実行でき、報告と事後状態は一致した。F-C1とF-C2は解消し、
受入条件を満たすため、`work-review-protocol.md` §4.7の判定は`verified`である。

## 3. commit列、変更path、履歴

【実測】`9c9d9a7..b8563fd`は次の直線で、各commitの親SHAは連続していた。

| commit | 役割 | 変更path |
| --- | --- | --- |
| `6ce4d03` | SCOPE v3 | scope v3 record 1件の追加だけ |
| `b44e1a6` | 修正RED | `tests/test_work_unit_transition.py`だけ |
| `dddaf9b` | 修正RED・契約更新 | 同test 1件だけ |
| `33dfa38` | 修正GREEN | `tools/development/work_unit_transition.py`、Evidence追記、receipt v2新規の3件 |
| `b8563fd` | review request v2 | 依頼書1件の追加だけ |

【実測】各commitの単独`git diff --check <parent> <commit>`は5件すべて終了コード0だった。
`git fsck --no-dangling --no-reflogs`も終了コード0だった。scope v1、v2、v3、先行判定、
修正RED 2件、修正GREENはすべて元のSHAのまま祖先列に存在する。

【判断】修正RED 2件はGREEN前にあり、scope v3が許可した同一test pathだけを変更した。
GREENの3 pathもscope v3 §4の変更可能path内である。F-C2の対象だった契約v2は、scope v3 §2で
変更可能pathへ追加され、変更を固定sourceのSHA-256値1箇所に限定している。過去commitの
amend、rebase、reset等による書き換えは観測されず、F-C2は解消した。

## 4. F-C1の独立反証

反証用scriptは`/private/tmp`だけへ作成し、各Git操作は
`TemporaryDirectory(dir="/private/tmp")`配下の使い捨てrepositoryで行った。終了時に一時repositoryと
scriptを削除した。最終scriptのSHA-256は
`73ec25eca03c2691a2ebff1cad223dce1788ff25697efebd80b2a5664853c452`。

【実測】`skip-worktree`と`assume-unchanged`の各場合で、追跡fileのbytes変更後も
`git status --porcelain=v1 --untracked-files=all`と`git diff --name-only HEAD --`は共に空だった。
修正後の`preflight_next_work`は両方を`blocked`、`next_work_allowed=false`とした。

【実測】Pilotのfixtureにないhigh risk用の追加反証として、`skip-worktree`指定後に追跡fileを
削除した。通常の状態表示とHEAD差分表示は共に空だったが、blob取得不能を差ありとして扱い、
完了関門は`blocked`を返した。

【実測】clean repositoryは`passed`、要求rootがrepository内の入れ子directoryの場合は
`WorkUnitTransitionError`で拒否した。一方、別の正当なclean repository自体を要求rootとして
明示指定した場合は`passed`だった。

【判断】索引の隠蔽指定2種によるW1型の迂回は不成立となり、fail-closed（取得不能時に安全側へ
停止する方式）も維持されている。W2型は、呼出し側が選んだ別の正当なrepositoryと、本来意図した
repositoryをtool単体で区別できない。指定rootとGitが答えるrootの不一致は拒否できているため、
依頼書§3、scope v3 §3.1、Evidence §8.2の限界表明は妥当であり、F-C1は解消した。

## 5. 修正REDと検査性質

独立再現は`/private/tmp`へのlocal cloneだけで行った。cloneを`dddaf9b`へcheckoutし、同commitの
testへ修正前実装と修正後実装を順に当てた後、`dddaf9b`の実装へ復元した。復元後の
`git status --short`は空で、HEADも`dddaf9b`だった。cloneとscriptは終了時に削除した。
最終scriptのSHA-256は
`266fc73758283665336de816290fffc42ecd64bb5729f3d6506e8244dfadde25`。

| 実行 | 結果 | exit code |
| --- | --- | ---: |
| `pytest -q tests/test_work_unit_transition.py::test_preflight_reads_git_state_mechanically`を修正前実装へ適用 | `1 failed` | `1` |
| 同一testを`33dfa38`の修正後実装へ適用 | `1 passed` | `0` |
| `pytest -q tests/test_work_unit_transition.py`を修正後実装へ適用 | `13 passed` | `0` |

【実測】両側で使ったtest SHA-256は
`f811eb9caa276f7b88e3ae237cec5c745cf2a85b93bf27eed12aacb33c01b40d`で同一だった。
`dddaf9b`の差分は、期待するGit呼出し列へ`git ls-files -v`を1行追加しただけである。

【判断】修正REDは修正前後を区別し、Git状態を機械取得してdirty状態を停止する従来の検査性質を
弱めていない。むしろ隠蔽指定の機械検査を期待呼出しへ追加している。

## 6. 正例、公式全Test、v1確認事項

公式runはHEAD `b8563fd`を`/private/tmp`へlocal cloneし、`.venv`だけをcloneのGit内部除外へ
登録して実行した。receiptはclone外の一時領域へ出力した。検証用checkoutは`b8563fd`へ復元し、
実行後と復元後の`git status --short`が共に空であることを確認してからcloneを削除した。
最終scriptのSHA-256は
`7f38f4f87b91172da99918188d195443dab67a5a534b4ea25ddb259d66c878dd`。

```text
.venv/bin/python3 -m tools.development.policy_test_runner \
  --project-root . --suite full --receipt <一時領域>/independent-official-receipt.json
```

【実測】上記は終了コード0、status `passed`、failed 0、errors 0、skipped 0、
`1469 passed,total=1469`だった。別の`pytest --collect-only -q`は終了コード0、
`1469 tests collected`で、公式receiptの件数と一致した。

【実測】v1でP1〜D3を検査した実装3 file、`conftest.py`、関連test 5 file、契約v1・v2は、
`9c9d9a7..b8563fd`で差分がなかった。`policy_test_runner.py`のSHA-256はv1と同じ
`0f7072ab8a7c4ab9093f394858c7629e2f60c1d2b774d5fd3b640622998e5b24`で、
RED作成中の上書き事故の痕跡は現在成果物にも対象commit列にもない。

【実測】契約v1のSHA-256は
`89c92ae260bfb1efd201d414e0235b66ebb270b457942c59ef5fccfc9cfa5387`、契約v2は
`5123b778cb12b8cf23f353d9725c0598f9214fdcf66d625f9385ef2ebd8a20f0`で、v1判定時から不変。
`e07183d..f8c01b5`の構造差分は、契約v2の
`fixed_sources[5].sha256` 1値だけである。

【判断】公式正例と件数一致、P1〜D3の反証不成立、事故痕跡なし、契約pinがv2の1箇所のみという
v1の確認事項は維持されている。

## 7. 成果物DigestとN-C1

【実測】レビュー依頼§4の4件は全件再計算一致した。

| file | SHA-256 |
| --- | --- |
| `tools/development/work_unit_transition.py` | `93e005fe299bd0e33d0ada6b92ad1732d05194ebe4d92e100e5111bd659b33b6` |
| `tests/test_work_unit_transition.py` | `f811eb9caa276f7b88e3ae237cec5c745cf2a85b93bf27eed12aacb33c01b40d` |
| Evidence | `f38e9e59396954e75b73768e7328e355aa2ad93c38fcb841f36998fd200e1444` |
| 公式receipt v2 | `49785d1bf32b458f9f673f91dee0c03344e0e95c26871f06e88847542e94f870` |

【実測】公式receipt v2の`source_state_digest`は`fd90d6a1…`だが、GREEN `33dfa38`のtreeから
receiptとsummaryを除いて再生成した値は`26bc1ae7…`で一致しなかった。

【判断】これはv1のN-C1と同じ既知の再生成不一致であり、本修正の対象外である。現在の公式全Testと
独立収集件数を再実行して一致を確認できたため、完了判定を止めない。

## 8. Finding（§11）

### F-C1 解消／旧blocking／completion／§11.1類型3

【実測】索引の隠蔽指定2種とReviewer独自の隠蔽file削除はすべて`blocked`になり、正常系は
`passed`だった。W2型の限界は実挙動と説明が一致した。

【判断】「誤った合格」を実証した旧欠陥は再現しない。解消済み。

### F-C2 解消／旧blocking／completion／§11.1類型4

【実測】scope v3は契約v2の限定変更を変更可能pathへ追加し、その後の修正RED 2件とGREENは
許可path内だった。履歴は元のcommit列を保持した。

【判断】変更file境界の破りは是正済み。

### N-C1 non-blocking／completion／§11.1閉じた4類型の列挙外

【実測】receipt v2の`source_state_digest`はGREEN treeから再生成一致しなかった。

【判断】本修正の対象外で、公式runを独立再実行して合格と件数を確認済みである。類型1〜4の
blocking根拠には追加せず、non-blockingのまま保持する。

blocking Findingは0件。v1で挙げなかった新規Findingは0件。defer Findingも0件。

## 9. Human境界、禁止事項、未実施、次

【実測】外部送信、push、tag、amend、rebase、reset、TODO・checklist・Closer変更は対象commit列に
ない。一時repositoryはすべて破棄し、本record作成前の実repositoryはcleanだった。

【判断】Human境界と禁止事項は維持された。本review resultは完了projectionではない。

未実施：group C・D、N-C1の修正、TODO・checklist反映、Closer作業、外部操作、push、履歴書換え。

次：Humanが本`verified`判定を確認し、必要な段完了承認後にCloserが別作業単位で完了projectionを行う。
