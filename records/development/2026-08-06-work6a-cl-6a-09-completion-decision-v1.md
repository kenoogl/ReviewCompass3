# Work 6A `CL-6A-09` 項目完了 承認Decision v1

- Decision ID：`DEC-WORK6A-CL-6A-09-COMPLETION-001`
- decision maker：Human
- decided at：`2026-08-06T15:16:12+09:00`
- decision：`approved`
- decision class：`item_completion_decision`
- 関連Decision：`DEC-WORK6A-CL-6A-08-COMPLETION-001`

## 1. 承認対象

初期開発チェックリスト9節「Work 6A：初期sliceのnegative path」の項目`CL-6A-09`に
Humanが完了を承認した。

> 表示器だけのfailureで有効成果を破棄しないことを確認する。

Claudeが被覆済み5項目の敵対的検証結果を提示し、`fully_covered`と判定された本項目だけを
完了印の候補として諮った。Humanは「推奨案で」と回答した。

## 2. 完了根拠（独立検証済み）

被覆主張を疑う側から検証した独立検証で、次の2 testが項目の文言と1対1で対応することを確認した。

| test | 固定していること |
| --- | --- |
| `tests/test_session_bootstrap_e2e.py::test_display_failure_does_not_discard_valid_capture_or_authority` | renderer例外を注入し、raw captureとevidenceの残存、`diagnostics.status == "complete"`、`authority_status == "valid"`、`display_status == "failed"`を直接assert |
| `tests/test_session_bootstrap_e2e.py::test_missing_authority_is_incomplete_not_a_display_failure` | 逆方向。authority欠落は`incomplete`であって表示failureではない（`display_status == "rendered"`） |

公式全Testは`1032 passed`（failed 0、Python 3.9.6、pytest 8.4.2、fallback `false`）。

## 3. 同時に確定した部分被覆の扱い

同じ検証で、被覆済みとされていた他4項目は`partially_covered`と判定され、Humanの承認により
次のとおり処置した。正本は
`records/development/2026-08-06-work6a-inventory-correction-v1.md`（SHA-256
`41b6e8436f437da1eccf911f2e34cff211d5959110ed91e18ce9ea4887bfcdc0`）。

- `CL-6A-01`：未被覆だった「Plan欠落」を境界例
  `tests/test_work6a_coverage_boundaries.py::test_missing_compile_verdict_is_rejected_as_provenance_node_missing`
  で閉じた（追加時点で成功。検出機構は既存の汎用node検査）。
- `CL-6A-02`：「permission過剰」は実在する非引用test（`superuser`拒否3件）の引用補充、
  「optional観測欠測」は`test_i10_missing_external_records_do_not_block_current`の引用で閉じた。
- `CL-6A-03`：「誤停止側」はHumanが**緩い読み**を採用した（「緩い読みでよい。」）。既存の正例テスト群が
  誤停止の回帰検出を兼ねる。系統的測定（誤停止率、変異検査）はCurrent Planの評価指標として
  Work 8へ割当て済みであり、前倒ししない。
- `CL-6A-05`：Change SetとTest Evidenceは正式artifactが未整備のため、`out_of_approved_scope`相当へ
  分類を訂正し保留とした。

`CL-6A-01`〜`05`のcheckboxは、上記の残余があるため**未完了のまま保持**する。完了印を付けたのは
`CL-6A-09`だけである。

## 4. 完了に含まれない範囲

Work 6Aの段完了ではない。`CL-6A-04`（正式Workflow state未承認）、`CL-6A-06`（関数台帳未実装、
Work 4B領域）、`CL-6A-07`（外部side effect、Work 7領域）、`CL-6A-10`（Final Challenge専用負例、
別提案予定）、`CL-6A-11`（段の完了関門）は未着手のまま残る。

## 5. 既存recordへの影響

new-onlyで作成した。checklistは当該checkboxとEvidence節の追記だけを更新する。
旧inventoryは履歴として保持し、訂正は訂正recordが担う。
