# 範囲固定 v2：Work 7A第2項 前駆slice — read-only Gitによる捕捉とcheckout移動後照合

- 作成日：2026-08-09
- 作成者：Claude（Pilot）
- 状態：再範囲レビュー待ち（risk `high`のため、実装はHuman再開承認まで開始しない）
- 先行版：`scope-v1`（SHA-256 `ae40db7fdb4675f581fa516c1eaf9ec33cb36b1f83b55a1ae56e68630e9faee8`、
  変更せず保持）。Codex範囲レビューv1の判定は`reported_unverified`
  （SR-P1-001／002、SR-P2-003／004）。

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: Work 7A第2項の前駆slice（read-only GitによるRepository Binding／
           Source Snapshot／Change Setの捕捉と、checkout移動後の照合）
```

## 2. Human裁定（分割案1）の固定

Humanは2026-08-09、範囲レビューv1のSR-P2-003／004に対し次を裁定した。

1. 今回は**read-only GitによるRepository Binding／Source Snapshot／Change Setの捕捉と
   checkout移動後照合**を前駆sliceとして実施する。
2. **Project Bindingの耐久保存・復元とVerification Runは後続sliceへ分ける**。
3. **今回のGREENだけでWork 7A第2項のcheckboxを完了にしない**。
4. 次のTODO projectionもWork 7A第2項内の後続sliceを指す。
5. riskは`high`のまま維持する。

## 3. risk

- 提案・確定とも`high`（維持）。source identityの合否を決める守り役のcodeであり、
  誤った合格が黙って現れる。本文書のcommit後に停止し、Codexの再範囲レビューと
  Humanの再開承認までREDを開始しない。

## 4. 開始状態

- branch：`main`
- base commit：`3970e1ebd2e8cb9346f9169091eff2986493468c`（範囲レビューv1のrecord commit）
- 開始時worktree：clean（機械確認済み）

## 5. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 現在位置 | `TODO_NEXT_SESSION.md` | `19fd2246f87eeca4bbbcc8287d7a9400482240bee0d6455a1949a69aed842b15` |
| Work 7A checklist（第2項） | `docs/development/2026-08-03-initial-development-checklist.md` | `496a028e22c5f07ce54b670cdc6a6425d4e45252e5f5841cfc1cb620f46c3a1c` |
| Plan（Work 7A節） | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| 用語集 | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` |
| **Source Identity／Stale Candidate（承認対象）** | `records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json` | `e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc` |
| **同 Human承認Decision** | `records/development/2026-08-03-work-3-source-identity-stale-decision.json` | `1eba4807e9b1e5d5ff4fa38e8617e768c27cfe02c553572d91c86cd67366bae9` |
| **同 Completion Evidence** | `records/development/2026-08-03-work-3-source-identity-stale-completion-evidence-v1.md` | `e0c450b3ec7758f46a9056620513bfa023e8ca8dc8ad78e2e4eb1c65871edb06` |
| **Identity timing memo** | `docs/design/2026-08-03-source-change-verification-identity-timing-memo.md` | `08f973be1f4b0134f4a6a48af98fcbad4948bae890178fd8de6ce98d68e8235a` |
| 第1項 独立レビューEvidence | `records/development/2026-08-09-work7a-four-root-separation-independent-review-evidence-v1.md` | `5418bc5839cd01cf8f6b99088c33108fb83fb366fa7a49ff773959e556fab1ec` |
| Layout v3固定record | `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json` | `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38` |
| Layout v3承認Decision | `records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json` | `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275` |
| deployment／Project Artifact境界Decision | `records/development/2026-08-04-deployment-project-artifact-boundary-decision.json` | `237dd1d0d40304240f0d8376713509c34364aaa6369d3161df3d3be2cc623c1b` |
| Layout実装（再利用のみ） | `tools/layout/baseline.py` | `6d00c3053da820cd694a0c4b47d5e5f1b632f00d83e81691f99060626bc94cb7` |
| Work 5A Snapshot実装（変更せず。制約の参照のみ） | `tools/task_contract/execution.py` | `32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0` |
| record identity共通規則（変更せず） | `tools/task_contract/identity.py` | `bbbce848e3beb50301c2ef4e242a75daf64968a0d5c1f2f733751ac2a75a5c42` |
| 第1項実装（再利用のみ） | `tools/deployment/local_integrated_roots.py` | `31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149` |
| Layout既存Test（回帰対象） | `tests/test_layout_baseline.py` | `cdefaa57d8a41d59ac5275d55bd3498682f76bdd901eaf9efc31692883143ec0` |
| 第1項Test（回帰対象） | `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| 本mode手順書 | `docs/development/role-neutral-pilot-review-collaboration.md` | `856f5508787af653ecc2227a7f6376754963fdc42d61a1e98c577a01875af9ba` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `a3c6b608d243dd07ab5c9a1d9726c84e6ce71c498b3f134b6bfff2d5a7adbf37` |
| 先行scope v1（変更せず保持） | `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v1.md` | `ae40db7fdb4675f581fa516c1eaf9ec33cb36b1f83b55a1ae56e68630e9faee8` |
| 範囲レビューv1結果 | `records/session-handoffs/2026-08-09-codex-scope-review-work7a-checkout-relocation-v1.md` | `76d4084194da1d412a30126c4d1813bfd5e0c958833468650cebf6ecaf93c590` |

## 6. Project BindingとRepository Bindingの区別（SR-P1-001）

- **Project Binding**（Layout v3・用語集）：project IDと特定checkoutまたは配置を結ぶ記録。
  storage shapeは`state_root/projects/<project_id>/bindings/<binding_id>.json`で、
  binding directoryは`deferred_until_concurrent_checkout_need`。**本sliceでは耐久保存・
  復元を扱わず、後続sliceへ分ける（Human裁定2）**。`tools/layout/baseline.py`の
  `ProjectBinding`と検証APIは変更しない。
- **Repository Binding**（Work 3承認authority）：SCM非依存のsource identity。
  identity fieldsは`project_id`、`repository_id`、`binding_id`、`scm_kind`、
  `repository_root`、`checkout_or_worktree`。**本sliceの捕捉対象はこちら**であり、
  同じcommitを共有する別checkout／worktreeでも異なるbinding identityを持ち、
  branch名とfilesystem pathを唯一のdurable identityとして受理しない。
- 両者の関係：Repository BindingはSource Snapshot／Change Setが参照するsource側の
  identityであり、Project Bindingの耐久保存が後続sliceで実装される際に
  `repository_id`・`checkout_or_worktree`の対応を裁定する。この対応の裁定は本sliceに
  含めない。

## 7. 今回の最小E2E（前駆slice）

新module `tools/deployment/checkout_relocation.py`（新規、namespace package、
`__init__.py`なし、4スペースindent）に次の公開APIを作る。

1. **捕捉**：実Git checkoutから、read-only Git観測だけで次を生成する。
   - Repository Binding値：`project_id`（Project Manifestから）、`repository_id`
     （HEAD履歴のroot commit群から決定的に導出。複数rootは辞書順連結のSHA-256。
     導出規則の妥当性は再範囲レビューの確認対象）、`binding_id`（repository_id＋
     checkout_or_worktree等から決定的に導出し、checkoutごとに異なる）、
     `scm_kind`（`git`固定）、`repository_root`（canonical path。durable identityには
     使わない）、`checkout_or_worktree`（`git rev-parse --git-dir`／`--git-common-dir`の
     関係から導出したcheckout／worktree識別）。
   - Source Snapshot値：`repository_binding_id`、`base_commit`・`head_commit`
     （実Gitのrev解決で存在検証）、`index_state`・`tracked_changes`（staged／dirtyを
     区別して機械取得）、`included_untracked_files`（対象untrackedの明示列挙）、
     `content_manifest_digest`（対象fileのpathとSHA-256の正規化manifest）、
     `dependency_lock_identity`（本sliceでは該当なしを明示表現）、`capture_time`、
     `exclusion_rules_and_reasons`（除外規則と理由の明示）。
   - Change Set値：`base_snapshot_id`・`candidate_snapshot_id`、実Git deltaから
     **add／modify／delete／renameを区別**した項目、`changed_files_and_symbols`
     （file単位まで。symbol単位は明示defer）、`work_item_id`・`task_contract_id`
     （呼出し側指定）、`change_semantics`（呼出し側指定）、
     `merge_split_supersedes_relations`（本sliceでは空を明示表現）。
2. **checkout移動後の照合**：checkoutのdirectory移動、または同一repositoryの
   別checkout（clone）・worktreeに対して、
   - `repository_id`・`project_id`の保持を照合し、新しい`binding_id`
     （異なるcheckout identity）のRepository Binding値を導出する。
   - 捕捉済みSource Snapshot／Change Setを現状態と照合する（commit存在、
     manifest digest、dirty／index一致、untracked網羅）。
   - Manifestは書き換えない。照合・導出は何も作成・変更しない。
3. **production APIはread-only Gitのみ**：objects・refs・index・worktreeを変更しない
   読み取り専用subcommand（`rev-parse`、`rev-list`、`status --porcelain
   --no-optional-locks`、`diff --name-status`、`ls-files`等）に限定する。
   `init`・`add`・`commit`・`checkout`・`worktree add`等の変更操作をproduction API
   から呼ばない。
4. **Test fixtureの分離**：Acceptance Testに限り、`tmp_path`内での`git init`、
   `git add`、`git commit`、`git worktree add`、clone等のfixture構築を許可する。
   fixture構築はTest側helperだけで行い、production module経由では行わない。
   実ホーム・既存repositoryへはaccessしない。
5. 失敗・不一致・逸脱は型付き例外と安定stop codeでfail-closedに拒否し、例外連鎖・
   表面文言にhost path・未検査内容を残さない（第1項の例外連鎖修正の契約を踏襲）。

## 8. 受入条件

新規`tests/test_work7a_checkout_relocation.py`。`tmp_path`と`monkeypatch`の合成fixture
のみ。公開APIの入出力とfilesystem事後状態をoracleにする。

正例：

1. 実Git checkoutからの捕捉で、Repository Bindingが承認済みidentity fields 6種を持ち、
   Source Snapshotの`base`・`HEAD`・`index_state`・`tracked_changes`（staged／dirty
   区別）・`included_untracked_files`が実Git状態と一致する。
2. clean・同一状態での再捕捉は`capture_time`を除き同じnormalized identityを生む
   （決定性）。
3. 同じcommitを共有するclone（別checkout）とworktreeが、同一`repository_id`・
   同一`project_id`のまま**異なる`binding_id`**を持つ。
4. checkout移動後の再解決で`repository_id`・`project_id`が保持され、新`binding_id`が
   導出され、移動前Snapshotとの照合（同一HEAD・clean）が成立する。
5. add・modify・delete・renameを1つずつ含む実Git deltaから、Change Setが4種を
   区別して導出され、実際の変更集合と一致する。

負例：

6. 実repositoryに存在しない`base_commit`／`head_commit`は拒否する（範囲レビューv1の
   独立反証の封じ込め）。
7. project内symlinkがproject外を指す場合、resolve後pathの照合で拒否し、外部内容を
   Snapshotへ取り込まない。
8. 対象untracked fileがmanifestから欠落した状態を照合失敗にする（silent除外禁止）。
9. 記録した`index_state`／dirty状態と実状態の不一致を照合失敗にする。
10. Project Manifest欠落・`project_id`改変後の照合・再bindを拒否する。
11. branch名とfilesystem pathだけではidentityを認めない（branch改名・path移動後も
    `repository_id`は不変で、identity判定にbranch名を使わない）。

境界例：

12. clean・同一HEADのclone間で`content_manifest_digest`が一致する。
13. 捕捉record（Binding／Snapshot／Change Set値）のcontent digest改竄を照合で拒否する。

## 9. 変更可能pathとschema境界

変更可能path：

- `tests/test_work7a_checkout_relocation.py`（新規）
- `tools/deployment/checkout_relocation.py`（新規）
- `records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md`（新規）
- `records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json`（新規）
- `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-review-request-v1.md`（新規、実装完了後）

schema境界：

- 捕捉record（Repository Binding／Source Snapshot／Change Set）は**永続保存しない
  in-memory値**とし、fieldsはWork 3承認authorityに従う。digestは既存
  `tools.common.digests.canonical_content_digest`を再利用する。
- `tools/task_contract/identity.py`の`RECORD_KINDS`・`STOP_CODES`・既存schemaへの
  追加・変更はしない。既存`read_source_snapshot`とその利用元も変更しない
  （Work 5Aの契約は本sliceの対象外のまま）。
- 新しい永続record kind・Layout schema・Manifest schema・外部依存を作らない。
  値schemaの正式record化は耐久Binding後続sliceの範囲とする。

## 10. 禁止事項

- `tools/layout/baseline.py`、`tools/task_contract/`配下、
  `tools/deployment/local_integrated_roots.py`を変更しない。
- production APIからGitの変更操作を行わない（read-only限定）。fixture構築のGit操作は
  Test内・`tmp_path`内に限定する。
- Project Manifestの書換えでproject移動・複数checkoutを表現しない。
- Bindingの耐久保存・binding directory新設・Verification Run復元を実装しない
  （後続slice。§12）。
- 実ホーム・既存利用者data・既存repositoryへaccessしない。
- TODO・checklist・Plan・Decision・既存Evidence・scope v1を変更しない。
- push、tag、PR、amend、rebase、reset、履歴書換え、`git add -A`／`git add .`を
  行わない（このGit規律はrepository本体への操作であり、fixture内のtmp repositoryには
  適用されない）。

## 11. 停止条件

1. base、commit列、worktree、固定入力Digestが不一致。
2. §9以外のpath、特に固定入力実装の変更が必要。
3. `RECORD_KINDS`追加、新永続schema、Layout authority変更、binding directory新設が必要。
4. `repository_id`・`checkout_or_worktree`の導出規則が承認authorityと矛盾すると判明し、
   意味的裁定が必要。
5. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
6. targeted、関連回帰、公式全Test、`git diff --check`、receipt、Digest照合のいずれかが
   不合格。
7. 実データaccess、Human境界の変更が必要。

## 12. 後続sliceと未完了維持（SR-P2-003／004のHuman裁定反映）

- **耐久Binding保存・復元slice**（後続）：consumer＝Layout v3のbinding storage shape
  （`state_root/projects/<project_id>/bindings/<binding_id>.json`）を使うProject Binding
  永続化と、別checkoutからの復元。開始条件＝本sliceの`verified`＋Human着手指示。
  `concurrent_checkout_need`充足の意味的裁定はその開始時にHumanが行う。
- **Verification Run復元slice**（後続）：consumer＝Work 3承認のtarget consistency gates
  （test／review／decision／commit）が要求するVerification Run binding。開始条件＝
  耐久Binding sliceの後、Human着手指示。
- **未完了維持**：本sliceの`verified`ではWork 7A第2項checkboxを完了にしない。
  Closer（Codex）の完了projectionは、checkboxを開けたまま、TODO「次の一作業」を
  上記後続sliceへ向ける。

## 13. Test・validator・独立oracle

- targeted：`.venv/bin/python3 -m pytest tests/test_work7a_checkout_relocation.py`（単独）
- 関連回帰：`tests/test_layout_baseline.py`、
  `tests/test_work7a_local_integrated_root_separation.py`、
  `tests/test_first_review_task_contract_e2e.py`
- 公式全Test：`.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json`
- Reviewer向け独立oracle：受入条件をWork 3承認authority（identity fields・stale
  trigger・acceptance）から独立導出し、`high`のためPilotのfixtureに無い反証を最低1件
  機械実行する。

## 14. 予定するcommit境界

1. **SCOPE v2**（本commit）：本文書のみ。commit後に停止し、再範囲レビューとHuman
   再開承認を待つ。
2. **RED**：Testのみ。単独実行で今回の未実装だけを理由とする失敗とexit code `1`を
   確認してからcommit。RED実行結果はGREEN Evidenceへ記録する。
3. **GREEN**：実装・GREEN Evidence・公式receiptのみ。Testは変更しない（要求誤解等は
   停止しHuman承認後に理由を記録して訂正）。
4. **review request**：依頼書のみ。各handoff commit前に
   `git check-ignore --no-index <path>`を単独実行し、exit `1`のみ続行する。

各commit前に`git diff --check`を実行し、明示pathだけをstageする。
