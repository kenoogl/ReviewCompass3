# Work 7A第2項 checkout relocation 範囲レビュー結果 v2

- review date：2026-08-09
- Pilot：Claude
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- risk：`high`
- verdict：`reported_unverified`
- execution state：`correctly_stopped_before_RED`

## 1. 対象

- scope：`records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md`
- scope SHA-256：`f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`
- SCOPE commit：`4990ba64c7035d06fa77e1e3a68fb5a8d36a59f6`
- base：`3970e1ebd2e8cb9346f9169091eff2986493468c`
- branch：`main`

SCOPE commitは対象文書1件だけを追加し、parentは申告baseと一致する。review開始時worktreeはcleanで、
scope pathと本review result予定pathの`git check-ignore --no-index`はともにexit `1`だった。固定入力22件の
SHA-256は全件再計算値と一致し、`TODO_NEXT_SESSION.md`の統合validatorも合格した。

## 2. 範囲レビューv1 FindingsとHuman裁定の反映

| finding／裁定 | v2の反映 | 判定 |
| --- | --- | --- |
| SR-P1-001 authority欠落、Binding混同 | Work 3 authority 4件を追加し、Project BindingとRepository Binding、必要fieldを分離 | 一部解消。新しいidentity導出規則とSnapshot束縛に残件 |
| SR-P1-002 directory copyと既存APIによる偽合格 | 実Gitのread-only観測、無効commit、symlink、untracked、dirty／index、add／modify／delete／renameを固定 | 一部解消。Git観測commandと捕捉対象集合に残件 |
| SR-P2-003 耐久Binding境界 | 前駆sliceと後続耐久Binding sliceへ分割し、第2項checkboxを未完了維持 | 解消 |
| SR-P2-004 Verification Run除外 | Work 7A第2項内の後続slice、consumer、開始条件を固定し、第2項checkboxを未完了維持 | 解消 |
| Human裁定「分割案1」 | read-only捕捉を前駆slice、耐久BindingとVerification Runを後続、TODOを後続へ向ける | 反映済み |

scope v2はHuman裁定の対象を拡張せず、`high`、再範囲レビュー、Human再開承認の境界を維持している。

## 3. 上流から独立導出した受入境界

Work 3承認authorityは次を要求する。

- Repository Bindingは安定したrepositoryとcheckout／worktreeの対応を表し、別checkoutは同じcommitを共有しても
  異なるbinding identityを持つ。branch名またはfilesystem pathだけをdurable identityにしない。
- Source Snapshotはbase、HEAD、index、tracked、staged、対象untracked、manifest、dependency、capture、
  exclusionを持ち、必要fileの欠落、dirty差、Binding stale、manifestまたは除外規則の非再現を拒否する。
- Change Setは固定したbase Snapshotとcandidate Snapshotから導出し、add、modify、delete、renameを区別して、
  Work Item、Task Contract、change semanticsへ束縛する。
- read-only local Git adapterはidentityを取得するが、accepted stateやHuman Decisionを所有しない。

Work 7AはこれらとVerification Runの別checkoutでの復元・照合を一つの項目としている。Human裁定
「分割案1」は実装順を前駆sliceと後続sliceへ分けるが、このauthorityを変更せず、第2項を未完了に保つ。

## 4. Findings

### SR2-P1-001：root commit集合は安定した`repository_id`にならない

scope §7は、HEADから到達するroot commit群を辞書順連結してSHA-256化し、`repository_id`を導出する。
この規則はWork 3 authorityに無く、repository identityではなく現在到達可能な履歴shapeへ依存する。

独立反証では、一つのGit repository内で最初のroot commitを捕捉した後、unrelated historyを同じrepositoryへ
mergeした。repositoryとcheckoutを変更していないにもかかわらず、root集合が1件から2件へ変わり、提案規則の
SHA-256も`7c3cd152...`から`b21355a6...`へ変化した。逆に、cloneまたはforkはroot集合を共有できるため、
「同じsource lineage」と「同じrepository」の意味も区別できない。

影響：同じrepositoryを別repositoryとしてstaleにする一方、異なるrepositoryを同一と扱う可能性があり、
Repository Binding、Snapshot、Change Setの全下流identityへ誤ったstaleまたは偽の再利用を伝播する。
scope自身の停止条件4に該当する。`repository_id`を安定した明示identityにするか、lineage identityとして
別概念にするかをHumanが裁定し、scope v3で導出・移行・不一致条件を固定する必要がある。

### SR2-P1-002：base／candidate Snapshotとmanifest対象集合が固定されていない

scope §7はSource Snapshot値を一つだけ定義する一方、Change Setには`base_snapshot_id`と
`candidate_snapshot_id`を持たせる。Work 3 authorityは、固定した二つのSnapshotからChange Setを導出し、
同じ二つから同じnormalized change identityを得ることを要求する。scopeには、base tree用Snapshotと
candidate worktree用Snapshotをそれぞれ生成してDigestを固定し、Change Setの両refをその値へ照合する受入がない。

また、`included_untracked_files`を「対象untrackedの明示列挙」とするが、何を対象とし、何をどの固定規則と
理由で除外するかを機械導出するsource universeがない。負例8の「対象untracked fileが欠落」は、対象集合を
呼出し側が狭めれば成立しない循環oracleになる。

影響：任意のSnapshot ID、または必要fileを除外したmanifestでも、自己整合したChange Setとして合格できる。
base／candidate各Snapshotの完全な値とcontent digest、Change Set refの一致、tracked・untracked・ignoredの
捕捉／除外規則、除外理由の再現をscope v3の受入へ固定する必要がある。`capture_time`を除く
normalized identityと、`canonical_content_digest`が全fieldを含むrecord digestの区別も同時に明示する。

### SR2-P2-003：read-only Git commandとrename判定が再現可能な契約になっていない

scope §7.3の例`git status --porcelain --no-optional-locks`をそのまま単独実行すると、
`unknown option 'no-optional-locks'`、exit `129`となった。`--no-optional-locks`は`git`のglobal optionであり、
subcommandの後ろには置けない。

加えて、path出力のNUL区切り、external diff無効化、untracked／ignoredの扱い、rename検出の有無とthreshold、
利用者Git configからの隔離が固定されていない。特にrenameはheuristicと設定によりadd／deleteへ変わり得るため、
scope §8の決定性と4種区別を同時には保証できない。

影響：特殊文字を含むpath、利用者config、rename類似度により、同じsourceから異なるSnapshot／Change Setを作るか、
必要fileを誤解析する可能性がある。scope v3で正しいglobal option順、NUL区切りのmachine format、config隔離、
rename規則を固定し、対応する境界fixtureを追加する必要がある。

## 5. 変更範囲とHuman境界

- RED、GREEN、実装module、Acceptance Test：未作成
- 固定入力実装、TODO、checklist、Plan、Decision、既存Evidence：未変更
- push、外部送信、不可逆操作：未実施
- Pilotは`high` scope review境界で正しく停止している

Human裁定「分割案1」とrisk境界は維持されている。ただし、SR2-P1-001はidentityの意味的裁定、
SR2-P1-002〜003はAcceptance真偽と必須Provenanceに影響するため、scope v2でのRED再開を承認できない。

## 6. 独立確認

- `git diff-tree --no-commit-id --name-status -r 4990ba6...`：scope v2 1件だけ
- `git diff --check 3970e1e... 4990ba6...`：exit `0`
- scope v2固定入力SHA-256：22／22一致
- `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`：exit `0`、findings `[]`
- scope v2／review result v2の`git check-ignore --no-index`：ともにexit `1`
- root commit集合によるrepository ID反証：同一repository内でroot 1件から2件となり、導出SHA-256が変化
- `git status --porcelain --no-optional-locks`反証：exit `129`

## 7. 次

`reported_unverified`。REDは開始しない。HumanがSR2-P1-001のrepository identity意味を裁定し、Pilotが
SR2-P1-002〜003を含むscope v3を新規commitして停止した後、Codexが再範囲レビューする。
