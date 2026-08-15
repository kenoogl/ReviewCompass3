# Session記録安全保存 境界9 四操作製品入口TDD Evidence v1

- 実施日：2026-08-15
- 開始基準commit：`7658773`

【実測】`store`、`load-derived`、`plan-delete`、`delete`の連続呼出し、非正常な上流結果の保存拒否、
停止出力、配布用実行名、能力拡張禁止を先に5試験へ固定した。単独実行は終了コード1、5 failedで、
主要理由は`tools.session_logs.safe_storage_entry`不在だった。

【実測】引数で受けた明示root、一記録ID、時刻、確認値だけを保存核へ渡す入口を追加した。`store`は既存の
`prepare_safe_result`を値で呼び、終了コード0かつ`status: ok`だけを保存する。各呼出しは正準順のJSONを一回だけ
標準出力へ出し、`StorageStop`と予期しない例外はpathと例外本文を含まない固定停止結果に変換する。

【実測】同じ試験は終了コード0、5 passed。保存核と新入口60 passed、既存正式入口・pipeline・provenance・
開発環境30 passed、`git diff --check`は終了コード0だった。入口sourceはnetwork、外部process、Git、環境値解決を
含まないことを試験で確認した。

- 入口実装SHA-256：`566aedf4410ebb5ae963063eb10eb41616795d8a1a2078e5ca611527f251cc52`
- 入口試験SHA-256：`2ad0c021cdc4cf8e40cf910b82d43fe5062f1961a0ab087abf0c8ff79e8a50e1`
- 配布宣言SHA-256：`ce5e971d3769b676d11435e8ad76b84e52fbb4131a97202fa7deef707ea1fd72`

【判断】境界9はREDを変えず最小GREENとなった。境界1から9の最終検証、独立完了レビュー、利用者の
製品受入判断は未実施であり、この時点では正式・安定と表示しない。
