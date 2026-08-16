# Claude → Codex：Task Contract固定source検証の根本修正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-historical-task-contract-source-resolution.md`

指定されたTDD、実装、new-only record作成、方針文書の確定、検証、単独の意味単位commitをすべて完了した。

## commit

- commit SHA：`2cc4b80661408927e6f6f28d377571a2bed02af9`
- message：`Resolve historical task contract sources for semantic commits`
- 18 file、927行追加・79行削除
- commit後のread-only照合：`git status --short`は空。
  `python3 tools/development/work_unit_transition.py --work-status completed`は
  `{"findings": [], "next_work_allowed": true, "reminder": null, "status": "passed"}`
- stageは対象pathの明示列挙のみ。`git add -A`と`git add .`は使っていない。

## RED の確認

新規test `tests/test_task_contract_source_resolution.py`（13 test）を先に追加し、機械実行した。

- RED：`7 failed, 6 passed`
  （失敗理由は、共通resolverと`development_records`公開入口が未実装であること、
  todo-compaction v1／v2のlifecycle status・source pin recordが存在しないこと、
  pinの無いsourceに対する明示policy検査が無いこと）
- RED testだけのcommitは作っていない。

固定した振る舞いは指示§1の6点である。

1. 歴史状態のv1契約が、方針文書がworking treeで変わってもpinで通る。
2. 歴史状態の**v2**契約も同じ条件で通る。
3. 歴史状態でpinが無く、明示policyも無ければ`pin_unresolvable`で停止する。
   明示`verify_working_tree`があるときだけworking treeで照合し、その場合も変更済みなら停止する。
   未知のpolicy値も`pin_unresolvable`で停止する。
4. pinの契約Digest、source Digest、Git blobの不一致はいずれも`source_pin_mismatch`で停止する。
5. `active`はworking tree不一致で停止し、`active_stale`はpinがあっても停止する。
   session-transcriptの停止意味は変えていない。
6. repositoryの三つの歴史契約が、各fixed sourceをpinされたGit blobまたは明示`verify_working_tree`で
   解決でき、pinのcommitとblobが受理時点のDigestと一致する。

## GREEN test数

| 対象 | 結果 |
| --- | --- |
| source pin／lifecycle関連（新規＋既存＋v1／v2契約＋pilot） | `54 passed` |
| TODO validator `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md` | `{"findings": [], "status": "passed"}` |
| 公式runner全test | `829 passed`（exit 0） |
| `git diff --check` | 合格（stage前後とも） |

receipt：

- 診断（根本原因を再現した失敗）：
  `records/development/2026-08-05-semantic-commit-minimal-guards-test-receipt-v1.json`
  （`failed` / `13 failed, 803 passed`）
- GREEN：`records/development/2026-08-05-semantic-commit-minimal-guards-green-test-receipt-v1.json`
  （`passed` / `829 passed`、SHA-256 `62c9b0bb0571ca615b77e858cfd525c0a17490a42a9c46c810e4dd488e23c9e8`）

両方をcommitに含め、Decisionでも併記した。失敗receiptは破棄していない。

## 実装（共通resolver）

`tools/development/issue_resolution_pilot.py`へ`resolve_fixed_sources()`を追加し、
v1の`validate_fixed_sources_for_contract()`とv2の`validate_implementation_task_contract_v2()`の
双方がこれだけを使う形にした。v2が持っていたworking treeの直接照合は削除した。

- 歴史状態（`historical`／`completed`／`completed_carried_forward`／`superseded`）：
  pinされたsourceを受理時点のGit blobで照合する。
- pinの無いsourceは、pin recordの明示的な`unpinned_source_policy: "verify_working_tree"`が
  ある場合だけworking treeで照合する。暗黙fallbackは無くした。
- `active_stale`は必ず`stale_fixed_source`で停止し、pinを読んで通過させない。
- 停止codeはschemaによらず同一にした。
- 緩めていない点：pinされたsourceが`content_digest`を持つ場合、**pinされたblobの中の**
  `content_digest`を検証する。working tree照合側の`content_digest`検証も従来どおり残した。
- contract IDから正本contract fileを一意に引く`_task_contract_path_for_id()`を追加し、
  v2のようにrecordだけを受け取る経路でも状態解決できるようにした。

## new-onlyで作成したstatus／pin records（5件）

既存recordは一件も編集していない。

| path | 種別 | 対象契約 |
| --- | --- | --- |
| `records/development/2026-08-05-task-contract-source-pin-early-pilot-policy-v1.json` | source pin | early-pilot v1（方針文書だけ） |
| `records/development/2026-08-05-task-contract-lifecycle-status-todo-compaction-v1.json` | lifecycle status `historical` | todo-compaction v1 |
| `records/development/2026-08-05-task-contract-source-pin-todo-compaction-v1.json` | source pin | todo-compaction v1（方針文書だけ） |
| `records/development/2026-08-05-task-contract-lifecycle-status-todo-compaction-v2.json` | lifecycle status `historical` | todo-compaction v2 |
| `records/development/2026-08-05-task-contract-source-pin-todo-compaction-v2.json` | source pin | todo-compaction v2（方針文書だけ） |

- pinのcommitは`063236512845bde1bc8574c9507bba77f917fade`。これは、方針文書のblob SHA-256が
  各契約の固定Digest`9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`と一致し、
  かつ各契約の初出commitの祖先である唯一のcommitとして機械探索・照合して選んだ。
  HEADや推測したcommitを手入力していない。
- 全fixed sourceをpinしていない。working treeで変化した方針文書だけをpinし、残りは
  `unpinned_source_policy: "verify_working_tree"`の明示規則で照合する。
- 各lifecycle status recordには、歴史状態とする根拠（後続契約、完了Evidence、閉鎖Evidence）を
  pathとSHA-256で記録した。early-pilot v1の既存`completed_carried_forward`はそのまま維持した。

## 更新した文書

| path | 内容 |
| --- | --- |
| `AGENTS.md` | 「コミット方針」を最小4条件へ置換。共通手順への言及は既存testが要求する一行だけに保ち、追加箇所では引き継ぎ文書の名称文字列を使わない表現にした |
| `docs/development/2026-08-02-development-policy.md` | 同じ方針へ更新し、旧制限を「置換済み」として短く残した。自律化は通常commitだけであり、push等を含まない |
| `docs/development/prompts/todo-handoff-update.md` | 手順6を、最小条件を満たす意味単位commitを機械処理で行いtransitionを再実行する形へ更新 |
| `docs/development/2026-08-03-initial-development-checklist.md` | Commit／handoff安定化節の旧claimを置換し、本Decisionと最小ガードを接続 |
| `docs/current/reviewcompass3-plan-current.md` | Inter-work表の実施範囲へ「意味単位commitの自律化と最小ガード」を追加。stateは`verified / completed`のまま、未完了境界にpush、hook、履歴書換えを残した |
| `records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md` | `DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`。Human決定、対象外、`stage_completion`維持、C9全体を承認しないこと、全確定文書の実Digest、今回の根本修正を記録 |
| `TODO_NEXT_SESSION.md` | 共通手順で現在位置を更新。receipt digestのplaceholderは残していない。C9 Plan提案は全体としてHuman判断待ちである旨を明記 |

## 既存testの扱い

削除・弱化はしていない。事実に合わせた更新が2件ある。

1. `tests/test_task_contract_source_pin.py::test_cli_reports_pin_resolution_without_removing_existing_keys`：
   方針文書のpinを追加したため`pin_resolved_count`が`1`→`2`。件数の事実更新である。
2. `tests/test_issue_resolution_pilot_implementation_task_contract.py::test_contract_digest_and_fixed_references_are_current`：
   固定sourceの照合を、直接のworking tree比較から共通resolver経由へ変更した。契約自身のcontent digest、
   親契約・Issue・Plan・Challenge・承認Decisionのworking tree照合、各参照の`content_digest`検証は
   すべてそのまま残している。stale判定は緩んでおらず、pinの無い変更済みsourceが停止することは
   新規testで固定した。

この2件はいずれも今回の根本修正に伴う事実の反映であり、指示§1の「削除・弱化しない」に抵触しないと
判断した。もし別の扱いが必要なら指示をいただきたい。

## 維持した範囲

- `session-transcript-eventual-preservation-v1`の`active_stale`を維持した。source pinを追加しておらず、
  有効化していない。testで停止することを確認済み。
- `records/task-contract/`内の既存Task Contractを一件も書き換えていない（commitに含まれない）。
- 既存のlifecycle status record、source pin record、Evidence、Decisionを変更・削除・移動していない。
- 未コミットだった8成果物（6文書、semantic commit Decision、失敗receipt）を破棄・reset・revertしていない。
- `config/development-policy.json`と`tools/development/policy.py`、`stage_completion`関連の
  policy evaluator／testは変更していない。

## C9・push等を変更していないこと

- `ISSUE-HTC-C9F6C917`のPlan提案`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md`の
  状態は`awaiting_human_approval`のままである。
- operation runner、構造化argv executor、Git metadata preflight、cache routingは実装していない。
- V4 Issue 3件はいずれも`registered`のままで、file digestも変わっていない
  （`a4a1511e6090…`、`66cfe50ce791…`、`56e0911d6f56…`）。active Issueは0件。
- push、tag、amend、rebase、reset、force push、外部送信、hook、watcher、scheduler、
  background serviceのいずれも行っていない。
- 本完了報告はcommitに含めていない（`.gitignore`により無視される）。指示書もcommitしていない。
