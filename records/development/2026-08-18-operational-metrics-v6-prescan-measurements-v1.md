# 測定ブロック：運用集計v6（時系列復元・欠落由来）事前走査の実測

- captured_at：2026-08-18T21:47:40+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-operational-metrics-v6-prescan-commands-v1.json`（SHA-256 `aa989d6677fbc2f8cdfb510707908255d4163d8680ff6816a18ab06b82877ac2`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## raw区画の系統構成

- argv：`["ls", "/Users/keno/.reviewcompass3/projects/reviewcompass3/development/sensitive/eventual-preservation/raw"]`
- 実行体：/bin/ls
- exit：0・elapsed：0.002s
- 完全性：二重実行一致

- stdout：

```text
b12edc2408fa1263
c5ae2c27e5f07634
d48f07ecdd30cb6f

```

## 系統別file数と行形の出現数（内容不読・件数のみ）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nroot = Path('/Users/keno/.reviewcompass3/projects/reviewcompass3/development/sensitive/eventual-preservation/raw')\nfor system_dir in sorted(p for p in root.iterdir() if p.is_dir()):\n    files = sorted(system_dir.rglob('*.jsonl'))\n    print(system_dir.name, 'files:', len(files))\n    if files:\n        sample = files[0]\n        text = sample.read_bytes()\n        print(' ', 'sample_lines:', text.count(b'\\n'))\n        for pattern in (b'\\\"type\\\":\\\"tool_use\\\"', b'\\\"type\\\": \\\"tool_use\\\"', b'tool_use', b'\\\"timestamp\\\"', b'function_call'):\n            print(' ', pattern.decode(), text.count(pattern))\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.038s
- 完全性：二重実行一致

- stdout：

```text
b12edc2408fa1263 files: 1152
  sample_lines: 385
  "type":"tool_use" 0
  "type": "tool_use" 0
  tool_use 1
  "timestamp" 386
  function_call 0
c5ae2c27e5f07634 files: 19
  sample_lines: 861
  "type":"tool_use" 0
  "type": "tool_use" 0
  tool_use 0
  "timestamp" 866
  function_call 0
d48f07ecdd30cb6f files: 560
  sample_lines: 483
  "type":"tool_use" 73
  "type": "tool_use" 0
  tool_use 478
  "timestamp" 390
  function_call 0

```

## 装置と試験のdigest固定

- argv：`["shasum", "-a", "256", "tools/evaluation/operational_metrics.py", "tests/test_operational_metrics.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
d3c96f26f61e05781a0bbed8d9af8d1b82edc30b18a38551a5586175e3f3832a  tools/evaluation/operational_metrics.py
edd92afd0c07487b4e42af25a9f1fa136f708c13ce1ebad9bf0a882fcd53b305  tests/test_operational_metrics.py

```
