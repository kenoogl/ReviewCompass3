# Claude → Codex：V4 Issue永続化と会話記録方針候補のtriage 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-v4-issue-persistence-and-session-policy-triage.md`

指示の全項目を完了した。設計上の矛盾や既存V1／V4の互換性破壊は生じていない。

## commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 実装 | `0a64a081290e04ad75d5578999d3d2c205509faa` | V4 Issue永続化のschema・config・validator・受入test・RED／GREEN Evidenceとreceipt |
| Human承認recordとIssue record | `f268b2a00fc0729cfe1f43d3b88286bfdb5d82da` | 承認済み四decision、正式Issue一件、TODO更新、作成後の全test receipt |

各commit後に追跡fileのworktreeがcleanであることを確認した。未追跡のまま残っているのは、
指示によりcommitへ混ぜないsession-handoffsの完了報告6件のみである（本報告を含む）。

## RED／GREEN結果

公式Test runner（`tools/development/policy_test_runner.py`、suite `full`、Python 3.9.6、
pytest 8.4.2、fallback false）で実行した。

| 段階 | receipt | status | 結果 |
| --- | --- | --- | --- |
| RED | `records/development/2026-08-05-v4-issue-persistence-red-test-receipt-v1.json` | `failed`／exit 1 | `3 failed, 809 passed, 3 errors` |
| GREEN（実装後） | `records/development/2026-08-05-v4-issue-persistence-green-test-receipt-v1.json` | `passed`／exit 0 | `815 passed` |
| decision／Issue作成後 | `records/development/2026-08-05-v4-issue-persistence-decisions-test-receipt-v1.json` | `passed`／exit 0 | `815 passed` |

追加した受入testはL1〜L6の6件で、指示§2の6条件に一対一で対応する。実装中に緩めていない。
既存809testは変更していない。TODOの最終更新後にも全testを再実行し、`815 passed`を確認した
（このrunはreceiptを上書きしないため、receiptは上表の3件のままである）。

Evidence：

- RED：`records/development/2026-08-05-v4-issue-persistence-red-evidence-v1.md`
- GREEN：`records/development/2026-08-05-v4-issue-persistence-green-evidence-v1.md`

## 実装したもの

### V4専用Issue directoryと永続schema

- `directories.issue_record_v2`：`.reviewcompass/workflow/issues-v4`
- `issue_record_v2`：`schema_version: 2`、`issue_id_prefix: ISSUE`、`initial_state: registered`、
  `record_fields`（10個）

`load_config()`は、V4 Issue directoryが未設定の場合、旧Issue directoryと同一の場合、
schema versionが食い違う場合、初期stateが未知または作業中stateの場合を`config_invalid`で拒否する。

file名は`{issue_id小文字}--v{issue_version}.json`として決定的に導出する。`candidate_ref`は
bundleのpath・SHA-256・schema version・candidate ID・candidate content digestを、
`triage_decision_ref`はdecisionのID・version・path・file SHA-256・content digestを持ち、
検証時に実fileから再確認する。参照先decisionは単体検証したうえで、candidate参照の一致、
昇格承認、issue IDの一致まで確認する。

拒否する条件：未知field、field欠落、schema version不一致（旧Issueを含む）、ID・version・
作成時刻の形式不正、未知state、record path不一致、decision pathの絶対path／`..`脱出、
decision fileの不存在・SHA不一致、decisionのID／version／content digest／candidate参照／
昇格承認／issue IDの不一致、bundle SHA不一致、candidate不存在、candidate digest不一致、
content digest不一致。

`validate_v4_issue_repository()`はV4 directoryだけを走査し、issue IDの重複と、同一candidateへの
有効Issue重複（`v4_issue_duplicate_for_candidate`）を拒否する。旧Issue directoryは読まない。

`build_v4_issue_record()`は既存の`promote_candidate_from_decision()`を権限の関門として呼ぶ。
候補bundleは読むだけで書き換えない。初期stateは`registered`で、`in_progress`へは進めない。

## 四decision ID

| decision ID | candidate ID | 判断 | disposition |
| --- | --- | --- | --- |
| `DEC-HTC-045A8FB5` | `HTC-045A8FB5` | 未解決false／再発false／影響 not_applicable／優先 not_applicable／昇格false | `historical_completed` |
| `DEC-HTC-4ED2C5B1` | `HTC-4ED2C5B1` | 未解決true／再発true／影響 medium／優先 low／昇格false | `dependency` |
| `DEC-HTC-BEB5E0BD` | `HTC-BEB5E0BD` | 未解決true／再発true／影響 high／優先 high／昇格true | `issue_resolution` |
| `DEC-HTC-CD984CD0` | `HTC-CD984CD0` | 未解決true／再発true／影響 high／優先 low／昇格false | `dependency` |

四件とも`blocking: false`、`decision_version: 1`、`supersedes: null`、
`decided_at: 2026-08-05T13:17:35+09:00`である。

content digest：

- `DEC-HTC-045A8FB5`：`17236725f5f3f477480abef1e5ebabafb705fbc0749fdb9949f0dd12a920dfe0`
- `DEC-HTC-4ED2C5B1`：`94f292c44acab60e61887bbba2328ce7c508bf08a522fb7dc91238323ef45911`
- `DEC-HTC-BEB5E0BD`：`bf372984bb1a85b146802c721ae983362107f73aa2cc440fa54a0e450d74e20d`
- `DEC-HTC-CD984CD0`：`6c9a116068b374d758d99668034721d310be20e39a082766a9cb2154571367d7`

`HTC-4ED2C5B1`と`HTC-CD984CD0`のnext actionは、それぞれ「正式Issueの保存方針決定後に自動化の
要否を再判定」「2026-09-03または正式IssueのPlan作成時に再確認」とした。
`HTC-BEB5E0BD`だけが`issue_promotion: {"approved": true, "issue_id": "ISSUE-HTC-BEB5E0BD"}`である。

## V4 Issueのpath／digest

| 項目 | 値 |
| --- | --- |
| path | `.reviewcompass/workflow/issues-v4/issue-htc-beb5e0bd--v1.json` |
| issue ID | `ISSUE-HTC-BEB5E0BD` |
| state | `registered`（active Issue数は0） |
| problem | 生会話記録の保存期間、削除、application-layer暗号化、backupの方針が未決定である。 |
| content digest | `f207a48da548f2fc224f9bd975836e90f823c00d1f3437ee90a490df73ae210c` |
| file SHA-256 | `a4a1511e609005193a3d127080a3eabf4f56a67529c5bd9b4e0f55b467422d62` |

nonblockingは真偽値fieldではなく、Issueが`registered`のままであることと、参照する
triage decisionの`blocking: false`で表している。Plan、Work、scheduler、hook、暗号化、backup、
retention変更、実会話の追加captureはいずれも作っていない。

## 旧Issue不変確認

- 旧Issue directory`.reviewcompass/workflow/issues/`は`issue-pilot-todo-growth-001--v1.json`の1件のままである。
- 同directoryのGit履歴の最新commitは`ccd804b`であり、今回の2commitは触れていない。
- 旧PilotのvalidatorはそのIssueを従来どおり通す（`ISSUE-PILOT-TODO-GROWTH-001`）。
- V4 validatorは旧Issueを`v4_issue_schema_version_unsupported`として扱い、V4語彙で再判定しない。
- 旧Pilotのconfig、V1 decision、V1 Issue、旧testは変更していない。

## 候補bundle不変確認

- SHA-256は作業前後で`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま変わらない。
- 候補41件すべての`human_fields`は`null`のままである（機械確認済み）。
- `promotion_status`は`none`のままである。
- Git履歴上、bundle fileを変更したcommitは生成時の`3ef8759`だけである。

## その他の検証

- V4 decision集合検証：有効decisionは8候補ぶん（今回の4件と前作業の4件）で競合なし。
- V4 Issue集合検証：有効Issueは`HTC-BEB5E0BD`の1件、active Issueは0件。
- TODOの参照digest整合（26参照）とcommit安定Git節はいずれも合格。TODOは8,346 bytesで上限内。
- TODOのactive ID projectionは`ISSUE-PILOT-TODO-GROWTH-001`の1件のままで、
  `ISSUE-HTC-BEB5E0BD`はactive Issueとして数えていない。
- `git diff --check`は各commit前後で合格。

## 未実施事項（指示どおり行っていないこと）

- 他の33候補の判断、Issue、Plan、Workの作成・変更：行っていない。
- `HTC-BEB5E0BD`のPlan化、`in_progress`への移行：行っていない。
- 旧Pilotのconfig、V1 decision、V1 Issue、旧testの変更：行っていない。
- push、PR、外部送信、scheduler／hookの有効化、暗号化・backup・retentionの実装、
  実会話の追加capture、Work 4B、Work 6A、E2以降：いずれも開始していない。
- 本完了報告はcommitに混ぜていない。
