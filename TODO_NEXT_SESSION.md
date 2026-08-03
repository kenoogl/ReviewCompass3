# TODO_NEXT_SESSION

更新日：2026-08-03
用途：session更新・次sessionへの引き継ぎ

> 本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない。
> 過去sessionを累積せず、固定Plan、checklist、Git、Test、Decision、Provenanceをリンクして使う。

## 現在位置

- 全体：初期開発Work 1BとWork 2完了
- 現在の工程：Work 3 Requirements開始待ち
- activeなTask Contract／Work Item：正式Task Contractなし。activeなWork Itemなし
- 製品実装code：capture、projection、text、durable writer、E2E orchestration、完了NEXT遷移を実装
- 当面の進行入口：`docs/development/2026-08-03-initial-development-checklist.md`
- 進行入口SHA-256：`253bcf43c5e492d47c34e4cc505670ae69b56d21496014af85fb301c918d9d45`
- 現行計画：`docs/current/reviewcompass3-plan-current.md`
- 現行計画SHA-256：`0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f`
- 現行開発方針：`docs/development/2026-08-02-development-policy.md`
- 現行開発方針SHA-256：`a094926a5c9f981cdb1997b4a8e205da9a333fda51f2876b47e76d53fcf7dc1c`
- 直近のDecision／Evidence：`records/development/2026-08-03-work-2-completion-evidence-v1.md`
- Decision／Evidence SHA-256：`8a5f42dbde5d3b79ae2b200746e46f441cf07219a8ff5836fbf749d6563442d2`

## 実施報告照合

### verified

- Claim `EC-019`：raw／派生物root分離、source availability、restore、主要状態event、短縮／詳細表示、
  欠測／競合を13個の固定fixtureと7件のAcceptance Testへ固定した。
  - Evidence：`tests/test_session_log_bootstrap.py`、SHA-256
    `7b7f46b2c5df5de55032eb311632cafc10b885399ad00d3d8ff7f8ec714aa685`、fixture inventory SHA-256
    `7b713d65afffa3267954b42eb028e37b17906681ddc1570bc2deebc0f76e50e3`
  - 観測した事後状態：Test sourceを`compile()`、JSON／JSONLを再読込し、固定fixture 13 fileを確認した。
- Claim `EC-020`：Work 1B Testがbootstrap mapping未実装を期待理由としてredになることを確認した。
  - Evidence：`records/development/2026-08-03-work-1b-red-evidence-v1.md`、SHA-256
    `079277ae1f3f1c5277672d2ad24e4e1650983c0e0fc3eec5da4ee6f56d79604a`
  - 観測した事後状態：targeted `7 failed`、全Test `419 passed, 7 failed`。失敗7件は全件
    `ModuleNotFoundError: tools.development.session_log_bootstrap`だった。
- Claim `EC-021`：raw、3派生物、workflow event、projection inputの固定Digestが相互に一致することを確認した。
  - Evidence：capture profile raw SHA-256
    `461d29923f1b3c5ac5926458c469620ce1f945a863daab86b120de3a36d8db23`、workflow event SHA-256
    `8009712a3c673e935aa60434839acc104bae6ab606638538f172df1d43c4b024`
  - 観測した事後状態：独立fixture integrity commandが`fixture_integrity: passed`を返した。
- Claim `EC-022`：固定Testを変更せず、保存先mapping、availability、restore、projection、text rendererの
  最小実装を追加した。
  - Evidence：`tools/development/session_log_bootstrap.py`、SHA-256
    `eeacccb8635820ef4e15a7e7dd7b47a973096727830c8637092b06198e0b9fa8`
  - 観測した事後状態：実装を再読込し、`compile()`が`compile_ok`、固定Test SHA-256がred時点と一致した。
- Claim `EC-023`：Work 1B targeted Testと全Testをgreenにした。
  - Evidence：`records/development/2026-08-03-work-1b-green-evidence-v1.md`、SHA-256
    `fdaeeb439226c6e86b17b8aa33e0e11fbdc64512ccd3b2c3f9a14f0970e169b9`
  - 観測した事後状態：targeted `7 passed`、全`426 passed`を確認した。
- Claim `EC-024`：durable captureの正常保存、再読込、Digest不一致、既存file衝突、部分書込みrollbackを
  独立fixture 1件とAcceptance Test 4件へ固定した。
  - Evidence：`tests/test_session_log_durable_capture.py`、SHA-256
    `36aab68bcc65966f20ac04e8d2f1f20ec527629020b5c3fef1cd4b776359366e`、expected Session Evidence
    SHA-256 `bc98331a48667ec3799ba2533710db080601ed1b829a2afcf0b2b78809d15906`
  - 観測した事後状態：Test `compile_ok`、fixture JSON再読込、managed absolute path finding 0件を確認した。
- Claim `EC-025`：durable capture Testがwriter API未実装だけを理由としてredになることを確認した。
  - Evidence：`records/development/2026-08-03-work-1b-durable-capture-red-evidence-v1.md`、SHA-256
    `a25c7cfde5817ff35375b07087e740820a7080b67bec8b6921fac167eb5e862d`
  - 観測した事後状態：targeted `4 failed`、全Test `426 passed, 4 failed`。失敗4件は全件
    `AttributeError: persist_session_capture`だった。
- Claim `EC-026`：固定durable Testを変更せず、write前検証、保存、再読込、衝突拒否、rollbackを実装した。
  - Evidence：`tools/development/session_log_bootstrap.py`、SHA-256
    `fd2b286e2d0d72a05eb1f4f0cc0f19650eb41a4c9d2e7921eb9b61b374066339`
  - 観測した事後状態：実装を再読込し`compile_ok`、durable TestとfixtureのDigestがred時点と一致した。
- Claim `EC-027`：durable、bootstrap、全Testをgreenにした。
  - Evidence：`records/development/2026-08-03-work-1b-durable-capture-green-evidence-v1.md`、SHA-256
    `7ab01e1a106c6d8cb2711f1b8bc4df150d34761d94c7d0f13f033332783f2f22`
  - 観測した事後状態：durable `4 passed`、bootstrap `7 passed`、関連`11 passed`、全`430 passed`。
- Claim `EC-028`：session開始／終了のcapture、再読込、projection、text、display／authority failure分離を
  fixture 10件とE2E Test 4件へ固定した。
  - Evidence：`tests/test_session_bootstrap_e2e.py`、SHA-256
    `ca4486fb43b3e5f4bd32175b0e177efb1a8612c08e2b43edaa98206e453eaedb`、fixture inventory SHA-256
    `0c3fad4328c9e151e18e44aff06699043cde555e0c6807af32e5496f1b58a837`
  - 観測した事後状態：`e2e_fixture_integrity=passed`、managed absolute path finding 0件を確認した。
- Claim `EC-029`：E2E Testがorchestration API未実装だけを理由としてredになることを確認した。
  - Evidence：`records/development/2026-08-03-work-1b-session-e2e-red-evidence-v1.md`、SHA-256
    `84cf75898883b73d4db996dbcdf465ada0a6a8b2375551c866d6a22a3e3429ab`
  - 観測した事後状態：targeted `4 failed`、全Test `430 passed, 4 failed`。失敗4件は全件
    `AttributeError: run_session_bootstrap`だった。
- Claim `EC-030`：固定E2E Testを変更せず、durable保存後のraw再読込、projection、text、
  authority／display状態分離を実装した。
  - Evidence：`tools/development/session_log_bootstrap.py`、SHA-256
    `5ce2f77d671d48c8627cc3072a1b2111a4fc4ef615f3454d7b353d3b9ad2ac97`
  - 観測した事後状態：実装`compile_ok`、E2E Test、fixture、red EvidenceのDigestがred時点と一致した。
- Claim `EC-031`：E2E、関連、全Testをgreenにした。
  - Evidence：`records/development/2026-08-03-work-1b-session-e2e-green-evidence-v1.md`、SHA-256
    `b3ec1686d6caeaba6f745a3ec355a24152e42572c77a451c06343d6ffa013e84`
  - 観測した事後状態：E2E `4 passed`、関連`15 passed`、全`434 passed`を確認した。
- Claim `EC-032`：実使用sessionの開始eventからshort textを生成し、開始表示として使用した。
  - Evidence：operational session event prefix Digest
    `7751abc44b0b34163e32105503f5bf23e758234a89fae6e1f099ffe587733611`、start display receipt SHA-256
    `4bda609bf80d345ee82f92730a700c5691cba5cc7c2d5e566a570e3f2486f051`
  - 観測した事後状態：short textがWork 1B `active`、blocker 0、decision 0、次actionを表示した。
- Claim `EC-033`：完成event streamをdurable captureし、保存後再読込と終了detailed text表示を実施した。
  - Evidence：operational event Digest
    `900811d92d60854d6bc50ffdf53bd3a91dbf201a9309212bcc5c49f0602e5d5d`、Session Evidence SHA-256
    `2f4ffa1941faad3320d19ee98c59689a35c34478cef7470d13bdfaf81291d7a3`、end display receipt SHA-256
    `62e692e5ef9eb142c377991eaa16cac89c4334c5facb17d08586cae7565556c8`
  - 観測した事後状態：rawと保存raw、3派生物Digest、Plan／event input、generated_at、freshnessを再照合した。
- Claim `EC-034`：終了表示で`state: completed`と消費済みNEXTが同時に残る不整合を検出し、完了判断を停止した。
  - Evidence：`records/development/2026-08-03-work-1b-completed-next-candidate.md`、SHA-256
    `8a36ceffdfe8da4289cc0728b7b34b5a95588140b0b2a5a0580787e83d3a71f4`
  - 観測した事後状態：保存後再読込commandが
    `projection_mismatch: completed_with_consumed_next_action`を返し、全Testは`434 passed`だった。
- Claim `EC-035`：Humanが選択肢1を選び、完了eventのNEXT必須・旧NEXT置換・欠落時`incomplete`を承認した。
  - Decision：`records/development/2026-08-03-work-1b-completed-next-decision.json`、SHA-256
    `ba70d88a9a9a023954b9879c7658c788fd8984663e6cc5a93085051b8fdab273`
  - 観測した事後状態：候補を`current_work_repair`へrouteし、Work 1B段完了は未承認として固定した。
- Claim `EC-036`：完了NEXT遷移を2件の回帰Testへ固定し、修正前REDを確認した。
  - Evidence：`records/development/2026-08-03-work-1b-completed-next-red-evidence-v1.md`、SHA-256
    `00c0b86eba28c5c4351ccf332a06a4e3fda33dd2b955dff5febbac6d09056f0a`
  - 観測した事後状態：旧NEXT残留と必須NEXT欠落未検出により`2 failed in 0.02s`となった。
- Claim `EC-037`：projectionを修正し、完了NEXT置換と欠落時`incomplete`を実装した。
  - Evidence：`records/development/2026-08-03-work-1b-completed-next-green-evidence-v1.md`、SHA-256
    `03541809e7f57cdc80308ad7eb1ab6f2e4b20a7d487263eaa32219257d031afb`
  - 観測した事後状態：関連`17 passed in 0.07s`、全`436 passed in 1.85s`を確認した。
- Claim `EC-038`：別の外部development rootで開始／終了表示とdurable captureを再実行した。
  - Evidence：operational raw SHA-256
    `85ca5e12cb0b2d0ebedd43730ae4a43ff9c175f55b2cae4030e7bf6d9b3535d6`、Session Evidence SHA-256
    `75e1de2ff8415687dbbea15943c98e12261de276a4c61d2b34e0ea631011b357`、end receipt SHA-256
    `84d4be22b372ab24bb957ce9caf434338fd7bb8b1dcc24a87206456a1623ecba`
  - 観測した事後状態：終了表示は`completed`、active workなし、NEXTはHuman完了承認依頼となり、
    source／保存raw byte一致と4 artifactのDigest一致を独立再確認した。
- Claim `EC-039`：Work 1Bの全技術的完了関門をEvidenceへ接続した。
  - Evidence：`records/development/2026-08-03-work-1b-completion-candidate-v1.md`、SHA-256
    `cb48778b36bf1d26673f753a91f97faf25c13a8d738d9193e4e23d9e4497d03d`
  - 観測した事後状態：技術的完了関門を満たした候補へHuman完了承認を接続し、`completed`へ更新した。
- Claim `EC-040`：HumanがWork 1Bの段完了を明示承認した。
  - Decision：`records/development/2026-08-03-work-1b-completion-decision.json`、SHA-256
    `69b4f792e3ccf529af338bce08e46ec2dace77ba86b5e4df624ff4b399e63ac8`
  - 観測した事後状態：checklistはWork 1B `verified / completed`、次の未完了工程はWork 2となった。
- Claim `EC-041`：Work 2の現行Intent、統合用語集、PlanをWork 1 corrective snapshotへ再照合した。
  - Evidence：Intent SHA-256
    `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6`、用語集SHA-256
    `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa`、Plan SHA-256
    `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f`
  - 観測した事後状態：Plan current refsとsnapshot commit `ee60e3b`の3 Digestが一致した。
- Claim `EC-042`：Intent、利用者、非目標、authority境界と統合用語をHuman判断候補へ固定した。
  - Evidence：`records/development/2026-08-03-work-2-intent-glossary-candidate-v1.md`、SHA-256
    `2666511bcf95a2fdc5237257b5c5e38fbc7dc1c80fd829064b02e34b759e6ab9`
  - 観測した事後状態：Intent必須8節、authority境界3件、canonical token 109件、必須13語、
    旧語読み替え8件を確認し、欠落・重複0、追加本文差分0だった。
- Claim `EC-043`：Work 2のHuman判断待ち状態をSession Log Bootstrapでdurable captureした。
  - Evidence：operational raw SHA-256
    `7cc254470abd013b94df534cf4bea7b94394b4590154da746091a37171ae4277`、Session Evidence SHA-256
    `456c9071781d5bbcddadd6cb2fa181274ba1930e34c5903c18eb96066719e5c6`
  - 観測した事後状態：projectionは`paused`、Human判断1件、blocker／staleなし、次actionは候補判断となり、
    保存後rawと3派生物のDigest一致を確認した。
- Claim `EC-044`：post-write確認でWork 2候補の生成時刻不整合を検出し、完了判断を停止した。
  - Evidence：`records/development/2026-08-03-work-2-candidate-timestamp-improvement.md`、SHA-256
    `6d0f4722a2aa926b638384ee58789be0fce6f4b617932c2c2a2c3d744c5357c5`
  - 観測した事後状態：candidate `generated_at`は`14:35:03`、Work 2 session開始は`14:56:34`であり、
    Work 2 checklist項目を未完了へ戻して`pause_and_triage`とした。
- Claim `EC-045`：Human選択肢1に従い、候補生成時刻を訂正して同じ内容監査を再実行した。
  - Decision：`records/development/2026-08-03-work-2-candidate-timestamp-decision.json`、SHA-256
    `9dcc7570d80bde8711049c688e5f03ec4a607457a96179fd146c512c288f271a`
  - Evidence：`records/development/2026-08-03-work-2-candidate-timestamp-repair-evidence-v1.md`、SHA-256
    `d1fb1e1f6f2ad0c794fdf36d74fa188ef068753a10f3e71c8428bf39a6c25ad0`
  - 観測した事後状態：候補SHA-256は
    `bfec3b29cf8ebb5ffeedc349e39b2215922ebef8e4105a258e73279a7226a252`となり、Intent 8節、authority
    3境界、canonical token 109件、必須13語、欠落・重複0の監査が再合格した。
- Claim `EC-046`：session `002`で旧候補stale、新候補reverified、新Digestへの判断要求を保存した。
  - Evidence：raw SHA-256 `71346c1f6689fc686d1e26debb6d3572d12854f1859aaa53799f74b7c7af7cae`、
    Session Evidence SHA-256 `9af96cd068b61a093b4f7068bfd7e553b3bdc475d3ba87f93771434700ae340a`
  - 観測した事後状態：保存後rawと3派生物Digestが一致し、projectionは`paused`、Human判断1件、
    blocker／staleなし、authority `valid`、display `rendered`だった。
- Claim `EC-047`：Humanが選択肢1として訂正済みIntent／統合用語集候補を承認した。
  - Decision：`records/development/2026-08-03-work-2-intent-glossary-approval.json`、SHA-256
    `068ff06132dfcd24685d4a626d9107cf65b37456eebcd567dc72b9f6b27c7b78`
  - 観測した事後状態：候補、Intent、用語集のDigestへ承認を束縛し、現行Planはprovisionalのままとした。
- Claim `EC-048`：promotion状態変更後のWork 1固定入力をEvidence v3で再検証した。
  - Evidence：`records/development/2026-08-03-work-1-fixed-input-evidence-v3.md`、SHA-256
    `334f7aeee44f65ee953d13f1737d08e24c38a4b2356aff26e3f7d4accec60d8a`
  - 観測した事後状態：snapshot 13 artifact、承認対象2文書、Plan参照が一致し、内容Digestの変更は0だった。
- Claim `EC-049`：Work 2完了状態をsession `003`へdurable captureした。
  - Evidence：raw SHA-256 `52f7487d6321b7fc37751ff9b96cfacf97f515d0a5f41960ea3637ba1cfcf7e9`、
    Session Evidence SHA-256 `341911fda7e7ac25c210c389c1e8fd33d9bed0117d7eecfb13e91a12b1726cb3`
  - 観測した事後状態：projectionは`completed`、active work／Human判断／staleなし、次actionはWork 3だった。
- Claim `EC-050`：Approval、再検証、session captureをWork 2完了Evidenceへ接続した。
  - Evidence：`records/development/2026-08-03-work-2-completion-evidence-v1.md`、SHA-256
    `8a5f42dbde5d3b79ae2b200746e46f441cf07219a8ff5836fbf749d6563442d2`
  - 観測した事後状態：Work 2は`verified / completed`、次の未完了工程はWork 3となった。

### reported_unverified／contradicted

- `report_execution_mismatch`：Work 2を`verified / human_decision_pending`とした報告は、candidateの
  `generated_at`が事後状態と一致しないため無効だった。`EC-045`と`EC-046`で修復し、旧candidate Digestと
  session `001`をsuperseded、新candidateとsession `002`をcurrentとして閉じた。

### 未実施

- Work 3着手
- platform別OS標準rootの具体解決とProject Bindingのdurable保存
- 実施報告照合の自動Claim抽出、Provenance対応、完了state結線

### 残余risk

- operational保存物はproject外の一時development rootにあり、Completion CandidateへidentityとDigestを固定した。
- Layout validatorはWork 1A固定規則のbootstrap oracleであり、正式製品Runtimeではない。
- documentation revision v16は`digest-only`の履歴として残るが、現行固定入力とWork 1A Evidenceは
  Gitから再構築可能である。
- Intent／用語集候補のfrontmatterはpromotion前snapshotである。現行authorityは外部Approval Decisionと
  承認対象Digestであり、候補fileを第二正本にはしない。
- session `001`と旧candidate Digestは問題発生Evidenceとして保持し、current判断関門には使用しない。

## 次に行う一作業

Work 3 Requirementsの固定sourceと被覆baselineを確認する。

開始条件：

- Work 2 Approval Decision、Work 1固定入力Evidence v3、Work 2 Completion EvidenceのidentityとDigestが一致する。
- Work 2は`verified / completed`で、現行Planはprovisionalとして明示されている。

完了条件：

- 既存37要件と追加13要件の固定sourceを特定し、順逆被覆のbaselineをEvidenceへ固定する。
- owner、停止、復旧、受入、対象外の欠測を識別し、次の一作業を決める。

後続作業：source、Change Set、Test／CI／Build Artifactのidentityとstale規則を確認する。

## blocker・Human判断待ち

- blocker：なし
- Human判断待ち：なし
- 再開条件：Work 2完了EvidenceとchecklistのDigest一致を確認する

## stale・deferred

- stale：current artifactはなし。Work 1固定入力Evidence v2はpromotion前state、旧candidate Digestと
  session `001`はsupersededとして保持する。現行はEvidence v3、Approval Decision、session `003`とする。
- deferred：画面UI、As-Built projection、AI判断委譲、shared／distributed deployment、改善候補・
  Issue Resolution・実施報告照合のautomation、汎用Task Registry／plugin system

## Git・Test

- branch：`main`
- HEAD：`eba6960aba234889f82fd68bb7d4678fc8b795bd`
- remote：`origin/main`と同期済み
- worktree：Work 1B成果一式、Work 2完了Decision／Evidence、checklist、TODOが未コミット
- 直近の関連Test：bootstrap／durable／E2E／NEXT回帰、合計`17 passed in 0.07s`
- 直近の全Test：`436 passed in 1.95s`
- 差分検査：`git diff --check`、通過

## 更新規則

- session終了時に、現在位置、実施報告照合、未実施、次の一作業、blocker、stale、Git／Test、
  参照Digestを更新する。
- 報告だけでClaimを`verified`にせず、Evidenceと観測した事後状態を記録する。
- TODOは現行handoffだけを保持し、過去sessionの時系列logにしない。
- Stage変更、長期中断、大きな計画改定など、独立保持する価値がある場合だけ
  `records/session-handoffs/`へ日付付きの不変snapshotを作る。
- 通常のsession履歴と完了EvidenceはSession Evidence、Decision、Provenance、Gitへ保存する。
