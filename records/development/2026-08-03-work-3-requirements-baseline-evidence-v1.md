---
evidence_id: RC3-WORK3-REQUIREMENTS-BASELINE-2026-08-03-V1
recorded_at: 2026-08-03T16:27:33+09:00
stage: initial-development
work: Work 3
status: verified_baseline
workflow_state: active
completion_authority: human
confidentiality_class: project-internal
---

# Work 3 Requirements固定source・被覆Baseline Evidence V1

## 1. 結果

既存37要件と追加13要件の固定sourceを特定し、計50 IDの母集合、owner、停止、復旧、受入、対象外を
再監査した。現行Planに対するIDの順逆照合は欠落・余剰0で、既存37要件のsource traceにも未被覆はない。

一方、既存37 Requirementそれぞれを追加差分に対して`preserve | adapt | replace | defer`へ分類した
Requirement単位の37行matrixは固定されていない。既存の継承matrixは37 Acceptance Testを分類するが、
Requirement ID単位の意味的な後継関係を代替しない。このgapがあるため、Work 3先頭項目は完了にせず、
本Evidenceを`verified_baseline / coverage_gap_open`として次作業へ渡す。Requirements本文、現行Plan本文、
既存Approvalは変更していない。

## 2. 開始条件

| artifact | SHA-256／state |
|---|---|
| `records/development/2026-08-03-work-2-completion-evidence-v1.md` | `8a5f42dbde5d3b79ae2b200746e46f441cf07219a8ff5836fbf749d6563442d2`／Work 2 `verified / completed` |
| `records/requirements/stage-four-user-approval.json` | `48ea1b075caa628fcfb1f6391d3eb6e51a3584a136d8a5706ecbd8a2cc8cedfc`／既存37要件Human承認 |
| `records/requirements/stage-four-completion.json` | `c13fab7dae8b81a45e6661aea60172d125abf44b09ccab6c953b6f2ea9a795b0`／37要件、未被覆0、未解決0 |
| `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f`／provisional |

Work 2完了、blockerなし、Human判断待ちなしを再確認してから監査を開始した。

## 3. 固定source

### 3.1 既存37要件

| role | artifact | SHA-256 |
|---|---|---|
| Review Context 7要件本文 | `docs/requirements/review-context-requirements.md` | `0622d8b1cc80e0c23119b78bd137c90e8e1c621bc0fde2e99f8a82e71e76ac23` |
| Review Context 7要件構造化record | `records/requirements/review-context-batch-0001.json` | `8dbcf5af0a9b1ba15c30bc4f3c8b8853000999b597f01b1ae51dc4c26c5c759a` |
| 残り30要件本文 | `docs/requirements/remaining-feature-requirements.md` | `ec31ce53ce097a8ff8a59a4649d97e4af8d8dd0cbdb8a1a8c7d4e8d2a1f8bcf6` |
| 残り30要件構造化record | `records/requirements/remaining-batches-0002-0009.json` | `71e21125bf56ad08b0a11af58de9010b528c2a2e9dcd3987e618c6aec095e4c4` |
| 37要件coverage audit | `records/requirements/requirements-coverage-audit.json` | `21de7978a0bede5ea014e0e978ae25b9b280e6d0402ae6a6af7e13e503be6de2` |

Coverage audit内の12 artifact参照は全件、現行fileの再計算Digestと一致した。既存37要件のHuman承認は
外部Approval Recordへ束縛されており、Requirements文書frontmatterのprovisional表示を承認正本として
解釈しない。

### 3.2 追加13要件

| role | artifact | SHA-256／state |
|---|---|---|
| Task Contract／Workflow Requirements差分 | `docs/requirements/2026-08-02-task-contract-requirements-delta.md` | `9c69f54aae6b03549844db73aab24aac0d448f856f2b3faf81f2b0549ece9ccd`／review-candidate |
| 旧第5段継承matrix | `docs/design/2026-08-02-stage-five-to-task-contract-inheritance.md` | `b75450300fc6a254843d5353be17d66838553376393d68a0da8f529ab26cdd5e`／successor-candidate |
| 継承Decision／検証record | `records/task-contract/task-contract-centered-documentation-v4.json` | `d3ac4ecee32006470ef258a4e80413542585f0816c22f5a0266ce888b84e70ae`／documented |

追加13要件はWork 3のHuman判断候補であり、既存37要件のApprovalまたは現行Planだけから承認済みとは
扱わない。

## 4. ID母集合とowner

| owner | ID範囲 | 件数 | source class |
|---|---|---:|---|
| `FEAT-REVIEW-CONTEXT` | `REQ-CONTEXT-001`〜`007` | 7 | existing |
| `FEAT-HARNESSED-EXECUTION` | `REQ-EXEC-001`〜`006` | 6 | existing |
| `FEAT-REVIEW-TRIAGE` | `REQ-TRIAGE-001`〜`003` | 3 | existing |
| `FEAT-SEMANTIC-TRACE` | `REQ-TRACE-001`〜`005` | 5 | existing |
| `FEAT-SESSION-RECORDS` | `REQ-SESSION-001`〜`003` | 3 | existing |
| `FEAT-WORKFLOW-CONTROL` | `REQ-WORKFLOW-001`〜`004` | 4 | existing |
| `FEAT-PORTABLE-LIFECYCLE` | `REQ-PORTABLE-001`〜`004` | 4 | existing |
| `FEAT-EVIDENCE-EVALUATION` | `REQ-EVAL-001`〜`003` | 3 | existing |
| `FEAT-SELF-IMPROVEMENT` | `REQ-IMPROVE-001`〜`002` | 2 | existing |
| `FEAT-TASK-CONTRACT-CONTROL` | `REQ-CONTRACT-001`〜`008` | 8 | added |
| `FEAT-WORKFLOW-CONTROL` | `REQ-WORKFLOW-005`〜`009` | 5 | added |

既存owner欠落は0。追加13要件はRequirements差分の対象Feature宣言と現行PlanのFeature区分から上表ownerへ
一意に対応する。`REQ-WORKFLOW-010`と`011`は手作業Pilot後の候補であり、現行50要件へ数えない。

## 5. 機械監査結果

固定sourceを再読込して次を確認した。

```text
old_count 37
new_count 13
total_count 50
old_new_overlap 0
old_shape_gaps 0
new_shape_gaps 0
plan50_count 50
source_to_plan_missing []
plan_to_source_extra []
excluded_candidates_present ['REQ-WORKFLOW-010', 'REQ-WORKFLOW-011']
old_trace_uncovered_requirements 0
old_trace_uncovered_obligations 0
result passed
```

`old_shape_gaps`は構造化37要件の`inputs`、`outputs`、`stop_conditions`、
`recovery_conditions`、`acceptance_criteria`、`non_goals`の欠測数である。`new_shape_gaps`は追加13要件の
入力、出力、停止条件、復旧条件、失敗時に保存するもの、受け入れ条件、対象外の見出し欠測数である。

既存Requirements専用Testは次の結果だった。

```text
python3 -m pytest -q \
  tests/test_requirements_fixed_inputs.py \
  tests/test_requirements_batch.py \
  tests/test_requirements_feature_partition.py \
  tests/test_requirements_source_trace.py \
  tests/test_requirement_boundary_relations.py

59 passed in 0.07s
```

## 6. 順逆被覆の判定

| 観点 | 結果 | Evidence |
|---|---|---|
| 既存37 source → 現行Plan | pass | 37 ID全件が50 ID母集合に存在し、欠落0 |
| 追加13 source → 現行Plan | pass | 13 ID全件が50 ID母集合に存在し、欠落0 |
| 現行Plan → 37＋13 source | pass | 候補`010/011`を除いた50 IDに余剰0 |
| 既存37 Requirement → approved essence／atomic obligation | pass | requirement未trace 0、obligation未trace 0 |
| 旧37 Acceptance Test → proposed successor test | pass | 37行、`preserve: 15`、`adapt: 20`、`replace: 2`、後継test ID 37件 |
| 既存37 Requirement → 追加差分disposition／successor | incomplete | Requirement ID単位の37行matrixなし |

最後のgapは、Acceptance Test継承表からRequirementの意味的dispositionを暗黙推定して埋めない。Humanが
reviewできるRequirement単位の候補へ明示してから完了判断する。

## 7. 判定と次作業

- 固定source、50 ID母集合、owner、停止、復旧、受入、対象外のbaseline確認は`verified`。
- ID inventoryと既存source traceの順逆照合は`passed`。
- Requirement単位の新旧semantic coverageは`incomplete`。
- Work 3先頭checkboxは未完了のままとする。
- blockerはない。Human判断待ちもまだ発生していない。
- 次に実行可能な一作業は、既存37 Requirementの`preserve | adapt | replace | defer`、successor、
  追加13要件との関係を1行ずつ持つcoverage matrix候補を作成し、独立照合することである。

