# Session記録安全保存 境界4 再保存・競合TDD Evidence v1

- 実施日：2026-08-15
- 対象境界：累積実装作業票v2＋v3の境界4
- 開始基準commit：`6d8b8cd`

## 1. 目的とRED

【判断】同一入力の再保存を同じIDの`unchanged`とし、異なる内容と同時更新を既存内容の無変更で拒否する。

【実測】同一入力二回目の全file bytes・inode・mtime不変、合成した同一IDへの異なるbytesの拒否、barrierで同時開始した
二処理が両方成功しないことの3試験を追加した。次の単独commandは終了コード1、3 failed、26 deselectedだった。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py -k 'unchanged or existing_record_id or concurrent'
```

失敗は順に`record_exists`、異なるIDへの誤った新規保存、競合側の`record_exists`で、主要理由は既存IDと同時更新を
安全に区別する処理がないことだった。

## 2. 最小GREEN

【実測】記録ID算出を`_record_id`へ分け、排他的directory作成が既存を検出した場合だけ、二rootの記録directoryを
symlink非追跡で開き、安全属性、固定file集合、全file bytesを読取り専用で照合する処理を追加した。完全一致だけを
`unchanged`、確定印前を`record_busy`、確定済み不一致を`record_conflict`とする。復旧、通常再読込み、削除は追加していない。

## 3. GREENと回帰

【実測】上記単独commandは終了コード0、3 passed、26 deselected。専用試験は終了コード0、29 passed。
正式入口関連を含む次の単独commandは終了コード0、50 passedだった。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py tests/test_session_log_read_only_entry.py tests/test_session_log_pipeline.py tests/test_session_log_provenance.py
```

【実測】`git diff --check`は終了コード0。変更後SHA-256は次のとおり。

- `tools/session_logs/safe_storage.py`：`9a7be77d2ca1bf655614a973a2af52990a2a24a5597875a443bd9051ac3c7a2b`
- `tests/test_session_artifact_safe_storage.py`：`3cfcf2e1a9bc94e12ef147885156b46c540a69f660f5f6aafa3094229e1a9116`

## 4. 判断・未実施

【判断】境界4はREDを変えず最小GREENとなり、同一入力の無書込みと一件排他を実fileで確認した。

【未実施】途中復旧、通常再読込み、期限切れ、削除計画、削除、製品入口、正規全試験、故障注入、独立完了レビュー、
製品受入判断、外部送信、push、履歴書換えは実施していない。
