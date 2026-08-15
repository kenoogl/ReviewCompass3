# Session記録安全保存 最終検証Evidence v3

- 実施日：2026-08-15
- v1：独立完了レビューv1の四指摘によりstale
- v2：独立完了再レビューv2の二指摘によりstale
- 修正commit：`3141179`、`96cf393`

## 残る二原因のRED・GREEN

【実測】確定印公開直前の中止は、両rootのoperationが`committed`へ置換済みで`commit.json`だけ未公開の
合成停止を先に作った。`plan-delete`が`record_conflict`で1 failedとなった。記録表示stateは`incomplete`のまま、
共通operation validatorだけが`incomplete/committed`双方を許す最小修正により、計画と確認済み削除は1 passedとなった。

【実測】保存再開中の再中断は、製品入口から初回raw公開後停止、同じ入力の再開中に派生物公開後停止、再々開を
順に行う1試験を先に作った。二度目だけ`stopped/4`へ退行して1 failedとなった。既存内容とoperationの完全照合が
全て終わり、再開書込みを開始した後の`StorageStop`だけを固定`incomplete`結果へ変換した。同じ試験は、初回と
二度目がともに`incomplete/3`・同じrecord ID・例外詳細なし、三度目が`stored/0`となり1 passedだった。
既存不一致、属性不適合、事前拒否は`stopped/4`のままである。

## 再検証

【実測】修正後の単独command結果は次のとおりである。

- `.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py tests/test_session_artifact_safe_storage_entry.py`
  — 97 passed、終了コード0。
- `.venv/bin/python3 -m pytest -q tests/test_session_log_read_only_entry.py tests/test_session_log_pipeline.py tests/test_session_log_provenance.py tests/test_development_environment.py`
  — 30 passed、終了コード0。
- `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt /private/tmp/reviewcompass-safe-storage-full-receipt-20260815-v4.json`
  — 1,862 passed、failed 0、error 0、skip 0、終了コード0。
- `git diff --check` — 終了コード0。

- 保存核SHA-256：`78e67aad09784ffe93b81d1b25971d6766b91384961c0f64d52bad1737e12ab1`
- 製品入口SHA-256：`a67a36927ab751616437c2cf5d5abd50436026490fdc2a3e08c93abf53ee66ce`
- 保存核試験SHA-256：`d6d5db15e591c3017c80fd5ed131095608224eeb19e8aa9d5f636c8a88653c78`
- 製品入口試験SHA-256：`e7c8cc8295acdaff7ac58108a010b420d84ee6c4a26bfb51f5eb571cefcc2012`
- 全試験receipt SHA-256：`e1005f53740a3d2f1f5176a322b70a14874a63df5748cf7df5ab972dea7e3ca9`

【判断】独立完了再レビューv2の二原因は既存契約・既存試験期待を変えずREDからGREENになった。条件1から21を
独立再々レビューへ提示できる状態である。止める指摘0件になるまで条件22の利用者受入へは進まない。

【未実施】実Session、実保存root、push、外部送信、自動削除、複数記録探索は使用・実行していない。
