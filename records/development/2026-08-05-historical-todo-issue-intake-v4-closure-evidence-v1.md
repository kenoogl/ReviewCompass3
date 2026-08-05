# Issue Intake V4 検証閉鎖Evidence v1

- 対象：Issue Intake V4の複数Issue受付に関する実地検証
- 承認record：`records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md`、SHA-256 `019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-approve-and-close-v4-issue-intake.md`

旧Issue Resolution早期Pilotのbootstrapはすでに閉鎖済みである。ここで閉じるのは、その後に追加した
**V4複数Issue受付の実地検証**である。

## 1. 受入testのGREEN

V4設計§5のI1〜I9（正常例）とJ1〜J16（負例）はtestで固定済みであり、その後に追加した
Human triage永続化のK1〜K7、Issue永続化のL1〜L6も合格している。

| Evidence | SHA-256 |
| --- | --- |
| `records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md` | `28809b220e8e5b16f3f643c8994ea9bdeb73ac83d3e506daaea6baceb751e75f` |
| `records/development/2026-08-05-v4-human-triage-persistence-green-evidence-v1.md` | `41fcbbbd6acc278055dd3e43e64fcb0c603627319eae1fb13b853262bda305d7` |
| `records/development/2026-08-05-v4-issue-persistence-green-evidence-v1.md` | `3ae17b4b5828429ee8c7f1b6dfbc3b80d9439da4bace685542cee3845640b731` |

対象test file：`tests/test_issue_intake_v4.py`、SHA-256 `0d9b3f0356294cf83cc80848675c1eb7e2d602afebd3f44b21109bcb58493bbd`
（`38 passed`）。全testのreceiptは`records/development/2026-08-05-historical-todo-issue-intake-v4-closure-test-receipt-v1.json`。

## 2. 候補bundleの不変性

| 項目 | 値 |
| --- | --- |
| path | `records/development/2026-08-05-historical-todo-intake-candidates-v1.json` |
| SHA-256 | `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` |
| 候補数 | 41 |
| `human_fields` | 全件`null` |
| `promotion_status` | `none` |

生成commit`3ef8759`以降、このfileを変更したcommitは無い。Humanの判断はbundleへ書き戻さず、
別recordとして保存している。

## 3. 有効decision 41件、未判断0件、競合0件

`validate_triage_decision_repository()`は有効decision 41件を返し、競合は無い。
候補bundleの41候補のうち、有効decisionが無いものは0件である。

| disposition | 件数 |
| --- | --- |
| `defer` | 10 |
| `dependency` | 3 |
| `historical_completed` | 12 |
| `issue_resolution` | 3 |
| `reject` | 13 |

各decisionのIDとfile digestは承認recordの表に固定してある。

## 4. V4 Issue 3件、active Issue 0件

| issue ID | state | path | file SHA-256 |
| --- | --- | --- | --- |
| `ISSUE-HTC-66C3E6CA` | `registered` | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |
| `ISSUE-HTC-BEB5E0BD` | `registered` | `.reviewcompass/workflow/issues-v4/issue-htc-beb5e0bd--v1.json` | `a4a1511e609005193a3d127080a3eabf4f56a67529c5bd9b4e0f55b467422d62` |
| `ISSUE-HTC-C9F6C917` | `registered` | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |

3件とも`registered`であり、参照するtriage decisionは`blocking: false`である。
`count_active_issues()`は0を返す。`in_progress`のIssueは無い。

## 5. 設計・config・validator・testと承認recordの参照関係

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` | `8475cd94b449e0709eb97e6d487b86cceef86e0307b3bbb7e78351d8f43147a9` |
| `config/development-issue-resolution-pilot-v4.json` | `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e` |
| `tools/development/issue_intake_v4.py` | `7a1d557e82acd6554c3e137345f02ba476cbf448184a9a0348dca6beec26e27a` |
| `tests/test_issue_intake_v4.py` | `0d9b3f0356294cf83cc80848675c1eb7e2d602afebd3f44b21109bcb58493bbd` |

参照の向きは次のとおりである。

- 各V4 Issueは`triage_decision_ref`で判断recordのpath、file SHA-256、content digestを指す。
- 各判断recordは`candidate_ref`で候補bundleのpath、SHA-256、schema version、候補ID、
  候補content digestを指す。
- 検証時はいずれも実fileから読み直して再確認する。参照先が変われば検証は失敗する。
- 承認record`records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md`は、上記すべてのpathと実digestを一箇所に固定している。

## 6. 残余riskと後続

- 3正式Issue（`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`、`ISSUE-HTC-66C3E6CA`）は未着手のままである。
  Plan化は、Humanが必要と判断した時点で一件ずつ決める。まとめてPlan化しない。
- V4は開発用・暫定の限定機能である。正式製品機能へ拡張しない。正式製品schema、UI、automation、
  Work 8評価は承認範囲外のままである。
- `pilot_mode: development_only_provisional`を維持する。
- 候補bundleと41件の判断record、3件のIssueは履歴として保持し、上書き・削除しない。
