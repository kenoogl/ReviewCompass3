# group C 現在地正本修正 範囲レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー）
- risk：`high`（Human確定済み）
- 判定：**要修正（RED開始不可）**
- Finding：blocking 2件、non-blocking 1件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-current-position-fix-scope-v1.md`
- 対象SHA-256：`733c424727bc2262adcff7b91f2450ae5881b0150377f6ed3dbcc4763502595b`
- 対象commit：`183145038b94f166812948e61fc04b896e5fdbb1`
- 対象commitの親：`cbc8709a849f43b5398ed610aebe770b8adbcc40`
- branch：`main`
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、決定的な照合
- 禁止範囲：対象scope、code、test、既存record、config、schema、上流設計、TODO、
  checklistの変更、RED、GREEN、外部送信、push、履歴書換え

【実測】対象commitの親はscope記載のbase `cbc8709`と一致し、変更pathは対象scope 1件の
追加だけだった。レビュー開始時のworktreeとindexはcleanだった。対象commitの
`git diff --check`は終了コード0だった。

【実測】scope §3の固定入力5件と対象実装2件のSHA-256を内容から再計算し、7／7で記載値と
一致した。対象scope自身のSHA-256も上記のとおり再計算した。

【実測】本recordの予定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test ! -e`は終了コード0だった。

## 2. F-C1〜F-C5と修正境界

【記録】上流のgroup C判定recordは、F-C1・F-C2を`todo_handoff.py`、F-C3〜F-C5を
`todo_update_path.py`へ結び、H1〜H6・U1〜U4の機械反証をblocking根拠としている。

| Finding | scope §4の境界 | 照合結果 |
| --- | --- | --- |
| F-C1 | 短縮・大文字SHAと実branch不一致を正しいGit欄として合格させない | 方針には3変種が入るが、受入条件からH3が漏れる |
| F-C2 | 見出し・節・行構造の別表現でGit欄検査を逃げられない | 方針には末尾空白・別見出し・Unicode空白が入るが、受入条件からH6のUnicode空白変種が漏れる |
| F-C3 | 第2receiptの構造・結果・identity・実pathを検証し、第1receipt再利用を合格させない | 既存receipt契約への適合に収まる |
| F-C4 | 第2実行後の実TODOと候補bytesの同一性を確定前に再照合する | 既存の二段確認境界への適合に収まる |
| F-C5 | 非機械管理bytesを変えず、CRLF等を保持する | 既存の非機械管理部分保持契約への適合に収まる |

【判断】5 Findingの対象moduleと修正方向に取りこぼしや他groupへのはみ出しはない。新しいTODO書式、
receipt field、receipt kind、schema、検査項目を追加せず、既存契約への適合修正に閉じている。

【判断】ただし、scope §5.1が危険側として列挙する8件はH1・H2・H4・H5・U1〜U4であり、
F-C1のbranch差替えを実証したH3と、F-C2のUnicode空白による行構造逃れを実証したH6の該当変種が
無い。H6のBOM、CRLF読取り、必須3行の順序入替えは上流Findingではないため拒否対象に広げないが、
全角空白でworktree必須文を箇条書き外へ出す変種はF-C2の根拠そのものである。

## 3. 変更可能path、関連Test、既存指紋の機械照合

【実測】`rg`で対象2 moduleのimport、module起動文字列、公開関数の利用、file path、現行SHA-256、
変更候補5 testのpathと現行SHA-256を、`tests/`、`tools/`、`records/`、`docs/`、`config/`、
`.reviewcompass/`から横断検索した。

【実測】scope §7の5 testを単独実行した結果は`42 passed in 0.11s`、終了コード0だった。
このうちFindingの対象実装を直接検査するのは次の2 fileである。

- `tests/test_todo_handoff_git_state.py`
- `tests/test_todo_update_path.py`

【実測】残る次の3 fileは、対象2 moduleをimportせず、それぞれ別moduleのrenderer、repository
template、共通promptとAGENTS／CLAUDE入口を検査する。

- `tests/test_todo_handoff_projection.py`
- `tests/test_todo_handoff_projection_repository.py`
- `tests/test_todo_handoff_prompt_entrypoints.py`

【判断】上記3 fileを回帰確認として実行することは妥当だが、F-C1〜F-C5のために変更を許す根拠は
見つからない。scope §6のREDを「§7のtest fileのみ」、§7を変更可能pathとしているため、無関係な
renderer、template、prompt入口の契約までREDで変更できる。これは変更可能pathの過大である。

【実測】§7外で対象実装への実行時結線が見つかった回帰testは次の4 fileだった。単独実行は
`87 passed in 0.42s`、終了コード0だった。

- `tests/test_common_digests.py`：実TODOを`todo_handoff`のmodule入口で検査する
- `tests/test_issue_resolution_pilot_wi_005.py`：`load_known_active_issue_ids()`を利用する
- `tests/test_shared_function_sweep.py`：`todo_update_path`のmodule起動を検査する
- `tests/test_common_errors_paths_output.py`：`TodoUpdatePathError`とJSON出力を検査する

【実測】`tools/development/issue_resolution_post_write.py`は
`validate_commit_stable_git_section()`を直接importする。上記WI-005 testが実TODOによる事後検証を通す。

【判断】これら4 testと呼出元は変更対象ではなく回帰確認対象である。scope §5.3の公式全Test合格に
含まれるため、現時点で変更可能pathへ加える根拠はない。実装中に変更が必要と判明すればscope §8.2で
Humanへ停止する。関連回帰としての明示が無い点だけをnon-blockingの完了時確認事項とする。

【実測】現行test SHA-256は、`tests/test_todo_handoff_projection.py`がInitial Development Checklistと
WI-003 RED Evidence、`tests/test_todo_handoff_projection_repository.py`がWI-003 Completion Evidence、
`tests/test_todo_handoff_git_state.py`と`tests/test_todo_handoff_prompt_entrypoints.py`が
2026-08-08 TODO単一入口GREEN Evidence、`tests/test_todo_update_path.py`がgroup C判定recordに現れる。
対象2 moduleの現行SHA-256も2026-08-08 TODO単一入口GREEN Evidence等に現れる。

【実測】対象2 moduleまたは変更候補5 testの現行SHA-256を、現在のbytesとの一致条件として検査する
test、config、workflow台帳は検索で見つからなかった。上記recordは各作業時点の実装・Test identityを
記録しており、内容を現行bytesへ追随させる機械結線も見つからなかった。

【判断】既存recordの指紋は変更可能pathの不足を生じさせない。既存recordは変更禁止のまま保持し、
追随再計算や移行が実際に必要と判明した場合だけscope §8.2・§8.4でHumanへ停止する境界が妥当である。

## 4. Human境界と停止条件

【記録】包括承認record `271826a`は、group Cについてrisk `high`の確定、着手、RED開始、
GREEN着手、レビュー依頼を事前承認している。Human停止として、変更可能path外、上流設計・config・
schema変更、既存台帳・recordの再計算または移行、RED後のtest変更、完了レビューblocking後の修正、
その他の意味的裁定を残している。

【判断】scope §2は包括承認の対象identityと事前承認範囲を正しく固定している。§6はRED以後のtest変更を
Human承認へ戻す。§8は固定入力不一致、§7外path、実TODO正例の不成立、TODO書式・既存record移行、
上流設計・config・schema変更を停止条件にしている。完了レビュー後の修正はreview requestでPilotが
停止した後の段階であり、固定入力の包括承認record §2がHuman承認を要求する。Human境界に欠落はない。

【判断】範囲レビューで要修正となった場合のscope改訂と再レビューは包括承認record §3に含まれる。
今回のblocking修復自体は新たなHuman停止条件ではない。停止条件または修正承認へ触れた場合だけ
Humanへ戻る。

## 5. 受入条件、RED、commit境界、一時領域

【実測】正例として指定された次の単独commandは終了コード0、`status: passed`だった。

```text
env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md
```

【判断】scope §5は、列挙済み8反証の拒否、実TODOの単一入口合格、対象test、公式全Test、
schema・既存record非変更を機械照合できる方向にしている。しかしH3とH6のUnicode空白変種が無いため、
危険側全体と正例側の双方向受入としては未完了である。

【判断】SCOPE、testだけのRED、実装・新規Evidence・新規receiptのGREEN、review requestを
別commitにする境界は妥当である。REDは新規反証と欠陥側の旧契約を写した既存testの契約更新だけを許し、
削除・緩和を禁止する。実装前は変更testだけが反証どおり失敗し、他は合格、単独commandの終了コード1を
要求しており、REDの方向も妥当である。ただし、変更可能testの過大はSR-C-SCOPE-002の修復が必要である。

【判断】反証を使い捨ての一時領域だけで行い、実`TODO_NEXT_SESSION.md`と実Git索引を変更しない規定は、
group Bで生じた実repositoryへの反証書込みを防ぐ境界として妥当である。

## 6. Finding（`work-review-protocol.md` §11）

### SR-C-SCOPE-001 blocking／scope／§11.1類型1・3

【実測】scope §5.1の危険側8件はH1・H2・H4・H5・U1〜U4であり、H3とH6を列挙しない。

【記録】上流group C判定のF-C1はH3による実branch差替え、F-C2はH6によるUnicode空白の行構造逃れを
blocking根拠に含める。両反証は一時Git repositoryまたは一時TODOで機械実行済みで、欠陥側が合格した。

【判断】8件だけを拒否してH3とH6の該当変種を合格させる実装でも、scope §5の受入条件を満たせる。
上流Findingとの不一致である類型1と、現在地偽装を誤って合格させる受入条件欠陥である類型3の
blockingとする。

### SR-C-SCOPE-002 blocking／scope／§11.1類型4

【実測】§7の変更可能test 5件のうち3件は対象実装をimportせず、renderer、repository template、
prompt入口の別契約を検査する。F-C1〜F-C5および§4の修正方針は、この3契約の変更を要求していない。

【判断】回帰確認対象3 fileを変更可能pathとRED commitへ含めると、今回のFinding修正を越えて別契約を
変更できる。禁止事項またはscope境界の破りに当たる類型4のblockingとする。

### SR-C-SCOPE-NB-001 non-blocking／implementation・completion

【実測】§7外の関連回帰test 4件と直接呼出元1 moduleが見つかった。現状は87件すべて合格し、
公式全Testの受入条件にも含まれる。

【判断】変更可能pathの追加は不要である。修正後も関連回帰として独立確認し、失敗して§7外変更が
必要ならscope §8.2へ停止したことを完了レビューで確認する。

### defer

【判断】0件。command option、Git取得手段、正規化関数、receipt validatorの呼出し方、fixture構成などの
実装細部には立ち入っていない。

## 7. 判定と次

判定：**要修正（RED開始不可）**。

【判断】対象scope commitは申告base、固定入力Digest、risk、Human境界、既存契約への修正方向、
commit境界、一時領域規定を正しく固定している。しかしSR-C-SCOPE-001によりF-C1・F-C2を残したまま
受入可能であり、SR-C-SCOPE-002により変更可能test pathがFinding境界を越える。現scopeをRED開始の
根拠にはできない。

Human境界：維持。包括承認により、PilotはHumanへ追加確認せずscope改訂版を新規commitし、再レビューを
依頼できる。scope §8または包括承認record §2の修正承認へ触れた場合だけHumanへ戻る。

未実施：対象scope、code、test、既存record、config、schema、上流設計、TODO、checklistの変更、RED、
GREEN、完了レビュー、Closer作業、外部操作、push、履歴書換え。

次：PilotはSR-C-SCOPE-001・002だけを解消したscope改訂版を固定し、Codexへ範囲再レビューを依頼する。
