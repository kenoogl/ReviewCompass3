# 測定ブロック：運用集計v7（系統意味づけ・道具正規化・活動時間）事前走査の実測

- captured_at：2026-08-18T22:20:51+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-operational-metrics-v7-prescan-commands-v1.json`（SHA-256 `8006403be12925b6478e780a6fe18e3b09326db5f5bc3c6d0db95fdcde987d87`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## raw区画の系統構成

- argv：`["ls", "/Users/keno/.reviewcompass3/projects/reviewcompass3/development/sensitive/eventual-preservation/raw"]`
- 実行体：/bin/ls
- exit：0・elapsed：0.003s
- 完全性：二重実行一致

- stdout：

```text
b12edc2408fa1263
c5ae2c27e5f07634
d48f07ecdd30cb6f

```

## 保全設定からのnamespace導出と系統dirの照合（label・hashのみ出力）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfrom tools.session_logs.eventual_preservation import _namespace\nfrom tools.session_logs.record_run import DEFAULT_SYSTEMS\nroot = Path('/Users/keno/.reviewcompass3/projects/reviewcompass3/development/sensitive/eventual-preservation/raw')\ndirs = sorted(p.name for p in root.iterdir() if p.is_dir())\nmapping = {}\nfor label, source_root, _tool_version in DEFAULT_SYSTEMS:\n    namespace = _namespace(source_root)\n    mapping[namespace] = label\n    print('system', label, 'namespace', namespace, 'dir_exists', namespace in dirs)\nfor name in dirs:\n    print('dir', name, 'matched', name in mapping)\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.039s
- 完全性：二重実行一致

- stdout：

```text
system claude namespace d48f07ecdd30cb6f dir_exists True
system codex現行 namespace b12edc2408fa1263 dir_exists True
system codex保管 namespace c5ae2c27e5f07634 dir_exists True
dir b12edc2408fa1263 matched True
dir c5ae2c27e5f07634 matched True
dir d48f07ecdd30cb6f matched True

```

## 全corpusの構造探針（内容不転記・正準位置のtype語彙とtimestamp・間隔分布の件数のみ）

- argv：`[".venv/bin/python3", "-c", "import json\nimport re\nfrom datetime import datetime\nfrom pathlib import Path\nroot = Path('/Users/keno/.reviewcompass3/projects/reviewcompass3/development/sensitive/eventual-preservation/raw')\nTOKEN = re.compile(r'^[A-Za-z0-9_.\\-]{1,40}$')\ndef vocab_add(vocab, value):\n    if isinstance(value, str) and TOKEN.match(value):\n        key = value\n    else:\n        key = '__nonconforming__'\n    if key not in vocab and len(vocab) >= 1000:\n        key = '__overflow__'\n    vocab[key] = vocab.get(key, 0) + 1\ndef top_items(vocab):\n    return sorted(vocab.items(), key=lambda kv: (-kv[1], kv[0]))[:20]\nfor system_dir in sorted(p for p in root.iterdir() if p.is_dir()):\n    files = sorted(system_dir.rglob('*.jsonl'))\n    line_count = 0\n    json_ok = 0\n    typed_byte_marker = 0\n    top_level = {}\n    content_types = {}\n    payload_types = {}\n    ts_present = 0\n    ts_iso_ok = 0\n    ts_naive = 0\n    pairs = 0\n    negative = 0\n    buckets = [0, 0, 0, 0]\n    sums = [0.0, 0.0, 0.0, 0.0]\n    for item in files:\n        prev = None\n        with open(item, 'rb') as stream:\n            for raw_line in stream:\n                line_count += 1\n                typed_byte_marker += raw_line.count(b'\\x22type\\x22:\\x22tool_use\\x22')\n                try:\n                    doc = json.loads(raw_line)\n                except ValueError:\n                    continue\n                if not isinstance(doc, dict):\n                    continue\n                json_ok += 1\n                vocab_add(top_level, doc.get('type'))\n                message = doc.get('message')\n                if isinstance(message, dict) and isinstance(message.get('content'), list):\n                    for block in message['content']:\n                        if isinstance(block, dict):\n                            vocab_add(content_types, block.get('type'))\n                payload = doc.get('payload')\n                if isinstance(payload, dict):\n                    vocab_add(payload_types, payload.get('type'))\n                timestamp = doc.get('timestamp')\n                if timestamp is None:\n                    continue\n                ts_present += 1\n                try:\n                    moment = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))\n                except ValueError:\n                    continue\n                if moment.tzinfo is None:\n                    ts_naive += 1\n                    continue\n                ts_iso_ok += 1\n                if prev is not None:\n                    gap = (moment - prev).total_seconds()\n                    pairs += 1\n                    if gap < 0:\n                        negative += 1\n                    else:\n                        index = 0 if gap <= 60 else 1 if gap <= 600 else 2 if gap <= 3600 else 3\n                        buckets[index] += 1\n                        sums[index] += gap\n                prev = moment\n    print('system', system_dir.name)\n    print(' files', len(files), 'lines', line_count, 'json_ok', json_ok)\n    print(' typed_byte_marker', typed_byte_marker)\n    print(' top_level_type', top_items(top_level))\n    print(' message_content_type', top_items(content_types))\n    print(' payload_type', top_items(payload_types))\n    print(' timestamp_present', ts_present, 'iso_ok', ts_iso_ok, 'naive', ts_naive)\n    print(' gap_pairs', pairs, 'negative', negative)\n    print(' gap_buckets_le60_le600_le3600_gt3600', buckets, [round(total) for total in sums])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：9.242s
- 完全性：二重実行一致

- stdout：

```text
system b12edc2408fa1263
 files 1152 lines 971101 json_ok 971101
 typed_byte_marker 0
 top_level_type [('event_msg', 534725), ('response_item', 394179), ('turn_context', 18510), ('session_meta', 14568), ('world_state', 4550), ('inter_agent_communication_metadata', 2934), ('compacted', 1635)]
 message_content_type []
 payload_type [('token_count', 210273), ('agent_message', 119230), ('agent_reasoning', 108245), ('message', 104757), ('reasoning', 79004), ('function_call', 57846), ('function_call_output', 57846), ('custom_tool_call', 45841), ('custom_tool_call_output', 45841), ('__nonconforming__', 42197), ('patch_apply_end', 26587), ('task_started', 18217), ('user_message', 17531), ('task_complete', 17358), ('thread_settings_applied', 10608), ('sub_agent_activity', 6428), ('context_compacted', 1635), ('turn_aborted', 791), ('web_search_end', 555), ('mcp_tool_call_end', 196)]
 timestamp_present 971101 iso_ok 971101 naive 0
 gap_pairs 969949 negative 0
 gap_buckets_le60_le600_le3600_gt3600 [963960, 4854, 831, 304] [1390459, 771168, 1120974, 13150223]
system c5ae2c27e5f07634
 files 19 lines 11898 json_ok 11898
 typed_byte_marker 0
 top_level_type [('event_msg', 7741), ('response_item', 3581), ('turn_context', 238), ('session_meta', 139), ('inter_agent_communication_metadata', 120), ('world_state', 57), ('compacted', 22)]
 message_content_type []
 payload_type [('token_count', 2476), ('agent_reasoning', 2270), ('agent_message', 2102), ('message', 1013), ('reasoning', 962), ('custom_tool_call', 653), ('custom_tool_call_output', 653), ('__nonconforming__', 576), ('patch_apply_end', 227), ('task_started', 220), ('task_complete', 209), ('user_message', 118), ('thread_settings_applied', 110), ('sub_agent_activity', 95), ('function_call', 90), ('function_call_output', 90), ('context_compacted', 22), ('turn_aborted', 7), ('mcp_tool_call_end', 5)]
 timestamp_present 11898 iso_ok 11898 naive 0
 gap_pairs 11879 negative 0
 gap_buckets_le60_le600_le3600_gt3600 [11789, 59, 21, 10] [12264, 13617, 28728, 123066]
system d48f07ecdd30cb6f
 files 562 lines 130943 json_ok 130943
 typed_byte_marker 28760
 top_level_type [('assistant', 55362), ('user', 33103), ('attachment', 11955), ('queue-operation', 7509), ('last-prompt', 6956), ('custom-title', 5469), ('ai-title', 4322), ('system', 3225), ('mode', 2613), ('result', 210), ('started', 210), ('agent-name', 4), ('file-history-snapshot', 3), ('permission-mode', 2)]
 message_content_type [('tool_result', 28778), ('tool_use', 28760), ('thinking', 16722), ('text', 10049), ('image', 165), ('fallback', 17), ('document', 1)]
 payload_type []
 timestamp_present 111154 iso_ok 111154 naive 0
 gap_pairs 110594 negative 3567
 gap_buckets_le60_le600_le3600_gt3600 [101693, 4693, 527, 114] [560625, 821247, 658524, 4087434]

```

## 装置・保全実装・試験のdigest固定

- argv：`["shasum", "-a", "256", "tools/evaluation/operational_metrics.py", "tests/test_operational_metrics.py", "tools/session_logs/record_run.py", "tools/session_logs/eventual_preservation.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.018s
- 完全性：二重実行一致

- stdout：

```text
d0ad1b4d857a1a8bf9bf8aa6fb0a571c5d8275cf74af81930096f71ae2ace9ff  tools/evaluation/operational_metrics.py
40d35750acd41653ec7401bfb73ce2da1623c2aa73ff6e565cca50120728ca18  tests/test_operational_metrics.py
89c45318488cfcba9583f3626c3104803ea5b07d1f9a4284541cd350ff18e1c3  tools/session_logs/record_run.py
4fa0d87173c094a766c8d2f6021a5a9db17920b32dfdb7acb9b879601ceb5342  tools/session_logs/eventual_preservation.py

```

## operational_metricsの参照元（Pythonのみ・機械列挙）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nhits = []\nfor base in ('tools', 'tests'):\n    for path in sorted(Path(base).rglob('*.py')):\n        try:\n            text = path.read_text(encoding='utf-8')\n        except (OSError, UnicodeDecodeError):\n            continue\n        if 'operational_metrics' in text:\n            hits.append(path.as_posix())\nfor hit in hits:\n    print(hit)\nprint('total', len(hits))\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.082s
- 完全性：二重実行一致

- stdout：

```text
tests/test_operational_metrics.py
total 1

```
