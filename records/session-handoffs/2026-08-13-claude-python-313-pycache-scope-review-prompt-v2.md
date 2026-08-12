# Claude向け Python 3.13一時cache補正・修正後確認指示 v2

あなたはReviewCompass3の独立修正後確認担当です。先行レビューが止めた1件について、作業票v3からv4への
変更点だけを確認してください。成果物は変更せず、読み取りと照合だけを行ってください。

## 対象

- 先行版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v3.md`
- 先行版SHA-256：`8a9b5d1a04428ebf906b060a397ac2934d4dd408d06bf608542aa818af9d821d`
- 対象版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v4.md`
- 対象版SHA-256：`e2b753d882803c1c1f655d32a6c0202e89108f7af6b2b307c11206e5f2e8fcfe`
- 先行レビュー：`records/development/2026-08-13-python-313-pycache-correction-start-review-v1.md`
- 先行レビューSHA-256：`966613b7aee69c23c912793bb8adccb522c6e7bb2c669c92fb74e98dea026cd6`

## 確認する一点

v3では、子pytestへproject外の一時`PYTHONPYCACHEPREFIX`を渡しても、公式runner自身が設定前にproject内へ
`.pyc`を作る欠陥が残りました。v4は公式runnerの起動commandだけを
`.venv/bin/python3 -B -m tools.development.policy_test_runner ...`へ変え、子pytest側の2 path案は維持します。

次だけを確認してください。

1. 起動側の`-B`がrunner自身のcache生成を止め、子pytest側の一時cache処理とは役割が重ならないか。
2. `config/development-test-runner.json`の子suite commandへ`-B`を入れないため、
   `tests/test_task_python_cache.py`のcache作成検査を無効化しないか。
3. 実装対象2 path、設定形式、結果記録形式、試験集合がv3から増えていないか。

先行レビューの使い捨て複製で行った`-B`対照結果を再利用してよいです。新しい仕組み、一般化、別案、
将来改善を提案しないでください。止める欠陥が残る場合だけ、今回の一点に対する最小修正を示してください。

## 禁止

- Homebrew取得、依存固定、`.venv`退避復旧、v3の2 path案全体を再レビューしない。
- fileの作成、変更、削除、stage、commit、外部送信、ネット検索、全試験、第2段完了をしない。
- `.gitignore`、Git検査、task cache、他の環境変数へ広げない。

## 出力

日本語で、`判定`（`開始可`または`修正要`）、`止める指摘`、`報告不一致`、確認した一点、未実施を
簡潔に示してください。これは変更点だけを見る一回限りの修正後確認です。
