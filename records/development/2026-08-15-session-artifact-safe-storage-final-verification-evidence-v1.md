# Session記録安全保存 最終検証Evidence v1

- 実施日：2026-08-15
- 境界1から9のcommit：`c90daa1`、`81d7f4d`、`6d8b8cd`、`d9c08dd`、`1295f04`、
  `f21c8ac`、`ec50cf6`、`7658773`、`6316d5f`
- 採用契約：`TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002` version 3、SHA-256
  `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`

## 実施と結果

【実測】製品入口E2Eは、repository外の合成一件について`store`、`load-derived`、`plan-delete`、`delete`を
同じ入口から順に呼び、各呼出しが標準error 0 byte、標準出力JSON一件、期待終了区分となった。保存拒否のpartial・
stoppedも固定停止JSON一件で、上流結果本文を転送しなかった。

【実測】故障注入は、raw書込み後、派生物書込み後、manifest書込み後、確定印前、raw一時file書込み後、片側の
`deleting`書込み後、raw削除後、派生物削除後、確定印削除後から、同じ入力または同じ削除確認値で再開できた。
誤確認値3例はbytes、inode、mtimeを変えなかった。

【実測】raw、派生物、manifest、operation、commitの各一文字改変では通常本文を返さなかった。保存後のfile mode、
記録directory mode、追加ACL、file symlink、所有者不一致、file種別不一致を四操作へそれぞれ注入した24例は、
全て本文返却・書込み・削除前に固定理由で停止し、対象状態を変えなかった。

【実測】独立oracleは、契約から固定file・一時file集合とmanifest来歴項目を実装とは別に列挙した。初回は終了コード1、
1 failedで、manifestの先行契約ID・版、正式入口版、規則SHA、書込み版の不足だけを検出した。三案比較では、既存版だけの
代用は不足、別file追加は変更過大、manifestへの平坦な固定項目追加が最小だったため最後を採用した。同じoracleは
変更せず終了コード0、1 passedとなった。

【実測】対象試験は次の単独command結果になった。

- `.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py tests/test_session_artifact_safe_storage_entry.py`
  — 85 passed、終了コード0。
- `.venv/bin/python3 -m pytest -q tests/test_session_log_read_only_entry.py tests/test_session_log_pipeline.py tests/test_session_log_provenance.py tests/test_development_environment.py`
  — 30 passed、終了コード0。
- `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt /private/tmp/reviewcompass-safe-storage-full-receipt-20260815-v2.json`
  — 1,850 passed、failed 0、error 0、skip 0、終了コード0。
- `git diff --check` — 終了コード0。

【実測】正規全試験の初回は1,849 passed、1 failedだった。安全保存の失敗ではなく、初期開発チェックリストが現行開発方針の
旧SHAを参照していた。checkerは不一致1、欠落・invalid 0と特定した。方針・checkerを変えず参照値一箇所だけを現行bytesへ
更新し、11参照中11一致を確認して`fd46af4`へ別commitした後、上記の正規全試験が合格した。

## 再読込み照合

- 保存核SHA-256：`c1b6fe5eccd14eda2b380ce58081bc31d84802b9dbc397fa71c8e7118c0ffec3`
- 製品入口SHA-256：`566aedf4410ebb5ae963063eb10eb41616795d8a1a2078e5ca611527f251cc52`
- 保存核試験SHA-256：`01678b3859bc31b32e03c0e58ddb3c56c8513ec404bd8995d24253859a137008`
- 製品入口試験SHA-256：`2ad0c021cdc4cf8e40cf910b82d43fe5062f1961a0ab087abf0c8ff79e8a50e1`
- 配布宣言SHA-256：`ce5e971d3769b676d11435e8ad76b84e52fbb4131a97202fa7deef707ea1fd72`
- 全試験receipt SHA-256：`5da2cac4dd26d96c0ae0f9d73badb07425bf8e5b955966c0a21bd85718db4f0b`

【実測】保存核と製品入口sourceに`subprocess`、`socket`、network client、`os.environ`、`os.getenv`、Git commandは
0件だった。標準出力、保存用派生物、manifest、削除後監査、固定名を対象にした合成秘密値・入力path・root不在試験は合格した。

## 判断

【判断】契約受入条件1から21を独立完了レビューへ渡せる技術状態になった。受入条件22の利用者受入は未実施であり、
本Evidenceだけで正式・安定とは表示しない。独立担当が固定commitを反証し、止める指摘が0件の場合だけ製品受入候補とする。

【未実施】push、外部送信、実Session記録の保存、実保存rootへの書込み、自動削除、複数記録探索は行っていない。
