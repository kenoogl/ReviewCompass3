# TODO handoff update

`TODO_NEXT_SESSION.md`を読む、作る、更新する、検証するときは、この手順だけを使う。

1. session開始時にroot TODOを入口として読み、authority、Plan、checklist、Task Contract、固定Evidenceを
   参照して現在状態を確認する。TODO自体をWorkflow stateまたは完了Evidenceの正本にしない。
2. LLMは文章操作と意味分析だけを行う。state導出、Digest、件数、byte数、参照、file書込み、Test、Git確認は
   機械処理にする。stateを手入力で推測しない。
3. 新規作成または構造復元では
   `docs/development/templates/TODO_NEXT_SESSION.template.md`を使う。通常更新では構造化入力と
   `tools/development/todo_handoff_projection.py`から現在projectionを生成する。
4. 現在位置、active Issue 1件、最新authority／EvidenceのpathとDigest、次の一作業、blocker、
   Human判断待ち、stale／deferred、Git／Testだけを現在値へ置き換える。過去session、完了Claim、
   手戻り詳細を累積しない。詳細は固定sourceを持つCandidate／Issue／Evidenceへ保存する。
5. `tools/development/todo_compaction.py`で12,288 bytes以下、active ID 1件、禁止履歴0、参照解決を
   機械検証する。最終stage前に次を実行する。

   `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`

6. 完了した作業単位から次へ移る前に次を実行する。

   `python3 -m tools.development.work_unit_transition --work-status completed`

   `completed_work_unit_uncommitted`なら、`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`の最小条件
   （意味的に完結した単位、明示pathだけのstage、`git diff --check`と該当test／validatorの合格、
   commit後のread-only照合）を満たす意味単位コミットを機械処理で行い、その後にtransitionを再実行する。
   最小条件を満たせないときだけ次作業を開始せず停止して報告する。
7. Git欄はcommit安定形式にする。TODOを含むcommit自身のSHA、固定ahead／behind、push済否、
   未コミット状態を書かない。commit後はread-onlyで再照合し、Git状態転記だけの追加commitを作らない。

機械処理がなく手入力による手戻りが生じた場合は、現行TODOへ詳細を追加せず、期待executor、実executor、
原因、Evidence、機械化案、routeを作業Evidenceへ記録する。
