# Layout Baseline v3 Project-first GREEN Evidence v1

- Evidence ID：`RC3-LAYOUT-BASELINE-V3-PROJECT-FIRST-GREEN-2026-08-04-V1`
- status：`verified / candidate_green / human_approval_pending`
- scope：project-first runtime rootのcandidateと最小resolver。現行v2の正本は変更しない。

## Fixed inputs

- RED Evidence：`records/development/2026-08-04-layout-baseline-v3-project-first-red-evidence-v1.md`
- candidate：`records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`、SHA-256
  `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38`
- implementation：`tools/layout/baseline.py`、SHA-256
  `6d00c3053da820cd694a0c4b47d5e5f1b632f00d83e81691f99060626bc94cb7`
- Acceptance Test：`tests/test_project_runtime_layout.py`、SHA-256
  `255d3aadd102093849001cdd3b8e0716a2211096680bee281ce4443ed171aa4a`

## Implemented boundary

- `resolve_project_runtime_layout`はabsolute runtime root、Project Manifest由来の明示project ID、
  `development`／`runtime` profileから、`config/`およびprofile内の6 rootを副作用なしで解決する。
- `initialize_project_runtime_layout`は要求されたroot種別だけを作成する。Unixではruntime rootと
  `sensitive/`を`0700`へ固定する。Windows ACLの実装は後続のplatform native operationに残す。
- deployment package検査はv3だけで`.reviewcompass3/`の同梱を拒否する。
- v1/v2の`resolve_layout`と既存の`stable`／`development` roleは変更していない。v3のprofileは
  project-first runtime配置専用の新しい概念である。

## GREEN verification

```text
.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py -q
```

結果：`7 passed`。

```text
.venv/bin/python3 -m pytest tests/test_layout_baseline.py -q
```

結果：`12 passed`。v2互換境界を確認した。

```text
.venv/bin/python3 -m pytest -q
```

結果：`664 passed in 3.71s`、Python `3.9.6`、pytest `8.4.2`、fallback `false`。

## Human approval required

candidateをcurrent baselineへ昇格するには、v3のproject-first配置、profile名、Unix権限、
package除外、および「既存dataを自動migrationしない」方針をHumanが承認する必要がある。承認前は、
実home directoryへの初期化およびWork 4Aのactual Source Snapshot保存を行わない。
