# Claude → Codex：Work 7A runtime初期化時のsymlink差替え修正 完了報告

- 指示書：`records/session-handoffs/2026-08-09-codex-to-claude-work7a-root-initialization-symlink-correction.md`
- 作成日：2026-08-09
- 本報告はClaimであり、Codexの再レビューを待つ。

## 1. 判定

`completed_claim`

## 2. commit系列と変更path

| 種別 | SHA | 変更path |
| --- | --- | --- |
| correction base | `663ec503ce92307332a532af7b3eb7259b0b0fe3` | （先行GREEN。先行RED `b006e603e3e32c0baec47ec0c2fc87a3161b6abe`とも書き換えていない） |
| 指示書commit | `172db71681d75a9e6bc6e9b7037b806d52600e5d` | 修正指示書1fileのみ（212行。指示書§3の規定どおり正常） |
| 修正RED | `2239a02bb0d19d1d3f339cf74d654b0ee0c7cf15` | `tests/test_work7a_local_integrated_root_separation.py`のみ（93行追加、差替え3態様のTest） |
| 修正GREEN | `6f1c41708c606099139ba71d3ad0d529b25c536c` | `tools/deployment/local_integrated_roots.py`、`records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-evidence-v1.md`（新規）、`records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json`（新規） |

開始状態の機械照合：branch `main`、worktree clean、固定入力10fileのSHA-256は指示書の表と
全件一致。GREEN commitでTestは変更していない。

## 3. command・結果・exit code

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| 修正RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py` | 31件収集、新規3件のみ失敗（全件「差替えが検出されず例外が出ない」＝反証そのもの）、先行28件合格 | `1` |
| targeted GREEN | 同上command | 31 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py tests/test_layout_baseline.py tests/test_task_python_cache.py` | 46 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json` | 1313 passed、status `passed`（receipt再読込みでfailed 0を機械確認） | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |
| 事後transition | `python3 -m tools.development.work_unit_transition --work-status completed` | status `passed`、findings空 | `0` |

## 4. 3種の差替えの実測結果（合成fixtureのみ）

いずれも解決成功後・初期化呼出し前にsymlinkへ差し替えた3態様で、初期化は
filesystemへの最初の副作用より前に停止した。

| 差替え態様 | stop code | initializer呼出し（spy実測） | install／project | 作成artifact |
| --- | --- | --- | --- | --- |
| runtime root本体→install symlink | `runtime_initialization_target_invalid` | 0回 | inventory・SHA-256・mode・mtime不変 | なし（`install/projects`もsensitiveも未作成） |
| runtime配下`projects`→install symlink | 同上 | 0回 | 不変 | なし（`install/project-alpha`もsensitiveも未作成） |
| 解決時未作成の祖先→install symlink | 同上 | 0回 | 不変 | なし（`install/.reviewcompass3`もsensitiveも未作成） |

- `initialize_project_runtime_layout()`の非呼出しは、layout moduleへの記録spyで機械確認
  （呼出し回数0）。
- install／projectの不変は、root自身を含む全entryのmode・mtime・種別・内容SHA-256の
  snapshot一致で機械確認。
- 例外連鎖の文言に`tmp_path`配下のpath・fixture markerが含まれないことを機械確認。
- 先行の通常初期化（未作成runtimeの正常初期化、sensitiveと必要祖先のみ作成、mode 0700）は
  引き続き合格し、正例契約を弱めていない。

実装は`initialize_local_integrated_roots()`内のread-only再検査1点のみ：内部整合
（runtime／sensitive／project_id／profileの保存値とLayout解決値の一致）、install・projectの
現在identity（絶対path・実在directory・非symlink・canonical一致）、runtime・sensitiveの
canonical一致とoverlapなし、runtime→sensitiveの各path componentの非symlink・directory性を
検査し、不合格は新しい安定stop code `runtime_initialization_target_invalid`で
`RootSeparationError`とする。再検査中の`OSError`・`RuntimeError`もpathを出さず同stop codeへ
変換。resolver・write target関門・既存stop code・4 root構造・Layout v3再利用は不変。

## 5. SHA-256

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_local_integrated_root_separation.py` | `023f3dc7351a1934a74276e46aaa748677a68df66311173f03b9ae244e86e01a` |
| `tools/deployment/local_integrated_roots.py` | `bc9bc19bede6e9052b4222b02131d7b2b81ebca54d8f7de7d5b10a0fe7819870` |
| `records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-evidence-v1.md` | `49d557782f59f7435c8359a3b3e42e393bd24e752283bebfbd18aee2ad737159` |
| `records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json` | `1ad9bc09c9121a9809d1e06b2bc635f499890a2f476dc03c31b0260447e77a0f` |

## 6. 禁止操作・未実施の宣言

- 変更禁止path：`tools/layout/baseline.py`・authority・`TODO_NEXT_SESSION.md`・checklist・
  Plan・Decision・Issue・Candidate・workflow台帳・先行Evidence／receiptは未変更。
  変更は§2の4 file（Test 1・実装1・Evidence 1・receipt 1）のみ。
- 実data：実ホーム・既存利用者data・既存保全dataへのaccessなし。Testは`tmp_path`のみ。
- 外部操作：外部送信・push・tag・PR・`git add -A`／`git add .`・amend・rebase・reset・
  revert・履歴書換えは未実施。
- 後続Work：先行指示書の後続（Project Binding耐久保存、stable／development分離、
  実deployment等）は未実施。
- **原子的filesystem protocolは未実施**：本修正が検出するのは「解決後から初期化呼出し前に
  完了したfilesystem差替え」であり、初期化syscallと同時の別process競合の防止は
  指示書§4.2どおり後続とし、完了Claimに含めない。

## 7. 停止条件の発生有無と未実施範囲

- 停止条件1〜7：いずれも発生せず。
- 未実施範囲：TODO・checklistへの完了反映（Codex再レビュー後）、上記の後続Work・
  原子的filesystem protocol。
- 本報告fileはcommitに含めていない。Codexによる再レビューが終わるまで次の作業へ進まない。
