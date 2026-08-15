# One-design acceptance boundary 4 completion evidence v1

## Purpose

G08 の境界1〜4を結合し、配布後の正式実行名、対象・関連・全試験、既存G08不変、変更範囲、合成一件を独立完了確認へ渡せる固定Evidenceにする。

## Fixed authority

- Task Contract: `records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- Contract SHA-256: `8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- Work ticket v1: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md`
- Work ticket v2: `docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v2.md`
- Boundary 4 RED commit: `1a86295`
- Existing G08 protected baseline: `40b399d`

## Product artifacts

| path | SHA-256 |
| --- | --- |
| `tools/design/one_design_acceptance.py` | `da340bda3b8d8b51a95afecb6ebcd273fcd52ce9e8e2a7b39cc336b0074b7ed3` |
| `tools/design/one_design_acceptance_entry.py` | `7535aa6652514c6ce4dfd31facd2640944a356ddc04802b0df8ae63a9bec9823` |
| `tests/test_one_design_acceptance.py` | `cfdbc3eee7b5fcfcf98ee10454d67308c6ed681de9afb7c0deb8c5a7e997197b` |
| `pyproject.toml` | `d6feb1494e03f94dfe4efad0cb22117c94d35e13902571604833cdda63b4d2f8` |

【実測】`pyproject.toml`の製品変更は次の正式実行名一件だけで、既存実行名と依存一覧を変更していない。

```text
reviewcompass3-design-acceptance-check = "tools.design.one_design_acceptance_entry:main"
```

## Distribution execution

【実測】次を単独実行し、終了コード0となった。

```text
.venv/bin/python3 -m pip install --no-deps --no-build-isolation -e .
```

出力は`file:///Users/Daily/Development/ReviewCompass3`からeditable wheelを構築し、`reviewcompass3 0.0.1`を再配置した。依存packageの取得・追加はなく、pip cacheは権限不足のため無効化された。

## Test and validation receipts

【実測】各commandを単独で実行した。

1. `.venv/bin/python3 -m pytest -q tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: `91 passed in 0.54s`
2. `.venv/bin/python3 -m pytest -q tests/test_bootstrap_conformance.py tests/test_design_contract.py`
   - exit code: `0`
   - result: `31 passed in 0.13s`
3. `git diff --exit-code 1a86295 -- tests/test_one_design_acceptance.py`
   - exit code: `0`
   - result: 境界4 RED commit後の試験差分なし
4. `git diff --exit-code 40b399d -- tools/design/bootstrap_conformance.py tools/design/design_contract.py tests/test_bootstrap_conformance.py tests/test_design_contract.py`
   - exit code: `0`
   - result: 既存G08保護対象4fileの差分なし
5. `git diff --check`
   - exit code: `0`

### Full-suite environment observation

【実測】通常環境の`.venv/bin/python3 -m pytest -q --tb=short`は終了コード1、`12 failed, 2099 passed in 48.59s`だった。12件はすべて既存`tests/test_claude_implementation_executor.py`で、host環境に存在する`ANTHROPIC_API_KEY`を既存安全機構が`api_key_environment_forbidden`としてfixtureより先に拒否した。G08対象の失敗ではない。

【実測】既存executorが禁止する認証環境名6件だけをprocess環境から除き、次を単独実行した。

```text
env -u ANTHROPIC_API_KEY -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_FOUNDRY_API_KEY -u ANTHROPIC_VERTEX_PROJECT_ID -u AWS_BEARER_TOKEN_BEDROCK .venv/bin/python3 -m pytest -q --tb=short
```

- exit code: `0`
- result: `2111 passed in 49.45s`

【判断】最初の12件は製品差分ではなく、既存試験の隔離前提とhost認証環境の差である。既存コード・試験を変更せず、禁止認証値を子processへ渡さない既存方針と同じ隔離条件で全試験合格を確認した。

## Change scope

【実測】実装開始訂正commit `063621a`より後の製品・試験差分は、作業票§2.1が許可した次の4 pathだけである。

1. `tools/design/one_design_acceptance.py`
2. `tools/design/one_design_acceptance_entry.py`
3. `tests/test_one_design_acceptance.py`
4. `pyproject.toml`の実行名一件

その他は本作業のEvidence、review、TODOである。既存G08保護対象、既存schema、既存試験は変更していない。

## Synthesized one-item result

【実測】配置後の正式実行名をrepository外の`/private/tmp/g08-acceptance-e2e/outside`から実行し、終了コード0、標準エラー空で次を得た。

- design: `DESIGN-SAMPLE`、3 facts、SHA-256 `08e0a3dfea15b97b187985bacaabcfc8268aefb497ac3cc7a26c8ca3cf421402`
- acceptance: `ACCEPTANCE-SAMPLE`、3 conditions、SHA-256 `5018b3557cb86a0f7fbb07147e7719059f2e1ca23d7023b750699c0006c60961`
- comparison SHA-256: `6867a81051cf955b987976378f5ccdcafc07edf3fc99b41cbabca961030b0474`
- counts: satisfied 1、contradicted 1、missing 1、unreferenced fact 1
- Human queue: contradicted `C-LEVEL`、missing `C-MISSING`、satisfied `C-MODE`、unreferenced `F-EXTRA`の固定順
- verdict: `review_required`
- decision: `pending_human_decision`
- external send approved: `false`

【実測】出力には入力自由値と絶対pathを含めず、安全な識別子、固定語彙、件数、内容識別値だけを含んだ。

## Contract connection before independent review

| conditions | evidence |
| --- | --- |
| 1〜9 | 境界1の比較核43件とGREEN Evidence |
| 10〜11 | 境界2の安全読込、hard link、symlink差替え、前後identity試験とGREEN・訂正Evidence |
| 12〜14 | 境界3のsource別停止、安全表示、禁止作用試験とGREEN Evidence |
| 15 | 配置後正式名をrepository外から正常・停止実行する境界4試験 |
| 16 | 既存G08保護対象差分0、関連31件成功 |
| 17 | 対象91件、関連31件、隔離全2111件成功 |
| 18 | 固定commitへの別担当読取り専用確認待ち |
| 19 | 上記合成一件 |
| 20 | 条件18合格後の利用者製品受入待ち |

## Judgment

【判断】境界4の実装と機械確認は完了した。条件18の独立完了確認はまだ未実施であり、製品受入を求める段階ではない。配布設定、Evidence、本TODOを固定commitへ置いた後、別担当が条件1〜19を読取り専用で確認する。
