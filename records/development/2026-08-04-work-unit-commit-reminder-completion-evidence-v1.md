---
evidence_id: RC3-WORK-UNIT-COMMIT-REMINDER-COMPLETION-2026-08-04-V1
recorded_at: 2026-08-04T07:12:19+09:00
status: verified_completed_pending_commit
confidentiality_class: project-internal
---

# Work Unit Commit Reminder Completion Evidence V1

## 結果

完了した作業単位に未コミット差分がある場合、Humanへリマインドし、コミットされるまで次作業への遷移を
停止するdevelopment限定Pilotを実装した。自動コミット、push、guarded commit、Git hook、履歴書換えは
導入していない。

## Human DecisionとRED

| role | artifact | SHA-256 |
|---|---|---|
| Human Decision | `records/development/2026-08-04-work-unit-commit-reminder-pilot-decision.json` | `327cdf74c4cedfa2230a906fbe4e75f24b2cff1da6a00c06a6c3ea03c1cdb64b` |
| RED Evidence | `records/development/2026-08-04-work-unit-commit-reminder-red-evidence-v1.md` | `2fabf5401ef44c1fbcf92758215855b941d8ef5de30178dea0b2763870e31f0b` |

初回REDは遷移preflight未実装だけを理由として`5 failed in 0.04s`だった。

## 実装と運用境界

| role | artifact | SHA-256 |
|---|---|---|
| deterministic preflight／CLI | `tools/development/work_unit_transition.py` | `de131c00baef55799b6222aec578c2ad4e960b5e56df8a0b97fcdabd998d434e` |
| positive／negative／boundary Test | `tests/test_work_unit_transition.py` | `08ffe474117ceeedbb746d6b0278ca0dc29f859f7348c37dfb141a7f8dcbea4f` |
| development policy | `docs/development/2026-08-02-development-policy.md` | `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0` |
| agent instruction | `AGENTS.md` | `683f37e084798a8605337b7c9cacbee874ec26fbd00ac2800683d8e952c8b1a9` |
| session checklist | `docs/development/2026-08-03-initial-development-checklist.md` | `b088822c477d3103efd936a382a067a7e13a976fa11e5002b76cd43530b65383` |
| TODO template | `docs/development/templates/TODO_NEXT_SESSION.template.md` | `5cc96f7fa45e2d2f12a1ba2fa4422de9e70f1a9ae29feda0cbfd59c09ea3cca7` |

`completed`とGit porcelainのdirtyを同時に満たす場合だけ
`completed_work_unit_uncommitted`を返す。`in_progress`のdirty差分はcommit reminderの対象外とする。

## Verification

- targeted／handoff Test：`11 passed in 0.03s`
- TODO template validator：finding 0
- 公式全Test：
  `records/development/2026-08-04-work-unit-commit-reminder-green-test-receipt-v1.json`を正本とする。
- post-write transition preflight：本作業単位が完了済みでdirtyのため
  `completed_work_unit_uncommitted`となることを確認する。

## Pilot後の判断

誤停止、停止漏れ、コミット忘れ、作業単位混在、追加操作量を観測する。Pilot評価前に自動コミットへ
移行しない。コミットとpushは本作業では未実施である。
