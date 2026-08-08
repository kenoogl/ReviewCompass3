# Codex → Claude：Work 7A 4種root分離の最初の縦切り

## 1. 役割と作業単位

- Humanは`TODO_NEXT_SESSION.md`の次作業候補に対して「次へ」と指示し、
  `docs/development/codex-claude-collaboration.md`に従って進めることを先に指示した。
- Codexは固定入力、受入条件、変更可能path、禁止事項、停止条件を本指示書へ
  固定する。
- ClaudeはWork 7Aの第1項に限り、次の**1つの小さなE2E縦切り**をTDDで実装する。
  1. install、project、runtime、sensitiveの4種root identityを、現行Layout v3から
     副作用なしで解決する。
  2. 承認済み配置に従って物理分離を検査し、宣言rootを越えるwrite targetを
     fail-closedに拒否する。
  3. 明示初期化でruntime rootとsensitive rootだけを作成し、install packageと
     target projectを書き換えない。
- 完了後は指定のClaude→Codex報告を作成し、Codexの独立確認まで停止する。

## 2. authorityの読み方

本作業で新しいroot schemaを作らない。用語は次のように現行authorityへ対応させる。

| Work 7Aの用語 | 現行authority上の意味 |
| --- | --- |
| install root | Layout v3の`code_root`。検証済みinstalled codeを持つdeployment所有root |
| project root | Project Manifestで`project_id`を固定したtarget project checkout |
| runtime root | Layout v3の外部`runtime_root`。deployment packageとGitに含めない |
| sensitive root | `<runtime_root>/projects/<project_id>/runtime/sensitive`。runtime profile内の専用root |

- install、project、runtimeは相互に非overlapとする。
- sensitiveは承認済みLayout v3どおりruntime rootの子である。これをruntime rootの外へ
  出す変更は禁止する。
- sensitiveはinstallとprojectの外にあり、同じruntime profileのdata、state、cache、
  logs、evaluationと異なるroot identityを持つ。
- profileは最小deployment E2Eの`runtime`に固定する。`development`と`runtime`間の
  state／data分離はWork 7A第5項の後続であり、今回実装しない。

## 3. 開始状態と固定入力

- branch：`main`
- implementation base：`ebc0bffdc42b7595727701788094fc74d201da04`
- 本指示書はimplementation baseの直後にCodexがcommitする。Claudeの開始HEADがbaseより
  1 commit先で、そのdiffが本指示書1 fileの追加だけであることは正常とする。
- implementation base時点のworktreeはcleanである。

| role | path | SHA-256 |
| --- | --- | --- |
| 現在位置 | `TODO_NEXT_SESSION.md` | `e66ae9bee24ff6e3d5b4a7cec389b16638b0b3ada5a7769e72d62e2e6713aa38` |
| 現行Plan | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Work 7A checklist | `docs/development/2026-08-03-initial-development-checklist.md` | `32c5fe8e6707a2f139a7486a5a6da9e484629f57b1cf6200dd5a96fca0611496` |
| 共同作業手順 | `docs/development/codex-claude-collaboration.md` | `beab9d2cf0db4f31a869ae2d597dff8265ace9a022d83bba2d03b810a984cc49` |
| 作業レビュー手順 | `docs/development/work-review-protocol.md` | `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967` |
| Layout v3承認Decision | `records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json` | `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275` |
| Layout v3固定record | `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json` | `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38` |
| deployment／Project Artifact境界Decision | `records/development/2026-08-04-deployment-project-artifact-boundary-decision.json` | `237dd1d0d40304240f0d8376713509c34364aaa6369d3161df3d3be2cc623c1b` |
| 現行Layout実装 | `tools/layout/baseline.py` | `6d00c3053da820cd694a0c4b47d5e5f1b632f00d83e81691f99060626bc94cb7` |
| Layout v3 Test | `tests/test_project_runtime_layout.py` | `255d3aadd102093849001cdd3b8e0716a2211096680bee281ce4443ed171aa4a` |

作業開始時にbranch、commit列、worktree、固定入力Digestを機械照合する。不一致、
本指示書以外の先行差分、別executorの未commit差分がある場合は帰属を推測せず停止する。

## 4. 実装契約

### 4.1 新規の合成resolver

`tools/deployment/local_integrated_roots.py`に、Layout v3を再利用する最小APIを作る。

- 公開の副作用なしresolverは、少なくとも次を受け取る。
  - Layout v3 recordの絶対path
  - 既存install rootの絶対path
  - 既存project rootの絶対path
  - runtime rootの絶対path（未作成でよい）
- callerから`project_id`または任意profileを受け取らない。`project_id`はproject内の
  `.reviewcompass/project-manifest.json`から読み、profileは`runtime`に固定する。
- Layout recordは`tools.layout.baseline.load_layout_baseline()`、runtime pathは
  `resolve_project_runtime_layout()`で解決する。同じschema・path組み立てを複製しない。
- install packageは`validate_deployment_package_layout()`で検査し、Project Artifactまたは
  runtime rootを内包するpackageを拒否する。
- 解決結果はimmutableな構造で、少なくとも`install_root`、`project_root`、
  `runtime_root`、`sensitive_root`、`project_id`、`profile`、Layout v3の解決結果を持つ。
- resolver自体はdirectoryやfileを作成・書換えしない。

### 4.2 物理分離とfail-closed

- install、project、runtimeは実在する祖先を含めてcanonical pathへ正規化し、どの2つも
  parent／child、同一path、symlink経由の別名にならないことを確認する。
- sensitive rootはLayout v3で解決したruntime profile rootの`sensitive`と完全一致し、
  installとprojectの外にあることを確認する。
- 相対path、存在しないinstall／project、不正Project Manifest、root overlap、symlinkによる
  escape、Layout不一致は、型付きの定常な例外と安定stop codeで拒否する。
- 例外文にproject manifestの未検査内容を出さない。

### 4.3 write target関門

解決結果とroot kind（`install`、`project`、`runtime`、`sensitive`）およびwrite targetを受け取る
公開検査APIを作る。

- targetは絶対pathだけを受け付け、宣言されたroot kindの配下だけを許可する。
- `runtime`の許可範囲から`sensitive_root`配下を除外する。runtime一般writeが
  sensitiveへ混入することを許可しない。
- `sensitive`はsensitive root配下だけを許可する。
- 他rootへの越境、root本体と子pathの境界の誤判定（例：`runtime-other`）、
  実在symlinkを介した許可root外へのescape、未知root kindを全て拒否する。
- このAPIは検査だけを行い、targetを作成しない。

### 4.4 明示初期化

- 初期化APIは上記の型付き解決結果だけを受け付ける。
- `initialize_project_runtime_layout(..., requested_kinds=["sensitive"])`を再利用し、
  runtime rootの必要な祖先とsensitive rootだけを作成する。
- Unixではruntime rootとsensitive rootのmode `0700`を実測する。Windows ACLは後続とする。
- install、project、同じruntime profileのdata、state、cache、logs、evaluation、
  configを作成・変更しない。installとprojectは初期化前後のfile inventoryとDigestが
  一致することをTestで固定する。

## 5. Acceptance Test

新規`tests/test_work7a_local_integrated_root_separation.py`に、`tmp_path`の合成install package、
Project Manifest v2付きproject、未作成runtime rootだけを使うTestを書く。

### 5.1 正例

1. 解決を2回行っても4 root、`project_id`、`runtime` profileが一致し、何も作成しない。
2. 各root kindの直下の合成targetをそのroot kindで検査すると許可される。
3. 明示初期化でsensitiveと必要なruntime祖先だけが作成され、installとprojectの
   inventory／Digestが不変である。

### 5.2 負例

1. install、project、runtimeの各組合せで、同一・parent／child・symbolic link別名の
   overlapを拒否する。
2. 各root kindから他rootへのwrite targetを全て拒否し、`runtime`からsensitiveへの
   writeも拒否する。
3. 許可root内に置いたsymlinkがroot外を指すtargetを拒否する。
4. relative path、未知root kind、存在しないinstall／project、不正／欠落Project Manifest、
   Project Artifactまたはruntime rootを含むinstall packageを拒否する。

### 5.3 境界例

1. `runtime-other`のような文字列prefixがroot配下と誤判定されない。
2. sensitiveはruntimeの子であっても正常に解決され、それ以外のruntime root kindとは
   異なることを固定する。
3. runtime root未作成の解決は成功し、解決中はinstall、project、runtimeの全ての
   mtime／inventoryを変えない。

Testはimplementationのprivate helper名、source文字列、禁止語検索に依存せず、公開APIの
入出力とfilesystem上の事後状態をoracleにする。

## 6. TDDとcommit境界

### Commit 1：RED Testだけ

- `tests/test_work7a_local_integrated_root_separation.py`だけを作成する。
- 実装前に対象Testを単独commandで実行し、新module／APIの未実装だけを理由に
  exit code `1`で失敗することを確認する。
- `git diff --check`後、Test pathだけを明示stageし、RED Testだけのcommitを作る。

### Commit 2：GREEN実装とEvidence

- RED commit後は、要求の誤解または未承認設計変更が判明しない限り、Testを変更せず
  実装側を修正して通す。
- 対象Test、関連回帰、公式全Testをそれぞれ別の単独commandで実行し、exit codeで
  合否を判定する。
- 関連回帰には少なくとも次を含める。
  - `tests/test_project_runtime_layout.py`
  - `tests/test_layout_baseline.py`
  - `tests/test_task_python_cache.py`
- 公式全Test command：

  `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json`

- GREEN Evidence：
  `records/development/2026-08-08-work7a-four-root-separation-green-evidence-v1.md`
- Evidenceにはbase、RED commit、承認authority、4 root identity、解決／初期化の副作用境界、
  正例・負例・境界例、targeted・関連・公式全Test、exit code、Digest、禁止境界、
  未実施範囲を記録する。
- `git diff --check`、receipt再読込み、Evidence参照、SHA-256を機械照合する。
- 実装、Evidence、receiptだけを明示stageしてGREEN commitを作る。TestはRED commitのままとする。
- commit後に`python3 -m tools.development.work_unit_transition --work-status completed`を実行する。

## 7. 変更可能path

- `tests/test_work7a_local_integrated_root_separation.py`
- `tools/deployment/local_integrated_roots.py`
- `records/development/2026-08-08-work7a-four-root-separation-green-evidence-v1.md`
- `records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json`

`tools/deployment/`はPython namespace packageとし、`__init__.py`は追加しない。上記以外の変更が
必要な場合は実装せず停止する。`tools/layout/baseline.py`と固定したTestは変更しない。
Pythonはproject規則どおり4スペースindentとする。

## 8. 禁止事項と停止条件

### 8.1 禁止事項

- `TODO_NEXT_SESSION.md`、initial checklist、Plan、Layout authority、Decision、Issue、Candidate、
  workflow台帳、既存Evidenceを変更しない。完了反映はCodexの独立確認後とする。
- Project Bindingの耐久保存、別checkout／project移動後のSnapshot／Change Set復元、
  Control／Execution I/O、checkpoint再開、side effect重複防止を実装しない。
- stable／developmentのstate／data分離、Project Artifact更新時の再install不要E2E、
  Current Work Projection再生成を実装しない。
- Deployment Manifest、package builder、staging、原子的切替、rollback、migration、uninstall、
  hook、watcher、scheduler、background service、実deploymentを実装・実行しない。
- 実ホームの`~/.reviewcompass3`、既存runtime・project・保全dataを読まない、書かない、
  変更・削除しない。Testは`tmp_path`のみで行う。
- 新しいroot kind、Layout schema version、Manifest schema、外部依存、Human Decisionを作らない。
- 外部送信、push、tag、PR、amend、rebase、reset、履歴書換え、`git add -A`、
  `git add .`を行わない。

### 8.2 停止条件

次のいずれかに該当したら、範囲を広げず停止する。

1. base、commit列、branch、worktree、固定入力Digestが不一致。
2. 変更可能path以外、特に`tools/layout/baseline.py`またはauthority recordの変更が必要。
3. `install_root`という新しいLayout root kind、sensitiveをruntime外に出す変更、
   任意profile選択が必要。
4. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
5. rootの正規化、symlink境界、write target許可をfail-closedにするために
   既存Layout契約の変更が必要。
6. targeted、関連回帰、公式全Test、diff check、receipt、Digestのいずれかが不合格。
7. 実ホーム、既存利用者data、外部systemへのaccessが必要。
8. 後続checkboxの設計または意味的裁定が必要。

## 9. Claude→Codex報告

完了または停止後、次を作成し、commitに含めず停止する。

`records/session-handoffs/2026-08-08-claude-to-codex-work7a-four-root-separation.md`

報告には次を含める。

- `completed_claim`または`blocked_claim`
- implementation base、指示書commit、RED、GREENのSHAと各commitの変更path
- RED、targeted GREEN、関連回帰、公式全Test、diff checkのcommand・結果・exit code
- 4 rootの解決値、副作用なし解決、初期化後の作成path、install／project不変、
  正例・負例・境界例の件数と結果
- Test、実装、Evidence、receiptのSHA-256
- 変更禁止path、実runtime、外部操作、push、後続Workが未実施であること
- 停止条件の発生有無と未実施範囲

Claudeの報告はClaimでありEvidenceそのものではない。Codexがcommit列、diff、Digest、
Test、4 rootのwrite境界、初期化side effect、禁止境界を独立確認する。本作業は
filesystem write境界の守り役を実装するため`high`とし、CodexはClaudeのfixturesに無い
新しい反証を最低1件機械実行する。
