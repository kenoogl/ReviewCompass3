# Claude → Codex：Work 5A Definition Challenge実装 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-implementation.md`

**作業単位1・2・3をすべて完了し、指示どおりContract version 2のHuman承認前で停止した。**
初回Definition Challenge Runは`passed`、blocking Findingは0件である。`contract_approval`は作っていない。

## 1. commit

| 作業単位 | commit SHA | 内容 |
| --- | --- | --- |
| 事前修正 | `c2e8d4802c89aa28d356cb5538d16515b161a191` | 既存Test`test_actual_post_write_and_isolated_restore_rehearsal`の旧ID固定を廃止 |
| 1 RED | `927183bf25d7782f4a84fdbe45eb9e1357c89b91` | 受入Test 45件とRED Evidence（実装なし） |
| 2 GREEN | `35e21455eca1cb22751fbf60bca75f7ee4d423f1` | 実装、Test、GREEN Evidence、公式receipt |
| 3 初回Run | `6b4c15fa12d006ca7c4f9d3085aa923149dacb83` | Run records、Run Evidence、機械生成済みTODO |

各commitは明示pathだけをstageした。`git add -A`と`git add .`は使っていない。
commit前に`git diff --check`と該当Test・validator、commit後にread-only照合と
`work_unit_transition --work-status completed`を実行し、いずれも合格・
`next_work_allowed: true`である。利用者のuntracked file（`docs/development/`配下）には触れていない。

## 2. 事前に修正した既存Test不具合

`tests/test_issue_resolution_pilot_wi_005.py::test_actual_post_write_and_isolated_restore_rehearsal`は、
許可するactive Issue IDを`{"ISSUE-PILOT-TODO-GROWTH-001"}`という固定値で持っていた。
TODOのactive Issueが`ISSUE-HTC-C9F6C917`へ正常に移った`4de5afb`以降、TODOもIssueも壊れていないのに
このTestだけが落ちていた。判定の正本がTest内の記憶だったことが原因である。

`tools.development.todo_update_path.load_known_active_issue_ids(ROOT)`で
`.reviewcompass/workflow/`の正本Issue一覧を取得して`verify_post_write()`へ渡し、
active IDが1件でその一覧に含まれることを確認する形へ直した。

- `TODO_NEXT_SESSION.md`は変更していない。
- Definition ChallengeのRED Testは変更・緩和していない。
- 修正後、新Testを除外した全Testは`962 passed`である。
- この修正だけを独立commit`c2e8d48`にした。

## 3. 追加したpublic API・record kind・stop reason・変更module

### 3.1 変更module

| module | 変更 |
| --- | --- |
| `tools/task_contract/definition_challenge.py` | **新設**。material set、D1〜D8、verdict、Contract approval |
| `tools/task_contract/identity.py` | record kind 3件、stop code 14件の登録 |
| `tools/task_contract/contract.py` | version 2の宣言（設計§6.1の差分だけ）とcompile事前gate |
| `tools/task_contract/execution.py` | Contract versionに応じた来歴の期待node／edge、封の再確認 |
| `tools/task_contract/__init__.py` | public APIの明示export |

未定義の汎用framework、plugin、policy、拡張pointは作っていない。

### 3.2 追加したpublic API

```python
build_definition_challenge_material_set(project_root, contract, material_paths,
                                        material_records=(), record_id=None)
run_definition_challenge(project_root, contract, requirement_binding, material_set,
                         owner=DEFINITION_CHALLENGE_OWNER)
build_contract_approval(contract, definition_challenge_verdict, decision,
                        human_id, decided_at, owner=CONTRACT_APPROVAL_OWNER)
compile_gate_reason(contract, definition_challenge_verdict, contract_approval)
provenance_node_roles(contract_version)
```

既存関数の追加引数（version 1の呼出しは引数なしでそのまま動く）。

- `build_review_task_contract(..., supersedes, requirement_receivers, review_owners)`
- `compile_contract(..., definition_challenge_verdict, contract_approval)`
- `verify_provenance(..., definition_challenge_verdict, contract_approval)`

定数も明示exportした。`DEFINITION_CHECKS`、`DEFINITION_SEVERITY_CLASSES`、
`DEFINITION_VERDICT_STATUSES`、`FORBIDDEN_CAPABILITIES`、`STAGE_CONFUSION_KINDS`、
`BOUND_REQUIREMENT_IDS`、`REQUIREMENT_RECEIVERS`、`DEFAULT_REVIEW_OWNERS`、
`DEFINITION_CHALLENGE_OWNER`、`CONTRACT_APPROVAL_OWNER`、`CONTRACT_APPROVAL_DECISIONS`、
`COMPILE_GATE_REASONS`、`CONTRACT_V2_REQUIRED_EDGES`、`CONTRACT_V2_EDGE_ORDER`、
`PROVENANCE_EDGE_ORDER`。

### 3.3 追加したrecord kind

| record kind | identity | 上流参照 |
| --- | --- | --- |
| `definition_challenge_material_set` | `DCM-<contract id>` v1 | `contract_ref` |
| `definition_challenge_verdict` | `DCV-<contract id>` v1 | `contract_ref`、`material_set_ref`、`requirement_binding_ref` |
| `contract_approval` | `CA-<contract id>` v1 | `contract_ref`、`definition_challenge_ref` |

いずれも版付き、Digest付き、上流`record_ref`付きの閉じたrecordである。

### 3.4 追加したstop reason（14件）

D1〜D8：`definition_requirement_unreceived`、`definition_section_missing`、
`definition_scope_violation`、`definition_forbidden_capability`、`definition_owner_separation`、
`definition_deferred_requirement_accepted`、`definition_material_missing`、`definition_stage_confusion`。

compile事前gate（Amendment§3の閉じた語彙）：`definition_challenge_missing`、
`definition_challenge_failed`、`definition_challenge_invalid`、`contract_approval_missing`、
`contract_approval_rejected`、`contract_approval_invalid`。

gateは10段の順で検査し、一件でも満たさなければ`compile_verdict.status`を`not_compilable`にして
`plan_bundle`を含めない。Contract version 1はこのgateを通さない（履歴再読込みの互換性）。

来歴の期待nodeはContract versionから決める。version 1は9 node／8 edge、version 2は
`contract_approval`をChallengeとcompileの間に置く11 node／10 edgeである。
来歴が主張するversionは来歴自身の`review_task_contract` nodeの`record_version`から読むため、
nodeを削ってversion 1として通すことはできない。

## 4. RED・GREEN・全Testの実測

| 対象 | RED | GREEN |
| --- | --- | --- |
| `tests/test_work5a_definition_challenge.py`（45件） | `44 failed, 1 passed` | `45 passed` |
| `tests/test_first_review_task_contract_e2e.py`（既存38件） | `38 passed` | `38 passed` |
| 公式policy runner suite `full` | 実施不能（着手前から1件失敗） | **`1007 passed`** |

REDの失敗理由は43件が`TypeError: build_review_task_contract() got an unexpected keyword
argument 'supersedes'`、1件が`AssertionError: 'definition_challenge_material_set' in RECORD_KINDS`で、
すべて「version 2の新APIとgateが未実装」という期待理由である。通過した1件はG8（version 1経路が
変更なく通ること）で、実装の前後どちらでも通るべきTestである。

公式receipt：`records/development/2026-08-05-work5a-definition-challenge-green-test-receipt-v1.json`
（`{"errors": 0, "failed": 0, "passed": 1007, "skipped": 0, "total": 1007, "xfailed": 0, "xpassed": 0}`、
Python 3.9.6、pytest 8.4.2、fallbackなし）。

### 4.1 RED Testのfixtureを1点だけ直した（GREEN commitに含む）

「別Contractへのapproval差し替え」を確かめる2件で、比較対象の「別Contract」を同じ`contract_id`・
同じ内容で作っていた。record identityも内容も同一なので実際には同じrecordであり、負例になっていなかった。
`contract_id`を別にして、真に別のContractを比較するよう直した。

- 直したのはfixtureだけで、assertionは1件も変えていない（`not_compilable`、
  `contract_approval_invalid`、`failed`、`D7`の期待はそのまま）。
- 期待を実装へ合わせて緩めてはいない。それまで実質何も検査していなかった負例が、
  実際に別Contractのapprovalを拒否することを検査するようになった。
- 他の43件は変更していない。

## 5. 初回Definition Challenge Run

Run records：`records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json`
Evidence：`records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md`
実行時刻：2026-08-06T06:12:09+0900

| 項目 | 値 |
| --- | --- |
| verdict status | **`passed`** |
| `blocking_count` | **0** |
| Finding件数 | **0件**（`nonblocking`も0件） |
| 実行した検査 | D1〜D8 |
| 固定材料 | 19件（束縛16 Requirement definition、対象文書、開発方針、Current Plan） |

### 5.1 作ったrecordのidentity、version、content digest

| record | record_id | version | content digest |
| --- | --- | --- | --- |
| `requirement_binding` | `RB-FIRST-REVIEW-CONTRACT` | 1 | `831217a7c3850fb711427ddc2c6aaf686b9155338e34dfa406a6fbc9f7af68de` |
| `review_task_contract`（draft v2） | `TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 2 | `cfa129d3afce155a683fed7e7da07c3272fb89922264edf79c239b6d3846cfb4` |
| `definition_challenge_material_set` | `DCM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `d90b9f5efb12bd8bc3b58174f8c323017356194133481bfa9e2f2fe30a778816` |
| `definition_challenge_verdict` | `DCV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `d951862f9ab8b760afe796a4356a1a89cc6dd8053bb597768b4916b7cde4a967` |

すべてnew-onlyである。draft Contract v2の`supersedes`は、既存受理bundleが持つversion 1の
node ref（`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1`、version 1、
digest `e67dc0d175510d22fbb657556361757f0b147ca7dcaddbe8941c3a9cc939ed98`）をそのまま指す。
version 1を無効にもstaleにもしていない。

### 5.2 決定性と材料の再照合

同じ固定材料で組み直した結果、draft Contract v2、material set、verdictの3 recordとも
content digestが一致した。材料19件のSHA-256もRun後に再計算し、全件一致している。

## 6. `contract_approval`・compile・Review Run・accepted artifactを作っていない確認

Run bundleの`records`に含まれるrecord種別は`requirement_binding`、`review_task_contract`、
`definition_challenge_material_set`、`definition_challenge_verdict`の**4種だけ**である。
次はいずれも作成していない（bundleの`not_executed_steps`へ機械可読で明示した）。

`contract_approval`、`compile_verdict`、`plan_bundle`、`context_manifest`、`workflow_permit`、
`finding_set`、`conformance_verdict`、`final_challenge_verdict`、`human_decision`、
`provenance_verdict`、`accepted_artifact`。

- `compile_contract`と`build_contract_approval`はRunで一度も呼んでいない。
- Definition ChallengeはContract定義だけを検査し、対象文書の再Reviewはしていない。
- verdictが`passed`でも、HumanのContract version 2承認を代行していない。

## 7. TODO更新

指示§5に従い、`docs/development/prompts/todo-handoff-update.md`の共通手順だけを使った。

- 現在位置、最新Evidence、次の一作業、blocker、Human判断待ちを現在値へ置き換えた。
- 全Test表示は公式receiptから機械生成した（`build_todo_candidate()`）。手入力していない。
  作業単位3のcommitへ余分なreceiptを足さないため、作業単位2で作った公式receiptを入力にした。
- `todo_handoff.py`は`{"findings": [], "status": "passed"}`、compaction validatorは合格
  （5,758 bytes、上限12,288）、参照Digest照合は11件すべて一致。

## 8. 変更していない範囲

- 承認済み設計、Amendment、Decision、Requirement、Current Plan、checklist、Development Policy。
- Contract version 1の出力、既存accepted artifact、既存Provenance record、既存recordの上書き。
  version 2専用fieldはversion 1へ足していない（version 1で渡すと`schema_violation`で止まる）。
- `tests/test_first_review_task_contract_e2e.py`（1文字も変更していない）。
- Work 4B、Work 6A、Architecture Policy、Challenge Policy、risk catalog、隣接Contract、
  汎用Challenge framework、LLM reviewer、UI、CI、外部`DATA_ROOT`。
- push、PR、tag、amend、rebase、reset、force push、履歴書換え、外部送信。
- 利用者のuntracked file。stage も commit もしていない。

## 9. 設計の読み取りで判断した点（設計は変更していない）

D7だけは扱いを二つに分けた。

- **材料の欠落とDigest不一致**は`definition_material_missing`で停止し、verdictを発行しない。
  根拠は設計§2.2の「材料が一件でも欠ける、またはDigestが一致しない場合は
  `definition_material_missing`で停止し、verdictを発行しない」である。
- **material setが別Contractへ結ばれている場合**は検査対象が読み取れる状態なので、
  D7のblocking Findingとして`failed` verdictを出す。

§3の表と§5のH7はstop codeだけを示しており、この読みと矛盾しないと判断した。
意図と異なる場合は指摘いただきたい。

## 10. 次に必要なもの

Contract version 2を承認するかどうかのHuman判断である。承認する場合は`contract_approval`
（`decision: approved`、`human_id`、`decided_at`、上記Contract v2とverdictへの参照）が要る。
それが作られるまで、compile、Review Run、accepted artifactへ進まない。

本報告はcommitに含めていない（`.gitignore`により無視される）。
Codexの独立検証まで次の作業へ進まない。
