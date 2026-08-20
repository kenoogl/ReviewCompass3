# 測定ブロック：codex-cli第3 backend事前走査の実測（所在・import元・digest・主題語・試験規模）

- captured_at：2026-08-20T17:38:51+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-20-codex-cli-backend-prescan-commands-v1.json`（SHA-256 `7145c5952f45eebf697778c74cb71149ae944572bc367692afdd40f9a0518372`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## codex CLIの所在

- argv：`["which", "codex"]`
- 実行体：/usr/bin/which
- exit：0・elapsed：0.003s
- 完全性：二重実行一致

- stdout：

```text
/Users/keno/.local/bin/codex

```

## codex CLIの版

- argv：`["codex", "--version"]`
- 実行体：/Users/keno/.local/bin/codex
- exit：0・elapsed：0.009s
- 完全性：二重実行一致

- stdout：

```text
codex-cli 0.147.0

```

## 契約候補が参照するfileのdigest固定

- argv：`["shasum", "-a", "256", "tools/reviewer_launch/core.py", "tools/reviewer_launch/entry.py", "tools/reviewer_launch/record.py", "tools/request_builder/core.py", "tools/session_logs/parse_codex.py", "docs/development/prompts/reviewer-launch-run.md", "docs/development/pilot-driven-record-handoff.md", "records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md", "records/development/2026-08-17-claude-subagent-backend-product-acceptance-decision-v1.md", "records/development/2026-08-17-review-tooling-module-pause-decision-v1.md", "records/development/2026-08-17-improvement-candidates-triage-decision-v1.md", "records/development/2026-08-17-backend-registry-shallow-generalization-observation-v1.json", "records/development/2026-08-17-request-builder-union-model-check-observation-v1.json", "records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md", "records/development/2026-08-20-codex-cli-backend-reuse-search-plan-v1.json", "records/development/2026-08-20-codex-cli-backend-reuse-search-attestation-v1.json"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.027s
- 完全性：二重実行一致

- stdout：

```text
814f890360312e70904fbb6b4654ed930cffa8a1db18351bf42dc54fe30318b7  tools/reviewer_launch/core.py
b8b33d9229b1f48258ab7c26475e5593093eb78799bc261db3f28aa316ec6fe1  tools/reviewer_launch/entry.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
e61215eddc0e7f50468c87a9b17c2cba6825fd2470a80d0bac3eca72c0e3907d  tools/request_builder/core.py
e6f1aca565f09dcc18754e01d4a68f72e5f9cc94223a8b53a4300036a8e6d1a3  tools/session_logs/parse_codex.py
59d71bcfa7a3502f44475f6b52a996aed6b5ae5ba045a19e9dc33a3abde3bcc5  docs/development/prompts/reviewer-launch-run.md
eb999d29947f973edbf0700c5cff97ec3bb4a46cbc66119f63a0c9a9b1ea275f  docs/development/pilot-driven-record-handoff.md
f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d  records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md
dad40e6c88a5c46dd4008806ab0e94c797d4c5f55aefd4f0d3d08891d343afb8  records/development/2026-08-17-claude-subagent-backend-product-acceptance-decision-v1.md
9b4d184f378d5dc8dad203caba5daf6b6e58b2471dd387187d5c5ede971cfd6c  records/development/2026-08-17-review-tooling-module-pause-decision-v1.md
34f7ca163645fe50770734f92b48ad41b6415983ab1eda61c57efc104be8a162  records/development/2026-08-17-improvement-candidates-triage-decision-v1.md
b09c397744e81db5936cef14f29aa9e15ceb41e0bbcfb60c815a57873639893a  records/development/2026-08-17-backend-registry-shallow-generalization-observation-v1.json
ea3cdc0d048d9604272c7c918287856e8ec3a6013856b5cde66410b262432517  records/development/2026-08-17-request-builder-union-model-check-observation-v1.json
ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
005c86b3c095041ea0ca42690c617e709394023951adb4e54d4ef5aa43efcd2b  records/development/2026-08-20-codex-cli-backend-reuse-search-plan-v1.json
dc0eaa5a963a586e8d381d6f16dbf7546ab27d7ad24038e8aa5f3bcae8c99bb0  records/development/2026-08-20-codex-cli-backend-reuse-search-attestation-v1.json

```

## reviewer_launchのimport元（全一致行）

- argv：`["grep", "-rn", "--include=*.py", "tools.reviewer_launch", "tools", "tests"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.038s
- 完全性：二重実行一致

- stdout：

```text
tools/operations/operation_contract_run.py:15:from tools.reviewer_launch.entry import g30_main as reviewer_launch_prepare_main
tools/evaluation/rq2_paired_trial.py:176:    from tools.reviewer_launch import entry as reviewer_entry
tools/request_builder/core.py:14:from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
tools/request_builder/core.py:15:from tools.reviewer_launch.record import verdict_record_relative_path
tools/reviewer_launch/core.py:32:from tools.reviewer_launch.record import VerdictInvalid, validate_verdict
tools/reviewer_launch/entry.py:12:from tools.reviewer_launch import core
tools/reviewer_launch/entry.py:13:from tools.reviewer_launch import record as record_module
tools/reviewer_launch/record.py:190:    from tools.reviewer_launch.core import BACKENDS
tests/test_reviewer_launch.py:27:    return importlib.import_module("tools.reviewer_launch.core")
tests/test_reviewer_launch.py:31:    return importlib.import_module("tools.reviewer_launch.record")
tests/test_reviewer_launch.py:35:    return importlib.import_module("tools.reviewer_launch.entry")
tests/test_request_builder.py:150:    from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
tests/test_request_builder.py:151:    from tools.reviewer_launch.record import verdict_record_relative_path
tests/test_request_builder.py:379:    from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS

```

## 起動核のname分岐とbackend別定数の所在

- argv：`["grep", "-nE", "backend_name ==|^BACKENDS|_AGY_ALLOWED|^SUBAGENT_ALLOWED|^CLAUDE_FORBIDDEN|^CLAUDE_PASSTHROUGH|^CLAUDE_CHILD_ENVIRONMENT|^ALLOWED_RESPONSE_MODELS|^FORBIDDEN_AUTH_ENVIRONMENT|^PASSTHROUGH_ENVIRONMENT", "tools/reviewer_launch/core.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.003s
- 完全性：二重実行一致

- stdout：

```text
39:FORBIDDEN_AUTH_ENVIRONMENT = (
48:_AGY_ALLOWED_RESPONSE_MODELS = ("gemini-3.1-pro-high",)
52:SUBAGENT_ALLOWED_RESPONSE_MODELS = ("claude-opus-5",)
55:ALLOWED_RESPONSE_MODELS = (
56:    _AGY_ALLOWED_RESPONSE_MODELS + SUBAGENT_ALLOWED_RESPONSE_MODELS
61:CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT = (
73:PASSTHROUGH_ENVIRONMENT = (
87:CLAUDE_PASSTHROUGH_ENVIRONMENT = (
104:CLAUDE_CHILD_ENVIRONMENT_INJECTIONS = {
116:BACKENDS = {
612:    if backend_name == "claude-subagent":
621:        allowed_models = _AGY_ALLOWED_RESPONSE_MODELS
643:    if backend_name == "antigravity-cli":
669:    if backend_name == "claude-subagent":
697:    if backend_name == "claude-subagent":
762:    if backend_name == "claude-subagent":

```

## 組み立て器のmodel照合箇所

- argv：`["grep", "-n", "ALLOWED_RESPONSE_MODELS", "tools/request_builder/core.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.002s
- 完全性：二重実行一致

- stdout：

```text
14:from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
257:    if not ALLOWED_RESPONSE_MODELS:
268:        model=ALLOWED_RESPONSE_MODELS[0],
442:    if model_match.group(1) not in ALLOWED_RESPONSE_MODELS:

```

## 主題語の一致file数（tracked全体）

- argv：`["sh", "-c", "for t in codex codex-cli openai gpt- BACKENDS; do c=$(git grep -il -- \"$t\" | wc -l | tr -d ' '); echo \"$t $c\"; done"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.401s
- 完全性：二重実行一致

- stdout：

```text
codex 607
codex-cli 29
openai 20
gpt- 159
BACKENDS 21

```

## code層のcodex一致file一覧

- argv：`["git", "grep", "-il", "codex", "--", "tools", "tests"]`
- 実行体：/usr/bin/git
- exit：0・elapsed：0.02s
- 完全性：二重実行一致

- stdout：

```text
tests/fixtures/claude_bootstrap/contract-v1.json
tests/fixtures/claude_bootstrap/helpers.py
tests/fixtures/claude_bootstrap/success-result-v1.json
tests/fixtures/development/session-log-bootstrap/capture-profile.json
tests/fixtures/development/session-log-bootstrap/expected/summary.json
tests/fixtures/development/session-log-durable-capture/expected-session-evidence.json
tests/fixtures/session_logs/codex-exec-public-shape.jsonl
tests/fixtures/session_logs/metadata.json
tests/test_claude_bootstrap_entrypoints.py
tests/test_extraction_empirical_revalidation.py
tests/test_issue_intake_v4.py
tests/test_issue_resolution_pilot_implementation_task_contract_v2.py
tests/test_operation_routing_v2.py
tests/test_operational_metrics.py
tests/test_pilot_collaboration.py
tests/test_policy_test_runner_summary.py
tests/test_python_ast_boundary_check.py
tests/test_redaction_registration_preservation_path.py
tests/test_session_log_bootstrap.py
tests/test_session_log_e2e_fixtures.py
tests/test_session_log_eventual_preservation.py
tests/test_session_log_mutation_assurance.py
tests/test_session_log_parse_codex.py
tests/test_session_log_parse_codex_rollout.py
tests/test_session_log_pipeline.py
tests/test_session_log_prefix_interpretation.py
tests/test_session_log_private_validation.py
tests/test_session_log_read_only_entry.py
tests/test_session_log_record_run.py
tests/test_session_log_regeneration.py
tests/test_session_log_source_adapter.py
tests/test_session_log_source_kind.py
tests/test_structured_argv_executor.py
tests/test_task_contract_source_pin.py
tests/test_task_contract_source_resolution.py
tests/test_task_python_cache.py
tests/test_todo_handoff_projection.py
tests/test_todo_handoff_prompt_entrypoints.py
tests/test_todo_record_generation.py
tests/test_todo_update_path.py
tests/test_trusted_claude_transport.py
tests/test_work5a_definition_challenge.py
tests/test_work7a_checkout_relocation.py
tests/test_work7a_local_integrated_root_separation.py
tests/test_work_unit_transition.py
tools/deployment/installed/trusted_review_send_dispatch.py
tools/development/claude_bootstrap.py
tools/development/pilot_collaboration.py
tools/development/python_ast_boundary_check.py
tools/development/todo_update_path.py
tools/evaluation/operational_metrics.py
tools/session_logs/parse_codex.py
tools/session_logs/parse_codex_rollout.py
tools/session_logs/private_validation.py
tools/session_logs/record_run.py
tools/session_logs/source_adapter.py
tools/session_logs/source_kind.py

```

## reviewer_launch試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_reviewer_launch.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.185s
- 完全性：二重実行一致

- stdout：

```text
70

```

## request_builder試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_request_builder.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.098s
- 完全性：二重実行一致

- stdout：

```text
42

```
