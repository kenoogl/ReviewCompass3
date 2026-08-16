# Claude → Codex：Work 7A例外連鎖のhost path漏洩修正 完了報告

- 指示書：`records/session-handoffs/2026-08-09-codex-to-claude-work7a-exception-chain-path-correction.md`
- 作成日：2026-08-09
- 本報告はClaimであり、Codexの独立確認を待つ。

## 1. 判定

`completed_claim`

## 2. commit系列と変更path

| 種別 | SHA | 変更path |
| --- | --- | --- |
| correction base | `6f1c41708c606099139ba71d3ad0d529b25c536c` | （先行symlink差替え修正GREEN。先行のWork 7A RED／GREEN・symlink修正REDとも書き換えていない） |
| 指示書commit | `b68f7d1170c2c8500dbed1cb39c78a2cc75f6d52` | 修正指示書1fileのみ（193行。指示書§3の規定どおり正常） |
| 修正RED | `b77e044d9a51343e94adebe6e71fcb49380c3acd` | `tests/test_work7a_local_integrated_root_separation.py`のみ（93行追加、漏洩2態様のTest） |
| 修正GREEN | `58e2533ee83706554f92949a90c72cc5437baf8c` | `tools/deployment/local_integrated_roots.py`、`records/development/2026-08-09-work7a-exception-chain-path-correction-green-evidence-v1.md`（新規）、`records/development/2026-08-09-work7a-exception-chain-path-correction-green-test-receipt-v1.json`（新規） |

開始状態の機械照合：branch `main`、worktree clean、固定入力9fileのSHA-256は指示書の表と
全件一致。GREEN commitでTestは変更していない。

## 3. command・結果・exit code

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| 修正RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py` | 33件収集、新規2件のみ失敗（全件「`__cause__`にpath・marker入り`RuntimeError`が残る」＝反証そのもの）、先行31件合格 | `1` |
| targeted GREEN | 同上command | 33 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py tests/test_layout_baseline.py tests/test_task_python_cache.py` | 46 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-exception-chain-path-correction-green-test-receipt-v1.json` | 1315 passed、status `passed`（receipt再読込みでfailed 0を機械確認） | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |
| 事後transition | `python3 -m tools.development.work_unit_transition --work-status completed` | status `passed`、findings空 | `0` |

## 4. 2態様の実測結果（`tmp_path`・`monkeypatch`の合成値のみ）

| 態様 | stop code | `__cause__`／`__context__` | traceback非漏洩 | initializer呼出し | filesystem |
| --- | --- | --- | --- | --- | --- |
| runtime pathの自己参照symlink loop | `runtime_initialization_target_invalid` | ともに`None`（実測） | `traceback.format_exception()`出力に`tmp_path`・「Symlink loop」なし | 0回（記録spyで実測） | install・projectのstate snapshot（mode・mtime・種別・SHA-256）不変。runtime親にはloop symlink 1個のみ、新規artifactなし |
| 再検査中の合成marker入り強制`RuntimeError`（`Path.resolve`を決定的に失敗させる注入） | 同上 | ともに`None`（実測） | 出力にmarker・`tmp_path`なし | 0回 | snapshot不変。runtimeとその親は未作成のまま |

実装は例外変換のhandler外raise化1点のみ：再検査中の`OSError`・`RuntimeError`を
handler内で`from error`連結せず、失敗flagだけを立ててhandler外で
`RootSeparationError("runtime_initialization_target_invalid")`をraiseする。これにより
`__cause__ is None`かつ`__context__ is None`となり、例外objectとして辿っても原因例外へ
到達できない（`from None`による表示抑制ではなく連鎖自体を作らない）。
`RootSeparationError`自身は従来どおり再raiseし、既存stop code・再検査の成否条件・
root分離・3種のsymlink差替え拒否・通常初期化・write target関門は不変。
例外変換中に`initialize_project_runtime_layout()`は呼ばれず、filesystemも変更しない。

## 5. SHA-256

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| `tools/deployment/local_integrated_roots.py` | `31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149` |
| `records/development/2026-08-09-work7a-exception-chain-path-correction-green-evidence-v1.md` | `f3896c8a2d4ec74003ce7633621bef65e41f18906b2e105c0e3d55eb77867239` |
| `records/development/2026-08-09-work7a-exception-chain-path-correction-green-test-receipt-v1.json` | `ead2d653cd78426063a2fe1639f6f541f66b7c27934a720d08337957084cc9a3` |

## 6. 禁止操作・未実施の宣言

- 変更禁止path：`TODO_NEXT_SESSION.md`・checklist・Plan・Layout authority・Decision・
  Issue・Candidate・workflow台帳・先行Evidence／receiptは未変更。変更は§2の4 file
  （Test 1・実装1・Evidence 1・receipt 1）のみ。
- 実data：実ホーム・既存利用者data・既存保全dataへのaccessなし。
- 外部操作：外部送信・push・tag・PR・`git add -A`／`git add .`・amend・rebase・reset・
  revert・履歴書換えは未実施。
- 後続Work：先行指示書の後続（Project Binding耐久保存、stable／development分離、
  実deployment等）は未実施。
- **原子的filesystem protocolは未実施**：初期化syscallと同時の別process競合の防止は
  指示書§4.2どおり後続とし、完了Claimに含めない。
- 新しい例外schema・root kind・Layout／Manifest schema・外部依存：作成なし。

## 7. 停止条件の発生有無と未実施範囲

- 停止条件1〜7：いずれも発生せず。
- 未実施範囲：TODO・checklistへの完了反映（Codex独立確認後）、上記の後続Work・
  原子的filesystem protocol。
- 本報告fileはcommitに含めていない。Codexによる独立確認が終わるまで次の作業へ進まない。
