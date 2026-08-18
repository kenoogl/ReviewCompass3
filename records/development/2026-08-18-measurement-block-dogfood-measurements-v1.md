# 測定ブロック：測定ブロックtool新設のGREEN測定（dogfooding）

- captured_at：2026-08-18T19:08:44+09:00
- 宣言file：`records/development/2026-08-18-measurement-block-dogfood-commands-v1.json`（SHA-256 `96018b30ee59870491976cdda067e5bb69335f1ba15c64c20d81a57ad4de5a08`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止）

## 新設試験の単独実行

- argv：`[".venv/bin/python3", "-m", "pytest", "tests/test_measurement_block.py", "-q"]`
- exit：0・elapsed：0.2s

- stdout：

```text
.......                                                                  [100%]
7 passed in 0.10s

```

## 流用元保護（record_run系）の単独実行

- argv：`[".venv/bin/python3", "-m", "pytest", "tests/test_session_log_record_run.py", "-q"]`
- exit：0・elapsed：0.442s

- stdout：

```text
..........                                                               [100%]
10 passed in 0.34s

```

## 複製禁止掃引の単独実行

- argv：`[".venv/bin/python3", "-m", "pytest", "tests/test_shared_function_sweep.py", "-q"]`
- exit：0・elapsed：0.415s

- stdout：

```text
.........................                                                [100%]
25 passed in 0.32s

```

## 遡り一元化の維持確認

- argv：`["grep", "-rn", "parents\\[", "tools/", "--include=*.py"]`
- exit：0・elapsed：0.016s

- stdout：

```text
tools/common/roots.py:16:  return Path(__file__).resolve().parents[2]

```
