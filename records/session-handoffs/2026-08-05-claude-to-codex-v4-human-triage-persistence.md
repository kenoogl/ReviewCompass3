# Claude → Codex：Issue Intake V4 Human triage永続化 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-v4-human-triage-persistence.md`

Humanは本実装を承認済みである。指示の全項目を完了した。停止して報告すべき設計上の矛盾や
V1互換性の破壊は生じていない（directoryの扱いについては後述の「実装中に決めた設計判断」を参照）。

## commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 実装 | `a6f6eea9799d1a6c8db2714d87763349760df476` | schema・config・validator・昇格結線・受入test・RED／GREEN Evidenceとreceipt |
| 判断record | `dd3ea755dcdd77fc361a0dc5ec40ab75f3ce6a68` | 承認済み四decision record、TODO更新、全test receipt |

各commit後にworktreeを確認した。未追跡のまま残っているのは、指示によりcommitへ混ぜない
session-handoffsの完了報告5件のみである（本報告を含む）。追跡fileの未commit変更はない。

## RED／GREEN結果

いずれも公式Test runner（`tools/development/policy_test_runner.py`、suite `full`、
Python 3.9.6、pytest 8.4.2、fallback false）で実行した。

| 段階 | receipt | status | 結果 |
| --- | --- | --- | --- |
| RED | `records/development/2026-08-05-v4-human-triage-persistence-red-test-receipt-v1.json` | `failed`／exit 1 | `7 failed, 802 passed` |
| GREEN（実装後） | `records/development/2026-08-05-v4-human-triage-persistence-green-test-receipt-v1.json` | `passed`／exit 0 | `809 passed` |
| 判断record作成後 | `records/development/2026-08-05-v4-human-triage-decisions-test-receipt-v1.json` | `passed`／exit 0 | `809 passed` |

RED時に追加した受入testはK1〜K7の7件で、指示§5の7条件に一対一で対応する。実装中に
これらのtestを緩めていない。既存802testは変更していない。

Evidence：

- RED：`records/development/2026-08-05-v4-human-triage-persistence-red-evidence-v1.md`
- GREEN：`records/development/2026-08-05-v4-human-triage-persistence-green-evidence-v1.md`

## 実装したもの

### 1. 一候補につき一つのV4 Human triage decision（schema version 2）

集約recordは作らず、既存の粒度を維持した。decision recordのfieldは15個で固定し、
それ以外は拒否する。`candidate_ref`は候補bundleと候補の両方を指紋で押さえる。

`bundle_path`、`bundle_sha256`、`bundle_schema_version`、`candidate_id`、
`candidate_content_digest`

ID規則は`DEC-<candidate_id>`（改訂や別案は`DEC-<candidate_id>-<接尾辞>`）、path規則は
`{V4 decision directory}/{decision_id小文字}--v{decision_version}.json`、content digestは
`content_digest`を除いた正準JSONのSHA-256とする。

fail-closedで拒否する条件：未知field、field欠落、schema version不一致（V1 decisionを含む）、
bundle pathの絶対pathと`..`脱出、path不一致、bundle SHA不一致、bundle schema version不一致、
candidate ID不存在、candidate digest不一致、未知disposition、昇格の整合性違反、content digest不一致。

### 2. 判断の競合と改訂

`resolve_effective_triage_decisions()`が候補ごとに有効decisionを一つだけ決める。
同一候補に`supersedes`を持たないdecisionが二件以上あれば`human_triage_decision_conflict`で拒否する。
判断を変える場合は旧recordを上書きせず、`decision_version`を上げ、`supersedes`へ旧recordの
ID・version・content digestを持たせた改訂recordとして保存する。参照先が無い、digestが古い、
versionが増えていない、同じrecordを二重に改訂している場合も拒否する。
`validate_triage_decision_repository()`がrecord単体検証と集合の競合確認の両方を行う。
V1の旧decisionはV4 directoryの外にあり、読み込みも再判定も変更もしていない。

### 3. Issue昇格の権限をdecisionへ移す

`promote_candidate_from_decision()`は、`decision_maker`が`human`、`promote_to_issue`が`true`、
`disposition`が`issue_resolution`、candidate参照がbundle digestを含めて完全一致、
同候補に競合する有効decisionが無い、のすべてを満たす場合だけIssue recordを作る。
満たさない場合は`human_triage_decision_required`または具体的な検証codeで停止する。
この関数は候補bundleの`human_fields`を読まず、書き換えもしない。
既存V1の昇格規則と既存V4の`promote_candidate_to_issue()`は変更していない。

## 四decision IDとcandidate ID

| decision ID | candidate ID | version | content digest |
| --- | --- | --- | --- |
| `DEC-HTC-14D810C7` | `HTC-14D810C7` | 1 | `1e7791b18317bc8be6492e90e679bd440a0290f3f9d0c7b2c3f1268ab730e978` |
| `DEC-HTC-1AB699F7` | `HTC-1AB699F7` | 1 | `cbda8ed448e8f883916bd05889f1f9e26b185812f5b83a786fdab58e452bd763` |
| `DEC-HTC-21C3CE46` | `HTC-21C3CE46` | 1 | `be9369e4411321fc81bc2ec859066af3b6e489d4e218c9bb7182d0c08f399c84` |
| `DEC-HTC-6ABDDC35` | `HTC-6ABDDC35` | 1 | `d642d21ea08e18f1e4f7bfad829b6b40b7b3d78ffd0b4f05f2585b3f72698ad7` |

四件とも次で共通である。

- `unresolved: false`、`recurrence: false`、`impact: not_applicable`、
  `priority: not_applicable`、`promote_to_issue: false`
- `disposition: historical_completed`、`blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`（Issue IDを持たない）
- `decided_at: 2026-08-05T12:49:31+09:00`、`decision_maker: human`、`supersedes: null`
- `rationale`に`6b68c25`（WI-006実装済み）、`b10cd09`（WI-007 snapshot保存済み）、
  `416e4e1`（TODO compaction完了済み）を平易な日本語で記載

保存path（V4 decision directory `.reviewcompass/workflow/triage-decisions-v4/`）：

- `dec-htc-14d810c7--v1.json`（file SHA-256 `022d3e25ffb3dd991cf4add659b8baf6e8a26960820a189e5c8f96343d0c3b07`）
- `dec-htc-1ab699f7--v1.json`（file SHA-256 `841139138a4216e5500801ebe8a8cf804d5bd956edb1eb416ae16119f3f327a1`）
- `dec-htc-21c3ce46--v1.json`（file SHA-256 `3a78429b82fccfa20f11dfaa1c05e6f07b5795cb7c6c0812ab924734b483c9f4`）
- `dec-htc-6abddc35--v1.json`（file SHA-256 `6c6320b220f72a49462e492e09c58b568b6b129693e95d2e435943e9932fc67d`）

## bundle不変確認

- 候補bundleのSHA-256は作業前後で `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` のまま変わらない。
- 候補41件すべての`human_fields`は`null`のままである（機械確認済み）。
- bundleの`promotion_status`は`none`のままである。
- Git履歴上、bundle fileを変更したcommitは生成時の`3ef8759`だけである。
- V1 decision directory`.reviewcompass/workflow/triage-decisions/`の履歴は`16a2b16`と`ab1fc8e`のままで、
  今回のcommitは触れていない。Issue fileは`issue-pilot-todo-growth-001--v1.json`の1件のみで増えていない。

## その他の検証

- repository集合検証：有効decisionは`HTC-14D810C7`、`HTC-1AB699F7`、`HTC-21C3CE46`、`HTC-6ABDDC35`の
  4候補ぶんで、競合なし。
- 各recordのpathがID規則と一致し、`content_digest`が再計算値と一致することを機械確認した。
- TODOの参照digest整合（`validate_todo_reference_digests`）とcommit安定Git節
  （`validate_commit_stable_git_section`）はいずれも合格。TODOは7,692 bytesで上限内。
- `git diff --check`は各commit前後で合格。

## 実装中に決めた設計判断

### V4 decisionを専用directoryへ置いた理由

既存の`tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject`は、
V1 decision directory`.reviewcompass/workflow/triage-decisions`に対して`len(decision_files) <= 1`を
固定している。同directoryへdecision fileを1件追加すると`assert 2 <= 1`で失敗することを実験で確認した。

既存testを緩めることもV1互換性を壊すことも禁止されているため、V4 schema version 2のdecisionは
V4 configで固定する専用directory`.reviewcompass/workflow/triage-decisions-v4`へ置いた。
`load_config()`は二つのdirectoryが同一である設定を`config_invalid`で拒否する。
これはV4 configがV4のdirectory規則を持つという指示§4の枠内であり、粒度は
「一候補につき一判断record」のままである。集約recordは作っていない。

### `historical_completed`を追加した理由

四候補への判断は「当時の完了済み手順の記録であり、現在解くIssueではない」である。
`reject`は「候補の内容を退ける」意味になり、当時正しく実行され完了した事実を失う。
`defer`は「後で扱う」意味になり、未処理の滞留として誤読される。`duplicate`は重複を意味するが、
四候補に重複疑いは無い。よってV4 configの`human_triage_decision_v2.dispositions`へ
`historical_completed`を追加して固定した。V1のdisposition語彙は変更していない。
この根拠はGREEN Evidenceにも記載した。

## 未実施事項（指示どおり行っていないこと）

- 残り37候補の判断、正式Issue化、Plan化、実作業開始：行っていない。
- 四候補の正式Issueへの昇格：行っていない（`issue_promotion.approved`はすべて`false`、Issue IDなし）。
- 既存候補bundle、旧Pilotのconfig／record、V1 decisionの書換え：行っていない。
- TODOの過去履歴の上書き：行っていない。TODOは更新規則どおり、現在位置・最新Evidence・
  次の一作業・blocker・Git／Test欄だけを置き換えた。
- push、PR、外部送信、CI、Work 4B、Work 6A、E2以降：行っていない。
- 本完了報告はcommitに混ぜていない。

## 補足

判断recordのcommitには、四decision recordとTODO更新に加えて、指示§作業単位3が求める
「全test」の結果receipt1件を含めた（`records/development/2026-08-05-v4-human-triage-decisions-test-receipt-v1.json`）。
実装fileやcodeは含んでいない。
