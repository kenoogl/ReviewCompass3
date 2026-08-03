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
    sha256: 0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f
operational_policy:
  path: docs/development/2026-08-02-development-policy.md
  sha256: a094926a5c9f981cdb1997b4a8e205da9a333fda51f2876b47e76d53fcf7dc1c
policy_decision:
  path: records/development/development-policy-v4.json
  sha256: 87bd0460bce3ae471a598ae5ab2964d05e6ceb97701870f25b5cc9110133f24a
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
- [ ] TODOへ過去sessionを累積せず、現行handoffを短時間で読める量に保った。

`Evidence`：未記録

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

- [ ] 既存37要件と追加13要件の順逆被覆、owner、停止、復旧、受入、対象外を確認した。
- [ ] source、Change Set、Test／CI／Build Artifactのidentityとstale規則を確認した。
- [ ] 必須非機能義務をVerification Profileへ接続した。
- [ ] deferred候補を初期Requirementの暗黙依存にしていない。

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

`Evidence`：未記録

## 7. Work 4A：関数台帳baseline

- [ ] 固定Source Snapshotとsymbol identity規則を確定した。
- [ ] 全関数・methodをSource Symbol Indexへ機械収録した。
- [ ] coverage、freshness、再生成一致を確認した。
- [ ] public、共有、cross-contract、high-risk、重複候補、retiredを抽出した。
- [ ] 対象routineをReusable Routine Ledgerへ登録した。
- [ ] 今回の実装候補を`reuse | extend | merge | split_with_rationale`へ分類した。
- [ ] Humanが生成規則、coverage、代表sample、重複、retiredを確認した。

### 完了関門

- [ ] 配置、Index、Ledger、実codeが照合済みである。
- [ ] 最初のImplementation Task Contractへ`implementation_ready`を出せる前提が揃っている。

`Evidence`：未記録

## 8. Work 5A：最小Review Task Contractの定義とhappy path

### Contractとred

- [ ] 一種類のReview Task Contractを固定Requirementから定義した。
- [ ] Responsibility、Boundary、Context、Capability、Output、Acceptance、Provenance、Escalationを定めた。
- [ ] Definition Challengeを通し、Contractの粒度と依存を確認した。
- [ ] Acceptance Testとnegative fixtureを先に作成した。
- [ ] 実装がなければ期待理由で失敗するredを確認した。

### green実装

- [ ] 最小schemaとvalidatorを実装した。
- [ ] 一Contractから一Plan bundleと6 typed viewを生成した。
- [ ] Context Manifest、Workflow permit、Harness stub、Traceを接続した。
- [ ] deterministic stub reviewerからConformanceとFinal Challengeを生成した。
- [ ] Human decision、Decision Record、Provenance verdict、accepted artifactを接続した。
- [ ] read-only local GitのSource SnapshotとChange Setを接続した。
- [ ] bootstrap Current Work Projectionを正式recordへ写像し、textとmachine-readable出力の同値を確認した。
- [ ] 同じTestを変更せずgreenにし、refactor後も再確認した。

### 完了関門

- [ ] Requirementからaccepted artifactまで一つのE2Eがgreenである。
- [ ] 汎用DSL、plugin、任意Task orchestration、画面UIを実装していない。

`Evidence`：未記録

## 9. Work 6A：初期sliceのnegative path

- [ ] Contract／Requirement／Plan／Context／Provenance欠落を検出する。
- [ ] permission過剰、stale、crash、optional観測欠測を区別する。
- [ ] validatorの既知違反見逃しと正常例誤停止を検出する。
- [ ] maintenance、reopen、上流改定、dependency、cycle、terminationを検証する。
- [ ] Source Snapshot、Change Set、Test Evidenceの不一致を拒否する。
- [ ] 関数台帳stale、理由なし新規routine、retired routine復活を拒否する。
- [ ] 部分side effect後のcompensation／reconciliation／Human escalation欠落を検出する。
- [ ] Current Work Projectionの第二正本化、欠測推測、stale／競合の正常表示を検出する。
- [ ] 表示器だけのfailureで有効成果を破棄しないことを確認する。
- [ ] Contract適合でも上位Intent／Requirementを損なう成果をFinal Challengeで検出する。
- [ ] 全Test、risk別Verification、post-write verificationを通す。

`Evidence`：未記録

## 10. Work 5B：内部Implementation Task Contract Pilot

- [ ] ReviewCompass3自身の小さなhelper一件を選定した。
- [ ] Contract、red、固定source、Index／Ledger照合を通した。
- [ ] Humanの`implementation_ready`判断を記録した。
- [ ] Testを弱めずgreen実装、refactor、台帳更新を行った。
- [ ] post-write verification、Provenance、分割commitを確認した。
- [ ] provisionalな自己適用能力を正式Runtime既定にしていない。

`Evidence`：未記録

## 11. Work 7A：`local_integrated` deployment E2E

- [ ] install、project、runtime、sensitiveの各rootを分離した。
- [ ] 別checkoutとproject移動後にBinding、Snapshot、Change Setを復元できる。
- [ ] Control／Executionのstructured I/Oとstate ownerを確認した。
- [ ] worker停止後にcheckpointから再開し、side effectを重複させない。
- [ ] stableとdevelopmentのstate／dataを分離し、cross-writeを拒否する。
- [ ] Project Artifacts更新がRuntime Core再installを要求しない。
- [ ] Current Work Projectionが別rootと再開後も同じauthorityから再生成できる。

`Evidence`：未記録

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

`Evidence`：未記録

## 13. Work 8A：`bounded_parallel` Pilot（条件付き）

- [ ] Work 8の開始条件評価で、安全性と効果が確認された。
- [ ] 実施しない場合、理由とEvidenceをDeferred Workへ記録した。
- [ ] 実施する場合、単一project、low risk、`max_parallel: 2`、Human判断に限定した。
- [ ] conflict domain、owner／lease、固定source、checkpoint、直列fallbackを確認した。
- [ ] merge後のstale、Test、Integration Verdict、Current Work Projectionを確認した。
- [ ] 成功しても初期既定policyへ自動昇格していない。

`Evidence`：未記録

## 14. Work 7B：lifecycle deployment E2E

- [ ] update、migration dry-run、staging、原子的切替を確認した。
- [ ] uninstall、rollback、crash復旧を確認した。
- [ ] Layout変更時にlink migrationと旧配置からの復旧を確認した。
- [ ] Build ArtifactをSource Snapshot、build Run、Verification、Digestへ束縛した。
- [ ] lifecycle操作の前後でCurrent Work Projectionを再生成できる。

`Evidence`：未記録

## 15. Stage G：Release Evaluation

- [ ] 固定Source Snapshotで全Testを実行した。
- [ ] 必須deployment／migration verificationを実行した。
- [ ] 全Task ContractのConformanceとIntegration Verdictを確認した。
- [ ] Provenance完全性、未解決Finding、stale、known riskを確認した。
- [ ] stable candidateをdevelopment candidate自身だけで判定していない。
- [ ] release、defer、accept-with-known-riskまたは中止をHumanが判断した。

`Evidence`：未記録

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

`Evidence`：未記録

## 18. チェックリスト自身の改定

- [ ] 改定理由と利用中に見つかった不足を記録した。
- [ ] Intent、用語集、計画の参照Digestを再確認した。
- [ ] 追加項目を既存ownerへ割り当て、新しい大域Stageを安易に増やしていない。
- [ ] 削除項目が持っていた停止、復旧、Evidence、後継Testを失っていない。
- [ ] Humanが新しい順序と適用開始を判断した。

`Evidence`：未記録
