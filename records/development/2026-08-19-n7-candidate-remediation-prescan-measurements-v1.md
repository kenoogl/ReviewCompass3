# 測定ブロック：N7未充足候補4件の是正 事前走査の実測

- captured_at：2026-08-19T06:29:30+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-19-n7-candidate-remediation-prescan-commands-v1.json`（SHA-256 `b10bf5ce6b7f42cf00e4cad2fe67b85d68a8edf5d2d14c5ad38dd3c61140a010`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 4候補の規定形とのずれ・出所束縛の生存（機械診断）

- argv：`[".venv/bin/python3", "-c", "import hashlib\nimport json\nfrom pathlib import Path\ntargets = [\".reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json\"]\nconfig = json.load(open('config/development-issue-resolution-pilot-v3.json', encoding='utf-8'))\nexpected = set(config['record_fields']['improvement_candidate'])\nallowed_classifications = set(config['classification_candidates'])\nallowed_routes = set(config['dispositions'])\nfor target in targets:\n    document = json.loads(Path(target).read_text(encoding='utf-8'))\n    print(Path(target).name)\n    print('  extra_fields', sorted(set(document) - expected))\n    print('  missing_fields', sorted(expected - set(document)))\n    source = document.get('source_identity', {})\n    print('  source_identity_keys', sorted(source))\n    print('  invalid_classifications', sorted(set(document.get('classification_candidates', [])) - allowed_classifications))\n    print('  invalid_routes', sorted(set(document.get('route_candidates', [])) - allowed_routes))\n    source_path = Path(str(source.get('path', '')))\n    exists = source_path.is_file()\n    print('  source_exists', exists)\n    if exists:\n        digest = hashlib.sha256(source_path.read_bytes()).hexdigest()\n        print('  source_sha256_matches', digest == source.get('sha256'))\n    refs = document.get('evidence_refs', [])\n    for reference in refs:\n        ref_path = Path(str(reference.get('path', '')))\n        ok = ref_path.is_file() and hashlib.sha256(ref_path.read_bytes()).hexdigest() == reference.get('sha256')\n        print('  evidence_ref', ref_path.name, 'binding_ok', ok)\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.021s
- 完全性：二重実行一致

- stdout：

```text
ic-contract-014-canonical-sequence-gaps-001--v1.json
  extra_fields ['related_candidates']
  missing_fields []
  source_identity_keys ['kind', 'path', 'section', 'sha256', 'source_id', 'source_version']
  invalid_classifications ['documentation']
  invalid_routes []
  source_exists True
  source_sha256_matches True
  evidence_ref 2026-08-18-rq2-adjudication-and-byproducts-v2.md binding_ok True
ic-launch-metrics-acceptance-title-001--v1.json
  extra_fields ['related_candidates']
  missing_fields []
  source_identity_keys ['kind', 'path', 'section', 'sha256', 'source_id', 'source_version']
  invalid_classifications ['documentation']
  invalid_routes []
  source_exists True
  source_sha256_matches True
  evidence_ref 2026-08-18-rq2-adjudication-and-byproducts-v2.md binding_ok True
ic-session-log-exit-code-doc-drift-001--v1.json
  extra_fields ['related_candidates']
  missing_fields []
  source_identity_keys ['kind', 'path', 'section', 'sha256', 'source_id', 'source_version']
  invalid_classifications ['documentation']
  invalid_routes []
  source_exists True
  source_sha256_matches True
  evidence_ref 2026-08-18-rq2-adjudication-and-byproducts-v2.md binding_ok True
ic-session-log-exit-code-vocabulary-001--v1.json
  extra_fields ['related_candidates']
  missing_fields []
  source_identity_keys ['kind', 'path', 'section', 'sha256', 'source_id', 'source_version']
  invalid_classifications ['design']
  invalid_routes []
  source_exists True
  source_sha256_matches True
  evidence_ref 2026-08-18-rq2-adjudication-and-byproducts-v2.md binding_ok True

```

## 4候補の登録履歴（初回commit・改版数）

- argv：`[".venv/bin/python3", "-c", "import subprocess\ntargets = [\".reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json\", \".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json\"]\nfor target in targets:\n    completed = subprocess.run(\n        ['git', 'log', '--format=%h %ad', '--date=short', '--reverse', '--', target],\n        capture_output=True,\n        text=True,\n    )\n    lines = completed.stdout.strip().splitlines()\n    first = lines[0] if lines else '(履歴なし)'\n    print(target.rsplit('/', 1)[-1], '初回commit', first, '改版数', len(lines))\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.071s
- 完全性：二重実行一致

- stdout：

```text
ic-contract-014-canonical-sequence-gaps-001--v1.json 初回commit 3b76b97 2026-08-18 改版数 1
ic-launch-metrics-acceptance-title-001--v1.json 初回commit 3b76b97 2026-08-18 改版数 1
ic-session-log-exit-code-doc-drift-001--v1.json 初回commit 3b76b97 2026-08-18 改版数 1
ic-session-log-exit-code-vocabulary-001--v1.json 初回commit 3b76b97 2026-08-18 改版数 1

```

## N7の現在状態（是正前RED・exit 1が現状）

- argv：`[".venv/bin/python3", "-c", "import subprocess\nresult = subprocess.run(\n    ['.venv/bin/python3', '-m', 'pytest', '-q',\n     'tests/test_issue_intake_v4_single_candidate.py::test_n7_all_candidate_records_validate_or_are_allowlisted'],\n    capture_output=True,\n    text=True,\n)\nprint('exit', result.returncode)\nprint(result.stdout.strip().splitlines()[-1].rsplit(' in ', 1)[0])\n"]`
- 実行体：.venv/bin/python3
- exit：0・elapsed：0.145s
- 完全性：二重実行一致

- stdout：

```text
exit 1
1 failed

```

## 対象4候補・allowlist・検証器・試験のdigest固定

- argv：`["shasum", "-a", "256", ".reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json", ".reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json", ".reviewcompass/workflow/improvement-candidates/historical-allowlist-v1.json", "config/development-issue-resolution-pilot-v3.json", "tools/development/issue_resolution_pilot.py", "tests/test_issue_intake_v4_single_candidate.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.027s
- 完全性：二重実行一致

- stdout：

```text
947a2791b6d7e054cd30f0a31470bdbb6fb6753bed03d2108fed5e9c48961f44  .reviewcompass/workflow/improvement-candidates/ic-contract-014-canonical-sequence-gaps-001--v1.json
00d67789b0df74ac9cef3d71d146ece251a7288afd99d382858361ccd86ca86e  .reviewcompass/workflow/improvement-candidates/ic-launch-metrics-acceptance-title-001--v1.json
4fbc1b436327039ae2e8c5835aa4a01590dae62f445b4095ca9403a135cd96ec  .reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-doc-drift-001--v1.json
21f75f05cd6b60ee0cfcdd47ab44fdd9edc4c0eb9ac0e5a9889df027bcfaa899  .reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json
25bf17ae9d53a5a01f370b477c001d6e040a7e1e645e00cb25dbd4caa0043c0a  .reviewcompass/workflow/improvement-candidates/historical-allowlist-v1.json
f3130d03805cd78e1622cc20f64df2062c21ba57ea460ef9f9766d132f92d7b9  config/development-issue-resolution-pilot-v3.json
71e8daebe1a991bde307b0ab9498082218cfef9a6cab6661fa43cb093821f6ef  tools/development/issue_resolution_pilot.py
86f0b09864a0def0ed633aa444c1f5317df72d07734e6ac55289d5212bc258e2  tests/test_issue_intake_v4_single_candidate.py

```
