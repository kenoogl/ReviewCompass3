# GREEN Evidence：Work 7A 4種root分離の最初の縦切り

- 指示書：`records/session-handoffs/2026-08-08-codex-to-claude-work7a-four-root-separation.md`
- 作成日：2026-08-08
- executor：Claude（Codex指示書に基づく委譲作業）

## 1. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| implementation base | `ebc0bffdc42b7595727701788094fc74d201da04` | 指示書の固定base |
| 指示書配布 | `b754db2fd38c8f1d458d45d323dbdd502518934e` | 指示書1fileのみ追加（244行。指示書§3で正常と規定） |
| RED | `b006e603e3e32c0baec47ec0c2fc87a3161b6abe` | `tests/test_work7a_local_integrated_root_separation.py`のみ追加（453行、28 Test） |

開始時確認：branch `main`、worktree clean、固定入力10fileのSHA-256は指示書の表と全件一致。

## 2. 承認authority

- Layout Baseline v3（project-first runtime root）承認Decision：
  `records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json`
- Layout v3固定record（Testと実装が読む唯一のschema source）：
  `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`
- deployment／Project Artifact境界Decision：
  `records/development/2026-08-04-deployment-project-artifact-boundary-decision.json`

新しいroot schema・root kind・Layout schema version・Manifest schemaは作っていない。
用語対応は指示書§2どおり：install root＝Layout v3の`code_root`相当のdeployment所有root、
project root＝Project Manifestで`project_id`を固定したtarget checkout、runtime root＝
Layout v3の外部`runtime_root`、sensitive root＝`<runtime_root>/projects/<project_id>/runtime/sensitive`。

## 3. RED（Commit 1）

- command：`.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py`
- 結果：28件全てが新module `tools.deployment` の未実装（`ModuleNotFoundError`）だけを
  理由に失敗、exit code `1`。fixture不備・実在値・別原因の失敗は無い。
- Testはimplementationのprivate helper名・source文字列・禁止語検索に依存せず、公開APIの
  入出力とfilesystem上の事後状態をoracleにする。

## 4. GREEN（Commit 2）の実装

新規`tools/deployment/local_integrated_roots.py`のみ（`tools/deployment/`はnamespace package、
`__init__.py`なし。Python 4スペースindent）。

- `resolve_local_integrated_roots(layout_record_path, install_root, project_root, runtime_root)`：
  副作用なしresolver。Layout recordは`load_layout_baseline()`、runtime pathは
  `resolve_project_runtime_layout()`で解決し、schema・path組み立てを複製しない。
  install packageは`validate_deployment_package_layout()`で検査。`project_id`はproject内の
  `.reviewcompass/project-manifest.json`から読み（manifest検証はLayout実装の
  manifest loaderを再利用）、profileは`runtime`に固定。callerから`project_id`・profileを
  受け取らない。解決結果はimmutableな`LocalIntegratedRoots`
  （`install_root`・`project_root`・`runtime_root`・`sensitive_root`・`project_id`・
  `profile`・`runtime_layout`）。
- 物理分離：install・project・runtimeは実在祖先を含むcanonical化（`Path.resolve()`）後、
  どの2つも同一・parent／child・symlink別名にならないことを検査。sensitiveはLayout v3で
  解決したruntime profile rootの`sensitive`と完全一致し、install・projectの外にあることを検査。
  拒否は型付き`RootSeparationError`と安定stop code
  （`install_root_invalid`／`project_root_invalid`／`runtime_root_invalid`／`root_overlap`／
  `layout_baseline_invalid`／`install_package_invalid`／`project_manifest_invalid`／
  `runtime_layout_invalid`／`sensitive_root_invalid`）。例外文はstop codeのみで、
  manifestの未検査内容を含めない。
- `validate_root_write_target(roots, root_kind, target)`：絶対pathのみ受付け、canonical化後に
  宣言root kind配下だけを許可。`runtime`はsensitive配下を除外
  （`runtime_write_target_in_sensitive`）、`sensitive`はsensitive配下のみ。越境・prefix誤判定
  （`runtime-other`）・symlink escape・未知kindは`write_target_outside_root`／
  `write_target_invalid`／`unknown_root_kind`で拒否。検査のみでtargetを作成しない。
- `initialize_local_integrated_roots(roots)`：型付き解決結果だけを受付け、
  `initialize_project_runtime_layout(..., requested_kinds=["sensitive"])`を再利用して
  runtime root祖先とsensitive rootだけを作成。

RED commit後、Testは無変更（実装のみで合格）。

## 5. 4 root identityの解決値（合成fixtureの実測）

`tmp_path`配下で：install root＝合成install package、project root＝Project Manifest v2付き
合成project（`project_id = "project-alpha"`）、runtime root＝未作成
`<tmp>/runtime-home/.reviewcompass3`。解決結果：

- `install_root`／`project_root`：canonical化された各fixture root
- `runtime_root`：`<tmp>/runtime-home/.reviewcompass3`（未作成のまま解決成功）
- `sensitive_root`：`<runtime_root>/projects/project-alpha/runtime/sensitive`
- `project_id = "project-alpha"`、`profile = "runtime"`（固定）

## 6. 副作用境界の実測

- 解決：2回実行で全field一致。runtime rootは未作成のまま、install・projectの
  file inventory（path・SHA-256・mtime）は解決前後で不変。
- 初期化：作成されたのは`{"sensitive": <sensitive_root>}`と必要なruntime祖先のみ。
  Unixでruntime rootとsensitive rootのmode `0700`を実測。data・state・cache・logs・
  evaluation・configは未作成。install・projectのinventory／Digestは初期化前後で不変。

## 7. 正例・負例・境界例の件数と結果

| 区分 | Test | 件数 | 結果 |
| --- | --- | --- | --- |
| 正例 | 2回解決一致・無副作用（境界例3「未作成runtimeでの解決成功・mtime／inventory不変」を統合）／各kind直下target許可（4 kind）／明示初期化の作成範囲 | 6 | passed |
| 負例 | root overlap 6態様（同一・parent／child 4・symlink別名）／他rootへのwrite越境（4 kind×他root）／runtime→sensitive混入／symlink escape／relative path・未知kind／install・project不存在／manifest不正4態様／禁止内容入りpackage 2態様 | 20 | passed |
| 境界例 | `runtime-other` prefix誤判定防止／sensitiveはruntimeの子として解決され他のruntime配下kindと別 | 2 | passed |

合計28件（parametrize展開後）。

## 8. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py` | 28 failed（全件ModuleNotFoundError） | `1` |
| targeted GREEN | 同上command | 28 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py tests/test_layout_baseline.py tests/test_task_python_cache.py` | 46 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json` | 1310 passed、status `passed` | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |

公式receiptは再読込みし、status `passed`・exit `0`・1310件全合格・failed 0を機械確認済み。

## 9. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/deployment/local_integrated_roots.py` | `326a2d7f66c6db0ec886c9c6a4596db17ced33c040304658e305454908d3d052` |
| `tests/test_work7a_local_integrated_root_separation.py` | `18c7135762d43b3748741d39ff0fdb43bc1034a1a96a7d2916e818265999ffbb` |
| 公式receipt（同上JSON） | `5e741a6f4cff5c3adc67bfddde4a8a67caeb04193d520c74f940686db273516b` |

## 10. 禁止境界と未実施範囲

- `tools/layout/baseline.py`・authority record・`TODO_NEXT_SESSION.md`・initial checklist・
  Plan・Decision・Issue・Candidate・workflow台帳・既存Evidence：未変更。
- 実ホームの`~/.reviewcompass3`・既存runtime・project・保全data：読取り・書込み・変更・
  削除なし。Testは`tmp_path`のみ。
- Project Bindingの耐久保存、Snapshot／Change Set復元、Control／Execution I/O、
  checkpoint再開、side effect重複防止：未実施（後続）。
- stable／developmentのstate／data分離（Work 7A第5項）、Project Artifact更新時の
  再install不要E2E、Current Work Projection再生成：未実施（後続）。
- Deployment Manifest、package builder、staging、原子的切替、rollback、migration、
  uninstall、hook、watcher、scheduler、background service、実deployment：未実施。
- 新しいroot kind・Layout schema version・Manifest schema・外部依存・Human Decision：作成なし。
- 外部送信・push・tag・PR・amend・rebase・reset・履歴書換え・`git add -A`／`git add .`：未実施。
