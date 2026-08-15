# One-design acceptance boundary 2 GREEN evidence v1

## Purpose

G08 の第2境界について、明示root内の異なる通常file二件だけを、全構成要素のsymlinkと読取り中の変更を受け入れずに読めることを確認する。

## Fixed inputs

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md` §4
- Boundary 2 RED commit: `33db426`
- Product: `tools/design/one_design_acceptance.py`
- Test: `tests/test_one_design_acceptance.py`
- Test correction evidence: `records/development/2026-08-15-one-design-acceptance-boundary2-test-correction-evidence-v1.md`

## Execution and results

【実測】各commandを単独で実行した。

1. `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `70 passed in 0.04s`
2. `.venv/bin/python3 -m pytest -q tests/test_bootstrap_conformance.py tests/test_design_contract.py tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `101 passed in 0.16s`
3. `git diff --exit-code 40b399d -- tools/design/bootstrap_conformance.py tools/design/design_contract.py tests/test_bootstrap_conformance.py tests/test_design_contract.py`
   - exit code: `0`
   - result: 既存G08保護対象4fileの差分なし
4. `git diff --check`
   - exit code: `0`

## Implemented scope

【実測】`read_input_pair()`は絶対pathを純粋な構成要素へ分け、`/`からroot、rootから各fileまでをdirectory file descriptor相対で一要素ずつ開く。directoryは`O_DIRECTORY | O_NOFOLLOW`、fileは`O_RDONLY | O_NOFOLLOW | O_NONBLOCK`を使い、必須flag不在では停止する。

【実測】open後と読取り後に通常file、size、機器番号、inodeを照合し、262,144 bytesより1 byte多く読める上限処理、実読取りbyte数、二fileのopen後identityを検査する。成功・停止経路でdescriptorを閉じる。

【実測】CLI entry、`pyproject.toml`、file書込み、directory作成、通信、外部process、Git、環境値、権限変更、削除、探索は追加していない。

## Test correction boundary

【記録】RED後の試験差分は、実socket fixtureを決定的な`fstat`差替えへ直した1件、既存契約のhard link・open直前symlink差替えを補った2件、低位例外保持を検出して実際にREDとなった1件である。理由と初回失敗はtest correction evidenceへ分離した。比較・停止・pathの期待値は変更していない。

## Judgment

【判断】第2境界はGREENであり、境界3の正式命令入口と安全表示へ進める。合格根拠は対象70件、既存関連31件、保護対象差分0、安全読込以外の製品能力追加なしである。
