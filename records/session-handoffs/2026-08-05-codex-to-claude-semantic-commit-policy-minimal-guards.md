# Codex → Claude：意味単位コミットの最小ガード方針を固定する指示

## 誰が何をするか

- **Human**は、通常のコミットについては毎回の個別承認を不要とし、過剰な制限を課さず、問題を起こす操作だけを最小限に防ぐ方針を承認した。
- **Codex**は、この承認の範囲を固定する。
- **Claude**は、この文書に指定した方針・記録・Plan・checklist・TODOを更新し、意味単位の一つのコミットとして確定する。

これは、`ISSUE-HTC-C9F6C917`のPlan提案全体を承認するものではない。runner、executor、Git metadata preflight、cache routingの実装には着手しない。

## Humanの決定

通常の開発作業は、次の最小条件をすべて満たす場合、コミットごとのHuman明示指示なしにコミットしてよい。

1. 一つの目的と確認結果を独立して説明できる、意味的に完結した作業単位である。
2. stage対象は明示したrepository-relative pathの列挙だけである。`git add -A`、`git add .`、範囲外ファイルの一括追加を使わない。
3. `git diff --check`と、変更に応じたtest／validatorを実行して合格している。`TODO_NEXT_SESSION.md`を含める場合は、共通手順に従い`python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`も合格している。
4. commit後はread-onlyで状態を照合し、完了済み作業単位を未コミットのまま次の作業へ渡さない。

次は引き続きHumanの明示承認を必要とし、通常commitの自律化に含めない。

- 方針変更、段完了、意味的裁定、不可逆操作、外部送信
- push、tag、amend、rebase、reset、force push、履歴書換え
- sandboxまたはhostの権限の迂回

guarded commit、hook、コミットごとの恒久的な承認ファイル、巨大なcommit manifestは導入しない。Claudeのローカル完了報告（Git ignore済み）はstage対象にしない。

## Claudeが更新する成果物

1. 新規Decisionを作成する。

   `records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md`

   decision IDは`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`とする。上記Humanの決定、対象、除外、既存`stage_completion`承認を維持すること、`ISSUE-HTC-C9F6C917`のPlan提案全体を承認していないことを明記する。

2. `AGENTS.md`の「コミット方針」を更新する。毎回のHuman明示指示を必須とする記述を上の最小条件へ置換する。意味単位の分割、明示path stage、検証、post-commit read-only照合、未コミット遷移停止を記す。`stage_completion`などのHuman承認境界を緩めない。

3. `docs/development/2026-08-02-development-policy.md`の「作業単位終端のcommit reminder Pilot」を同じ方針へ更新する。旧方針が歴史として必要なら、旧制限を「置換済み」と短く記録する。自律化は通常commitだけであり、push等を含まないことを明確にする。

4. `docs/development/prompts/todo-handoff-update.md`の手順6を更新する。`completed_work_unit_uncommitted`では、最小条件を満たす意味単位コミットを機械処理で行い、その後にtransitionを再実行する。条件を満たせないときだけ停止する。毎回Humanへ確認する文言を削除する。

5. `docs/development/2026-08-03-initial-development-checklist.md`のCommit／handoff安定化節を更新する。旧「自動commitを対象外」の完了claimを置換し、今回のDecisionと最小ガードをEvidenceとして接続する。

6. `docs/current/reviewcompass3-plan-current.md`のInter-work表のCommit／handoff stability行を更新する。stateは完了のままにし、実施範囲へ「意味単位commitの自律化と最小ガード」を追加する。未完了境界にはpush、hook、履歴書換えを残す。

7. `TODO_NEXT_SESSION.md`を共通手順に従って現在位置へ更新する。C9 Plan提案が全体としてはまだHuman判断待ちであることを保ち、今回のDecisionは通常commitの運用だけを確定したと記す。Decision、更新されたPolicy、Current Plan、checklistの実際のSHA-256を機械取得して参照する。

## 検証とコミット

- 上記文書を再読込し、Decisionから各更新先への参照が解決することを確認する。
- `git diff --check`を実行する。
- 公式runnerで全testを実行し、receiptを次へ新規作成する。

  `records/development/2026-08-05-semantic-commit-minimal-guards-test-receipt-v1.json`

  ```text
  .venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt records/development/2026-08-05-semantic-commit-minimal-guards-test-receipt-v1.json
  ```

- 最終stage前にTODO validatorを実行する。
- stageは、この指示で作成・更新したpathだけを明示列挙する。`git add -A`と`git add .`は使わない。
- この作業単位の内容を一つの意味単位コミットにする。commit messageは`Adopt semantic commits with minimal guards`とする。
- push、tag、rebase、reset、amend、guarded commit、hook、外部送信をしない。

## 禁止事項

- `config/development-policy.json`、`tools/development/policy.py`、既存testを変更しない。`stage_completion`は通常Git commitを意味しないため、今回の対象外である。
- C9のPlan proposalの状態を変更しない。runner・config・policy evaluator・operation executor・cache routingを実装しない。
- Issueのstate、Task Contract、外部DATA_ROOT、既存Evidenceを変更しない。

## Claudeの完了報告

commitには混ぜず、次のローカル報告だけを作る。Git ignore済みのためstageしない。

`records/session-handoffs/2026-08-05-claude-to-codex-semantic-commit-policy-minimal-guards.md`

報告には、commit SHA、Decision path、変更した各path、full test数、TODO validator結果、C9全体・push等を変更していないことを記す。
