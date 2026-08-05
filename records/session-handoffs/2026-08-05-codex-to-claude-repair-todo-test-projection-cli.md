# Codex → Claude：TODO全Test表示を機械更新するCLIの修正指示

## 誰が何をするか

- **Human**は、最新全TestのTODO表示を、公式receiptから機械更新する作業を選択した。
- **Codex**は、手入力の訂正ではなく、既存の二段更新経路を実際に使えるようにする範囲を固定する。
- **Claude**は、TDDでCLIを追加し、そのCLIでroot TODOの全Test表示を更新して、同じ漏れを繰り返さない状態にする。

## 問題と原因

読み取り専用argv executorのGREEN receiptは`905 passed`である。

`records/development/2026-08-05-machine-operation-routing-read-only-argv-green-test-receipt-v1.json`

しかし`TODO_NEXT_SESSION.md`の`## Git・Test`節は`892 passed`のままである。

これはTestやexecutorの失敗ではない。`tools/development/todo_record_generation.py`と
`tools/development/todo_update_path.py`には、公式receiptの構造化`test_summary`から全Test行を更新する
機能があるにもかかわらず、前作業でその二段更新経路を呼ばず、TODO本文を直接更新したことが原因である。

数値を手で`905`へ直して終わらせない。既存の`run_two_phase_update()`を、機械処理として起動できるCLIにし、
そのCLIを実際に使って修正する。

## 承認済み範囲と対象外

この作業は`DEC-RECORD-GENERATION-PLAN-001`が承認したTODO最小縦切り（公式receiptからの全Test表示と
Evidence Digestの決定的更新）の範囲内である。新しいDecisionは作らない。

対象外：Evidence／Decision一般のrenderer、TODO自由文・Evidence link label・path・順序の自動決定、
Issue state、Task Contract、policy、config、cache root、argv executor、既存操作の移行、外部操作。

## 作業単位1：CLIのRED test（実装しない）

既存`tests/test_todo_update_path.py`へ、CLIの受入testを追加する。実装はこの段階で変更しない。

CLIの実行形式は次に固定する。

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/<first>.json \
  --final-receipt records/development/<final>.json
```

CLIの受入条件：

1. `--todo`、`--first-receipt`、`--final-receipt`を必須とする。省略時は停止する。
2. project root基準の相対pathだけを受ける。絶対path、`..`、symlink、`records/development/`外のreceipt pathを拒否し、TODOもreceiptも作成・変更しない。
3. `policy_test_runner`の正式APIを2回呼ぶ。1回目はfirst receiptを作り、既存`run_two_phase_update()`を通じてTODO候補を生成・検証し、2回目はfinal receiptを作る。
4. 2回の構造化集計・suite・Python版・pytest版・fallback・statusが一致しない場合、TODOを元のbytesへ戻して停止する。
5. 成功時、TODOの「直近の全Test」行は**1回目の公式receiptの構造化fieldからだけ**生成される。stdout正規表現や手入力を使わない。
6. 自由文、Evidence linkのlabel・path・順序、関連Test行を変更しない。既存のEvidence Digestはbytesから再計算される。
7. CLIはJSONで、status、first/final receipt path、全Test集計を出す。Git操作をしない。

RED実行と結果を次へ記録する。

`records/development/2026-08-05-todo-test-projection-cli-red-evidence-v1.md`

RED testとRED Evidenceだけを1つの意味的commitにする。

## 作業単位2：CLI実装と実修正（GREEN）

`tools/development/todo_update_path.py`に、上記CLIを実装する。

- 既存`run_two_phase_update()`、`policy_test_runner.load_config()`、`policy_test_runner.execute()`を再利用する。二段更新ロジックを複製しない。
- receipt pathの検証は、project rootと`records/development/`の境界を機械検証する。path外への書込みを試さない。
- CLIの実装は、TODO本文を直接編集しない。更新は`run_two_phase_update()`だけを通す。
- CLIの実装はGitを呼ばず、commit・pushをしない。

GREEN後、実際にCLIを次の固定pathで実行する。

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/2026-08-05-todo-test-projection-correction-first-receipt-v1.json \
  --final-receipt records/development/2026-08-05-todo-test-projection-correction-final-receipt-v1.json
```

この実行後のTODOの全Test行は、実行時の公式receiptと一致していなければならない。値を事前に想定・手記入しない。

次を作成する。

- `records/development/2026-08-05-todo-test-projection-cli-green-evidence-v1.md`
- `records/development/2026-08-05-todo-test-projection-correction-first-receipt-v1.json`
- `records/development/2026-08-05-todo-test-projection-correction-final-receipt-v1.json`

GREEN Evidenceには、前作業の`905 passed`とTODOの`892 passed`が不一致だったこと、CLIで得た実際のfirst/final集計、
TODOの全Test行が公式receiptから生成されたこと、対象外を記録する。

CLI実装、追加test、GREEN Evidence、2つのreceipt、TODO更新を1つの意味的GREEN commitにする。

## 検証

- 追加したCLI test、`tests/test_todo_record_generation.py`、既存`tests/test_todo_update_path.py`を実行する。
- CLIによる実修正後、`python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`、
  `python3 tools/development/todo_compaction.py TODO_NEXT_SESSION.md`、Evidence節に限定したDigest照合、
  TODOの全Test行とfinal receiptの構造化集計の独立照合を実行する。
- CLIのfirst receiptから生成したTODO数値が、比較済みのfinal receiptの構造化集計と一致することを確認する。
- 各commit前に`git diff --check`、commit後にread-only照合と
  `python3 tools/development/work_unit_transition.py --work-status completed`を実行する。

## 禁止事項と停止条件

- `TODO_NEXT_SESSION.md`の全Test行を手編集しない。
- Evidence／Decisionの一般化、自由文・link label・link path・順序の自動生成、既存recordの書換えを行わない。
- Issue state、Task Contract、policy、config、argv executor、cache root、移行inventoryを変更しない。
- push、外部送信、hook、watcher、scheduler、Git操作をCLIに追加しない。
- CLIが既存二段更新経路で処理できない矛盾、またはauthority／安全境界の問題を見つけた場合は、局所パッチを選ばず停止して報告する。

## Claudeの完了報告

Git管理外の次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-repair-todo-test-projection-cli.md`

RED／GREEN commit SHA、実際のfirst/final集計、TODO表示、検査結果、対象外を簡潔に報告する。
