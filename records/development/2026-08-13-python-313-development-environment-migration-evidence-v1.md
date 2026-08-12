# Python 3.13開発環境移行 Evidence v1

> **後続訂正（2026-08-13）**
> Python 3.13移行の事実は維持するが、本記録の一時キャッシュ隔離案と`verified`候補は取り下げた。
> 現在の判断と回復結果は
> `records/development/2026-08-13-python-313-pycache-overengineering-recovery-evidence-v1.md`を参照する。
> 以下のキャッシュ関連部分は、訂正前の経過として保存する。

- 日付：2026-08-13
- 作業票ID：`BTW-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-001`
- 最終作業票：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v5.md`
- 最終作業票SHA-256：`38284c7272398acebc2de8ff77b9dedbf88eb69eb56a0dc19f90d7dbb648ddd5`
- 最終GREEN commit：`caa14f4d689f364c5f6672cf701c57d02f6b1216`
- 判定候補：`verified`

## 1. 結果

【実測】正式`.venv`はPython 3.13.14、pytest 8.4.2へ移行した。3.13用依存固定10件は実環境と完全一致し、
対象138試験、独立収集、公式全試験はいずれも終了コード0だった。最終公式結果は1,738件成功、失敗・error・
skip・xfail・xpass 0、fallbackなしである。実行後にproject内と公式runner用一時領域へbytecode cacheは残らず、
作業ツリーはcleanだった。

【判断】Python 3.13開発環境移行と、その過程で表面化した公式試験のcache出力先補正は、独立完了レビューへ
渡せる状態である。この記録は第2段完了の判断ではない。

## 2. 固定材料と試験先行

| 意味単位 | commit | 実測 |
| --- | --- | --- |
| 当初の3.13要求RED | `520b6c8f9c8b0364719f12179188073b5dba59d3` | 対象34件中16 failed / 18 passed、終了コード1。3.9設定、`python3.13`、新しい依存固定の未反映だけを検出 |
| 設定と依存固定GREEN | `f969dbd6cfe8d2516d9ce7982b81efe318586a59` | 設定2件と`constraints/development-py313.txt`だけを変更。REDの試験3件は不変 |
| 全試験本体の一時cache RED | `a6fcd39f915635cda1da514319c70949894a58f3` | 11件中、新しい1件だけ失敗、終了コード1 |
| 全試験本体の一時cache GREEN | `a3e86fa9a4a04b7faa7c6c66deba378d7a99a0c2` | 公式runnerとtask cache試験の2 pathを変更。RED試験は不変 |
| 事前確認の一時cache RED | `9dfe5ad08bc98329faefdff7d3e545a032c18a64` | 12件中、新しい1件だけ失敗、終了コード1 |
| 事前確認の一時cache GREEN | `caa14f4d689f364c5f6672cf701c57d02f6b1216` | 公式runner 1 pathだけを変更。RED試験は不変 |

【実測】各REDから対応GREENまでの試験file不変を`git diff --exit-code`で確認し、すべて終了コード0だった。
最終的な実装関係pathは次の8件である。

- `tests/test_development_environment.py`
- `tests/test_policy_test_runner.py`
- `tests/test_policy_test_runner_summary.py`
- `tests/test_task_python_cache.py`
- `config/development-environment.json`
- `config/development-test-runner.json`
- `constraints/development-py313.txt`
- `tools/development/policy_test_runner.py`

当初作業票の7 pathに、cache補正で承認された公式runner、同試験内の追加RED、task cache試験の3 pathを
加えた集合である。製品code、`tools/development/task_python_cache.py`、公開Python対応範囲は変更していない。

## 3. Python 3.13取得と隔離確認

【実測】同じ次の4変数を使い、Homebrewの依存木、dry-run、TTYの`install --ask`を順に確認した。

- `HOMEBREW_NO_AUTO_UPDATE=1`
- `HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK=1`
- `HOMEBREW_NO_INSTALL_CLEANUP=1`
- `HOMEBREW_NO_INSTALL_UPGRADE=1`

【実測】依存閉包は`python@3.13`、`mpdecimal`、`openssl@3`、`sqlite`、`xz`、`ca-certificates`、`readline`だった。
dry-runとTTY計画の対象集合は一致し、閉包外の対象はなかった。本実行は確認入力後に終了コード0となった。
導入後の読み取り確認は次を示し、終了コード0だった。

| package | version |
| --- | --- |
| `python@3.13` | `3.13.14_1` |
| `mpdecimal` | `4.0.1` |
| `openssl@3` | `3.6.3` |
| `sqlite` | `3.53.4` |
| `xz` | `5.8.3` |
| `readline` | `8.3.3` |
| `ca-certificates` | 現行`2026-07-16`。先行cellar `2026-05-14`も保持 |

【実測】`/private/tmp/reviewcompass-python313-isolated.aUH363/venv`へ隔離環境を作り、現在の3.9用固定を制約に
toolchainと`.[development]`を導入した。project import、pytest、platformdirs、PyYAML、宣言済みconsole script
7件を確認し、対象34試験は34 passed、終了コード0だった。

【実測】隔離環境の実導入結果から作った`constraints/development-py313.txt`は10行、名前順、完全固定、重複0で、
SHA-256は`f8d4343c239413d073270441c6882208a60184807b75e0bbc0caa0652bb97db4`である。最終`.venv`の
`pip list --format=freeze --exclude reviewcompass3`と機械比較し、10件対10件の完全一致、終了コード0だった。
旧`constraints/development-py39.txt`は不変で、SHA-256は
`1307ed9075ddcc312697d18114b8f5b594796f047ab5df586e7a7b448058c8f2`である。

## 4. 正式`.venv`切替えと復旧確認

【実測】旧`.venv`を`/private/tmp/reviewcompass-python39-backup.GxRJLy/.venv`へ移し、Python 3.9.6が起動する
ことを確認した。最初の正規bootstrapは`project_scripts_mismatch`で終了コード1だった。不完全な3.13環境を
`/private/tmp/reviewcompass-python313-incomplete.LpEPvs/.venv`へ退避し、3.9 backupを正式`.venv`へ戻して
Python 3.9.6の起動を再確認した。

【実測】原因はrepository内に残っていた無視対象`reviewcompass3.egg-info`だった。2026-08-04時点の古い生成情報は
現行7件のうち2件のconsole scriptだけを持ち、隔離環境と最初の正式環境で再利用されていた。これを削除せず
`/private/tmp/reviewcompass-python313-generated-backup.X9d52C/reviewcompass3.egg-info`へ退避し、不完全3.13環境へ
再導入すると7件すべてが一致した。

【実測】その後、旧3.9環境を同じbackupへ再退避し、正規bootstrapを再実行した。終了コード0、
`status=created`、Python 3.13.14、pytest 8.4.2だった。現在の正式`.venv`はPython 3.13.14で、旧3.9 backupは
削除せず保持している。

## 5. 公式全試験で判明した問題と解消

| 順 | command条件と結果記録 | 結果 | 判断 |
| --- | --- | --- | --- |
| 1 | 手作業で`PYTHONDONTWRITEBYTECODE=1`を追加。結果記録v1 | 1 failed / 1,735 passed、終了1 | cache作成を検査する既存試験を手作業条件が無効化した。合否根拠に不使用 |
| 2 | 余計な条件を外した正規command。結果記録v2 | 6 failed / 1,730 passed、終了1 | Homebrew 3.13はApple 3.9と異なり既定cache出力先がなく、合成Git worktreeへ`__pycache__`を作った |
| 3 | 全試験本体だけ一時cacheへ移した結果記録v3 | 1,737 passed、終了0 | 事前の`pytest --version`がproject内へ2 `.pyc`を残したため最終根拠に不使用 |
| 4 | 事前確認2回と全試験本体を一時cacheへ移した結果記録v4 | 1,738 passed、終了0 | 最終根拠。実行後残留0 |

結果記録のSHA-256は順に次のとおりである。

- v1：`f537dae22206f325967324388fda62a72dba4c4cc249ae080763f04b91d7ef36`
- v2：`eeb4ed725095b7c569b9fc222c14ef5f23ae2579193ee3a8a11e9a1cc0c4fd42`
- v3：`242934de66bab1bbf13d7a8c42afa2a54c81b25068c88c77aa8fa10739534bad`
- v4：`ba2e3a2043397fc44bcc7ed00abd1b0773bf869c42034bbfd090607c8fdabe45`

【実測】公式runner自身は`.venv/bin/python3 -B -m tools.development.policy_test_runner`で起動し、runnerの
module読込み時cacheを止める。runnerは事前確認2回と全試験本体へ、それぞれproject外の一時
`PYTHONPYCACHEPREFIX`を渡す。一時directoryは各子process実行中に存在し、終了後に消える。親processの環境は
変更しない。子pytestのcommand自体には`-B`を加えず、task cacheの実出力検査を維持する。

## 6. 最終機械確認

| 確認 | 結果 | 終了コード |
| --- | --- | --- |
| 公式runner単体 | 12 passed | 0 |
| 公式環境を再現した関連6 file | 138 passed | 0 |
| 独立収集 | 1,738 collected | 0 |
| 公式全試験 | 1,738 passed、failed/error/skip 0 | 0 |
| 結果記録のPython | 3.13.14 | 0 |
| 結果記録のpytest | 8.4.2 | 0 |
| fallback | false | 0 |
| `source_state_digest`独立再計算 | `2ebe29435834bd31d503189d389a0fa5fd517ed248202e0b4a4fe79c7bcb7096`で一致 | 0 |
| 依存固定と正式`.venv` | 10件対10件で完全一致 | 0 |
| project内`__pycache__` | 0 directory | 0 |
| 残留公式一時cache | 0 directory | 0 |
| `git diff --check` | 問題0 | 0 |

【実測】移行前は1,736件だった。公式runnerの全試験本体用cache試験と事前確認用cache試験を各1件追加したため、
最終件数は1,738件である。既存試験の削除、skip、xfail、選択除外は行っていない。

## 7. 手戻りと機械処理候補

| 事象 | 対象操作 | 期待executor / 実executor | 手作業理由とEvidence | 機械処理候補とroute |
| --- | --- | --- | --- | --- |
| 古い生成情報でbootstrap失敗 | 正式`.venv`構築 | 正規bootstrap / 正規bootstrap | 無視対象生成物の鮮度を事前確認していなかった。2 script対7 script | bootstrap前の古いinstall metadata警告。今回は実装せず将来の改善候補 |
| 公式結果v1の1失敗 | 公式全試験 | 正規runner / 手作業条件付きrunner | project汚染回避のため未定義の`PYTHONDONTWRITEBYTECODE`を追加 | 作業票固定commandをそのまま使う。今回のEvidenceでrouteを解消 |
| 関連試験の15失敗 | 関連回帰 | 公式相当環境 / 直接pytest | 部分確認を早く行うため認証6名除外とcache先を省略 | 公式環境条件を明示した再実行で解消。共通runner新設はしない |
| 関連試験の1失敗 | task cache環境不変試験 | 公式相当環境 / 公式相当環境 | 試験が変数不存在を暗黙前提としていた | 試験自身が開始前提を用意し、既存assertionを維持。実装済み |
| 退避commandの同名衝突 | 15 cache directory退避 | 一意退避 / basename共通退避 | 複数`__pycache__`を同一名で一括移動した | 一意名で14件を再実行し解消。削除・喪失なし |
| v3後の2 `.pyc`残留 | 公式全試験 | 全子process隔離 / 全試験本体だけ隔離 | Python起動回数を3回でなく本体1回だけとして調査した | 3回すべての環境を検査する受入試験を追加し解消 |
| レビュー後のclean報告不一致 | 作業単位確認 | 読み取りのみ / 通常Python起動 | 確認役自身がcacheを生成 | 担当が検出・退避後、`-B`付き確認で解消。報告不一致は隠さず本記録へ固定 |

【判断】一律に新しい管理機構を増やさず、実害が出た境界だけを受入試験へ変換した。bootstrapの古い生成情報警告
だけは今回の許可範囲外なので候補に留め、現作業へ連鎖させていない。

## 8. 保持している復旧材料

【実測】次の一時材料は独立完了レビューが終わるまで削除しない。

- 旧3.9正式環境：`/private/tmp/reviewcompass-python39-backup.GxRJLy/.venv`
- 隔離3.13環境：`/private/tmp/reviewcompass-python313-isolated.aUH363/venv`
- 最初の不完全3.13環境：`/private/tmp/reviewcompass-python313-incomplete.LpEPvs/.venv`
- 古いegg-info等：`/private/tmp/reviewcompass-python313-generated-backup.X9d52C`
- 初回生成cache退避：`/private/tmp/reviewcompass-python313-generated-pycache-backup.p72p4r`
- レビュー時cache退避：`/private/tmp/reviewcompass-pycache-review-transition.Brdq9W`
- v3後cache退避：`/private/tmp/reviewcompass-python313-post-official-pycache-backup.NpO8N3`

## 9. 対象外と未実施

【未実施】`pyproject.toml`と`setup.py`の公開Python対応範囲、製品code、旧依存固定の変更・削除、依存版の更新、
試験のskip・xfail・選択除外、Git検査、`OUT-PC-006`、重大な欠陥12件、第3段、第2段完了は実施していない。
外部実装経路は`使用停止`のままで、既知の静的Git検査を保証根拠に使っていない。Claude用指示文は作成したが、
外部送信は行っていない。push、tag、amend、rebase、reset、force push、履歴書換えも行っていない。
