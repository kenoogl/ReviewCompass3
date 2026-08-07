# dry-run報告（送信は行っていない）

- 一覧digest：`baa6491f55554898430c88ab48f85bc12c241164e7da8bc2e6550ed5288f1241`
- 分類：明らかに同じ 187／明らかに別 1169／曖昧（payload化） 59

| # | 組 | 合成類似度 | payload digest |
| --- | --- | --- | --- |
| 1 | `tools/development/work4a_rebuild_v3.py:Continuity`<br>`tools/development/work4a_rebuild_v3.py:CurrentState` | 0.5 | `1ba3403c67ae174e…` |
| 2 | `tools/development/work4a_rebuild_v3.py:Policy`<br>`tools/development/work4a_rebuild_v3.py:Universe` | 0.629 | `a76ea62afbbd28e7…` |
| 3 | `tools/extraction/batch_reassessment.py:BatchReassessmentResult`<br>`tools/extraction/reassessment.py:ReassessmentResult` | 0.848 | `8f0870ef50181943…` |
| 4 | `tools/requirements/source_trace.py:ObligationSourceTrace`<br>`tools/requirements/source_trace.py:RequirementSourceTrace` | 0.729 | `eb8fbe58713e8be0…` |
| 5 | `tools/session_logs/deployment_lifecycle.py:DeploymentLifecycleResult`<br>`tools/session_logs/limited_deployment.py:LimitedDeploymentResult` | 0.767 | `f902a31d157e990c…` |
| 6 | `tools/bootstrap/review_execution.py:ReviewExecution`<br>`tools/bootstrap/review_triage.py:ReviewTriage` | 0.481 | `a04b5394806a4504…` |
| 7 | `tools/bootstrap/stage_one_gate.py:StageOneAudit`<br>`tools/extraction/stage_two_audit.py:StageTwoAudit` | 0.487 | `1dbcf6796fbbe0da…` |
| 8 | `tools/bootstrap/stage_one_gate.py:StageOneAudit`<br>`tools/session_logs/stage_gate.py:StageGateResult` | 0.563 | `6d5cd98eada86f9e…` |
| 9 | `tools/requirements/source_trace.py:ObligationSourceRecord`<br>`tools/requirements/source_trace.py:RequirementSourceRecord` | 0.791 | `9fff8caf5e8cc5e6…` |
| 10 | `tools/session_logs/deployment_paths.py:DeploymentPaths`<br>`tools/session_logs/deployment_paths.py:_BuiltinPlatformDirs` | 0.457 | `65119c189785fb2a…` |
| 11 | `tools/session_logs/parse_claude.py:ToolCall`<br>`tools/session_logs/parse_claude.py:ToolResult` | 0.636 | `982111e80d5d8544…` |
| 12 | `tools/bootstrap/raw_review_store.py:RawReviewRecord`<br>`tools/bootstrap/review_response_parser.py:ParsedReview` | 0.532 | `495c8b94fb831891…` |
| 13 | `tools/development/bootstrap_environment.py:_sha256`<br>`tools/development/issue_resolution_pilot.py:_sha256_bytes` | 0.6 | `cfe3538ce3b845c2…` |
| 14 | `tools/development/bootstrap_environment.py:_sha256`<br>`tools/development/session_log_bootstrap.py:_sha256` | 0.76 | `46aae22ff9b858dd…` |
| 15 | `tools/development/bootstrap_environment.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | 0.76 | `6378f50d2d511d46…` |
| 16 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/issue_resolution_post_write.py:_sha256` | 0.6 | `51b1d057d1b733a3…` |
| 17 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/session_log_bootstrap.py:_sha256` | 0.6 | `9944fde085831f52…` |
| 18 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/todo_compaction.py:_sha256` | 0.6 | `fa1d9c3210db3cd0…` |
| 19 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/todo_snapshot.py:_sha256` | 0.6 | `07b6f5562a91955f…` |
| 20 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/session_logs/eventual_preservation.py:_sha256` | 0.6 | `35269b32ced8f180…` |
| 21 | `tools/development/issue_resolution_post_write.py:_sha256`<br>`tools/development/session_log_bootstrap.py:_sha256` | 0.76 | `8b55ec30b5a8548d…` |
| 22 | `tools/development/issue_resolution_post_write.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | 0.76 | `7e9b28c42d34b787…` |
| 23 | `tools/development/session_log_bootstrap.py:_sha256`<br>`tools/development/todo_compaction.py:_sha256` | 0.76 | `7b9419a10b50996b…` |
| 24 | `tools/development/session_log_bootstrap.py:_sha256`<br>`tools/development/todo_snapshot.py:_sha256` | 0.76 | `771a40d8f831d856…` |
| 25 | `tools/development/todo_compaction.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | 0.76 | `611bfa62b31cd8db…` |
| 26 | `tools/development/todo_snapshot.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | 0.76 | `df890b82794ba54f…` |
| 27 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/python_ast_boundary_check.py:PythonAstBoundaryError` | 0.48 | `f8ade1b5d2cdb5f8…` |
| 28 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/structured_argv_executor.py:StructuredArgvExecutorError` | 0.583 | `922150c02b6a16fe…` |
| 29 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/task_python_cache.py:TaskPythonCacheError` | 0.497 | `51d30a22f683c112…` |
| 30 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | 0.497 | `2bbf36d87072ecd4…` |
| 31 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | 0.48 | `fd4f6ce2560ec66b…` |
| 32 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/task_contract/identity.py:ContractError` | 0.61 | `88ad670484f20f91…` |
| 33 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/structured_argv_executor.py:StructuredArgvExecutorError` | 0.469 | `64d176292d6ff5e4…` |
| 34 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/task_python_cache.py:TaskPythonCacheError` | 0.617 | `162ebd725f70fc01…` |
| 35 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | 0.505 | `4a3dffc10cbcd123…` |
| 36 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | 0.486 | `31e1b6beb2b8524a…` |
| 37 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/task_contract/identity.py:ContractError` | 0.48 | `9db55236c00b110d…` |
| 38 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/development/task_python_cache.py:TaskPythonCacheError` | 0.486 | `bf8fa84b4700e598…` |
| 39 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | 0.486 | `a24736556becd6d3…` |
| 40 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | 0.469 | `64c2d08192e20ab1…` |
| 41 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/task_contract/identity.py:ContractError` | 0.583 | `0e0421e57524dd52…` |
| 42 | `tools/development/task_python_cache.py:TaskPythonCacheError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | 0.529 | `1a9a6d1f57989754…` |
| 43 | `tools/development/task_python_cache.py:TaskPythonCacheError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | 0.505 | `0b67bf7d7664a3a4…` |
| 44 | `tools/development/task_python_cache.py:TaskPythonCacheError`<br>`tools/task_contract/identity.py:ContractError` | 0.563 | `1b35f685d6b3a9ab…` |
| 45 | `tools/development/todo_record_generation.py:TodoRecordGenerationError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | 0.617 | `75a047d39853cc82…` |
| 46 | `tools/development/todo_record_generation.py:TodoRecordGenerationError`<br>`tools/task_contract/identity.py:ContractError` | 0.497 | `41067e0be1aaf7a6…` |
| 47 | `tools/development/todo_update_path.py:TodoUpdatePathError`<br>`tools/task_contract/identity.py:ContractError` | 0.48 | `c05877206098c4dc…` |
| 48 | `tools/development/candidate_ranking.py:_content_digest`<br>`tools/development/issue_intake_v4.py:_canonical_digest` | 0.837 | `aadd85e461f33be1…` |
| 49 | `tools/development/integration_exclusions.py:content_digest`<br>`tools/development/issue_intake_v4.py:_canonical_digest` | 0.781 | `f2531b890552700a…` |
| 50 | `tools/development/issue_intake_v4.py:_canonical_digest`<br>`tools/development/reuse_search_record.py:_content_digest` | 0.837 | `e409774d3698880c…` |
| 51 | `tools/session_logs/distribution_validation.py:_within`<br>`tools/session_logs/private_validation.py:_within` | 0.742 | `252fa2e80a10c199…` |
| 52 | `tools/session_logs/eventual_preservation.py:_within`<br>`tools/session_logs/private_validation.py:_within` | 0.742 | `c383869aa6b37fce…` |
| 53 | `tools/session_logs/native_validation.py:_within`<br>`tools/session_logs/private_validation.py:_within` | 0.742 | `352a4a8729f1da14…` |
| 54 | `tools/session_logs/scheduler.py:_absolute_path`<br>`tools/session_logs/systemd_scheduler.py:_absolute_path` | 0.833 | `11f8ae2eb9be2538…` |
| 55 | `tools/session_logs/scheduler.py:_absolute_path`<br>`tools/session_logs/windows_scheduler.py:_absolute_path` | 0.833 | `c1f980897eef129e…` |
| 56 | `tools/session_logs/systemd_scheduler.py:_absolute_path`<br>`tools/session_logs/windows_scheduler.py:_absolute_path` | 0.833 | `a21df923cfd753b2…` |
| 57 | `tools/development/todo_update_path.py:main.<locals>._report`<br>`tools/session_logs/cli.py:_print_json` | 0.587 | `33074bae8791c364…` |
| 58 | `tools/development/todo_update_path.py:main.<locals>._report`<br>`tools/session_logs/private_validation.py:_print_result` | 0.548 | `9021b95b6cd711b8…` |
| 59 | `tools/session_logs/cli.py:_print_json`<br>`tools/session_logs/private_validation.py:_print_result` | 0.8 | `ec5273614ac4c36a…` |
