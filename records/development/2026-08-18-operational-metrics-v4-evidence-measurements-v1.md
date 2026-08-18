# 測定ブロック：運用集計v4（基点別解決・履歴照合）受入確認の実測

- captured_at：2026-08-18T21:33:23+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-operational-metrics-v4-evidence-commands-v1.json`（SHA-256 `9aeb0aba6b9abe989c341d7cf42db5879b281863f5113da350feca0d7d158022`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 運用集計試験15本の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nr = subprocess.run(['.venv/bin/python3', '-m', 'pytest', 'tests/test_operational_metrics.py', '-q'], capture_output=True, text=True)\nprint('exit', r.returncode)\nprint(r.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.427s
- 完全性：二重実行一致

- stdout：

```text
exit 0
15 passed

```

## dataset v1〜v3不変とv4・装置・試験のdigest固定

- argv：`["shasum", "-a", "256", "records/development/2026-08-18-operational-metrics-dataset-v1.json", "records/development/2026-08-18-operational-metrics-dataset-v2.json", "records/development/2026-08-18-operational-metrics-dataset-v3.json", "records/development/2026-08-18-operational-metrics-dataset-v4.json", "tools/evaluation/operational_metrics.py", "tests/test_operational_metrics.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
6a85d7d87239bdc17afbad3459c9bdca52d1402cbfc0137039388fb3619cdd25  records/development/2026-08-18-operational-metrics-dataset-v1.json
d39fbf1f641ae426a63736856cb99d7c3e02620894aae517c6c7e13ee476c0fd  records/development/2026-08-18-operational-metrics-dataset-v2.json
ef79c8e506cd0e276a80a1bb0a8ed17d2d337ce89925ec8c25b107001859ffbb  records/development/2026-08-18-operational-metrics-dataset-v3.json
faad88327bf4a0a987fb88e8b8eff45a0f55b50d959e6b08a833da33d6cbc8bb  records/development/2026-08-18-operational-metrics-dataset-v4.json
c82805939e644d6e8165a18811bda91356522b82f2014cbe43b6ebe94856106e  tools/evaluation/operational_metrics.py
80f9f7588f25f0a89cb9a9bd8d59931997871af0ef0571400032176057559694  tests/test_operational_metrics.py

```
