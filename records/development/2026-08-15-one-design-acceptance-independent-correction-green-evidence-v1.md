# One-design acceptance independent correction GREEN evidence v1

## Purpose

独立完了確認v1が止めた形式検査1系統3変種を、既存試験を変えずに限定修正し、条件9・12の再確認材料を固定する。

## Fixed inputs

- Independent review: `records/development/2026-08-15-one-design-acceptance-independent-completion-review-v1.md`
- Review SHA-256: `4af8107d8f617f26720cf34bc6ab12167e8f73c31439ecfc7aa4f14f6ca05888`
- Correction RED commit: `184f1f5`
- Correction RED Evidence: `records/development/2026-08-15-one-design-acceptance-independent-correction-red-evidence-v1.md`
- Product core: `tools/design/one_design_acceptance.py`
- Product core SHA-256: `b3af7fdf254b21e5d368f2a02cf2aba23a86233a67b4120e7c2b39a3fd4a5c14`
- Test SHA-256: `6adc44ad7c7c9dff37ad3e671abfc0e86d9c5afe53861f2edeafc7acd01e1542`

## Limited implementation

【実測】製品差分は`tools/design/one_design_acceptance.py`の25行だけで、他の製品fileは変更していない。

1. `schema_version`を`type(value) is int`かつ値1に限定した。
2. JSON復号の`ValueError`を対象sourceの`invalid_schema`へ変換した。
3. scalar文字列と文字列配列要素で、Unicode単独surrogateを`invalid_schema`として拒否した。

【実測】比較、正常・停止出力schema、path読取り、CLI、配布設定、既存G08は変更していない。

## Execution and results

【実測】各commandを単独実行した。

1. `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `107 passed in 0.13s`
2. `.venv/bin/python3 -m pytest -q tests/test_bootstrap_conformance.py tests/test_design_contract.py`
   - exit code: `0`
   - result: `31 passed in 0.12s`
3. `git diff --exit-code 184f1f5 -- tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: correction RED commit後の試験差分なし
4. `git diff --exit-code 40b399d -- tools/design/bootstrap_conformance.py tools/design/design_contract.py tests/test_bootstrap_conformance.py tests/test_design_contract.py`
   - exit code: `0`
   - result: 既存G08保護対象4fileの差分なし
5. `git diff --check`
   - exit code: `0`
6. 禁止認証環境名6件を除く`.venv/bin/python3 -m pytest -q --tb=short`
   - exit code: `0`
   - result: `2127 passed in 42.45s`

## Corrected counterexamples

【実測】設計・受入条件それぞれで、形式版`true`、`false`、`1.0`、5,000桁整数、単独surrogate文字列、単独surrogate文字列配列が、直接核の`invalid_schema / target source`となった。巨大整数と単独surrogateの正式入口は終了コード2、同じsourceの固定停止JSONとなった。

【判断】独立レビューの3変種は閉じた。条件9の固定形式と条件12の対象source別固定停止は、追加16件へ接続された。

## Judgment

【判断】限定修正はGREENである。ただし条件18は、修正後固定commitを同じ別担当が再確認するまで未達であり、Human条件20をまだ求めない。
