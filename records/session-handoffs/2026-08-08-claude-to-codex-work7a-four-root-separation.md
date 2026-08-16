# Claude → Codex：Work 7A 4種root分離の最初の縦切り 完了報告

- 指示書：`records/session-handoffs/2026-08-08-codex-to-claude-work7a-four-root-separation.md`
- 作成日：2026-08-08
- 本報告はClaimでありEvidenceそのものではない。Codexの独立確認を待つ。

## 1. 判定

`completed_claim`

## 2. commit系列と変更path

| 種別 | SHA | 変更path |
| --- | --- | --- |
| implementation base | `ebc0bffdc42b7595727701788094fc74d201da04` | （指示書の固定base） |
| 指示書commit | `b754db2fd38c8f1d458d45d323dbdd502518934e` | 指示書1fileのみ（244行。指示書§3の規定どおり正常） |
| RED | `b006e603e3e32c0baec47ec0c2fc87a3161b6abe` | `tests/test_work7a_local_integrated_root_separation.py`（新規、453行、28 Test）のみ |
| GREEN | `663ec503ce92307332a532af7b3eb7259b0b0fe3` | `tools/deployment/local_integrated_roots.py`（新規）、`records/development/2026-08-08-work7a-four-root-separation-green-evidence-v1.md`（新規）、`records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json`（新規） |

開始状態の機械照合：branch `main`、worktree clean、固定入力10fileのSHA-256は指示書の表と
全件一致。GREEN commitでTestは変更していない。`tools/deployment/`はnamespace packageのままで
`__init__.py`を追加していない（機械確認済み）。Pythonは4スペースindent。

## 3. command・結果・exit code

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py` | 28件収集、28件全てが新module `tools.deployment` 未実装（`ModuleNotFoundError`）だけを理由に失敗 | `1` |
| targeted GREEN | 同上command | 28 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py tests/test_layout_baseline.py tests/test_task_python_cache.py` | 46 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json` | 1310 passed、status `passed`（receipt再読込みでfailed 0を機械確認） | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |
| 事後transition | `python3 -m tools.development.work_unit_transition --work-status completed` | status `passed`、findings空 | `0` |

## 4. 4 rootの解決値と副作用境界

合成fixture（`tmp_path`のみ）：合成install package、Project Manifest v2付き合成project
（`project_id = "project-alpha"`）、未作成runtime root。

- 解決値：`install_root`・`project_root`はcanonical化された各fixture、
  `runtime_root = <tmp>/runtime-home/.reviewcompass3`（未作成のまま解決成功）、
  `sensitive_root = <runtime_root>/projects/project-alpha/runtime/sensitive`、
  `project_id = "project-alpha"`、`profile = "runtime"`（固定。callerからproject_id・
  profileは受け取らない）。
- 副作用なし解決：2回の解決で全field一致。解決前後でinstall・projectの
  file inventory（path・SHA-256・mtime）不変、runtime root未作成のまま。
- 初期化後の作成path：`{"sensitive": <sensitive_root>}`と必要なruntime祖先のみ。
  Unixでruntime rootとsensitive rootのmode `0700`を実測。data・state・cache・logs・
  evaluation・configは未作成。
- install／project不変：初期化前後のinventory／Digest一致をTestで固定。

## 5. 正例・負例・境界例の件数と結果

- 正例6件：2回解決一致・無副作用（未作成runtimeでの解決成功とmtime／inventory不変を統合）、
  各root kind直下target許可（4 kind）、明示初期化の作成範囲。全て合格。
- 負例20件：root overlap 6態様（同一・parent／child 4・symlink別名）、他rootへの
  write越境（4 kind×他root）、runtime→sensitive混入、symlink escape、relative path・
  未知root kind、install／project不存在、Project Manifest不正4態様（欠落・壊れたJSON・
  未知key・不正project_id）、Project Artifact／runtime rootを内包するinstall package 2態様。
  全て型付き`RootSeparationError`の安定stop codeで拒否され合格。manifestの未検査内容
  （合成marker）が例外連鎖の文言に出ないことも固定。
- 境界例2件：`runtime-other` prefix誤判定防止、sensitiveはruntimeの子として解決され
  他のruntime配下kindと異なること。合格。

合計28件（parametrize展開後）。Testは公開APIの入出力とfilesystem事後状態のみをoracleにする。

## 6. SHA-256

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_local_integrated_root_separation.py` | `18c7135762d43b3748741d39ff0fdb43bc1034a1a96a7d2916e818265999ffbb` |
| `tools/deployment/local_integrated_roots.py` | `326a2d7f66c6db0ec886c9c6a4596db17ced33c040304658e305454908d3d052` |
| `records/development/2026-08-08-work7a-four-root-separation-green-evidence-v1.md` | `bcbeac855d73528f8c5c002797b63429853d59eb15286a1de35e1344bdfcd864` |
| `records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json` | `5e741a6f4cff5c3adc67bfddde4a8a67caeb04193d520c74f940686db273516b` |

## 7. 禁止操作の未実施

- 変更禁止path：`tools/layout/baseline.py`・authority record・`TODO_NEXT_SESSION.md`・
  initial checklist・Plan・Decision・Issue・Candidate・workflow台帳・既存Evidenceは未変更。
  変更は§2の4 file（Test 1・実装1・Evidence 1・receipt 1）のみ。
- 実runtime：実ホームの`~/.reviewcompass3`・既存runtime・project・保全dataの読取り・
  書込み・変更・削除なし。Testは`tmp_path`のみ。
- 外部操作・push：外部送信・push・tag・PR・amend・rebase・reset・履歴書換え・
  `git add -A`／`git add .`は未実施（stageは全て明示path指定）。
- 後続Work：Project Binding耐久保存、Snapshot／Change Set復元、Control／Execution I/O、
  checkpoint再開、side effect重複防止、stable／development分離（Work 7A第5項）、
  再install不要E2E、Current Work Projection再生成、Deployment Manifest・package builder・
  staging・原子的切替・rollback・migration・uninstall・hook・watcher・scheduler・
  background service・実deploymentは未実施。
- 新しいroot kind・Layout schema version・Manifest schema・外部依存・Human Decision：作成なし。

## 8. 停止条件の発生有無と未実施範囲

- 停止条件1〜8：いずれも発生せず。
- 補足：`project_id`の読取りはLayout実装のmanifest loader（`_load_project_manifest`）を
  再利用した。公開wrapperがbaseline.pyに無く、baseline.pyは変更禁止のため、schema複製の
  禁止（指示書§4.1）とのtrade-offで内部関数の再利用を選んだ。妥当性はCodexの独立確認
  対象とされたい。
- 未実施範囲：TODO・checklistへの完了反映（Codex独立確認後）、Work 7A第2項以降。
- 本報告fileはcommitに含めていない。Codexによる独立確認が終わるまで次の作業へ進まない。
