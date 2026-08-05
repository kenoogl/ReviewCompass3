# 意味単位コミットの最小ガード Decision v1

- decision ID：`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`
- decision maker：Human
- decided at：2026-08-05
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-semantic-commit-policy-minimal-guards.md`

## 1. Humanの決定

Humanは、通常のコミットについて毎回の個別承認を不要とし、過剰な制限を課さず、問題を起こす操作だけを
最小限に防ぐ方針を承認した。

通常の開発作業は、次の最小条件を**すべて**満たす場合、コミットごとのHuman明示指示なしにコミットしてよい。

1. 一つの目的と確認結果を独立して説明できる、意味的に完結した作業単位である。
2. stage対象は明示したrepository-relative pathの列挙だけである。`git add -A`、`git add .`、
   範囲外fileの一括追加を使わない。
3. `git diff --check`と、変更に応じたtest／validatorを実行して合格している。
   `TODO_NEXT_SESSION.md`を含める場合は、共通手順に従い
   `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`も合格している。
4. commit後はread-onlyで状態を照合し、完了済み作業単位を未コミットのまま次の作業へ渡さない。

## 2. 対象外（引き続きHumanの明示承認が要る）

次は通常commitの自律化に含めない。

- 方針変更、段完了、意味的裁定、不可逆操作、外部送信
- push、tag、amend、rebase、reset、force push、履歴書換え
- sandboxまたはhostの権限の迂回

また、次は導入しない。

- guarded commit
- hook
- コミットごとの恒久的な承認file
- 巨大なcommit manifest

Claudeのローカル完了報告（`records/session-handoffs/*-claude-to-codex-*.md`、Git ignore済み）は
stage対象にしない。

## 3. 既存のHuman承認境界を緩めない

`stage_completion`など、既存のHuman承認境界はそのまま維持する。`stage_completion`は通常のGit commitを
意味しないため、この決定の対象外である。`config/development-policy.json`と
`tools/development/policy.py`は変更していない。

## 4. この決定が承認していないこと

- `ISSUE-HTC-C9F6C917`のPlan提案（`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md`、
  SHA-256 `722e9448971bcf3e97423ab1b9b137ca202f1f1c0ed7afdd92a619738e608bfa`）**全体の承認ではない**。
  同提案の状態は`awaiting_human_approval`のままである。
- runner、構造化argv executor、Git metadata preflight、cache routingの実装には着手しない。
- Issueのstate、Task Contract、外部DATA_ROOT、既存Evidenceは変更しない。

## 5. この決定を反映した文書

| path | SHA-256 |
| --- | --- |
| `AGENTS.md` | `b7157936d92e7c322c32c68a6536c304ce24d0d170cf5b8a82a1c205b008a502` |
| `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |
| `docs/development/prompts/todo-handoff-update.md` | `eff64878479ce82a48f8e5b4160dd7913364268c9e94d1a6f0a63087e7fb0f4d` |
| `docs/development/2026-08-03-initial-development-checklist.md` | `7e7a2971fe67640dcccf21adddbf3da917201ec94c2bec1767a6caa1322212f5` |
| `docs/current/reviewcompass3-plan-current.md` | `6100ea7b6f0fa0ec025e076eadcd322609a0019222ad9c81045bb6ab827cca2f` |

反映の内容は次のとおりである。

- `AGENTS.md`の「コミット方針」：毎回のHuman明示指示を必須とする記述を、上の最小条件へ置換した。
  意味単位の分割、明示pathのstage、検証、post-commit read-only照合、未コミット遷移の停止を記した。
- 開発方針の「作業単位終端のcommit reminder Pilot」：同じ方針へ更新し、旧制限を「置換済み」として
  短く残した。自律化は通常commitだけであり、pushなどを含まないことを明記した。
- TODO handoff手順の手順6：`completed_work_unit_uncommitted`のとき、最小条件を満たす意味単位コミットを
  機械処理で行い、transitionを再実行する。条件を満たせないときだけ停止する。
- checklistのCommit／handoff安定化節：旧「自動commitを対象外」の完了claimを置換し、本Decisionと
  最小ガードをEvidenceとして接続した。
- Current PlanのInter-work表：Commit／handoff stability行の実施範囲へ「意味単位commitの自律化と
  最小ガード」を追加した。stateは`verified / completed`のままとし、未完了境界にpush、hook、
  履歴書換えを残した。

## 6. この決定を実行可能にした根本修正

開発方針文書を更新すると、その文書を過去のDigestで`fixed_sources`に含むTask Contractの検証が壊れた。
これは方針更新を取り止める理由ではなく、固定source検証が三状態を一貫して扱えていないことが原因である。
Humanの指示（`records/session-handoffs/`
`2026-08-05-codex-to-claude-repair-historical-task-contract-source-resolution.md`）に従い、
`tools/development/issue_resolution_pilot.py`へv1／v2共通の固定source resolverを実装した。

- 歴史状態：pinされたsourceを受理時点のGit blobで照合する。
- 現在有効状態：working treeと一致しなければ停止する。
- `active_stale`：source pinで有効化せず停止したままにする。
- pinの無いsourceは、pin recordの明示的な`unpinned_source_policy: "verify_working_tree"`が
  ある場合だけworking treeで照合する。暗黙のfallbackはしない。

既存のTask Contract、lifecycle status record、source pin record、Evidence、Decisionは書き換えず、
new-onlyのlifecycle status／source pin recordだけを追加した。
`session-transcript-eventual-preservation-v1`の`active_stale`は維持し、pinを追加していない。

診断Evidenceとして、根本原因を再現した失敗receipt
`records/development/2026-08-05-semantic-commit-minimal-guards-test-receipt-v1.json`を保持し、
修正後のGREEN receipt
`records/development/2026-08-05-semantic-commit-minimal-guards-green-test-receipt-v1.json`と
併記する。
