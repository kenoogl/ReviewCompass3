# 測定ブロック：計画JSON writer（対策2）受入確認の実測

- captured_at：2026-08-18T21:05:12+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-plan-writer-evidence-commands-v1.json`（SHA-256 `826f0f94e2b2bace833e2674b53c83449211e8cda54090b79764ce62a6f11935`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## writer試験の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nr = subprocess.run(['.venv/bin/python3', '-m', 'pytest', 'tests/test_reuse_search_plan.py', '-q'], capture_output=True, text=True)\nlast = r.stdout.strip().splitlines()[-1]\nprint('exit', r.returncode)\nprint(last.rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.172s
- 完全性：二重実行一致

- stdout：

```text
exit 0
6 passed

```

## 検索側保護試験の単独実行（決定的射影）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nr = subprocess.run(['.venv/bin/python3', '-m', 'pytest', 'tests/test_formal_code_reuse_search.py', '-q'], capture_output=True, text=True)\nlast = r.stdout.strip().splitlines()[-1]\nprint('exit', r.returncode)\nprint(last.rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.941s
- 完全性：二重実行一致

- stdout：

```text
exit 0
12 passed

```

## committed全計画の一括verify

- argv：`[".venv/bin/python3", "-c", "import json, io, contextlib\nfrom pathlib import Path\nfrom tools.development import reuse_search_plan\nok = 0\ntotal = 0\nfor p in sorted(Path('records/development').glob('*.json')):\n    try:\n        d = json.loads(p.read_text(encoding='utf-8'))\n    except ValueError:\n        continue\n    if not isinstance(d, dict) or d.get('record_kind') != 'formal_code_reuse_search_plan':\n        continue\n    total += 1\n    buf = io.StringIO()\n    with contextlib.redirect_stdout(buf):\n        code = reuse_search_plan.run(('verify', '--plan', str(p), '--project-root', '.'))\n    verdict = json.loads(buf.getvalue())\n    print(p.name, verdict['status'], code)\n    ok += 1 if code == 0 else 0\nprint(f'plans={total} ok={ok}')\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.053s
- 完全性：二重実行一致

- stdout：

```text
2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v2.json ok 0
2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v3.json ok 0
2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v4.json ok 0
2026-08-15-safe-storage-formal-code-reuse-search-plan-v1.json ok 0
2026-08-17-claude-subagent-backend-reuse-search-plan-v1.json ok 0
2026-08-17-free-text-request-type-reuse-search-plan-v1.json ok 0
2026-08-17-launch-metrics-reuse-search-plan-v1.json ok 0
2026-08-17-reviewer-bridge-reuse-search-plan-v1.json ok 0
2026-08-17-rq1-apparatus-reuse-search-plan-v1.json ok 0
2026-08-17-rq2-apparatus-reuse-search-plan-v1.json ok 0
2026-08-17-session-log-prefix-interpretation-reuse-search-plan-v1.json ok 0
2026-08-17-session-log-record-run-reuse-search-plan-v1.json ok 0
2026-08-17-vertical-a-request-builder-reuse-search-plan-v1.json ok 0
2026-08-18-cli-defaults-rollout-plan-v1.json ok 0
2026-08-18-measurement-block-integrity-guard-plan-v1.json ok 0
2026-08-18-measurement-block-plan-v1.json ok 0
2026-08-18-operational-metrics-reuse-search-plan-v1.json ok 0
2026-08-18-operational-metrics-v2-reuse-search-plan-v1.json ok 0
2026-08-18-placement-root-resolution-reuse-search-plan-v1.json ok 0
2026-08-18-plan-writer-plan-v1.json ok 0
2026-08-18-reuse-search-cli-defaults-plan-v1.json ok 0
2026-08-18-session-log-exit-code-reuse-search-plan-v1.json ok 0
plans=22 ok=22

```

## 変更・新設fileのdigest固定

- argv：`["shasum", "-a", "256", "tools/development/reuse_search_plan.py", "tests/test_reuse_search_plan.py", "docs/development/prompts/scope-prescan-run.md"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
2708ad14318a2136c4f5bb5a0ca5e7b15b4f48bf663e0278cca8eb5286073b85  tools/development/reuse_search_plan.py
30f80b2449a352e77288b52f69d24e6e5440c5986b6d16ed604bf5a3042282bd  tests/test_reuse_search_plan.py
fb5b8383731f031414e6e4cf56394cb557e5e0e130c70a1609ddc3d95589b816  docs/development/prompts/scope-prescan-run.md

```
