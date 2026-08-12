# Python 3.13開発環境移行 軽量作業票 v5

> **後続訂正（2026-08-13）**
> 本作業票の一時キャッシュ隔離案は過剰と判断し、取り下げた。現在の判断と回復結果は
> `records/development/2026-08-13-python-313-pycache-overengineering-recovery-evidence-v1.md`を参照する。
> 以下は訂正前の経過を保存したもので、実装指示として使わない。

- 作業票ID：`BTW-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-001`
- 作成日：2026-08-13
- 状態：`awaiting_correction_review`
- 基準コミット：`a6fcd39f915635cda1da514319c70949894a58f3`
- 先行版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v4.md`
- 先行版SHA-256：`e2b753d882803c1c1f655d32a6c0202e89108f7af6b2b307c11206e5f2e8fcfe`
- 先行修正後レビュー：`records/development/2026-08-13-python-313-pycache-correction-review-v1.md`
- 先行レビューSHA-256：`3259ba3a49c17a13d68b76d7b6d0de1f476d95b70be8e0fa2e7afd873242fb23`
- 危険度：`high`（v4から不変）

## 1. この版の変更点

本版はv4実装中に成立した反証1件だけを補正する。v4の公式runner起動側の`-B`、子pytest用のproject外一時
`PYTHONPYCACHEPREFIX`、公式runnerとその試験の実装案、設定、結果記録、試験集合は変えない。

【実測】公式runnerと同じく認証用環境変数6名を除外し、project外の一時`PYTHONPYCACHEPREFIX`を与えて
関連137試験を実行すると、136件成功、1件失敗、終了コード1だった。失敗は
`tests/test_task_python_cache.py::test_environment_mapping_does_not_change_the_running_process`だけである。

【実測】この試験は、対象関数の呼出し前後で`os.environ`全体が一致することに加え、試験開始前から
`PYTHONPYCACHEPREFIX`が存在しないことを暗黙に仮定していた。変数を除外した直接確認では同fileの27試験が
すべて成功し、終了コード0だった。全参照箇所の検索では、同じ開始前提を持つ試験はこの1件だけだった。

## 2. 追加する第三の変更path

v4の2 pathへ、次の1 pathだけを追加する。

| path | 許可する変更 |
| --- | --- |
| `tests/test_task_python_cache.py` | 該当試験へ`monkeypatch`を受け取り、`before`取得前に`monkeypatch.delenv("PYTHONPYCACHEPREFIX", raising=False)`を1回行う |

既存の次の二つのassertionは削除も変更もしない。

```text
assert "PYTHONPYCACHEPREFIX" not in os.environ
assert dict(os.environ) == before
```

これにより試験は「開始時に変数がない」条件を自分で用意し、対象関数がその条件を変えないことを従来どおり
検査する。`monkeypatch`は試験終了時に元の親環境を復元する。製品codeの保証、task専用cacheの出力確認、
公式runnerが親processの環境を変えない検査は弱めない。

## 3. 変えない範囲

- `tools/development/task_python_cache.py`は変更しない。
- 既存assertionを削除、緩和、skip、xfailしない。
- 共通fixture、自動環境正規化、他の環境変数へ広げない。
- v4の実装対象2 path、公式command、設定、結果記録、試験集合を変えない。
- `.gitignore`、Git差分検査、合成worktree、外部実装経路、第2段完了へ広げない。

## 4. 変更点限定レビュー

修正後確認はv4から本版へ増やした第三の試験pathだけを見る。

1. 試験自身が開始前提を用意するだけで、対象関数の環境不変保証を弱めないか。
2. `monkeypatch`による一時除外と自動復元で、公式runnerの一時cache環境と両立するか。
3. 同じ前提を持つ他の参照を見落としていないか。
4. 実装や設定へ新しい変更を要求していないか。

一般化、別案、将来改善は提案しない。今回の一点で関連137試験の残る1失敗を正しく解消できない場合だけ、
止める指摘を出す。

## 5. 実施と完了確認

修正後確認が`開始可`の場合だけ、第三の試験pathへ§2の変更を行う。既に固定済みのRED commit
`a6fcd39f915635cda1da514319c70949894a58f3`にある`tests/test_policy_test_runner.py`は変更しない。

その後、v4の実装と合わせ、次をそれぞれ単独実行する。

1. 公式runner試験11件。
2. 公式runnerが作る子環境と同じ条件で、v4記載の関連6 file、137件。
3. 独立収集。
4. v4記載の`-B`付き公式runnerによる全試験と結果記録。
5. `git diff --check`、許可3 path、RED試験不変、一時cacheの終了後不存在。

全試験成功後、v2からv5までの失敗・手戻り・復旧・一時退避先をEvidence一件へ記録する。GREEN実装commit、
Evidence commit、新規実行単位による独立完了レビューの順を維持する。第2段完了は別の利用者判断とする。
