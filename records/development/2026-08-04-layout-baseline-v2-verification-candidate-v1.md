---
record_id: RC3-LAYOUT-BASELINE-V2-VERIFICATION-CANDIDATE-2026-08-04-V1
recorded_at: 2026-08-04T06:26:15+09:00
status: verified_technical_human_approval_pending
---

# Layout Baseline v2 Verification Candidate V1

## 1. 対象

デプロイパッケージを交換可能にし、Project Artifactを移動させない境界を、Layout Baseline v2候補、
Project Manifest v2 fixture、機械validatorへ固定した。本Evidenceは技術的検証結果であり、Human承認前に
v2を現行authorityへ昇格しない。

## 2. 固定artifact

| role | artifact | SHA-256 |
|---|---|---|
| adopted design memo | `docs/design/2026-08-04-deployment-project-artifact-boundary-adoption-memo.md` | `a12434bb1fd927be25b060b07804877937406f93e14735f8564f19e3988752f1` |
| Human Decision | `records/development/2026-08-04-deployment-project-artifact-boundary-decision.json` | `237dd1d0d40304240f0d8376713509c34364aaa6369d3161df3d3be2cc623c1b` |
| v2 Layout candidate | `records/development/2026-08-04-layout-baseline-v2-candidate.json` | `4a086be730b3310cc6933826ab6dac751e36af0596c5a8b6a7e381357d956282` |
| validator | `tools/layout/baseline.py` | `f7aba48e31021ec5a8ee6b9840804cc20e4988b0682256f53a6880e857dd42ad` |
| Test | `tests/test_layout_baseline.py` | `baf7ae308aa2aa7f887b69f60e37f367ba8ddc1597564071af10e4e14f4f3ef4` |
| Project Manifest fixture | `tests/fixtures/layout/empty-project-v2/.reviewcompass/project-manifest.json` | `78eebc2b86779c6b6b9ece1fb9ed1fd458ebd3a22d3d1cb9df6681af64295e2c` |
| RED Evidence | `records/development/2026-08-04-layout-baseline-v2-red-evidence-v1.md` | `07f4d724c5ab8c11f3d25b38261e36433aef7b18e0a0a956807101cc0b7507d5` |
| official GREEN receipt | `records/development/2026-08-04-layout-baseline-v2-green-test-receipt-v1.json` | `0c95f01246bba78272cbd55a6f3ae1e2367d2b1ca9c446ead048440b836c8aae` |

## 3. 実装した機械検査

- v1を変更せず、Layout BaselineとProject Manifestのversion 2を別形状として読める。
- Project Manifest v2は`.reviewcompass/workflow`を必須artifact rootとして扱う。
- workflow配下の既存pathとDigestをsnapshotし、追加を許可しながら既存recordの削除、移動、書換えを拒否する。
- deployment package直下へProject Manifestまたは`.reviewcompass/workflow`が混入すると拒否する。
- stable／development分離、checkout移動、相対参照、migration completenessのv1検査を維持する。

## 4. 検証結果

- 対象Test：`11 passed in 0.05s`
- 公式全Test：`500 passed in 2.56s`
- 公式runner：`RC3-DEVELOPMENT-TEST-RUNNER` version 1
- configured／resolved Python：`python3`／`/usr/bin/python3`
- fallback：`false`
- v2 fixtureの端末固有絶対path finding：0件
- JSON再読込：candidate、Decision、GREEN receiptが合格
- `git diff --check`：findingなし
- task専用`PYTHONPYCACHEPREFIX`を使用した`py_compile`：合格

## 5. 未実施とauthority状態

- v2 candidateの`status`は`candidate`のままである。
- Work 1A v1 recordとEvidenceは書き換えていない。
- 実際の`.reviewcompass/workflow/` Pilot recordは作っていない。
- Deployment Manifest、package builder、原子的切替、rollbackは実装していない。
- v2を現行Layout Baselineへ昇格するHuman判断は未実施である。

## 6. Human判断候補

v2候補と本検証結果を承認し、Issue Resolution早期PilotのProject Artifact配置として
`.reviewcompass/workflow/`を有効にするか判断する。承認時はv1を削除せずhistorical verifiedとして保持し、
v2のcurrent authority、v1のsuperseded範囲、Pilot再開条件を別Decisionへ固定する。
