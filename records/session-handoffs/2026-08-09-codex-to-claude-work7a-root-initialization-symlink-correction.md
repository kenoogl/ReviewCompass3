# Codex → Claude：Work 7A runtime初期化時のsymlink差替え修正

## 1. 判定と修正対象

- Humanは、Codexの独立レビューで見つかったroot境界違反に対し、選択肢1
  「いま対処」を選択した。
- 先行RED commit `b006e603e3e32c0baec47ec0c2fc87a3161b6abe`とGREEN commit
  `663ec503ce92307332a532af7b3eb7259b0b0fe3`は書き換えない。
- 修正対象は1点だけである。

  `resolve_local_integrated_roots()`の後、`initialize_local_integrated_roots()`の前に
  runtime pathまたはその下位componentをsymlinkへ差し替えられても、初期化は
  install、project、宣言runtime以外へ書かず、副作用前にfail-closedに停止する。

- Claudeはこの不一致のRED Testを先にcommitし、Testを変更せず最小の初期化前
  再検査でGREENにする。
- 完了後はClaude→Codex報告を作り、Codexの再レビューまで停止する。

## 2. 独立レビューで成立した反証

CodexはClaudeのfixturesに無い次の反証を`tmp_path`相当の一時directoryで機械実行した。

1. 合成install、Project Manifest付き合成project、未作成runtimeを正常に解決する。
2. 解決後、未作成runtime pathをinstall rootへのsymbolic linkに差し替える。
3. 先行の公開初期化APIを呼ぶ。

結果：exit code `1`で次を再現した。

```text
COUNTEREXAMPLE: initialization followed a replaced runtime symlink and wrote sensitive under install_root
```

作成先は`<install_root>/projects/<project_id>/runtime/sensitive`である。また現行Layout初期化は
runtime rootに`chmod(0700)`を行うため、symlink先のinstall rootのmodeも変え得る。

先行Test 28件、関連回帰 46件、公式全Test 1310件は再実行で全て合格したが、
この反証は先行fixtureに存在しない。したがって「installとprojectは初期化前後で不変」
という先行`completed_claim`は`report_execution_mismatch`であり、TODO・checklistの完了反映は
停止したままである。

## 3. 開始状態と固定入力

- branch：`main`
- correction implementation base：`663ec503ce92307332a532af7b3eb7259b0b0fe3`
- 本指示書はbaseの直後にCodexがcommitする。Claudeの開始HEADがbaseより1 commit先で、
  そのdiffが本指示書1 fileの追加だけであることは正常とする。
- base時点のbranchは`main`、worktreeはclean。

| role | path | SHA-256 |
| --- | --- | --- |
| 現在位置 | `TODO_NEXT_SESSION.md` | `e66ae9bee24ff6e3d5b4a7cec389b16638b0b3ada5a7769e72d62e2e6713aa38` |
| 元指示書 | `records/session-handoffs/2026-08-08-codex-to-claude-work7a-four-root-separation.md` | `4a00cb4a159cd65f31454a4f29e788f7a9046dbae56ec2a972de1a18fce5efda` |
| 先行Test | `tests/test_work7a_local_integrated_root_separation.py` | `18c7135762d43b3748741d39ff0fdb43bc1034a1a96a7d2916e818265999ffbb` |
| 先行実装 | `tools/deployment/local_integrated_roots.py` | `326a2d7f66c6db0ec886c9c6a4596db17ced33c040304658e305454908d3d052` |
| 先行GREEN Evidence | `records/development/2026-08-08-work7a-four-root-separation-green-evidence-v1.md` | `bcbeac855d73528f8c5c002797b63429853d59eb15286a1de35e1344bdfcd864` |
| 先行公式receipt | `records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json` | `5e741a6f4cff5c3adc67bfddde4a8a67caeb04193d520c74f940686db273516b` |
| Layout v3固定record | `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json` | `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38` |
| 共同作業手順 | `docs/development/codex-claude-collaboration.md` | `beab9d2cf0db4f31a869ae2d597dff8265ace9a022d83bba2d03b810a984cc49` |
| レビュー手順 | `docs/development/work-review-protocol.md` | `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967` |
| 先行Claude報告 | `records/session-handoffs/2026-08-08-claude-to-codex-work7a-four-root-separation.md` | `68cc12d4e727b2d7d3b55e88a1cbd596c250b7cc639a789c0b63994cfd298db0` |

作業開始時にcommit列、branch、worktree、固定入力Digestを機械照合する。不一致、
本指示書以外の先行差分、別executorの未commit差分がある場合は帰属を推測せず停止する。

## 4. 修正契約

### 4.1 初期化前のroot identity再検査

`initialize_local_integrated_roots()`は、filesystemへの最初の副作用より前に次を再検査する。

1. 引数が`LocalIntegratedRoots`である。
2. 保存された`runtime_root`と`runtime_layout.runtime_root`、`sensitive_root`と
   `runtime_layout.roots["sensitive"]`、`project_id`とprofileが内部整合している。
3. installとprojectは現在も絶対pathの実在directoryで、保存されたcanonical identityと一致する。
4. runtime rootとsensitive rootの現在のcanonical pathが解決時のidentityと一致し、
   install・projectとoverlapしない。
5. runtime rootからsensitive rootまでの存在する各path componentがsymlinkでなくdirectoryである。
   通常file、symlink、canonical identityの差替え、root escapeのどれかを1つでも検出したら
   停止する。

不安全な状態は全て`RootSeparationError`と新しい安定stop code
`runtime_initialization_target_invalid`で拒否する。例外文にhost pathや未検査内容を含めない。

### 4.2 副作用境界

- 再検査はread-onlyとし、不合格な場合は
  `initialize_project_runtime_layout()`を呼ばない。
- 不合格時はinstallとprojectのfile inventory、SHA-256、directory mode、mtimeを変えず、
  runtimeまたはsymlink先にfile・directoryを作らない。
- 通常の未作成runtime rootは引き続き初期化でき、sensitiveと必要なruntime祖先だけを
  作成する。先行の正例契約を弱めない。
- `initialize_project_runtime_layout()`が返す`LayoutError`に加え、初期化前検査で生じる
  `OSError`・`RuntimeError`はpathを出さず`RootSeparationError`へ変換する。
- 今回は「解決後から初期化呼出し前に完了したfilesystem差替え」を検出する。
  初期化syscallと同時の別processによる競合を防ぐ原子的filesystem protocolは後続であり、
  本修正の完了Claimに含めない。

### 4.3 先行契約の維持

- resolver、write target関門、4 root配置、`runtime` profile、Layout v3再利用、stop codeの
  既存意味は変えない。
- `tools.layout.baseline._load_project_manifest`の使用は本修正の対象にしない。
- 新しいroot kind、Layout／Manifest schema、外部依存を追加しない。

## 5. 修正Acceptance Test

`tests/test_work7a_local_integrated_root_separation.py`に、次の負例を追加する。

1. **runtime root本体の差替え**：未作成runtimeを解決後、install rootへのsymlinkに
   差し替えて初期化すると`runtime_initialization_target_invalid`で停止する。
2. **runtime下位componentの差替え**：解決後にruntime rootだけを通常directoryとして作り、
   その`projects`をinstall rootへのsymlinkにして初期化すると同じstop codeで停止する。
3. **runtime祖先identityの差替え**：解決時に未作成だったruntimeの祖先directoryを、
   解決後にinstall rootへのsymlinkとして作った場合も同じstop codeで停止する。

各Testで次を機械確認する。

- `initialize_project_runtime_layout()`が呼ばれない。
- installとprojectのfile inventory、SHA-256、directory mode、mtimeが初期化前後で不変。
- install、project、symlink先に`sensitive`またはその祖先が作成されない。
- 例外連鎖にpath・fixture markerが含まれない。
- 先行の通常初期化Testは引き続き合格する。

Testは実ホームや既存dataを使わず、`tmp_path`の合成fixtureだけで実行する。

## 6. TDDとcommit境界

### Commit 1：修正RED

- `tests/test_work7a_local_integrated_root_separation.py`だけを変更する。
- 実装前に対象Testを単独実行し、新規3 Testだけが期待したsymlink差替えで失敗し、
  先行28 Testは通ることとexit code `1`を確認する。
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

  `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json`

- 修正Evidence：
  `records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-evidence-v1.md`
- Evidenceにはbase、先行mismatch、修正RED commit、3種の差替え、副作用前停止、install／project
  不変、先行28 Test維持、targeted・関連・公式全Test、exit code、Digest、禁止境界、
  原子的競合防止が未実施であることを記録する。
- `git diff --check`、receipt再読込み、Evidence参照、SHA-256を機械照合する。
- 実装、Evidence、receiptだけを明示stageし、修正GREEN commitを作る。TestはRED commitのままとする。
- commit後に`python3 -m tools.development.work_unit_transition --work-status completed`を実行する。

## 7. 変更可能path

- `tests/test_work7a_local_integrated_root_separation.py`
- `tools/deployment/local_integrated_roots.py`
- `records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-evidence-v1.md`
- `records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json`

上記以外の変更が必要な場合は実装せず停止する。先行Testの期待と既存stop codeを
弱めない。

## 8. 禁止事項と停止条件

### 8.1 禁止事項

- 先行commitをamend、rebase、reset、revert、履歴書換えしない。
- `TODO_NEXT_SESSION.md`、checklist、Plan、Layout authority、Decision、Issue、Candidate、workflow台帳、
  先行Evidence・receiptを変更しない。
- resolverとwrite target関門の公開contract、4 root構造、profile、Manifest解決、初期化の
  正常範囲を変えない。
- Layout v3初期化を複製した新しいdirectory builder、新schema、新依存を作らない。
- 先行指示書の後続Work、実deployment、実ホーム・既存dataへのaccess、外部送信を行わない。
- push、tag、PR、`git add -A`、`git add .`を行わない。

### 8.2 停止条件

次のいずれかに該当したら、範囲を広げず停止する。

1. base、commit列、branch、worktree、固定入力Digestが不一致。
2. 変更可能path以外、特に`tools/layout/baseline.py`またはauthorityの変更が必要。
3. 差替えの拒否にLayout v3初期化の複製、新schema、外部依存、または原子的
   filesystem protocolの実装が必要。
4. REDの新規3 Testが期待した差替え以外の理由で失敗、または先行28 Testが不合格。
5. GREENのために先行Test、root構造、正常初期化、既存stop codeを弱める必要がある。
6. targeted、関連回帰、公式全Test、diff check、receipt、Digestのいずれかが不合格。
7. 実ホーム、既存利用者data、外部systemへのaccessが必要。

## 9. Claude→Codex報告

完了または停止後、次を作成し、commitに含めず停止する。

`records/session-handoffs/2026-08-09-claude-to-codex-work7a-root-initialization-symlink-correction.md`

報告には次を含める。

- `completed_claim`または`blocked_claim`
- correction base、指示書commit、修正RED、修正GREENのSHAと各変更path
- RED、targeted GREEN、関連回帰、公式全Test、diff checkのcommand・結果・exit code
- 3種のsymlink／identity差替えのstop code、initializer非呼出し、install／project不変、
  作成artifactなしの実測
- Test、実装、修正Evidence、修正receiptのSHA-256
- 変更禁止path、実data、外部操作、後続Work、原子的filesystem protocolが未実施であること
- 停止条件の発生有無と未実施範囲

Codexは報告後、commit列、diff、Digest、Test、3種の反証、副作用なし停止、禁止境界を
独立確認する。本修正もfilesystem write境界の守り役であるため`high`とし、
Claudeのfixturesに無い新しい反証を最低1件機械実行する。
