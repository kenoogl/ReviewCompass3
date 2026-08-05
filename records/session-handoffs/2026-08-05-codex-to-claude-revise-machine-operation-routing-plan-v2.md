# Codex → Claude：機械操作routing Plan提案 v2 の作成指示

## 誰が何をするか

- **Human**は、`ISSUE-HTC-C9F6C917`の次作業として、既存Plan提案を改訂し、承認可能なv2提案を作るよう指示した。
- **Codex**は、改訂の対象・結論・非対象をこの文書へ固定する。
- **Claude**は、新しいv2提案、test receipt、TODOだけを作成し、意味単位commitとして確定する。

これは実装承認ではない。operation runner、argv executor、Git preflight、cache routing、config、policy evaluator、Test code、Issue state、Task Contractを変更しない。

## 改訂が必要な理由

旧提案`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md`は、開発方針の旧Digestを固定入力にしている。また、Git metadata書込みごとに「止めてHumanへ要求する」前提であり、Humanが承認した次の方針と一致しない。

- 通常commitは、意味的完結・明示path stage・検証・post-commit read-only照合の最小4条件を満たせば、コミットごとのHuman承認なしに実行する。
- 操作に必要な権限は、失敗後に切り替えるのではなく、作業単位の開始前に機械が全操作を判定する。
- sandbox／hostの承認そのものは迂回しない。必要な承認が未取得なら、最初の書込みを試さず、作業単位の開始前に一度だけ要求する。

旧提案は履歴として残す。上書き・削除・状態変更をしない。

## Claudeが作るv2提案

新規作成先：

`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`

状態は`awaiting_human_approval`とする。正式Plan、Decision、Task Contractではないことを冒頭に明記する。

### 必須内容

1. **固定入力を機械再取得する。**
   対象Issue、関連triage decision、開発方針、`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`、V4 approval／closure Evidence、隣接Issueのpathと現在のSHA-256を表にする。旧提案のSHA-256も「superseded proposal」として参照する。

2. **問題と非対象を平易に説明する。**
   LLMが目的と意味を扱い、機械が決定的なoperation inventory、argv、cwd、書込み分類、権限種別、cache先、receiptを扱う境界を残す。host側のJavaScript tool構文・外部tool API schema・sandbox承認の決定はproject内では解けないことを明記する。

3. **最小縦切りを改訂する。**
   v2の推奨案は、次の3部だけとする。

   - versioned operation inventory：作業単位で必要な操作を、read-only／project artifact write／Git metadata write／externalに分類する。
   - permission preflight：実行前にinventory全体を走査し、必要な権限種別を一回で出す。未取得なら書込みを一度も試さず停止し、hostへ一回の承認要求を渡す。取得済みなら正常に続行する。
   - execution receipt：inventory、preflight verdict、実行結果を結ぶ。

   通常のGit commitは、`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`の4条件を満たす場合、Humanの個別承認を要求しない。これはsandboxの権限承認を自動化・迂回する意味ではない。

4. **最初に含めないものを明確にする。**
   構造化argv executor、shell特殊文字対策の全面移行、cache root固定、既存直接shell操作の一括置換、host側tool構文の解決、外部送信、`ISSUE-HTC-66C3E6CA`の定型record生成は後続に残す。

5. **受入条件を更新する。**
   少なくとも、次を正常・負例・境界例で示す。

   - Git read-only／project artifact write／Git metadata write／external／unknownを誤分類しない。unknownはfail-closed。
   - write権限が必要な操作が一件でもあれば、最初のwrite前に全必要権限を一回で列挙する。
   - 権限が未取得ならexecutorが一度も呼ばれない。失敗してから権限を切替える経路はない。
   - 最小4条件を満たす通常commitは、Human個別承認を待たない。
   - inventoryとreceiptのidentityが一致しない場合は停止する。
   - host側の問題を解決済みと誤報しない。

6. **Human判断を3点だけに絞る。**

   - v2最小縦切りを承認するか。
   - project内runnerを既存policy runnerと分けるか統合するか。
   - 取得済み権限の確認をhost側へどう渡すか（project内は要求種別を出すだけとする）。

   既存直接操作の移行順、argv executor、cache rootは後続の個別Planで決めるため、今回の判断項目に入れない。

### TODO更新

`TODO_NEXT_SESSION.md`を共通手順で更新する。

- 旧提案は履歴、v2提案がHuman判断待ちであること。
- 次の一作業は、v2最小縦切りのHuman判断であること。
- v2提案、旧提案、今回のtest receipt、semantic commit Decisionの実SHA-256を機械取得して記録する。

## 検証とコミット

1. 新旧提案・TODOを再読込し、pathとSHA-256参照を再計算する。
2. `git diff --check`を実行する。
3. TODO validatorを実行する。

   `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`

4. 公式全testを実行し、receiptを次へ作る。

   `records/development/2026-08-05-machine-operation-routing-plan-v2-proposal-test-receipt-v1.json`

   ```text
   .venv/bin/python3 -m tools.development.policy_test_runner --suite full \
     --receipt records/development/2026-08-05-machine-operation-routing-plan-v2-proposal-test-receipt-v1.json
   ```

5. 最終stage前にTODO validatorを再実行する。stageは新規v2提案、TODO、receiptだけを明示列挙する。
6. commit messageは`Revise machine operation routing plan proposal`とする。
7. commit後は`git status --short`と`python3 tools/development/work_unit_transition.py --work-status completed`をread-onlyで確認する。

push、tag、amend、rebase、reset、force push、外部送信をしない。

## Claudeの完了報告

commitに混ぜず、次だけをローカルに作る。Git ignore済みのためstageしない。

`records/session-handoffs/2026-08-05-claude-to-codex-revise-machine-operation-routing-plan-v2.md`

報告にはcommit SHA、v2提案path、Human判断3点、全test数、TODO validator結果、実装やIssue stateを変更していないことを記す。
