# GREEN Evidence：Work 7A runtime初期化時のsymlink差替え修正

- 指示書：`records/session-handoffs/2026-08-09-codex-to-claude-work7a-root-initialization-symlink-correction.md`
- 作成日：2026-08-09
- executor：Claude（Codex修正指示書に基づく委譲作業）

## 1. 先行mismatchと修正対象

Codexの独立レビューで、`resolve_local_integrated_roots()`の後に未作成runtime pathを
install rootへのsymbolic linkへ差し替えてから`initialize_local_integrated_roots()`を呼ぶと、
初期化が差替え後のsymlinkを辿り`<install_root>/projects/<project_id>/runtime/sensitive`を
作成し、runtime rootへの`chmod(0700)`がsymlink先のinstall root modeも変え得ることが
反証された（先行fixtureに無い反証）。「installとprojectは初期化前後で不変」という先行
`completed_claim`は`report_execution_mismatch`。本修正は、初期化の最初の副作用より前の
read-onlyなroot identity再検査1点だけで解消する。

## 2. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| correction implementation base | `663ec503ce92307332a532af7b3eb7259b0b0fe3` | 先行GREEN（書き換えていない。先行RED `b006e603e3e32c0baec47ec0c2fc87a3161b6abe`も同様） |
| 指示書配布 | `172db71681d75a9e6bc6e9b7037b806d52600e5d` | 修正指示書1fileのみ追加（212行。指示書§3で正常と規定） |
| 修正RED | `2239a02bb0d19d1d3f339cf74d654b0ee0c7cf15` | `tests/test_work7a_local_integrated_root_separation.py`のみ（symlink差替え3態様のTest、93行追加） |

開始時確認：branch `main`、worktree clean、固定入力10fileのSHA-256は指示書の表と全件一致。

## 3. 修正RED（Commit 1）

- command：`.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py`
- 結果：31件収集、新規3件（runtime root本体差替え・下位component `projects`差替え・
  解決時未作成だった祖先の差替え）のみが「差替えが検出されず例外が出ない
  （DID NOT RAISE）」という反証そのものを理由に失敗、先行28件は合格、exit code `1`。

## 4. 修正GREEN（Commit 2）の実装

`tools/deployment/local_integrated_roots.py`のみ変更（RED commit後、Testは未変更）。

`initialize_local_integrated_roots()`に、filesystemへの最初の副作用より前の
read-only再検査`_revalidate_initialization_targets()`を追加した。

1. 引数が`LocalIntegratedRoots`である（既存stop code `root_resolution_required`は不変）。
2. 保存された`runtime_root`と`runtime_layout.runtime_root`、`sensitive_root`と
   `runtime_layout.roots["sensitive"]`、`project_id`・profile（`runtime`固定）の内部整合。
3. install・projectが現在も絶対pathの実在directoryで、symlinkでなく、保存canonical
   identity（`resolve()`再計算）と一致する。
4. runtime root・sensitive rootの現在のcanonical pathが解決時identityと一致し、
   sensitiveがruntimeの内側、runtimeがinstall・projectとoverlapしない。
5. runtime rootからsensitive rootまでの各path componentについて、存在するものが
   symlinkでなくdirectoryである（通常file・symlink・identity差替え・root escapeを拒否）。

不合格は全て新しい安定stop code `runtime_initialization_target_invalid`の
`RootSeparationError`で、`initialize_project_runtime_layout()`を呼ばずに停止する。
再検査中の`OSError`・`RuntimeError`もpathを出さず同stop codeへ変換する。例外文は
stop codeのみでhost path・未検査内容を含めない。合格時は従来どおり
`initialize_project_runtime_layout(..., requested_kinds=["sensitive"])`を再利用し、
正常な未作成runtime rootの初期化契約（sensitiveと必要なruntime祖先だけを作成）は弱めていない。

## 5. 3種の差替えの実測（合成fixtureのみ）

| 差替え態様 | stop code | initializer呼出し | install／project | 作成artifact |
| --- | --- | --- | --- | --- |
| runtime root本体→installへのsymlink | `runtime_initialization_target_invalid` | なし（spy実測0回） | inventory・SHA-256・mode・mtime不変 | なし（`install/projects`・sensitive未作成） |
| runtime配下`projects`→installへのsymlink | 同上 | なし | 不変 | なし（`install/project-alpha`・sensitive未作成） |
| 解決時未作成の祖先→installへのsymlink | 同上 | なし | 不変 | なし（`install/.reviewcompass3`・sensitive未作成) |

いずれも例外連鎖の文言に`tmp_path`配下のpath・fixture markerが含まれないことを機械確認。
先行の通常初期化Test（正常な未作成runtimeの初期化・mode 0700実測・install／project不変）は
引き続き合格。

## 6. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| 修正RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py` | 3 failed（新規のみ・DID NOT RAISE）／28 passed | `1` |
| targeted GREEN | 同上command | 31 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py tests/test_layout_baseline.py tests/test_task_python_cache.py` | 46 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json` | 1313 passed、status `passed` | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |

公式receiptは再読込みし、status `passed`・exit `0`・1313件全合格・failed 0を機械確認済み。

## 7. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/deployment/local_integrated_roots.py` | `bc9bc19bede6e9052b4222b02131d7b2b81ebca54d8f7de7d5b10a0fe7819870` |
| `tests/test_work7a_local_integrated_root_separation.py` | `023f3dc7351a1934a74276e46aaa748677a68df66311173f03b9ae244e86e01a` |
| 公式receipt（同上JSON） | `1ad9bc09c9121a9809d1e06b2bc635f499890a2f476dc03c31b0260447e77a0f` |

## 8. 禁止境界と未実施範囲

- 先行commitのamend・rebase・reset・revert・履歴書換え：未実施。
- `tools/layout/baseline.py`・authority・`TODO_NEXT_SESSION.md`・checklist・Plan・Decision・
  Issue・Candidate・workflow台帳・先行Evidence／receipt：未変更。
- resolver・write target関門の公開contract、4 root構造、`runtime` profile、Manifest解決、
  初期化の正常範囲、既存stop codeの意味：不変。
- Layout v3初期化を複製した新directory builder・新schema・新依存・新root kind：作成なし。
- 実ホーム・既存data・外部system：access・送信なし。Testは`tmp_path`のみ。
- push・tag・PR・`git add -A`／`git add .`：未実施（stageは全て明示path指定）。
- **原子的filesystem protocol（初期化syscallと同時の別process競合の防止）は未実施**。
  本修正が検出するのは「解決後から初期化呼出し前に完了したfilesystem差替え」であり、
  同時競合の防止は後続とする（指示書§4.2どおり、完了Claimに含めない）。
- 先行指示書の後続Work（Project Binding耐久保存、stable／development分離ほか）：未実施。
