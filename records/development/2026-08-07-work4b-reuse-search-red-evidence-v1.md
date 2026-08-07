# Work 4B最小試行 reuse_search_record RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK4B-MINIMAL-PILOT-SCOPE-001`
  （`records/development/2026-08-07-work-4b-minimal-pilot-scope-approval-decision-v1.md`）
- 範囲提案：`docs/design/2026-08-07-work-4b-minimal-pilot-scope-proposal.md`、SHA-256
  `51eec963e5b7469110658a2a0b95f9d4effbe9279f078175076fe0e1dda2169a`

## 1. 宣言→RED対応表の関門

対応表は`records/development/2026-08-07-work4b-reuse-search-declaration-red-map-v1.json`
（`RC3-WORK4B-REUSE-SEARCH-DECLARATION-RED-MAP-001`）。機械照合（Python AST）の結果：

- 宣言：7件（R1〜R7）
- **testの無い宣言：0件**
- 列挙したのにfileへ実在しないtest：0件
- どの宣言にも結ばれないtest：0件

## 2. 固定したTest

`tests/test_work4b_reuse_search_record.py`、8 test。宣言との対応は対応表を正本とする。

## 3. RED結果（機械実行）

- targeted：`.venv/bin/python3 -m pytest -q tests/test_work4b_reuse_search_record.py`、
  exit code `2`、`1 error during collection`。失敗理由は全件
  `ImportError: cannot import name 'reuse_search_record' from 'tools.development'`
  であり、対象module `tools/development/reuse_search_record.py` 未実装による期待どおりのREDである。
- 既存全Test：`.venv/bin/python3 -m pytest -q --ignore=tests/test_work4b_reuse_search_record.py`、
  `1047 passed`、exit code `0`。既存Testは弱めていない。

## 4. 状態と次

- 実装、実検索、`reuse_search_record`の実record生成、GREENは未実施。
- 本RED作業単位のcommit後、固定Testを変更せずGREEN実装（提案§5手順3〜4）へ進む。
- 恒久tool化の判断点（対応表の機械照合を毎回のその場AST照合から恒久toolへ移すか）はHumanへ提示済みで、
  判断まで本mapは確立済みのその場照合方式で作成した。
