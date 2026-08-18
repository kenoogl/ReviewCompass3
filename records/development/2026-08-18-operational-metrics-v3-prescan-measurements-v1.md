# 測定ブロック：運用集計v3（書式C＝表cell束縛）事前走査の実測

- captured_at：2026-08-18T21:23:08+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-18-operational-metrics-v3-prescan-commands-v1.json`（SHA-256 `10bc00ddb6448e053898f4135fe39b4e5a2794b83480a1f9f89a75efb8646035`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 表行にhexを含む行数（書式Cの母数）

- argv：`["grep", "-rEc", "^\\|.*[0-9a-f]{64}", "records/development/"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.075s
- 完全性：二重実行一致

- stdout：

```text
records/development/2026-08-09-work7a-exception-chain-path-correction-green-test-receipt-v1.json:0
records/development/2026-08-18-operational-metrics-v3-prescan-commands-v1.json:0
records/development/2026-08-15-one-item-review-boundary2-red-evidence-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-reassessment-v2.md:0
records/development/2026-08-17-session-log-prefix-interpretation-product-acceptance-decision-v1.md:0
records/development/2026-08-13-python-313-pycache-correction-review-v1.md:0
records/development/2026-08-05-shell-path-variable-digest-check-improvement-candidate-v1.md:0
records/development/2026-08-15-one-design-acceptance-boundary3-red-evidence-v1.md:0
records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-evidence-v1.md:0
records/development/2026-08-17-request-builder-implementation-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-v4-red-evidence-v1.md:0
records/development/2026-08-13-stage3-test-cleanup-execution-sequencing-decision-v1.md:0
records/development/2026-08-07-candidate-ranking-reuse-search-attestation-v1.json:0
records/development/2026-08-11-codex-pilot-claude-session-bootstrap-blocked-evidence-v1.md:0
records/development/2026-08-10-egress-guard-fix-slice1-test-receipt-v1.json:0
records/development/2026-08-05-task-contract-source-pin-early-pilot-policy-v1.json:0
records/development/2026-08-17-rq2-case-fixture-prescan-v1.md:0
records/development/2026-08-16-reviewer-launch-adapter-v1-self-review-v1.md:0
records/development/2026-08-15-one-design-acceptance-contract-v3-independent-rereview-v1.md:0
records/development/2026-08-07-work4b-a1-integration-exclusions-green-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-task-contract-state-gap-decision.json:0
records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-test-receipt-v1.json:0
records/development/2026-08-16-external-reviewer-single-send-completion-review-v1.md:0
records/development/2026-08-17-rq2-measurement-and-pool-decision-v1.md:0
records/development/2026-08-03-work-3-unified-requirements-revalidation-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md:2
records/development/2026-08-04-issue-resolution-pilot-wi-001-red-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-review-repair-correction-review-reassessment-v1.md:0
records/development/2026-08-06-work5a-contract-v2-approval-decision-v1.md:3
records/development/2026-08-04-work-4a-v3-acceptance-red-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-contract-adoption-and-implementation-start-decision-v1.md:0
records/development/2026-08-05-machine-operation-routing-task-python-cache-approval-final-receipt-v1.json:0
records/development/2026-08-07-verification-boundary-layer2-declaration-red-map-v1.json:0
records/development/2026-08-16-reviewer-launch-allowed-models-approval-v1.md:0
records/development/2026-08-11-claude-bootstrap-review-repair-scope-v1.md:0
records/development/2026-08-17-e2e-012-001-tier3-acceptance-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-candidate-review-v1.md:0
records/development/claude-bootstrap-completion-review-v1.json:0
records/development/2026-08-15-one-item-review-final-verification-evidence-v1.md:4
records/development/2026-08-18-rq2-paired-trial-dataset-v1.json:0
records/development/2026-08-17-claude-subagent-backend-product-acceptance-decision-v1.md:8
records/development/2026-08-05-machine-operation-routing-read-only-argv-green-evidence-v1.md:4
records/development/2026-08-17-claude-subagent-backend-implementation-evidence-v1.md:0
records/development/2026-08-05-historical-todo-issue-intake-v4-closure-test-receipt-v1.json:0
records/development/2026-08-03-work-2-intent-glossary-candidate-v1.md:3
records/development/2026-08-04-reviewcompass2-issue-path-early-pilot-decision.json:0
records/development/2026-08-17-session-log-prefix-interpretation-prescan-v1.md:0
records/development/2026-08-05-machine-operation-routing-read-only-argv-green-test-receipt-v1.json:0
records/development/2026-08-04-work-4a-v2-revert-green-test-receipt-v1.json:0
records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md:9
records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v2.md:0
records/development/2026-08-08-redaction-production-entry-completion-projection-input-v1.json:0
records/development/2026-08-15-safe-storage-capability-search-formal-execution-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-test-receipt-v1.json:0
records/development/2026-08-17-claude-subagent-verbose-argument-correction-decision-v1.md:0
records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md:0
records/development/2026-08-05-work-4a-v3-3-actual-comparison-discovery-evidence-v1.md:7
records/development/2026-08-04-work-4a-v3-1-acceptance-red-evidence-v1.md:0
records/development/2026-08-03-work-1b-completed-next-green-evidence-v1.md:10
records/development/2026-08-04-work-4a-v3-1-plan-alignment-failure-test-receipt-v1.json:0
records/development/2026-08-13-python-313-development-environment-migration-bootstrap-correction-review-v1.md:0
records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-rereview-v1.md:5
records/development/2026-08-17-request-builder-product-acceptance-decision-v1.md:4
records/development/2026-08-04-session-transcript-eventual-preservation-limited-capture-receipt-v1.json:0
records/development/2026-08-04-session-transcript-eventual-preservation-red-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-bootstrap-red-evidence-v1.md:0
records/development/2026-08-15-one-requirement-candidate-consistency-check-contract-v2-independent-rereview-v1.md:0
records/development/2026-08-07-verification-boundary-layer2-green-evidence-v1.md:0
records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json:0
records/development/2026-08-12-stage2-official-test-entry-restoration-evidence-v1.md:16
records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-independent-completion-review-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-boundary-2-tdd-evidence-v1.md:0
records/development/2026-08-05-work-4a-v3-1-plan-alignment-green-test-receipt-v1.json:0
records/development/2026-08-05-record-generation-issue-plan-proposal-test-receipt-v1.json:0
records/development/2026-08-03-work-3-completion-decision.json:0
records/development/2026-08-03-work-3-nfr-verification-profile-candidate-v1.json:0
records/development/2026-08-08-egress-b-check-decision-v1.md:0
records/development/2026-08-03-work-2-candidate-timestamp-improvement.md:3
records/development/2026-08-07-verification-boundary-layer3-red-evidence-v1.md:0
records/development/2026-08-16-review-tooling-formalization-study-v1.md:0
records/development/2026-08-05-v4-issue-persistence-red-evidence-v1.md:1
records/development/2026-08-05-task-contract-source-pin-green-test-receipt-v1.json:0
records/development/2026-08-14-stage3-known-correct-state-witness-start-review-v1.md:0
records/development/2026-08-03-work-1-fixed-input-evidence.md:12
records/development/2026-08-18-review-plan-defaults-evidence-measurements-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v1-decision.json:0
records/development/development-policy-v3.json:0
records/development/2026-08-18-review-plan-defaults-prescan-v1.md:0
records/development/2026-08-16-reviewer-launch-adapter-v2-independent-review-v1.md:0
records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md:7
records/development/2026-08-15-formal-code-reuse-search-one-operation-entry-implementation-plan-v1.md:0
records/development/2026-08-04-layout-baseline-v2-approval-decision.json:0
records/development/2026-08-15-safe-storage-provisional-g26-reuse-search-attestation-v2.json:0
records/development/2026-08-04-work-unit-commit-reminder-completion-evidence-v1.md:8
records/development/2026-08-13-cleanup-decision-scope-and-lifecycle-policy-adoption-v1.md:0
records/development/2026-08-18-operational-metrics-reuse-search-plan-v1.json:0
records/development/2026-08-17-request-builder-contract-adoption-decision-v1.md:4
records/development/2026-08-15-one-design-acceptance-contract-internal-challenge-v1.md:0
records/development/2026-08-17-reviewer-launch-adapter-product-acceptance-decision-v1.md:5
records/development/2026-08-14-stage3-completion-claude-overall-review-result-v1.md:0
records/development/2026-08-05-v4-issue-persistence-red-test-receipt-v1.json:0
records/development/2026-08-17-evaluation-recoverability-map-v1.md:0
records/development/2026-08-15-safe-storage-preimplementation-code-management-routing-evidence-v1.md:3
records/development/2026-08-06-intake-v4-declaration-red-map-v1.json:0
records/development/2026-08-03-work-3-completion-evidence-v1.md:10
records/development/2026-08-11-development-venv-entrypoint-sync-green-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-implementation-task-contract-test-receipt-v1.json:0
records/development/2026-08-04-project-manifest-v2-completion-evidence-v1.md:5
records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-start-review-v1.md:0
records/development/2026-08-17-claude-bootstrap-binary-pin-update-decision-v1.md:0
records/development/2026-08-04-development-venv-red-test-receipt-v1.json:0
records/development/2026-08-08-egress-name-contract-adjudication-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-closure-test-receipt-v1.json:0
records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md:0
records/development/2026-08-07-four-rulings-decision-v1.md:0
records/development/2026-08-14-recovery-plan-v5-stage4-lightweight-code-cleanup-boundary-amendment-decision-v1.md:0
records/development/2026-08-07-work4b-a1-integration-exclusions-red-evidence-v1.md:0
records/development/2026-08-13-stage2-minimum-trust-foundation-completion-candidate-v1.md:3
records/development/2026-08-03-work-3-requirements-artifact-layout-decision.json:0
records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-review-v1.md:7
records/development/2026-08-17-claude-subagent-backend-prescan-v1.md:0
records/development/2026-08-16-external-reviewer-single-send-live-e2e-evidence-v1.md:0
records/development/2026-08-07-layer3-reuse-search-attestation-v1.json:0
records/development/2026-08-18-roots-module-pin-addition-decision-v1.md:0
records/development/2026-08-06-frozen-lane-guidance-correction-decision-v1.md:3
records/development/2026-08-15-one-design-acceptance-boundary1-green-evidence-v1.md:0
records/development/2026-08-08-shared-function-adversarial-review-v1.md:0
records/development/2026-08-09-work7a-checkout-relocation-precursor-completion-projection-input-v1.json:0
records/development/2026-08-15-one-item-review-product-acceptance-decision-v1.md:4
records/development/2026-08-13-python-313-pycache-correction-start-review-v1.md:6
records/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-independent-completion-review-v1.md:0
records/development/2026-08-05-machine-operation-routing-read-only-argv-red-evidence-v1.md:0
records/development/claude-bootstrap-send-manifest-v1.json:0
records/development/2026-08-06-intent-damage-declaration-red-map-v1.json:0
records/development/2026-08-03-work-3-unified-requirements-promotion-green-test-receipt-v2.json:0
records/development/2026-08-17-session-log-record-run-reuse-search-attestation-v1.json:0
records/development/2026-08-04-work-4a-v3-data-root-initialization-evidence-v1.md:0
records/development/2026-08-16-three-provider-live-check-evidence-v1.md:0
records/development/2026-08-07-reuse-search-freshness-reuse-search-attestation-v1.json:0
records/development/2026-08-03-work-1b-completed-next-red-evidence-v1.md:0
records/development/2026-08-03-development-policy-v5-green-test-receipt-v2.json:0
records/development/2026-08-04-work-unit-commit-reminder-green-test-receipt-v1.json:0
records/development/2026-08-17-review-tooling-module-pause-decision-v1.md:0
records/development/2026-08-08-consolidation-digest-family-materials-v1.md:0
records/development/2026-08-05-work5a-first-real-review-acceptance-records-v1.json:0
records/development/2026-08-15-committed-source-formal-search-precheck-decision-v1.md:0
records/development/2026-08-15-one-item-review-implementation-start-review-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v2-decision.json:0
records/development/2026-08-17-rq2-apparatus-reuse-search-attestation-v1.json:0
records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-scope-correction-review-v1.md:0
records/development/2026-08-07-candidate-ranking-v2.json:0
records/development/2026-08-11-mechanical-review-plan-claude-bootstrap-review-v1.md:0
records/development/2026-08-16-reviewer-launch-e2e-attempt2-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-005-post-write-verification-receipt-v1.json:0
records/development/2026-08-13-cleanup-decision-scope-policy-review-completion-decision-v1.md:0
records/development/2026-08-03-work-1b-green-evidence-v1.md:5
records/development/2026-08-15-session-artifact-safe-storage-boundary-1-tdd-evidence-v1.md:0
records/development/2026-08-03-work-2-candidate-timestamp-repair-evidence-v1.md:6
records/development/2026-08-05-work-4a-rebuild-design-v3-2-approval-decision-v1.md:0
records/development/2026-08-05-task-python-cache-ast-boundary-green-test-receipt-v1.json:0
records/development/2026-08-03-work-3-nfr-verification-profile-evidence-v1.md:0
records/development/2026-08-10-egress-guard-fix-evidence-v1.md:14
records/development/2026-08-06-work6a-cl-6a-09-completion-decision-v1.md:0
records/development/2026-08-16-one-item-review-safe-projection-independent-completion-review-v1.md:5
records/development/2026-08-15-one-requirement-candidate-consistency-check-adoption-decision-v1.md:0
records/development/2026-08-08-egress-method-conclusion-decision-v1.md:0
records/development/2026-08-17-vertical-a-request-builder-reuse-search-attestation-v1.json:0
records/development/2026-08-06-work6a-red-entry-projection-input-v1.json:0
records/development/development-policy-v2.json:0
records/development/2026-08-11-claude-bootstrap-review-repair-green-evidence-v1.md:0
records/development/2026-08-05-record-generation-todo-green-test-receipt-v1.json:0
records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-test-receipt-v1.json:0
records/development/2026-08-17-vertical-a-request-builder-prescan-v1.md:0
records/development/2026-08-14-stage5-g25-session-artifact-entry-claude-completion-review-result-v1.md:0
records/development/2026-08-05-todo-update-transaction-boundary-red-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md:10
records/development/2026-08-08-consolidation-lane-summary-v1.md:0
records/development/2026-08-13-stage3-g04-role-classification-evidence-v1.md:0
records/development/2026-08-13-work5b-contract-v2-content-digest-correction-stopped-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-boundary4-completion-evidence-v1.md:4
records/development/2026-08-07-preservation-layout-v3-migration-evidence-v1.md:0
records/development/2026-08-07-work4b-a1-integration-exclusions-declaration-red-map-v1.json:0
records/development/2026-08-07-reuse-search-externalization-reuse-search-attestation-v1.json:0
records/development/2026-08-07-work4b-d-ledger-first-operation-evidence-v1.md:0
records/development/2026-08-18-reuse-search-cli-defaults-prescan-v1.md:0
records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md:0
records/development/2026-08-17-reviewer-bridge-reuse-search-plan-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-resolution-verdict-candidate-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-candidate-triage-completion-evidence-v1.md:0
records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md:12
records/development/2026-08-16-one-item-review-safe-projection-green-evidence-v1.md:0
records/development/2026-08-03-work-3-requirements-coverage-evidence-v1.md:2
records/development/2026-08-14-recovery-plan-v5-stage3-test-authority-consistency-amendment-decision-v1.md:0
records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-decision-v1.md:4
records/development/2026-08-05-task-python-cache-ast-boundary-red-evidence-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-reassessment-v3.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-decision.json:0
records/development/2026-08-07-redaction-environment-rules-red-evidence-v1.md:0
records/development/2026-08-17-reviewer-launch-permission-grant-discovery-v1.md:0
records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-scope-one-time-review-v1.md:0
records/development/2026-08-16-external-reviewer-single-send-v5-adoption-decision-v1.md:0
records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-correction-evidence-v1.md:2
records/development/2026-08-07-layer1-remainder-reuse-search-attestation-v1.json:0
records/development/2026-08-18-plan-writer-prescan-commands-v1.json:0
records/development/2026-08-15-capability-reuse-search-work4a-alignment-correction-decision-v1.md:0
records/development/2026-08-15-one-item-review-boundary6-green-evidence-v1.md:0
records/development/2026-08-04-session-transcript-eventual-preservation-storage-decision.json:0
records/development/2026-08-08-shared-function-digest-green-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-task-contract-v2-completion-evidence-v1.md:0
records/development/2026-08-07-adversarial-remedy-i4-declaration-red-map-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-closure-completion-evidence-v1.md:0
records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-correction-review-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-v4-green-test-receipt-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-implementation-task-contract-completion-evidence-v1.md:0
records/development/2026-08-18-operational-metrics-prescan-v1.md:0
records/development/2026-08-16-g20-live-e2e-order-v1.json:0
records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-decision-v1.md:0
records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-adoption-decision-v1.md:5
records/development/2026-08-04-issue-resolution-pilot-wi-006-completion-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-triage-green-test-receipt-v1.json:0
records/development/2026-08-15-one-design-acceptance-independent-correction-rereview-v1.md:0
records/development/2026-08-12-stage2-minimum-trust-foundation-completion-review-v1.md:0
records/development/2026-08-16-one-requirement-candidate-consistency-check-independent-completion-review-v1.md:7
records/development/2026-08-18-llm-machine-split-audit-v1.md:0
records/development/2026-08-14-stage3-g01-authority-reference-reassessment-evidence-v1.md:3
records/development/2026-08-17-claude-subagent-backend-reuse-search-plan-v1.json:0
records/development/2026-08-15-one-item-review-boundary3-green-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-plan-v2-proposal-test-receipt-v1.json:0
records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json:0
records/development/2026-08-18-cli-defaults-rollout-evidence-commands-v1.json:0
records/development/2026-08-04-session-transcript-eventual-preservation-storage-candidate-v1.json:0
records/development/2026-08-18-session-log-exit-code-reuse-search-plan-v1.json:0
records/development/2026-08-15-safe-storage-formal-code-reuse-search-attestation-v2.json:0
records/development/2026-08-06-work5a-contract-v2-review-run-evidence-v1.md:8
records/development/2026-08-16-external-send-scan-refinement-v1-self-review-v1.md:0
records/development/2026-08-15-one-item-review-boundary1-red-evidence-v1.md:0
records/development/2026-08-17-request-builder-union-model-check-observation-v1.json:0
records/development/2026-08-05-machine-operation-routing-task-python-cache-green-first-receipt-v1.json:0
records/development/2026-08-04-layout-baseline-v3-project-first-red-evidence-v1.md:0
records/development/2026-08-05-todo-evidence-reference-count-correction-v1.md:0
records/development/2026-08-07-work4b-a2-candidate-ranking-green-evidence-v1.md:3
records/development/2026-08-17-session-log-prefix-interpretation-implementation-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-task-python-cache-approval-first-receipt-v1.json:0
records/development/2026-08-06-authority-reference-digest-drift-observation-v1.json:0
records/development/2026-08-10-official-oracle-fix-test-receipt-v1.json:0
records/development/2026-08-13-test-growth-nodeid-candidates-v1.txt:0
records/development/2026-08-18-session-log-exit-code-vocabulary-prescan-v1.md:0
records/development/2026-08-03-work-1b-red-evidence-v1.md:7
records/development/2026-08-04-issue-resolution-pilot-wi-002-red-evidence-v1.md:0
records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-attestation-v1.json:0
records/development/2026-08-13-stage3-g04-role-classification-independent-completion-review-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-independent-completion-review-v1.md:0
records/development/2026-08-03-work-3-requirements-artifact-layout-evidence-v1.md:1
records/development/2026-08-08-digest-family-consolidation-outcome-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-bootstrap-resume-decision.json:0
records/development/2026-08-12-stage2-official-test-entry-restoration-scope-correction-decision-v1.md:0
records/development/2026-08-17-claude-subagent-e2e-evidence-v1.md:0
records/development/2026-08-17-request-builder-e2e-evidence-v1.md:0
records/development/2026-08-05-task-python-cache-ast-boundary-green-evidence-v1.md:0
records/development/2026-08-18-operational-metrics-dataset-v2.json:0
records/development/2026-08-03-work-1-corrective-snapshot-v1.json:0
records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-evidence-v1.md:0
records/development/2026-08-17-e2e-012-002-tier3-acceptance-v1.md:0
records/development/2026-08-13-cleanup-decision-scope-policy-delta-review-v1.md:0
records/development/2026-08-04-work-4a-v2-revert-map-v1.md:0
records/development/2026-08-07-work4b-d-ledger-reuse-decision-v1.md:0
records/development/2026-08-18-measurement-block-plan-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v4-test-receipt-v1.json:0
records/development/2026-08-07-work4b-b-reuse-search-freshness-red-evidence-v1.md:0
records/development/2026-08-06-checklist-authority-reference-digest-repair-evidence-v1.md:0
records/development/2026-08-05-task-contract-lifecycle-status-session-transcript-v1.json:0
records/development/2026-08-03-work-1b-session-e2e-red-evidence-v1.md:7
records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json:0
records/development/2026-08-13-stage3-first-test-cleanup-implementation-approval-decision-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-003-projection-input-v1.json:0
records/development/2026-08-13-test-growth-state-pinning-current-validity-decision-v1.md:0
records/development/2026-08-03-work-1b-completion-decision.json:0
records/development/2026-08-16-external-reviewer-single-send-v4-limited-rereview-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-candidate-test-receipt-v2.json:0
records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md:0
records/development/2026-08-10-common-guard-fix-evidence-v1.md:11
records/development/2026-08-17-checklist-freeze-and-overview-decision-v1.md:0
records/development/2026-08-15-one-design-acceptance-contract-v2-independent-review-v1.md:0
records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md:1
records/development/development-policy-v5.json:0
records/development/2026-08-03-session-transcript-source-formats-completion-evidence-v1.md:14
records/development/2026-08-05-v4-human-triage-decisions-test-receipt-v1.json:0
records/development/2026-08-07-verification-boundary-layer3-green-evidence-v1.md:0
records/development/2026-08-08-redaction-registration-preservation-green-test-receipt-v1.json:0
records/development/2026-08-17-launch-metrics-reuse-search-attestation-v1.json:0
records/development/2026-08-13-stage3-first-test-cleanup-implementation-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-candidate-triage-green-test-receipt-v2.json:0
records/development/2026-08-04-issue-resolution-pilot-wi-004-red-evidence-v1.md:0
records/development/2026-08-10-common-guard-fix-test-receipt-v2.json:0
records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-start-review-v1.md:0
records/development/2026-08-07-work4b-reuse-search-declaration-red-map-v1.json:0
records/development/2026-08-17-deployment-policy-decision-v1.md:0
records/development/2026-08-05-task-contract-source-pin-todo-compaction-v1.json:0
records/development/2026-08-13-stage3-g06-common-guards-reassessment-correction-review-v1.md:0
records/development/2026-08-04-work-4a-rebuild-design-v3-1-approval-decision-v1.md:0
records/development/2026-08-13-review-target-process-connection-correction-review-v1.md:0
records/development/2026-08-16-external-reviewer-single-send-v3-independent-review-v1.md:0
records/development/2026-08-04-work-4a-rebuild-design-v2-approval-decision-v1.md:0
records/development/2026-08-18-reuse-search-cli-defaults-evidence-v1.md:3
records/development/2026-08-04-issue-resolution-pilot-wi-003-completion-evidence-v1.md:3
records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v2.md:0
records/development/2026-08-07-intake-v4-red-map-supersede-decision-v1.md:0
records/development/2026-08-05-machine-operation-routing-read-only-argv-approval-decision-v1.md:6
records/development/2026-08-13-stage3-g07-declaration-red-contract-reassessment-independent-completion-review-v1.md:0
records/development/2026-08-06-work6a-evidence-correction-v1.md:4
records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-v1.md:9
records/development/2026-08-08-egress-a1prime-comparison-v1.md:0
records/development/2026-08-14-work5b-contract-test-cleanup-evidence-v1.md:0
records/development/2026-08-07-unreviewed-work-review-backlog-observation-v1.json:0
records/development/2026-08-04-work-4a-v3-1-acceptance-green-test-receipt-v1.json:0
records/development/2026-08-06-work6a-green-completed-projection-input-v1.json:0
records/development/2026-08-08-redaction-production-entry-independent-review-evidence-v1.md:6
records/development/2026-08-09-work7a-four-root-separation-independent-review-test-receipt-v1.json:0
records/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-evidence-v1.md:3
records/development/2026-08-08-todo-handoff-unified-verification-green-evidence-v1.md:10
records/development/2026-08-03-work-3-nfr-verification-profile-completion-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-model-selection-green-evidence-v1.md:0
records/development/2026-08-10-authority-reference-checker-green-test-receipt-v1.json:0
records/development/2026-08-06-session-transcript-current-codex-recapture-receipt-v1.json:0
records/development/2026-08-17-rq1-apparatus-first-measurement-evidence-v1.md:0
records/development/2026-08-06-work5a-contract-v2-review-acceptance-records-v1.json:0
records/development/2026-08-07-work4b-b-reuse-search-freshness-green-evidence-v1.md:0
records/development/2026-08-15-python-venv-entry-correction-evidence-v1.md:0
records/development/2026-08-06-intake-v4-evidence-correction-v1.md:0
records/development/2026-08-07-adversarial-review-batch2-redaction-v1.md:0
records/development/2026-08-17-rq1-apparatus-reuse-search-attestation-v1.json:0
records/development/2026-08-05-work5a-provenance-closure-repair-green-evidence-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-candidate-selection-v1.md:0
records/development/2026-08-03-work-3-source-identity-stale-decision.json:0
records/development/2026-08-07-work4b-main-design-bundle-approval-decision-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-bootstrap-green-test-receipt-v1.json:0
records/development/2026-08-15-safe-storage-preimplementation-code-management-search-evidence-v1.md:6
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-red-evidence-v1.md:0
records/development/2026-08-18-placement-root-resolution-prescan-v1.md:0
records/development/2026-08-08-v4-issue-resolution-persistence-gap-observation-v1.json:0
records/development/2026-08-07-adversarial-remedy-batch1-reuse-search-attestation-v1.json:0
records/development/2026-08-15-session-artifact-safe-storage-final-verification-evidence-v3.md:0
records/development/2026-08-15-tdd-implementation-boundary-precheck-policy-decision-v1.md:0
records/development/2026-08-08-consolidation-eval2-approval-decision-v1.md:0
records/development/2026-08-04-layout-boundary-corrective-rework-evidence-v1.md:0
records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-evidence-v1.md:0
records/development/2026-08-18-contract-014-canonical-sequence-gaps-observation-v1.md:0
records/development/2026-08-16-one-item-review-safe-projection-v1-independent-review-v1.md:3
records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json:0
records/development/2026-08-07-checklist-approval-scope-statement-drift-observation-v1.json:0
records/development/2026-08-17-rq2-paired-trial-plan-v1.md:0
records/development/2026-08-04-work-4a-sequence-green-test-receipt-v1.json:0
records/development/2026-08-04-work-4a-v3-acceptance-green-evidence-v1.md:0
records/development/2026-08-16-one-requirement-candidate-consistency-check-product-acceptance-decision-v1.md:0
records/development/2026-08-04-work-unit-commit-reminder-red-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-independent-completion-review-v1.md:0
records/development/2026-08-16-external-reviewer-single-send-correction-rereview-v1.md:0
records/development/2026-08-14-stage3-deferred-quality-concerns-trigger-and-routing-decision-v1.md:0
records/development/2026-08-08-shared-function-bde-green-evidence-v1.md:0
records/development/2026-08-05-work-4a-v3-2-acceptance-green-evidence-v1.md:0
records/development/2026-08-07-verification-boundary-layer3-declaration-red-map-v1.json:0
records/development/2026-08-03-session-transcript-eventual-preservation-documentation-evidence-v1.md:2
records/development/2026-08-15-session-artifact-safe-storage-task-contract-temporary-file-correction-review-v1.md:0
records/development/2026-08-17-free-text-request-type-prescan-v1.md:0
records/development/2026-08-09-work7a-exception-chain-path-correction-green-evidence-v1.md:3
records/development/2026-08-03-work-3-permanent-remediation-green-evidence-v1.md:0
records/development/2026-08-12-clean-development-repository-future-memo-v1.md:0
records/development/2026-08-15-one-requirement-candidate-consistency-check-candidate-v3-limited-rereview-v1.md:0
records/development/2026-08-03-work-3-permanent-remediation-full-test-receipt-v3.json:0
records/development/2026-08-04-issue-resolution-pilot-plan-revision-red-evidence-v1.md:0
records/development/2026-08-03-session-transcript-source-formats-green-test-receipt-v1.json:0
records/development/2026-08-05-v4-human-triage-persistence-red-evidence-v1.md:1
records/development/2026-08-17-review-path-design-principles-memo-v1.md:0
records/development/2026-08-13-stage3-g06-common-guards-reassessment-evidence-v1.md:0
records/development/2026-08-03-work-3-requirements-baseline-evidence-v1.md:12
records/development/2026-08-10-pilot-review-method-positioning-decision-v1.md:0
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-attestation-v1.json:0
records/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-independent-completion-review-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-boundary-7-tdd-evidence-v1.md:0
records/development/2026-08-13-review-target-process-connection-bootstrap-correction-review-v1.md:0
records/development/2026-08-17-rq2-case-answer-key-v2.md:8
records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json:0
records/development/2026-08-12-stage2-official-test-entry-restoration-scope-extension-decision-v1.md:0
records/development/2026-08-17-rq2-experiment-plan-prescan-v1.md:0
records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json:0
records/development/2026-08-16-egress-sensitive-scan-false-positive-observation-v1.json:0
records/development/2026-08-04-work-4a-v1-prototype-removal-green-test-receipt-v1.json:0
records/development/2026-08-04-commit-handoff-stability-red-evidence-v1.md:0
records/development/2026-08-04-work-4a-v1-prototype-removal-map-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-006-green-test-receipt-v1.json:0
records/development/2026-08-13-test-growth-nodeid-enumeration-evidence-v1.md:4
records/development/2026-08-07-work4b-a2-candidate-ranking-declaration-red-map-v1.json:0
records/development/2026-08-07-adversarial-remedy-i4-decision-v1.md:0
records/development/2026-08-05-semantic-commit-minimal-guards-green-test-receipt-v1.json:0
records/development/2026-08-17-rq2-preregistration-v1.md:2
records/development/2026-08-17-adversarial-fixture-catalog-observation-v1.json:0
records/development/2026-08-03-work-3-requirements-artifact-runtime-red-evidence-v1.md:2
records/development/2026-08-11-claude-bootstrap-model-selection-review-plan-v1.json:0
records/development/2026-08-03-work-2-candidate-timestamp-decision.json:0
records/development/2026-08-05-machine-operation-routing-task-python-cache-red-evidence-v1.md:0
records/development/2026-08-05-task-contract-lifecycle-status-todo-compaction-v1.json:0
records/development/2026-08-14-recovery-plan-v5-stage5-completion-decision-v1.md:0
records/development/2026-08-17-request-builder-v1-self-review-v1.md:0
records/development/2026-08-13-stage3-g07-declaration-red-contract-reassessment-evidence-v1.md:0
records/development/2026-08-06-deep-dive-stop-rule-decision-v1.md:1
records/development/2026-08-15-session-artifact-safe-storage-final-verification-evidence-v2.md:0
records/development/2026-08-07-adversarial-remedy-batch1-declaration-red-map-v1.json:0
records/development/2026-08-07-llmgp-external-review-assets-observation-v1.json:0
records/development/2026-08-05-task-contract-lifecycle-status-early-pilot-v1.json:0
records/development/2026-08-09-work7a-four-root-separation-independent-review-evidence-v1.md:6
records/development/2026-08-15-session-artifact-safe-storage-boundary-9-tdd-evidence-v1.md:0
records/development/2026-08-03-work-3-permanent-remediation-full-test-receipt-v2.json:0
records/development/2026-08-07-redaction-rules-absent-observation-v1.json:0
records/development/2026-08-03-work-1b-completion-candidate-v1.md:9
records/development/2026-08-08-consolidation-family-a-materials-v1.md:0
records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-evidence-v1.md:7
records/development/2026-08-17-launch-metrics-reuse-search-plan-v1.json:0
records/development/2026-08-05-triage-authority-boundary-test-receipt-v1.json:0
records/development/2026-08-05-triage-machine-operation-root-issue-test-receipt-v1.json:0
records/development/2026-08-15-session-artifact-safe-storage-boundary-4-tdd-evidence-v1.md:0
records/development/2026-08-18-review-plan-defaults-plan-v1.json:0
records/development/2026-08-03-work-3-completion-green-test-receipt-v1.json:0
records/development/2026-08-15-one-design-acceptance-implementation-start-review-v1.md:0
records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-independent-overall-review-v1.md:9
records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-claude-overall-review-result-v1.md:0
records/development/2026-08-11-mechanical-review-plan-claude-bootstrap-v1.json:0
records/development/2026-08-15-safe-storage-code-reuse-search-reference-investigation-v1.md:6
records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-plan-v1.json:0
records/development/2026-08-18-cli-defaults-rollout-prescan-commands-v2.json:0
records/development/2026-08-07-routine-ledger-reuse-search-attestation-v1.json:0
records/development/2026-08-07-adversarial-review-batch1-new-modules-v1.md:0
records/development/2026-08-11-claude-bootstrap-model-selection-review-v1.md:0
records/development/2026-08-16-reviewer-launch-e2e-attempt1-evidence-v1.md:0
records/development/2026-08-07-adversarial-remedy-i4-reuse-search-attestation-v1.json:0
records/development/2026-08-10-all-reviewcompass3-codex-session-capture-evidence-v1.md:3
records/development/2026-08-17-claude-subagent-backend-v1-self-review-v1.md:0
records/development/2026-08-14-issue-resolution-v4-maturity-reassessment-independent-completion-review-v1.md:6
records/development/2026-08-07-redaction-rules-design-approval-decision-v1.md:0
records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md:4
records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-start-review-v1.md:5
records/development/2026-08-15-session-artifact-safe-storage-option-c-implementation-start-decision-v1.md:0
records/development/2026-08-11-claude-bootstrap-model-selection-human-decision-v1.md:0
records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md:52
records/development/2026-08-18-review-plan-defaults-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/red-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/review-repair-correction-declaration-red-map-v2.json:0
records/development/2026-08-11-claude-bootstrap-manifests/claude-2.1.220-result-schema-v1.json:0
records/development/2026-08-11-claude-bootstrap-manifests/red-test-implementation-request-v2.md:0
records/development/2026-08-11-claude-bootstrap-manifests/review-repair-declaration-red-map-v2.json:0
records/development/2026-08-11-claude-bootstrap-manifests/review-repair-red-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/process-call-baseline-v1.json:0
records/development/2026-08-11-claude-bootstrap-manifests/review-repair-correction-red-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/green-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/red-test-prompt-quality-round-1-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/red-test-implementation-request-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/declaration-red-map-v1.json:0
records/development/2026-08-11-claude-bootstrap-manifests/red-review-result-v1.md:0
records/development/2026-08-11-claude-bootstrap-manifests/red-test-prompt-finding-human-decision-v1.md:0
records/development/2026-08-18-measurement-block-integrity-guard-prescan-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2-claude-delta-review-result-v1.md:0
records/development/2026-08-07-egress-adversarial-review-v1.md:0
records/development/2026-08-03-work-3-source-identity-stale-completion-evidence-v1.md:3
records/development/2026-08-15-one-design-acceptance-product-acceptance-decision-v1.md:0
records/development/2026-08-07-redaction-rules-reuse-search-attestation-v1.json:0
records/development/2026-08-14-recovery-plan-v5-stage3-created-artifact-completion-condition-amendment-decision-v1.md:0
records/development/2026-08-16-g20-anthropic-check-order-v1.json:0
records/development/2026-08-17-deployment-policy-review-prescan-v1.md:0
records/development/2026-08-15-one-item-review-boundary2-green-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-task-python-cache-green-test-receipt-v1.json:0
records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json:0
records/development/2026-08-07-fixed-source-kind-evidence-v1.md:0
records/development/2026-08-10-issue-resolution-v4-green-evidence-v1.md:6
records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-correction-review-v1.md:0
records/development/2026-08-07-work4b-c-externalization-green-evidence-v1.md:0
records/development/2026-08-05-work-4a-v3-2-design-fix-green-test-receipt-v1.json:0
records/development/2026-08-07-work4b-c-externalization-red-evidence-v1.md:0
records/development/2026-08-15-capability-reuse-search-work4a-alignment-implementation-evidence-v1.md:0
records/development/2026-08-05-record-generation-todo-green-evidence-v1.md:2
records/development/2026-08-14-stage3-test-authority-consistency-policy-correction-one-time-review-v1.md:6
records/development/2026-08-16-reviewer-launch-adapter-contract-adoption-decision-v1.md:3
records/development/2026-08-15-safe-storage-formal-code-reuse-search-one-operation-execution-evidence-v1.md:0
records/development/2026-08-15-one-item-review-synthetic-acceptance-evidence-v1.md:0
records/development/2026-08-12-stage1-current-position-completion-decision-v1.md:0
records/development/2026-08-07-work5b-discussion-outcomes-decision-v1.md:2
records/development/2026-08-05-v4-issue-persistence-green-test-receipt-v1.json:0
records/development/2026-08-16-minimal-operation-contract-execution-correction-evidence-v1.md:0
records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-independent-completion-review-v1.md:2
records/development/2026-08-18-review-plan-defaults-prescan-measurements-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-v4-approval-completion-evidence-v1.md:0
records/development/2026-08-05-issue-intake-v4-green-test-receipt-v1.json:0
records/development/2026-08-14-stage3-g01-authority-reference-guard-activation-independent-completion-review-v1.md:2
records/development/2026-08-16-external-reviewer-single-send-green-evidence-v1.md:0
records/development/2026-08-05-work-4a-v3-3-design-fix-green-test-receipt-v1.json:0
records/development/2026-08-15-one-item-review-boundary4-red-evidence-v1.md:0
records/development/2026-08-05-record-generation-todo-boundary-repair-green-test-receipt-v1.json:0
records/development/2026-08-14-session-artifact-safe-storage-task-contract-definition-challenge-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-004-completion-evidence-v1.md:2
records/development/2026-08-17-session-log-record-run-reuse-search-plan-v1.json:0
records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-v3-delta-review-v1.md:0
records/development/2026-08-10-guard-backfill-autonomous-authorization-v1.md:0
records/development/2026-08-13-stage3-g07-declaration-red-contract-correction-independent-completion-review-v1.md:0
records/development/2026-08-07-redaction-environment-rules-declaration-red-map-v2.json:0
records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md:6
records/development/2026-08-18-cli-defaults-rollout-prescan-measurements-v2.md:0
records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-independent-completion-review-v1.md:0
records/development/2026-08-03-work-1b-durable-capture-red-evidence-v1.md:6
records/development/2026-08-07-verification-boundary-approval-decision-v1.md:0
records/development/2026-08-06-work6a-cl-6a-01-02-03-completion-decision-v1.md:0
records/development/2026-08-10-official-oracle-fix-evidence-v1.md:14
records/development/2026-08-16-external-send-scan-refinement-completion-review-v1.md:0
records/development/2026-08-18-rq2-adjudication-and-byproducts-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-triage-completion-evidence-v1.md:0
records/development/2026-08-14-stage3-known-correct-state-witness-execution-evidence-v1.md:0
records/development/2026-08-18-rq2-scoring-judgments-v2.json:0
records/development/development-policy-v4.json:0
records/development/2026-08-12-pilot-git-runtime-read-only-guard-bootstrap-start-review-v1.md:0
records/development/2026-08-08-test-sha256-fixture-duplication-observation-v1.json:0
records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v3.md:0
records/development/2026-08-18-cli-defaults-rollout-evidence-v1.md:0
records/development/2026-08-14-stage3-g06-common-guards-cleanup-evidence-v1.md:0
records/development/2026-08-07-work5b-implementation-task-contract-v2.json:0
records/development/2026-08-07-work4b-reuse-search-green-evidence-v1.md:0
records/development/2026-08-12-claude-bootstrap-diagnostic-and-json-fence-human-decision-v1.md:0
records/development/2026-08-07-work5b-checker-first-run-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-plan-v4-completion-evidence-v1.md:0
records/development/2026-08-07-work5b-red-map-checker-red-evidence-v1.md:0
records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md:0
records/development/2026-08-17-reviewer-bridge-reuse-search-attestation-v1.json:0
records/development/2026-08-07-todo-handoff-verification-gap-observation-v1.json:0
records/development/2026-08-18-review-plan-defaults-evidence-commands-v1.json:0
records/development/2026-08-17-session-log-prefix-interpretation-contract-adoption-decision-v1.md:0
records/development/2026-08-10-guard-backfill-priority-decision-v1.md:0
records/development/2026-08-18-measurement-block-nondeterminism-observation-v1.md:0
records/development/2026-08-06-work5a-contract-v2-review-acceptance-decision-v1.md:3
records/development/2026-08-04-commit-handoff-stability-green-test-receipt-v1.json:0
records/development/2026-08-18-rq2-final-metrics-v1.json:0
records/development/2026-08-13-review-target-process-connection-correction-evidence-v1.md:0
records/development/2026-08-17-reuse-search-gate-disconnection-observation-v1.json:0
records/development/2026-08-17-reviewer-bridge-prescan-v1.md:0
records/development/2026-08-05-work-5a-first-review-contract-green-test-receipt-v1.json:0
records/development/2026-08-05-task-python-cache-ast-boundary-green-first-receipt-v1.json:0
records/development/2026-08-15-session-artifact-safe-storage-task-contract-adoption-decision-v1.md:0
records/development/2026-08-14-stage3-g01-authority-reference-reassessment-independent-completion-review-v1.md:3
records/development/2026-08-03-work-3-unified-requirements-promotion-red-evidence-v1.md:0
records/development/2026-08-17-e2e-findings-triage-decision-v1.md:0
records/development/2026-08-03-work-1-fixed-input-evidence-v2.md:5
records/development/2026-08-17-session-log-prefix-interpretation-triage-decision-v1.md:0
records/development/2026-08-06-work6a-red-completed-projection-input-v1.json:0
records/development/2026-08-16-external-reviewer-single-send-impl-self-review-v1.md:0
records/development/2026-08-05-triage-existing-machine-closure-test-receipt-v1.json:0
records/development/2026-08-04-session-transcript-eventual-preservation-implementation-checkpoint-test-receipt-v1.json:0
records/development/2026-08-11-claude-bootstrap-review-repair-correction-green-evidence-v1.md:0
records/development/2026-08-18-rq2-answer-key-vocabulary-format-decision-v1.md:2
records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-independent-completion-review-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-final-verification-evidence-v1.md:0
records/development/2026-08-05-work-4a-v3-2-actual-routine-profile-v2-evidence-v1.md:5
records/development/2026-08-07-fixed-source-kind-decision-v1.md:0
records/development/2026-08-17-free-text-request-type-contract-adoption-decision-v1.md:4
records/development/2026-08-05-work-4a-v3-3-acceptance-green-evidence-v1.md:0
records/development/2026-08-16-external-send-scan-refinement-product-acceptance-decision-v1.md:0
records/development/2026-08-07-redaction-environment-rules-declaration-red-map-v1.json:0
records/development/2026-08-17-reviewer-launch-e2e-attempt5-evidence-v1.md:0
records/development/2026-08-18-operational-metrics-v2-reuse-search-plan-v1.json:0
records/development/2026-08-17-rq1-apparatus-reuse-search-plan-v1.json:0
records/development/2026-08-18-plan-writer-plan-v1.json:0
records/development/2026-08-14-issue-resolution-v4-maturity-reassessment-evidence-v1.md:6
records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-implementation-evidence-v1.md:3
records/development/2026-08-16-reviewer-launch-adapter-implementation-evidence-v1.md:0
records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md:11
records/development/2026-08-13-review-target-classification-process-policy-adoption-decision-v1.md:0
records/development/2026-08-11-claude-bootstrap-review-repair-correction-plan-v1.json:0
records/development/2026-08-05-machine-operation-routing-issue-plan-proposal-test-receipt-v1.json:0
records/development/2026-08-06-work5a-contract-v2-review-acceptance-evidence-v1.md:3
records/development/2026-08-04-work-4a-sequence-approval-decision-v1.json:0
records/development/2026-08-18-review-plan-defaults-prescan-commands-v1.json:0
records/development/2026-08-07-work5b-implementation-task-contract-v1.json:0
records/development/2026-08-11-mechanical-review-plan-scope-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-005-completion-evidence-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-boundary-8-tdd-evidence-v1.md:0
records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md:0
records/development/2026-08-18-cli-defaults-rollout-attestation-v1.json:0
records/development/2026-08-03-work-1-corrective-snapshot-v1-post-commit-verification.json:0
records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md:14
records/development/2026-08-15-session-artifact-safe-storage-boundary-5-tdd-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-boundary3-green-evidence-v1.md:0
records/development/2026-08-07-work5b-checker-green-evidence-v1.md:0
records/development/2026-08-17-claude-subagent-backend-reuse-search-attestation-v1.json:0
records/development/2026-08-05-todo-update-transaction-boundary-final-receipt-v1.json:0
records/development/2026-08-07-integration-exclusions-helper-reuse-search-attestation-v1.json:0
records/development/2026-08-18-operational-metrics-evidence-v1.md:3
records/development/2026-08-17-subagent-allowed-models-approval-v1.md:0
records/development/2026-08-08-work7a-four-root-separation-green-test-receipt-v1.json:0
records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-evidence-v2-one-time-correction-review-v1.md:0
records/development/2026-08-14-recovery-plan-v5-stage4-formal-product-code-identification-amendment-decision-v1.md:0
records/development/2026-08-08-v4-resolution-persistence-deferred-projection-input-v1.json:0
records/development/2026-08-07-local-prefilter-experiment-evidence-v1.md:3
records/development/2026-08-05-task-python-cache-ast-boundary-inspection-improvement-candidate-v1.md:0
records/development/2026-08-05-task-contract-lifecycle-status-todo-compaction-v2.json:0
records/development/2026-08-04-issue-resolution-pilot-wi-007-test-receipt-v1.json:0
records/development/2026-08-04-thread-added-work-plan-checklist-reconciliation-v1.md:0
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-attestation-v3.json:0
records/development/2026-08-14-stage5-g25-session-artifact-entry-receipt-binding-adjudication-v1.md:0
records/development/2026-08-18-plan-writer-attestation-v1.json:0
records/development/2026-08-07-layer2-reuse-search-attestation-v1.json:0
records/development/2026-08-05-v4-issue-persistence-green-evidence-v1.md:0
records/development/2026-08-04-todo-growth-pilot-observation-v1.json:0
records/development/2026-08-07-adversarial-remedy-batch1-green-evidence-v1.md:0
records/development/2026-08-04-development-venv-baseline-completion-evidence-v1.md:0
records/development/2026-08-14-work5b-contract-lifecycle-reassessment-independent-completion-review-v1.md:0
records/development/2026-08-14-stage5-g25-session-artifact-product-entry-acceptance-decision-v1.md:4
records/development/2026-08-07-work4b-b-reuse-search-freshness-declaration-red-map-v1.json:0
records/development/2026-08-05-record-generation-todo-boundary-repair-green-evidence-v1.md:2
records/development/2026-08-16-external-reviewer-single-send-product-acceptance-decision-v1.md:0
records/development/2026-08-04-layout-baseline-v3-project-first-green-evidence-v1.md:0
records/development/2026-08-07-c4-red-verification-green-evidence-v1.md:0
records/development/2026-08-16-minimal-operation-contract-execution-v1-independent-review-v1.md:2
records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md:0
records/development/2026-08-03-work-3-permanent-remediation-full-test-receipt-v1.json:0
records/development/2026-08-07-adversarial-remedy-batch1-declaration-red-map-v2.json:0
records/development/2026-08-05-machine-operation-routing-follow-on-plan-test-receipt-v1.json:0
records/development/2026-08-18-placement-root-resolution-reuse-search-plan-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-wi-004-green-test-receipt-v1.json:0
records/development/2026-08-04-session-transcript-eventual-preservation-completion-evidence-v1.md:2
records/development/2026-08-15-one-item-review-boundary1-green-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-task-python-cache-approval-decision-v1.md:7
records/development/2026-08-03-session-transcript-source-formats-red-evidence-v1.md:0
records/development/2026-08-03-work-3-deferred-scope-completion-evidence-v1.md:0
records/development/2026-08-05-work-4a-rebuild-design-v3-3-approval-decision-v1.md:0
records/development/2026-08-18-plan-writer-prescan-v1.md:0
records/development/2026-08-12-stage1-current-position-and-active-routes-v1.md:13
records/development/2026-08-17-claude-subagent-child-injection-correction-decision-v1.md:0
records/development/2026-08-07-work5b-implementation-ready-decision-v1.md:0
records/development/2026-08-16-minimal-operation-contract-execution-product-acceptance-decision-v1.md:0
records/development/2026-08-11-claude-bootstrap-real-run-host-safety-stop-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-005-projection-input-v1.json:0
records/development/2026-08-16-external-send-scan-refinement-green-evidence-v1.md:4
records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md:4
records/development/2026-08-05-todo-test-projection-cli-green-evidence-v1.md:0
records/development/2026-08-18-review-plan-defaults-attestation-v1.json:0
records/development/2026-08-13-stage2-minimum-trust-foundation-reassessment-candidate-v1.md:0
records/development/2026-08-13-review-target-process-connection-completion-decision-v1.md:0
records/development/2026-08-06-encountered-problem-inventory-v1.md:22
records/development/2026-08-13-stage3-manual-external-review-limit-decision-v1.md:0
records/development/2026-08-18-cli-defaults-rollout-prescan-measurements-v1.md:0
records/development/2026-08-15-one-item-review-contract-adoption-and-implementation-start-decision-v1.md:0
records/development/2026-08-05-v4-human-triage-persistence-green-evidence-v1.md:0
records/development/2026-08-14-recovery-plan-v5-stage4-completion-decision-v1.md:0
records/development/2026-08-18-placement-root-resolution-evidence-v1.md:5
records/development/2026-08-13-python-313-pycache-test-precondition-correction-review-v1.md:0
records/development/2026-08-09-role-neutral-mode-trial-metrics-v1.md:0
records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-improvement-candidate-v1.md:5
records/development/2026-08-16-external-reviewer-single-send-correction-evidence-v1.md:2
records/development/2026-08-04-layout-baseline-v2-green-test-receipt-v1.json:0
records/development/2026-08-18-measurement-block-dogfood-commands-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-wi-006-red-evidence-v1.md:0
records/development/2026-08-07-egress-dry-run-v1/report.md:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-a21df923cfd753b28d806de9e6722b7250e78a675f1227240b2b8abbaf03d944.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-f902a31d157e990c3bcece310c0a89661fb4e6445ebe83d0e4a4c788a1136660.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-cfe3538ce3b845c2ee56e8b32139e198c265f79f1458375e5e8992c67c233815.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-8b55ec30b5a8548d306e266bf390cf82c19260dd3416ee5d4d4c70e86cda2bfb.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-33074bae8791c364c2454d0bfcc0b516631f71578f4828ad61a7c84d988625ad.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-7b9419a10b50996b34863cd134477241ccc725f49673925660e1671b86eb7aba.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-75a047d39853cc8258a965d5f5a8751a206edcab755614ee5e7e30e8fee06dd0.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-f2531b890552700a3b1254545efb1666e26cbb6ff7dcd4d857a7e0ddeb09d65e.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-9fff8caf5e8cc5e6e8e6794b2eaf92c3250284ef6e5719962bcb4a66d7b64b5a.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-1a9a6d1f57989754ac51bada3b92421b028fc7117145e0edff368997396c54a3.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-9021b95b6cd711b84232a9b2a98d3350382fdfa02e770fa7ae6d2ef15bd47d93.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-0e0421e57524dd527c9f6ac35c7c13e7955f432809c695bd6a8cc685ea6eb8eb.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-162ebd725f70fc0129d38fa03d71413e98148b5f8d32ad35571052d9464f2113.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-c1f980897eef129efed5e6298fa316f7cf1babcd12e1d4ec08d5b68c48c3016b.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-51b1d057d1b733a3221270d1e6ca6b2b6e3cc90a085a4b4db3616ff80c9d8791.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-8f0870ef50181943281eb157af12c7f932c8c48b3f2cb0ab42f6b2a85abb3124.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-65119c189785fb2a27db0e937da5c07225d47ea1f788661e9e006f1feb142e9f.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-64d176292d6ff5e4cc1d9719f2a9f8ae738cae928bb806177858a0c0c381262b.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-6d5cd98eada86f9e5e0bb3dc8077fcc66e04e92280628d3b3c332a5297de0ac2.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-611bfa62b31cd8dbe60cd0dac57e80f4c4c8d95a90f167839cd300bdf0425e53.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-aadd85e461f33be1564b3bbcff41255dfae0ac63d57e2f96391c9809bb4f07e9.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-e409774d3698880cb12578ec1ec8adaa67f29dec0831f620f350a51ac388a3ad.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-64c2d08192e20ab1bae63315dba124dd9924f1b61e540b7293b588c8781e0ddd.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-352a4a8729f1da140b9f36b3fef4ed202fc446b6eff7c58fcbb2ee0be140643e.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-771a40d8f831d856afa672790c0c0c2da93388a431b137fa17bdcf4607193d33.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-11f8ae2eb9be2538ee699484c4f4939afa474f46eac23aceaaec13ecdb4f22eb.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-eb8fbe58713e8be007dfbb9a60e810ff7ca7ad39d207a4f73f727bfd1bde502b.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-2bbf36d87072ecd4bba4339ee4f2e75e19bda1e2e9f3abdc96a9aaa56d6e3297.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-a24736556becd6d3f751b157162f37c5b4a2a487437b7e7e5acaed60f307b3ac.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-7e9b28c42d34b787c0d37a670d9bf7a6b8d60c50b6f1f2f4c416201b2926e5cf.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-f8ade1b5d2cdb5f8bb914397ab2535d2605cda32e54e3eb549e548c75201aa40.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-1b35f685d6b3a9ab8857bd8e57550f3a0aadd6afa765cb4d896e575b3502deb0.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-9944fde085831f523110ffd64f804f223961efeb2f6c6e3f6597024ea4c75a2f.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-4a3dffc10cbcd123906c4bf18207c352b2969e447b9c0cab82b971bfa244d31f.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-46aae22ff9b858dd4d4b55f1592d4038f9708e3a3f316e6e87b744d250550a4b.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-c05877206098c4dcc752d4374b1b165322ac278ddb570c1ba529022e745d5a9f.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-35269b32ced8f180121d1debb512a9a118bd1ddcea219a080300d3cc9064a450.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-6378f50d2d511d4626789b90adcd446810ca3f14856aea9937d425c5818b0f78.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-07b6f5562a91955fe94d35211ab648a20c9fa6a656379e116433f6b7fbfde7f5.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-922150c02b6a16fe27c5d3f01ecf14bcc737fff7607cddb566b3ac63e5ab7301.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-252fa2e80a10c199ec013668c7ba4f6ce930b33b69ea70561bc7877cb9232307.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-a04b5394806a4504934b154ab6f4c99c1ff46ffc0bbb32f6ac88cd65f2457f25.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-1ba3403c67ae174ef1eb7cfcff21d8580ba7b6c96dda0b75b9338fc4dcd08f66.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-31e1b6beb2b8524a55567709553f17724ad089d384a50f16e5f9275c0b4ad193.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-bf8fa84b4700e598a3a51552a7dc58e4780cdd7fddb177b23f7a85646951b96c.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-0b67bf7d7664a3a406eb25deb29941710f786537adcaaf46f85e6d56047a9adf.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-c383869aa6b37fce0129ce7b9ab91a52d16b0297b1572d8c7b5d4b26db89ba2d.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-df890b82794ba54f0394756135afcb74b47a1c75d2a6db3138599fd92dce8fe0.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-1dbcf6796fbbe0dad49db1c9c05bd747e27e04643f960fd3c5cc68980f59b0ce.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-51d30a22f683c1122ff32ce45bbe9cbc89c1ab259097c0837b5d528c9550ce03.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-495c8b94fb831891e86ffe87e1effa7991f7e732c07ac16915fb1479f840bbe2.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-fd4f6ce2560ec66bfcd82bcaa67c20e181bd4420e9229b6eaca0dbb8554e3c01.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-fa1d9c3210db3cd08914ae48d74dea006eb64e5fb33f5cebeeb2879e2de341ae.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-a76ea62afbbd28e714e9089952872d3798effdc5b4e3166aa2b5de717eed44e0.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-88ad670484f20f910224d0b44230c1999c6479e3868e71b84511aafc4a3ee53d.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-ec5273614ac4c36a12911a977ff175ac840031db7636870103b28cae80fd1957.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-982111e80d5d85445b7d80df831dc9c96c0122ff1a3a878d994a93009c05d4fc.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-41067e0be1aaf7a6f0e0250c58f2b0ff42ac57180d29e8ec50a0c08dea20dadf.json:0
records/development/2026-08-07-egress-dry-run-v1/payloads/payload-9db55236c00b110d282ac92b8f0e23ac1ccde690f715176cfc2ecaeab499a48a.json:0
records/development/2026-08-07-egress-dry-run-v1/manifest.json:0
records/development/2026-08-18-cli-defaults-rollout-prescan-commands-v1.json:0
records/development/2026-08-08-redaction-registration-preservation-green-evidence-v1.md:5
records/development/2026-08-04-issue-resolution-pilot-bootstrap-green-test-receipt-v3.json:0
records/development/2026-08-13-python-313-development-environment-migration-completion-decision-v1.md:3
records/development/2026-08-13-stage3-g07-declaration-red-contract-correction-evidence-v1.md:0
records/development/2026-08-15-one-item-review-boundary5-red-evidence-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-review-completion-v1.md:0
records/development/2026-08-10-issue-resolution-v4-green-test-receipt-v1.json:0
records/development/2026-08-15-one-item-review-boundary4-green-evidence-v1.md:0
records/development/2026-08-15-committed-source-formal-search-precheck-implementation-evidence-v1.md:0
records/development/2026-08-05-historical-todo-intake-triage-material-v1.md:0
records/development/2026-08-07-red-verification-adoption-decision-v1.md:0
records/development/2026-08-15-one-design-acceptance-boundary4-red-evidence-v1.md:0
records/development/2026-08-18-entry-delegation-form-confirmation-v1.md:0
records/development/2026-08-17-rq2-scoring-judgments-v1.json:0
records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md:2
records/development/2026-08-17-backend-registry-shallow-generalization-observation-v1.json:0
records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-independent-completion-review-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-v3-red-evidence-v1.md:0
records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md:2
records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-correction-review-v1.md:2
records/development/2026-08-08-todo-handoff-unified-verification-projection-input-v1.json:0
records/development/2026-08-07-declaration-red-map-checker-reuse-search-attestation-v1.json:0
records/development/2026-08-08-redaction-production-entry-correction-green-evidence-v1.md:3
records/development/2026-08-04-issue-resolution-pilot-closure-projection-input-v1.json:0
records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md:5
records/development/2026-08-07-adversarial-remedy-i4-green-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-005-red-evidence-v1.md:0
records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md:6
records/development/2026-08-03-work-2-intent-glossary-approval.json:0
records/development/2026-08-06-intake-v4-single-candidate-green-evidence-v1.md:11
records/development/2026-08-04-issue-resolution-pilot-bootstrap-green-test-receipt-v2.json:0
records/development/2026-08-16-g20-real-doc-e2e-order-v1.json:0
records/development/2026-08-14-issue-resolution-v4-use-stop-and-state-reflection-cancellation-independent-completion-review-v1.md:10
records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md:34
records/development/2026-08-12-stage2-minimum-trust-foundation-post-fix-review-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v4-completion-evidence-v1.md:0
records/development/2026-08-05-work5a-provenance-closure-repair-approval-decision-v1.md:2
records/development/2026-08-13-python-313-development-environment-migration-evidence-v1.md:1
records/development/2026-08-10-all-reviewcompass3-codex-session-capture-receipt-v1.json:0
records/development/2026-08-12-stage2-official-test-entry-restoration-scope-extension-start-review-v1.md:0
records/development/2026-08-03-work-3-unified-requirements-promotion-completion-evidence-v1.md:0
records/development/2026-08-14-issue-resolution-v4-use-stop-and-state-reflection-cancellation-decision-v1.md:0
records/development/2026-08-03-work-3-deferred-scope-evidence-v1.md:0
records/development/2026-08-14-recovery-plan-v5-stage3-completion-decision-v1.md:0
records/development/2026-08-12-stage2-official-test-entry-restoration-scope-correction-review-v1.md:0
records/development/2026-08-03-work-1-reconstructability-candidate.md:5
records/development/2026-08-07-sensitive-definition-decision-v1.md:0
records/development/2026-08-14-stage3-completion-candidate-v1.md:0
records/development/2026-08-13-review-target-process-connection-completion-review-v1.md:0
records/development/2026-08-15-one-item-review-boundary6-red-evidence-v1.md:0
records/development/2026-08-14-authority-reference-issue-resolution-start-review-v1.md:5
records/development/2026-08-11-claude-bootstrap-host-route-diagnosis-v1.md:0
records/development/2026-08-07-preservation-layout-v3-migration-receipt-v1.json:0
records/development/2026-08-05-work-4a-v3-2-acceptance-red-evidence-v1.md:0
records/development/2026-08-15-post-recovery-product-development-position-correction-decision-v1.md:0
records/development/2026-08-03-work-3-requirements-artifact-layout-candidate-v1.json:0
records/development/2026-08-18-measurement-block-dogfood-measurements-v1.md:0
records/development/2026-08-14-work5b-contract-lifecycle-reassessment-evidence-v1.md:0
records/development/2026-08-03-work-3-deferred-scope-decision.json:0
records/development/2026-08-04-commit-handoff-stability-decision.json:0
records/development/2026-08-17-rq2-apparatus-reuse-search-plan-v1.json:0
records/development/2026-08-15-session-artifact-safe-storage-implementation-start-review-v1.md:0
records/development/2026-08-15-capability-derived-code-reuse-search-candidate-expansion-correction-evidence-v1.md:0
records/development/2026-08-17-free-text-request-type-reuse-search-plan-v1.json:0
records/development/2026-08-04-work-4a-v3-actual-observation-evidence-v1.md:8
records/development/2026-08-15-formal-code-reuse-search-one-operation-entry-implementation-evidence-v1.md:0
records/development/2026-08-07-egress-stage1-green-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-003-green-test-receipt-v1.json:0
records/development/2026-08-16-minimal-operation-contract-execution-v4-limited-rereview-v1.md:3
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-attestation-v2.json:0
records/development/2026-08-16-handoff-gitignore-record-canonical-mismatch-observation-v1.json:0
records/development/2026-08-15-capability-derived-code-reuse-search-implementation-evidence-v1.md:0
records/development/2026-08-18-operational-metrics-reuse-search-attestation-v1.json:0
records/development/2026-08-07-c4-red-verification-declaration-red-map-v1.json:0
records/development/2026-08-12-stage1-current-position-bootstrap-completion-review-v1.md:0
records/development/2026-08-05-work-5a-first-review-contract-green-evidence-v1.md:0
records/development/claude-bootstrap-human-decision-v1.json:0
records/development/2026-08-13-test-growth-nodeid-enumeration-completion-review-v1.md:4
records/development/2026-08-15-session-artifact-safe-storage-product-acceptance-decision-v1.md:3
records/development/2026-08-03-work-1b-completed-next-decision.json:0
records/development/2026-08-05-work5a-provenance-closure-repair-green-test-receipt-v1.json:0
records/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-scope-independent-completion-review-v1.md:1
records/development/2026-08-05-work5a-provenance-closure-repair-red-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-boundary2-test-correction-evidence-v1.md:0
records/development/2026-08-03-development-policy-v5-red-evidence-v1.md:0
records/development/2026-08-13-review-target-process-connection-implementation-start-decision-v1.md:0
records/development/2026-08-03-work-1-reconstructability-repair-decision.json:0
records/development/2026-08-13-stage3-first-test-cleanup-independent-completion-review-v1.md:0
records/development/2026-08-17-reviewer-launch-e2e-attempt3-evidence-v1.md:0
records/development/2026-08-11-claude-bootstrap-review-repair-plan-v1.json:0
records/development/2026-08-12-stage2-minimum-trust-foundation-start-decision-v1.md:0
records/development/2026-08-16-external-reviewer-single-send-adoption-decision-v1.md:0
records/development/2026-08-17-improvement-candidates-triage-decision-v1.md:0
records/development/2026-08-10-authority-reference-checker-green-evidence-v1.md:7
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v4.json:0
records/development/2026-08-04-issue-resolution-pilot-wi-002-completion-evidence-v1.md:0
records/development/2026-08-06-intent-damage-red-evidence-v1.md:9
records/development/2026-08-04-deployment-project-artifact-boundary-decision.json:0
records/development/2026-08-03-work-1-fixed-input-evidence-v3.md:7
records/development/2026-08-09-work7a-checkout-relocation-precursor-completion-evidence-v1.md:4
records/development/2026-08-16-one-item-review-safe-projection-adoption-decision-v1.md:0
records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md:5
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-candidate-test-receipt-v1.json:0
records/development/2026-08-03-work-1a-layout-evidence-v1.md:7
records/development/2026-08-10-group-c-reset-decision-v1.md:0
records/development/2026-08-16-external-reviewer-single-send-v2-self-review-v1.md:0
records/development/2026-08-18-placement-root-resolution-reuse-search-attestation-v1.json:0
records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-challenge-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-boundary-6-tdd-evidence-v1.md:0
records/development/2026-08-16-one-item-review-safe-projection-product-acceptance-decision-v1.md:0
records/development/2026-08-05-todo-test-projection-cli-red-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-contract-definition-evidence-v1.md:2
records/development/2026-08-08-checklist-revision-r1-record-v1.md:0
records/development/2026-08-15-one-item-review-implementation-start-correction-review-v1.md:0
records/development/2026-08-07-work-4b-minimal-pilot-scope-approval-decision-v1.md:3
records/development/2026-08-04-issue-resolution-pilot-candidate-triage-green-test-receipt-v1.json:0
records/development/2026-08-07-integration-exclusion-entries-candidate-v1.md:0
records/development/2026-08-04-project-manifest-v2-green-test-receipt-v1.json:0
records/development/2026-08-05-work4-first-review-contract-design-approval-decision-v1.md:0
records/development/2026-08-03-work-3-completion-candidate-v1.md:0
records/development/2026-08-10-common-guard-fix-test-receipt-v1.json:0
records/development/2026-08-17-session-log-run-procedure-prescan-v1.md:0
records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md:6
records/development/2026-08-06-session-transcript-current-codex-recapture-evidence-v1.md:8
records/development/2026-08-05-task-contract-source-pin-todo-compaction-v2.json:0
records/development/2026-08-03-session-transcript-eventual-preservation-documentation-test-receipt-v1.json:0
records/development/2026-08-07-redaction-environment-rules-green-evidence-v1.md:0
records/development/2026-08-07-ruling4-deletion-receipt-v1.md:0
records/development/2026-08-11-mechanical-review-plan-green-evidence-v1.md:0
records/development/2026-08-13-stage3-g04-role-classification-evidence-v2-one-time-correction-review-v1.md:0
records/development/2026-08-03-work-1b-durable-capture-green-evidence-v1.md:6
records/development/2026-08-17-session-log-prefix-interpretation-gap-observation-v1.json:0
records/development/2026-08-16-minimal-operation-contract-execution-v3-limited-rereview-v1.md:3
records/development/2026-08-03-session-transcript-eventual-preservation-decision.json:0
records/development/2026-08-07-adversarial-remedy-batch1-decision-v1.md:0
records/development/2026-08-17-reviewer-launch-e2e-attempt4-evidence-v1.md:0
records/development/2026-08-17-rq1-apparatus-prescan-v1.md:0
records/development/2026-08-05-todo-update-transaction-boundary-first-receipt-v1.json:0
records/development/2026-08-04-commit-handoff-stability-completion-evidence-v1.md:8
records/development/2026-08-13-review-target-classification-process-gap-evidence-v1.md:0
records/development/2026-08-17-vertical-a-request-builder-reuse-search-plan-v1.json:0
records/development/2026-08-04-work-4a-rebuild-design-approval-decision-v1.md:0
records/development/2026-08-03-session-transcript-eventual-preservation-implementation-decision.json:0
records/development/2026-08-06-work6a-cl-6a-10-completion-decision-v1.md:0
records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json:0
records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md:4
records/development/2026-08-18-operational-metrics-v2-reuse-search-attestation-v1.json:0
records/development/2026-08-18-measurement-block-integrity-guard-attestation-v1.json:0
records/development/2026-08-08-egress-a1-subagent-judgment-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2-one-time-correction-review-v1.md:0
records/development/2026-08-17-reviewer-launch-e2e-attempt7-success-evidence-v1.md:0
records/development/2026-08-03-work-3-requirements-artifact-layout-completion-evidence-v1.md:3
records/development/2026-08-18-reuse-search-cli-defaults-attestation-v1.json:0
records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-evidence-v1.md:0
records/development/2026-08-15-safe-storage-capability-reuse-human-adjudication-decision-v1.md:0
records/development/2026-08-04-layout-baseline-v2-candidate.json:0
records/development/2026-08-12-stage1-current-position-bootstrap-start-decision-v1.md:0
records/development/2026-08-17-free-text-request-type-reuse-search-attestation-v1.json:0
records/development/2026-08-07-work4b-reuse-search-red-evidence-v1.md:0
records/development/2026-08-05-todo-related-test-path-discovery-improvement-candidate-v1.md:0
records/development/2026-08-16-minimal-operation-contract-execution-adoption-decision-v1.md:0
records/development/2026-08-10-policy-document-retirement-decision-v1.md:3
records/development/2026-08-15-one-requirement-feature-source-contract-definition-evidence-v1.md:5
records/development/2026-08-16-g20-live-e2e-order-v2.json:0
records/development/2026-08-04-work-4a-v3-acceptance-green-test-receipt-v1.json:0
records/development/2026-08-18-measurement-block-attestation-v1.json:0
records/development/2026-08-16-minimal-operation-contract-execution-v2-limited-rereview-v1.md:3
records/development/2026-08-04-conformance-evaluation-scope-relaxation-decision-v1.md:0
records/development/2026-08-07-verification-boundary-layer1-red-evidence-v1.md:0
records/development/2026-08-07-work4b-a2-candidate-ranking-red-evidence-v1.md:4
records/development/2026-08-07-adversarial-review-batch1-legacy-systems-v1.md:0
records/development/2026-08-05-v4-human-triage-persistence-red-test-receipt-v1.json:0
records/development/2026-08-14-work5b-contract-test-cleanup-independent-completion-review-v1.md:0
records/development/2026-08-17-subagent-hardening-env-omission-observation-v1.json:0
records/development/2026-08-10-all-reviewcompass3-codex-session-capture-decision-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v3-decision.json:0
records/development/2026-08-06-test-growth-state-pinning-observation-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-triage-green-test-receipt-v2.json:0
records/development/2026-08-09-deferred-items-triage-decision-v1.md:0
records/development/2026-08-15-safe-storage-formal-code-reuse-search-attestation-v1.json:0
records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md:0
records/development/2026-08-07-c4-red-verification-reuse-search-attestation-v1.json:0
records/development/2026-08-05-work-4a-v3-2-acceptance-green-test-receipt-v1.json:0
records/development/2026-08-06-work5a-contract-v2-review-run-records-v1.json:0
records/development/2026-08-13-process-inventory-safety-claim-observation-v1.json:0
records/development/2026-08-18-session-log-exit-code-vocabulary-evidence-v1.md:0
records/development/2026-08-04-layout-baseline-v2-verification-candidate-v1.md:8
records/development/2026-08-15-one-item-review-boundary5-green-evidence-v1.md:0
records/development/2026-08-07-llmgp-external-review-assets-investigation-v1.md:0
records/development/2026-08-07-work-review-protocol-high-risk-additions-decision-v1.md:3
records/development/2026-08-04-issue-resolution-pilot-issue-plan-completion-evidence-v1.md:0
records/development/2026-08-10-official-oracle-fix-test-receipt-v2.json:0
records/development/2026-08-08-work7a-four-root-separation-green-evidence-v1.md:3
records/development/2026-08-17-reviewer-launch-e2e-attempt6-evidence-v1.md:0
records/development/2026-08-09-test-fixture-dedup-receipt-v1.json:0
records/development/2026-08-03-work-1b-completed-next-candidate.md:11
records/development/2026-08-05-work-4a-v3-3-acceptance-green-test-receipt-v1.json:0
records/development/2026-08-12-project-stall-recovery-plan-v5-adoption-decision-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-issue-plan-red-evidence-v1.md:0
records/development/2026-08-17-claude-subagent-backend-contract-adoption-decision-v1.md:4
records/development/2026-08-05-task-contract-source-pin-early-pilot-v1.json:0
records/development/2026-08-13-stage3-g04-role-classification-evidence-v2.md:0
records/development/2026-08-04-layout-baseline-v3-project-first-green-test-receipt-v1.json:0
records/development/2026-08-03-work-1b-session-e2e-green-evidence-v1.md:6
records/development/2026-08-07-work5b-start-decision-v1.md:2
records/development/2026-08-15-one-item-review-task-contract-definition-challenge-v1.md:0
records/development/2026-08-18-measurement-block-integrity-guard-plan-v1.json:0
records/development/2026-08-03-work-3-deferred-scope-candidate-v1.json:0
records/development/2026-08-16-external-send-scan-refinement-adoption-decision-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-007-completion-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-002-green-test-receipt-v1.json:0
records/development/2026-08-09-test-fixture-dedup-evidence-v1.md:7
records/development/2026-08-16-vertical-b-prescan-agy-addendum-v1.md:0
records/development/2026-08-18-operational-metrics-dataset-v1.json:0
records/development/2026-08-17-rq2-apparatus-prescan-v1.md:0
records/development/2026-08-06-work6a-cl-6a-08-completion-decision-v1.md:6
records/development/2026-08-04-work-4a-v3-1-acceptance-green-evidence-v1.md:0
records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json:0
records/development/2026-08-06-improvement-candidate-lane-guidance-decision-v1.md:1
records/development/2026-08-07-intake-v4-declaration-red-map-v3.json:0
records/development/2026-08-18-measurement-block-prescan-v1.md:0
records/development/2026-08-15-one-design-acceptance-boundary1-red-evidence-v1.md:0
records/development/2026-08-14-stage4-product-code-and-task-contract-input-start-review-v1.md:2
records/development/2026-08-14-issue-resolution-v4-maturity-reassessment-correction-review-v1.md:0
records/development/2026-08-04-plan-reconciliation-stale-closure-evidence-v1.md:0
records/development/2026-08-05-record-generation-issue-plan-approval-decision-v1.md:8
records/development/2026-08-06-intake-v4-n7-n9-amendment-decision-v1.md:1
records/development/2026-08-12-stage2-minimum-trust-foundation-adoption-table-candidate-v1.md:6
records/development/2026-08-04-session-transcript-eventual-preservation-completion-test-receipt-v1.json:0
records/development/2026-08-10-trusted-core-policy-proposal-v1.md:0
records/development/2026-08-15-one-design-acceptance-implementation-start-correction-review-v1.md:0
records/development/2026-08-18-rq2-byproduct-candidates-triage-decision-v1.md:4
records/development/2026-08-05-work5a-first-real-review-run-records-v1.json:0
records/development/2026-08-18-plan-writer-evidence-commands-v1.json:0
records/development/2026-08-03-work-3-unified-requirements-promotion-green-test-receipt-v1.json:0
records/development/2026-08-08-shared-function-sweep-green-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-003-red-evidence-v1.md:0
records/development/2026-08-17-rq2-paired-trial-evidence-v1.md:0
records/development/2026-08-03-development-policy-v5-green-test-receipt-v1.json:0
records/development/2026-08-05-task-contract-source-pin-green-evidence-v1.md:0
records/development/2026-08-13-python-313-pycache-overengineering-recovery-evidence-v1.md:0
records/development/2026-08-07-work5b-ledger-item-defer-decision-v1.md:0
records/development/2026-08-05-work5a-definition-challenge-green-test-receipt-v1.json:0
records/development/2026-08-05-v4-issue-persistence-decisions-test-receipt-v1.json:0
records/development/2026-08-06-intent-damage-green-evidence-v1.md:10
records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md:0
records/development/2026-08-05-historical-todo-intake-candidates-v1.json:0
records/development/2026-08-09-work7a-root-initialization-symlink-correction-green-evidence-v1.md:3
records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json:0
records/development/2026-08-04-work-unit-commit-reminder-pilot-decision.json:0
records/development/2026-08-07-confidentiality-work-order-decision-v1.md:0
records/development/2026-08-18-operational-metrics-v2-prescan-v1.md:0
records/development/2026-08-07-work5b-red-map-checker-declaration-red-map-v1.json:0
records/development/2026-08-07-candidate-ranking-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-issue-plan-green-test-receipt-v1.json:0
records/development/2026-08-04-layout-baseline-v2-red-evidence-v1.md:4
records/development/2026-08-04-issue-resolution-pilot-plan-v3-candidate-test-receipt-v1.json:0
records/development/2026-08-15-one-design-acceptance-boundary2-green-evidence-v1.md:0
records/development/2026-08-05-todo-update-transaction-boundary-green-evidence-v1.md:0
records/development/development-policy-v1.json:0
records/development/2026-08-17-free-text-request-type-implementation-e2e-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-independent-correction-green-evidence-v1.md:0
records/development/2026-08-05-todo-test-projection-correction-first-receipt-v1.json:0
records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md:5
records/development/2026-08-18-session-log-exit-code-reuse-search-attestation-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-task-contract-v2-green-test-receipt-v1.json:0
records/development/2026-08-04-work-4a-v3-actual-observation-green-test-receipt-v1.json:0
records/development/2026-08-03-work-3-requirements-coverage-decision.json:0
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v3.json:0
records/development/2026-08-06-work6a-non-authority-completed-projection-input-v1.json:0
records/development/2026-08-11-claude-bootstrap-review-repair-correction-review-v1.md:0
records/development/2026-08-05-work5a-first-real-review-acceptance-v2-evidence.md:3
records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-evidence-v2.md:0
records/development/2026-08-18-agents-norm-transfer-decision-v1.md:0
records/development/2026-08-03-work-3-requirements-coverage-completion-evidence-v1.md:4
records/development/2026-08-04-session-transcript-eventual-preservation-implementation-checkpoint-evidence-v1.md:8
records/development/2026-08-15-session-artifact-safe-storage-independent-completion-review-v2.md:0
records/development/2026-08-04-project-manifest-v2-red-evidence-v1.md:2
records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-pause-evidence-v1.md:0
records/development/2026-08-18-cli-defaults-rollout-prescan-v1.md:0
records/development/2026-08-03-work-3-requirements-coverage-candidate-v1.json:0
records/development/2026-08-14-stage3-g06-common-guards-cleanup-independent-completion-review-v1.md:0
records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-reassessment-v1.md:0
records/development/2026-08-17-free-text-request-type-product-acceptance-decision-v1.md:7
records/development/2026-08-03-layout-baseline-v1.json:0
records/development/2026-08-15-safe-storage-capability-derived-code-reuse-search-plan-v2.json:0
records/development/2026-08-16-external-send-scan-refinement-v2-independent-review-v1.md:0
records/development/2026-08-03-work-2-completion-evidence-v1.md:11
records/development/2026-08-14-stage3-correct-behavior-witness-method-amendment-independent-completion-review-v1.md:11
records/development/2026-08-05-semantic-commit-minimal-guards-test-receipt-v1.json:0
records/development/2026-08-05-work5a-definition-challenge-green-evidence-v1.md:0
records/development/2026-08-07-reuse-search-record-helper-reuse-search-attestation-v1.json:0
records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md:0
records/development/2026-08-18-measurement-block-evidence-v1.md:4
records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-observation-v1.json:0
records/development/2026-08-05-machine-operation-routing-task-python-cache-green-evidence-v1.md:0
records/development/2026-08-18-cli-defaults-rollout-plan-v1.json:0
records/development/2026-08-08-shared-function-policy-decision-v1.md:0
records/development/2026-08-06-session-transcript-repair-and-recapture-decision-v1.json:0
records/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-scope-one-time-review-v1.md:0
records/development/2026-08-15-safe-storage-provisional-g26-reuse-search-attestation-v1.json:0
records/development/2026-08-15-safe-storage-formal-code-reuse-search-plan-v1.json:0
records/development/2026-08-13-review-target-process-connection-bootstrap-start-review-v1.md:0
records/development/2026-08-09-work7a-four-root-separation-completion-projection-input-v1.json:0
records/development/2026-08-07-verification-boundary-layer1-green-evidence-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-task-contract-definition-correction-review-v1.md:0
records/development/2026-08-17-claude-subagent-passthrough-environment-correction-decision-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-task-contract-state-gap-candidate-v1.json:0
records/development/2026-08-11-claude-bootstrap-review-repair-scope-v2.md:0
records/development/2026-08-15-one-item-review-boundary3-red-evidence-v1.md:0
records/development/2026-08-05-todo-test-projection-correction-final-receipt-v1.json:0
records/development/2026-08-08-todo-handoff-unified-verification-green-test-receipt-v1.json:0
records/development/2026-08-10-scope-prescan-rule-decision-v1.md:0
records/development/2026-08-03-work-3-added-requirements-promotion-completion-evidence-v1.md:0
records/development/2026-08-15-one-design-acceptance-boundary2-red-evidence-v1.md:0
records/development/2026-08-12-claude-bootstrap-real-run-host-safety-stop-v2.md:0
records/development/2026-08-03-session-transcript-source-formats-decision.json:0
records/development/2026-08-04-work-4a-v1-revert-map-v1.md:0
records/development/2026-08-03-work-3-unified-requirements-promotion-negative-red-evidence-v1.md:0
records/development/2026-08-17-launch-metrics-recoverability-prescan-v1.md:0
records/development/2026-08-18-measurement-block-integrity-guard-evidence-v1.md:0
records/development/2026-08-03-work-3-deferred-scope-approval-green-test-receipt-v1.json:0
records/development/2026-08-16-one-item-review-safe-projection-v2-limited-rereview-v1.md:3
records/development/2026-08-18-measurement-block-nondeterminism-investigation-v1.md:0
records/development/2026-08-15-one-item-review-task-contract-definition-correction-review-v1.md:0
records/development/2026-08-07-intake-v4-declaration-red-map-v2.json:0
records/development/2026-08-03-work-3-nfr-verification-profile-decision.json:0
records/development/2026-08-15-capability-derived-code-reuse-search-implementation-plan-v1.md:0
records/development/2026-08-12-stage2-official-test-entry-restoration-completion-review-v1.md:0
records/development/2026-08-18-plan-writer-prescan-measurements-v1.md:0
records/development/2026-08-04-development-venv-red-test-receipt-v2.json:0
records/development/2026-08-16-external-send-scan-refinement-real-doc-e2e-evidence-v1.md:0
records/development/2026-08-04-development-venv-green-test-receipt-v1.json:0
records/development/2026-08-15-session-artifact-safe-storage-independent-completion-review-v3.md:0
records/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-start-review-v1.md:0
records/development/2026-08-05-work-4a-v3-3-actual-generation-green-test-receipt-v1.json:0
records/development/2026-08-03-work-3-permanent-remediation-red-evidence-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v4-decision.json:0
records/development/2026-08-13-stage3-first-test-cleanup-lifecycle-scope-review-v1.md:0
records/development/2026-08-07-work4b-c-externalization-declaration-red-map-v1.json:0
records/development/2026-08-03-work-3-requirements-artifact-runtime-green-evidence-v1.md:7
records/development/2026-08-10-review-material-mode-decision-v1.md:0
records/development/2026-08-16-vertical-b-reviewer-launch-adapter-prescan-v1.md:0
records/development/2026-08-08-redaction-production-entry-independent-review-test-receipt-v1.json:0
records/development/2026-08-15-one-requirement-feature-source-contract-v1-independent-review-v1.md:13
records/development/2026-08-16-minimal-operation-contract-execution-green-evidence-v1.md:0
records/development/2026-08-13-python-313-development-environment-migration-bootstrap-start-review-v1.md:0
records/development/2026-08-12-stage2-official-test-entry-restoration-start-decision-v1.md:0
records/development/2026-08-14-stage3-created-artifact-lifecycle-inventory-independent-completion-review-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-005-green-test-receipt-v1.json:0
records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md:11
records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-candidate-v1.json:0
records/development/2026-08-03-work-3-source-identity-stale-evidence-v1.md:1
records/development/2026-08-15-one-item-review-independent-completion-review-v1.md:0
records/development/2026-08-07-reliable-reporting-rule-decision-v1.md:1
records/development/2026-08-07-integration-exclusion-entries-decision-v1.md:0
records/development/2026-08-18-plan-writer-evidence-v1.md:0
records/development/2026-08-05-work-4a-v3-3-acceptance-red-evidence-v1.md:0
records/development/2026-08-10-review-method-consolidation-v1.md:0
records/development/2026-08-18-reuse-search-cli-defaults-plan-v1.json:0
records/development/2026-08-04-work-4a-rebuild-design-v3-approval-decision-v1.md:0
records/development/2026-08-13-review-target-process-connection-implementation-evidence-v1.md:0
records/development/2026-08-05-issue-intake-v4-red-evidence-v1.md:0
records/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-evidence-v1.md:3
records/development/2026-08-07-universe-v2-timing-decision-v1.md:0
records/development/2026-08-14-stage3-test-authority-consistency-policy-correction-independent-completion-review-v1.md:0
records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md:0
records/development/2026-08-14-recovery-plan-v5-artifact-lifecycle-completion-condition-amendment-decision-v1.md:0
records/development/2026-08-18-plan-writer-evidence-measurements-v1.md:0
records/development/2026-08-05-triage-authority-history-and-procedure-test-receipt-v1.json:0
records/development/2026-08-13-stage2-minimum-trust-foundation-completion-decision-v1.md:0
records/development/2026-08-17-free-text-request-type-v1-self-review-v1.md:0
records/development/2026-08-05-triage-record-generation-root-issue-test-receipt-v1.json:0
records/development/2026-08-16-one-requirement-candidate-consistency-check-green-evidence-v1.md:0
records/development/2026-08-05-v4-human-triage-persistence-green-test-receipt-v1.json:0
records/development/2026-08-05-triage-planned-and-completed-work-test-receipt-v1.json:0
records/development/2026-08-06-work6a-inventory-correction-v1.md:10
records/development/2026-08-16-external-send-scan-refinement-impl-self-review-v1.md:0
records/development/2026-08-18-cli-defaults-rollout-evidence-measurements-v1.md:0
records/development/2026-08-13-stage3-first-multi-group-test-cleanup-implementation-plan-independent-review-v1.md:0
records/development/2026-08-10-review-protocol-overview-v1.md:0
records/development/2026-08-04-issue-resolution-pilot-wi-004-projection-input-v1.json:0
records/development/2026-08-18-operational-metrics-v2-evidence-v1.md:3
records/development/2026-08-15-one-design-acceptance-independent-correction-red-evidence-v1.md:0
records/development/2026-08-07-universe-v2-outcome-evidence-v1.md:0
records/development/2026-08-07-verification-boundary-layer1-declaration-red-map-v1.json:0
records/development/2026-08-04-issue-resolution-pilot-bootstrap-completion-evidence-v1.md:0
records/development/2026-08-14-stage3-known-correct-state-witness-independent-completion-review-v1.md:0
records/development/2026-08-05-work-5a-first-review-contract-red-evidence-v1.md:0
records/development/2026-08-13-test-growth-nodeid-enumeration-completion-decision-v1.md:0
records/development/2026-08-05-work5a-definition-challenge-red-evidence-v1.md:0
records/development/2026-08-15-session-artifact-safe-storage-boundary-3-tdd-evidence-v1.md:0
records/development/2026-08-13-stage2-minimum-trust-foundation-reassessment-decision-v1.md:0
records/development/2026-08-07-verification-boundary-layer2-red-evidence-v1.md:0
records/development/2026-08-10-egress-guard-fix-slice2-test-receipt-v1.json:0
records/development/2026-08-15-git-derived-code-search-source-correction-decision-v1.md:0
records/development/2026-08-13-stage3-g06-common-guards-reassessment-independent-completion-review-v1.md:0
records/development/2026-08-16-g20-openai-check-order-v1.json:0
records/development/2026-08-04-work-4a-v3-1-actual-routine-profile-evidence-v1.md:5
records/development/2026-08-05-work5a-first-real-review-acceptance-evidence-v1.md:6
records/development/2026-08-07-egress-gate-v3-judgments-decision-v1.md:0
records/development/2026-08-06-intake-v4-single-candidate-red-evidence-v1.md:11
records/development/2026-08-04-issue-resolution-pilot-task-contract-v2-red-evidence-v1.md:0

```

## 書式C行の実例（形の見本・先頭12行）

- argv：`["grep", "-rEh", "^\\|.*[0-9a-f]{64}", "records/development/", "-m", "2"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.055s
- 完全性：二重実行一致

- stdout：

```text
| module | `tools/development/operation_routing.py` | `0fb5636feac3e12c42104830cd710bdb2a6f9398b784edf211c57128e1cd9178` |
| 受入test | `tests/test_operation_routing_v2.py` | `369544e87bf673222ca6fec0306b55dc130b831094f51c93afa3e46c5fb075c5` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json` | `aace8f35b79cbe4e3113433b55e903e86e0171f04738b180e1728eb83bd93ca6` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md` | `ad7b82ae74cec8655c205191feb4bf89801353eb8c7838f239f8b1c7da4c6658` |
| `tools/reviews/one_item_review.py` | `de658b6e96b804af393d106cbc11c39d7452e9cb54c24c5157853bc5dcd9ad57` |
| `tools/reviews/one_item_review_entry.py` | `92a770583b14728b5f6606a851357efb27a19fdba11d07fecd12d941f633c390` |
| 契約012候補v2（受入対象） | `records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md` | `f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d` |
| 実装Evidence（§9-1〜7） | `records/development/2026-08-17-claude-subagent-backend-implementation-evidence-v1.md` | `979b48868bdc69751c60fec4bb3f5e9abdf910b4c7d30b941b5cd7fe0922a7de` |
| 実装module | `tools/development/structured_argv_executor.py` | `c697c9804ff5decdf21530744c97752b564bb42a895bcb2544dec2d81ea206ea` |
| 受入test | `tests/test_structured_argv_executor.py` | `9166e680d6c1b528163df23e5ecb0852c5fdf614875818737a265bc49760b9ff` |
| Intent候補 | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` |
| 統合用語集候補 | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` |
| `tools/deployment/checkout_relocation.py` | `e48d65dbb1ef39420c44e2c05fcf55da3100bba92a5b5d6d7a185340b00b434c` |
| `tests/test_work7a_checkout_relocation.py` | `db68cc42b4020ff7e5ad6ee485aa7ad401df5ccd18fd6f57dae93ef5378586e1` |
| `work4a/observations/3ecb6a8b629706c990d47a7683d5beef238057274f7105fb916b75e45e308e5f.json` | 再観測 |
| `work4a/profiles/55fdacd5aec93a857b7c4900eb895488f77b5f57419c25af5309fdafe10ad8c1.json` | Routine Profile v3 |
| 修正実装 | `55a7c38b8d60101d709f21196f06db1943325e8d149b8c68aad69055158ac5c3` |
| 回帰Test | `e9735910650b4da522664eefb4c93ca1c02a4daa41e004f6d6b18c60ee15923b` |
| 先行完了レビュー | `38460b84e469cc81950633b3026cb195d6c308e4aaa171a22d10458cd0e13281` |
| 訂正Evidence | `c2a386c87e542a7f626e77b931bb24672fd6bf392fda71e216a5c19923959c30` |
| 契約011候補v3（受入対象） | `records/task-contract/2026-08-17-request-builder-candidate-v3.md` | `146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1` |
| 実運用E2E・完了レビューEvidence（2往復・fence修正） | `records/development/2026-08-17-request-builder-e2e-evidence-v1.md` | `fac5a19072ef241a24c248a9d09cb4efd92d11ccd5e8ba62434cc37492ceba09` |
| 作業票v1 | `docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md` | `5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`、commit `120ec5e3922fa7aaa886cb3aca647e93943ef016` |
| 独立開始前レビュー | `records/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-start-review-v1.md` | `5dc23327f1072fd5438ca8ff2e2c22634f4257dd8970426471f69696be3a80ad`、commit `644391c3eeaae97f3b70593ef5827f071e664484` |
| candidate SHA-256 | `2666511bcf95a2fdc5237257b5c5e38fbc7dc1c80fd829064b02e34b759e6ab9` |
| Work 2 session raw SHA-256 | `7cc254470abd013b94df534cf4bea7b94394b4590154da746091a37171ae4277` |
| bundle SHA-256 | `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` |
| 1 | Intent候補 | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` | `provisional`、Human承認前 |
| 2 | 統合用語集候補 | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` | `provisional`、Human承認前 |
| 承認済み設計提案 | `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f` |
| Work 4設計提案 | `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` | `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054` |
| Human Decision | `records/development/2026-08-04-work-unit-commit-reminder-pilot-decision.json` | `327cdf74c4cedfa2230a906fbe4e75f24b2cff1da6a00c06a6c3ea03c1cdb64b` |
| RED Evidence | `records/development/2026-08-04-work-unit-commit-reminder-red-evidence-v1.md` | `2fabf5401ef44c1fbcf92758215855b941d8ef5de30178dea0b2763870e31f0b` |
| 契約011候補v3（採用対象） | `records/task-contract/2026-08-17-request-builder-candidate-v3.md` | `146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1` |
| 独立確認判定record（cr-011-001・verified_with_findings・blocking 0件） | `records/session-handoffs/2026-08-17-request-builder-v2-review-verdict-v1.md` | `f8a719f74f880eac80b95582073a12aff2d481b097add45c38dbaf17b996e51a` |
| 契約010候補v2（受入対象） | `records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md` | `7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a` |
| 実E2E成功Evidence（第7試行） | `records/development/2026-08-17-reviewer-launch-e2e-attempt7-success-evidence-v1.md` | `eca7ae8f534a467e4e16bf094416bc742aeebd85231558c2fca98033e6b15711` |
| source content ID | `c8880cb4dee72e73264e342b8a5b249b8e971c45ce3dcb8294aec6c06edefcf6` |
| Profile ID | `303fd52862e3667e47730351936cb4c776f6e627652a3bd6c0e41d725121f264` |
| Work 3 Completion Candidate | `records/development/2026-08-03-work-3-completion-candidate-v1.md` | `aff0f3977a50f0e4aee9a2937b16518665d0267f44094780b75eba65991d7788` |
| Human Completion Decision | `records/development/2026-08-03-work-3-completion-decision.json` | `5cf7bb52e5cff547e06581ed6c8b57e8b77eaedc352615e5a063f422467dcf45` |
| Layout v2 Approval | `records/development/2026-08-04-layout-baseline-v2-approval-decision.json` | `856345948af57bcfa373eb2766768d9c38078d7ba5fe65b0d76d68e452ceaa7e` |
| Project Manifest v2 | `.reviewcompass/project-manifest.json` | `e4e0636cf2d6382c870acd88e82b8a9febe10e14a4cc4ffc40d08af6018f9c30` |
| 公式試験入口IDの参照列挙 | 6経路、列挙SHA-256 `424136f6fea94837638175b09fe0714755aff1c9055965a76840307c51f8764d` | 0 |
| 公式結果記録SHA-256 | `b95f039aee1e60678d83644740e630250dda4ff8ecee3d6bcb988263900d73d5` | 0 |
| 契約v4 | `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1` |
| 採用judgment | `5f8c9fab3e3512376359f4b58ca528b87adcb74d0d488e1e86af1af06f2b6614` |
| `AGENTS.md`（訂正後） | `eb2e5535a0bcb03ad1ace973178b90da60eb1acd6d34c76276919b574e622ade` |
| `tests/test_agents_lane_guidance.py` | `2916ba1ae0bcfdffffefc6248c239324e11271227fa4411b7eba788b03071000` |
| 採用済み契約v3 | `records/task-contract/2026-08-15-one-item-review-material-and-result-organization-candidate-v3.md` | `a52cd717f6709c5ca01a1e339385272abfe976a0b9ce176e857b427778cf07d6` |
| 最終検証Evidence v1 | `records/development/2026-08-15-one-item-review-final-verification-evidence-v1.md` | `3c11a18d68d50b54aba7465290534690b49cabe6c6295126f6a1c29ab1dd4aaa` |
| `tools/development/policy_test_runner.py` | `d749685737f09c301cfb9f118a8fe4688ad1d864d47f7c7e1ff9ef44bd7df076` |
| `tests/test_policy_test_runner.py` | `0319df8f16ae76353e67b33013371cb28a0e1c7dd1b07882760d17bf9a17df7f` |
| Work 1B red Evidence | `records/development/2026-08-03-work-1b-red-evidence-v1.md` | `079277ae1f3f1c5277672d2ad24e4e1650983c0e0fc3eec5da4ee6f56d79604a` |
| 固定Acceptance Test | `tests/test_session_log_bootstrap.py` | `7b7f46b2c5df5de55032eb311632cafc10b885399ad00d3d8ff7f8ec714aa685` |
| candidate SHA-256 | `2666511bcf95a2fdc5237257b5c5e38fbc7dc1c80fd829064b02e34b759e6ab9` | `bfec3b29cf8ebb5ffeedc349e39b2215922ebef8e4105a258e73279a7226a252` |
| raw event stream | `71346c1f6689fc686d1e26debb6d3572d12854f1859aaa53799f74b7c7af7cae` |
| `tools/egress/approval.py` | `cb8f97e1d2b05f0ec7e9bad9e045c80b8378a03167be2d623f13853c3236b243` |
| `tools/egress/gate.py` | `ec611dfa65c0ff8f8ccf586ed491e944430cf80952a797861ea3b06a7f1de0c1` |
| 採用済み契約v2 | `9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603` |
| 採用判断 | `17b4f4f522810db3a851b1bc8dd1ab65bb90fb9ce5df2276ae60a42fcb19ec99` |
| v2提案（承認は§3のみ） | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md` | `7c812b68b4b4b0cd282af29b44ff117e78aa172b6f2b830f6d684856f9bf7a31` |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |
| `tools/design/one_design_acceptance.py` | `da340bda3b8d8b51a95afecb6ebcd273fcd52ce9e8e2a7b39cc336b0074b7ed3` |
| `tools/design/one_design_acceptance_entry.py` | `7535aa6652514c6ce4dfd31facd2640944a356ddc04802b0df8ae63a9bec9823` |
| `records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md` | `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb` |
| `records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md` | `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda` |
| `records/development/2026-08-03-work-3-requirements-coverage-candidate-v1.json` | `c529e1495a8ea5a84ac15ae651299a410f6aba627ee115b395a5940aa209cb7e`／`human_decision_candidate` |
| `records/development/2026-08-03-work-3-requirements-baseline-evidence-v1.md` | `7fdc24c8063292871761af3c888824f3e3c715689df3a3924c28c7856f9c5a20`／`verified_baseline` |
| `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md` | `c150187e7e79ddd955942bba5c4a775dbda64537f31931bd048604ab5cb082ad` | `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c` |
| `docs/development/2026-08-02-development-policy.md` | `b3c7ce815705ba11915d3d384ee5d7fa2b8175503a03c9ff2417e79c83aeb5dc` | `422d234a0503670e61936edfe98cd13451f4e7af6bfc1506a07824f2904f0fac` |
| `tools/session_logs/read_only_entry.py` | `8d03610aaa677b9e4d6d4271fbb698ddd81928db95a72b14e7eb4e3588592c8a` |
| `tests/test_session_log_read_only_entry.py` | `8152c5bb82ca235d723aac69fb519b2b6284a3f92cf6e2972328b4f479e5e053` |
| 承認済みAmendment | `docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md` | `881a9192322e1e1176d3b453dfa121b6dea1a99a6e1c438ad637fc209ed5d0da` |
| blocking候補 | `records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-improvement-candidate-v1.md` | `96ee100a0633be4525e59f27d090e6460657e26352416e88d0261172845ff18d` |
| 契約v3 | `7ad6da3c77632f3fc82bdbbabcb71d431d490bc78e12004d2331ef44cfdf0081` |
| 利用者採用判断 | `35eb9a0b34d6ecf3e7d503498ca0a0f04234fd4519c33eecee3b816cf8dd5c41` |
| `tools/development/authority_reference_checker.py` | `584c9669c5b0230f2fa460ce9d0b975d7c416371529cf6f6f2a9d2221ca8ffcf` |
| `tools/development/authority_reference_keys.json` | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| `contract_approval` | `CA-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `af4209029b2d11f53d9abf0e3ed67dd8d182c1177dfe1625507f03bcb2095b25` |
| `compile_verdict` | `CV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `ad45ebba3659d5ea34751d103bd1fde96b075162bc00a6cabc2aa5b85b8ac332` |
| snapshot_id | `5cea442a82a5662c3a8fa0db49f1c741842489f8965223b7c2ae981bc3c6d4d0` |
| profile_run_id | `b4ba016eaac8bc07326ef24e8c730d235dcf97b01ed7c4312107bc96fff1b66d`（routine 1245件、file 119） |
| 現行Plan | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |
| Work 1A Evidence | `records/development/2026-08-03-work-1a-layout-evidence-v1.md` | `5d54c7de759388ae81c1fefebcc50c817c0b38ae2bcdc65444f47aa48cc8e899` |
| `records/development/2026-08-03-work-3-requirements-artifact-layout-candidate-v1.json` | `154a4f40487bc52537e87575d063f0c3e0e72b19fa13d2cdcee0e4fc0339e6ed`／`human_decision_candidate` |
| durable green Evidence | `records/development/2026-08-03-work-1b-durable-capture-green-evidence-v1.md` | `7ab01e1a106c6d8cb2711f1b8bc4df150d34761d94c7d0f13f033332783f2f22` |
| green実装 | `tools/development/session_log_bootstrap.py` | `fd2b286e2d0d72a05eb1f4f0cc0f19650eb41a4c9d2e7921eb9b61b374066339` |
| `tools/common/digests.py` | `db6b8305…` | `fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7` |
| `tools/common/paths.py` | `daa32579…` | `039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec` |
| target SHA-256 | `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054` |
| Human implementation scope Decision | `records/development/2026-08-03-session-transcript-source-formats-decision.json` | `a8810356db36ec9483880c300e59ad7919d3716ff488723c433591a12e065bfe` |
| test-first RED Evidence | `records/development/2026-08-03-session-transcript-source-formats-red-evidence-v1.md` | `a40dc78d848e7c067652b3cc1f7b051c98ba8c88f4354bdd1e1e5eb6130b453c` |
| `tools/development/formal_code_reuse_search.py`【変更】 | `default_runtime_root()`・`latest_policy_file()`新設。`--runtime-root`／`--universe`／`--policy`任意化＋自動解決、`--captured-at`旗を削除 | `f9faab7074e0320d385937f27b52f9d387a6041e008a1723c62c0ac781af0077` |
| `tests/test_formal_code_reuse_search.py`【拡張】 | 追加4本（数値最大版選択・既定保存先・解決不能停止・旗拒否）＝計12本 | `649739902416485867c1c3e5aedf761237f2b79717f394b5f066da17cac0773d` |
| 書換え前TODO／WI-007 snapshot SHA-256 | `16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`で一致 |
| 書換え後TODO SHA-256 | `6acb26636c5b50fe4ecb527ce49cc2f78ca3b801e57b612e4fa8a1122b68978e` |
| 後続Plan提案 | `docs/design/2026-08-05-machine-operation-routing-follow-on-plan-proposal.md` | `ab6d9b3bf33a6348a5718062930a7d58aa1bf8df75c22fc415a7221ba29d024c` |
| 最小縦切りの既存設計 | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md` | `e01c3aaf8039377da2b43dab7f735d28a2f86bf10aa83f5bb22e5dd1eefa8572` |
| 実装digest | `125b4e18145b5fa2f41ecb8208a018b9bdb706dacb8278dda2d2fc23c58abbe1` | `b97bd5eec6f6ae4fedd7a719089a8af0f642ddfb59e6ee4e29f851993db02a97` |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` のSHA-256 | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20`。作成時の値と一致（未変更） |
| 承認済みTask Contract | `records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md` | `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b` |
| 定義訂正後の独立確認 | `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-correction-review-v1.md` | `8f07d74cb03e4ab6134a1774af8b775e1d01c57d836f32720ad6296dd1099e91` |
| `tools/session_logs/config.py` | `af8651cc911b7d4afac2a4b02562b60cd408a21c98967a2c700d2392b1e4dc8c` |
| `tools/session_logs/portable_config.py` | `135faff2d565f36206ce8017f46fb0d016b1c883b66444537c7eec90ee93d34b` |
| `tools/development/process_call_inventory.py` | `5b5f521bd02f81a485376ea86cbf274733b896c37d7860279fee49cdd957fc1b` | `generate_process_call_inventory`は対象試験一件だけ。`compare_process_call_inventories`はPythonからの呼出し0件 |
| `records/development/2026-08-11-claude-bootstrap-manifests/process-call-baseline-v1.json` | `96d9dddebb26355b85addbb1a8d73adfe4adc0636e1097dd44214c02663a0460` | 対象試験一件が読込み。ほかは2026-08-11の指示・計画・証跡からの参照 |
| Issue正本 | `.reviewcompass/workflow/issues-v4/issue-todo-handoff-verification-gap-001--v1.json` | `475b0ea27b331b1d44e3883a30c575d21ebd14ab14b894725e8aa9121e51bba5` |
| 発生観測 | `records/development/2026-08-07-todo-handoff-verification-gap-observation-v1.json` | `01f57093a875059d738f7045cfc9ca124dde3d838f6bed4f1a9c533382a43dcc` |
| source universe | v3、内容識別値`3a9c13c27f69e428c057b67e3db5c51dac44ee6af5cd2b4e37d90da9548fb534` |
| freshness policy | v6、内容識別値`b718f6ce9dc00ac588e3bf365a6f28b156d148978f0b6d6dd8a7725a44223134` |
| 対象契約候補 | `b42232fd0f6a559a680c5447845502a0947b0d96caaaddae208c8bf0c94a2f9b` |
| 基底契約006 v4 | `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1` |
| approved design document | `docs/design/2026-08-03-session-transcript-eventual-preservation-design.md` | `b387b9cf913b11a0d39e13cbd5aa6222527fdb4f801e478f1110683c3dd8d1fe` |
| Human design direction Decision | `records/development/2026-08-03-session-transcript-eventual-preservation-decision.json` | `620fde82dc424141f4f5a9e8ce383fd9669506149e764eceebff0ada6addfcba` |
| `tools/deployment/local_integrated_roots.py` | `31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149` |
| `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| bundle SHA-256 | `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e` |
| `records/development/2026-08-03-work-2-completion-evidence-v1.md` | `8a5f42dbde5d3b79ae2b200746e46f441cf07219a8ff5836fbf749d6563442d2`／Work 2 `verified / completed` |
| `records/requirements/stage-four-user-approval.json` | `48ea1b075caa628fcfb1f6391d3eb6e51a3584a136d8a5706ecbd8a2cc8cedfc`／既存37要件Human承認 |
| 複製元 | `records/task-contract/2026-08-17-session-log-prefix-interpretation-candidate-v2.md`（`4dd6796d179f76fa58930108146ab1a9a007838577365d8a1a118e455c34a3b1`）の §7冒頭〜§7.2直前を抜粋。観測記録側は調査結果を材料用に1表へ整理したもの |
| 複製元 | 手順書側＝commit `0d3c992`時点の`docs/development/prompts/session-log-record-run.md`（当時のfile digest `e1a25223df1b3bc58749940150b6c4a79cda20e83b04cc20f20700d723b57893`）の§2。契約側＝候補v2の§7.3〜§7.4直後まで |
| 基準 | 3.9.6 / 8.4.2 | 1,338 | `148767a3a05564c5c67c7c86b1525cfb32ed7130d1fb9162a5abe203ed479389` |
| 基準対照 | 3.13.14 / 8.4.2 | 1,338 | `148767a3a05564c5c67c7c86b1525cfb32ed7130d1fb9162a5abe203ed479389` |
| SHA-256 | `0d290876110440df6ac5f14bd2efcc3d3d8f244b66f5d19354c4e7bb98f8cb64` |
| 参考：v1（path改訂前） | `790f80c9c185805107bc56edc3adc38c64248559094310225fc41a8796095f6a` |
| `tests/test_requirements_artifact_layout.py` | `49df58714f901cf83c11594a9ac0f5f77567ac445e3977f81a1c756d9325a6a9` |
| `tests/fixtures/requirements/artifact-layout/valid-artifacts.json` | `8d063195352ac6b376b16cea32fc4bcb7584ac98a52ada83f50979dbb5b4c59c` |
| `AGENTS.md`のSHA-256（追記後） | `30704aad10b316b3a2ec2456d6878b4a8ecbfbf589bbddf9e8f0f7461b0b8741` |
| `tools/deployment/local_integrated_roots.py` | `31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149` |
| `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| NEXT規則Decision | `records/development/2026-08-03-work-1b-completed-next-decision.json` | `ba70d88a9a9a023954b9879c7658c788fd8984663e6cc5a93085051b8fdab273` |
| 改善候補Outcome接続 | `records/development/2026-08-03-work-1b-completed-next-candidate.md` | `8a36ceffdfe8da4289cc0728b7b34b5a95588140b0b2a5a0580787e83d3a71f4` |
| 結果記録SHA-256 | `358cfdff60d994073c43ce92395f021576f8f13e57cb9034a805a0e64ec38f9b` |
| 状態識別値 | `6ca1d8a4a92cbe9ef2e5b5a01c387b73cacd0ad5c8afbe07032206275106f36b` |
| Task Contract v1 | `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b` | `dbb9f2f` |
| 定義訂正後の独立確認 | `8f07d74cb03e4ab6134a1774af8b775e1d01c57d836f32720ad6296dd1099e91` | `a57bef3` |
| 安全保存Task Contract v3 | `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac` |
| 能力別検索計画v3 | `7b385de1f1ae216b711daf29499afa86bea93fdc65d2d86890bc2d172f130a9e` |
| Human scope Decision | `records/development/2026-08-10-all-reviewcompass3-codex-session-capture-decision-v1.json` | `6d1367e121959197cd71a8e33a2e9aa45a95b20b18decc20688c708ef68ecbc6` |
| Task Contract v3 | `records/task-contract/session-transcript-eventual-preservation-v3.json` | `4e9498e3514aa5efcf4a9803b2ca49ba16e774500e5be51b571c728d74bd480f` |
| `tools/development/issue_resolution_v4.py` | `770585427e6185730506ec6aa5da8004a79d77e2cee00e9b4210290d03a2bae8` |
| `tests/test_issue_resolution_v4.py` | `d1d09ab998ebed10a85a9f93613463ba756593052a214853d02b52aab749a4fb` |
| `requirement_binding` | `RB-FIRST-REVIEW-CONTRACT` | 1 | `831217a7c3850fb711427ddc2c6aaf686b9155338e34dfa406a6fbc9f7af68de` |
| `review_task_contract`（draft v2） | `TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 2 | `cfa129d3afce155a683fed7e7da07c3272fb89922264edf79c239b6d3846cfb4` |
| 立て直し計画v5 | `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c` |
| 現行開発方針 | `422d234a0503670e61936edfe98cd13451f4e7af6bfc1506a07824f2904f0fac` |
| `docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` | `8475cd94b449e0709eb97e6d487b86cceef86e0307b3bbb7e78351d8f43147a9` |
| `config/development-issue-resolution-pilot-v4.json` | `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e` |
| Candidate | `records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json` | `e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc`／approved snapshot |
| Candidate Evidence | `records/development/2026-08-03-work-3-source-identity-stale-evidence-v1.md` | `3d04943d0174c323d9b5f1feb605eb70ff3e4dc3a779e681bf179d810db16812`／verified candidate |
| `tools/development/issue_resolution_v4.py` | `c4b5c57dcfe69b8ce87c370361171f8eaba664f38186f1fd3db54d43c6405216` |
| `tests/test_issue_resolution_v4.py` | `29be67ce761ad0449f1adc2ba5d58e8a9a1d27ebaade4b2d7a7c8c8586e2e4a6` |
| 一時（commitしない） | `<scratchpad>/record-generation-todo-temporary-receipt.json` | `d175bdb2cc2d4265f3c646d6f47de5d0640c186de2cd0214ba5f2acc3eb84f91` | `passed` | passed 881／total 881 |
| 最終（commitする） | `records/development/2026-08-05-record-generation-todo-green-test-receipt-v1.json` | `70aaeab191424651956f6d896df7da7c9e682d7cf376e45de925b78fbeafaf6a` | `passed` | passed 881／total 881 |
| `TODO_NEXT_SESSION.md` | `d1c2dfca0fbf8ecf434482ad03d813a3abe4df0aa4913e5c8ff3eb10c47ca738` |
| `docs/development/2026-08-02-development-policy.md` | `b3c7ce815705ba11915d3d384ee5d7fa2b8175503a03c9ff2417e79c83aeb5dc` |
| 契約候補v2（採用対象） | `records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md` | `7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a` | `41a705b` |
| 独立確認判定record（開始可） | `records/development/2026-08-16-reviewer-launch-adapter-v2-independent-review-v1.md` | `b2c37c97ca4d6fb1989b8bd07be0cdee94c0e819f5b0fca20e1bbad7e13724e3` | `d7155a1` |
| Work 5B開始Decision | `records/development/2026-08-07-work5b-start-decision-v1.md` | `b99da9e4f3eb2913731ebf2701eb6abcf7787548feb5c152118c7aa98d916bfe` |
| Work 5B Contract | `records/development/2026-08-07-work5b-implementation-task-contract-v1.json` | `89c92ae260bfb1efd201d414e0235b66ebb270b457942c59ef5fccfc9cfa5387` |
| コード候補 | 152 | `5d116414e108851af39710abc8483c0a5c48bd7b6a9a7db8377d014dc650e3ed` | `c8c1cf64d011ce15234a584b1604953907bd87051673eb74df8475ebcda4c29e` |
| 試験関連 | 192 | `f6db6ef2955bb4dcec171580e01660681b51704af47eaa823ad5f481242a856f` | `3426dbe2529af2f2971eb1d5c7c75678da39726d7d416081aae1131837d1d821` |
| 結果記録SHA-256 | `9e9e60f880f4655d5ee83af65689d43b77dc249f0d124de39136ade07f911001` |
| 状態識別値 | `9c31872a6c511efec5daa1276be3f20ced13e21ea6eb21b95c8f3c46c5ba1c2d` |
| 更新後TODO | 2,893 bytes、64 lines、active Issue 1件、SHA-256 `388ccc4699a8aa1438a4f04b6ce88abc73ef07e5fd9664c87763056d2bd24769` |
| 公式receipt | `records/development/2026-08-04-issue-resolution-pilot-wi-004-green-test-receipt-v1.json`、SHA-256 `7cd110a4dadffaa5d7ee2c62051b409bda7bac8f8eab95767787853f10f3195e` |
| E1 | `tools/deployment/local_integrated_roots.py` | `records/development/2026-08-09-work7a-four-root-separation-independent-review-evidence-v1.md` | `5418bc5839cd01cf8f6b99088c33108fb83fb366fa7a49ff773959e556fab1ec` |
| E2 | `tools/deployment/checkout_relocation.py` | `records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v3.md`（v1・v2から継続） | `ec30754f1ff8d6e06b791b1be78c58dd558e1966b80c34716807b15c0d497a3c` |
| 直前green Evidence | `records/development/2026-08-03-work-1b-green-evidence-v1.md` | `fdaeeb439226c6e86b17b8aa33e0e11fbdc64512ccd3b2c3f9a14f0970e169b9` |
| green実装 | `tools/development/session_log_bootstrap.py` | `eeacccb8635820ef4e15a7e7dd7b47a973096727830c8637092b06198e0b9fa8` |
| `tools/development/policy_test_runner.py` | `0f7072ab8a7c4ab9093f394858c7629e2f60c1d2b774d5fd3b640622998e5b24` |
| `tools/development/pytest_summary.py` | `febbdc68d64048c2351a343f83e121b2d06823515741d33ee1216203533d22b4` |
| `records/development/2026-08-06-work5a-contract-v2-review-run-records-v1.json` | `51f93bc14e47a3fe2e78eec8daa875930153ecb9d0c1031c12af800eeb723979` |
| `records/development/2026-08-06-work5a-contract-v2-review-run-evidence-v1.md` | `49d2df92e02c21491b0bf57c6bf31bd77b3beff1c41757863dcec9fa62af735b` |
| `tools/development/authority_reference_checker.py` | `584c9669c5b0230f2fa460ce9d0b975d7c416371529cf6f6f2a9d2221ca8ffcf` |
| `tools/development/authority_reference_keys.json` | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| blocked Evidence | `records/development/2026-08-03-work-1-fixed-input-evidence.md` | `d07c5abdce7bc4b3322e7c6f973feb0e00d7218151dafe7013aff5d08148b879` | v1を上書きせず保持 |
| blocking candidate | `IC-WORK1-DOC-RECONSTRUCTABILITY-001` | `4206805e3066335c5a84a56baa839e4b074da4b5af1f8cd17b20bcbe22860404` | 修復routeを実行 |
| 7語彙の機械形 | `tools/evaluation/rq2_paired_trial.py`の`JUDGMENTS`定数（SHA-256 `890996191d60ec6ea49742345ac60599071aa88ea3cbc5070e051d2f6d4dbd25`） | `tests/test_rq2_paired_trial.py` 14件（SHA-256 `f00ef74c3014197e1affe49e69d2236f2accb7a2991b31d41664adc07da37ca2`） |
| 全44指摘への適用値 | `records/development/2026-08-17-rq2-scoring-judgments-v1.json` | SHA-256 `082af4aa9cc29e92c60d53c0ad0b5922d8a40f3bee0c0da8057887b1841b0b18` |
| `work4a/observations/7d9522de102de0a7f84ade4f1ef95487a3852f30c83f27129832a9d83dc0dbc4.json` | 再採取した観測 |
| `work4a/profiles/78f8b8733b3baf1bfe8bc46efaf77c498cf362eb1a44086d32f1f39efabef8e4.json` | Routine Profile v2 |
| 採用する契約013候補v3（cr-013-001所見反映済み） | `records/task-contract/2026-08-17-free-text-request-type-candidate-v3.md` | `73a287c137a73c617e25655c35377b88a7ffc033b89e4be68d63d3b0ce245ffc` |
| 独立確認判定record（cr-013-001・verified_with_findings・blocking 0件・機械転記） | `records/session-handoffs/2026-08-17-free-text-request-type-contract-review-verdict-v1.md` | `dcfffbec261db38ba7c58dc8b92b9c5fa3b4d708940198abedaade29ae7112a6` |
| `tools/development/issue_resolution_v4.py` | `770585427e6185730506ec6aa5da8004a79d77e2cee00e9b4210290d03a2bae8` |
| `tests/test_issue_resolution_v4.py` | `d1d09ab998ebed10a85a9f93613463ba756593052a214853d02b52aab749a4fb` |
| `tools/session_logs/read_only_entry.py` | 新しい読取り専用入口 | `b88f256cab9df9c988541408579f3930311468f3cdc292d20bdacfa97c0e5c4f` |
| `pyproject.toml` | `[project.scripts]`へ実行名一件を追加 | `ec771cd06e063d2f4b252ecfc9962d7f221effbf072169edbabfb7c8f71d3229` |
| `records/development/2026-08-05-issue-intake-v4-green-evidence-v1.md` | `28809b220e8e5b16f3f643c8994ea9bdeb73ac83d3e506daaea6baceb751e75f` |
| `records/development/2026-08-05-v4-human-triage-persistence-green-evidence-v1.md` | `41fcbbbd6acc278055dd3e43e64fcb0c603627319eae1fb13b853262bda305d7` |
| `human_decision` | `HD-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `0feea7519d0bd7c3362dc867282f0b866c26a0ec1eb0bd3f0cd7815e44371d1c` |
| `provenance_verdict` | `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `9e4a06cdaf83a1544c2308c4ebb620c4e04790a881157839b8c60e64c992df5d` |
| `records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md` | `2991aed38dd7e6f294774baa0ff98d664168bd8f2fffdc3337e7228938109af8` |
| `records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md` | `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb` |
| `tools/evaluation/operational_metrics.py`【新設】 | launch実測の分計＋承認点分布の集計装置（一行JSON・0／2・fail-closed） | `ff5b26e3ab3c6fa7ead6214d302b7cd500e7bfbd2a456c0c0bcc45897c38511c` |
| `tests/test_operational_metrics.py`【新設】 | 分計・統計値・日付分布・一行JSON・終了コード・`-m`疎通の5本 | `1efd0c8f09df8e18d77dcb69c48ce85e97324e6846c84df109334968f8e29c0e` |
| Comparison Discovery（816 group） | runtime領域 `work4a/comparison-discoveries/80668a….json` | `b7758366bffc0b16a46008cdfaadbe8625ae331bfb441647c8fbe37aad5f5855` |
| Routine Profile（1,252関数） | runtime領域 `work4a/profiles/75b9bd3f….json` | `0354635de80b45906c638bde2b79ded1c42768688090ec06f6aac8907cb6eaa5` |
| Task Contract | `records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md` | `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b` |
| 実装開始承認 | `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md` | `dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39` |
| 一時（commitしない、repository外） | `<scratchpad>/boundary-repair-temporary-receipt.json` | `aa5526282604ec39bfdf7795f645217e4b0ee58315e9bc3cc0f32cff88742e82` | `passed` |
| 最終（commitする） | `records/development/2026-08-05-record-generation-todo-boundary-repair-green-test-receipt-v1.json` | `ad0f191e0af53a21ab130d9346743d0b214ac56ad6cf958b64ae175535df98df` | `passed` |
| 対象契約候補 | `1ed92a89a96550fe1ea5df74fc40fd74102694e8bfefa07b5ec0c9d09df1bb6d` |
| 利用者の運用化目標 | `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a` |
| Storage Candidate | `records/development/2026-08-04-session-transcript-eventual-preservation-storage-candidate-v1.json` | `0c712308275cd321870fe2c203b0b53207bc817108a9fba3910da6ee730a5fdc` |
| Human storage Decision | `records/development/2026-08-04-session-transcript-eventual-preservation-storage-decision.json` | `79c9e7aa781d09cb4afe477919889e12583ae1d8e57b15317046cff5c1e74953` |
| Layout v3正本 | `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json` | `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38` |
| Layout v3承認 | `records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json` | `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275` |
| 追跡パス列挙 | `git ls-tree -r --name-only cc2f0476...` | 0 | 1,780件、SHA-256 `bb2b53ebbe2fe1f4e3663f5838e498019f6f49ba95c40a71a272594b9a10217e` |
| 対象期間の件名列挙 | `git log --reverse --format=%H%x09%s c24e3b41^..cc2f0476` | 0 | 175行、SHA-256 `aefdda6ea359ab96a0d8a620a0c4450c1d940040edef4ac6b354468b6435f617` |
| `tools/external_review/send.py` | `fcecb2e35ffca0b6341cd7e102c4e6f0dc8b7b5871c36d87b8eae0a07a8d0197` |
| `tools/external_review/send_entry.py` | `ebe8f0b4908493d464fdb8e39bfe09d59c1fa8e16b1dec643e2e79d4f7dcdd5e` |
| 生データ（31実行） | `records/development/2026-08-18-rq2-paired-trial-dataset-v1.json` | `d34ecd24a8d87c49e5b50f4ae204295841622ea12c34886e29dba5a32c85b893` |
| 採点裁定（確定） | `records/development/2026-08-18-rq2-scoring-judgments-v2.json` | `865ad0e34c3de742301443824dc41c3e8f866aab0a9c7591836a838391613e59` |
| 記録先 | `records/development/2026-08-06-checklist-authority-reference-digest-repair-evidence-v1.md`（SHA-256 `b7b280e7c61b193f6ed19f798279fc19a0942e8daa7a99ee7dcaf5549420c373`）／観測record `records/development/2026-08-06-authority-reference-digest-drift-observation-v1.json`（SHA-256 `6ccf3d15c28c56a5b74730a9ac056ef3abe13967da0427549e05308cc0ab3841`） |
| 何が起きたか | front matterのYAMLを解析して記載Digestを参照先の現行bytesと突き合わせる恒久的な検査器が、repository内に存在しない。`tools/`配下にfront matter YAML parserは無い。類似の照合は`tools/development/todo_record_generation.py`（SHA-256 `f5ae4328b211b0d140856a5e29663673f604ba69623b65c13848e432896e37ea`）にあるが、対象は`TODO_NEXT_SESSION.md`の`## 最新のauthority／Evidence`節に限られる（測定commitで参照8件・不一致0件） |
| `tools/common/roots.py`【新設】 | `repo_root()`のみの一元化module（RC2 paths.py型） | `478476817a5fcc755c7e96f33cfe2a68f093e0a4dd26ae3405cbac2ff8d33791` |
| `tools/session_logs/entry.py` | 14行の遡りを、file位置読込み（`_load_roots`）経由の`repo_root()`委譲へ置換 | `9fd812b4b3934f167b21d8f78752487fba9a086e78f0ffe07473553c1aef159f` |
| 承認Decision | `records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md` | `9ca6a0f75c00f2979437fceca225ede10d28c84f1578a1624db0f04747d7214d` |
| 承認済み設計 | `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f` |
| `tools/external_review/gemini_send.py` | `1cb2de0c155a450fb3ca827005c2ea81fcb303728a2a85fdb18a8d63353c5538` |
| `tests/test_gemini_send.py` | `bba82572456376257d1b24f4a2a4422996a250a60709d8c29d1b82fd5f991c60` |
| `tools/session_logs/config.py` | `af8651cc911b7d4afac2a4b02562b60cd408a21c98967a2c700d2392b1e4dc8c` |
| `tools/session_logs/portable_config.py` | `135faff2d565f36206ce8017f46fb0d016b1c883b66444537c7eec90ee93d34b` |
| 依存固定SHA-256 | `f8d4343c239413d073270441c6882208a60184807b75e0bbc0caa0652bb97db4`。設定値と一致 |
| 結果記録SHA-256 | `a5facbeb100d64a4f2d1a524be6c1083975038ccbb572b9f4878a8b6b51d042f` |
| module | `tools/development/operation_routing.py` | `f735299433b49b868b713dfcc4ed1973c7d4771f906242e3e3932e39bf269049` |
| 受入test | `tests/test_operation_routing_v2.py` | `6da141f20f7b8a31e270c6a2dc2195cbce20c908633d81e0e939e51b703d6fc4` |
| `records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md` | `e4f8d9f865e6b6d35e7d00a21eba54c13b1ed331fca3183827b1262d285d88eb` |
| `records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json` | `b6f55b5c7096b19106656403d9a7ad975f79debff61767827ac425be111d018a` |
| `tools/session_logs/read_only_entry.py` | `8d03610aaa677b9e4d6d4271fbb698ddd81928db95a72b14e7eb4e3588592c8a` |
| `tests/test_session_log_read_only_entry.py` | `8152c5bb82ca235d723aac69fb519b2b6284a3f92cf6e2972328b4f479e5e053` |
| `tools/session_logs/eventual_preservation.py` | `9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18` |
| `tests/test_redaction_registration_preservation_path.py` | `ae370016e70d2baba00f9c259e3c59ef4046ae4a54c6b56c23e1af21797bd53b` |
| `AGENTS.md` | `b7157936d92e7c322c32c68a6536c304ce24d0d170cf5b8a82a1c205b008a502` |
| `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |
| `docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md` | `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809` |
| `records/session-handoffs/2026-08-06-codex-to-claude-development-continuation.md` | `5d488a132777bf012bc433e7929c4db60c8a174077f543936b8d786f918f2563` |
| `docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md` | `d5164077b8a53141eb647e57f4746e3347ac4650c03a0d1d553571348fc63358` |
| `records/development/2026-08-06-intake-v4-declaration-red-map-v1.json` | `c24ebaf58eee3ce2d318084697051d41c9669e30aa756086706f9f110117ce40` |
| 成熟度精査Evidence | `8038ce27b0c3fa41e0ebdb70a860811d4bb7e1649847b16c0a88c25d5834d050` | 親フォルダ作成失敗でIssueだけが`resolved`に残る反証を記録 |
| 独立完了レビュー | `893fde2d1d05f438f47b87fe28ac5c5103081ac0eec127019a14f58c7b7aa1fd` | 別の使い捨て複製と独自の故障注入でも同じ片残りを再現 |
| コード候補 | 152 | `5d116414e108851af39710abc8483c0a5c48bd7b6a9a7db8377d014dc650e3ed` | `c8c1cf64d011ce15234a584b1604953907bd87051673eb74df8475ebcda4c29e` |
| 試験関連 | 192 | `f6db6ef2955bb4dcec171580e01660681b51704af47eaa823ad5f481242a856f` | `3426dbe2529af2f2971eb1d5c7c75678da39726d7d416081aae1131837d1d821` |
| `provenance_verdict` | `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `7975c7619dbca8c95fd249303dba47e46e0d8ec681e386866e1dddfbfa38aae0` |
| `accepted_artifact` | `AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1 | `6c4c690a39bbf0b1a845432e8dfe6c8f155598927e74e92d51a51eb28c7d9d4c` |
| `source_state_digest`独立再計算 | `2ebe29435834bd31d503189d389a0fa5fd517ed248202e0b4a4fe79c7bcb7096`で一致 | 0 |
| `README.md` | `8bdcd33d1cc4091353e2bc7edf29544d495e2c8fef5c63f004c8e886136eaf8b` | `529a344aa61bb11c8bf48f452b2af5c9b8c31b7af88843d47a9fd1f729a4fc8f` |
| `docs/README.md` | `0c115beb2822fb635195be60c3a90c2d5c4ae20dd88bc8719c31dd7a435ab28d` | `639164d691fababd6238e7e5ba5c2d9824ab76e58478167a0f4280e20e4ea8c3` |
| 作業票v1 | `554f38ca40474ce56900e102bfd7f5246150e5c393b0805b0cc89e5bcb87b9f5` |
| Issue | `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe` |
| `.reviewcompass/policies/work4a-source-universe-v1.json` | `652bf2d8bec5a09c2d765c07644b97508b3a08dc76216ad87ee20320e46c5856` |
| `.reviewcompass/policies/work4a-freshness-policy-v1.json` | `f5e2d6340c0e08a0a90a7f237bcc44fc8fd274360cafe204342f1ac32abf0c7d` |
| 対象契約候補v4 | `d7b1861ccc73cb8f1c305294bf7c7e2a5fddd6ddb3fb46eab74e3204e8a2a7a1` |
| 直前版契約v3 | `d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85` |
| 基準 | 3.9.6 / 8.4.2 | 1,338 | 0 | `aa8355e773f243ab1e94b42d4ee260a89d65907d5415f192000ff80edb98154f` |
| 基準対照 | 3.13.14 / 8.4.2 | 1,338 | 0 | `aa8355e773f243ab1e94b42d4ee260a89d65907d5415f192000ff80edb98154f` |
| 採用済み契約v3 | `records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md` | `38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac` |
| 最終技術検証Evidence v3 | `records/development/2026-08-15-session-artifact-safe-storage-final-verification-evidence-v3.md` | `fc2d86c305b4198b774b57e550205732b599c4f4c753f8db89c52b19175facbd` |
| 全試験集合 | 正規収集は終了コード0。試験識別子1,728行、重複0件、SHA-256 `5a22372d02cf4708809a029603945a5b9ff4d5c7c06aea66468da198b60b62e1`で申告と一致 |
| `tools/development/authority_reference_checker.py` | `8641ceb7fb615c217ff9d67fd15229409d6a30dd1fb3a443ce556a1425cb707f` |
| `tools/development/authority_reference_keys.json` | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| `docs/design/2026-08-06-final-challenge-intent-damage-proposal.md` | `7f8cd3bc6da61efbc1fbcef7b93007e1534e8b77d53e329fbcd8026bf143baf6` |
| `tests/test_final_challenge_intent_damage.py`（新規） | `25ce60f3d6893681776bb636baf7ff02ecb51556ed92b6159a5b2f3f75371391` |
| prior Evidence | `records/development/2026-08-03-work-1-fixed-input-evidence-v2.md` | `7997b203935a9e53c56ed2556b4598773cd9d7b13c43079fcf8524b5e06bc9be` |
| corrective snapshot | `records/development/2026-08-03-work-1-corrective-snapshot-v1.json` | `08365d976f020b428c46d1f83b14d7b0861beb335103493cf81823a144cc25c4` |
| scope | `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md` | `f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8` |
| GREEN Evidence | `records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md` | `c20a8d4056cbe55870defd61f7a3f3de61942f945a1fe9cb7bfb696d34105c10` |
| file SHA-256 | `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6` |
| content digest | `760d9ef9811e6d95c9af406a6664e0e2ef5df9c33e32aa6ebbc33721c931753f` |
| Work 1 Evidence | `records/development/2026-08-03-work-1-fixed-input-evidence-v2.md` | `7997b203935a9e53c56ed2556b4598773cd9d7b13c43079fcf8524b5e06bc9be` |
| Layout Baseline Record | `records/development/2026-08-03-layout-baseline-v1.json` | `c18ee7a14a5720e578ea24b71e0cc120524fcfc2bca9df87a81de795cfc36cc2` |
| `tools/design/bootstrap_conformance.py` | 898 | `100d46a4013c3cea3981d6a665d8cfda5f372d2a6e70ccc5fd3fde346bb58fcb` |
| `tools/design/design_contract.py` | 1,573 | `4678b9e16a5e4b02b3e065ab69c94ffacc10a975986c2d0c238039ea02ad3792` |
| 範囲提案（承認対象） | `docs/design/2026-08-07-work-4b-minimal-pilot-scope-proposal.md` | `51eec963e5b7469110658a2a0b95f9d4effbe9279f078175076fe0e1dda2169a` |
| Current Plan | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| 製品コード候補と作業契約入力の目録 | `c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a` | 製品用途の意味群を抽出する |
| 製品の目的候補 | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` | 利用者が得る価値との近さを比べる |
| Task Contract v2 | `records/task-contract/session-transcript-eventual-preservation-v2.json` | `d75049cb8f53dc0d7ae7429270c00ca539e90485133d1984edde07f61158355a` |
| Human Decision | `records/development/2026-08-06-session-transcript-repair-and-recapture-decision-v1.json` | `c6ff5904d86049f4e414e93dd3342b0ab793b1a50d0b4f664f507e2faf5c05a5` |
| durable red Evidence | `records/development/2026-08-03-work-1b-durable-capture-red-evidence-v1.md` | `a25c7cfde5817ff35375b07087e740820a7080b67bec8b6921fac167eb5e862d` |
| durable Acceptance Test | `tests/test_session_log_durable_capture.py` | `36aab68bcc65966f20ac04e8d2f1f20ec527629020b5c3fef1cd4b776359366e` |
| 対象契約候補v3 | `d97a742bd2c67946f4336a06167767c4060a38157073e13cb42e5ecbf2117f85` |
| v2限定再確認 | `1926cfa2f4ebbb45d500813348e61cebc9f25018eae22194d28afaaa5aec005d` |
| Human Decision | `records/development/2026-08-04-commit-handoff-stability-decision.json` | `3569bbdcfdc2cfa0181951aeb0699f2409aa4ed675be5f33ce8afb36dbaf8428` |
| RED Evidence | `records/development/2026-08-04-commit-handoff-stability-red-evidence-v1.md` | `b3fdf564af7cfa51321da721b6534321cf79ef1b8cec64b909ca21a3b32305ed` |
| `records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md` | `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda` |
| `records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md` | `8dcff9e7f08a2098c6be6175cd940291f8f93a99903691dd0b94542671896d20` |
| Candidate | `records/development/2026-08-03-work-3-requirements-artifact-layout-candidate-v1.json` | `154a4f40487bc52537e87575d063f0c3e0e72b19fa13d2cdcee0e4fc0339e6ed`／approved snapshot |
| Candidate Evidence | `records/development/2026-08-03-work-3-requirements-artifact-layout-evidence-v1.md` | `25c7a61e99f04b78ab2732ef70bf507ec161f859085238579f6d0fcb09285871`／verified candidate |
| 1 | `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`（規約A/B/C） | `bb24ab9d046dd103462f192236b2ea057f5a77f32cd1f4e04be49518d5160174` | 規約B・Cは`DES-EVIDENCE-EVALUATION`（限界を別フィールドで保持・未確定停止）の再発明 |
| 2 | `records/development/2026-08-10-review-method-consolidation-v1.md`（型1〜4） | `93d2dbb26d9c5742c2f7c1ae0dcec4d4448c1c4dddef41a40b5ee89960be6a15` | `DES-REVIEW-TRIAGE`・`DES-HARNESSED-EXECUTION`の役割4分割の劣化版 |
| `tools/requirements/boundary_relations.py` | 143 | `31ae6b8edfde022300a817ec3d9d553ddb3f64d71a92a3d95c35e01a8e40e869` | `validate_boundary_relations` | 渡された値の検査と内容識別値計算 |
| `tools/requirements/feature_partition.py` | 239 | `0796d436b7f6c3e075b998f1d80451ea59d3cb3cc6b77e6ef3084f9ffbecec2a` | `validate_feature_partition` | 渡された値の検査と内容識別値計算 |
| 対象契約候補v2 | `927965f9502c0762c0ba289968d37d16237ae0ef433f15c2ac53cc8dacd94090` |
| v1独立確認 | `3eb9eba738171ac0f66572de1da5454377684f5ab4d4c110e85397c86657e5ca` |
| snapshot_id | `e349bb9c4c3e5d0531a8f889135f6c0e0f8a0cc905327cdd58df0ad07f3d76fa` |
| source_content_id | `82634be2f6437338c2542554dcafd8028a3ae68da676d722d6e4fa6df7a2d6bd` |
| adopted design memo | `docs/design/2026-08-04-deployment-project-artifact-boundary-adoption-memo.md` | `a12434bb1fd927be25b060b07804877937406f93e14735f8564f19e3988752f1` |
| Human Decision | `records/development/2026-08-04-deployment-project-artifact-boundary-decision.json` | `237dd1d0d40304240f0d8376713509c34364aaa6369d3161df3d3be2cc623c1b` |
| 追記前SHA-256（commit `56dbfeb`の親時点） | `1a4f8ce267793f1d80585f6a01ea6f2fd622f7185b7d6a527da7502acf5f2d00` |
| 追記1〜3反映後SHA-256（commit `56dbfeb`） | `a55edfcdfc7fc3690e10eccf667014c3ab6ef295762186bb5c69ed55484e5ec1` |
| `tools/deployment/local_integrated_roots.py` | `326a2d7f66c6db0ec886c9c6a4596db17ced33c040304658e305454908d3d052` |
| `tests/test_work7a_local_integrated_root_separation.py` | `18c7135762d43b3748741d39ff0fdb43bc1034a1a96a7d2916e818265999ffbb` |
| 現行Plan | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |
| bootstrap実装 | `tools/development/session_log_bootstrap.py` | `5ce2f77d671d48c8627cc3072a1b2111a4fc4ef615f3454d7b353d3b9ad2ac97` |
| 契約012候補v2（採用対象） | `records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md` | `f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d` |
| 独立確認判定record（cr-012-001・verified・blocking 0） | `records/session-handoffs/2026-08-17-claude-subagent-backend-contract-review-verdict-v1.md` | `ae78da140e9b72576700437569f91aa67cdce2be237ae0a0cf48829b3d1676c3` |
| E2E red Evidence | `records/development/2026-08-03-work-1b-session-e2e-red-evidence-v1.md` | `84cf75898883b73d4db996dbcdf465ada0a6a8b2375551c866d6a22a3e3429ab` |
| E2E Acceptance Test | `tests/test_session_bootstrap_e2e.py` | `ca4486fb43b3e5f4bd32175b0e177efb1a8612c08e2b43edaa98206e453eaedb` |
| Work 4B最小試行 GREEN Evidence | `records/development/2026-08-07-work4b-reuse-search-green-evidence-v1.md` | `3284f77507a2ad09992404cae1ced846a6fe5ccdd564af8c8c0e8772e0588e0c` |
| Work 4B範囲提案 承認Decision | `records/development/2026-08-07-work-4b-minimal-pilot-scope-approval-decision-v1.md` | `4db98a488c76a7d15c1ddffca5c8f94139c29eadcc985930f30af5636b59adfc` |
| separation_manifest ＝ relocation_manifest | `c38144d35713bd7e70eba766ef3548c4c4a6f42059bbdc590ad5e77e1e7a98db` |
| separation_readme | `1750a907a3031a3ae59255e406e22e7a6b753793805289d4a1ae7d71d76f222d` |
| `records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md` | `79c5783c6f759c631aeabc41916fcc93f914984e2278ab1acb29589e1119a5ac` |
| `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md` | `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c` |
| `AGENTS.md`のSHA-256（追記後） | `330b6f9f21dfa618bbb9d06a10eb25078d69da9ba0e691dd4ad0c75c7458e933` |
| `tools/**/*.py`、指定した拡張子なしfile、`setup.py` | 152 | `5d116414e108851af39710abc8483c0a5c48bd7b6a9a7db8377d014dc650e3ed` | `c8c1cf64d011ce15234a584b1604953907bd87051673eb74df8475ebcda4c29e` |
| `tests/**/*.py`、`conftest.py` | 192 | `f6db6ef2955bb4dcec171580e01660681b51704af47eaa823ad5f481242a856f` | `3426dbe2529af2f2971eb1d5c7c75678da39726d7d416081aae1131837d1d821` |
| Plan提案（承認対象） | `docs/design/2026-08-05-record-generation-issue-plan-proposal.md` | `79ed49831ebd9b69c9713fcd71becfaa1d85f7fd97759e5fff373f99126a2a7c` |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |
| 改定後の対象test file | `11 passed`、SHA-256 `86f0b09864a0def0ed633aa444c1f5317df72d07734e6ac55289d5212bc258e2` |
| `SRC-RC2-SHARED-ROUTINE-001` | `records/sources/2026-08-02-reviewcompass2-shared-routine-ledger.md` | `043ff5c5c83db2bad2b968b32ac332e40ad64d9baeb4ad86dc273addfb904d9b` | Git object固定 |
| `SRC-RC2-ISSUE-PLAN-001` | `records/sources/2026-08-02-reviewcompass2-issue-plan-path.md` | `d28234ca17b2f2308bad9a63ed551f21caf4b3e4527416f4627bf05d1b5a84f7` | Git object固定 |
| `IC-SESSION-LOG-EXIT-CODE-DOC-DRIFT-001` | 5.1 | 手順書の記述が実装と食い違う | `3abc98d6db9764cdde8334093988d376ef95090daefd6e8713e08372266aa52d` |
| `IC-LAUNCH-METRICS-ACCEPTANCE-TITLE-001` | 5.2 | 受入条件の表題が実態と違う | `3b09a6e8a722dd3bb8eb85dab2008461ec25b6be34da4a28c85c2822c9795d73` |
| `docs/design/2026-08-06-final-challenge-intent-damage-proposal.md` | `7f8cd3bc6da61efbc1fbcef7b93007e1534e8b77d53e329fbcd8026bf143baf6` |
| `records/development/2026-08-06-intent-damage-declaration-red-map-v1.json` | `80decdaa37ac8a0f977128d7a7866c6e00c6defd58faacf32eceeeb2a90ae3d0` |
| `tools/deployment/local_integrated_roots.py` | `bc9bc19bede6e9052b4222b02131d7b2b81ebca54d8f7de7d5b10a0fe7819870` |
| `tests/test_work7a_local_integrated_root_separation.py` | `023f3dc7351a1934a74276e46aaa748677a68df66311173f03b9ae244e86e01a` |
| v2 candidate | `records/development/2026-08-04-layout-baseline-v2-candidate.json` | `4a086be730b3310cc6933826ab6dac751e36af0596c5a8b6a7e381357d956282` |
| RED／GREEN共通Test | `tests/test_layout_baseline.py` | `baf7ae308aa2aa7f887b69f60e37f367ba8ddc1597564071af10e4e14f4f3ef4` |
| `records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md` | `20a21c56710c71b413215e12752f090674e9cad8035a2eee7b380a14098c19bb` |
| `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md` | `cc52783bc898a62e96a52e6b5d3df548e5572818ea2e37d4b5b43d3e5898638c` |
| `human_decision` | `HD-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1（再利用） | `a240921a70a40837efa2d45ee83def0059c125a2a343b7eb415841ddce65d8af` |
| `provenance_verdict` | `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | **2** | `7db7e9521d19ce958ab6e88b5d493c4e28c3ca9af1a5f08db30b0e17ab76bf12` |
| Baseline Evidence | `records/development/2026-08-03-work-3-requirements-baseline-evidence-v1.md` | `7fdc24c8063292871761af3c888824f3e3c715689df3a3924c28c7856f9c5a20`／verified |
| Coverage Candidate | `records/development/2026-08-03-work-3-requirements-coverage-candidate-v1.json` | `c529e1495a8ea5a84ac15ae651299a410f6aba627ee115b395a5940aa209cb7e`／approved snapshot |
| implementation Decision | `records/development/2026-08-03-session-transcript-eventual-preservation-implementation-decision.json` | `1fe3c2a6cf8a3430ffb9a290a437dbc34777d2514beac910a26f52a419732262` |
| Task Contract | `records/task-contract/session-transcript-eventual-preservation-v1.json` | `981e7cb1e7344f576afe3dbaf9fee94462e353980e4944b7fd2bd33401e595cf` |
| current Layout approval | `records/development/2026-08-04-layout-baseline-v2-approval-decision.json` | `856345948af57bcfa373eb2766768d9c38078d7ba5fe65b0d76d68e452ceaa7e` |
| RED／GREEN共通Test | `tests/test_layout_baseline.py` | `fb122cee9186ba22883ba081e578fcc5fd617ba400ae5a908bc30808844bc077` |
| 契約013候補v3（受入対象・cr-013-001所見反映済み） | `records/task-contract/2026-08-17-free-text-request-type-candidate-v3.md` | `73a287c137a73c617e25655c35377b88a7ffc033b89e4be68d63d3b0ce245ffc` |
| 採用と実装開始のHuman判断record | `records/development/2026-08-17-free-text-request-type-contract-adoption-decision-v1.md` | `83894a4ea18fa23fa382ac0f90bc86e6d0bf01d0aedc6a99cb07becdcd237528` |
| Work 2判断候補 | `records/development/2026-08-03-work-2-intent-glossary-candidate-v1.md` | `bfec3b29cf8ebb5ffeedc349e39b2215922ebef8e4105a258e73279a7226a252` |
| Human Approval | `records/development/2026-08-03-work-2-intent-glossary-approval.json` | `068ff06132dfcd24685d4a626d9107cf65b37456eebcd567dc72b9f6b27c7b78` |
| 作業票v2 | `22220624e145877712e064911bf99ffa893b816b318d8e803842c0b822bd982a` |
| 方針修正Decision | `76aa813046a07176650e0bc5db5d5308f569a8e51011f15cd2c21341852e0d2f` |
| `tools/development/measurement_block.py`【新設】 | 宣言JSON→argv実行→機械生成markdown（new-only・fence耐性・切り詰め印・0／1／2） | `2fb69a27d4b1449cfb61c52ecffda3dde385fdf8299eac7c65396a5da45118e4` |
| `tests/test_measurement_block.py`【新設】 | 7本（生成内容・new-only・入力不備・非0はデータ・**fence偽装**・切り詰め印・spawn失敗） | `362ed3807083a0f9dcf03c5e52a43bda36b74390cebbecc37a5a6490a40120d3` |
| 対象契約候補v2 | `9a35a25fc6481a62e8978574f8f1e73dc123eda2f96e9acb213851686d10f603` |
| v1独立確認 | `b211626ba83409e9a892c202c0903e1363b535dc93b6f390627d42361ba3d33f` |
| `tests/test_requirements_artifact_layout.py` | `49df58714f901cf83c11594a9ac0f5f77567ac445e3977f81a1c756d9325a6a9` |
| `tests/fixtures/requirements/artifact-layout/valid-artifacts.json` | `8d063195352ac6b376b16cea32fc4bcb7584ac98a52ada83f50979dbb5b4c59c` |
| `tools/design/one_design_acceptance.py` | `b3af7fdf254b21e5d368f2a02cf2aba23a86233a67b4120e7c2b39a3fd4a5c14` |
| `tools/design/one_design_acceptance_entry.py` | `7535aa6652514c6ce4dfd31facd2640944a356ddc04802b0df8ae63a9bec9823` |
| `records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md` | `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda` |
| `docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md` | `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809` |
| `records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json` | `e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc`／`human_decision_candidate` |
| `AGENTS.md`のSHA-256（追記後） | `b0e4039b1f14a5eccda001b8c700324b5df57544fc3d43de77c74f6084bf3f58` |
| 直接参照・逆引き結果JSON | `aecbb09fa2f4fe51ce7fb6a2af8bb685ce4868ce4f28fefd55aa93efb1143d47` |
| 抽出script | `8fc7a4e1819c7f21dd0097b24002476d0c6105d364fcbcc4e443d5bf40036ab3` |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`（旧inventory） | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |
| `tests/test_first_review_task_contract_e2e.py` | `cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f` |
| `tools/evaluation/operational_metrics.py`【拡張】 | 集計3（H5束縛照合）＋`field_count`＋schema_version 2 | `f7d550ab269c28f1f84ef49badeea7de8457147506cb9aeff7293e069874d786` |
| `tests/test_operational_metrics.py`【拡張】 | 追加4本（束縛3分類・採点外計上・欄形式計数・schema 2）＝計9本 | `ea52bdba20d3dde2a479a4c95e1defbebbadc561c825828ad78fedcc74d6b722` |
| `work4a/observations/6e8fae1323a61690bd63a3b1cbf21fe0dce0f827fc376177eaaa738da6f9f345.json` | 再採取した観測 |
| `work4a/profiles/5d1f174fc2941a7ee57ce27663c07030e21db0db88d4429b63b7806773e47db6.json` | Routine Profile |
| 上流record bundle `records/development/2026-08-05-work5a-first-real-review-run-records-v1.json` | `658e5ba98d6023085709733f91130a8b64acd674b3c9ca497b3f23784d588447` | 一致 |
| 上流Evidence `records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md` | `cdc4c4d8ad08a6f0d8373ea56d46018e070618ba2152ade7ac4dd09d72808b50` | 一致 |
| `docs/design/2026-08-06-issue-intake-v4-single-candidate-reference-proposal.md` | `d5164077b8a53141eb647e57f4746e3347ac4650c03a0d1d553571348fc63358` |
| `records/development/2026-08-06-authority-reference-digest-check-triage-decision-v1.md` | `be9e7d3a2af88a4452a5055d39be8a6e2f77514a5529a134db2086fb49664fb9` |

```

## 現行装置と試験のdigest固定

- argv：`["shasum", "-a", "256", "tools/evaluation/operational_metrics.py", "tests/test_operational_metrics.py"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
f7d550ab269c28f1f84ef49badeea7de8457147506cb9aeff7293e069874d786  tools/evaluation/operational_metrics.py
ea52bdba20d3dde2a479a4c95e1defbebbadc561c825828ad78fedcc74d6b722  tests/test_operational_metrics.py

```
