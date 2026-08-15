# One-design acceptance boundary 3 GREEN evidence v1

## Purpose

G08 の第3境界について、正式命令入口が引数を読取り前に閉じて検査し、正常・停止とも安全な正準JSON一件だけを返すことを確認する。

## Fixed inputs

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md` §5
- Overlay: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v2.md` §2
- Boundary 3 RED commit: `4984c2b`
- Entry: `tools/design/one_design_acceptance_entry.py`
- Fixed test: `tests/test_one_design_acceptance.py`

## Execution and results

【実測】各commandを単独で実行した。

1. `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `88 passed in 0.05s`
2. `.venv/bin/python3 -m pytest -q tests/test_bootstrap_conformance.py tests/test_design_contract.py tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `119 passed in 0.17s`
3. `git diff --exit-code 4984c2b -- tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: 境界3 RED commit後の試験差分なし
4. `git diff --exit-code 40b399d -- tools/design/bootstrap_conformance.py tools/design/design_contract.py tests/test_bootstrap_conformance.py tests/test_design_contract.py`
   - exit code: `0`
   - result: 既存G08保護対象4fileの差分なし
5. `git diff --check`
   - exit code: `0`

## Implemented scope

【実測】入口は`check`と3個の一意な固定引数だけを受け付け、絶対pathの字句構造を入力読取り前に検査する。安全読込と比較核へ規則を追加せず、正常結果をそのまま正準JSONへ変換する。

【実測】既知停止は固定reason/sourceだけを終了コード2へ、未知例外は本文を捨てて`internal_failure / none`だけを終了コード4へ変換する。正常は終了コード0である。各出力は正準JSON一件と改行一つだけで、標準エラーへ書かない。

【実測】設計・受入条件それぞれのopen、size、UTF-8、schema停止、owner不明読取り停止、内部例外の秘密候補・path非表示を試験した。file書込み、通信、外部process、Git、環境値、権限変更、探索は追加していない。

## Judgment

【判断】第3境界はGREENであり、境界4の配布・結合へ進める。合格根拠は固定対象88件、既存関連31件、試験無変更、保護対象差分0である。
