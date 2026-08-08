# GREEN Evidence：Work 7A例外連鎖のhost path漏洩修正

- 指示書：`records/session-handoffs/2026-08-09-codex-to-claude-work7a-exception-chain-path-correction.md`
- 作成日：2026-08-09
- executor：Claude（Codex修正指示書に基づく委譲作業）

## 1. 先行mismatchと修正対象

Codexの再レビューで、runtime pathを自己参照symbolic link loopへ差し替えて
`initialize_local_integrated_roots()`を呼ぶと、表面は
`runtime_initialization_target_invalid`でfilesystem writeなしに停止するものの、
`RootSeparationError.__cause__`を辿るとhost path入りの`RuntimeError`
（`Path.resolve()`の「Symlink loop from '<path>'」）へ到達できることが反証された。
原因は再検査中の例外を`raise RootSeparationError(...) from error`で連結していたこと。
「例外連鎖にpathを含めない」という先行`completed_claim`は`report_execution_mismatch`。
本修正は例外変換のhandler外raise化1点だけで解消する。

## 2. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| correction implementation base | `6f1c41708c606099139ba71d3ad0d529b25c536c` | 先行symlink差替え修正GREEN（書き換えていない。先行のWork 7A RED／GREEN、symlink修正REDも同様） |
| 指示書配布 | `b68f7d1170c2c8500dbed1cb39c78a2cc75f6d52` | 修正指示書1fileのみ追加（193行。指示書§3で正常と規定） |
| 修正RED | `b77e044d9a51343e94adebe6e71fcb49380c3acd` | `tests/test_work7a_local_integrated_root_separation.py`のみ（93行追加、漏洩2態様のTest） |

開始時確認：branch `main`、worktree clean、固定入力9fileのSHA-256は指示書の表と全件一致。

## 3. 修正RED（Commit 1）

- command：`.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py`
- 結果：33件収集、新規2件（実symlink loop・合成marker入り強制`RuntimeError`）のみが
  「`__cause__`に原因例外（path・marker入り`RuntimeError`）が残る」という漏洩そのものを
  理由に失敗、先行31件は合格、exit code `1`。

## 4. 修正GREEN（Commit 2）の実装

`tools/deployment/local_integrated_roots.py`のみ変更（RED commit後、Testは未変更）。

`initialize_local_integrated_roots()`の例外変換を、handler内の
`raise RootSeparationError(...) from error`から、handler内では失敗flagを立てるだけにし、
**handler外**で`RootSeparationError("runtime_initialization_target_invalid")`をraiseする
最小実装へ変更した。これにより：

- `__cause__ is None`かつ`__context__ is None`。例外objectとして辿っても原因例外へ
  到達できない（表示抑制の`from None`ではなく、連鎖自体を作らない）。
- 表面文言は安定stop codeのみ。`traceback.format_exception()`の出力にも入力由来の
  host path・fixture marker・原因例外文言（「Symlink loop」等）が出ない。
- `RootSeparationError`（再検査自身の拒否）はそのまま再raiseし、既存stop code・
  再検査の成否条件・root分離・通常初期化・write target関門は不変。
- 例外変換中に`initialize_project_runtime_layout()`を呼ばず、filesystemを変更しない。

## 5. 2態様の実測（合成fixture・`monkeypatch`のみ）

| 態様 | stop code | `__cause__`／`__context__` | traceback | initializer呼出し | filesystem |
| --- | --- | --- | --- | --- | --- |
| runtime pathの自己参照symlink loop | `runtime_initialization_target_invalid` | ともに`None` | `tmp_path`・「Symlink loop」なし | 0回（spy実測） | install・project snapshot不変。runtime親directoryにはloop symlink 1個のみ、新規artifactなし |
| 再検査中の合成marker入り強制`RuntimeError`（`Path.resolve`を決定的に失敗させる） | 同上 | ともに`None` | marker・`tmp_path`なし | 0回 | install・project snapshot不変。runtimeとその親は未作成のまま |

state snapshotはroot自身を含む全entryのmode・mtime・種別・内容SHA-256。
先行31 Test（4種root解決、write target関門、3種のsymlink差替え拒否、通常初期化）は
引き続き合格し、成否条件を弱めていない。

## 6. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| 修正RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py` | 2 failed（新規のみ・`__cause__`漏洩）／31 passed | `1` |
| targeted GREEN | 同上command | 33 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py tests/test_layout_baseline.py tests/test_task_python_cache.py` | 46 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-exception-chain-path-correction-green-test-receipt-v1.json` | 1315 passed、status `passed` | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |

公式receiptは再読込みし、status `passed`・exit `0`・1315件全合格・failed 0を機械確認済み。

## 7. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/deployment/local_integrated_roots.py` | `31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149` |
| `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| 公式receipt（同上JSON） | `ead2d653cd78426063a2fe1639f6f541f66b7c27934a720d08337957084cc9a3` |

## 8. 禁止境界と未実施範囲

- 先行commitのamend・rebase・reset・revert・履歴書換え：未実施。
- `TODO_NEXT_SESSION.md`・checklist・Plan・Layout authority・Decision・Issue・Candidate・
  workflow台帳・先行Evidence／receipt：未変更。
- root resolver・write target関門・root配置・profile・Manifest解決・symlink再検査の
  成否条件：不変。`tools.layout.baseline._load_project_manifest`の使用も本修正の対象外のまま。
- 新しい例外schema・root kind・Layout／Manifest schema・外部依存：作成なし。
- 実ホーム・既存data・外部system：access・送信なし。Testは`tmp_path`と`monkeypatch`のみ。
- push・tag・PR・`git add -A`／`git add .`：未実施（stageは全て明示path指定）。
- **原子的filesystem protocol（初期化syscallと同時の別process競合の防止）は未実施**
  （指示書§4.2どおり後続とし、完了Claimに含めない）。
- 先行指示書の後続Work（Project Binding耐久保存、stable／development分離ほか）：未実施。
