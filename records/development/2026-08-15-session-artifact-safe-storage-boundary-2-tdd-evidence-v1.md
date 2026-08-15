# Session記録安全保存 境界2 事前拒否TDD Evidence v1

- 実施日：2026-08-15
- 対象境界：累積実装作業票v2＋v3の境界2「安全な事前拒否」
- 開始基準commit：`c90daa1`
- 実施担当：主担当Codex

## 1. 目的

【判断】保存条件を満たさない入力または保存場所では一byteも作らず固定理由で停止し、適合する合成入力でも
書込み準備の値だけを返す。記録directory、operation、本文、一時file、確定印は作らない。

## 2. RED

【実測】`tests/test_session_artifact_safe_storage.py`を新設し、次の21例を固定した。

- 必須三rootの各欠落3例、五pathの各非絶対5例
- repository内、同一root、包含rootの分離違反3例
- 保存rootの広いmode、所有者不一致、追加ACL、symlink各1例
- 正式入口の停止、部分、外部送信許可、絶対path残存4例
- raw内容識別値不一致1例、適合入力1例

全例は二保存rootの実在するentryとbytesの前後snapshotを比較し、変更0を要求する。

【実測】次を実装前に単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py
```

- 終了コード：1
- 結果：21 failed
- 全例の主要な失敗理由：`ModuleNotFoundError: No module named 'tools.session_logs.safe_storage'`

【判断】一件専用の事前検査module不在という一つの理由で全例が失敗し、境界2のREDとして正しい。

## 3. RED fixtureの限定訂正

【実測】実装前の再読で、要求と期待結果を変えない二つのfixture欠陥を見つけた。

1. 所有者不一致のlambdaが、差替え後の共有`os.geteuid`を再び呼んで再帰する形だった。差替え前UIDを値で固定した。
2. 必須root欠落時のsnapshot helperが、欠落値`None`自体を読もうとした。実在する保存rootだけを前後比較する形にした。

【実測】訂正後に同じ単独commandを再実行し、終了コード1、21 failed、全例が同じmodule不在で失敗することを確認した。

【判断】対象操作は合成反証fixture、期待executorと実executorはともにpytestである。手作業理由はfixtureのPython評価順を
意味確認したためで、製品仕様、期待結果、対象数は変えていない。同型の機械処理追加は不要と判断し本Evidenceへrouteする。

## 4. 最小GREEN

【実測】`tools/session_logs/safe_storage.py`を追加し、`preflight_store`と固定理由だけを持つ`StorageStop`を実装した。

- 明示絶対path、repository境界、二保存root分離を値から検査する
- rootの各componentをdirectory file descriptorから`O_NOFOLLOW`で開き、open後に種類を確認する
- 保存rootの実効利用者所有、mode 0700、Darwin拡張ACLなしをfile descriptorから確認する
- 正式入口結果が`status: ok`、`external_send_approved: false`で絶対pathなしであることを確認する
- rawをrootから相対的・symlink非追跡で開き、通常fileを再読込みして`source_sha256`と照合する
- 成功時は`status: ready`と`external_send_approved: false`だけを返す

【実測】file作成、directory作成、名前変更、同期、上書き、削除、探索、環境値解決、network、外部process、Git操作を
実装していない。repository確認は明示root直下の`.git`種別をfile descriptorから読むだけで、Git processを呼ばない。

## 5. GREENと回帰確認

【実測】対象試験を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py
```

- 終了コード：0
- 結果：21 passed

【実測】境界1と正式入口の関連試験を含めて単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py tests/test_session_log_read_only_entry.py tests/test_session_log_pipeline.py tests/test_session_log_provenance.py
```

- 終了コード：0
- 結果：42 passed

【実測】`git diff --check`は終了コード0だった。変更後SHA-256は次のとおり。

- `tools/session_logs/safe_storage.py`：`acf9c51bc1893590c9d3654a4221985afb59698a7ef98efd85b780c70b25fca2`
- `tests/test_session_artifact_safe_storage.py`：`f6eba3ce8e0108323f433fdb8aeb02d3f9e7f52ef67a69ae6b7ad64103ae60f2`

## 6. 判断

【判断】境界2は、要求を変えないfixture訂正後のREDを維持し、事前検査だけの最小GREENになった。不適合と正常の
全21例で保存root変更0、関連42件成功であり、境界3へ進む前に本単位をcommitする。

## 7. 未実施

【未実施】記録directoryと固定fileの作成、保存、同期、確定印、同一入力、競合、復旧、再読込み、保持期限、
削除計画、削除、製品入口、正規全試験、故障注入、独立完了レビュー、製品受入判断は実施していない。
外部送信、push、履歴書換えも行っていない。
