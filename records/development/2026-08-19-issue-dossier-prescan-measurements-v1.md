# 測定ブロック：issue実態調書tool 事前走査の実測

- captured_at：2026-08-19T11:54:59+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-issue-dossier-prescan-commands-v1.json`（SHA-256 `af0fff3174dc3cd9b0a017901ad7d39740b30e24ed5ccd2068da9ddeb0be31cf`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 新設名の衝突なしの機械確認

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfor candidate in (\n    'tools/development/issue_reconciliation_dossier.py',\n    'tests/test_issue_reconciliation_dossier.py',\n):\n    print(candidate, 'exists', Path(candidate).exists())\nhits = []\nfor base in ('tools', 'tests'):\n    for path in sorted(Path(base).rglob('*.py')):\n        try:\n            text = path.read_text(encoding='utf-8')\n        except (OSError, UnicodeDecodeError):\n            continue\n        if 'reconciliation_dossier' in text:\n            hits.append(path.as_posix())\nprint('name_hits', hits)\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.033s
- 完全性：二重実行一致

- stdout：

```text
tools/development/issue_reconciliation_dossier.py exists False
tests/test_issue_reconciliation_dossier.py exists False
name_hits []

```

## TODOのissue言及行の現形（拘束flagの対象構造）

- argv：`[".venv/bin/python3", "-c", "from pathlib import Path\nfor line in Path('TODO_NEXT_SESSION.md').read_text(encoding='utf-8').splitlines():\n    if 'ISSUE-' in line:\n        print(line[:160])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.018s
- 完全性：二重実行一致

- stdout：

```text
- `ISSUE-TEST-GROWTH-STATE-PINNING-001`：`registered / 第3段完了・条件付き再開待ち`、影響：次縦切りの選択・着手を妨げない持ち越し負債である、次：Issue状態を変更せず、状態固定試験の変更・削除または別途承認されたWork 8測定の前にだけ対象限定で再開する

```

## 台帳の現況（一括検証・exit 0が前提）

- argv：`[".venv/bin/python3", "-m", "tools.development.workflow_ledger_verify"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.052s
- 完全性：二重実行一致

- stdout：

```text
{"accounted":{"allowlist":1,"decision":7,"validator":13},"candidate_total":21,"decision_total":53,"findings":[],"issue_states":{"registered":5,"resolved":3},"issue_total":8,"status":"passed"}

```

## 流用部品のdigest固定

- argv：`["shasum", "-a", "256", "tools/development/issue_intake_v4.py", "tools/development/workflow_ledger_verify.py", "tools/development/issue_state_transition.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
42b797ad9e1aef81620a94a08c279a99c8daa7924329b44a54da1024cc9f4fde  tools/development/issue_intake_v4.py
81a8a72b56edaced0901c57263319c9dcac1bc2e581c0f6d9837cfa65b0b5174  tools/development/workflow_ledger_verify.py
e2ec4c3a3c4d6926d55c30cdb14e62de4b0047abf30060be405aca52d5f66526  tools/development/issue_state_transition.py

```
