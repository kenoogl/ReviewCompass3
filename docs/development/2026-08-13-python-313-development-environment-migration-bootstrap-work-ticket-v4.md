# Python 3.13開発環境移行 軽量作業票 v4

- 作業票ID：`BTW-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-001`
- 作成日：2026-08-13
- 状態：`awaiting_correction_review`
- 基準コミット：`8ad4687`
- 先行版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v3.md`
- 先行版SHA-256：`8a9b5d1a04428ebf906b060a397ac2934d4dd408d06bf608542aa818af9d821d`
- 先行レビュー：`records/development/2026-08-13-python-313-pycache-correction-start-review-v1.md`
- 先行レビューSHA-256：`966613b7aee69c23c912793bb8adccb522c6e7bb2c669c92fb74e98dea026cd6`
- 危険度：`high`（v3から不変）

## 1. この版の変更点

本版はv3の開始前レビューで見つかった止める指摘1件だけを修正する。v3の目的、実装対象2 path、試験先行、
一時cacheの範囲と寿命、対象外、停止条件、完了条件は維持する。

【実測】子pytestへ一時`PYTHONPYCACHEPREFIX`を渡す前に、公式runner自身と`pytest_summary.py`が読まれ、
project内へ2個の`.pyc`を作る反証が成立した。runner起動時にPythonの`-B`を付けた対照では残留0だった。
通常起動した作業単位完了確認でも同じ生成が再現し、`-B`付きの再確認では終了コード0、`passed`だった。

## 2. v3への一点補正

公式全試験の起動commandだけを次へ変更する。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage2-python313-migration-green-v3.json
```

`-B`は公式runnerを起動するPython processだけのbytecode cache作成を止める。runnerが起動した後の子pytestには
v3どおりproject外の一時`PYTHONPYCACHEPREFIX`を設定する。これにより、子pytest内で独自のcache出力を検査する
`tests/test_task_python_cache.py`を無効化しない。

## 3. 変えない範囲

- 実装変更は`tests/test_policy_test_runner.py`と`tools/development/policy_test_runner.py`の2 pathだけ。
- v2で変更済みの試験3件、設定2件、依存固定は変更しない。
- `config/development-test-runner.json`内の子suite commandへ`-B`を追加しない。
- 設定形式、結果記録形式、runner版、公式試験集合を変更しない。
- `.gitignore`、Git検査、task cache、合成worktree、他の環境変数へ広げない。
- `PYTHONDONTWRITEBYTECODE=1`を手で付けた失敗への一般対策を追加しない。

## 4. 修正後確認

修正後確認はv3から本版へ変えた次の一点だけを見る。

1. 公式runner起動側の`-B`と、子pytest側の一時`PYTHONPYCACHEPREFIX`の役割が分離されているか。
2. v3レビューの反証だったrunner自身のproject内cache生成を`-B`で止められるか。
3. 設定や実装対象を増やしていないか。

修正後確認が`開始可`の場合だけ、v3 §5のREDから実装へ進む。完了確認commandは上記の`-B`付き公式commandを
使う。Evidenceには、v3レビュー後の通常起動した作業単位確認が未追跡cacheを生成したこと、退避先、
`-B`付き再確認で成功したことも含める。
