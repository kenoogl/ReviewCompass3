# Session記録安全保存 境界1 値受渡しTDD Evidence v1

- 実施日：2026-08-15
- 対象境界：累積実装作業票v2＋v3の境界1「正式入口の値受渡し」
- 開始可レビュー：`records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v3.md`
- 開始基準commit：`2d314f4`
- 実施担当：主担当Codex

## 1. 目的

【判断】既存の正式な読取り専用入口が正常、部分、停止の安全結果を、標準出力せず`(終了コード, 結果)`として
保存処理へ渡せるようにする。保存、保持期限、root権限、削除は扱わない。

## 2. RED

【実測】`tests/test_session_log_read_only_entry.py`へ、正常、部分、停止の三例で
`prepare_safe_result(raw_root, raw_log)`を呼び、stdoutとstderrが空で、終了コードと結果値が従来契約に一致する試験を追加した。

【実測】実装変更前に次を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_log_read_only_entry.py -k prepare_safe_result
```

- 終了コード：1
- 結果：3 failed、12 deselected
- 三例の主要な失敗理由：`AttributeError: module 'tools.session_logs.read_only_entry' has no attribute 'prepare_safe_result'`

【判断】正常、部分、停止の三例はすべて公開関数不在という一つの理由だけで失敗し、境界1のREDとして正しい。

## 3. 最小GREEN

【実測】`tools/session_logs/read_only_entry.py`で、既存`run()`内の入力解決、成果物作成、安全結果作成、例外分類を
`prepare_safe_result`へ移し、同関数が標準出力せずtupleを返すようにした。`run()`は引数解決後に同関数を呼び、
従来どおり一回だけJSONを表示して同じ終了コードを返す。

【実測】保存module、保持期限、root権限、削除、製品設定、配布入口は追加または変更していない。

## 4. GREENと回帰確認

【実測】新規試験を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_log_read_only_entry.py -k prepare_safe_result
```

- 終了コード：0
- 結果：3 passed、12 deselected

【実測】正式入口file全体を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_log_read_only_entry.py
```

- 終了コード：0
- 結果：15 passed

【実測】正式入口とpipeline、provenanceの関連試験を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_log_read_only_entry.py tests/test_session_log_pipeline.py tests/test_session_log_provenance.py
```

- 終了コード：0
- 結果：21 passed

【実測】`git diff --check`は終了コード0だった。変更後SHA-256は次のとおり。

- `tools/session_logs/read_only_entry.py`：`7d731d0c6304e4dc0e1d2a706adfabb757981822c1506914000736b99e1f7871`
- `tests/test_session_log_read_only_entry.py`：`0dd4d70123deb0a8d12284d58fbe74d905d2e2d8e48c2032f55cec77d2d9e940`

## 5. 判断

【判断】境界1はRED試験を変更せず最小GREENになった。既存入口の正常、部分、停止出力、終了区分、安全検査、
stderr空は既存試験を含む15件で維持され、関連21件も合格した。境界2へ進む前に本単位をcommitする。

## 6. 未実施

【未実施】安全な保存前検査、記録directory作成、保存、保持期限、再読込み、復旧、削除計画、削除、製品入口、
正規全試験、故障注入、独立完了レビュー、製品受入判断は実施していない。外部送信、push、履歴書換えも行っていない。
