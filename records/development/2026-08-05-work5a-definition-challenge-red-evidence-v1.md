# Work 5A Definition Challenge RED Evidence v1

- 対象：後継draft Review Task Contract version 2（`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2`）
- 承認：`DEC-WORK5A-DEFINITION-CHALLENGE-001`、`DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`
- 正本設計：`docs/design/2026-08-05-work5a-definition-challenge-proposal.md`
- Amendment：`docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-implementation.md`

## 1. 開始前の機械照合

開始基準commit`6b6c989cd676be81b81a376a2f6b6253c869c406`はHEAD`87b0217`の祖先である。
worktreeに他者の未コミット変更は無かった（`git status --short`が空）。

指示§2の固定資料13件をすべて全文読み、SHA-256を機械照合した。**13件すべて一致**である。

| path | 判定 |
| --- | --- |
| `records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-adoption-decision-v1.md` | 一致 |
| `docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md` | 一致 |
| `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | 一致 |
| `records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md` | 一致 |
| `records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-improvement-candidate-v1.md` | 一致 |
| `records/requirements/definitions/req-contract-004--v1.json` | 一致 |
| `docs/current/reviewcompass3-plan-current.md` | 一致 |
| `docs/development/2026-08-02-development-policy.md` | 一致 |
| `tools/task_contract/contract.py` | 一致 |
| `tools/task_contract/execution.py` | 一致 |
| `tools/task_contract/identity.py` | 一致 |
| `tools/task_contract/__init__.py` | 一致 |
| `tests/test_first_review_task_contract_e2e.py` | 一致 |

Work 5Aが直接束縛する16 Requirement definitionも全文を読み、`records/requirements/definitions/`に
16件すべて実在することを機械確認した。Architecture Policy、risk catalog、同じ運用面の隣接Contract、
Challenge Policyは実在しないため、推測で新設していない（設計§2.2）。

## 2. この段階で作っていないもの

`tools/task_contract/`は**1文字も変更していない**。実装moduleも作っていない。
Test fileとこのEvidenceだけを追加した。

## 3. 追加したTest

`tests/test_work5a_definition_challenge.py`を新規作成した。45件（parametrizeを展開した数）である。
元設計§5のG1〜G4、H1〜H11と、Amendment§5のG5〜G8、H12〜H17を正例・負例・境界例として固定した。

### 3.1 正常例

| test | 固定する条件 |
| --- | --- |
| G1 `test_g1_valid_draft_contract_v2_passes_with_no_findings` | 材料が揃った正しいdraft Contract v2で`passed`、`blocking_count`が0、`findings`が空、`checks`がD1〜D8 |
| G2 `test_g2_compile_requires_a_passed_challenge` | `passed` Challengeがある場合だけcompileが`compiled`を返し、Plan bundleを持つ |
| G3 `test_g3_definition_challenge_precedes_compile_in_provenance` | 来歴でDefinition Challengeがcompileより前にあり、自己辺が無い |
| G4 `test_g4_contract_v2_declares_receivers_and_distinct_owners` | v2が`requirement_receivers`（16件、値は実在する非空の10節）と、pairwise distinctな`review_owners`、`supersedes`を持つ |
| G5 `test_g5_compile_requires_both_passed_challenge_and_approved_approval` | `passed` Challengeと`approved` approvalの両方が揃った場合だけ`compiled` |
| G6 `test_g6_contract_approval_binds_contract_and_challenge` | approvalがContract v2とChallenge verdictのidentity、version、Digestを保持し、owner・decision class・human identity・decided atを持つ |
| G7 `test_g7_contract_v2_provenance_has_eleven_nodes_and_ten_edges` | v2来歴が11 node、10 edgeで、`contract_approval`がChallengeとcompileの間にある |
| G8 `test_g8_contract_version_one_path_is_unchanged` | Contract version 1のcompileと9 node、8 edge来歴、accepted artifactがそのまま通る |

### 3.2 負例（D1〜D8）

| test | 期待するstop code |
| --- | --- |
| H1、H1b | `definition_requirement_unreceived`（受け先欠落と、10節でないfieldを指す受け先） |
| H2、H2b | `definition_section_missing`（節が空、AcceptanceがDefinition Challengeを必須にしない） |
| H3 | `definition_scope_violation`（target 2件、`docs/`外） |
| H4 | `definition_forbidden_capability`（`call_llm`、`external_transmission`、`write_artifact`、`git_write`の各々） |
| H5 | `definition_owner_separation` |
| H6 | `definition_deferred_requirement_accepted` |
| H7、H7b | `definition_material_missing`（材料file欠落、Digest不一致。**verdictを発行せず停止**する。設計§2.2） |
| H8 | `definition_stage_confusion`（`plan_bundle`、`compile_verdict`、`finding_set`、`conformance_verdict`、`final_challenge_verdict`の各々） |
| H9 | `failed` Challengeで`not_compilable`となり、`plan_bundle`を作らない |
| H10 | `provenance_node_missing`（Challenge nodeを欠く来歴） |
| H11 | `failed` Challengeからaccepted artifactへ到達できない |

### 3.3 負例（approval gate）

| test | 期待するstop code |
| --- | --- |
| H12 | `contract_approval_missing`（`passed` Challengeだけではcompileできない） |
| H13 | `contract_approval_rejected` |
| H14 | `contract_approval_invalid`（content digest改竄） |
| H15、H15b | `contract_approval_invalid`（別Contract、別Challengeへの差し替え） |
| H16 | `provenance_node_missing`、detailは`contract_approval` |
| H17 | 改竄approvalの来歴からaccepted artifactを作れず、`rejected` approvalで`contract_approval_rejected` |

### 3.4 決定性と閉じたschema

- `test_challenge_is_deterministic_for_identical_input`：同一入力で同一content digestになる。
- `test_material_set_fixes_every_file_digest`：material setが各fileのpathとSHA-256を固定する。
- `test_finding_and_verdict_vocabularies_are_closed`：severityは`blocking | nonblocking`、statusは
  `passed | failed`だけで、既存の`error / warning / info`と別語彙である。Findingのfield集合も固定する。
- `test_definition_challenge_record_kinds_and_stop_codes_are_registered`：3 record kindと14 stop codeの登録。
- `test_challenge_rejects_a_material_set_bound_to_another_contract`、
  `test_missing_challenge_input_is_not_compilable`、`test_tampered_challenge_verdict_is_not_compilable`。

Testはすべて`tmp_path`（pytestが用意する一時directory）配下だけで完結する。
実projectのfile、Contract version 1の既存record、既存accepted artifactへは書いていない。

## 4. RED実行結果

```text
.venv/bin/python3 -m pytest -q tests/test_work5a_definition_challenge.py
→ 44 failed, 1 passed
```

失敗理由の内訳は次であり、すべて「version 2の新APIとgateが未実装」という期待理由である。

| 件数 | 失敗理由 |
| --- | --- |
| 43 | `TypeError: build_review_task_contract() got an unexpected keyword argument 'supersedes'` |
| 1 | `AssertionError: assert 'definition_challenge_material_set' in RECORD_KINDS` |

唯一通過した1件はG8である。G8は「Contract version 1の既存経路が変更なく通る」ことを固定するTestで、
実装の前後どちらでも通らなければならない。実装不在で失敗すべきTestではない。

既存Testの状態も機械確認した。

```text
.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py
→ 38 passed
```

既存38件はGREENのままである。弱めた期待は無い。

## 5. 着手前から公式全Testが1件失敗している（停止事由）

公式全Testを実行すると、**この作業とは無関係のTestが1件失敗する**。

```text
FAILED tests/test_issue_resolution_pilot_wi_005.py::test_actual_post_write_and_isolated_restore_rehearsal
tools.development.todo_compaction.TodoCompactionError: unknown active ID
```

追加Test fileを除外しても同じである。

```text
.venv/bin/python3 -m pytest -q --deselect tests/test_work5a_definition_challenge.py
→ 1 failed, 961 passed
```

### 5.1 機械的に特定した原因

そのTestは`TODO_NEXT_SESSION.md`の実fileを読み、既知active IDを
`{"ISSUE-PILOT-TODO-GROWTH-001"}`と固定値で持つ。
`tools/development/todo_compaction.py`のactive ID判定は
`^- \`(?P<record_id>ISSUE-[A-Z0-9-]+)\`：`という行頭patternである。

各commitのTODOからこのpatternを機械抽出した結果は次である。

| commit | 抽出したactive ID | 判定 |
| --- | --- | --- |
| `9ebefba`（Claudeの直前作業） | `ISSUE-PILOT-TODO-GROWTH-001` | 一致 |
| `1f8374d`、`464be6b`、`01f2fcf`、`cfcb334`、`96e9da0` | `ISSUE-PILOT-TODO-GROWTH-001` | 一致 |
| **`4de5afb`（Pause Work 5A for approval gate triage）** | `ISSUE-HTC-C9F6C917` | **不一致** |
| `6b6c989`（本作業の開始基準）、`be82301`、`2470cc2`、`87b0217`（HEAD） | `ISSUE-HTC-C9F6C917` | 不一致 |

`4de5afb`でTODOの「現在作業に影響する改善候補／Issue」節の行が
`- \`ISSUE-PILOT-TODO-GROWTH-001\`：resolved。…`から
`- \`ISSUE-HTC-C9F6C917\`：…`へ替わり、固定値のknown active IDと合わなくなった。
**本作業の開始基準commit`6b6c989`の時点で、既にこの状態である。**

`records/development/2026-08-05-todo-related-test-path-discovery-improvement-candidate-v1.md`は、
TODO更新後に関連Testを`todo_(handoff|compaction|projection)`の6 fileへ限定して実行し
`31 passed`だったと記録している。公式全Testはその時点で実行されていない。

### 5.2 停止の理由

指示§7の停止条件に「全Test不合格」がある。また指示§4は作業単位2の完了条件として
「追加Test、既存`tests/test_first_review_task_contract_e2e.py`、公式全TestをGREENにする」と定める。
この失敗はDefinition Challengeの実装では解消しない。解消するには次のどちらかが要るが、
どちらも本指示の固定範囲外である。

1. `TODO_NEXT_SESSION.md`のactive ID行を戻す。TODO更新は指示§5の作業単位3の範囲であり、
   かつHEADのTODOはHumanとCodexが本handoffのために書いたものである。
2. `tests/test_issue_resolution_pilot_wi_005.py`の固定known active IDを直す。
   既存Testの変更であり、指示§7の「既存Testを弱めない」に触れる可能性がある。

したがって作業単位1を完了・commitしたうえで、作業単位2へ進まずに停止して報告する。
推測でTODOも既存Testも書き換えない。

## 6. この作業単位で変更していないもの

- `tools/task_contract/`、既存Test、Contract version 1、既存accepted artifact、既存Provenance record。
- 承認済み設計、Amendment、Decision、Requirement、Current Plan、checklist、Development Policy。
- `TODO_NEXT_SESSION.md`。この作業単位では更新しない（指示§3）。
- `contract_approval`とHuman review acceptanceは作成も代行もしていない。
