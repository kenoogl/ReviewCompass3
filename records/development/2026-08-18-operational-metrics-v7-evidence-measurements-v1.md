# 測定ブロック：運用集計v7（系統意味づけ・道具正規化・活動時間）受入確認の実測

- captured_at：2026-08-18T22:35:56+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-operational-metrics-v7-evidence-commands-v1.json`（SHA-256 `cef93abdb85f053cf30ec6de731925b541056864c22e7c2c8f9be4f4c262fdfd`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 運用集計試験25本の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nr = subprocess.run(['.venv/bin/python3', '-m', 'pytest', 'tests/test_operational_metrics.py', '-q'], capture_output=True, text=True)\nprint('exit', r.returncode)\nprint(r.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：28.579s
- 完全性：二重実行一致

- stdout：

```text
exit 0
25 passed

```

## dataset v1〜v7・装置・試験のdigest固定

- argv：`["shasum", "-a", "256", "records/development/2026-08-18-operational-metrics-dataset-v1.json", "records/development/2026-08-18-operational-metrics-dataset-v2.json", "records/development/2026-08-18-operational-metrics-dataset-v3.json", "records/development/2026-08-18-operational-metrics-dataset-v4.json", "records/development/2026-08-18-operational-metrics-dataset-v5.json", "records/development/2026-08-18-operational-metrics-dataset-v6.json", "records/development/2026-08-18-operational-metrics-dataset-v7.json", "tools/evaluation/operational_metrics.py", "tests/test_operational_metrics.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
6a85d7d87239bdc17afbad3459c9bdca52d1402cbfc0137039388fb3619cdd25  records/development/2026-08-18-operational-metrics-dataset-v1.json
d39fbf1f641ae426a63736856cb99d7c3e02620894aae517c6c7e13ee476c0fd  records/development/2026-08-18-operational-metrics-dataset-v2.json
ef79c8e506cd0e276a80a1bb0a8ed17d2d337ce89925ec8c25b107001859ffbb  records/development/2026-08-18-operational-metrics-dataset-v3.json
faad88327bf4a0a987fb88e8b8eff45a0f55b50d959e6b08a833da33d6cbc8bb  records/development/2026-08-18-operational-metrics-dataset-v4.json
2b6d9bbe5c99c44eeee08d3e32b9d4718cdc0d6c8fce322f9b604e8f6fdaf186  records/development/2026-08-18-operational-metrics-dataset-v5.json
94cfd626c817fd084514cdaf4ccedf6b01c94ffb98d7dbfdd8e1b6a1e18e3995  records/development/2026-08-18-operational-metrics-dataset-v6.json
7702463b46678ab52cf15b3f077fc590f51a2707fab5ab64bf6356ff5c3843c2  records/development/2026-08-18-operational-metrics-dataset-v7.json
0095c6e39dc13a59bfa3ccf61a45b4f8d0195172301f31027aaf8f660544ce4b  tools/evaluation/operational_metrics.py
cf003b343b74367495695fff1ced983c8978c868f67fe24a3ab03b32c67c2ea7  tests/test_operational_metrics.py

```

## dataset v1〜v6の不変（tracked差分なし＝出力空が合格）

- argv：`["git", "diff", "--name-only", "--", "records/development/2026-08-18-operational-metrics-dataset-v1.json", "records/development/2026-08-18-operational-metrics-dataset-v2.json", "records/development/2026-08-18-operational-metrics-dataset-v3.json", "records/development/2026-08-18-operational-metrics-dataset-v4.json", "records/development/2026-08-18-operational-metrics-dataset-v5.json", "records/development/2026-08-18-operational-metrics-dataset-v6.json"]`
- 実行体：/usr/bin/git
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

## dataset v7に絶対pathが無いことの機械確認（該当なし＝exit 1が合格）

- argv：`["grep", "-n", "/Users", "records/development/2026-08-18-operational-metrics-dataset-v7.json"]`
- 実行体：/usr/bin/grep
- exit：1・elapsed：0.002s
- 完全性：二重実行一致
