---
lifecycle: active
normative_status: operational-checklist
document_role: initial-development-execution-checklist
activated_at: 2026-08-03
authority_order:
  - path: docs/current/reviewcompass3-intent-current.md
    sha256: 1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6
  - path: docs/current/reviewcompass3-glossary-current.md
    sha256: f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa
  - path: docs/current/reviewcompass3-plan-current.md
    sha256: 1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f
operational_policy:
  path: docs/development/2026-08-02-development-policy.md
  sha256: 08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c
policy_decision:
  path: records/development/development-policy-v5.json
  sha256: 88af550d5bc77406cd796e4c78efc20225134473d3d87251942854e6dc57fe98
related_design:
  - path: docs/design/2026-08-03-current-work-projection-memo.md
    sha256: 940bff56f749bebdff08698882ca92dbe8505cb4692ba864c8ee7b76b4f01595
  - path: docs/design/2026-08-03-self-application-improvement-routing-memo.md
    sha256: 0ee336ac2da20e78df00cc096eceb9dc4907a096835f7e579050072478b5d14f
  - path: docs/design/2026-08-03-execution-claim-verification-memo.md
    sha256: 32caf8ea2052b81001a77caa78ffcc3900574ab3bde59a63ee8e3ab8447ad542
---

# ReviewCompass3初期開発チェックリスト

## 1. 目的と使い方

本書は、ReviewCompass3の初期開発を、配置と記録のbootstrapから最小Task Contract、自己適用、
deployment、評価、releaseへ順番に進めるための当面の実行チェックリストである。2026-08-03の
Human指示により、後継判断があるまで開発作業は本書の未完了項目を確認して進める。

本書はIntent、Requirements、計画、Task Contract、Decision Record、Provenanceの正本を置き換えない。
checkboxは進行を見失わないための操作viewであり、完了のauthorityは各項目の固定Evidenceである。

### 運用規則

- 原則として上から順に進め、前工程の完了関門を満たす前に下流の製品実装を開始しない。
- 一度にactiveにする製品Work Itemは一件とし、条件付き並行Pilotまでは`single_active_leaf`を守る。
- checkboxを完了にする場合、同じ節の`Evidence`へ固定path、ID、Digest、Test RunまたはDecisionを記す。
- 会話、TODO、checklistまたは最終報告の「実施した」を完了根拠にせず、実施報告ClaimをEvidenceと
  観測した事後状態へ照合する。
- 既存artifactが項目を満たす場合は固定sourceと適合性を確認してEvidenceへ結び、同じ成果を作り直さない。
- 既完了項目がstaleになった場合、理由、影響範囲、旧Evidenceを残して再確認対象へ戻す。
- 手順変更、順序変更、scope変更は黙って行わず、理由とHuman判断を記録して本書を改定する。
- 自己適用中の問題、改善案、新機能案は、現行のPlan、Task Contract、Testまたは受入基準を
  先に変更せず、17節の改善候補として記録、分類、停止判定、routeする。
- 調査、文書、試作へ形式的red-greenを強制しない。振る舞いを変更するcodeはrisk-based test-firstで進める。
- 各節の対象外能力を、便利だからという理由で前倒ししない。

## 2. 毎sessionの開始・終了

現在位置プロジェクション（`current_work_projection`）が利用可能になるまでは、次を手作業で確認する。
利用可能になった後は生成結果を確認し、必要なauthorityまたはrelationの欠落だけを修復する。
本節はsessionごとに繰り返すtemplateであり、本ファイル上で一度だけ完了にせず、各Session Evidenceへ
実施結果を記録する。
ルートの`TODO_NEXT_SESSION.md`を人向けのsession更新・引き継ぎメモとして使う。TODOは現在位置の
authorityではなく、固定Plan、checklist、Evidence、Git、Testへの入口である。
新規作成または構造を復元する場合は、
`docs/development/templates/TODO_NEXT_SESSION.template.md`を使用する。
TODOには現行handoffだけを置き、過去内容を累積しない。Stage変更、長期中断、大きな計画改定など、
独立保持する価値がある場合だけ`records/session-handoffs/`へ不変snapshotを作る。通常のsession履歴は
Session EvidenceとGitへ委ねる。

### session開始

- [ ] 使用するIntent、用語集、計画のpathとDigestを確認した。
- [ ] Gitのbranch、HEAD、作業ツリー、対象Change Setを確認した。
- [ ] 現在のStage、Work、Task Contract、Work Itemを確認した。
- [ ] 直近の完了関門とEvidenceを確認した。
- [ ] blocker、dependency、cycle、Human判断待ち、staleを確認した。
- [ ] 次に実行可能な一作業を特定した。
- [ ] 今回の作業範囲と非目標を短く提示した。
- [ ] `TODO_NEXT_SESSION.md`の現行更新欄とauthorityの不一致がないことを確認した。
- [ ] TODOの必須欄が欠けている場合、`TODO_NEXT_SESSION.template.md`から構造を復元した。

### session終了

- [ ] 報告を実施、結果、判断、提案、未実施へ分け、後続状態を変える複合報告を原子的Claimへ分解した。
- [ ] 実施・結果・判断Claimをpath、diff、Digest、command結果、commit SHA、receiptまたはDecisionへ
      接続し、対象の事後状態を再確認した。
- [ ] EvidenceがないClaimを`reported_unverified`として未完了にし、checkboxまたは完了判断に使っていない。
- [ ] 報告と事後状態が競合する場合は`report_execution_mismatch`として進行を停止し、影響するTODO、
      checkbox、Verdict、projectionをstaleにした。
- [ ] 提案、予定、deferred、未実施作業を、実施済みの報告と分離した。
- [ ] Test、review、残余riskを記録した。
- [ ] 完了、継続、pause、blocked、stale、deferredのいずれかを明示した。
- [ ] 次に実行可能な一作業、必要なHuman判断、再開条件を記録した。
- [ ] 現在位置表示または手作業statusとauthorityの不一致がないことを確認した。
- [ ] `TODO_NEXT_SESSION.md`の先頭へ、現在地、実施内容、次作業、blocker、Human判断待ち、
      stale、Git／Test結果、Evidence linkを更新した。
- [ ] 最終stage前にTODOのGit欄をcommit安定形式へ更新し、
      `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`が合格した。
- [ ] 完了した作業単位から次作業へ移る前にwork unit transition preflightを実行し、
      `completed_work_unit_uncommitted`ならコミットまで移行を停止した。
- [ ] コミット後のGit確認はread-onlyで行い、自己SHA、固定ahead／behind、push済否の転記だけを目的とする
      追加コミットを作成していない。
- [ ] TODOへ過去sessionを累積せず、現行handoffを短時間で読める量に保った。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 3. Work 1：固定入力と開発入口

### 開始条件

- [x] 利用者から開発着手の指示がある。
- [x] 本チェックリストを当面の進行入口として確認している。

### 確認項目

- [x] Intent、統合用語集、現行計画の対象versionとDigestを固定した。
- [x] 既存baseline、前身Evidence、未コミット変更を列挙した。
- [x] 今回のsource universe、対象、非対象、confidentialityを定めた。
- [x] 初期scopeとDeferred Workを確認した。
- [x] 未承認事項、既知Finding、必要なHuman判断を列挙した。
- [x] Evidence Extraction ContractとConsumption Closureの最小運用を定めた。
- [x] 固定入力が変わった場合のstale化と再開入口を定めた。

### 完了関門

- [x] 固定入力、scope、非目標、未解決事項を一つのEvidenceから確認できる。
- [x] blockingなIntent／Requirement／Plan競合がない、または停止理由が明示されている。

`Evidence`：`RC3-WORK1-FIXED-INPUT-2026-08-03-V2`、
`records/development/2026-08-03-work-1-fixed-input-evidence-v2.md`、SHA-256
`7997b203935a9e53c56ed2556b4598773cd9d7b13c43079fcf8524b5e06bc9be`。
corrective snapshot commit `ee60e3b4baf74c60da949a9d04d793fb83a61e69`からmanifest 13件、
source catalog 10件、前身inventory 2件を再読込し、全件一致した。結果は`verified / completed`。
先行するblocked Evidence v1は
`records/development/2026-08-03-work-1-fixed-input-evidence.md`、SHA-256
`d07c5abdce7bc4b3322e7c6f973feb0e00d7218151dafe7013aff5d08148b879`として保持する。

## 4. Work 1A：Layout Baseline

### 確認項目

- [x] `CODE_ROOT`、`CONFIG_ROOT`、`PROJECT_ROOT`、`DATA_ROOT`、`STATE_ROOT`、`LOG_ROOT`、
      `CACHE_ROOT`、`SENSITIVE_ROOT`、`EVALUATION_ROOT`の意味と解決規則を固定した。
- [x] Git管理対象、project外data、機密data、生成物、cacheの境界を固定した。
- [x] Project ManifestとProject Bindingの最小構造を定めた。
- [x] stableとdevelopmentのroot、state、data、cross-write禁止を定めた。
- [x] 空配置fixtureを作り、別checkoutとproject移動後の相対参照を確認した。
- [x] 端末固有絶対pathが管理成果へ混入しないことを確認した。
- [x] 後続の配置変更を通常編集でなくmigrationとして扱う規則を定めた。

### 完了関門

- [x] Layout Baseline Recordと空配置Testが固定されている。
- [x] project移動、link解決、Manifest／Binding照合がgreenである。

`Evidence`：`RC3-WORK1A-LAYOUT-2026-08-03-V1`、
`records/development/2026-08-03-work-1a-layout-evidence-v1.md`、SHA-256
`5d54c7de759388ae81c1fefebcc50c817c0b38ae2bcdc65444f47aa48cc8e899`。
Layout一式はcommit `d3add9f2e6bc812bf512a36a24877e29879e9842`へ固定し、targeted
`7 passed`、全`419 passed`。結果は`verified / completed`。

2026-08-04 successor：Project Artifactを移動せずdeployment packageを交換する境界を追加したLayout Baseline
v2をHumanが承認した。現行authorityは
`records/development/2026-08-04-layout-baseline-v2-approval-decision.json`、SHA-256
`856345948af57bcfa373eb2766768d9c38078d7ba5fe65b0d76d68e452ceaa7e`。承認対象v2 candidateは
SHA-256 `4a086be730b3310cc6933826ab6dac751e36af0596c5a8b6a7e381357d956282`、公式全Testは
`500 passed in 2.56s`、fallback `false`。v1 recordとEvidenceは`historical_verified`として保持する。
本承認はWork 7A／7Bのdeployment lifecycle実装完了を意味しない。

ReviewCompass3自己適用projectのManifest v2 bootstrapは
`records/development/2026-08-04-project-manifest-v2-completion-evidence-v1.md`、SHA-256
`154d3f5d930b16c9974431568e9430d896f580d99e03c59efffb5fba878ec020`へ固定した。Project ID
`reviewcompass3`、workflow root、相対document link 5件、端末固有絶対path finding 0を確認し、公式全Testは
`501 passed in 2.24s`、fallback `false`。Project Bindingのdurable保存とdeployment lifecycleは未実施のまま。

2026-08-04 successor：project-first runtime rootを追加したLayout Baseline v3をHumanが承認した。
現行authorityは`records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json`、SHA-256
`793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275`である。
`~/.reviewcompass3/projects/<project-id>/<development|runtime>/`にprofileを物理分離し、必要なrootだけを
明示作成する。candidate内の`status: candidate`は履歴内容として保持する。既存v2 caller、data、migrationは
変更せず、Work 4Aのactual Source Snapshot保存を次作業とする。

## 5. Work 1B：Session Log Bootstrapと現在位置text表示

### Session Evidence

- [x] session ID、source identity、取得範囲、時刻、Digest、完全性を記録できる。
- [x] rawを`SENSITIVE_ROOT`、伏字化派生物・要約・索引を`DATA_ROOT`へ分離した。
- [x] confidentiality、access、retention、capture deadline、source availabilityを定めた。
- [x] `source_missing | source_expired | non_reconstructable`を正常な空記録と区別した。
- [x] rawから派生物を再生成し、Digestを照合するrestore fixtureを確認した。

### bootstrap現在位置プロジェクション

- [x] Work開始／完了、pause／resume、blocker発生／解消を記録できる。
- [x] Human判断要求／決定、upstream revision、stale／再検証を記録できる。
- [x] cancel／defer、session開始／終了を記録できる。
- [x] 固定入力から同じstructured projectionを決定的に生成できる。
- [x] 全体Stage／Work、active作業、TDD状態、次作業、blocker、Human判断待ち、staleをtext表示できる。
- [x] session開始用の短縮表示と、調査用の詳細表示を生成できる。
- [x] 入力identity、Digest、生成時刻、freshnessを表示できる。
- [x] 欠測または競合を推測で埋めず、不完全または不整合として詳細表示できる。
- [x] 手編集する`STATUS.md`、第二の状態台帳、WebUI、常駐serviceを作っていない。
- [x] 表示器だけのfailureとWorkflow authority欠落を区別できる。

### 完了関門

- [x] Work 2以降のsessionと主要状態変化を失わず記録できる。
- [x] 現在位置のtext表示をsession開始・終了で実際に使用できる。
- [x] bootstrap toolingを作成した場合、固定fixture、red確認、関連Test、全Testがgreenである。

`Evidence`：`RC3-WORK1B-RED-2026-08-03-V1`、
`records/development/2026-08-03-work-1b-red-evidence-v1.md`、SHA-256
`079277ae1f3f1c5277672d2ad24e4e1650983c0e0fc3eec5da4ee6f56d79604a`。
固定fixture 13 fileとAcceptance Test 7件を追加し、targeted `7 failed`、全Test
`419 passed, 7 failed`。失敗は全件bootstrap mapping module未実装による期待どおりのredである。
red時点ではWork 1Bを`active / red`とし、checkboxと完了関門を未完了のまま保持した。
Green Evidenceは`RC3-WORK1B-GREEN-2026-08-03-V1`、
`records/development/2026-08-03-work-1b-green-evidence-v1.md`、SHA-256
`fdaeeb439226c6e86b17b8aa33e0e11fbdc64512ccd3b2c3f9a14f0970e169b9`。
固定Testを変更せずtargeted `7 passed`、全`426 passed`。Work 1Bは`active / green`であり、durable
captureとsession開始／終了での実使用に関する項目・完了関門は未完了のまま保持する。
Durable capture red Evidenceは`RC3-WORK1B-DURABLE-RED-2026-08-03-V1`、
`records/development/2026-08-03-work-1b-durable-capture-red-evidence-v1.md`、SHA-256
`a25c7cfde5817ff35375b07087e740820a7080b67bec8b6921fac167eb5e862d`。
writer未実装を理由にtargeted `4 failed`、全Testは既存`426 passed`、新規red `4 failed`。現在の
durable capture Work Itemは`active / red`であり、既存green項目は維持し、保存関連項目は未完了とする。
Durable capture green Evidenceは`RC3-WORK1B-DURABLE-GREEN-2026-08-03-V1`、
`records/development/2026-08-03-work-1b-durable-capture-green-evidence-v1.md`、SHA-256
`7ab01e1a106c6d8cb2711f1b8bc4df150d34761d94c7d0f13f033332783f2f22`。
固定Testを変更せずdurable `4 passed`、bootstrap `7 passed`、全`430 passed`。Session Evidence関連項目を
完了Evidenceへ接続した。Work 1Bは`active / green`であり、実session利用の完了関門は未完了とする。
Session lifecycle E2E red Evidenceは`RC3-WORK1B-SESSION-E2E-RED-2026-08-03-V1`、
`records/development/2026-08-03-work-1b-session-e2e-red-evidence-v1.md`、SHA-256
`84cf75898883b73d4db996dbcdf465ada0a6a8b2375551c866d6a22a3e3429ab`。
orchestration API未実装を理由にtargeted `4 failed`、全Testは既存`430 passed`、新規red `4 failed`。
現在のE2E Work Itemは`active / red`であり、session lifecycleと表示failure分離の項目は未完了とする。
Session lifecycle E2E green Evidenceは`RC3-WORK1B-SESSION-E2E-GREEN-2026-08-03-V1`、
`records/development/2026-08-03-work-1b-session-e2e-green-evidence-v1.md`、SHA-256
`b3ec1686d6caeaba6f745a3ec355a24152e42572c77a451c06343d6ffa013e84`。
固定E2E Testを変更せずE2E `4 passed`、関連`15 passed`、全`434 passed`。session lifecycleと
display／authority failure分離を完了Evidenceへ接続した。Work 1Bは`active / green`であり、実sessionでの
表示利用に関する完了関門は未完了とする。
実使用で検出した完了後NEXT残留は改善候補`IC-WORK1B-COMPLETED-NEXT-001`へ固定し、Human Decision
`DEC-WORK1B-COMPLETED-NEXT-2026-08-03-V1`で選択肢1を採用した。回帰Testは修正前`2 failed`、修正後は
関連`17 passed`、全`436 passed`。修復GREEN Evidenceは
`records/development/2026-08-03-work-1b-completed-next-green-evidence-v1.md`、SHA-256
`03541809e7f57cdc80308ad7eb1ab6f2e4b20a7d487263eaa32219257d031afb`。
別の外部development rootでsession開始short表示、完了eventを含むdurable capture、保存後rawからの終了
detailed表示を実際に使用し、終了NEXTがHuman完了承認依頼へ更新された。raw、派生3 artifact、Session
Evidence、start／end receiptを独立再読込し、Digest一致を確認した。
Work 1B Completion Candidateは
`records/development/2026-08-03-work-1b-completion-candidate-v1.md`、SHA-256
`cb48778b36bf1d26673f753a91f97faf25c13a8d738d9193e4e23d9e4497d03d`。
技術的完了関門は`verified_completion_candidate`となり、Humanが2026-08-03T14:35:03+09:00にWork 1Bの
段完了を承認した。Decision正本は`records/development/2026-08-03-work-1b-completion-decision.json`、
SHA-256 `69b4f792e3ccf529af338bce08e46ec2dace77ba86b5e4df624ff4b399e63ac8`。
Work 1Bの結果は`verified / completed`であり、次の未完了工程はWork 2とする。

### Work 1B後続：機密の扱い（2026-08-08改定r1で追加）

Work 1Bが敷いた機密分離（rawは`SENSITIVE_ROOT`、外に出すのは伏字化派生物のみ）の運用を
完成させる残項目。順序と根拠は`DEC-CONFIDENTIALITY-WORK-ORDER-001`
（`records/development/2026-08-07-confidentiality-work-order-decision-v1.md`）。
①出口の設計は完結した：関門・dry-runを段階2まで実装し（`tools/egress/`、反証レビュー済み）、
外部API比較の中止により送信実装（段階4）は不要となった（`DEC-EGRESS-METHOD-CONCLUSION-001`）。
資産は保持し、必要が再発したときの再判断材料は固定済みである。

- [ ] 伏字化規則を設定へ登録し、保全経路から呼ぶ（実施順序2番目。実装済み規則の登録）。
- [ ] C（内部の未公開情報）とD（会話に混入した外部データ）の扱いを定義する（同3番目）。
- [ ] 既存の保全済みデータへの遡及適用を判断する（同4番目。着手はHuman判断）。

## 6. Work 2〜4：上流文書、Requirements、最初のslice設計

### Work 2：Intentと用語

- [x] Intent、利用者、非目標、Human／AI／機械のauthority境界をHuman判断候補として固定した。
- [x] 新しいdomain用語を統合用語集へ登録した。

`Evidence`：Work 2 Human判断候補は
`records/development/2026-08-03-work-2-intent-glossary-candidate-v1.md`、SHA-256
`bfec3b29cf8ebb5ffeedc349e39b2215922ebef8e4105a258e73279a7226a252`。
現行PlanのIntent／用語集参照とWork 1 corrective snapshotを再照合し、Intent必須8節、authority境界3件、
canonical token 109件、Work 2必須13語、旧語読み替え8件を確認した。必須語の欠落と重複は0で、
追加本文差分は不要だった。Intent、用語集、Plan本文は変更していない。
Work 2 Session Evidenceは`rc3-work2-operational-20260803-001`、SHA-256
`456c9071781d5bbcddadd6cb2fa181274ba1930e34c5903c18eb96066719e5c6`。判断対象Digestをeventへ固定し、
Work Item `paused`、Human判断1件、blocker／staleなしとして保存後Digestを再照合した。
post-write確認でcandidateの`generated_at`がWork 1完了承認時刻を誤って再利用していることを検出した。
改善候補は`records/development/2026-08-03-work-2-candidate-timestamp-improvement.md`、SHA-256
`6d0f4722a2aa926b638384ee58789be0fce6f4b617932c2c2a2c3d744c5357c5`。candidate修正により判断対象Digestと
保存済みeventが変わるため、Work 2を`pause_and_triage`し、上記2項目を未完了へ戻した。Intent、用語集、
Plan本文と監査結果は変更していない。metadata修復、再capture、promotion、Work 3進行はHuman判断待ちとする。
Humanは選択肢1を承認した。Decisionは
`records/development/2026-08-03-work-2-candidate-timestamp-decision.json`、SHA-256
`9dcc7570d80bde8711049c688e5f03ec4a607457a96179fd146c512c288f271a`。候補の生成時刻を検証可能なWork 2
session境界へ訂正し、旧Digest`2666511b...`をmetadataに保持した。再監査は同じ被覆で合格した。
修復Evidenceは`records/development/2026-08-03-work-2-candidate-timestamp-repair-evidence-v1.md`、SHA-256
`d1fb1e1f6f2ad0c794fdf36d74fa188ef068753a10f3e71c8428bf39a6c25ad0`。session `001`をsupersededとし、
session `002`で旧Digestのstale化、新Digestの再検証、新DigestへのHuman判断要求を保存した。session `002`
Evidence SHA-256は`9af96cd068b61a093b4f7068bfd7e553b3bdc475d3ba87f93771434700ae340a`で、保存後照合は
`verification: passed`だった。
Humanは選択肢1として訂正済みIntent／統合用語集候補を承認した。Approval Decision正本は
`records/development/2026-08-03-work-2-intent-glossary-approval.json`、SHA-256
`068ff06132dfcd24685d4a626d9107cf65b37456eebcd567dc72b9f6b27c7b78`。候補、Intent、用語集のDigestへ
承認を束縛し、現行Planは引き続きprovisionalとして扱う。promotion状態の変更によりWork 1固定入力Evidence
v2をstaleとし、`records/development/2026-08-03-work-1-fixed-input-evidence-v3.md`、SHA-256
`334f7aeee44f65ee953d13f1737d08e24c38a4b2356aff26e3f7d4accec60d8a`でsnapshot 13 artifact、承認対象2文書、
Plan参照を再照合した。内容Digestに変化はなく、Work 1の`verified / completed`は維持する。
完了状態はsession `rc3-work2-operational-20260803-003`へdurable captureし、Session Evidence SHA-256
`341911fda7e7ac25c210c389c1e8fd33d9bed0117d7eecfb13e91a12b1726cb3`、保存後照合
`verification: passed`を確認した。Work 2 Completion Evidenceは
`records/development/2026-08-03-work-2-completion-evidence-v1.md`、SHA-256
`8a5f42dbde5d3b79ae2b200746e46f441cf07219a8ff5836fbf749d6563442d2`。Work 2は
`verified / completed`であり、次の未完了工程はWork 3とする。

### Work 3：Requirements

- [x] 既存37要件と追加13要件の順逆被覆、owner、停止、復旧、受入、対象外を確認した。
- [x] source、Change Set、Test／CI／Build Artifactのidentityとstale規則を確認した。
- [x] Requirement本体、候補、Decision、Evidence、schemaの配置、命名、authority結線を固定した。
- [x] 承認済み配置へ最小schema、validator、fixture、既存37要件のlegacy binding inventoryを実装した。
- [x] 追加13 Requirementをdefinition／candidate形式へ構造化し、schema検証、Evidence、Human promotionへ接続した。
- [x] 必須非機能義務をVerification Profileへ接続した。
- [x] deferred候補を初期Requirementの暗黙依存にしていない。

`Evidence`：固定sourceと被覆baselineは
`records/development/2026-08-03-work-3-requirements-baseline-evidence-v1.md`、SHA-256
`7fdc24c8063292871761af3c888824f3e3c715689df3a3924c28c7856f9c5a20`。既存37要件と追加13要件の
計50 IDは現行Planと欠落・余剰0で一致し、既存37要件のowner、停止、復旧、受入、対象外、source traceと
追加13要件の同じ形状に欠測はなかった。既存Requirements専用Testは`59 passed`。ただし、既存37
Requirementを追加差分に対して`preserve | adapt | replace | defer`へ結ぶRequirement単位の37行matrixは
baseline時点では未固定だった。既存の37 Acceptance Test継承表はこの意味的被覆を代替しないため、
先頭項目を未完了のままcoverage matrix候補の作成と独立照合へ進めた。
37行のcoverage matrix候補は
`records/development/2026-08-03-work-3-requirements-coverage-candidate-v1.json`、SHA-256
`c529e1495a8ea5a84ac15ae651299a410f6aba627ee115b395a5940aa209cb7e`。分類は`preserve: 15`、
`adapt: 20`、`replace: 2`、`defer: 0`で、37 ID、owner、旧／後継testは既存sourceと全件一致し、
追加13 IDは全件1行以上から逆引きできた。独立監査と転記ミス1件の訂正Evidenceは
`records/development/2026-08-03-work-3-requirements-coverage-evidence-v1.md`、SHA-256
`fa4dc0818ff4666a940b8347ee44af39b7262f09386cf903e9775165c5e31508`。候補は
`verified / human_decision_pending`となった。
Humanは選択肢1として候補を承認した。Decisionは
`records/development/2026-08-03-work-3-requirements-coverage-decision.json`、SHA-256
`cb1c879e28b27fdec765fb9c37636ab59b6017e822b9e4315c33965a8823e54f`。完了Evidenceは
`records/development/2026-08-03-work-3-requirements-coverage-completion-evidence-v1.md`、SHA-256
`bcddaa3e5b4388adba958cc3198c2ac543b2977e8efdcb48c1d440f332023e61`。承認は37行matrixと先頭項目だけに
限定し、Requirements／Plan本文と残り3項目は変更していない。先頭項目は`verified / completed`、次の
未完了項目はsource、Change Set、Test／CI／Build Artifactのidentityとstale規則である。
5種類のidentityと5つの対象一致関門を構造化したHuman判断候補は
`records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json`、SHA-256
`e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc`。Repository Binding、Source Snapshot、
Change Set、Verification Run、Build Artifactへidentity、stale、復旧、受入、対象外を固定し、Test、review、
Decision、commit、releaseから必要なbindingを逆引きした。監査Evidenceは
`records/development/2026-08-03-work-3-source-identity-stale-evidence-v1.md`、SHA-256
`3d04943d0174c323d9b5f1feb605eb70ff3e4dc3a779e681bf179d810db16812`。entity 5件、gate 5件、固定source
6件、relation 7段階を監査し、欠落・未知参照・Digest不一致は0、`AUDIT_OK`だった。候補は
`verified / human_decision_pending`であり、Human承認前は2番目のcheckboxを未完了のまま維持する。
追加13 Requirementの構造化前に固定する配置・authority候補は
`records/development/2026-08-03-work-3-requirements-artifact-layout-candidate-v1.json`、SHA-256
`154a4f40487bc52537e87575d063f0c3e0e72b19fa13d2cdcee0e4fc0339e6ed`。人向けsource、構造化definition、
candidate manifest、Decision、Evidence、schema、authority bundleの7 classを分離し、pathだけでは正本に
ならない規則、ID／version／Digest結線、stale 5区分、既存37要件のlegacy bindingを定めた。監査Evidenceは
`records/development/2026-08-03-work-3-requirements-artifact-layout-evidence-v1.md`、SHA-256
`25c7a61e99f04b78ab2732ef70bf507ec161f859085238579f6d0fcb09285871`。artifact class 7件、固定source
10件、stale規則5件の欠落・重複・Digest不一致は0、`LAYOUT_AUTHORITY_AUDIT_OK`だった。Human承認前は
提案directoryを作成せず、配置・authority項目を`verified / human_decision_pending`として未完了に保つ。
Humanは`A1、B1`として両候補を承認した。identity／stale Decisionは
`records/development/2026-08-03-work-3-source-identity-stale-decision.json`、SHA-256
`1eba4807e9b1e5d5ff4fa38e8617e768c27cfe02c553572d91c86cd67366bae9`、完了Evidenceは
`records/development/2026-08-03-work-3-source-identity-stale-completion-evidence-v1.md`、SHA-256
`e0c450b3ec7758f46a9056620513bfa023e8ca8dc8ad78e2e4eb1c65871edb06`。配置・authority Decisionは
`records/development/2026-08-03-work-3-requirements-artifact-layout-decision.json`、SHA-256
`516caf5214bd9bfe840d96a7f1249593c2844da26b511432a8cee12ff91e336e`、完了Evidenceは
`records/development/2026-08-03-work-3-requirements-artifact-layout-completion-evidence-v1.md`、SHA-256
`1aac602366fbe3e5c6a04ec9e509119bcd7472ef54cc627b7af44411f3822725`。両項目は
`verified / completed`となった。承認は規則の確定に限定され、提案directory、schema、追加13 definitionは
未作成、既存37要件は未変更である。次の未完了項目は、承認済み配置への最小schema、validator、fixture、
legacy binding inventoryのtest-first実装である。
実装前RED Evidenceは
`records/development/2026-08-03-work-3-requirements-artifact-runtime-red-evidence-v1.md`、SHA-256
`9c6ec0d66f3bda56deee59e1a410694dd5c60a0ad2dd30fc68125c6efb97d373`。固定Test 12件はvalidator module未実装に
より全件errorとなった。固定Testとfixtureを変更せず、承認済みdirectory、5 artifact kindの最小schema、
Digest／locator／authority chain／legacy sourceを検査するvalidator、既存37 Requirementと6 sourceを結ぶ
legacy inventoryを実装した。GREEN Evidenceは
`records/development/2026-08-03-work-3-requirements-artifact-runtime-green-evidence-v1.md`、SHA-256
`b213de7ae162879dfe7a73bae0aa69d6ccc9a2633dfb08091ebe20ca6dd515f2`。targeted `12 passed`、Requirements関連
`71 passed`、全`448 passed`、独立JSON Schema検査`artifacts=6`に合格した。既存37要件は未変更、追加13
definitionは未作成であり、本項目は`verified / completed`となった。次の未完了項目は追加13 Requirementの
definition／candidate構造化、schema検証、Evidence、Human promotionへの接続である。
追加13 Requirementは`records/requirements/definitions/`の13個の不変definitionへ構造化し、candidate manifestを
`records/requirements/candidates/rc3-requirements-added-13-2026-08-03-v1.json`、file SHA-256
`c3d6497516fcbabd18fdffe88279b1095eec8a140f32e8ca8c7f1d6e3c8d2525`、candidate digest
`89ee1908ec3c0cafd6b4c5d5fe244b7098745265dcc3f247b554a5abe1494773`として固定した。schema、固定source、
definition 13件のID／version／Digestへ結線し、Markdown sourceの8領域と全件一致した。検証Evidenceは
`records/requirements/evidence/rc3-requirements-added-13-evidence-2026-08-03-v1.json`、file SHA-256
`f57a5cdaeb4cf37a0285218e73c6e5342b417d822878d919c29bd0c13d810f55`、evidence digest
`4f5d76d4606627e47b98f8408cdac437d9cb8235e9d2be72f2114fc582d227ca`。独立schema、source alignment、
reference Digest、legacy 37件＋追加13件の50件coverageに合格し、post-write検証は15 artifact、
Requirements関連Testは`75 passed`、全Testは`448 passed`だった。
候補は`verified / human_decision_pending`である。Human promotion Decisionと50 Requirement authority bundleは
未作成であり、directory、definition、Evidenceだけではauthorityにならないため、本checkboxは未完了を維持する。
Humanは追加13 Requirement candidateを承認した。Decisionは
`records/requirements/decisions/dec-requirements-added-13-2026-08-03-v1.json`、file SHA-256
`5489b4b45baa8a9078f97540cc154363157c14e8c5cc56f151ca4d8259b46aff`、record digest
`707c306a19d82cfe94b1140bde884974973e9bf5daeb13d0d8b0f6376f632e31`。50 Requirement authority bundleは
`records/requirements/authority/rc3-requirements-authority-2026-08-03--v1.json`、file SHA-256
`fc6d945a6bef1ebea0c4ef22705d70fac6177a8c561be0f992ca94474a8a7509`、bundle digest
`497bcc4374e3224acbfbb08e38c7d9f3d4e5373f59df505179b6a19bc035a02c`。既存37 legacy bindingと追加13
definitionを結線し、authority chainは`effective`、50 IDの欠落・重複0、独立schema 17 artifact、全Test
`448 passed`だった。完了Evidenceは
`records/development/2026-08-03-work-3-added-requirements-promotion-completion-evidence-v1.md`、SHA-256
`dc945ec1d2eae4fe4c8c3293b9f1390fe4c527094e5dc209082dafc6f3b80649`。本項目は
`verified / completed`であり、次の未完了項目は必須非機能義務のVerification Profile接続である。
必須非機能義務の接続候補は
`records/development/2026-08-03-work-3-nfr-verification-profile-candidate-v1.json`、file SHA-256
`08d5159a483d16507c5652857e5245993b42559ed3bcc24c9434e70b0d5c2381`、candidate digest
`c93f9336790fc8641f3f89687f94fcff3baa23254936545ed9cb85c15c25d3a6`。50 RequirementをNFR接続29件と
functional／control only 21件へ重複・欠落0でscreeningし、Profile 19件を`initial_required: 8`、
`threshold_after_measurement: 6`、`deferred_to_deployment_profile: 5`へ分類した。性能、規模、信頼性、費用、
互換性、security・privacy、maintainabilityの7属性と、各Profileのauthority、適用条件、fixture、environment、
measurement、oracle、failure verdict、Evidenceを被覆した。監査Evidenceは
`records/development/2026-08-03-work-3-nfr-verification-profile-evidence-v1.md`、SHA-256
`e0800a9832798df5ab50a83203c42b16a2728488ff0f8942eb86e919740d2a12`。既知違反6件の負例監査、全Test
`448 passed`に合格した。承認済みArchitecture Policy recordはまだ存在しないため、Planの横断rule 6件は
`proposed_policy_rule_not_authoritative`としてWork 4へrouteし、Policy authorityにはしていない。候補は
`verified / human_decision_pending`であり、Human承認前は本checkboxを未完了のまま維持する。
HumanはNFR Verification Profile接続候補を承認した。Decisionは
`records/development/2026-08-03-work-3-nfr-verification-profile-decision.json`、SHA-256
`6cdb1f74c8b92bcc7257bf8087158f78e8c980428d1b0fa725a20e2dd8e96373`。candidate／Evidence Digestと
Profile 19件の3分類へ承認を束縛し、Architecture Policy昇格0、数値閾値承認0を確認した。完了Evidenceは
`records/development/2026-08-03-work-3-nfr-verification-profile-completion-evidence-v1.md`、SHA-256
`c8c99ca93d9eb29c112febbc18fa53fbf5476d703399a07888b7733cb9fb379f`。Decision bindingと全Test
`448 passed`に合格し、本項目は`verified / completed`となった。次の未完了項目は、deferred候補を初期
Requirementの暗黙依存にしていないことの確認である。
deferred scope候補は
`records/development/2026-08-03-work-3-deferred-scope-candidate-v1.json`、file SHA-256
`01da1ea0c6c4f6adad8fdcd09085f97b387ea4639d01b0811b80dc5957916210`、candidate digest
`8993a6e4671679ab8cfe665322efdaf862cf085a8f1fab7d500d15f5fd7deb84`。13候補を
`explicit_deferred: 9`、`conditional_pilot: 2`、`not_adopted_without_new_evidence: 2`へ分類し、
各候補のowner、成果、論理配置、有効化条件、初期非依存規則を固定した。監査Evidenceは
`records/development/2026-08-03-work-3-deferred-scope-evidence-v1.md`、SHA-256
`1c24269e36d2baa2a4e22d39162e7bb85b7c5e513c55a5035fa55efa54029b71`。50 Requirement、NFR Profile、
Work 5A、Work 6A、Work 7A、Work 8、Work 8A、Work 7B、Stage G／releaseの9 consumerでscope leak 0、
未知Requirement／Profile参照0、release blocker 0、既知違反6件の負例監査に合格した。
`REQ-CONTRACT-008`はeffectiveだが、definition自身の初期範囲外規則へ従い最初のContractとreleaseを
blockしない。候補は`verified / human_decision_pending`であり、Human承認前は本checkboxを未完了に保つ。
Humanは再検証済みdeferred scope候補を承認した。Decisionは
`records/development/2026-08-03-work-3-deferred-scope-decision.json`、SHA-256
`fc1aba9c31b612939c5e62fec3327ab1b65449257f044a2a7206f2c564cd7873`。candidate、旧監査Evidence、
authority v2に対する再検証Evidenceへ判断を束縛し、13件すべてのrelease effect `nonblocking`、scope leak 0、
release blocker 0を維持した。Completion Evidenceは
`records/development/2026-08-03-work-3-deferred-scope-completion-evidence-v1.md`、SHA-256
`2f79c3f8005967670b97c0597d86e3aeb17b5151ba7ebd260e201a3c66a893fe`。deferred能力の実装・有効化、個別Pilot開始、
Requirement／Plan変更、Work 3段完了は承認していない。本項目は`verified / completed`となり、Work 3の個別項目は
すべて完了Evidenceへ接続された。
scope監査中に発生したauthority bundle二形式読取りとTest実行環境選択の問題に対する恒久対策は
`records/development/2026-08-03-work-3-permanent-remediation-green-evidence-v1.md`、SHA-256
`096e91d786293b5d01f1a14717f49c2b0806c48a8ea8d3b76439108a7ec6af0c`。共通machine reader、旧37要件の
決定的移行器、版付きpolicy Test runnerをtest-firstで実装した。旧37 definitionと既存13 definitionを結ぶ
統一50 candidateは`records/requirements/candidates/rc3-requirements-unified-50-2026-08-03-v1.json`、file
SHA-256 `c82144375fecc22c088d06d510d9e041fe9c607a0d6e4eb353b034467654ca16`、candidate digest
`cc4ba8f872973f8035b798042f4a5335005394cca339ec6f0121cf16c8c533b4`。移行は意味field不一致0、再生成差分0、
schema不一致0で、policy runnerによる全Testは`462 passed`、fallbackは`false`だった。現行effective authorityは
v1のままであり、統一candidateは`verified / human_decision_pending`である。Human promotion後にだけ旧v1を
supersedeするauthority bundle v2を作成し、影響するNFR／deferred Evidenceを新identityへ再検証する。
Humanの方針変更指示により、LLMを文章操作・意味分析へ限定し、それ以外の決定的処理をmachineへ割り当て、
手作業由来の手戻りを機械化候補として報告するPolicy v5を実装した。Decision recordは
`records/development/development-policy-v5.json`、RED Evidenceは
`records/development/2026-08-03-development-policy-v5-red-evidence-v1.md`、GREEN receiptは
`records/development/2026-08-03-development-policy-v5-green-test-receipt-v2.json`。Policy evaluatorは
`manual_rework_candidate`と`manual_operation_candidate`、8つの必須報告fieldを機械判定し、全Test
`467 passed`だった。現行Planのpolicy参照はv5へ更新し、旧Plan Digestを固定したNFR／deferred候補は
identity再検証までstaleとする。
Humanは統一50 Requirement candidateを承認した。Decisionは
`records/requirements/decisions/dec-requirements-unified-50-2026-08-03-v1.json`、record digest
`b8cce324d5693a2bf4c8e5b9acb8adbf023f726069407e137faebcaa765442d8`。authority bundle v2は
`records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json`、bundle digest
`79a69d921bb00eb2b321e3d1adb073b88a527eb938398d1813567009255bd688`で、50 definition、legacy binding 0、
authority `effective`となった。生成器はtest-firstで追加し、全Test `470 passed`、独立JSON Schema 54 artifact、
再生成`written 0 / unchanged 2`に合格した。Completion Evidenceは
`records/development/2026-08-03-work-3-unified-requirements-promotion-completion-evidence-v1.md`、SHA-256
`c151019466bdcca66236646f6e635cc729b96585ffa43e68eacac975f3470e80`。NFR／deferred候補は新authorityと
current Planへ再検証し、NFRは既承認範囲の変更0によりfresh、deferredは`verified / human_decision_pending`とした。
HumanはWork 3 Completion Candidateを明示承認した。Decisionは
`records/development/2026-08-03-work-3-completion-decision.json`、SHA-256
`5cf7bb52e5cff547e06581ed6c8b57e8b77eaedc352615e5a063f422467dcf45`。7個別項目、現行effective authority v2、
blocker 0、完了を阻害するstale 0へ判断を束縛した。段完了Evidenceは
`records/development/2026-08-03-work-3-completion-evidence-v1.md`、SHA-256
`e602092b3236f62697b2f24d2b706095dda6b8c83e22e5b6211fb539542c7221`。公式全Testは`470 passed in 2.35s`、
fallback `false`である。Work 3は`verified / completed`となり、次の未完了工程はWork 4である。Work 4の
成果物変更、Plan全体の承認、deferred能力の有効化、commit、push、releaseは開始または承認していない。

### Inter-work：Work 3完了後の追加correctiveと早期Pilot

このthreadで当初順序外に追加した作業は、
`records/development/2026-08-04-thread-added-work-plan-checklist-reconciliation-v1.md`をscope正本として扱う。

#### Session transcript eventual preservation

- [x] Codex CLI／Desktopの異なるsource形式を扱い、Claudeをsource adapter境界へ含めた。
- [x] manual collector、durable cursor、再開、reconcile、raw／派生物／Provenance分離を実装した。
- [x] Humanが許可した現在のCodex Desktop taskだけを限定captureし、再実行一致と権限を検証した。
- [ ] background automation、長期retention、削除、application-layer暗号化、backupを判断・実装した。

`Evidence`：`records/development/2026-08-04-session-transcript-eventual-preservation-completion-evidence-v1.md`、
SHA-256 `194c302277299cb3ab8853951f8db8d5d64424d4f16c1798e0a82f40eb41740a`。本完了はdevelopment限定であり、
Session Records製品機能全体または常駐automationの完了を意味しない。

#### Deployment／Project Artifact boundary

- [x] Project Artifactを移動せずdeployment packageを交換するLayout Baseline v2を承認した。
- [x] ReviewCompass3 Project Manifest v2と移動させない`.reviewcompass/workflow/` rootを作成・検証した。
- [x] Issue、Plan、Decision、EvidenceをpathだけでなくID、version、Digest、relationで結ぶ境界を固定した。
- [ ] Deployment Manifest、package builder、原子的切替、rollback、durable Project Bindingを実装した。

`Evidence`：Layout v2 Approval Decision
`records/development/2026-08-04-layout-baseline-v2-approval-decision.json`、SHA-256
`856345948af57bcfa373eb2766768d9c38078d7ba5fe65b0d76d68e452ceaa7e`。Project Manifest v2 Completion
Evidenceは`records/development/2026-08-04-project-manifest-v2-completion-evidence-v1.md`、SHA-256
`154d3f5d930b16c9974431568e9430d896f580d99e03c59efffb5fba878ec020`。未完了項目はWork 7A／7Bに残す。

#### ReviewCompass Issue Resolution早期Pilot

- [x] ReviewCompass2のIssue→Plan経路をReviewCompass3へ継承する早期PilotをHumanが承認した。
- [x] TODOはactive ID projectionに限定し、詳細候補をdurable Candidate／Issue経路へ分離する案を固定した。
- [x] Pilot recordの移動させない上位rootを`.reviewcompass/workflow/`へ固定した。
- [x] Pilot Task Contractと固定sourceを作成した。
- [x] Improvement CandidateとHuman Triage Decisionのidentity、field、命名、version、Digest、参照規則を
      正常・負例・境界Testへ固定した。
- [x] 最初のCandidate／Triage Decisionを作り、Human判断なしのIssue昇格を拒否した。
- [x] ReviewCompass Issue Record、Resolution Plan、Plan Challenge、Verdictの最初の手作業経路を検証した。

`Evidence`：Early Pilot Decision
`records/development/2026-08-04-reviewcompass2-issue-path-early-pilot-decision.json`、SHA-256
`5e19bca05aead7836595168f8e44edc3a5f146507ab33ffde3646de964814f9f`。TODO routing revision memoは
`docs/design/2026-08-04-todo-rework-candidate-routing-revision-memo.md`、SHA-256
`e156a3b055b19b70bfb9bbe77d1af444ee30ecfcfbf47a7d436096dddcb571b3`。製品schema、正式state machine、
Workflow permit、自動Plan編集、automation、Work 8評価は前倒ししない。

Task Contract／暫定shape bootstrap Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-bootstrap-completion-evidence-v1.md`、SHA-256
`1f2b981301e9a249226de4253f504586cea6f6dc23c5c1d780c53e4ec84b1f37`。固定source 9件を再照合し、同じ
Pilot Testを変更せず`15 failed`から`15 passed`へした。既存Layout snapshot Testは意図した空directory追加へ
更新し、関連`27 passed`となった。Candidate、Decision、Issueは未作成である。Pilot全体の完了ではなく、次は
単一CandidateとHuman Triage Decisionを作成する。

Candidate／Triage Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-candidate-triage-completion-evidence-v1.md`、SHA-256
`9ebfe80bb351f6c09a0d27508c70988ce1fe24593324209423e94e9d94bea523`。Humanは選択肢1として
`issue_resolution / blocking=false`とIssue ID `ISSUE-PILOT-TODO-GROWTH-001`への昇格を承認した。Decisionは
CandidateのID、version、file Digest、content Digestへ束縛され、関連Testは`16 passed`となった。Issue Record、
Resolution Plan、Plan Challenge、TODO compactionは未実施であり、最後のPilot checkboxは未完了のままとする。

Issue／Plan Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-issue-plan-completion-evidence-v1.md`、SHA-256
`a1efb8ff5bb7027f604774a27cc5681bc4d6f6e0cf1931727407361803d7fa61`。承認済みIssue一件とResolution Plan一件を
別identityで作成し、Human promotion、固定参照、Issue obligation、作業項目、Acceptance、oracle、rollbackを
version 2 validatorへ固定した。関連Testは`33 passed`。Plan Challenge、TODO compaction、Verdictが未実施のため、
最後のPilot checkboxは未完了のままとする。

Plan Challenge v1はderived state closure欠落をblocking Findingとして検出し、Humanの修正Decision後にPlan v2と
Challenge v2を作成した。Challenge v2は10基準合格、blocking Finding 0、`ready_for_human_approval`となり、Humanは
Plan v2を承認した。Approval Decisionは
`records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v2-decision.json`、SHA-256
`07e6d865d27c86d9f039b5742092efcf1429656f38ec4ac3ddfc23e697d4f892`。次は別作業単位で実装Task Contractを作成する。
TODO compactionとResolution Verdictは未実施のため、最後のPilot checkboxは未完了のままとする。

Task Contract作成前の照合で、Plan v2のderived state表に「作成・検証済みだが未commit／未開始のTask Contract」状態が
ないことを検出した。Candidateは
`records/development/2026-08-04-issue-resolution-pilot-task-contract-state-gap-candidate-v1.json`、SHA-256
`b8300b13fed8af8c95cee424a1478aaedfaa085a27d9dcb6512c48ea15c6e632`。Acceptance truthへ影響するためTask Contract作成を
停止し、Plan v2を上書きせずPlan v3修正をHuman判断待ちとする。最後のPilot checkboxは未完了のままとする。

Humanが推奨案Aを承認し、Plan v3へ`task_contract_commit_pending`、`implementation_ready`、
`implementation_in_progress`の境界、containing commit関門、三状態oracleを追加した。Challenge v3は10基準合格、
blocking Finding 0、`ready_for_human_approval`である。RED／GREEN Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-plan-v3-red-evidence-v1.md`。Task Contract作成と実装は未開始で、
Plan v3の最終Human判断まで最後のPilot checkboxを未完了に維持する。

HumanはPlan v3を最終承認した。Approval Decisionは
`records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v3-decision.json`、SHA-256
`31abfa394605915d4abe4fe6f121816a1229669d9c9144b8184edad34d093b95`。Plan v3 Approval作業単位をcommitした後、
別作業単位で実装Task Contractを作成する。Task Contract、WI-001、TODO compaction、Resolution Verdictは未実施のため、
最後のPilot checkboxは未完了のままとする。

実装Task ContractをPlan v3とApproval Decisionへ結線して作成・検証した。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-implementation-task-contract-completion-evidence-v1.md`、SHA-256
`591b786b3128bde56d2d4c92af1b5883ec0c2323de5973758dab809f1b64d6f1`。6 Work Item、三状態境界、TDD、禁止事項、
rollback、Human関門はPlan v3と一致し、専用`5 passed`、公式全`562 passed`である。現行stateは
`task_contract_commit_pending`で、Task Contract work unitのcommit後までWI-001を開始しない。最後のPilot checkboxは
未完了のままとする。

Task Contract containing commitを確認後、WI-001のbyte-exact snapshot／別manifest／再読込／改変拒否を9件のTestへ
固定した。RED Evidenceは`records/development/2026-08-04-issue-resolution-pilot-wi-001-red-evidence-v1.md`、SHA-256
`b7b4b38b6aa983a219d554d8da341bbc4b1a1c8a303710ab84446f8820c45218`。targetedは`9 failed`、全体は既存
`562 passed, 9 failed`で、失敗は全件期待module未実装だけである。実TODO、snapshot、manifest、実装codeは未変更。
RED作業単位のcommit後まで実装を開始せず、最後のPilot checkboxは未完了のままとする。

固定Testを変更せずsnapshot helperを実装し、targeted `9 passed`を確認したが、実snapshot作成前にPlan v3
ACC-001の「圧縮直前TODO」とTask Contract v1のWI-001先行順序が、必須TODO更新により両立しないことを検出した。
Pause Evidenceは`records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-pause-evidence-v1.md`、
SHA-256 `727975c1293976959449360e2d1af10ad749b3cf4b7d4e94c8daba8f0bfe76ce`。実snapshot／manifestとTODO compactionは
未実施で、Acceptanceへ影響するため`pause_and_triage`とし、版付きUpstream RevisionのHuman判断を待つ。

Humanは推奨案を承認し、Decision
`records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-decision.json`で
`current_issue_plan_revision / blocking`を固定した。Triage Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-triage-completion-evidence-v1.md`、
SHA-256 `bcb4083827c6ce2b5de4bb23ec113e2543b006caedd6b8a30edd1421361beee3`。二件目workflow Candidate配置は
単一subject Testで`570 passed, 1 failed`となり、current Issue内改定recordを`records/development/`へ戻して
公式全`571 passed`を確認した。現在の停止・判断作業単位をcommitした後だけ、Plan v4のRED Testと候補作成へ
進む。最後のPilot checkboxは未完了のままとする。

停止・判断作業単位のcontaining commit `64782ec`とclean transitionを確認後、Plan v4のsnapshot timing境界を
10件のTestへ固定した。RED Evidenceは`records/development/2026-08-04-issue-resolution-pilot-plan-v4-red-evidence-v1.md`、
SHA-256 `3fe743c2be6e957fabaa1477745c66323c8b5077c9fd0ca83acc1c57a7a15c94`。targetedは`1 passed, 9 failed`、
全体は既存を含む`572 passed, 9 failed`で、失敗はPlan v4実体不在とversion 4専用validator未実装だけである。
RED作業単位のcommit後までPlan v4候補とvalidatorを作成せず、最後のPilot checkboxは未完了のままとする。

Plan v4 RED containing commit `7df9cb9`とclean transitionを確認後、固定Testを変更せずversion 4 validatorと
Plan v4候補を作成した。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-plan-v4-completion-evidence-v1.md`、SHA-256
`0d90206a1eaec5a2571ddc732d5fbd341593995562170e4d97fab31e43785720`。targeted `10 passed`、公式全
`581 passed`、fallback `false`で、Plan v1〜v3、Task Contract v1、実snapshot、TODO compactionは未変更。
GREEN作業単位のcommit後までChallenge v4を開始せず、最後のPilot checkboxは未完了のままとする。

Plan v4 GREEN containing commit `8f58235`とclean transitionを確認後、Challenge v4を実施した。Completion
Evidenceは`records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v4-completion-evidence-v1.md`、
SHA-256 `1290ec51776daf55ce43c450c24d665753a6223d975988a94050df8dfce17996`。10 criteriaは全pass、blocking
Finding 0、stale binding `false`、`ready_for_human_approval`、公式全`581 passed`、fallback `false`である。
Challenge作業単位のcommit後にHuman Plan Decisionを要求し、承認前はTask Contract v2を作成しない。

Challenge v4 containing commit `07b5617`とclean transitionを確認後、HumanはPlan v4を承認した。Approval
Completion Evidenceは`records/development/2026-08-04-issue-resolution-pilot-plan-v4-approval-completion-evidence-v1.md`、
SHA-256 `93cbd5815652777712da087c5ba4be4774da1d2e86972b7cec88336b0346aea3`。DecisionはPlan v4、Challenge v4、
公式全581 Test receiptへ結線され、Task Contract v2の別作業単位作成だけを許可した。承認作業単位のcommit後まで
Task Contract v2を作成せず、最後のPilot checkboxは未完了のままとする。

Plan v4 Approval Decision containing commit `b969200`とclean transitionを確認後、Task Contract v2のPlan v4結線、
WI-001 completion繰越、7 Work Item順、WI-007／WI-003 source identity境界を8件のTestへ固定した。RED Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-task-contract-v2-red-evidence-v1.md`、Test SHA-256
`afe238e5fa1857e5ea5ea03a5bc20bbd0e7216d3ddbeb16eb6af8e69c3b7aa13`。targetedは`8 failed`、全体は既存
`581 passed, 8 failed`で、失敗はTask Contract v2実体不在と専用validator未実装だけである。RED作業単位の
commit後までv2実体、実snapshot、WI-002、TODO compactionを開始せず、最後のPilot checkboxは未完了のままとする。

Task Contract v2 RED containing commit `0a8cc73`とclean transitionを確認後、旧Testを弱めずv2実体と専用validatorを
作成した。意味照合でv1由来goalの旧`Plan v3`表記を検出したため、要求誤解時の修正规則に従ってPlan v4へ補正し、
旧表記を拒否する負例を追加した。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-task-contract-v2-completion-evidence-v1.md`。Plan v4結線、
WI-001 completion繰越、7 Work Item順、WI-007／WI-003 source identity境界はtargeted `9 passed`、公式全
`590 passed`、fallback `false`。v2作業単位のcommit後までWI-002、実snapshot、TODO compactionを開始せず、
最後のPilot checkboxは未完了のままとする。

Task Contract v2 containing commit `156c823`とclean transitionを確認後、WI-002のTODO全体12 KiB上限、禁止履歴、
active ID、参照解決、snapshot Digest、決定的restoreを12件のTestへ固定した。RED Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-002-red-evidence-v1.md`、Test SHA-256
`c5dd608f2561130d3fb46ffa23bb6363e823d65eaa89c89b14a4741e788315a1`。targetedは`12 failed`、全体は既存
`590 passed, 12 failed`で、失敗は全件`tools.development.todo_compaction`未実装だけである。RED作業単位の
commit後までvalidator／restore実装、実snapshot、TODO compactionを開始せず、最後のPilot checkboxは未完了の
ままとする。

WI-002 RED containing commit `7e435d1`とclean transitionを確認後、固定12 Testを変更せず
`tools/development/todo_compaction.py`を実装した。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-002-completion-evidence-v1.md`。12288 bytes境界、
禁止履歴、active ID、参照解決、snapshot／manifest Digest、byte-exact restore、失敗時rollbackはtargeted
`12 passed`。restore対象path限定を別Test 4件でREDからGREENへ固定し、公式全`606 passed`、fallback `false`。
restore対象pathをroot TODOとsession-handoffsへ限定し、
実TODO、実snapshot、TODO compactionは未変更である。GREEN作業単位のcommit後までWI-006を開始せず、最後の
Pilot checkboxは未完了のままとする。

WI-002 GREEN containing commit `93785da`とclean transitionを確認後、WI-006の13許可state、最新版選択、欠落、
同version競合、stale binding、手入力不一致を18件のTestへ固定した。RED Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-006-red-evidence-v1.md`、Test SHA-256
`b0fd75602017d9552972e54f4696c9b5f7f8b796d5cfef5b406a2a0ba2579d9c`。targeted `18 failed`、全体は既存
`606 passed, 18 failed`で、失敗は全件専用module未実装だけ。RED commit後までresolver、実snapshot、TODO
compactionを開始せず、最後のPilot checkboxは未完了のままとする。

WI-006 RED containing commit `5750935`とclean transition確認後、固定18 Testを変更せずstate resolverを実装した。
Completion Evidenceは`records/development/2026-08-04-issue-resolution-pilot-wi-006-completion-evidence-v1.md`。
13許可state、最新版選択、Evidence ID、欠落、同version競合、stale、手入力不一致はtargeted `18 passed`、公式全
`624 passed`、fallback `false`。実snapshotとTODO compactionは未変更。GREEN commit後までWI-007を開始せず、
最後のPilot checkboxは未完了のままとする。

WI-006 GREEN containing commit `6b68c25`とclean transition確認後、WI-007を実施した。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-007-completion-evidence-v1.md`。source TODO、snapshot、
manifestを別々に再読込し、SHA-256 `16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`、
85219 bytes、900 lines、123 Claimsで一致した。versioned recoveryを含むsnapshot関連`10 passed`、公式全
`625 passed`、fallback `false`。本作業単位ではTODOを変更せず、containing commit後のsource再照合までWI-003を
開始しない。最後のPilot checkboxは未完了のままとする。

WI-007 containing commit `b10cd09`後にsource identity一致とclean transitionを再確認し、WI-003 projection rendererの
5 Testを固定した。RED Evidenceは`records/development/2026-08-04-issue-resolution-pilot-wi-003-red-evidence-v1.md`、
Test SHA-256 `c284b442c36b7bc46681a9a154038980b122ffd33001e1023d704ac69badbaf4`。targeted `5 failed`、全体は
`625 passed, 5 failed`で、失敗は専用module未実装だけ。本RED commitではTODOを変更せず、source SHA-256
`16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`を維持する。

WI-003 RED containing commit `05b0c98`後にsource identity一致を再確認し、root TODOを機械生成して85,219 bytes、
900 lines、123 Claimsから2,824 bytes、64 lines、詳細Claim 0、active Issue 1件へ圧縮した。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-003-completion-evidence-v1.md`。実templateとの結合不足を
書込み前検査で検出し、repository template結合Testを追加して修正前`1 failed`、修正後は関連`38 passed`、公式全
`631 passed`、fallback `false`。WI-007 snapshot／manifestは不変で、WI-003 containing commitとclean transition後に
WI-004へ進む。最後のPilot checkboxは未完了のままとする。

WI-003 containing commit `416e4e1`とclean transition後、WI-004の共通prompt、AGENTS一参照、Claude link-only入口、
第二authority拒否を3件のTestへ固定した。REDは`1 passed, 2 failed`、実装後はtargeted `3 passed`、公式全
`634 passed`、fallback `false`。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-004-completion-evidence-v1.md`。root TODOはactive Issue一件を
維持したままWI-005入口へ機械更新した。WI-004 containing commitとclean transition後だけWI-005へ進み、最後のPilot
checkboxは未完了のままとする。

WI-004 containing commit `665d9f6`とclean transition後、WI-005のpost-write、隔離restore、参照Digest、Verdict候補、
Human判断先取り拒否を5件のTestへ固定した。RED `5 failed`からGREEN `5 passed`、公式全`639 passed`、fallback
`false`。Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-wi-005-completion-evidence-v1.md`。機械導出stateは
`verdict_pending`、候補推奨は`resolved`、effective outcomeは`pending_human_decision`。WI-005 containing commit後に
Resolution VerdictのHuman判断を要求し、最後のPilot checkboxとWork 4復帰は未完了のままとする。

WI-005 containing commit `6da0270`後、Humanは固定候補の推奨、未処理、残余riskを確認し、Verdict `resolved`、
早期Pilot完了、Work 4復帰を承認した。Closure Completion Evidenceは
`records/development/2026-08-04-issue-resolution-pilot-closure-completion-evidence-v1.md`。Human以外、stale候補binding、
残余risk未受容の負例を含むtargeted `9 passed`、公式全`643 passed`、fallback `false`。正式製品schema、UI、
automation、Work 8評価はdeferredのまま、当初順序のWork 4へ戻る。

- [x] 上記bootstrap閉鎖の後、開発用の限定拡張としてIssue Intake V4を追加し、その実地検証も閉じた。

Issue Intake V4限定拡張の承認・閉鎖。V4は登録済みIssue数に上限を置かず、`in_progress`だけを最大1件に
制限する。Humanの判断recordを正本とし、候補bundleは機械抽出時の観測として書き換えない。過去TODO候補41件は
全件Human triage済みで有効decision 41件・競合0件、正式Issueは3件でいずれも`registered`かつnonblocking、
active Issueは0件である。承認Decision `DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`は
`records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md`、SHA-256
`019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c`。閉鎖Evidenceは
`records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md`、SHA-256
`b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e`。承認は開発用・暫定に限り、
`pilot_mode: development_only_provisional`を維持する。正式製品schema、UI、automation、3正式Issueの
Plan化・実装、Work 8評価は引き続き承認範囲外である。上記の早期Pilot完了記録は消さずに残す。

- [x] `ISSUE-HTC-C9F6C917`のPlan提案v2の§3最小縦切りだけをHumanが承認し、実装した。

機械操作routing v2の最小縦切り。承認したのはversioned operation inventory、permission preflight、
execution receiptの3部だけである。実装moduleは`tools/development/operation_routing.py`で、
既存policy runnerとは別moduleとし、shellも外部processも起動しない。承認と取得済み権限の確認はhost側に
置き、project内は必要な権限種別を計算して出すだけである。承認Decision
`DEC-MACHINE-OPERATION-ROUTING-001`は
`records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md`、SHA-256
`c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969`。GREEN Evidenceは
`records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md`、SHA-256
`e4f8d9f865e6b6d35e7d00a21eba54c13b1ed331fca3183827b1262d285d88eb`。対象testは`16 passed`、公式全testは
`845 passed`。定型欄生成、構造化argv executor、cache root固定の3項目は、その後の最小sliceがそれぞれ承認・実装済み
である（`DEC-RECORD-GENERATION-PLAN-001`、`DEC-MACHINE-OPERATION-ROUTING-READ-ONLY-ARGV-001`、
`DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001`。2026-08-08改定r1で反映、
指摘元は`IC-CHECKLIST-APPROVAL-SCOPE-STATEMENT-DRIFT-001`）。既存直接操作の移行、host側tool構文、
外部送信は引き続き承認範囲外である。`ISSUE-HTC-C9F6C917`のIssue recordは
`registered`のままであり、**V4 Issueの正式Plan化や実装一般が完了したわけではない**。

その後、execution receiptの改竄を拒否できない欠陥が見つかり、receipt validatorを訂正した。訂正後は、
receiptが完全な検証済みpreflight recordを保存し、validatorがinventoryから必要権限を再計算して照合する。
自己Digestを合わせ直した改竄も拒否する。execution receiptのschema versionは2（inventoryとpreflightは1）。
訂正Decision `DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`は
`records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md`、
SHA-256 `f73f06e12f464a27ded059522e37015acbd2f9487d7d65d55ed96823a6f8033b`。訂正GREEN Evidenceは
`records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md`、
SHA-256 `b6255b0a7de3bcd90b62745ff934a957dba94b3870bc847517f1dbde36a430ea`。対象testは`23 passed`、公式全testは`852 passed`。初回のGREEN Evidenceと
receiptは削除せず履歴として残すが、validatorの欠陥判明によりstaleであり、有効な完了根拠は訂正側である。

#### Commit／handoff安定化

- [x] TODOをcommit安定形式にし、commit後の自己SHA転記と追加commitを廃止した。
- [x] commit後はread-only照合だけを行い、guarded commit、amend、hookを使わない規則を固定した。
- [x] 完了済み作業単位が未コミットなら、次作業を停止してHumanへリマインドするPilotを実装した。
- [x] 通常commitを最小ガード付きで自律化し、push、tag、amend、rebase、reset、force push、
      履歴書換えはHuman明示承認のまま維持した。

`Evidence`：commit handoff Completion
`records/development/2026-08-04-commit-handoff-stability-completion-evidence-v1.md`、SHA-256
`a0e03f686c9879416798ed58a56e610f59e0fb775a9c4c73fb61a16a623ea077`。work unit reminder Completionは
`records/development/2026-08-04-work-unit-commit-reminder-completion-evidence-v1.md`、SHA-256
`b7f8e91520b2664ede24347144004b724c5654d23c5cb318864c1a8530ab35d0`。

旧「自動commit、push、rebase、reset、履歴書換えをPilot対象外に維持した」というclaimは、通常commitの
扱いだけを置換した。Humanは、意味的に完結した単位であること、明示pathだけをstageすること、
`git diff --check`と該当test／validatorに合格すること、commit後にread-onlyで照合することの4条件を
満たす通常commitについて、毎回の明示指示を不要とした。push、tag、amend、rebase、reset、force push、
履歴書換え、方針変更、段完了、意味的裁定、不可逆操作、外部送信、権限の迂回はHuman明示承認のままである。
guarded commit、hook、コミットごとの承認file、巨大なcommit manifestは導入しない。Decisionは
`records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md`
（`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`）。

#### Development venv baseline

- [x] `.venv`を機械作成し、Git管理対象外へ固定した。
- [x] pip、setuptools、wheelと全開発依存をexact lockへ固定した。
- [x] 公式Test runnerを`.venv/bin/python3`へ切り替え、system Python fallbackを禁止した。
- [x] venv欠落、Python不適合、lock改変、pytest不適合の負例を確認した。
- [x] system Pythonにだけ存在した未宣言`PyYAML`依存を正式な実行時依存へ修復した。
- [x] `.venv`とinstall metadataをsource state Digestから除外した。
- [x] 関連Testと公式全Testをvenv上で再実行した。

`Evidence`：`RC3-DEVELOPMENT-VENV-BASELINE-2026-08-04-V1`、
`records/development/2026-08-04-development-venv-baseline-completion-evidence-v1.md`。
関連`22 passed`、公式全`652 passed`、Python `3.9.6`、pytest `8.4.2`、fallback `false`。
旧system Python receiptは履歴として保持する。本baselineはWork 4／4Aの開始または順序変更を意味しない。

#### Inter-work完了関門

- [x] 完了済みcorrectiveを固定Evidenceへ接続した。
- [x] Layout bootstrapをWork 7、session保全をSession Records製品機能、早期PilotをWork 8完了と誤表示していない。
- [x] Issue Resolution早期Pilotの限定bootstrapを完了した。
- [x] 限定bootstrap完了後、当初順序のWork 4へ戻った。

#### Work 4A先行の実行順序Decision

- [x] HumanがWork 4よりWork 4Aを先行する順序変更を承認した。
- [x] Work 4Aの最初にSource Snapshot identityの最小必須境界を固定し、Work 4全体は先行完了しない境界を定めた。
- [x] Work 4A完了後に残りのWork 4へ戻ることを固定した。

`Evidence`：`RC3-WORK4A-SEQUENCE-APPROVAL-2026-08-04-V1`、
`records/development/2026-08-04-work-4a-sequence-approval-decision-v1.json`、SHA-256
`4a10d09c12f227e67399aad1dc9c1ca8a6c664edcc6bc7f99385edafa7f48f0f`。
本DecisionはCurrent Plan 17節の初期実装順6・7だけを`Work 4A -> Work 4`へ置き換える。
見出しの物理配置は安定したWork番号を維持するため移動しない。

### Work 4：Designと代表シナリオ

- [ ] Contract、Portfolio、Compiler、Plan bundle、Workflow、Provenance、Deploymentを設計した。
- [ ] `new_development / fresh`の最小vertical sliceを詳細化した。
- [ ] maintenance／reopen、上流改定、依存／中止、配置lifecycleを代表シナリオで縦断確認した。
- [ ] Current Work Projectionを正式Task Contract／Workflow／Provenanceへ写像する境界を設計した。
- [ ] negative path、停止、復旧、Human判断、Deferred Acceptanceのownerを定めた。
- [ ] 旧設計の全項目を`preserve | adapt | replace | defer`へ分類した。

### 完了関門

- [ ] 最初のReview Task Contractに必要なDesignとAcceptance Testが実装可能な粒度である。
- [ ] 新しい第5段相当の完了条件を満たし、Human判断を得ている。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 7. Work 4A：再利用探索baseline（早期完了）

- [x] source universeを再観測し、source content IDとObservationを外部`DATA_ROOT`へnew-only生成した。
- [x] Routine Profile v3を生成し、routine 1003件の機械的特徴を記録した。
- [x] Comparison Discoveryを生成し、682 groupの全memberを外部recordへ保持した。表示は代表最大3件に限定した。
- [x] ProfileとDiscoveryのidentity不一致、member切捨て、語彙外group、旧bounded seedの権威利用を
  acceptance testで拒否した。
- [x] v3.3 acceptance 15件、全test 739件を通した。LLM処理、Human処置label、Entry、Relation、
  Baselineは作成していない。

### 完了関門

- [x] 実sourceから再生成可能なReuse Discovery baselineがあり、比較候補を上限で失わない。
- [x] 機械的groupを意味的統合の結論として扱わない境界がTestとEvidenceで固定されている。
- [x] `DEC-WORK4A-EARLY-EXIT-001`により、全件分類・全件台帳化をWork 4Aの完了条件からWork 4Bへ移した。

`Authority`：[Work 4A Rebuild Design v3](../design/2026-08-04-work-4a-rebuild-design-v3-proposal.md)、
[v3.1 Amendment](../design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md)、
[v3.3 Proposal](../design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md)、
`DEC-WORK4A-REBUILD-DESIGN-003`、`004`、`006`、`DEC-WORK4A-EARLY-EXIT-001`。
Evidence：`records/development/2026-08-05-work-4a-v3-3-actual-comparison-discovery-evidence-v1.md`。
E2E Test：`tests/test_work4a_rebuild_v3_e2e.py`、`tests/test_work4a_rebuild_v3_1_e2e.py`、
`tests/test_work4a_rebuild_v3_2_e2e.py`、`tests/test_work4a_rebuild_v3_3_e2e.py`。

### Work 4B：再利用・統合の運用Pilot

- [x] 新規・変更routineの対象範囲で、既存routine検索を実装前に実施し、結果を記録する。
  （構成B GREEN Evidence 2026-08-07、以後の各作業単位でreuse-search attestationを実運用）
- [ ] 必要なcandidateだけについて、Humanが処置labelを確定し、Entry・Relation・Baselineをnew-onlyで記録する。
  （評価①の実装同一性判定は59組完了・基準確立：`DEC-EGRESS-B-CHECK-001`。処置label＝統合可否は
  評価②の手順4で系統ごとにHumanが確定する）
- [ ] 共通候補ごとに振る舞いTestを固定し、共通部品への段階移行と旧実装の削除判断を独立Work Itemで行う。
  （**実行形が承認済み**：評価②提案v2＝`DEC-CONSOLIDATION-EVAL2-APPROVAL-001`。1系統1単位・TDD・
  挙動不変・守り役への反証レビュー。系統A材料済み、次はA+C合流のdigest系材料）
- [x] Work 5Bの内部Implementation Task Contract Pilotで、再利用検索と台帳更新のgateを実証する。
  （Work 5B検査器 GREEN・構成D台帳初回実運用 2026-08-07、attestation群で継続実証）

Work 4Bは全routineの一括分類を前提にしない。LLMの説明・Disposition Proposalは別承認後のみ使用する。

### Work 4：最初のslice設計の承認

- [x] 最初のReview Task Contractの設計提案をHumanが承認した（`DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001`）。
- [x] 対象は`docs/`配下の一文書、束縛Requirementは16件、残り34件は`deferred`と確定した。
- [x] 後続評価E2〜E7を`deferred`とし、E2・E4・E5の開始に別途Human判断を要すると確定した。

本承認はWork 4全体、Work 5A、Work 4Bの完了を意味しない。

## 8. Work 5A：最小Review Task Contractの定義とhappy path

### Contractとred

- [x] 一種類のReview Task Contractを固定Requirementから定義した。
- [x] Responsibility、Boundary、Context、Capability、Output、Acceptance、Provenance、Escalationを定めた。
- [x] Definition Challengeを通し、Contractの粒度と依存を確認した。
- [x] Acceptance Testとnegative fixtureを先に作成した。
- [x] 実装がなければ期待理由で失敗するredを確認した。

### green実装

- [x] 最小schemaとvalidatorを実装した。
- [x] 一Contractから一Plan bundleと6 typed viewを生成した。
- [x] Context Manifest、Workflow permit、Harness stub、Traceを接続した。
- [x] deterministic stub reviewerからConformanceとFinal Challengeを生成した。
- [x] Human decision、Decision Record、Provenance verdict、accepted artifactを接続した。
- [x] read-only local GitのSource SnapshotとChange Setを接続した。
- [ ] bootstrap Current Work Projectionを正式recordへ写像し、textとmachine-readable出力の同値を確認した。
- [ ] 同じTestを変更せずgreenにし、refactor後も再確認した。

### 完了関門

- [x] Requirementからaccepted artifactまで一つのE2Eがgreenである。
- [x] 汎用DSL、plugin、任意Task orchestration、画面UIを実装していない。

`Evidence`：
`records/development/2026-08-05-work-5a-first-review-contract-green-evidence-v1.md`、
`records/development/2026-08-05-work5a-first-real-review-acceptance-v2-evidence.md`、
`records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json`、
`records/development/2026-08-05-work5a-provenance-closure-repair-green-evidence-v1.md`、
`records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md`、
`records/development/2026-08-06-work5a-contract-v2-review-acceptance-evidence-v1.md`。
Definition Challengeは`passed`、blocking Finding 0件であり、Contract version 2のReview経路は
11 node・10 edgeのProvenanceとaccepted artifactまで完了した。Codexの独立再確認は関連`83 passed`、
公式全`1007 passed`。Current Work Projectionの正式record写像と、同じTestを変更しないrefactor後再確認は
未完了のまま残す。

上記2項目のdeferをHumanが承認した。Decisionは
`records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md`
（`DEC-WORK5A-PROJECTION-ROUTING-001`）、提案正本は
`docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md`、SHA-256
`c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809`である。

defer理由：現在の正式recordには、Current Work Projectionに必要なStage、開発Work、Work Item、
dependency／cycle、pause／resume、session lifecycle、次作業を権威的に表すrecordがない。現在の
Review Task Contractは一文書reviewの実行経路であり、開発全体の現在位置authorityではない。
このまま部分実装すると、bootstrap eventまたはTODOを第二正本にする、未承認のPortfolio／Work Item／
Workflow state schemaをWork 5Aへ追加する、または欠けたStage・Work・next actionを推測することになり、
第二正本の禁止、小さなE2E縦切り、欠測時fail-closedの方針に反する。

再開条件：少なくとも次が固定された後に再開する。(1) Stage／Work／Work Item identityとstate owner、
(2) Plan、Portfolio、Work Item、Task Contractの型付きrelation、(3) dependency、cycle、pause／resume、
termination、Human decision、staleの正式record、(4) 次の実行可能作業を導出するWorkflow規則、
(5) 欠測、競合、stale、表示器failureを区別するnegative test。再開時もprojectionは派生viewとし、
手編集可能な状態正本、独立status database、UI固有authorityを作らない。

次工程：Current Plan §17の初期実装順11に従い、Work 6Aの中核negative pathをRED fixtureとして固定する。
この承認はWork 6AのGREEN実装、正式projection schema、Portfolio／Work Item schema、UI、automationを
承認しない。Work 5Aの2項目は未完了のまま保持し、段完了にもしない。

## 9. Work 6A：初期sliceのnegative path

- [x] Contract／Requirement／Plan／Context／Provenance欠落を検出する。
- [x] permission過剰、stale、crash、optional観測欠測を区別する。
- [x] validatorの既知違反見逃しと正常例誤停止を検出する。
- [ ] maintenance、reopen、上流改定、dependency、cycle、terminationを検証する。
- [ ] Source Snapshot、Change Set、Test Evidenceの不一致を拒否する。
- [ ] 関数台帳stale、理由なし新規routine、retired routine復活を拒否する。
- [ ] 部分side effect後のcompensation／reconciliation／Human escalation欠落を検出する。
- [x] Current Work Projectionの第二正本化、欠測推測、stale／競合の正常表示を検出する。
- [x] 表示器だけのfailureで有効成果を破棄しないことを確認する。
- [x] Contract適合でも上位Intent／Requirementを損なう成果をFinal Challengeで検出する。
- [ ] 全Test、risk別Verification、post-write verificationを通す。

`Evidence`：完了しているのは6項目（欠落検出、区別、validator検査、第二正本化等の検出、
表示器failure分離、意図毀損検出）である。**Work 6Aの段完了ではない。** 残り5項目のうち、
`CL-6A-04/06/07`は基盤未整備（それぞれ正式Workflow state、Work 4Bの関数台帳、Work 7の外部
side effect）、`CL-6A-05`はChange Set・Test Evidenceの正式artifact未整備、`CL-6A-11`は段の関門で
ある。計画のとおり、これらは対象能力のTask ContractがPortfolioへ入った時点で負例として有効化し、
先行completionをblockしない。

欠落検出・区別・validator検査の3項目の完了は
`DEC-WORK6A-CL-6A-01-02-03-COMPLETION-001`
（`records/development/2026-08-06-work6a-cl-6a-01-02-03-completion-decision-v1.md`）による。
独立検証→残余閉鎖→Human裁定の順を経ており、残余処置の正本は
`records/development/2026-08-06-work6a-inventory-correction-v1.md`。crash後の実地復旧は
Work 7Aへ移管し（選択肢ア）、誤停止率・変異検査の系統的測定はWork 8へ割当て済みである。

3番目の完了は`DEC-WORK6A-CL-6A-10-COMPLETION-001`
（`records/development/2026-08-06-work6a-cl-6a-10-completion-decision-v1.md`）による。
承認済み設計は`docs/design/2026-08-06-final-challenge-intent-damage-proposal.md`、
GREEN Evidenceは`records/development/2026-08-06-intent-damage-green-evidence-v1.md`。
Human採否済みの`intent_damage`所見でContract適合成果を拒否し、未裁定所見ではfail-closed停止する。
所見を生成するLLMレビュー（外部API・サブエージェント経路）は別Task Contractである。

2番目の完了は独立検証（被覆主張を疑う側からの検証）に基づく。承認は
`records/development/2026-08-06-work6a-cl-6a-09-completion-decision-v1.md`
（`DEC-WORK6A-CL-6A-09-COMPLETION-001`）。同じ検証で、被覆済みとされていた他4項目は
部分被覆と判定され、残余の処置（Plan欠落の境界例追加、実在testの引用補充、誤停止側の
緩い読み採用とWork 8への割当て、Change Set／Test Evidenceの保留訂正）は
`records/development/2026-08-06-work6a-inventory-correction-v1.md`を正本とする。

Human承認は`records/development/2026-08-06-work6a-cl-6a-08-completion-decision-v1.md`
（`DEC-WORK6A-CL-6A-08-COMPLETION-001`）。実装範囲の承認は
`records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md`
（`DEC-WORK6A-PROJECTION-GREEN-SCOPE-001`）と
`records/development/2026-08-06-work6a-non-authority-input-scope-decision-v1.md`
（`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001`）である。

RED Evidenceは`records/development/2026-08-06-work6a-projection-negative-red-evidence-v1.md`、
GREEN Evidenceは`records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md`と
`records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md`。
Work 6A項目と既存Testの対応は
`records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`にあり、
checklist 11項目、Plan 28項目を`covered_by_existing_test` 17件、`red_added_now` 2件、
`out_of_approved_scope` 20件へ分類した。RED Evidence §8-2の事実誤りと、改名により陳腐化した
GREEN Evidence v1の記述は`records/development/2026-08-06-work6a-evidence-correction-v1.md`で
訂正し、旧recordは履歴として保持している。

固定したのは`tools/development/session_log_bootstrap.py`の診断判定と表示であり、
正式入力欠落、第二正本化、欠測推測、stale／競合の誤表示をRED先行でTestへ固定してから
実装した。公式全Testは`1017 passed`、fallback `false`。同じTestを弱めていない。

残る限界：拒否対象は上位文書が非authorityと宣言する4 identityの完全一致であり、
名指しのない手編集経路、path表記のゆれ、file名変更後の追随は扱わない。`freshness`の
`unknown`など他の値、固定入力のDigestと実file内容の突き合わせ、入力側へのauthority宣言方式も
扱わない。Current Work Projectionの正式record写像は`DEC-WORK5A-PROJECTION-ROUTING-001`の
再開条件が満たされるまでdeferredである。

## 10. Work 5B：内部Implementation Task Contract Pilot

- [x] ReviewCompass3自身の小さなhelper一件を選定した。
- [x] Contract、red、固定source、Index／Ledger照合を通した。
- [x] Humanの`implementation_ready`判断を記録した。
- [x] Testを弱めずgreen実装、refactor、台帳更新を行った。
- [x] post-write verification、Provenance、分割commitを確認した。
- [x] provisionalな自己適用能力を正式Runtime既定にしていない。

`Evidence`：対象helperは宣言→RED対応表検査器（`tools/development/declaration_red_map_check.py`）。
選定・恒久tool化承認は`DEC-WORK5B-START-001`
（`records/development/2026-08-07-work5b-start-decision-v1.md`）。Contractは
`TC-WORK5B-DECLARATION-RED-MAP-CHECK-001`
（`records/development/2026-08-07-work5b-implementation-task-contract-v1.json`）。台帳（Index／Ledger）は
未整備のため、照合はWork 4B最小試行の再利用検索record＋gate判定
（`records/development/2026-08-07-declaration-red-map-checker-reuse-search-v1.json`、
`start_allowed: true`）で代替した（`DEC-WORK4A-EARLY-EXIT-001`の境界どおり）。
`implementation_ready`は設計議論の終了を条件とするHuman承認により成立
（`DEC-WORK5B-IMPLEMENTATION-READY-001`、議論証跡は`DEC-WORK5B-DISCUSSION-OUTCOMES-001`）。
REDは`records/development/2026-08-07-work5b-red-map-checker-red-evidence-v1.md`（宣言C1〜C4、
testの無い宣言0件）、GREENと第一実運用は
`records/development/2026-08-07-work5b-checker-green-evidence-v1.md`と
`records/development/2026-08-07-work5b-checker-first-run-v1.json`（4枚中3枚passed、自己検査passed、
Intake V4対応表に実在所見2件——処置はHuman判断待ち）。公式全Testは`1066 passed`、fallback `false`。
4番目の項目は当初、台帳未整備のため未完了とした（defer：`DEC-WORK5B-LEDGER-ITEM-DEFER-001`）。
2026-08-07に既存台帳経路の再利用（`DEC-WORK4B-D-LEDGER-REUSE-001`）でBaseline v1が整備され、
helper 2件のEntry 8件をHuman裁定（`DEC-RRL-HELPER-ENTRIES-001`、全件`as_is`）つきで記録して
完了へ戻した。Evidenceは
`records/development/2026-08-07-work4b-d-ledger-first-operation-evidence-v1.md`。
2026-08-07、全6項目のEvidence接続を前提にHumanがWork 5Bの**段完了を承認した**
（`DEC-FOUR-RULINGS-2026-08-07-001`裁定3）。Work 5Bは`verified / completed`である。

## 11. Work 7A：`local_integrated` deployment E2E

- [ ] install、project、runtime、sensitiveの各rootを分離した。
- [ ] 別checkoutとproject移動後にBinding、Snapshot、Change Setを復元できる。
- [ ] Control／Executionのstructured I/Oとstate ownerを確認した。
- [ ] worker停止後にcheckpointから再開し、side effectを重複させない。
- [ ] stableとdevelopmentのstate／dataを分離し、cross-writeを拒否する。
- [ ] Project Artifacts更新がRuntime Core再installを要求しない。
- [ ] Current Work Projectionが別rootと再開後も同じauthorityから再生成できる。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 12. Work 8：Evaluation Pilot

- [ ] 既存方式とTask Contract方式を同じ対象、source、model、Tool、budgetで比較した。
- [ ] 変更規模比例review、affected-test selection、Index増分更新を比較した。
- [ ] Evidence Coverage、Finding品質、lead time、費用、再作業、欠測を記録した。
- [ ] Issue Resolution Pathと共通routine照合を手作業Pilotした。
- [ ] Current Work Projectionあり／なしで状況復元時間と参照artifact数を比較した。
- [ ] Stage／Work、active作業、blocker、Human判断待ち、stale、次作業の正確性を確認した。
- [ ] 誤表示、古い表示、欠測・不整合検出、event記録負担を測定した。
- [ ] text／machine-readable projectionの実測から、画面UI着手の必要性をHuman判断へ渡した。
- [ ] 速度や入力削減だけを成功とせず、安全性と再生成一致を確認した。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 13. Work 8A：`bounded_parallel` Pilot（条件付き）

- [ ] Work 8の開始条件評価で、安全性と効果が確認された。
- [ ] 実施しない場合、理由とEvidenceをDeferred Workへ記録した。
- [ ] 実施する場合、単一project、low risk、`max_parallel: 2`、Human判断に限定した。
- [ ] conflict domain、owner／lease、固定source、checkpoint、直列fallbackを確認した。
- [ ] merge後のstale、Test、Integration Verdict、Current Work Projectionを確認した。
- [ ] 成功しても初期既定policyへ自動昇格していない。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 14. Work 7B：lifecycle deployment E2E

- [ ] update、migration dry-run、staging、原子的切替を確認した。
- [ ] uninstall、rollback、crash復旧を確認した。
- [ ] Layout変更時にlink migrationと旧配置からの復旧を確認した。
- [ ] Build ArtifactをSource Snapshot、build Run、Verification、Digestへ束縛した。
- [ ] lifecycle操作の前後でCurrent Work Projectionを再生成できる。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 15. Stage G：Release Evaluation

- [ ] 固定Source Snapshotで全Testを実行した。
- [ ] 必須deployment／migration verificationを実行した。
- [ ] 全Task ContractのConformanceとIntegration Verdictを確認した。
- [ ] Provenance完全性、未解決Finding、stale、known riskを確認した。
- [ ] stable candidateをdevelopment candidate自身だけで判定していない。
- [ ] release、defer、accept-with-known-riskまたは中止をHumanが判断した。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 16. 初期範囲へ前倒ししないもの

- [ ] As-Built projection
- [ ] AIへの判断委譲
- [ ] shared／distributed deployment
- [ ] Issue Resolution automation
- [ ] 改善候補の製品schema、正式state machine、permit連携、自動Plan編集
- [ ] 汎用Task Registry、plugin system、任意Agent orchestration
- [ ] Current Work Projectionの画面UI、通知、複数project dashboard
- [ ] 必要性を実測していないGraphRAGまたは高度な意味検索

上記checkboxは「実装完了」ではなく、「初期範囲へ入れていないこと」の確認に使う。

## 17. 中断、上流改定、再開

### 改善候補の受付とroute

- [ ] 新しい問題またはアイデアを、発生元Work、固定source、Evidenceを持つ改善候補
      （`improvement_candidate`）へ記録した。
- [ ] 実装、Test／oracle、Contract、Requirement、Intent、外部blocker、process改善、product ideaの
      分類候補を記録した。
- [ ] 必須field、identity、Digest、freshness、重複候補を検査した。
- [ ] safety、authority、Acceptanceの真偽、必須Provenance、source一致、不可逆side effectへの影響を確認した。
- [ ] blocking候補は`pause_and_triage`、非blocking候補はcheckpoint queueをroute候補とした。
- [ ] 機械またはAIのrouteを提案として扱い、Plan、Requirement、Contract、Testを自動変更していない。
- [ ] Humanがcurrent Work、Upstream Revision、Dependency、Issue Resolution、checkpoint queue、defer、
      reject、duplicateのrouteを判断した。
- [ ] 採用候補をconsumerとOutcomeへ接続し、record作成だけでclosedにしていない。

詳細な分類、決定表、機械化の境界は
[手作業自己適用からの改善候補を計画改定へ送る経路の検討メモ](../design/2026-08-03-self-application-improvement-routing-memo.md)
を参照する。

### 中断、改定、再開

- [ ] 問題を実装不良、Contract不良、Requirement不良、Intent競合、外部blockerへ分類した。
- [ ] 必要な最下位上流層へRevision Proposalを送った。
- [ ] 現行Workをpause、cancel、replace、close-scopeのいずれかで扱った。
- [ ] 部分成果、side effect、cleanup、rollback、未処理、移管先を記録した。
- [ ] 影響を受けるTest、Verdict、projection、checklist項目をstaleにした。
- [ ] 改定後のContract、Plan、Context、checkpointを再確認してから再開した。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）

## 18. チェックリスト自身の改定

- [ ] 改定理由と利用中に見つかった不足を記録した。
- [ ] Intent、用語集、計画の参照Digestを再確認した。
- [ ] 追加項目を既存ownerへ割り当て、新しい大域Stageを安易に増やしていない。
- [ ] 削除項目が持っていた停止、復旧、Evidence、後継Testを失っていない。
- [ ] Humanが新しい順序と適用開始を判断した。

`Evidence`：[改定r1 record](../../records/development/2026-08-08-checklist-revision-r1-record-v1.md)（2026-08-08。Work 4B追随・Work 1B後続追加・Digest8件一致確認）
