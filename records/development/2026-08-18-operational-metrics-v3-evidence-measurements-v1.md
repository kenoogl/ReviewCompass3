# 測定ブロック：運用集計v3（書式C照合）受入確認の実測

- captured_at：2026-08-18T21:26:14+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-operational-metrics-v3-evidence-commands-v1.json`（SHA-256 `5fa37ba506cc1dc312aa3028750d058070f5a73726b3c8d9036e4f719eff6998`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 運用集計試験12本の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nr = subprocess.run(['.venv/bin/python3', '-m', 'pytest', 'tests/test_operational_metrics.py', '-q'], capture_output=True, text=True)\nprint('exit', r.returncode)\nprint(r.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.176s
- 完全性：二重実行一致

- stdout：

```text
exit 0
12 passed

```

## dataset v1・v2の不変とv3のdigest固定

- argv：`["shasum", "-a", "256", "records/development/2026-08-18-operational-metrics-dataset-v1.json", "records/development/2026-08-18-operational-metrics-dataset-v2.json", "records/development/2026-08-18-operational-metrics-dataset-v3.json", "tools/evaluation/operational_metrics.py", "tests/test_operational_metrics.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
6a85d7d87239bdc17afbad3459c9bdca52d1402cbfc0137039388fb3619cdd25  records/development/2026-08-18-operational-metrics-dataset-v1.json
d39fbf1f641ae426a63736856cb99d7c3e02620894aae517c6c7e13ee476c0fd  records/development/2026-08-18-operational-metrics-dataset-v2.json
ef79c8e506cd0e276a80a1bb0a8ed17d2d337ce89925ec8c25b107001859ffbb  records/development/2026-08-18-operational-metrics-dataset-v3.json
4096ab447e179f73acdad3c1947c2934723b1e7867e06beb6fbe9e922ebe31b8  tools/evaluation/operational_metrics.py
fcad153ff04bab7c4e608320a8be57cde1150a95c2ea23ac2dded3d6d0107bc8  tests/test_operational_metrics.py

```
