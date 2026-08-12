# Python 3.13 cache試験前提 修正後レビュー v1

- 日付：2026-08-13
- 対象：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v5.md`
- 対象SHA-256：`38284c7272398acebc2de8ff77b9dedbf88eb69eb56a0dc19f90d7dbb648ddd5`
- 対象commit：`cde510b`
- 先行版SHA-256：`e2b753d882803c1c1f655d32a6c0202e89108f7af6b2b307c11206e5f2e8fcfe`
- 確認対象：`tests/test_task_python_cache.py::test_environment_mapping_does_not_change_the_running_process`の前提条件だけ
- 判定：`開始可`

## 1. 許可変更の照合

【実測】v4とv5を再読込し、SHA-256を機械照合した。申告値と一致した。v5が許可する変更は、対象試験へ
`monkeypatch`引数を加え、`before`取得前に次を1回行うことだけである。

```text
monkeypatch.delenv("PYTHONPYCACHEPREFIX", raising=False)
```

【実測】次の既存の二つの確認は削除も変更もしないと明記されている。

```text
assert "PYTHONPYCACHEPREFIX" not in os.environ
assert dict(os.environ) == before
```

## 2. 環境不変保証

【判断】`before`より先に変数を一時除外するため、この試験は「対象関数の呼出し前後で環境全体が同一か」を
従来どおり検査する。対象関数が変数を追加・削除・変更する、または他の環境値を変える場合は、既存の確認で
失敗する。したがって、対象関数が親processの環境を変えないという保証は弱まらない。

【実測】現行pytest 8.4.2の`monkeypatch.delenv()`は、変数が存在する場合は削除前の値を復元用一覧へ保存する。
fixtureは試験終了時に`undo()`を呼び、保存した親値を`os.environ`へ戻す。変数が最初から無い場合は、
`raising=False`により何も変更せず、終了後も無い状態を保つ。

## 3. 全参照検索

【実測】repository全体で`PYTHONPYCACHEPREFIX`、対象試験名、`bytecode_environment()`の参照を検索した。
同じ「試験開始時から変数が無い」という前提を持つ試験は対象の1件だけだった。

- 同fileの別試験は、返されたmappingの内容、または子processの出力先を検査する。
- `tests/test_policy_test_runner.py`は親値を明示設定し、runner実行後にその値が残ることを検査する。
- `tests/test_python_ast_boundary_check.py`の出現は検査用source文字列である。
- 製品側の参照はmapping生成と、保持中のrunner差分にある子process環境への設定である。

【判断】今回と同じ前提条件を整える必要がある別の試験はない。

## 4. 判定

`開始可`。止める指摘は0件、報告不一致は0件である。v5が許可した一変更だけを対象試験へ実施できる。

## 5. 未実施

`tools/development/task_python_cache.py`、保持中の`tools/development/policy_test_runner.py`差分、公式runnerの
一時cache方式、`-B`、設定、結果記録、他の試験は変更も再レビューもしていない。試験実行、全試験、実装、
外部送信、Claude送信、第2段完了、第3段は実施していない。一般化、別案、将来改善は追加していない。
