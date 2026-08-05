# 定型記録生成 TODO最小縦切り GREEN Evidence v1

- 対象Issue：`ISSUE-HTC-66C3E6CA`
- 承認：`DEC-RECORD-GENERATION-PLAN-001`
  （`records/development/2026-08-05-record-generation-issue-plan-approval-decision-v1.md`）
- 承認対象の設計：`docs/design/2026-08-05-record-generation-issue-plan-proposal.md`（案A、TODOだけ）
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-record-generation-todo-slice.md`

## 1. 実装した3段階

| 段階 | 内容 | module | 受入test |
| --- | --- | --- | --- |
| 1 | 公式Test receiptへ構造化`test_summary`を追加する | `tools/development/pytest_summary.py`、`conftest.py`、`tools/development/policy_test_runner.py` | `tests/test_policy_test_runner_summary.py` |
| 2 | TODO用材料の収集・検証（候補bytesを返すだけ） | `tools/development/todo_record_generation.py` | `tests/test_todo_record_generation.py` |
| 3 | root TODOへの更新経路（二段確認） | `tools/development/todo_update_path.py` | `tests/test_todo_update_path.py` |

いずれもTest先行で進め、REDを機械実行で確認してから実装した。RED testだけのcommitは作っていない。

| 段階 | RED | GREEN（対象test） | GREEN（公式全test） |
| --- | --- | --- | --- |
| 1 | `1 failed, 1 passed, 9 errors` | `11 passed` | `863 passed` |
| 2 | `9 errors` | `9 passed` | `872 passed` |
| 3 | `9 errors` | `9 passed` | `881 passed` |

件数はpytestのreport objectから数えており、実行結果の出力文字列を解析していない。
その性質は、集計moduleのsource textに出力解析の語が現れないことをtestで機械確認している。

## 2. 二段確認の実行結果

| 段 | receipt | SHA-256 | status | 集計 |
| --- | --- | --- | --- | --- |
| 一時（commitしない） | `<scratchpad>/record-generation-todo-temporary-receipt.json` | `d175bdb2cc2d4265f3c646d6f47de5d0640c186de2cd0214ba5f2acc3eb84f91` | `passed` | passed 881／total 881 |
| 最終（commitする） | `records/development/2026-08-05-record-generation-todo-green-test-receipt-v1.json` | `70aaeab191424651956f6d896df7da7c9e682d7cf376e45de925b78fbeafaf6a` | `passed` | passed 881／total 881 |

一時receiptはrepository外の作業領域に置き、commitしない。

照合したfieldは`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の
6つで、**すべて完全一致**した。集計は両段とも
`{"errors": 0, "failed": 0, "passed": 881, "skipped": 0, "total": 881, "xfailed": 0, "xpassed": 0}`である。

最終receiptは、更新済みTODOを含む状態で実行して得たものであり、その`source_state_digest`は
更新後の作業tree状態を指す。

## 3. TODOの実際の更新範囲

機械が書き換えたのは**1行だけ**である。

```diff
-- 直近の全Test：venv公式runner `852 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `881 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

- 自由文（全体説明、判断理由、次の一作業など）は1文字も変えていない。
- Evidence節のlink label、link path、行の並びは変えていない。
- 参照のSHA-256は全26件をfileのbytesから計算し直し、記録済みの値と一致した。一致したため
  値としての変化は無いが、書き込んだ値は人の手入力ではなく機械が計算したものである。
- 「直近の関連Test」行は意味的な選定を要するため機械が決めない。既存の値をそのまま保った。

## 4. validator結果

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator（size、active ID、禁止履歴、参照到達性） | 合格 |
| 参照Digest照合（`validate_todo_reference_digests`） | 26件一致 |
| 書込み後のread-back byte一致 | 一致 |
| `git diff --check` | 合格 |

## 5. 停止と原状復帰

更新経路は、次のいずれでもroot TODOを更新前のbytesへ戻して停止する。testで固定している。

| 状態 | 停止code | 二度目の実行 |
| --- | --- | --- |
| 二段の集計が不一致 | `receipt_summary_mismatch` | 実行済み。TODOを復帰 |
| 二段のversionが不一致 | `receipt_summary_mismatch` | 実行済み。TODOを復帰 |
| 書込み後のread-backが不一致 | `todo_read_back_mismatch` | **実行しない**。TODOを復帰 |
| validator失敗 | `todo_verification_failed` | **実行しない**。TODOを復帰 |
| receiptが`passed`でない | `todo_candidate_failed` | **実行しない**。TODOを書かない |

## 6. 既存Issueの状態

`ISSUE-HTC-66C3E6CA`のIssue recordは`registered`のままであり、file digestも変更していない。
他の2 Issueも`registered`のままである。V4の正式Issue Resolution Plan、Task Contract、
Workflow permitは作っていない。

## 7. 未実施の拡張

- Evidence／Decisionの定型欄への一般化（案B）。承認条件は、TODOで複数回の実運用が
  手入力訂正なしで通ってからHumanが判断することである。今回はその1回目にあたる。
- `render_todo_handoff()`による全TODOの再生成、TODO全体の新schemaへの移行。
- 「直近の関連Test」行の自動選定、監査内訳の自動集計。
- Git／shell／外部toolの実行routing（`ISSUE-HTC-C9F6C917`の範囲）。
- Evidence／Decisionの自動生成、既存record／receiptの一括書換え、hook、watcher、scheduler、
  background service、UI、外部送信。
