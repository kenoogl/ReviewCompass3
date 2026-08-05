# Codex → Claude：意味単位commit方針を阻害するTask Contract固定source検証の根本修正

## 誰が何をするか

- **Human**は、通常commitを最小ガード付きで自律化する方針を承認した。また、方針文書の更新を外す暫定策ではなく、Task Contractの固定source検証を根本修正するよう指示した。
- **Codex**は、修正範囲・保持対象・停止境界をこの文書へ固定する。
- **Claude**は、下記のTDD、実装、new-only record、方針文書の確定、検証、意味単位commitを実行する。

これは`ISSUE-HTC-C9F6C917`のoperation runner、Git metadata preflight、cache routingを実装する指示ではない。C9のPlan提案は`awaiting_human_approval`のまま保つ。

## 問題の事実

未コミットの意味単位commit方針更新は、`docs/development/2026-08-02-development-policy.md`を更新する。
その文書を過去のDigestで`fixed_sources`に含むTask Contractが存在するため、現在working treeだけで照合すると、既に完了した作業の検証まで失敗する。

これは方針更新を取り止める理由ではない。固定source検証が、次の三状態をv1とv2で一貫して扱えていないことが根本原因である。

1. **歴史状態**：受理時点のGit blobと一致すればよい。現在の方針文書が更新されても、過去の契約は壊れない。
2. **現在有効状態**：working treeと一致しなければ停止する。
3. **`active_stale`**：source pinで有効化せず、停止したままにする。

既存のv1 resolverは一部の歴史状態だけをsource pinで扱えるが、v2 Task Contractはworking treeを直接照合している。この非対称を解消する。

## 保持対象と明示的な状態判断

### 必ず保持するもの

- `records/task-contract/`内の既存Task Contractは一切書き換えない。
- 既存のlifecycle status record、source pin record、Evidence、Decisionを変更・削除・移動しない。
- `session-transcript-eventual-preservation-v1`の`active_stale`は維持する。source pinを追加せず、有効化しない。
- 現在の未コミット8成果物（6文書、semantic commit Decision、failed receipt）は破棄・reset・revertしない。failed receiptは今回の根本原因を再現した診断Evidenceとして保持し、GREEN receiptと併記する。

### 今回のHuman承認に基づく状態判断

次の3契約は、実装済み・完了済みの過去作業を表すため、**new-only lifecycle status recordで歴史状態として扱う**。

| Task Contract | lifecycle status | 理由 |
| --- | --- | --- |
| `records/task-contract/issue-resolution-early-pilot-v1.json` | 既存の`completed_carried_forward`を維持 | すでに後続v2への繰越Evidenceがある |
| `records/task-contract/issue-resolution-todo-compaction-implementation-v1.json` | `historical` | v2にsupersedeされ、実装作業は完了済み |
| `records/task-contract/issue-resolution-todo-compaction-implementation-v2.json` | `historical` | TODO compaction実装は完了済みで、現行Workではない |

この状態判断は、通常commit方針のHuman承認を実現するために必要な固定source検証の境界に限る。Task Contractの目的、受入条件、当時のfixed source Digestを変更しない。

## Claudeが行うこと

### 1. 失敗をまずTestで固定する（RED）

既存testを削除・弱化せず、次の振る舞いを新規または拡張testで固定する。

1. 歴史状態のv1 Task Contractは、policy文書がworking treeで変わっていても、対応するsource pinが受理時点Git blobを指せば通る。
2. 歴史状態の**v2** Task Contractも、同じ条件で通る。
3. 歴史状態でpolicy文書のpinが無い場合は`pin_unresolvable`で停止する。
4. pinの契約Digest、source Digest、Git blobが違えば`source_pin_mismatch`で停止する。
5. `active`はworking tree不一致を停止し、`active_stale`はpinがあっても停止する。既存のsession-transcriptの停止意味を変えない。
6. repositoryの既存three historical contractsは、各fixed sourceを「pinされたGit blob」または明示された`verify_working_tree`で検証できる。policy文書の更新後も全体testが通る。

REDを機械実行して確認する。RED testだけをcommitしない。

### 2. resolverを一つに統一して実装する（GREEN）

`tools/development/issue_resolution_pilot.py`を、v1/v2で重複したworking-tree照合を持たない構造へ直す。

- lifecycle statusとsource pinを解決する共通関数を一つ設け、v1とv2の双方が利用する。
- `historical`、`completed`、`completed_carried_forward`、`superseded`は、new-only pin recordにあるpathを受理時点のGit blobで照合する。
- pinが無いsourceは、pin recordの明示的な`unpinned_source_policy: "verify_working_tree"`がある場合だけworking treeで照合する。暗黙fallbackは禁止。
- `active_stale`は必ず`stale_fixed_source`で停止し、pinを読んで通過させない。
- 異なる契約schemaでも、固定sourceの意味とエラーcodeを同一にする。v2のreference record内部の`content_digest`検証など、fixed source以外の既存検証を緩めない。

### 3. new-only status／pin recordsを作る

既存recordを編集せず、次を新規作成する。名前は必要なら同じ規則の範囲で調整してよいが、各対象契約・対象policy source・commit・SHA-256を一意に識別できること。

1. early-pilot用の**policy文書だけ**の追加source pin record
2. todo-compaction v1用lifecycle status recordとsource pin record
3. todo-compaction v2用lifecycle status recordとsource pin record

pinのcommitは、当該fixed sourceのSHA-256と一致するGit blobを機械的に探索・照合して選ぶ。現在のHEADや推測したcommitを手入力しない。全fixed sourceをpinする必要はない。policy文書のようにworking treeで変化したsourceだけをpinし、残りは`verify_working_tree`の明示規則で照合する。

各lifecycle status recordには、歴史状態とする根拠となる既存のcommit、後続contract、completion EvidenceをpathとSHA-256で記録する。

### 4. 意味単位commit方針の文書を確定する

現在の未コミット文書を基礎に、以下を確定する。

- `AGENTS.md`：TODOの共通入口への言及は既存testが要求する一行だけにする。追加箇所では`TODO_NEXT_SESSION.md`や`TODO`という文字列を避け、共通手順／handoff validator等の表現へ置換する。意味は変えない。
- `docs/development/2026-08-02-development-policy.md`：通常commitの自律化は、意味的完結・明示path stage・`git diff --check`と該当test／validator・post-commit read-only照合の4条件だけに限る。push、tag、amend、rebase、reset、force push、履歴書換え、権限迂回を含めない。
- `docs/development/prompts/todo-handoff-update.md`、checklist、Current Plan：上記と矛盾なく更新する。
- `records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md`：`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`として、今回のHuman決定と全確定文書の実Digestを記録する。
- `TODO_NEXT_SESSION.md`：共通手順で更新する。test receiptのDigest placeholderを残さない。C9 Plan提案全体は依然Human判断待ちであることを明記する。

`config/development-policy.json`の`stage_completion`、およびそれを検査する既存policy evaluator/testは変更しない。通常Git commitは`stage_completion`ではない。

### 5. 検証とcommit

1. `git diff --check`
2. source pin／lifecycle関連testの正常・負例・境界例
3. TODO validator：`python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`
4. 公式全test：

   ```text
   .venv/bin/python3 -m tools.development.policy_test_runner --suite full \
     --receipt records/development/2026-08-05-semantic-commit-minimal-guards-green-test-receipt-v1.json
   ```

5. すべてGREEN後、今回の対象pathだけを明示列挙してstageする。`git add -A`と`git add .`は禁止。
6. 一つの意味単位commitを作る。messageは`Resolve historical task contract sources for semantic commits`とする。
7. commit後、`git status --short`と`python3 tools/development/work_unit_transition.py --work-status completed`をread-onlyで実行する。

最終commitに含めるもの：resolver、関連test、新規lifecycle／pin records、semantic commit Decision、6更新文書、失敗を事実どおり記録したdiagnostic receipt、GREEN receipt、TODO。

最終commitに含めないもの：Claude完了報告、指示書、外部data、C9実装。

push、tag、amend、rebase、reset、force push、既存recordの更新・削除、外部送信をしない。

## Claudeの完了報告

commitに混ぜず、次のローカルファイルだけを新規作成する。Git ignore済みのためstageしない。

`records/session-handoffs/2026-08-05-claude-to-codex-repair-historical-task-contract-source-resolution.md`

報告には、commit SHA、REDの確認、GREEN test数、new-onlyで作成したstatus／pin records、更新文書、`active_stale`を維持したこと、C9・push等を変更していないことを記す。
