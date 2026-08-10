# 守り役code後追いレビュー対象一覧（deferred #6・第1単位）

- 作成日：2026-08-10
- 作成者：Claude（Pilot。mode `role_neutral_pilot_review`、Reviewer=codex、Closer=codex、risk `low`）
- 範囲固定：`records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-inventory-scope-v1.md`
  （SHA-256 `b81ecaacfbe866719e25cb35764cd4754092d72ad55af63c83b7c429b6567204`、SCOPE commit `b1f96dc`）
- Human承認（2026-08-10）：「#6 risk lowを確定、着手を承認する」
- 位置づけ：調査記録。優先度は**Pilot提案**であり、確定はHuman裁定による。

## 1. 列挙の根拠（網羅性）

- command：`find tools -name "*.py" -not -name "__init__.py" | sort`
- 件数：**133 module**（別に`__init__.py`が3件あり、中身を持たないpackage初期化fileとして
  一覧対象外。`find tools -name "__init__.py" | wc -l` → `3`）
- Reviewerは同commandを再実行し、§4の全表の行数合計と一致することを照合できる。

## 2. 判定基準とレビュー区分

**守り役判定**は`docs/development/work-review-protocol.md` §3の定義
「validator・Digest照合・承認関門・改竄拒否など、**他の成果物の合否を決めるcode**
（誤りが誤った合格として現れるもの）」に照らす。生成・変換・解析・調査が主で、
その出力の合否を別の守り役が判定するmoduleは非該当とする。

**レビュー区分**（守り役該当moduleのみ）：

| 区分 | 意味 |
| --- | --- |
| ①現基準済 | 現行体制（Pilot fixtureに無い反証の機械実行を含む独立レビュー）のresult recordが存在する |
| ②反証歴あり | 旧体制でCodexの反証により欠陥が検出・修復されたEvidenceは存在するが、現基準の体系的独立レビューrecordは無い |
| ③無し | 反証つき独立レビューのEvidenceを特定できず＝**後追い対象** |

区分①②のEvidence参照（path＋SHA-256）は§3に置く。全moduleはTDD（RED→GREEN）と
公式全Test通過のEvidenceを持つが、それは自己検証であり本区分では「レビュー有」と
数えない。

## 3. レビューEvidence参照（区分①②の根拠）

| # | 対象module | Evidence record | SHA-256 |
| --- | --- | --- | --- |
| E1 | `tools/deployment/local_integrated_roots.py` | `records/development/2026-08-09-work7a-four-root-separation-independent-review-evidence-v1.md` | `5418bc5839cd01cf8f6b99088c33108fb83fb366fa7a49ff773959e556fab1ec` |
| E2 | `tools/deployment/checkout_relocation.py` | `records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v3.md`（v1・v2から継続） | `ec30754f1ff8d6e06b791b1be78c58dd558e1966b80c34716807b15c0d497a3c` |
| E3 | `tools/development/authority_reference_checker.py` | `records/session-handoffs/2026-08-10-codex-review-result-authority-reference-checker-v2.md`（v1から継続） | `e24d70af0ad74be5c869358f10c5a14f05ea9a0d8e1407627740245dd0f535c5` |
| E4 | `tools/development/issue_resolution_v4.py` | `records/session-handoffs/2026-08-10-codex-review-result-issue-resolution-v4-v2.md`（v1から継続） | `0f53e5527772f8d74fec7c71a420c07c2e2155951be070423ff87ac70e157bd5` |
| E5 | `tools/session_logs/eventual_preservation.py`・`config.py`（連鎖修復） | `records/development/2026-08-08-redaction-production-entry-correction-green-evidence-v1.md` | `d9ec9d812c3cd8a3eb2efdc293eb934fe02dafe157aae9c3b24c996f2cb08f21` |
| E6 | `tools/session_logs/redaction.py`（E9反証の修復） | `records/development/2026-08-07-redaction-environment-rules-green-evidence-v1.md` | `9dae5c2df9d39be08a63e22f47936fb27336d42c9032d8b5442bca8d7df68f85` |

## 4. 全module一覧（directory別）

列の意味：判定＝守り役該当／非該当、区分＝§2のレビュー区分（該当のみ）、
優先度＝後追い対象（区分③）へのPilot提案（高・中・低。§5に理由）。

### 4.1 tools/bootstrap（17）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `bundle_verification.py` | 該当 | 材料束の整合・原文一致・stale検査＝束の合否判定 | ③ | 中 |
| `closed_payload.py` | 該当 | 承認済み束からの閉鎖payload封緘。封緘の破れは改竄見逃し | ③ | 中 |
| `evidence_closure.py` | 該当 | 証拠閉包・材料被覆の機械判定 | ③ | 中 |
| `material_bundle.py` | 非該当 | 材料束の生成。合否判定は`bundle_verification`側 | — | — |
| `migration_candidates.py` | 非該当 | 既知移植候補の発見（調査） | — | — |
| `raw_review_store.py` | 該当 | raw応答の不変保存＝改竄拒否境界 | ③ | 中 |
| `review_assurance.py` | 該当 | 変異・障害注入でレビュー実効性を検査する監査器 | ③ | 中 |
| `review_cli.py` | 非該当（要Human判定） | CLI入口・引数固定。実判定は下層だが「配置境界」を含む | — | — |
| `review_contract.py` | 該当 | 固定プロンプト・出力schemaのレビュー契約検証 | ③ | 中 |
| `review_execution.py` | 該当 | 複数担当レビューの実行境界（隔離・注入先） | ③ | 中 |
| `review_materials.py` | 非該当 | レビュー材料の区分・選定（生成） | — | — |
| `review_pipeline.py` | 該当（要Human判定） | pipeline統括が関門の呼出し順を固定。統括誤り＝関門skip | ③ | 中 |
| `review_response_parser.py` | 該当 | 応答解析の誤読が誤合格に直結する厳格parser | ③ | 中 |
| `review_resume.py` | 非該当 | 中断再開と成功成果の温存（運搬） | — | — |
| `review_triage.py` | 非該当 | 所見の統合・triage（集約） | — | — |
| `source_universe.py` | 非該当 | source universeの機械列挙（生成） | — | — |
| `stage_one_gate.py` | 該当 | 第1段完了関門の機械監査 | ③ | 中 |

### 4.2 tools/common（4）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `digests.py` | 該当 | digest計算の正本。全validatorのDigest照合が依存 | ③ | 高 |
| `errors.py` | 非該当 | fail-closed例外の基底（合否判定なし） | — | — |
| `output.py` | 非該当 | 機械可読出力の整形正本 | — | — |
| `paths.py` | 該当 | path境界判定の正本。root脱出拒否の共通実装 | ③ | 高 |

### 4.3 tools/deployment（2）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `checkout_relocation.py` | 該当 | checkout移動の捕捉・照合（read-only Git境界） | ①（E2） | — |
| `local_integrated_roots.py` | 該当 | 4種root分離の検証（symlink・例外連鎖の境界含む） | ①（E1） | — |

### 4.4 tools/design（2）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `bootstrap_conformance.py` | 該当 | bootstrap実装の適合性監査契約 | ③ | 中 |
| `design_contract.py` | 該当 | designと受け入れ試験の契約検証 | ③ | 中 |

### 4.5 tools/development（28）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `authority_reference_checker.py` | 該当 | front matter authority参照のDigest検査器 | ①（E3） | — |
| `bootstrap_environment.py` | 該当 | venvの機械構築と**検証**。環境検証の誤りは公式Testの前提を崩す | ③ | 中 |
| `candidate_ranking.py` | 非該当 | 候補groupの機械的順位付け（調査） | — | — |
| `declaration_red_map_check.py` | 該当 | 宣言→RED対応表の検査器。TDD詐称の検出器 | ③ | 高 |
| `integration_exclusions.py` | 該当 | 統合禁止対象の機械可読宣言の照合 | ③ | 中 |
| `issue_intake_v4.py` | 該当 | V4 Issue台帳validatorの正本（digest・裁定連鎖・repository検査） | ③ | 高 |
| `issue_resolution_pilot.py` | 該当 | 旧Pilotのverdict連鎖validator（現用度低） | ③ | 中 |
| `issue_resolution_post_write.py` | 該当 | post-write検証・restore rehearsal・Verdict候補検証 | ③ | 中 |
| `issue_resolution_state.py` | 該当 | 固定record列からのactive state導出。誤導出＝誤運用 | ③ | 中 |
| `issue_resolution_v4.py` | 該当 | V4 Issue state遷移の正規永続化（fail-closed） | ①（E4） | — |
| `operation_routing.py` | 該当 | 機械操作routingとreceipt整合の検査 | ③ | 中 |
| `policy.py` | 該当（要Human判定） | リスクベース開発方針の決定的評価。誤評価はrisk区分の誤りに直結 | ③ | 中 |
| `policy_test_runner.py` | 該当 | 公式Test実行のoracleとreceipt生成。誤集計＝全体の誤合格 | ③ | 高 |
| `pytest_summary.py` | 該当 | 公式Test件数の構造化集計（runnerのreceipt数値の正本） | ③ | 高 |
| `python_ast_boundary_check.py` | 該当 | Python source操作のAST境界検査 | ③ | 中 |
| `reuse_search_record.py` | 該当 | `validate_reuse_search_record`・`gate_check`がDigest・鮮度を検査し着手可否`start_allowed`を決める | ③ | 中 |
| `session_log_bootstrap.py` | 該当 | 固定入力の欠落・競合・staleを検査し`authority_status`の有効・無効を判定する | ③ | 中 |
| `structured_argv_executor.py` | 該当 | 読み取り専用の構造化argv executor＝許可command制限の実行境界 | ③ | 高 |
| `task_python_cache.py` | 該当 | task専用bytecode cacheの隔離境界（明示初期化のみ） | ③ | 中 |
| `todo_compaction.py` | 該当 | compaction結果の検証とbyte-exact復元照合 | ③ | 中 |
| `todo_handoff.py` | 該当 | TODO Git欄の決定的検査＝現在地oracleの単一入口 | ③ | 高 |
| `todo_handoff_projection.py` | 非該当 | 構造化projectionからのhandoff生成。検査は`todo_handoff`側 | — | — |
| `todo_record_generation.py` | 該当 | receipt・参照fileからのTODO機械部分の決定的生成（数値転記誤り防止） | ③ | 中 |
| `todo_snapshot.py` | 該当 | TODOのbyte-exact snapshot・manifestの作成と検証 | ③ | 中 |
| `todo_update_path.py` | 該当 | root TODO更新経路の二段確認（数値と実状態の乖離防止） | ③ | 高 |
| `verification_boundary.py` | 該当 | 機械が保証しない箇所の宣言検査（層3） | ③ | 中 |
| `work4a_rebuild_v3.py` | 該当 | Reusable Routine Ledgerのidentity chain検証を含む | ③ | 中 |
| `work_unit_transition.py` | 該当 | 完了作業単位から次作業へ進む前のcommit関門 | ③ | 高 |

### 4.6 tools/egress（6）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `approval.py` | 該当 | Human承認recordの7項目機械照合（外部送信の承認関門） | ③ | 高 |
| `dry_run.py` | 非該当 | 送信機能を持たない演習経路 | — | — |
| `gate.py` | 該当 | 出口関門。送信前検査の単一実装（fail-closed） | ③ | 高 |
| `payload.py` | 該当 | 送信可能な3種への構成制限＝機微流出防止の型 | ③ | 高 |
| `prefilter.py` | 該当 | ローカル事前分類＝外部へ出す候補の絞り込み境界 | ③ | 高 |
| `sender.py` | 該当 | 送信係の境界（段階1は型として送信不可能） | ③ | 高 |

### 4.7 tools/extraction（23）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `batch_reassessment.py` | 非該当 | 構造化batch判断の独立再判定（調査材料） | — | — |
| `candidate_integration.py` | 非該当 | 独立抽出候補の決定的統合（変換） | — | — |
| `decision_review_material.py` | 非該当 | 再確認材料の生成 | — | — |
| `dependencies.py` | 非該当 | 依存展開（調査） | — | — |
| `dependency_materials.py` | 非該当 | 内部依存閉包の材料生成 | — | — |
| `design_decision_material.py` | 非該当 | 判断材料の生成 | — | — |
| `destination_classification.py` | 非該当 | 抽出項目の受け先分類 | — | — |
| `empirical_revalidation.py` | 非該当 | follow_upの再検証材料 | — | — |
| `essence_ledger.py` | 非該当 | エッセンス台帳schema（データ定義） | — | — |
| `file_edges.py` | 非該当 | 実在依存辺の抽出（解析） | — | — |
| `followup_resolution.py` | 該当 | 参照と再集計を検証し`resolved`／`follow_up`の別を決める | ③ | 低 |
| `group_coverage.py` | 該当 | 既知正例群の抽出被覆判定（抽出漏れの検出器） | ③ | 低 |
| `known_positives.py` | 非該当（要Human判定） | 既知正例の再発見（材料）。ただし証拠欠落時はfail-closedで失敗する | — | — |
| `population.py` | 非該当 | 抽出母集団の分類 | — | — |
| `priority_batches.py` | 非該当 | 優先度付きbatchの生成 | — | — |
| `reassessment.py` | 非該当 | 生材料の独立再判定（調査） | — | — |
| `rule_recount_correction.py` | 非該当 | 再集計の重複訂正（変換） | — | — |
| `seven_axes.py` | 非該当 | 7軸の初回抽出（生成） | — | — |
| `stage_two_audit.py` | 該当 | 第2段の被覆・未解決の関門監査 | ③ | 低 |
| `stage_two_completion.py` | 該当 | 残存母集団を閉じる完了関門 | ③ | 低 |
| `stage_two_reaudit.py` | 該当 | 増分被覆を合成する再監査 | ③ | 低 |
| `structured_batch.py` | 非該当 | 構造化材料batchの解決（変換） | — | — |
| `structured_materials.py` | 非該当 | 固定構造化材料の意味分類 | — | — |

### 4.8 tools/layout（1）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `baseline.py` | 該当 | Layout Baselineの読込と配置境界検証の正本 | ③ | 高 |

### 4.9 tools/requirements（7）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `artifact_layout.py` | 該当 | Requirements schema・identity・authority結線のvalidator | ③ | 低 |
| `boundary_relations.py` | 該当 | requirement機能境界relation契約の検証 | ③ | 低 |
| `feature_partition.py` | 該当 | 機能分割とエッセンス被覆契約の検証 | ③ | 低 |
| `fixed_inputs.py` | 該当 | 第4段の固定入力照合 | ③ | 低 |
| `requirement_batch.py` | 該当 | requirements batch契約の検証 | ③ | 低 |
| `source_trace.py` | 該当 | requirement由来記録契約の検証 | ③ | 低 |
| `unified_migration.py` | 該当 | `validate_evidence_record`・`check_migration_plan`がEvidenceと移行結果を検証する | ③ | 低 |

### 4.10 tools/session_logs（39）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `cli.py` | 該当 | `--verify`経路が保存成果物を再生成照合し、一致・不一致を終了コードで決める | ③ | 中 |
| `config.py` | 該当 | 設定境界（伏字規則の登録・機微path設定を含む） | ②（E5） | 低 |
| `deployment_lifecycle.py` | 該当 | ポータブル設定の安全な移行・解除（破壊防止境界） | ③ | 中 |
| `deployment_paths.py` | 非該当 | OS標準配置先の解決 | — | — |
| `deployment_preflight.py` | 該当 | 配置先へ書き込む前の非破壊検証 | ③ | 中 |
| `discovery.py` | 非該当 | 生ログの発見（列挙） | — | — |
| `distribution_validation.py` | 該当 | パッケージ導入・OS別dry-runの隔離検証 | ③ | 低 |
| `entry.py` | 非該当 | cwd非依存の固定実行入口（委譲） | — | — |
| `eventual_preservation.py` | 該当 | 終了hook非依存の継続回収と再照合 | ②（E5） | 低 |
| `hook_installation.py` | 該当 | Claude Code設定へのhook導入・解除（利用者環境変更の境界） | ③ | 中 |
| `hooks.py` | 非該当 | セッション開始・終了の安全な入口（委譲） | — | — |
| `limited_approval.py` | 該当 | 限定配置の未承認候補生成（承認境界の一部） | ③ | 中 |
| `limited_deployment.py` | 該当 | 明示承認対象だけを扱う限定配置境界 | ③ | 中 |
| `locking.py` | 該当 | 所有権付き排他制御（並行破壊の防止） | ③ | 中 |
| `native_evidence.py` | 該当 | 6組のCI artifactを完全一致検査し`passed`／`failed`を決める | ③ | 低 |
| `native_validation.py` | 該当 | ネイティブ環境での配布境界の値なし検証 | ③ | 低 |
| `parse_claude.py` | 非該当 | Claude生ログの解析 | — | — |
| `parse_codex.py` | 非該当 | Codex exec JSONLの解析 | — | — |
| `parse_codex_rollout.py` | 非該当 | Codex rollout JSONLの解析 | — | — |
| `pipeline.py` | 該当（要Human判定） | 統括pipelineが保全・伏字化の適用順を固定。順序誤り＝機微流出経路 | ③ | 中 |
| `portable_config.py` | 該当 | OS標準配置からのポータブル設定生成（機微pathの扱いを含む） | ③ | 中 |
| `preservation.py` | 該当 | 生ログの追記専用保全と復元（raw正本の改竄・喪失拒否） | ③ | 高 |
| `preservation_migration.py` | 該当 | 書庫のLayout v3移行（plan・execute・verify） | ③ | 中 |
| `private_validation.py` | 該当 | repository外の明示ログを値なしで検証する機微境界 | ③ | 高 |
| `provenance.py` | 該当 | 転写の来歴記録と照合 | ③ | 中 |
| `redaction.py` | 該当 | 機微情報の伏字化そのもの | ②（E6） | 低 |
| `regeneration.py` | 該当 | 記録済み範囲からの転写再生成の照合 | ③ | 中 |
| `repository_context.py` | 該当 | 明示Git範囲からの**安全な**要約材料収集（機微除外の境界） | ③ | 中 |
| `schedule_backends.py` | 非該当 | OS別定期実行の共通接続（設定） | — | — |
| `scheduler.py` | 該当 | launchd設定の所有物照合を行い、非所有物の有効化・解除を拒否する | ③ | 中 |
| `source_adapter.py` | 非該当 | 2形式を1入口で解析するadapter | — | — |
| `source_kind.py` | 非該当（要Human判定） | 生ログ種別の識別。誤識別は解析誤りに波及するが合否判定ではない | — | — |
| `stage_gate.py` | 該当 | 第0段セッションログ完了関門の機械監査 | ③ | 中 |
| `storage.py` | 該当 | 成果物の配置と追記専用保存（上書き拒否） | ③ | 中 |
| `summary.py` | 非該当 | 人が読む要約の生成 | — | — |
| `systemd_scheduler.py` | 該当 | systemd unitの所有物照合を行い、非所有物の操作を拒否する | ③ | 中 |
| `transcript.py` | 非該当 | 生ログの最小転写（生成） | — | — |
| `updates.py` | 該当 | 追記専用更新と変更検知 | ③ | 中 |
| `windows_scheduler.py` | 該当 | Windows task定義の所有物照合を行い、非所有物の操作を拒否する | ③ | 中 |

### 4.11 tools/task_contract（4）

| module | 判定 | 理由 | 区分 | 優先度 |
| --- | --- | --- | --- | --- |
| `contract.py` | 該当 | Requirement binding・Contract compileの検証 | ③ | 中 |
| `definition_challenge.py` | 該当 | compile前challengeとHuman承認recordの検証 | ③ | 中 |
| `execution.py` | 該当 | Source Snapshot→accepted artifactの実行経路関門群 | ③ | 中 |
| `identity.py` | 該当 | record identityとDigestの共通規則 | ③ | 高 |

## 5. 優先度提案の理由（Pilot提案。確定はHuman）

- **高**（19件）：誤った合格・境界破れの影響が全体へ波及するもの。
  (a) 全validatorの共通正本：`common/digests.py`・`common/paths.py`・
  `task_contract/identity.py`、
  (b) 公式検証のoracle：`policy_test_runner.py`・`pytest_summary.py`・
  `declaration_red_map_check.py`・`work_unit_transition.py`、
  (c) 現在地の正本：`todo_handoff.py`・`todo_update_path.py`、
  (d) 実行・台帳の境界：`structured_argv_executor.py`・`issue_intake_v4.py`・
  `layout/baseline.py`、
  (e) 外部送信・機微境界：`egress/`の5件（`approval`・`gate`・`payload`・
  `prefilter`・`sender`）・`session_logs/preservation.py`・
  `session_logs/private_validation.py`。
- **中**：単一領域の関門・改竄拒否で、現在も使用中のもの（bootstrapレビュー
  基盤・issue resolution系・TODO周辺・session_logs配置境界・task_contract等）。
- **低**：(a) 完了済み段の契約validator（extraction監査系・requirements系）で
  再実行頻度が低いもの、(b) 区分②（反証歴あり）の3件——旧体制でも反証による
  実欠陥検出・修復を経ているため、後追いの緊急度は低いとみる（現基準の体系的
  レビューrecordが無い事実は残るため、対象から外すか否かはHuman裁定）。

## 6. 要Human判定（境界事例。停止せず判定保留として可視化）

| module | 論点 |
| --- | --- |
| `bootstrap/review_cli.py` | 入口の引数固定・配置境界を「守り役」と数えるか（実判定は下層） |
| `bootstrap/review_pipeline.py` | 統括（関門の呼出し順の固定）を守り役本体と同格に扱うか |
| `development/policy.py` | 方針の決定的評価は「他成果物の合否」でなく「進め方」を決める。§3定義に含めるか |
| `session_logs/pipeline.py` | 統括の順序固定（保全→伏字化）を守り役と数えるか |
| `session_logs/source_kind.py` | 種別誤識別は解析誤りへ波及するが、合否判定ではない。非該当でよいか |
| `extraction/known_positives.py` | 材料生成だが証拠欠落時はfail-closedで失敗する。それ自体を守り役と数えるか（完了レビューv1のF2提案） |

## 7. 集計

- 全133 module中、守り役**該当 91**・非該当 42（要Human判定6件は上表の暫定判定で計上）。
- 区分①（現基準済）4件、区分②（反証歴あり）3件、区分③（後追い対象）**84件**。
- 区分③の内訳：高19・中50・低15。
- 本節の数値は表からの機械集計（行数133＝§1の列挙件数と一致）で照合済み。
- ※F1修正（§9）反映後の値。修正前は該当82・非該当51・③75（高19・中44・低12）だった。

## 8. 本recordが行わないこと

個別moduleの後追いレビュー実施、code・test・既存recordの変更、優先度の確定、
レビュー日程の計画（いずれもscope §6のとおり範囲外。優先度と要Human判定の
確定は次のHuman裁定へ渡す）。

## 9. F1修正（完了レビューv1反映）

完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-guard-backfill-inventory-v1.md`、
commit `66ee561`、判定`report_execution_mismatch`・blocking 1件）のF1を、
Human承認（2026-08-10「F1の修正を承認する」）に基づき本recordへ反映した。

- 原因：初版の判定はmodule冒頭の説明文のみを根拠とし、公開関数の実装
  （合否・可否を決める検証関数）まで確認していなかった。Reviewerは該当する
  負例test 14件の機械実行（`14 passed`）で守り役実装を実証した。
- 再分類（非該当→該当③）9件：`development/reuse_search_record.py`（中）・
  `development/session_log_bootstrap.py`（中）・`extraction/followup_resolution.py`（低）・
  `requirements/unified_migration.py`（低）・`session_logs/cli.py`（中）・
  `session_logs/native_evidence.py`（低）・`session_logs/scheduler.py`（中）・
  `session_logs/systemd_scheduler.py`（中）・`session_logs/windows_scheduler.py`（中）。
  優先度の考え方：着手関門・照合入口・利用者環境の所有物境界は「中」、
  完了済み段の検証や外部CI向け値なし検査は「低」。
- F2（non-blocking）反映：`extraction/known_positives.py`を§6の要Human判定へ追加
  （表上の暫定判定は非該当のまま）。
- §7集計を修正後の値へ更新し、修正前の値を併記した。
