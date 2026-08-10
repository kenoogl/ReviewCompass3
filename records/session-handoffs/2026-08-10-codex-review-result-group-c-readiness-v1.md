# group C 実装着手可否 独立点検結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope／RED着手前提の再点検
- risk：`high`（Human指定）
- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-group-c-readiness-selfcheck-v1.md`
- 対象commit：`6e90fc470429140bd20402c53da991932b48e02d`
- 対象SHA-256：`0d23e31b36bba98f50651c8744019d9b8f7846a43d2653e13c402625439b9ef4`
- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`
- 材料モード：発見力
- 起動記録からのpath抽出：可99件・不能14件・固有63件
  （session `019febef-3882-7103-a08b-6dd2e1a731ef`、
  cutoff `2026-08-10T13:59:39.222Z`。`cmd`の静的文字列からrepository相対pathと既知rootを
  機械抽出し、動的template 1件、`cmd`文字列なし1件、明示pathなし12件を不能とした）

## 1. 判定

**実装着手不可。** レビュー状態は`report_execution_mismatch`とする。

【実測】Pilotが「U2・U4以外は対応あり」とした対応表に対し、現行REDには次の競合がある。

- H1〜H6の6 testは、反証判定へ到達する前に、旧実装に無い`current_branch`引数の
  `TypeError`で失敗した。
- H1・H2の入力は現在HEADへ解決せず、H6は上流反証と異なる行を変え、既存実装が既に拒否する
  7文字SHAを同居させている。
- U1は偽runnerを試さず、基準receiptも公式receipt検証器が不足9 fieldで拒否する。
- U2・U4はtestが無い。
- 反証ではない正例2件まで同じ`TypeError`で失敗する。

【判断】「U2・U4だけが不足」「修正前実装しかないため12件すべてが期待どおりRED」という自己申告は、
test本文と実行結果に一致しない。上流10反証を正しく固定したREDがなく、範囲固定v3も後続のHuman指示と
現状態を覆わないため、GREEN実装を開始できない。

## 2. 観点1：上流§4の反証と現行REDの独立対応

上流はH1〜H6・U1〜U4の10反証を固定する。Pilotの表を使わず、上流§4.2と現行test本文から
次の対応を導出した。

| ID | 上流反証 | 現行test | 独立判定 |
| --- | --- | --- | --- |
| H1 | 現HEADへ解決する4文字小文字SHA | `test_short_lowercase_sha_snapshot_is_rejected` | **誤対応**。入力`a1b2`は`git rev-parse --verify`でexit 128、現在HEAD短縮形は`6e90` |
| H2 | 同じHEADへ解決する40文字大文字SHA | `test_uppercase_forty_character_sha_snapshot_is_rejected` | **誤対応**。固定値`A1B2…`はexit 128でHEADではない |
| H3 | 一時Git repositoryの実branchと記載branchの不一致 | `test_branch_mismatch_is_rejected` | **部分対応**。文字列`current_branch="main"`を直接渡すだけで、実Git取得とCLI／呼出元への結線を検査しない |
| H4 | 末尾空白付きGit見出しへHEAD・push済み・ahead／behind 0を置く | `test_trailing_space_heading_variant_is_counted` | **部分対応**。別節には7文字SHA 1行だけを置き、上流の可変状態一式を再現しない |
| H5 | 別のGit状態節へ同じ可変状態を逃がす | `test_alternative_git_section_heading_is_counted` | **部分対応**。別節には7文字SHA 1行だけで、push・ahead／behindを試さない |
| H6 | worktree必須文の前へ全角空白を置き、箇条書き外へ逃がす | `test_unicode_space_line_is_normalised` | **誤対応**。変更対象はcommit境界行のハイフン後で、worktree行は正規のまま。さらに既存拒否対象の7文字SHAを同居させる |
| U1 | 第2receiptの未知kind・偽runner・exit 9・浮動小数件数・fallback整数0 | 3 test | **部分対応**。未知kind、exit 9、fallback 0、浮動小数は記述するが偽runnerが無い。浮動小数は同じtestの後段で現RED時に未到達 |
| U2 | executorが第1receiptの実pathを第2段でも返す | なし | **不足** |
| U3 | 第2公式Test callback内で検証済みTODOを差し替える | `test_todo_swapped_after_verification_is_detected` | **対応** |
| U4 | CRLF 22個のTODOを正常更新するとLFへ変わる | なし | **不足** |

【実測】H6のtest入力を`current_branch`引数なしで旧実装へ直接渡すと、Unicode行構造ではなく
`self_commit_sha_snapshot`により`failed`となった。したがって、引数エラーだけを直すとH6 testは
F-C2を修正しなくてもGREENになり得る。

【実測】U1 classの基準receiptを
`todo_record_generation.validate_official_receipt()`へ渡す単独commandはexit 1となり、
`command`、`config_digest`、`configured_python`、`recorded_at`、`resolved_python`、
`runner_version`、`source_state_digest`、`stderr`、`stdout`の9 field不足で拒否された。

【判断】不足はU2・U4だけではない。H1・H2・H6は反証入力自体が違い、H3は実Gitへの結線がなく、
H4・H5は上流入力を縮小し、U1は偽runnerと有効な基準receiptを欠く。

## 3. 観点2：各RED testの失敗理由

対象2 fileの単独実行はexit 1、`12 failed, 34 passed`だった。各反証testも単独commandで実行した。

| test群 | 単独実行の失敗理由 | 反証そのものによるREDか |
| --- | --- | --- |
| H1〜H6の6件 | 全件`TypeError: ... unexpected keyword argument 'current_branch'` | **否**。反証判定へ未到達 |
| U1 未知kind | `DID NOT RAISE TodoUpdatePathError` | **可**。未知kindを拒否しない欠陥で失敗 |
| U1 exit 9 | `DID NOT RAISE TodoUpdatePathError` | **可**。非0終了を拒否しない欠陥で失敗 |
| U1 fallback 0／浮動小数 | 最初のfallback 0で`DID NOT RAISE` | **一部のみ可**。浮動小数の後段は実行されない |
| U3 差替え | `DID NOT RAISE TodoUpdatePathError` | **可**。差替え後も成功する欠陥で失敗 |

【実測】新規の正例`test_baseline_document_passes`と`test_matching_branch_passes`も同じ
`TypeError`で失敗し、`test_matching_receipts_still_compare_equal`だけが合格した。

【記録】範囲固定v3 §4は、実装前には新規・更新した**反証testだけ**が反証どおり失敗し、
それ以外は合格すると定義する。

【判断】正例2件が失敗し、H1〜H6が別理由で失敗する現RED commit `431dd7b`は、v3のRED定義を
満たさない。RED Evidenceとして使えず、修正前実装に対する対応確認をやり直す必要がある。

【実測】公式全Testを通常環境で再実行したreceipt
`/private/tmp/2026-08-10-codex-group-c-readiness-full-receipt-v2.json`
（SHA-256 `92105959a95dc1d659734c14e02960d5051691efa1d914c8b7d2e57d042bf03a`）は、
exit 1、status `failed`、`1470 passed / 12 failed / total 1482`、Python 3.9.6、pytest 8.4.2、
fallback falseだった。12件は上表の10反証test、H系正例2件である。

### 手戻りの記録

【実測】最初の公式全TestではReviewerがtargeted test用の
`PYTHONDONTWRITEBYTECODE=1`を誤って全Testへ付けた。期待executorは通常環境の公式runner、
実executorは同runnerだが不要な環境変数付きで、task cache test 1件が別理由で失敗し、
`1469 passed / 13 failed`となった。receipt v1のSHA-256は
`de22eb673c95a1e768ebb01abe145f724af73927545d1b5073c787ec45c1791a`である。

【判断】この結果はgroup CのEvidenceから除外した。手作業理由はReviewerの環境指定誤りであり、
同じ公式runnerを通常環境で再実行したv2を採用した。機械処理候補は、公式runnerの全Test commandへ
bytecode抑止変数を追加しない固定呼出しを使うことであり、本作業の製品Findingにはrouteしない。

## 4. 観点3：巻き添え経路

【実測】変更候補3 moduleを起点に、module名、公開関数、module起動文字列、直接呼出元、現行SHA-256を
`tests/`、`tools/`、`records/`、`docs/`、`config/`、`.reviewcompass/`へ横断検索した。

v3が固定済みの変更test 2件と回帰test 7件に、追加moduleの直接testを加えると、回帰対象は
少なくとも次の**10 file**である。

1. `tests/test_todo_handoff_git_state.py`
2. `tests/test_todo_update_path.py`
3. `tests/test_todo_handoff_projection.py`
4. `tests/test_todo_handoff_projection_repository.py`
5. `tests/test_todo_handoff_prompt_entrypoints.py`
6. `tests/test_common_digests.py`
7. `tests/test_issue_resolution_pilot_wi_005.py`
8. `tests/test_shared_function_sweep.py`
9. `tests/test_common_errors_paths_output.py`
10. `tests/test_todo_record_generation.py`

【判断】Pilotの9 fileには、v3 §3が既に回帰確認対象とした
`tests/test_todo_handoff_projection_repository.py`が無い。追加moduleのtestを足しながら既存回帰1件を
落として件数9を維持しており、巻き添え集合として誤りである。

【実測】追加の実行経路は次のとおり。

- `tools/development/todo_handoff.py::main` →
  `todo_update_path.default_verify()` → `validate_commit_stable_git_section()`。
- `tools/development/issue_resolution_post_write.py::verify_post_write()`は
  `validate_commit_stable_git_section()`を直接呼ぶ。WI-005 testが実TODOでこの経路を通す。
- 共通prompt、TODO template、開発方針、checklistは
  `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`を実運用入口にする。
- `tests/test_issue_resolution_pilot_verdict_closure.py`は直接呼出元moduleをimportするが、
  変更対象validatorの振る舞いは実行しないため、import回帰として全Testにのみ数える。

【判断】H3の現REDは引数へ文字列を注入するだけで、上記2実行経路が実Git branchを取得して検査へ
渡すことを証明しない。関数単体がGREENでも実運用入口が旧挙動のまま残る経路がある。

【実測】3 moduleの現行SHA-256を含む履歴recordは重複除去後5件だった。exact digestを現在bytesへ
実行時照合するtest、config、workflow台帳は見つからなかった。

【判断】「Digestの実行時照合は無い」というPilot申告は、この限定した意味では正しい。履歴recordは
時点固定Evidenceなので追随変更しない。ただし5件の検索結果はv4の事前走査結果として固定する必要がある。

## 5. 観点4：範囲固定v3、Human指示、commit境界

【記録】範囲固定v3 §3は実装変更を`todo_handoff.py`と`todo_update_path.py`の2 fileに限定し、
それ以外のtool変更を禁止する。継承するv1 §8-2は許可path外変更が必要ならHumanへ停止する。

【記録】Humanは本レビューの固定前提として、`todo_record_generation.py`を変更可能pathへ加え、
範囲固定v4を作って再レビューへ回すよう指示した。

【判断】v3の許可pathとHuman指示は両立せず、v1 §8-2の停止条件へ到達済みである。Human指示は
v4作成と再レビューを許可するが、v3をそのままGREENの根拠へ戻さない。

【実測】v3が継承するv1のbaseは`cbc8709`、test DigestはRED前である。現在はscope v3
`c1edf4f`、範囲レビュー`1871c93`、RED `431dd7b`の後にあり、test 2件のSHA-256は
`66fa2dd016e8316c00d6fd4efd508da6536c469eda37f8372b3b940390fd520b`と
`322f1629bfd2b308193ea6465e48e4534d273fb3388b6a8938d4243688f2a79a`へ変わっている。

【判断】v4は、現在base、開始worktree、修正前3 module、現RED 2 test、上流とHuman指示を
再固定しなければならない。v3のcommit表は「SCOPE→RED→GREEN」だが、v4は既存REDの後に来るため、
`431dd7b`を不合格REDとして保持し、v4の範囲レビュー後に**訂正RED**を別commitにする順序を
一意に書く必要がある。

【記録】Human裁定
`records/development/2026-08-10-policy-document-retirement-decision-v1.md`は、同日の規約A/B/C文書を
今後の判断根拠から外し、巻き添え防止の規約Aだけを生かす。したがって、廃棄候補となった規約B・Cを
新たな必須条件にはしない。一方、規約Aの5手順と
`records/development/2026-08-10-review-material-mode-decision-v1.md`の材料出自記録義務は残る。

【判断】v4には少なくとも、欠陥所在、test、Digest pin、実運用接続点、受入条件と変更pathの同一一覧、
および「固定入力の出自：機械導出／判断選定」の1行が必要である。現v3には後発のこれらが無い。

## 6. 観点5：Pilotが列挙していない着手前提

実装前に次をすべて満たす必要がある。

1. Pilotがv4を新規作成・単独commitし、3 module、10反証、10回帰test、実運用接続点、
   現在base／Digest、訂正RED境界、規約Aの事前走査、固定入力の出自を一体で固定する。
2. H1・H2は一時Git repositoryの実HEADから生成し、H3は実Git branchを使う。H4・H5は
   上流のHEAD・push・ahead／behind一式を再現し、H6はworktree行だけを全角空白で行構造外へ出す。
3. U1は公式検証器が受理する基準receiptを使い、未知kind、偽runner、exit 9、浮動小数件数、
   fallback整数0を各々到達確認する。U2とU4を追加し、U3を維持する。
4. 反証10件だけが狙った理由でREDとなり、基準文書、branch一致、同一receipt等の正例は合格することを、
   修正前3 moduleに対する単独commandとexit codeで記録する。
5. H3を単体引数注入だけで閉じず、TODO単一CLIと`issue_resolution_post_write`の実呼出経路が
   実Git照合を迂回しないことをREDまたは訂正scopeの完了条件へ接続する。
6. RED commit `431dd7b`後のtest変更になるため、testの訂正・追加についてHumanの明示承認を得る。
   現在の「module追加・v4・再レビュー」指示だけから、RED後test変更やGREEN再開の承認を拡張しない。
7. v4の`high`範囲レビューが`verified`となり、その固定identityに対するHumanの明示的な再開承認を得る。

【実測】`TODO_NEXT_SESSION.md`は現在も「技術上のblockerなし」「着手可能」と表示する。

【判断】TODOはauthorityではないが、v4未作成、停止条件到達、RED不成立と競合するため、この表示は
staleであり、実装開始根拠に使えない。既存recordとTODOは本レビューでは変更しない。

## 7. Finding（`work-review-protocol.md` §11）

### GC-READY-001 blocking／implementation／§11.1類型1・3

【実測】H1〜H6は別理由で失敗し、H1・H2・H6の入力は上流反証と異なる。U1は偽runnerと有効な
基準receiptを欠き、U2・U4は無い。正例2件も失敗する。

【判断】上流10反証を直さなくてもGREENになり得るtestと、正常入力までREDにするtestが混在する。
上流authorityとの矛盾、および誤った合格・不合格を許す検証欠陥としてblockingとする。

### GC-READY-002 blocking／scope／§11.1類型1・4

【実測】v3は実装2 fileだけを許可するが、Humanは第3 module追加とv4再レビューを指示した。
v3のbase・test Digest・commit境界も現状態を表さない。

【判断】Human指示と変更可能pathの矛盾、およびscope境界の破りである。v4が`verified`になるまで
v3を実装着手根拠にできない。

### GC-READY-003 blocking／scope／§11.1類型4

【実測】v3固定の回帰7件、変更test 2件、追加moduleの直接test 1件の和は10 fileであり、
Pilotの9 fileは`test_todo_handoff_projection_repository.py`を落とす。H3の実運用接続2経路も
現REDに接続されていない。

【判断】既知の回帰pathと実運用接続点をscopeから落とす境界欠陥としてblockingとする。

### GC-READY-004 blocking／scope／§11.1類型2

【記録】包括承認とv3は、RED後のtest変更をHuman承認へ戻す。Humanの後続指示は第3 module追加、
v4作成、再レビューまでを述べる。

【判断】訂正REDには既存test修正とU2・U4等の追加が必要だが、その修正承認とGREEN再開承認は
まだ固定されていない。必要なHuman境界の欠落としてblockingとする。

### non-blocking／defer

【判断】non-blocking 0件、defer 0件。実装方式の選定や上流10反証を越える新機能提案は行わない。

## 8. 影響、未実施、次

【判断】staleになるClaimは、Pilot自己点検の「U2・U4だけが不足」「12件は期待どおりRED」
「巻き添えtestは9 file」、範囲レビューv3の「このscopeでREDからGREENへ進める」、および
TODOの「blockerなし／着手可能」である。過去recordは履歴として保持し、書き換えない。

未実施：code、test、既存record、TODO、checklist、config、schemaの変更、v4作成、RED訂正、GREEN、
外部操作、push、tag、amend、rebase、reset、履歴書換え。

次：Pilotはcode・testへ触れず、§6の前提を含む範囲固定v4を新規commitして独立範囲レビューへ回す。
test訂正と実装は、v4の`verified`およびHumanの明示的な再開承認まで停止する。
