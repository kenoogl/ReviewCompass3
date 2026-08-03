---
record_id: RC3-LAYOUT-BASELINE-V2-RED-EVIDENCE-2026-08-04-V1
recorded_at: 2026-08-04T06:23:00+09:00
status: verified_red
---

# Layout Baseline v2 RED Evidence V1

## 固定対象

| role | artifact | SHA-256 |
|---|---|---|
| v2 candidate | `records/development/2026-08-04-layout-baseline-v2-candidate.json` | `4a086be730b3310cc6933826ab6dac751e36af0596c5a8b6a7e381357d956282` |
| RED／GREEN共通Test | `tests/test_layout_baseline.py` | `baf7ae308aa2aa7f887b69f60e37f367ba8ddc1597564071af10e4e14f4f3ef4` |
| implementation before change | `tools/layout/baseline.py` at `HEAD` | `3566bf40ff5e4da7ce1e2b832c92a615b38feed5cf08ff1f4e997ca17c2273e6` |
| v2 Project Manifest fixture | `tests/fixtures/layout/empty-project-v2/.reviewcompass/project-manifest.json` | `78eebc2b86779c6b6b9ece1fb9ed1fd458ebd3a22d3d1cb9df6681af64295e2c` |

## 実行

```text
python3 -m pytest tests/test_layout_baseline.py -q
```

結果は`4 failed, 7 passed in 0.08s`だった。

## 失敗理由

1. v2 Layout Baselineの追加fieldを現行loaderが拒否した。
2. schema version 2のProject Manifestを現行loaderが拒否した。
3. `snapshot_project_artifacts`が未実装だった。
4. deployment package境界の検査を開始する前にv2 baseline loadで停止した。

既存v1 Test 7件はすべて合格した。失敗はv2未実装と新API未実装に限定され、fixtureまたは既存機能の
偶発的な失敗ではなかった。

## 実行入口の手戻り

最初に`.venv/bin/python3`を選択したが、このworkspaceに`.venv/bin/python3`は存在せずTestを開始できなかった。
`command -v python3`、`python3 --version`、pytest importを機械確認し、policy設定と同じ`/usr/bin/python3`
（Python 3.9.6、pytest 8.4.2）で上記REDを取得した。成果物の失敗ではない。
