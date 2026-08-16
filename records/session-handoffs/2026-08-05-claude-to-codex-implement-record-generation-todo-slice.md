# Claude → Codex：定型記録生成のTODO最小縦切り 実装 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-record-generation-todo-slice.md`

承認記録の作成と、3段階のTest先行実装を、それぞれ緑の意味単位commitとして確定した。**停止はしていない。**

## commit（4件）

| # | commit SHA | 役割 |
| --- | --- | --- |
| 0 | `0a4fdf0762e9f9f6d16fa896a8e5b08242832d7f` | 承認記録`DEC-RECORD-GENERATION-PLAN-001`、Plan状態の更新、TODO現在位置（文書・Decision・TODOだけ） |
| 1 | `1e2197536d96a1bd1e28485244361bbc0d72fd2d` | 公式Test receiptの構造化集計（Test、集計module、`policy_test_runner.py`だけ） |
| 2 | `e7e8b75eed604c1414f27d93504e8fb6d645b38a` | TODO用材料の収集・検証（収集module、Testだけ。root TODOは更新しない） |
| 3 | `8baac3741e5e45a315a43d3c63d9de9576e01806` | root TODOへの更新経路の切替（更新module、Test、root TODO、最終receipt、GREEN Evidence） |

各commitは明示pathだけをstageした。`git add -A`と`git add .`は使っていない。
commit後は`git status --short`が空、`work_unit_transition.py --work-status completed`は
`next_work_allowed: true`である。TODOだけの追加commitは作っていない。

## 開始時の固定input照合

Plan提案が固定入力として記録した7件（対象Issue、Human triage decision、TODO手順、Test runner、
TODO renderer、TODO validator、TODO compaction validator）のSHA-256が、作業開始時点の現状と
**すべて一致**することを機械確認した。不一致は0件で、停止条件1には該当しなかった。

## RED／GREEN

| 段階 | RED | GREEN（対象test） | GREEN（公式全test） |
| --- | --- | --- | --- |
| 1 受領証の集計 | `1 failed, 1 passed, 9 errors` | `11 passed` | `863 passed` |
| 2 TODO用材料の収集 | `9 errors` | `9 passed` | `872 passed` |
| 3 更新経路の切替 | `9 errors` | `9 passed` | `881 passed` |

RED testだけのcommitは作っていない。実装中にtestの期待を緩めていない。
段階1では、新しい受領証contractに合わせて既存`tests/test_policy_test_runner.py`の
偽run関数2箇所へ集計の書出しを追加した。assertionの緩和はしていない。

## 最終receiptの集計

```json
{"errors": 0, "failed": 0, "passed": 881, "skipped": 0, "total": 881, "xfailed": 0, "xpassed": 0}
```

件数はpytestのreport objectから数えている。出力文字列の解析はしていない。その性質は
集計moduleと収集moduleのsource textをtestで機械確認している。

## 二段確認の一致

| 段 | receipt | SHA-256 | status |
| --- | --- | --- | --- |
| 一時（commitしない、repository外） | `<scratchpad>/record-generation-todo-temporary-receipt.json` | `d175bdb2cc2d4265f3c646d6f47de5d0640c186de2cd0214ba5f2acc3eb84f91` | `passed` |
| 最終（commitする） | `records/development/2026-08-05-record-generation-todo-green-test-receipt-v1.json` | `70aaeab191424651956f6d896df7da7c9e682d7cf376e45de925b78fbeafaf6a` | `passed` |

照合fieldは`test_summary`、`suite`、`python_version`、`pytest_version`、`fallback_used`、`status`の
6つで、**すべて完全一致**した。両段とも`passed 881／total 881`である。
最終receiptは更新済みTODOを含む状態で実行したものである。

## TODOの実際の変更範囲

機械が書き換えたのは**1行だけ**である。

```diff
-- 直近の全Test：venv公式runner `852 passed`、Python 3.9.6、pytest 8.4.2、fallback false
+- 直近の全Test：venv公式runner `881 passed`、Python 3.9.6、pytest 8.4.2、fallback false
```

- 自由文（全体説明、判断理由、次の一作業など）は1文字も変えていない。
- Evidence節のlink label、link path、行の並びは変えていない。
- 参照のSHA-256は全26件をbytesから計算し直し、記録済みの値と一致した。値は変わらないが、
  書き込んだのは人の手入力ではなく機械が計算した値である。
- 「直近の関連Test」行は意味的な選定を要するため機械が決めない。既存値を保った。

commit 0のTODO更新は人による現在位置の書換えであり、機械更新はcommit 3の1行だけである。
なおcommit 0では、更新規則に従い累積していた中間Evidence linkを4行整理して上限内に収めた。

## validator結果

| 検証 | 結果 |
| --- | --- |
| `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| TODO compaction validator | 合格（11,672 bytes、active ID 1件） |
| 参照Digest照合 | 26件一致 |
| read-back byte一致 | 一致 |
| `git diff --check` | 各commitのstage前後で合格 |

## 停止と原状復帰（testで固定）

| 状態 | 停止code | 二度目の実行 | root TODO |
| --- | --- | --- | --- |
| 二段の集計不一致 | `receipt_summary_mismatch` | 実行済み | 復帰 |
| 二段のversion不一致 | `receipt_summary_mismatch` | 実行済み | 復帰 |
| read-back不一致 | `todo_read_back_mismatch` | 実行しない | 復帰 |
| validator失敗 | `todo_verification_failed` | 実行しない | 復帰 |
| receiptが`passed`でない | `todo_candidate_failed` | 実行しない | 書かない |

収集器側も、参照fileの1 byte変更、summary欠落、`failed`、fallback、負数、`total`不整合、
未知field、見出し／対象行の欠落・重複、絶対path、`..`、symlinkのすべてで停止し、
TODOのbytesを変えないことをtestで固定している。

## 未実施の範囲

- Evidence／Decisionの定型欄への一般化（案B）。承認条件は、TODOで複数回の実運用が手入力訂正なしで
  通ってからHumanが判断することである。今回はその1回目にあたる。
- `render_todo_handoff()`による全TODO再生成、TODO全体の新schemaへの移行。
- 「直近の関連Test」行の自動選定、監査内訳の自動集計。
- Evidence／Decisionの自動生成、既存Evidence／Decision／receiptの一括書換え。
- Issueのstate変更。`ISSUE-HTC-66C3E6CA`、`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`は
  いずれも`registered`のままで、file digestも変わっていない
  （`56e0911d6f56…`、`a4a1511e6090…`、`66cfe50ce791…`）。
- V4の正式Issue Resolution Plan、Task Contract、Workflow permit、UI、hook、watcher、scheduler、
  background service。
- Git／shell／外部toolの実行routing（`ISSUE-HTC-C9F6C917`の範囲）。
- push、PR、外部送信。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。

## 停止の有無

**停止なし。** 指示書の停止条件1〜5のいずれにも該当しなかった。固定input digestは一致し、
構造化集計は承認範囲内のmoduleとhookで得られ、root TODOの更新は機械管理部分の1行だけに収まり、
二段確認は完全一致し、既存Task Contractとauthorityの固定source整合も崩れていない。
