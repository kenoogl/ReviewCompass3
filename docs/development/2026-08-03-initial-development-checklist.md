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

- [ ] 利用者から開発着手の指示がある。
- [ ] 本チェックリストを当面の進行入口として確認している。

### 確認項目

- [ ] Intent、統合用語集、現行計画の対象versionとDigestを固定した。
- [ ] 既存baseline、前身Evidence、未コミット変更を列挙した。
- [ ] 今回のsource universe、対象、非対象、confidentialityを定めた。
- [ ] 初期scopeとDeferred Workを確認した。
- [ ] 未承認事項、既知Finding、必要なHuman判断を列挙した。
- [ ] Evidence Extraction ContractとConsumption Closureの最小運用を定めた。
- [ ] 固定入力が変わった場合のstale化と再開入口を定めた。

### 完了関門

- [ ] 固定入力、scope、非目標、未解決事項を一つのEvidenceから確認できる。
- [ ] blockingなIntent／Requirement／Plan競合がない、または停止理由が明示されている。

`Evidence`：未記録

## 4. Work 1A：Layout Baseline

### 確認項目

- [ ] `CODE_ROOT`、`CONFIG_ROOT`、`PROJECT_ROOT`、`DATA_ROOT`、`STATE_ROOT`、`LOG_ROOT`、
      `CACHE_ROOT`、`SENSITIVE_ROOT`、`EVALUATION_ROOT`の意味と解決規則を固定した。
- [ ] Git管理対象、project外data、機密data、生成物、cacheの境界を固定した。
- [ ] Project ManifestとProject Bindingの最小構造を定めた。
- [ ] stableとdevelopmentのroot、state、data、cross-write禁止を定めた。
- [ ] 空配置fixtureを作り、別checkoutとproject移動後の相対参照を確認した。
- [ ] 端末固有絶対pathが管理成果へ混入しないことを確認した。
- [ ] 後続の配置変更を通常編集でなくmigrationとして扱う規則を定めた。

### 完了関門

- [ ] Layout Baseline Recordと空配置Testが固定されている。
- [ ] project移動、link解決、Manifest／Binding照合がgreenである。

`Evidence`：未記録

## 5. Work 1B：Session Log Bootstrapと現在位置text表示

### Session Evidence

- [ ] session ID、source identity、取得範囲、時刻、Digest、完全性を記録できる。
- [ ] rawを`SENSITIVE_ROOT`、伏字化派生物・要約・索引を`DATA_ROOT`へ分離した。
- [ ] confidentiality、access、retention、capture deadline、source availabilityを定めた。
- [ ] `source_missing | source_expired | non_reconstructable`を正常な空記録と区別した。
- [ ] rawから派生物を再生成し、Digestを照合するrestore fixtureを確認した。

### bootstrap現在位置プロジェクション

- [ ] Work開始／完了、pause／resume、blocker発生／解消を記録できる。
- [ ] Human判断要求／決定、upstream revision、stale／再検証を記録できる。
- [ ] cancel／defer、session開始／終了を記録できる。
- [ ] 固定入力から同じstructured projectionを決定的に生成できる。
- [ ] 全体Stage／Work、active作業、TDD状態、次作業、blocker、Human判断待ち、staleをtext表示できる。
- [ ] session開始用の短縮表示と、調査用の詳細表示を生成できる。
- [ ] 入力identity、Digest、生成時刻、freshnessを表示できる。
- [ ] 欠測または競合を推測で埋めず、不完全または不整合として詳細表示できる。
- [ ] 手編集する`STATUS.md`、第二の状態台帳、WebUI、常駐serviceを作っていない。
- [ ] 表示器だけのfailureとWorkflow authority欠落を区別できる。

### 完了関門

- [ ] Work 2以降のsessionと主要状態変化を失わず記録できる。
- [ ] 現在位置のtext表示をsession開始・終了で実際に使用できる。
- [ ] bootstrap toolingを作成した場合、固定fixture、red確認、関連Test、全Testがgreenである。

`Evidence`：未記録

## 6. Work 2〜4：上流文書、Requirements、最初のslice設計

### Work 2：Intentと用語

- [ ] Intent、利用者、非目標、Human／AI／機械のauthority境界をHuman判断候補として固定した。
- [ ] 新しいdomain用語を統合用語集へ登録した。

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
