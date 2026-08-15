# One-design acceptance boundary 1 GREEN evidence v1

## Purpose

G08 の第1境界について、固定済みの先行試験を変更せず、比較核だけで契約条件1〜9を満たしたことを確認する。

## Fixed inputs

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket overlay: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v2.md`
- Work ticket SHA-256: `a733a57203a0148c52d722713be4b3948134192da6f5bceef8ab5eb92e9a58ec`
- RED commit: `03beeb4`
- Product core: `tools/design/one_design_acceptance.py`
- Fixed test: `tests/test_one_design_acceptance.py`

## Execution and results

【実測】各commandを単独で実行した。

1. `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `43 passed in 0.02s`
2. `.venv/bin/python3 -m pytest -q tests/test_bootstrap_conformance.py tests/test_design_contract.py tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `74 passed in 0.14s`
3. `git diff --exit-code HEAD -- tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: RED commit後の試験差分なし
4. `git diff --exit-code 40b399d -- tools/design/bootstrap_conformance.py tools/design/design_contract.py tests/test_bootstrap_conformance.py tests/test_design_contract.py`
   - exit code: `0`
   - result: 既存G08保護対象4fileの差分なし
5. `git diff --check`
   - exit code: `0`

## Implemented scope

【実測】追加した製品コードは `tools/design/one_design_acceptance.py` だけである。比較値、設計、受入条件を閉じたschemaとして検査し、JSON同名項目を正規化前に拒否する。4演算、欠落、未参照、固定順の人の判断一覧、自由値を出さない正常結果、正規化後の内容識別値を生成する。

【実測】CLI入口、安全なfile読込、`pyproject.toml`のcommand登録、file書込み、通信、外部process、Git操作はこの境界に追加していない。

## Judgment

【判断】第1境界はGREENであり、境界2の安全読込に進める。合格根拠は固定試験43件、既存関連試験31件、試験無変更、保護対象無変更の4点である。
