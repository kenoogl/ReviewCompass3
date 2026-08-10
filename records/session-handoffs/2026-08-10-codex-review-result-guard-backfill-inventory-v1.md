# 守り役後追いレビュー対象一覧 完了レビュー結果 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（完了レビュー）
- risk：`low`（Human確定済み）
- 判定：`report_execution_mismatch`（要修正）
- Finding：blocking 1件、non-blocking 1件、defer 1件

## 1. 固定対象と開始状態

- レビュー依頼：
  `records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-inventory-review-request-v1.md`
  （commit `95502b51f50f8e02a52ffc8b4e71ee65c0c09b91`、SHA-256
  `ad47c34f9197b0b2c06a8bdbadec7f580d3129d5f5418682c3850b8593b322d9`）
- 範囲固定：
  `records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-inventory-scope-v1.md`
  （commit `b1f96dc772094983ed5e350ad433ce389434c102`、SHA-256
  `b81ecaacfbe866719e25cb35764cd4754092d72ad55af63c83b7c429b6567204`）
- 一覧成果物：
  `records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md`
  （commit `4bed486607ea488ee43493218bd699dc3165b5b5`、SHA-256
  `1af9d804bfab59aaa90250b2c67df270e108bba7fe31832b584950a2221d91fa`）
- 判定基準：`docs/development/work-review-protocol.md`（SHA-256
  `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`）
- review開始時HEAD：`95502b51f50f8e02a52ffc8b4e71ee65c0c09b91`
- 許可範囲：本判定recordの新規作成と単独commit
- 禁止範囲：依頼書、範囲固定、一覧record、code、test、その他既存fileの変更

【実測】開始時のworktreeとindexはcleanだった。`4bed486^`は`b1f96dc`であり、
`git log --reverse b1f96dc^..4bed486`は指定された2 commitだけを指定順で返した。
各commitの変更は、`b1f96dc`が範囲固定1件、`4bed486`が一覧record 1件だった。
`4bed486..95502b5`で`tools/`と`tests/`に差分はなかった。

## 2. low規定の再実行照合

### 2.1 列挙と網羅性

【実測】次を再実行し、終了コード0だった。

```text
find tools -name "*.py" -not -name "__init__.py" | sort
```

結果は133件だった。別に`find tools -name "__init__.py"`を実行し、対象外3件を確認した。
一覧record §4をdirectory見出しと表行から機械抽出して照合した結果は次のとおりだった。

- 表行133、固有path 133
- 重複0、実fileからの欠落0、余分なpath 0
- directory別件数：17、4、2、2、28、6、23、1、7、39、4

### 2.2 成果物とEvidenceのSHA-256

【実測】`shasum -a 256`で成果物を再計算し、依頼書の
`1af9d804bfab59aaa90250b2c67df270e108bba7fe31832b584950a2221d91fa`
と一致した。範囲固定の再計算値も申告値と一致した。

【実測】区分①②のEvidence 6件はすべて実在し、一覧record記載のSHA-256と一致した。

| Evidence | 対象 | SHA-256照合 |
| --- | --- | --- |
| E1 | `tools/deployment/local_integrated_roots.py` | 一致 |
| E2 | `tools/deployment/checkout_relocation.py` | 一致 |
| E3 | `tools/development/authority_reference_checker.py` | 一致 |
| E4 | `tools/development/issue_resolution_v4.py` | 一致 |
| E5 | `tools/session_logs/eventual_preservation.py`・`config.py` | 一致 |
| E6 | `tools/session_logs/redaction.py` | 一致 |

【実測】各Evidence本文にも対象moduleまたは記載された連鎖の参照が存在した。

### 2.3 §7集計

【実測】表からの機械再集計は次のとおりで、一覧record §7の記載値と一致した。

- 暫定表上の該当82、非該当51
- 区分①4、区分②3、区分③75
- 区分③の優先度：高19、中44、低12
- 要Human判定5

この一致は表内部の算術一致であり、次節の意味分類の正しさまでは示さない。

### 2.4 非該当51件の過小分類検査

【実測】非該当51件を一覧表から機械抽出し、各moduleの説明、公開関数、判定語、
既存の負例testを照合した。疑義のある同類型を一括確認するため、次の単独commandを実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_work4b_reuse_search_record.py::test_r7_gate_fails_closed_on_missing_record_and_stale_identity tests/test_extraction_followup_resolution.py tests/test_requirements_unified_evidence.py::test_rejects_failed_or_fallback_test_receipt tests/test_requirements_unified_migration.py::test_rejects_nonpassing_or_candidate_mismatched_promotion_evidence tests/test_session_log_cli.py::test_cli_verifies_saved_transcript_and_reports_condition_change tests/test_session_log_native_evidence.py::test_rejects_artifact_with_unexpected_value_field tests/test_session_log_scheduler.py::test_scheduler_preserves_unowned_target_and_rejects_unsafe_inputs tests/test_session_log_systemd_scheduler.py::test_systemd_backend_preserves_unowned_unit tests/test_session_log_windows_scheduler.py::test_windows_backend_preserves_unowned_definition tests/test_work6a_current_work_projection_negative.py::test_stale_freshness_is_not_displayed_as_complete tests/test_extraction_known_positives.py::test_fails_closed_with_group_and_responsibility_when_evidence_is_missing
```

【実測】結果は`14 passed`、終了コード0だった。次の9 moduleは一覧で非該当だが、
他成果物の合否、開始可否、所有物照合、またはauthority有効性を実際に判定している。

| module | 一覧の理由と競合する実装上の判定 |
| --- | --- |
| `tools/development/reuse_search_record.py` | `validate_reuse_search_record`と`gate_check`がDigest・鮮度を検査し、`start_allowed`を決める |
| `tools/development/session_log_bootstrap.py` | 固定入力の欠落・競合・staleを検査し、`authority_status`を`valid`／`incomplete`／`inconsistent`へ分ける |
| `tools/extraction/followup_resolution.py` | 参照と再集計を検証し、`resolved`／`follow_up`を決める |
| `tools/requirements/unified_migration.py` | `validate_evidence_record`と`check_migration_plan`がEvidenceと移行結果を検証する |
| `tools/session_logs/cli.py` | `--verify`経路が保存成果物を再生成照合し、一致／不一致を終了コードで決める |
| `tools/session_logs/native_evidence.py` | 6組のCI artifactを完全一致検査し、`passed`／`failed`を決める |
| `tools/session_logs/scheduler.py` | launchd設定の所有物照合を行い、非所有物の有効化・解除を拒否する |
| `tools/session_logs/systemd_scheduler.py` | systemd unitの所有物照合を行い、非所有物の操作を拒否する |
| `tools/session_logs/windows_scheduler.py` | Windows task定義の所有物照合を行い、非所有物の操作を拒否する |

## 3. Finding

### F1 blocking／completion／§11.1類型3

【実測】上記9 moduleは、§3の「他の成果物の合否を決めるcode」に該当する実装と
負例testを持つにもかかわらず、一覧では非該当として後追い対象から外れている。
したがって、一覧が受入条件を満たすというClaimとrepositoryの実状態が競合する。
競合Evidenceは§2.4の実装箇所と14件の機械実行結果である。

【判断】これは、守り役を非該当として合格させる偽陰性であり、
work-review-protocol §11.1のblocking類型3
「誤った合格を実証できる受入条件・検証の欠陥」に該当する。
表の意味集計は少なくとも該当91・非該当42へ変わり、追加9件には区分と、
区分③なら優先度提案が必要になる。Pilotによる再分類と再集計が必要である。

### F2 non-blocking／completion／要Human判定への追加提案

【実測】`tools/extraction/known_positives.py`は既知正例の必要証拠が欠けると
`MissingKnownPositiveError`でfail-closed（欠落時に安全側へ失敗）する。一方、別moduleの
`group_coverage.py`が被覆関門として既に該当扱いである。

【判断】前者を材料生成とみるか、それ自体も守り役とみるかは境界事例である。
§11比例原則に従いblockingへ拡張せず、「要Human判定」への追加候補とする。

### D1 defer／scope外

【記録】個別moduleの後追いレビュー実施、優先度のHuman確定、レビュー順と日程はscope §6で
本単位の対象外である。本レビューでは採否を判断せず、後続単位へdeferする。

## 4. 判定と次

判定：`report_execution_mismatch`（要修正）。

【判断】path網羅、SHA-256、Evidence実在、表の算術集計は一致したが、必須の過小分類検査で
F1が成立したため`verified`にはできない。停止系判定の根拠は、一覧の非該当Claimと
§2.4の実装・負例testの競合である。Human境界、禁止path、外部操作の違反は確認していない。

未実施：一覧record・code・test・既存recordの修正、優先度裁定、個別後追いレビュー、
TODO・checklist反映、外部操作。

次：PilotがF1の9 moduleを再分類し、区分・優先度・§7集計を更新した新しいreview requestを
固定してから、同じlow規定で再レビューする。
