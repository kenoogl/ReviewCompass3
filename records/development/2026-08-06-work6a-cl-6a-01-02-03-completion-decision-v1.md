# Work 6A `CL-6A-01`・`02`・`03` 項目完了 承認Decision v1

- Decision ID：`DEC-WORK6A-CL-6A-01-02-03-COMPLETION-001`
- decision maker：Human
- decided at：`2026-08-06T17:47:49+09:00`
- decision：`approved`（Human文言「Q1 OK,　Q2　ア」）
- decision class：`item_completion_decision`
- 関連Decision：`DEC-WORK6A-CL-6A-08-COMPLETION-001`、`DEC-WORK6A-CL-6A-09-COMPLETION-001`、
  `DEC-WORK6A-CL-6A-10-COMPLETION-001`

## 1. 承認対象

初期開発チェックリスト9節の次の3項目にHumanが完了を承認した。

- `CL-6A-01`：Contract／Requirement／Plan／Context／Provenance欠落を検出する（Q1）。
- `CL-6A-03`：validatorの既知違反見逃しと正常例誤停止を検出する（Q1）。
- `CL-6A-02`：permission過剰、stale、crash、optional観測欠測を区別する（Q2で選択肢アを採用）。

## 2. 完了根拠

いずれも、被覆主張を疑う側からの独立検証（2026-08-06）→残余の閉鎖→Human裁定、の順を経た。
残余の処置の正本は`records/development/2026-08-06-work6a-inventory-correction-v1.md`
（SHA-256 `41b6e8436f437da1eccf911f2e34cff211d5959110ed91e18ce9ea4887bfcdc0`）。

- **CL-6A-01**：唯一の未被覆だった「Plan欠落」を境界例
  `tests/test_work6a_coverage_boundaries.py::test_missing_compile_verdict_is_rejected_as_provenance_node_missing`
  で閉鎖した（SHA-256 `a7160e6749e0044b1ce7e2e76ead4f6a959ce6ed9c8efff355238445f3f0fc89`）。
  5要素すべてに1対1のtest対応がある。
- **CL-6A-03**：Humanが緩い読みを採用（「緩い読みでよい。」）。見逃し側は負例テスト群と
  bootstrap review pipelineの注入検査、誤停止側は正例テスト群が回帰検出器を兼ねる。
  誤停止率・変異検査の系統的測定はWork 8の評価指標として割当て済みであり前倒ししない。
- **CL-6A-02**：permission過剰は`superuser`拒否テスト3件、staleは既存2件、optional観測欠測は
  `test_i10_missing_external_records_do_not_block_current`の引用で被覆。
  **crash後の再開はWork 7Aへ移す（選択肢ア）。** 現在の被覆は「記録済みfailed実行の再実行」までで、
  書込み途中の破損からの復旧はWork 7Aの中核項目「worker停止後にcheckpointから再開し、
  side effectを重複させない」で扱う。02の本旨（権限・stale・crash・任意観測の混同を防ぐ区別）の
  負例は揃っている。

## 3. 完了に含まれない範囲

- crash後の実地復旧（Work 7Aへ移管。移管の事実は本Decisionとchecklist Evidence節が正本）。
- 誤停止率・変異検査の系統的測定（Work 8）。
- `CL-6A-05`（Change Set・Test Evidenceの正式artifact未整備）、`CL-6A-04/06/07`（基盤未整備）、
  `CL-6A-11`（段の関門）。Work 6Aの段完了ではない。

## 4. 既存recordへの影響

new-onlyで作成した。checklistは当該checkbox 3つとEvidence節の追記だけを更新する。
