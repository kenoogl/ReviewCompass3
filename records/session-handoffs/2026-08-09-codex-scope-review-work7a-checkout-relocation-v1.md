# Work 7A第2項 checkout relocation 範囲レビュー結果 v1

- review date：2026-08-09
- Pilot：Claude
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- risk：`high`
- verdict：`reported_unverified`
- execution state：`correctly_stopped_before_RED`

## 1. 対象

- scope：`records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v1.md`
- scope SHA-256：`ae40db7fdb4675f581fa516c1eaf9ec33cb36b1f83b55a1ae56e68630e9faee8`
- SCOPE commit：`47217cbdd79d7636d325b258495a2c5281700d43`
- base：`932d24697d4ee2f116b53a1bb4557527a2bf0023`
- branch：`main`

SCOPE commitは対象文書1件だけを追加し、parentは申告baseと一致する。review開始時worktreeはcleanで、
scope pathの`git check-ignore --no-index`はexit `1`だった。scopeに列挙された固定入力16件のSHA-256は
全件再計算値と一致し、`TODO_NEXT_SESSION.md`の統合validatorも合格した。

## 2. 上流から独立導出した受入境界

PilotのTest案を受入oracleにせず、次から独立に導出した。

- `docs/development/2026-08-03-initial-development-checklist.md` §11 Work 7A第2項
- `docs/current/reviewcompass3-plan-current.md` Work 7A
- `records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json`
- `records/development/2026-08-03-work-3-source-identity-stale-decision.json`
- `records/development/2026-08-03-work-3-source-identity-stale-completion-evidence-v1.md`
- `docs/design/2026-08-03-source-change-verification-identity-timing-memo.md`
- `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`
- `records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json`

Human承認済みWork 3 Decisionは、Repository Binding、Source Snapshot、Change Set、Verification Runの
identity、stale、復旧、対象一致を有効なauthorityとして固定している。最初のlocal scopeには、read-only
local Gitからrepository、base、HEAD、index、tracked change、対象untracked fileを取得することが含まれる。
Repository Bindingはrepository ID、SCM kind、checkout／worktree identityを持ち、異なるcheckoutは同じ
commitを共有しても異なるbinding identityを持つ。Source Snapshotはdirty、staged、untracked、除外規則を
含み、Change Setは固定base／candidate Snapshotからadd、modify、delete、renameを区別して導出する。

Plan Work 7AはRepository Binding、Source Snapshot、Change Set、Verification Runを別checkoutでも復元・
照合することを一つの境界としている。Layout v3はProject Bindingをproject外stateへ置くshapeと、
`binding_directory: deferred_until_concurrent_checkout_need`を固定している。

## 3. Findings

### SR-P1-001：承認済みSource Identity／Stale authorityが固定入力から欠落

scope §4には、Human承認済みの次のauthorityが含まれていない。

- Candidate：SHA-256 `e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc`
- Decision：SHA-256 `1eba4807e9b1e5d5ff4fa38e8617e768c27cfe02c553572d91c86cd67366bae9`
- Completion Evidence：SHA-256 `e0c450b3ec7758f46a9056620513bfa023e8ca8dc8ad78e2e4eb1c65871edb06`
- Identity timing memo：SHA-256 `08f973be1f4b0134f4a6a48af98fcbad4948bae890178fd8de6ce98d68e8235a`

scopeはLayoutのProject BindingをPlanのRepository Bindingとして扱うが、承認済みRepository Bindingの
`repository_id`、`scm_kind`、checkout／worktree identityを受入条件に持たない。新checkoutで
`binding_id`が変わることも明示していない。Source SnapshotとChange Setについても承認済みidentity field、
stale trigger、add／modify／delete／renameの区別が受入条件から抜けている。

影響：現scopeがGREENでも、上流で承認されたsource identity境界を満たしたとは判定できない。固定入力を
追加し、Project BindingとRepository Bindingの関係、必要field、staleと復旧条件をscope v2で裁定する必要が
ある。

### SR-P1-002：directory copyと既存APIだけで偽のcheckout／Change Setを合格できる

`tools/task_contract/execution.py::read_source_snapshot`はGitを読まず、呼出し側から渡された
`base_commit`、`head_commit`を検証せず保存し、`target_paths`をそのまま`changed_paths`にする。したがって
scope §6〜§7のdirectory move／copyとfile digest照合だけでは、repository、commit、index、dirty、staged、
untracked、実変更集合を確認しないまま「別checkoutのChange Set復元」をGREENにできる。

独立反証では、`base_commit="not-a-commit"`、`head_commit="also-not-a-commit"`を渡してもexit `0`で
Source Snapshotが生成され、両値と`changed_paths`がそのまま受理された。

さらに`safe_relative_path`は字句上の絶対pathと`..`だけを拒否する。project内symlinkからproject外fileを
参照するfixtureを`read_source_snapshot`へ渡すと、exit `0`で外部fileをSnapshotへ取り込んだ。scopeの
「path逸脱拒否」とhost path／未検査内容非漏洩は、絶対path・`..`のTestだけでは成立しない。

影響：実checkout identityとChange Setを取得するread-only Git境界、またはそれを満たす既存実装の固定入力が
必要である。symlink、base／HEAD不存在、dirty／index／untracked不一致、add／delete／renameを負例へ追加し、
resolve後のpathがproject root内であることを照合しなければならない。これに必要なAPI、schemaまたは変更pathが
現scope外なら、scope自身の停止条件2・3に従ってv2作成前にHuman判断が必要である。

### SR-P2-003：一時的な値の受渡しでは「復元」とbinding storage境界を確認できない

scope §5はBindingを呼出し側が保持する値として扱い、耐久保存を禁止している。しかしLayout v3には
`state_root/projects/<project_id>/bindings/<binding_id>.json`というProject Binding storage shapeがあり、
binding directoryのdefer条件は`concurrent_checkout_need`までである。本作業は別checkout／複数checkoutを
対象にするため、この条件を満たしたかの意味的裁定が必要である。

影響：旧BindingとSnapshotを同一processの引数で渡して新Bindingを作るだけでは、checkout移動後の復元可能性を
実証しない。Humanは、(a) 本sliceで耐久Bindingからの復元まで扱う、または(b) 本sliceをread-onlyな前駆sliceと
してWork 7A第2項のcheckboxを閉じず、耐久復元のconsumerと着手条件を固定する、のどちらかを選ぶ必要がある。

### SR-P2-004：Verification Runの除外根拠がTODOだけで、上流との競合が未裁定

scope §5は、TODOに記載がないことを理由にVerification Runを範囲外としている。しかしTODOはstateまたは
完了Evidenceのauthorityではない。Plan Work 7AとHuman承認済みWork 3 Decisionは、Verification Runを
Snapshot／Change Setと同じ対象一致境界に含め、Test、review、Decision、commit gateで必須bindingとしている。

影響：Verification Runを今回含めるか、後続のどのWork 7A itemへ移管して第2項を未完了に保つかをHumanが
裁定する必要がある。TODOの省略だけをPlan境界の変更根拠にしてはならない。

## 4. 変更範囲とHuman境界

- RED、GREEN、実装module、Acceptance Test：未作成
- 固定入力実装、TODO、checklist、Plan、Decision、既存Evidence：未変更
- push、外部送信、不可逆操作：未実施
- Pilotは`high` scope review境界で正しく停止している

Human境界は維持されている。ただし、SR-P1-001〜002はAcceptance真偽と必須Provenanceに影響し、
SR-P2-003〜004はscopeとauthorityの意味的裁定を要するため、現scopeでのRED再開を承認できない。

## 5. 必要な修復

推奨routeはscope v2の作成である。

1. 承認済みSource Identity／Stale Candidate、Decision、Completion Evidenceとidentity timing memoを固定入力へ
   追加する。
2. Project BindingとRepository Bindingを区別し、別checkoutで変わるidentity、保持するidentity、stale triggerを
   受入条件へ固定する。
3. 実Git checkout／worktreeまたは同等のread-only Git fixtureからrepository、base、HEAD、index、dirty、
   tracked／untracked、Change Setを機械取得して照合するE2Eへ改める。
4. symlink逸脱、無効commit、omitted untracked、dirty／index不一致、add／delete／renameを負例へ追加する。
5. Bindingの耐久復元とVerification Runについて、今回含めるか、後続consumerへ移して第2項を未完了に保つかを
   Humanが裁定し、そのDecisionをscope v2へ固定する。
6. 必要な変更pathとschema境界をv2で再固定し、Reviewerの再範囲レビュー後にだけHumanがRED再開を承認する。

## 6. 独立確認

- `git diff-tree --no-commit-id --name-status -r 47217cb...`：scope 1件だけ
- `git diff --check 932d246... 47217cb...`：exit `0`
- `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`：exit `0`、findings `[]`
- 固定入力16件のSHA-256再計算：16／16一致
- scope handoff `git check-ignore --no-index`：exit `1`
- `read_source_snapshot`無効commit／symlink反証：exit `0`、両方を受理

## 7. 次

`reported_unverified`。REDは開始しない。HumanがSR-P2-003／004を裁定し、Pilotがscope v2を新規commitして
停止した後、Codexが再範囲レビューする。
