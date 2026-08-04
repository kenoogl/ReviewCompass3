# Work 4A Start Boundary Evidence v1

- Evidence ID：`RC3-WORK4A-START-BOUNDARY-2026-08-04-V1`
- status：`defined / implementation_not_started`
- scope：Work 4AのSource Symbol Index開始境界。Index生成器、Index、Ledger、製品Runtimeは含まない。

## Authority

- Current Plan：`docs/current/reviewcompass3-plan-current.md`、SHA-256
  `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- Work 4A先行Decision：`records/development/2026-08-04-work-4a-sequence-approval-decision-v1.json`、SHA-256
  `4a10d09c12f227e67399aad1dc9c1ca8a6c664edcc6bc7f99385edafa7f48f0f`
- Source identity timing memo：`docs/design/2026-08-03-source-change-verification-identity-timing-memo.md`、SHA-256
  `08f973be1f4b0134f4a6a48af98fcbad4948bae890178fd8de6ce98d68e8235a`
- Layout approval：`records/development/2026-08-04-layout-baseline-v2-approval-decision.json`、SHA-256
  `856345948af57bcfa373eb2766768d9c38078d7ba5fe65b0d76d68e452ceaa7e`

## 観測した開始状態

観測時のGit HEADは`0880b547616c3308ed72ccb4795f2786a005183c`、worktreeはcleanである。
機械集計では、一次Index対象の`tools/**/*.py`は100 files、631 function／method、Test参照対象の
`tests/**/*.py`は121 files、682 function／methodだった。

この観測は開始前状態の説明であり、再利用可能なSource Snapshotではない。このEvidenceを含むcommitが
作られるため、次の作業ではそのcontaining commitのclean stateから新しいSource Snapshotを機械採取する。

## Source universeと除外規則

- 一次Index対象：Git追跡済みの`tools/**/*.py`。これは現時点のproject内bootstrap／development toolingであり、
  Layoutの外部`CODE_ROOT`そのものとは混同しない。
- Test参照対象：Git追跡済みの`tests/**/*.py`。v1ではTest functionを一次Index entryにせず、後続の
  `test_references`抽出の入力とする。
- 除外：`.git/`、`.venv/`、`.pytest_cache/`、`__pycache__/`、`*.egg-info/`、generated file、vendor、
  non-Python file、Git未追跡file。
- 将来追加するIndex generator自身は`tools/**/*.py`へ置き、追加後のSnapshotでは必ず一次Index対象に含める。

## 最小Source Snapshot規則

Snapshotは機械処理だけで作る。capture時に`git status --porcelain`が空でなければ
`source_snapshot_dirty`として停止する。Git追跡済み対象pathをPOSIX相対path順に並べ、各file bytesの
SHA-256、captureしたHEAD、source universe規則のDigestを正規化manifestへ格納する。Snapshot IDはその
canonical JSON bytesのSHA-256とする。LLMまたはHumanがpathやDigestを手入力してSnapshotを作らない。

## 最小symbol identity規則

- 対象node：`ast.FunctionDef`と`ast.AsyncFunctionDef`。class内はmethod、その他はfunctionとして区別する。
- `qualified_name`：repo相対pathから導くmodule nameに、classと入れ子functionをsource順に連結する。
- `symbol_id`：`py:<relative_posix_path>:<qualified_name>:<kind>`。path、qualified nameまたはkindが変われば
  新identityとし、旧identityは後続のretired／successor判断へ渡す。
- `signature`：Python ASTから機械正規化した引数表記、`signature_sha256`：そのUTF-8 bytesのSHA-256。
- `content_sha256`：Snapshot内のsymbol source segment bytesのSHA-256。file全体のDigestはSnapshot manifest側で保持する。
- 最低必須field：`symbol_id`、`qualified_name`、`kind`、`source_path`、`signature`、`signature_sha256`、
  `content_sha256`、`snapshot_id`。visibility、参照関係、Test参照は次のIndex schema／generator作業で追加する。

## 次のRED Acceptance入口

次作業ではIndex generatorを実装せず、まず`tests/test_source_symbol_index.py`を作る。少なくとも次を期待して
未実装によるREDを確認する。

1. clean tracked sourceから同一Snapshot IDとordered manifestを再生成できる。
2. dirty state、untracked対象、対象外path、欠落file Digestを拒否する。
3. `tools/**/*.py`の全`FunctionDef`／`AsyncFunctionDef`を一意なsymbol IDで収録する。
4. 同名でもpathまたはqualified nameが違うsymbolを衝突させず、signatureまたはcontent変化を検出する。

Work 4Aの最初のcheckbox、Source Symbol Index生成、coverage、Ledger登録、Human意味確認は未完了である。

## 作業中の手戻り候補

同じ`Evidence：未記録`を持つchecklist節への手書き置換が、最初はsession終了節へ当たった。未コミットのうちに
Work 4A節へ訂正した。繰返し見出しへの曖昧な文章置換は手戻り候補であり、将来はsection IDまたは構造化更新を
機械処理する候補とする。
