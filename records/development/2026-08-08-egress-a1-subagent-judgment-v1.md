# A1判定record（サブエージェントによる59組の実装同一性判定）v1

- 実施：2026-08-08。指示はHuman「AをやってみてBで答え合わせ。Aはサブエージェントもありうる。外部APIも比較してみるのも一案」（2026-08-07）
- 対象：dry-run一覧（digest `baa6491f55554898…`）の曖昧59組。**送ったpayloadはdry-runで固定した実物と同一**
- 判定者：サブエージェント4体（モデルは操縦と同じclaude-fable-5、経緯を知らないまっさらな文脈で独立実行。担当15/15/15/14組）
- 経路：この開発で既に使用中のAnthropic経路のみ。**新しい外部経路は開いていない**（出口関門の対象外）
- 限界：判定者は操縦LLMと**同一モデル系列**であり、提供元の独立性は無い。系列独立の判定はA2（外部API比較。段階3・4の承認と実装が前提）で得る

## 1. 集計

| verdict | 組数 | 意味 |
| --- | --- | --- |
| same | 49 | 同じ処理。置き換え可能（名前・整形の差のみ） |
| partial | 8 | 中核は同じだが無視できない差（例外型の違い等） |
| different | 2 | 別の処理 |

確信度：high 54／medium 5。

主な系統（sameの中身）：_sha256系14組（7関数が逐語同一）、fail-closed例外__init__系21組（7クラスが逐語同一）、canonical digest系3組、_within系3組、JSON print系3組、dataclass系5組。

## 2. 判定一覧（B答え合わせ用）

Humanは各行に○（同意）／×（不同意）を付ける。payload実物は
`records/development/2026-08-07-egress-dry-run-v1/payloads/` にある。

| # | 組 | A1判定 | 確信 | 根拠 |
| --- | --- | --- | --- | --- |
| 1 | `tools/development/work4a_rebuild_v3.py:Continuity`<br>`tools/development/work4a_rebuild_v3.py:CurrentState` | different | high | source_content_idとannotationsは共通だが、Continuityはstate/permits_baseline_advance、CurrentStateはbaseline_version/pathと中核フィールドが異なる別のデータ構造である。 |
| 2 | `tools/development/work4a_rebuild_v3.py:Policy`<br>`tools/development/work4a_rebuild_v3.py:Universe` | same | medium | id(str)/version(int)/path/content_digestという構造が完全に一致し、相違はpolicy/universeという識別子の接頭辞のみである。 |
| 3 | `tools/extraction/batch_reassessment.py:BatchReassessmentResult`<br>`tools/extraction/reassessment.py:ReassessmentResult` | same | high | status/agreed/conflicts/digestの4フィールドが完全に一致し、相違はクラス名のみである。 |
| 4 | `tools/requirements/source_trace.py:ObligationSourceTrace`<br>`tools/requirements/source_trace.py:RequirementSourceTrace` | same | high | status/records/digestの3フィールドが完全に一致し、相違はクラス名のみである。 |
| 5 | `tools/session_logs/deployment_lifecycle.py:DeploymentLifecycleResult`<br>`tools/session_logs/limited_deployment.py:LimitedDeploymentResult` | same | high | action/completed_steps/data_preservedの3フィールドが完全に一致し、相違はクラス名のみである。 |
| 6 | `tools/bootstrap/review_execution.py:ReviewExecution`<br>`tools/bootstrap/review_triage.py:ReviewTriage` | different | high | 共通フィールドはcontracted_payload_digestのみで、実行状態と仕分け結果という別のデータを表す。 |
| 7 | `tools/bootstrap/stage_one_gate.py:StageOneAudit`<br>`tools/extraction/stage_two_audit.py:StageTwoAudit` | partial | medium | どちらもstatusと未解決項目を持つ監査結果コンテナだが、フィールド構成が大きく異なる。 |
| 8 | `tools/bootstrap/stage_one_gate.py:StageOneAudit`<br>`tools/session_logs/stage_gate.py:StageGateResult` | partial | medium | ゲート監査結果として対応するが、user_approvedとrequired_gate_countの有無およびgatesの型が異なる。 |
| 9 | `tools/requirements/source_trace.py:ObligationSourceRecord`<br>`tools/requirements/source_trace.py:RequirementSourceRecord` | partial | high | 4フィールドは共通だが、片方のみobligation_id・もう片方のみdispositionを持ち、requirement_idの型も異なる。 |
| 10 | `tools/session_logs/deployment_paths.py:DeploymentPaths`<br>`tools/session_logs/deployment_paths.py:_BuiltinPlatformDirs` | same | medium | 5つのPathフィールドが1対1で対応し、相違は命名規則のみである。 |
| 11 | `tools/session_logs/parse_claude.py:ToolCall`<br>`tools/session_logs/parse_claude.py:ToolResult` | partial | high | 共通イベント枠は同じだが、呼び出しと結果という別種のイベントを表す。 |
| 12 | `tools/bootstrap/raw_review_store.py:RawReviewRecord`<br>`tools/bootstrap/review_response_parser.py:ParsedReview` | partial | medium | 4フィールドは共通だが、生レコードと解析済み結果という用途が異なる。 |
| 13 | `tools/development/bootstrap_environment.py:_sha256`<br>`tools/development/issue_resolution_pilot.py:_sha256_bytes` | same | high | hashlib.sha256(引数).hexdigest()を返す同一処理で、相違は関数名と引数名のみ。 |
| 14 | `tools/development/bootstrap_environment.py:_sha256`<br>`tools/development/session_log_bootstrap.py:_sha256` | same | high | 同一処理で、相違は引数名のみ。 |
| 15 | `tools/development/bootstrap_environment.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | same | high | 同一処理で、相違は引数名とインデント幅のみ。 |
| 16 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/issue_resolution_post_write.py:_sha256` | same | high | 関数名と引数名（value/content）が異なるのみで、hashlib.sha256(...).hexdigest()を返す同一処理。 |
| 17 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/session_log_bootstrap.py:_sha256` | same | high | 関数名と引数名（value/data）が異なるのみで、SHA-256のhexdigestを返す同一処理。 |
| 18 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/todo_compaction.py:_sha256` | same | high | 関数名と引数名（value/content）が異なるのみで、SHA-256のhexdigestを返す同一処理。 |
| 19 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/development/todo_snapshot.py:_sha256` | same | high | 関数名と引数名（value/content）が異なるのみで、SHA-256のhexdigestを返す同一処理。 |
| 20 | `tools/development/issue_resolution_pilot.py:_sha256_bytes`<br>`tools/session_logs/eventual_preservation.py:_sha256` | same | high | 関数名・引数名・インデント幅（4/2スペース）の差のみで、SHA-256のhexdigestを返す同一処理。 |
| 21 | `tools/development/issue_resolution_post_write.py:_sha256`<br>`tools/development/session_log_bootstrap.py:_sha256` | same | high | 引数名（content/data）が異なるのみで、SHA-256のhexdigestを返す同一処理。 |
| 22 | `tools/development/issue_resolution_post_write.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | same | high | 引数名（content/data）とインデント幅の差のみで、SHA-256のhexdigestを返す同一処理。 |
| 23 | `tools/development/session_log_bootstrap.py:_sha256`<br>`tools/development/todo_compaction.py:_sha256` | same | high | 引数名（data/content）が異なるのみで、SHA-256のhexdigestを返す同一処理。 |
| 24 | `tools/development/session_log_bootstrap.py:_sha256`<br>`tools/development/todo_snapshot.py:_sha256` | same | high | 引数名（data/content）が異なるのみで、SHA-256のhexdigestを返す同一処理。 |
| 25 | `tools/development/todo_compaction.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | same | high | 引数名（content/data）とインデント幅の差のみで、SHA-256のhexdigestを返す同一処理。 |
| 26 | `tools/development/todo_snapshot.py:_sha256`<br>`tools/session_logs/eventual_preservation.py:_sha256` | same | high | 引数名（content/data）とインデント幅の差のみで、SHA-256のhexdigestを返す同一処理。 |
| 27 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/python_ast_boundary_check.py:PythonAstBoundaryError` | same | high | クラス名とdocstringが異なるのみで、code/detailを保持しfail-closed用例外を組み立てる__init__は完全に同一。 |
| 28 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/structured_argv_executor.py:StructuredArgvExecutorError` | same | high | クラス名とdocstringが異なるのみで、code/detailを保持する例外の__init__実装は完全に同一。 |
| 29 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/task_python_cache.py:TaskPythonCacheError` | same | high | クラス名とdocstringが異なるのみで、code/detailを保持する例外の__init__実装は完全に同一。 |
| 30 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | same | high | クラス名とdocstringが異なるのみで、code/detailを保持する例外の__init__実装は完全に同一。 |
| 31 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | same | high | __init__本体（codeとdetailの整形・属性代入）が完全一致で、差はクラス名とdocstringのみ。 |
| 32 | `tools/development/issue_intake_v4.py:IntakeError`<br>`tools/task_contract/identity.py:ContractError` | same | high | 例外の初期化ロジックが完全一致で、差はクラス名とdocstringの対象領域のみ。 |
| 33 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/structured_argv_executor.py:StructuredArgvExecutorError` | same | high | code/detailを受けて整形・保持する__init__が同一で、差はクラス名とdocstringのみ。 |
| 34 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/task_python_cache.py:TaskPythonCacheError` | same | high | 実装本体は完全一致で、クラス名とdocstringの用途説明だけが異なる。 |
| 35 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | same | high | 例外初期化の処理内容が同一で、差はクラス名とdocstringのみ。 |
| 36 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | same | high | __init__の整形式・属性代入が完全一致で、差はクラス名とdocstringのみ。 |
| 37 | `tools/development/python_ast_boundary_check.py:PythonAstBoundaryError`<br>`tools/task_contract/identity.py:ContractError` | same | high | 処理内容は同一で、クラス名とdocstringの対象領域だけが異なる。 |
| 38 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/development/task_python_cache.py:TaskPythonCacheError` | same | high | code/detailの整形と属性保持が完全一致で、差はクラス名とdocstringのみ。 |
| 39 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | same | high | 実装本体は同一で、クラス名とdocstringの用途説明だけが異なる。 |
| 40 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | same | high | 例外初期化ロジックが完全一致で、差はクラス名とdocstringのみ。 |
| 41 | `tools/development/structured_argv_executor.py:StructuredArgvExecutorError`<br>`tools/task_contract/identity.py:ContractError` | same | high | fail-closed用例外として__init__が完全一致で、差はクラス名とdocstringの対象のみ。 |
| 42 | `tools/development/task_python_cache.py:TaskPythonCacheError`<br>`tools/development/todo_record_generation.py:TodoRecordGenerationError` | same | high | 処理内容は同一で、クラス名とdocstringだけが異なる。 |
| 43 | `tools/development/task_python_cache.py:TaskPythonCacheError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | same | high | code/detailの整形・属性代入が完全一致で、差はクラス名とdocstringのみ。 |
| 44 | `tools/development/task_python_cache.py:TaskPythonCacheError`<br>`tools/task_contract/identity.py:ContractError` | same | high | 実装本体は完全一致で、クラス名とdocstringの対象領域だけが異なる。 |
| 45 | `tools/development/todo_record_generation.py:TodoRecordGenerationError`<br>`tools/development/todo_update_path.py:TodoUpdatePathError` | same | high | 例外初期化ロジックが完全一致で、差はクラス名とdocstringのみ。 |
| 46 | `tools/development/todo_record_generation.py:TodoRecordGenerationError`<br>`tools/task_contract/identity.py:ContractError` | same | high | code/detailを保持しメッセージを組み立てる例外定義が完全に同一で、クラス名とdocstringのみ異なる。 |
| 47 | `tools/development/todo_update_path.py:TodoUpdatePathError`<br>`tools/task_contract/identity.py:ContractError` | same | high | __init__の実装が字句的に同一で、差はクラス名とdocstringの文言のみ。 |
| 48 | `tools/development/candidate_ranking.py:_content_digest`<br>`tools/development/issue_intake_v4.py:_canonical_digest` | same | high | content_digestキーを除外してcanonical JSONのSHA-256を返す処理が同一で、差は関数名と改行位置のみ。 |
| 49 | `tools/development/integration_exclusions.py:content_digest`<br>`tools/development/issue_intake_v4.py:_canonical_digest` | same | high | 同じキー除外とjson.dumps引数でSHA-256を計算する処理が同一で、差は関数名・引数名・整形のみ。 |
| 50 | `tools/development/issue_intake_v4.py:_canonical_digest`<br>`tools/development/reuse_search_record.py:_content_digest` | same | high | content_digest除外後のcanonical JSONをSHA-256化する処理が同一で、差は関数名と改行位置のみ。 |
| 51 | `tools/session_logs/distribution_validation.py:_within`<br>`tools/session_logs/private_validation.py:_within` | same | high | 両パスをresolveして一致またはparents包含を返すロジックが同一で、差は変数名と括弧の整形のみ。 |
| 52 | `tools/session_logs/eventual_preservation.py:_within`<br>`tools/session_logs/private_validation.py:_within` | same | high | resolve後の同一判定とparents包含判定という同じ処理で、変数名と整形のみが異なる。 |
| 53 | `tools/session_logs/native_validation.py:_within`<br>`tools/session_logs/private_validation.py:_within` | same | high | パス包含判定のロジックが同一で、差は変数名と改行整形のみ。 |
| 54 | `tools/session_logs/scheduler.py:_absolute_path`<br>`tools/session_logs/systemd_scheduler.py:_absolute_path` | partial | high | 絶対パス検証の中核は同一だが、送出する例外がScheduleErrorとSystemdScheduleErrorで型・メッセージが異なり相互置換できない。 |
| 55 | `tools/session_logs/scheduler.py:_absolute_path`<br>`tools/session_logs/windows_scheduler.py:_absolute_path` | partial | high | 検証ロジックは同一だが、失敗時の例外型とメッセージが異なる。 |
| 56 | `tools/session_logs/systemd_scheduler.py:_absolute_path`<br>`tools/session_logs/windows_scheduler.py:_absolute_path` | partial | high | 絶対パス必須チェックは同一だが、例外型が異なり捕捉側の挙動が変わる。 |
| 57 | `tools/development/todo_update_path.py:main.<locals>._report`<br>`tools/session_logs/cli.py:_print_json` | same | high | 同一引数のjson.dumpsをprintする処理で、差は関数名・引数名・整形と局所関数か否かのみ。 |
| 58 | `tools/development/todo_update_path.py:main.<locals>._report`<br>`tools/session_logs/private_validation.py:_print_result` | same | high | json.dumps(ensure_ascii=False, sort_keys=True)の結果をprintする同一処理で、差は名前と整形のみ。 |
| 59 | `tools/session_logs/cli.py:_print_json`<br>`tools/session_logs/private_validation.py:_print_result` | same | high | 関数名以外は字句的に完全一致する同一処理。 |

## 3. B（答え合わせ）の効率的な進め方

sameの49組は6系統に束なるため、系統ごとに代表1組を精査し残りを流し見すれば足りる。
個別に精査する価値があるのは partial 8組と different 2組、および medium確信の5組。

## 4. 境界

- 本recordは判定の固定であり、統合可否（評価②：文脈依存）を決めない
- Human答え合わせ（B）の結果は別途記録する
