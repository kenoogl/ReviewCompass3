# Codex → Claude：TODO二段更新の例外復元境界を修正する指示

## 問題の再現と根本原因

`tools/development/todo_update_path.py`は「どこかで失敗したらTODOを更新前のbytesへ戻す」と仕様化している。
しかし`run_two_phase_update()`は`TodoUpdatePathError`だけを捕捉していた。

そのため、次の再現で2回目の公式Test実行が通常の例外を送出すると、TODOは1回目receiptで更新されたまま戻らない。

```text
first receipt: 正常
TODO candidate write: 正常
second official test: RuntimeError("second run unavailable")
結果: calls=first,second / todo_restored=False
```

これは局所的な例外処理の不足ではなく、二段更新を「最終確認まで原状復帰可能なトランザクション」として
境界定義・受入Testへ落とし切れていなかった設計不足である。

## 誰が何をするか

- **Human**は、この不整合への対応を指示した。
- **Codex**は、修正を全例外に対するtransaction保証へ限定し、別機能の追加を禁止する。
- **Claude**は、RED Testで復元保証を固定し、既存の二段更新経路を修正し、CLIでTODOの全Test表示を再生成する。

この修正は`DEC-RECORD-GENERATION-PLAN-001`のTODO最小縦切りの範囲内である。新しいDecisionは作らない。

## 正本と不変条件

- 設計：`docs/design/2026-08-05-record-generation-issue-plan-proposal.md`
- 更新経路：`tools/development/todo_update_path.py`
- 公式runner：`tools/development/policy_test_runner.py`
- 対象Issue：`ISSUE-HTC-66C3E6CA`

固定する不変条件は次である。

1. 一時receiptからTODOを書き始めた後、**最終receiptの検証が成功するまで**更新は確定しない。
2. `Exception`を継承する失敗（公式runner実行失敗、receipt読取失敗、候補生成、write、read-back、
   validator、2回のreceipt照合を含む）が起きた場合、TODOが元bytesと異なれば必ず元bytesへ戻す。
3. 1回目の公式runnerが失敗した場合は、TODOを一度も変更しない。
4. `KeyboardInterrupt`と`SystemExit`は捕捉しない。
5. 復元自体に失敗した場合は`todo_restore_failed`で停止する。成功時に元の失敗を隠さない。
6. CLIは内部例外のtracebackを成功扱いにせず、停止JSONと非0 exitで返す。

## 作業単位1：RED Test（実装を変更しない）

既存`tests/test_todo_update_path.py`へ、少なくとも次の失敗注入Testを追加する。

1. **2回目runner例外**：1回目receipt後に`RuntimeError`を送出する。TODOは元bytesへ戻り、呼出し順は
   `first, second`だけであり、呼出し元には`TodoUpdatePathError`が返る。
2. **1回目runner例外**：TODOは元bytesのまま、2回目を呼ばず、`TodoUpdatePathError`が返る。
3. **最終receipt読取例外**：runner APIがreceipt pathを返すが、そのfileが読めない状態を注入する。TODOは元bytesへ戻る。
4. **CLI経由の2回目runner例外**：CLIは停止JSONと非0を返し、TODOを元bytesへ戻す。tracebackを通常出力へ流さない。

既存の不一致receipt、read-back破損、validator失敗のTestは緩めない。

REDを実行し、次へ記録する。

`records/development/2026-08-05-todo-update-transaction-boundary-red-evidence-v1.md`

RED TestとRED Evidenceだけを1つの意味的commitにする。

## 作業単位2：transaction境界のGREEN修正

`run_two_phase_update()`とCLIを、上記不変条件を満たすように修正する。

- 既存の`TodoUpdatePathError`を保ち、必要なら公式runner／receipt読取に由来する失敗を
  意味の分かる既存または新設stop codeへ正規化する。
- rollbackは、TODOが書き換わった可能性のあるすべての`Exception`経路で行う。
- 1回目runner失敗時は、元TODOへの追加writeを行わない。
- `run_two_phase_update()`の二段比較、`default_verify()`、atomic write、receiptの構造化集計を再実装・複製しない。
- CLIは`run_two_phase_update()`を唯一のTODO更新経路として維持する。
- `except BaseException`、失敗の握りつぶし、TODO全Test行の手編集は行わない。

GREEN後、CLIを実行してTODOの全Test行を公式receiptから更新する。

```text
.venv/bin/python3 -m tools.development.todo_update_path \
  --project-root . \
  --todo TODO_NEXT_SESSION.md \
  --first-receipt records/development/2026-08-05-todo-update-transaction-boundary-first-receipt-v1.json \
  --final-receipt records/development/2026-08-05-todo-update-transaction-boundary-final-receipt-v1.json
```

次を作成する。

- `records/development/2026-08-05-todo-update-transaction-boundary-green-evidence-v1.md`
- `records/development/2026-08-05-todo-update-transaction-boundary-first-receipt-v1.json`
- `records/development/2026-08-05-todo-update-transaction-boundary-final-receipt-v1.json`

GREEN Evidenceには、再現した`todo_restored=False`、修正後の各失敗注入結果、CLIによる実際のfirst/final集計、
TODO全Test行との一致、対象外を明記する。

GREEN実装、test、Evidence、2 receipt、CLI生成済みTODOを1つの意味的commitにする。

## 検証と対象外

- `tests/test_todo_update_path.py`、`tests/test_todo_record_generation.py`、公式全Testを実行する。
- CLI実行後、TODO validator、compaction validator、Evidence節Digest照合、TODO表示とfirst/final receiptの
  構造化集計照合、`git diff --check`を実行する。
- commit後にread-only照合と`python3 tools/development/work_unit_transition.py --work-status completed`を実行する。
- Evidence／Decision一般化、自由文・Evidence linkの自動生成、Issue state、Task Contract、policy、config、
  cache root、argv executor、移行inventory、外部操作を変更しない。
- 新しい問題が安全・authority・受入条件を超える場合は、継ぎ足さず停止して報告する。

## Claudeの完了報告

Git管理外の次へ保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-repair-todo-update-transaction-boundary.md`

RED／GREEN commit SHA、失敗注入の復元結果、CLIのfirst/final集計、TODO表示、対象外を報告する。
