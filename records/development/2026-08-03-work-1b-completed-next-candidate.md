---
candidate_id: IC-WORK1B-COMPLETED-NEXT-001
observed_at: 2026-08-03T13:50:06+09:00
origin_stage: initial-development
origin_work: Work 1B
origin_work_item: RC3-WORK1B-OPERATIONAL-USE
candidate_kind: improvement_candidate
status: closed
suggested_route: current_work_repair
confidentiality_class: project-internal
---

# Work 1B completed WorkのNEXT残留改善候補

## 1. 観測

Work 1B bootstrapを実session相当のdevelopment event streamへ自己適用した。開始時は
`session_started | work_started`から次のshort textを生成し、開始表示として使用した。

```text
RC3 | Work 1B | active | blockers:0 | decisions:0 | next:Complete operational session and verify saved evidence
```

終了時は`work_completed | session_ended`を追加し、完成event streamをdurable captureした。保存済みrawを
再読込して生成したdetailed textでは、Work stateとactive work itemは正しく完了へ遷移した。

```text
PLAN
  work: Work 1B Session Log Bootstrapと現在位置text表示
  state: completed

CURRENT ACTIVITY
  work_item: none
  tdd_state: green
```

一方、`NEXT`には開始時のactionが残った。

```text
NEXT
  Complete operational session and verify saved evidence
```

このactionは同じevent streamですでに完了している。したがって、終了表示は`completed`と「これから完了する」
actionを同時に示し、現在位置として不整合である。

## 2. 固定sourceとEvidence

| role | identity | SHA-256／結果 |
|---|---|---|
| 現行Plan | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |
| bootstrap実装 | `tools/development/session_log_bootstrap.py` | `5ce2f77d671d48c8627cc3072a1b2111a4fc4ef615f3454d7b353d3b9ad2ac97` |
| E2E固定Test | `tests/test_session_bootstrap_e2e.py` | `ca4486fb43b3e5f4bd32175b0e177efb1a8612c08e2b43edaa98206e453eaedb` |
| operational session | `operational-session:rc3-work1b-operational-20260803-001/events-final` | `900811d92d60854d6bc50ffdf53bd3a91dbf201a9309212bcc5c49f0602e5d5d` |
| start display receipt | `EVALUATION_ROOT/start-display.json` | `4bda609bf80d345ee82f92730a700c5691cba5cc7c2d5e566a570e3f2486f051` |
| end display receipt | `EVALUATION_ROOT/end-display.json` | `62e692e5ef9eb142c377991eaa16cac89c4334c5facb17d08586cae7565556c8` |
| Session Evidence | `DATA_ROOT/sessions/rc3-work1b-operational-20260803-001/session-evidence.json` | `2f4ffa1941faad3320d19ee98c59689a35c34478cef7470d13bdfaf81291d7a3` |
| full Test | `python3 -m pytest -q` | `434 passed in 1.84s` |

保存後再読込では、source rawと`SENSITIVE_ROOT`の保存rawがbyte一致し、rawおよび3派生物の実Digestが
Session Evidenceと一致した。

| artifact | SHA-256 |
|---|---|
| raw event stream | `900811d92d60854d6bc50ffdf53bd3a91dbf201a9309212bcc5c49f0602e5d5d` |
| index | `2b001749b90a4f2b062af9f363e333124f5de092454bddb6ee5069d788227548` |
| summary | `edbbcb684854de93085a89c3043b432625ffac7d1c2b30908b4499ea3003068d` |
| transcript | `e4d637538a9c0cb81af7315c5f32c3334bdf863f65ffd4a9c8d98ac7c07ed386` |

`generated_at`は`2026-08-03T13:50:06+09:00`、freshnessは`current`として保存・再読込した。

## 3. 原因仮説と分類

`project_current_work`の`work_completed`分岐は、Plan stateを`completed`、active work itemを`None`へ更新するが、
`next_action`を更新しない。このため`work_started.payload.next`がそのまま残る。

```yaml
classification_candidates:
  - implementation_defect
  - test_or_oracle_defect
affected_authority:
  - Work 1B Current Work Projection acceptance
  - session終了時の現在位置text
acceptance_truth_changed: true
safety_or_security_impact: false
authority_impact: false
provenance_reconstructability_impact: false
source_test_verdict_identity_impact: false
current_work_can_continue: false
suggested_route: pause_and_triage
route_reason: Work 1B完了関門で要求する現在位置textの正確性を満たさず、期待するNEXT遷移の意味判断が必要なため
duplicate_of: null
checkpoint: Work 1B completion gate before Human completion decision
human_decision: option_1_approved
consumer_refs:
  - DEC-WORK1B-COMPLETED-NEXT-2026-08-03-V1
outcome_ref: RC3-WORK1B-COMPLETED-NEXT-GREEN-2026-08-03-V1
```

既存Testは全件greenだが、`work_completed`後のNEXTを固定したoracleがない。したがって、green件数だけでは
Work 1BのAcceptanceを満たしたと判断できない。

## 4. route proposal

現行Workを`pause_and_triage`し、Work 1B完了判断を停止する。現行Plan、Test、Acceptanceは本候補だけで
変更しない。

Human判断候補は次の二つである。

1. `work_completed.payload.next`を必須にし、完了eventが次の実行可能actionを明示する。欠落時はprojectionを
   `incomplete`として表示する。
2. `work_completed`で旧nextを消去し、後続scheduler decisionが別eventでnextを与えるまで`none`と表示する。

既定提案は1である。完了後のnextを暗黙推測せず、event identityとDigestへ接続できるためである。

## 5. Human判断待ちと再開条件

- 判断対象：上記1または2のNEXT遷移規則を採用するか、別規則を指定するか。
- 判断後作業：新しい回帰Testをredで追加し、既存Testを変更せず実装修正する。
- stale閉包：bootstrap実装、E2E green Evidence、Work 1B完了候補、current projection表示。
- 再開条件：Humanが遷移規則とcurrent Workへのrouteを承認し、回帰Testの期待を固定できること。

本候補はroute proposalであり、Issue昇格、Test変更、実装修正、Work 1B完了を自動承認しない。

## 6. Human判断結果

2026-08-03T14:00:01+09:00にHumanが選択肢1を選択した。これにより、次の規則と
`current_work_repair` routeが承認された。

- `work_completed.payload.next`は必須である。
- 値がある場合は、開始時の旧NEXTを完了eventのNEXTで置き換える。
- 欠落時はprojectionを`incomplete`とし、`work_completed.payload.next`の欠落を表示する。

判断正本は`records/development/2026-08-03-work-1b-completed-next-decision.json`である。この判断は
回帰Test追加と実装修正を承認するが、Work 1Bの完了またはWork 2への移行は承認しない。

## 7. Outcome

選択1を回帰Testへ固定して修正し、関連`17 passed`、全`436 passed`、別の外部development rootでの
実運用再検証と保存後Digest照合を完了した。Outcomeは
`RC3-WORK1B-COMPLETED-NEXT-GREEN-2026-08-03-V1`であり、
`records/development/2026-08-03-work-1b-completed-next-green-evidence-v1.md`へ固定した。

本候補のconsumerとOutcomeが接続されたため候補を`closed`とする。Work 1Bの段完了承認は引き続き
Human判断待ちである。
