# 統合除外宣言 初版entry候補一覧 v1

- 状態：`human_decision_pending`（Human裁定まで除外宣言recordを作成しない）
- 作成日：2026-08-07
- 承認根拠：`DEC-WORK4B-MAIN-DESIGN-BUNDLE-001`
  （`records/development/2026-08-07-work4b-main-design-bundle-approval-decision-v1.md`）構成A-1
- 解決する既知の問題：凍結が機械可読な形でどこにも宣言されていないこと。
  `DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001`
  （`records/development/2026-08-06-frozen-lane-guidance-correction-decision-v1.md`、SHA-256
  `9c0b58bdfc868e03d9d4a3dd05c179157ec05324c88bffdc9a51a12fce2e8994`）§2が原因1として記録した
  「凍結がcommit message、設計提案の本文、Testのassertに散在している」状態を、本宣言が
  一箇所の機械可読recordへ集約する。

## 1. entryの意味

除外宣言に載った対象は、絞り込み順位表（構成A-2）から機械的に落ち、統合候補としてLLMにも
Humanにも提示されない。落とした件数は順位表が表示する。除外は「統合しない」の宣言であって、
コードの削除・変更・レビュー免除を意味しない。

## 2. 初版entry候補（3件）

### E1：旧Pilot subject固定の検証器群 — `frozen_lane`

- 対象：`tools/development/issue_resolution_pilot.py`のうち、旧Pilot subject
  （`ISSUE-PILOT-TODO-GROWTH-001`）へ固定された検証器関数群
  （`validate_implementation_task_contract_v2`とその固定source検証helper
  `validate_fixed_sources_for_contract`、`validate_task_contract_sources`）
- 確認方法【実測】：`validate_implementation_task_contract_v2`は580行目で
  `issue_id != "ISSUE-PILOT-TODO-GROWTH-001"`を拒否し、WI-001〜007の順序を釘付けしている
- 理由：旧Pilotの記録は旧規則のまま保持し、新規則で再判定しない（凍結）。これらの検証器を
  現行世代の検証器と統合すると、凍結の意味（旧記録が旧検証器で検証され続けること）が壊れる
- 根拠：`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` §1.1（SHA-256
  `8475cd94b449e0709eb97e6d487b86cceef86e0307b3bbb7e78351d8f43147a9`）、
  `DEC-FROZEN-LANE-GUIDANCE-CORRECTION-001`

### E2：Intake v2版のrecord検証経路 — `version_pinned`

- 対象：`config/development-issue-resolution-pilot-v2.json`と、これを入力とする
  `validate_record_file`のv2 config適用経路（schema_version 2のrecordをv2規則のまま検証する系）
- 理由：v2形式で作られた既存recordは、v2の規則で検証され続ける必要がある。v3系との統合や
  「最新版だけに一本化」は、既存recordの検証可能性を失わせる
- 根拠：同上（§1.1「旧記録は旧versionの規則のまま保持し、新規則で再判定しない」）

### E3：旧37要件の決定的移行器 — `historical_retained`

- 対象：`tools/requirements/unified_migration.py`（旧37 Requirement定義を統一50候補へ移行した
  一回性の移行器）
- 理由：移行の再現可能性（旧定義→統一候補の決定的変換が当時どう行われたか）を保持するための
  歴史的な一回性コードであり、現行の検証器・生成器との統合対象にしない
- 根拠：統一50 promotion完了Evidence
  （`records/development/2026-08-03-work-3-unified-requirements-promotion-completion-evidence-v1.md`）
  が移行器をtest-first固定として記録している

## 3. 候補に含めなかったもの（判断材料）

- `tools/session_logs/`のstage期module群：凍結・版固定のDecision記録が存在しないため、
  推測で除外しない。統合候補として順位表に載り、意味判断はHumanに残る
- superseded済みの記録（対応表v1など）：recordはroutine一覧に載らないため、除外宣言の対象外
  （統合候補にそもそもならない）
- Work 4A v1/v2の撤去済みcode：現存しないため対象外

## 4. 次の手順（裁定後）

1. 裁定済みentryで`.reviewcompass/workflow/integration-exclusions/`の初版record（new-only、
   schema・検証器つき）をtest-firstで実装する（宣言→RED対応表は恒久検査器で照合）
2. 構成B（再観測）→A-2（順位表）へ進む。順位表は本宣言を機械参照する

## 5. Human裁定のお願い

- 3件の採否（部分採用・追加・修正いずれも可）
- entry粒度（関数単位E1／file＋経路単位E2／file単位E3）がこの形でよいか
