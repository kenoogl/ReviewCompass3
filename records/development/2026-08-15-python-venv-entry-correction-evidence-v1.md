# Python仮想環境入口の不一致訂正 Evidence v1

- Work ID：`WORK-PYTHON-VENV-ENTRY-CORRECTION-2026-08-15-V1`
- 日付：2026-08-15
- 状態：`corrected / venv_reverification_passed`
- 結果commit：本Evidenceを含むcommit

## 1. 事象

【実測】安全保存の再利用裁定とTODO更新作業中に、`python3`でPython処理を実行した。実際に解決された実行器は
`/usr/bin/python3`、Python 3.9.6だった。現在の正規仮想環境は
`/Users/Daily/Development/ReviewCompass3/.venv/bin/python3`、Python 3.13.14である。

【記録】利用者が、仮想環境でないPythonを使用していることを指摘した。指摘後、文書変更とcommit作業を停止し、
システムPythonによる合格表示を現在作業の合格根拠から外した。

## 2. 期待executorと実executor

| 項目 | 値 |
| --- | --- |
| 期待executor | `.venv/bin/python3`、Python 3.13.14 |
| 実executor | `/usr/bin/python3`、Python 3.9.6 |
| 影響した処理 | TODO単一検証、作業単位遷移確認、構造化入力表示、TODO projection生成 |
| 製品コードへの影響 | なし。製品コード、製品試験、製品設定は変更していない |

## 3. 原因

【実測】現在使う正本に次の古い実行例が残っていた。

- `docs/development/prompts/todo-handoff-update.md`：2件
- `AGENTS.md`：2件
- `docs/development/2026-08-02-development-policy.md`：4件

【判断】直接原因は、操縦役が実行前に正規Python入口を確認せず、文字どおり`python3`を実行したことである。
誘因は、現在の開発基準がシステムPythonへのfallbackを禁止している一方、上記正本の実行例が`python3`のまま残り、
入口間で不一致があったことである。古い実行例があっても、操縦役が現在の仮想環境baselineを優先すべきだった。

## 4. 訂正

【実施】上記8件の現在用実行例を`.venv/bin/python3`へ訂正した。歴史記録に残る過去commandは書き換えていない。

【実施】構造化入力からのTODO生成、生成結果とのbyte一致、TODO単一検証を、正規仮想環境で再実行した。

## 5. 再確認結果

| 確認 | 結果 | 終了コード |
| --- | --- | ---: |
| 正規Python | `.venv/bin/python3`、Python 3.13.14 | 0 |
| TODO projection再生成一致 | 6,692 bytesで完全一致 | 0 |
| TODO単一検証 | `findings: [] / status: passed` | 0 |
| 方針、仮想環境、TODO手順とprojectionの関連試験 | 43 passed | 0 |

【判断】システムPythonで得た以前の合格表示は再利用せず、上表の仮想環境による結果へ置き換える。

## 6. 手戻りとroute

| 項目 | 内容 |
| --- | --- |
| 対象操作 | Pythonを使う生成、検証、遷移確認 |
| 手作業理由 | 正本の実行例と仮想環境baselineの不一致を操縦役が実行前に解消しなかった |
| 事象とEvidence | §1から§5、および本Evidenceを含む差分と単独command終了コード |
| 機械処理候補 | 現在用正本のPython commandが`.venv/bin/python3`以外を指す場合に失敗させる既存方針試験へ接続する |
| route | `manual_rework_candidate / addressed_in_current_work` |

【未実施】Python本体、仮想環境、依存固定、製品処理、製品試験、製品設定、外部送信、push、履歴書換えは
変更または実行していない。
