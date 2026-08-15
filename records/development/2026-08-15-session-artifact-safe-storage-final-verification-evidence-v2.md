# Session記録安全保存 最終検証Evidence v2

- 実施日：2026-08-15
- v1：独立完了レビューv1の四指摘によりstale
- 修正要レビュー：`records/development/2026-08-15-session-artifact-safe-storage-independent-completion-review-v1.md`
- 修正commit：`e1c6904`、`c3f9592`、`bf3facc`、`46d12ac`

## 四原因のRED・GREEN

【実測】operation完全照合は、両rootで同じ正準JSONへ意味改変した5反例を先に追加した。record ID、固定file集合、
一時file対応、期待SHAの改変が例外を出さず成功する一理由で5 failedとなった。完全な共通validatorと存在本文Digest
照合を`load-derived`、`plan-delete`、`delete`へ接続し、同じ5件は5 passedとなった。

【実測】片root中断は、sensitive側の有効`operation.json`作成後、data側record directory作成前に停止する2反例を
先に追加した。保存再試行は`record_busy`、確認済み削除は`record_unrecoverable`で2 failedとなった。残存operationと
全実在bytesを先に照合し、欠けた側を所有者限定0700で作成して同じ操作情報を置く処理により、保存再開と中止は2 passedとなった。

【実測】監査印公開後再試行は、`deleted.json`作成後・operation除去前に停止し、同じ確認値と1秒後の`deleted_at`で
再試行する1反例を先に追加した。監査印再生成による`record_conflict`で1 failedとなった。有効な既存監査印のrecord ID、
保持期限、削除済みDigestを照合して既存bytesを正本とする処理により、同じ1件は1 passedとなった。

【実測】途中製品出力は、raw公開後の保存停止とraw削除後の削除停止を製品入口から起こす2反例を先に追加した。
両方が終了コード4の`stopped`となり2 failedだった。有効operationが残る場合だけ、秘密を含まないrecord IDと
operation SHAを持つ`incomplete`または`deletion_incomplete`を終了コード3で返す処理により、同じ2件は2 passedとなった。
削除確認値、例外本文、raw本文、pathは出力していない。事前拒否は終了コード4の`stopped`のままである。

## 再検証

【実測】修正後の単独command結果は次のとおりである。

- `.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py tests/test_session_artifact_safe_storage_entry.py`
  — 95 passed、終了コード0。
- `.venv/bin/python3 -m pytest -q tests/test_session_log_read_only_entry.py tests/test_session_log_pipeline.py tests/test_session_log_provenance.py tests/test_development_environment.py`
  — 30 passed、終了コード0。
- `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt /private/tmp/reviewcompass-safe-storage-full-receipt-20260815-v3.json`
  — 1,860 passed、failed 0、error 0、skip 0、終了コード0。
- `git diff --check` — 終了コード0。

- 保存核SHA-256：`41375bc486e6a237eb14721b005ceea4961b349de58a32c3dfc6c9d00a3a06e5`
- 製品入口SHA-256：`a67a36927ab751616437c2cf5d5abd50436026490fdc2a3e08c93abf53ee66ce`
- 保存核試験SHA-256：`2e9a21970df1f72d81c1519cc7f0b7756390ceba9b088c8979df8e882dd8a562`
- 製品入口試験SHA-256：`50753f4043dd3a1a971ca9c418d2cb535564f91ed5a04e3a57725c5ffdf9afb6`
- 全試験receipt SHA-256：`cc82a647c96b75ce417f06359710a6cc04e087fdc78f0ddddd05684e99343f06`

【判断】独立完了レビューv1の四原因は、既存契約・既存試験期待を変えずREDからGREENになった。条件1から21を
独立再レビューへ再提示できる状態である。再レビューが止める指摘0件になるまで、条件22の利用者受入へは進まない。

【未実施】実Session、実保存root、push、外部送信、自動削除、複数記録探索は使用・実行していない。
