# Codex → Claude：Work 7A例外連鎖のhost path漏洩修正

## 1. 判定と修正対象

- Humanは、Codexの再レビューで見つかった例外連鎖のpath漏洩に対し、選択肢1
  「いま対処」を選択した。
- 先行のWork 7A RED／GREENとsymlink差替え修正RED／GREENは書き換えない。
- 修正対象は1点だけである。

  初期化前のroot再検査中に`OSError`または`RuntimeError`が発生しても、
  公開APIは`runtime_initialization_target_invalid`でfail-closedに停止し、
  表面文言、`__cause__`、`__context__`、表示tracebackのどこにも入力由来のhost pathや
  未検査内容を残さない。

- root分離、symlink差替え拒否、初期化範囲は変えない。
- Claudeは修正REDを先にcommitし、Testを変更せず最小修正でGREENにする。

## 2. 独立レビューで成立した反証

CodexはClaudeのfixturesに無い次の反証を一時directoryで実行した。

1. 合成install、project、未作成runtimeを正常に解決する。
2. runtime pathを、自分自身を指すsymbolic link loopへ差し替える。
3. `initialize_local_integrated_roots()`を呼ぶ。
4. `RootSeparationError`から`__cause__`を辿る。

表面のstop codeは`runtime_initialization_target_invalid`であり、filesystem writeも発生しない。
しかし次をexit code `1`で再現した。

```text
COUNTEREXAMPLE: RuntimeError cause leaked the host path through the RootSeparationError exception chain
```

原因は`initialize_local_integrated_roots()`がpath入り`RuntimeError`を
`raise RootSeparationError(...) from error`で連結していることである。

修正Test 31件、関連回帰 46件、公式全Test 1313件は再実行で合格し、3種の
symlink差替えも副作用前に拒否した。ただし「例外連鎖にpathを含めない」という
`completed_claim`は`report_execution_mismatch`であり、TODO・checklistの完了反映は停止したままである。

## 3. 開始状態と固定入力

- branch：`main`
- correction implementation base：`6f1c41708c606099139ba71d3ad0d529b25c536c`
- 本指示書はbaseの直後にCodexがcommitする。Claudeの開始HEADがbaseより1 commit先で、
  そのdiffが本指示書1 fileの追加だけであることは正常とする。
- base時点のbranchは`main`、worktreeはclean。

| role | path | SHA-256 |
| --- | --- | --- |
| 現在位置 | `TODO_NEXT_SESSION.md` | `e66ae9bee24ff6e3d5b4a7cec389b16638b0b3ada5a7769e72d62e2e6713aa38` |
| 元修正指示書 | `records/session-handoffs/2026-08-09-codex-to-claude-work7a-root-initialization-symlink-correction.md` | `1624176edc1a3e6ac0c13fe40a47125d22964c43e14653a644d6142ba1e3a8d8` |
| 現行Test | `tests/test_work7a_local_integrated_root_separation.py` | `023f3dc7351a1934a74276e46aaa748677a68df66311173f03b9ae244e86e01a` |
| 現行実装 | `tools/deployment/local_integrated_roots.py` | `bc9bc19bede6e9052b4222b02131d7b2b81ebca54d8f7de7d5b10a0fe7819870` |
| 先行修正Evidence | `records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-evidence-v1.md` | `49d557782f59f7435c8359a3b3e42e393bd24e752283bebfbd18aee2ad737159` |
| 先行修正receipt | `records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json` | `1ad9bc09c9121a9809d1e06b2bc635f499890a2f476dc03c31b0260447e77a0f` |
| 共同作業手順 | `docs/development/codex-claude-collaboration.md` | `beab9d2cf0db4f31a869ae2d597dff8265ace9a022d83bba2d03b810a984cc49` |
| レビュー手順 | `docs/development/work-review-protocol.md` | `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967` |
| 先行Claude報告 | `records/session-handoffs/2026-08-09-claude-to-codex-work7a-root-initialization-symlink-correction.md` | `1ed9f0d9ef08c72aa993eb46ff7e5620bc3ff8ebc629286cd884aa8ac1809267` |

作業開始時にcommit列、branch、worktree、固定入力Digestを機械照合する。不一致、
本指示書以外の先行差分、別executorの未commit差分がある場合は帰属を推測せず停止する。

## 4. 修正契約

### 4.1 例外変換の契約

- `_revalidate_initialization_targets()`の実行中に`OSError`または`RuntimeError`を
  検出した場合、公開APIは`RootSeparationError`の安定stop code
  `runtime_initialization_target_invalid`で停止する。
- 返す`RootSeparationError`は、pathや未検査内容を持つ原因例外を`__cause__`または
  `__context__`に保持しない。単に`raise ... from None`で表示を抑制するだけでなく、
  例外objectとして辿っても原因例外へ到達できないことを受入条件とする。
- 表面文言と`traceback.format_exception()`の出力には、入力由来のhost path、
  fixture marker、原因例外文言を含めない。
- 変換後の`RootSeparationError`を原因例外のhandler外でraiseするなど、
  `__cause__ is None`かつ`__context__ is None`を満たす最小実装とする。

### 4.2 副作用と互換境界

- 例外変換中に`initialize_project_runtime_layout()`を呼ばず、filesystemを変更しない。
- 先行31 Test、3種のsymlink差替え拒否、通常初期化、root解決、write target関門、
  既存stop codeを変えない。
- 初期化syscallと同時の別process競合を防ぐ原子的filesystem protocolは後続であり、
  本修正の完了Claimに含めない。
- `tools.layout.baseline._load_project_manifest`の使用は本修正の対象にしない。

## 5. 修正Acceptance Test

`tests/test_work7a_local_integrated_root_separation.py`に次の2 Testを追加する。

1. **実symlink loop**：解決後のruntime pathを自己参照symlinkにし、公開初期化APIを
   呼ぶ。`runtime_initialization_target_invalid`で停止し、`__cause__`・`__context__`が
   どちらも`None`で、表示tracebackに`tmp_path`やfixture markerが無いことを固定する。
2. **強制RuntimeError**：公開初期化APIの再検査中に、合成path markerを含む
   `RuntimeError`を決定的に発生させる。同じstop code、cause／context `None`、
   表示tracebackと例外文言へのmarker非漏洩を固定する。

両Testで次も確認する。

- `initialize_project_runtime_layout()`の呼出し0回。
- installとprojectのstate snapshot不変。
- runtime、install、project、symlink先に新しいartifactを作成しない。
- 先行31 Testは引き続き合格する。

Testは`tmp_path`と`monkeypatch`の合成値だけを使い、実ホーム・既存dataを読まない。

## 6. TDDとcommit境界

### Commit 1：修正RED

- `tests/test_work7a_local_integrated_root_separation.py`だけを変更する。
- 実装前に対象Testを単独実行し、新規2 Testだけが例外連鎖または表示tracebackへの
  path／marker漏洩で失敗し、先行31 Testは通ることとexit code `1`を確認する。
- `git diff --check`後、Test pathだけを明示stageし、修正RED commitを作る。

### Commit 2：修正GREEN

- RED commit後はTestを変更せず、`tools/deployment/local_integrated_roots.py`だけを
  実装修正して通す。
- 対象Test、関連回帰、公式全Testを別々の単独commandで実行し、exit codeで判定する。
- 関連回帰には少なくとも次を含める。
  - `tests/test_project_runtime_layout.py`
  - `tests/test_layout_baseline.py`
  - `tests/test_task_python_cache.py`
- 公式全Test command：

  `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-exception-chain-path-correction-green-test-receipt-v1.json`

- 修正Evidence：
  `records/development/2026-08-09-work7a-exception-chain-path-correction-green-evidence-v1.md`
- Evidenceにはbase、先行mismatch、修正RED commit、symlink loop、強制`RuntimeError`、
  cause／context／traceback非漏洩、副作用なし停止、先行31 Test維持、targeted・関連・公式全Test、
  exit code、Digest、禁止境界、原子的競合防止が未実施であることを記録する。
- `git diff --check`、receipt再読込み、Evidence参照、SHA-256を機械照合する。
- 実装、Evidence、receiptだけを明示stageし、修正GREEN commitを作る。TestはRED commitのままとする。
- commit後に`python3 -m tools.development.work_unit_transition --work-status completed`を実行する。

## 7. 変更可能path

- `tests/test_work7a_local_integrated_root_separation.py`
- `tools/deployment/local_integrated_roots.py`
- `records/development/2026-08-09-work7a-exception-chain-path-correction-green-evidence-v1.md`
- `records/development/2026-08-09-work7a-exception-chain-path-correction-green-test-receipt-v1.json`

上記以外の変更が必要な場合は実装せず停止する。

## 8. 禁止事項と停止条件

### 8.1 禁止事項

- 先行commitをamend、rebase、reset、revert、履歴書換えしない。
- `TODO_NEXT_SESSION.md`、checklist、Plan、Layout authority、Decision、Issue、Candidate、workflow台帳、
  先行Evidence・receiptを変更しない。
- root resolver、write target関門、root配置、profile、Manifest解決、symlink再検査の
  成否条件を変えない。
- 新しい例外schema、root kind、Layout／Manifest schema、外部依存を作らない。
- 先行指示書の後続Work、原子的filesystem protocol、実deployment、実data access、
  外部送信を行わない。
- push、tag、PR、`git add -A`、`git add .`を行わない。

### 8.2 停止条件

次のいずれかに該当したら、範囲を広げず停止する。

1. base、commit列、branch、worktree、固定入力Digestが不一致。
2. 変更可能path以外の変更が必要。
3. 例外objectから原因例外を切り離すために新schema、外部依存、または公開contract変更が必要。
4. REDの新規2 Testが期待したpath／marker漏洩以外の理由で失敗、または先行31 Testが不合格。
5. GREENのために先行Test、stop code、root分離、通常初期化を弱める必要がある。
6. targeted、関連回帰、公式全Test、diff check、receipt、Digestのいずれかが不合格。
7. 実ホーム、既存利用者data、外部systemへのaccessが必要。

## 9. Claude→Codex報告

完了または停止後、次を作成し、commitに含めず停止する。

`records/session-handoffs/2026-08-09-claude-to-codex-work7a-exception-chain-path-correction.md`

報告には次を含める。

- `completed_claim`または`blocked_claim`
- correction base、指示書commit、修正RED、修正GREENのSHAと各変更path
- RED、targeted GREEN、関連回帰、公式全Test、diff checkのcommand・結果・exit code
- symlink loopと強制`RuntimeError`のstop code、cause／contextの値、traceback非漏洩、
  initializer非呼出し、filesystem不変の実測
- Test、実装、修正Evidence、修正receiptのSHA-256
- 変更禁止path、実data、外部操作、後続Work、原子的filesystem protocolが未実施であること
- 停止条件の発生有無と未実施範囲

Codexは報告後、commit列、diff、Digest、Test、例外object・traceback、副作用なし停止、
禁止境界を独立確認する。本修正もfilesystem write境界の守り役であるため`high`とし、
Claudeのfixturesに無い新しい反証を最低1件機械実行する。
