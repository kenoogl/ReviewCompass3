# TODO_NEXT_SESSION

更新日：2026-08-04
用途：session更新・次sessionへの引き継ぎ

> 本書は人向けの入口であり、Workflow state、完了判断、Evidenceの正本ではない。
> 過去sessionを累積せず、固定Plan、checklist、Git、Test、Decision、Provenanceをリンクして使う。

## 現在位置

- 全体：初期開発Work 1B、Work 2、Work 3完了。次の未完了工程はWork 4
- 現在の工程：Work 3 `verified / completed`、Work 4 `not_started`。完了済みinter-work correctiveと、
  `bootstrap_in_progress`のIssue Resolution早期PilotをPlan／checklistへ反映済み。
- Issue Resolution早期Pilot：Layout Baseline v2、ReviewCompass3 Project Manifest v2、workflow rootを
  検証済み。Task ContractとImprovement Candidate／Triage Decisionの暫定形状をtest-firstで固定済み。
  単一Candidateを作成し、Humanが`issue_resolution / blocking=false`と一件のIssue昇格を承認した。
  Issue Record、Resolution Plan v1、Plan Challenge v1を作成し、Humanの修正Decisionに従ってPlan v2を作成した。
  Challenge v2はblocking Finding 0で、HumanがPlan v2を承認した。Task Contract作成前の照合でderived stateの
  中間状態欠落を検出し、Humanが推奨案Aを承認した。Plan v3とChallenge v3は三状態境界を補完して検証済み。
  HumanがPlan v3を最終承認した。実装Task Contractは作成・検証済みで、現行stateは
  `task_contract_commit_pending`。次はTask Contract作業単位をcommitする。
- work unit commit reminder Pilot：実装・検証・commit済み。以後、完了済み作業単位が未コミットなら
  `completed_work_unit_uncommitted`として次作業への移行を停止する。
- デプロイ／Project Artifact境界corrective：`approved_effective`。Approval Decisionは
  `records/development/2026-08-04-layout-baseline-v2-approval-decision.json`、SHA-256
  `856345948af57bcfa373eb2766768d9c38078d7ba5fe65b0d76d68e452ceaa7e`。
- TODO手戻り候補対策の修正案：`docs/design/2026-08-04-todo-rework-candidate-routing-revision-memo.md`、
  SHA-256 `e156a3b055b19b70bfb9bbe77d1af444ee30ecfcfbf47a7d436096dddcb571b3`。詳細は耐久Candidate／
  Issue経路へ分離し、TODOはactive ID projectionだけにする案。実装保留。
- activeなTask Contract／Work Item：`TC-RC3-ISSUE-RESOLUTION-TODO-COMPACTION-2026-08-04-V1`、
  state `task_contract_commit_pending`、WI-001 `not_started`。
- 製品実装code：capture、projection、text、durable writer、E2E orchestration、完了NEXT遷移を実装
- 当面の進行入口：`docs/development/2026-08-03-initial-development-checklist.md`
- 進行入口SHA-256：`b4817c685778fdcb831a653f794283a22ab8a87cf26f467f19276bbfce4e35ba`
- 現行計画：`docs/current/reviewcompass3-plan-current.md`
- 現行計画SHA-256：`0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`
- 現行開発方針：`docs/development/2026-08-02-development-policy.md`
- 現行開発方針SHA-256：`9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0`
- 直近のDecision／Evidence：
  `records/development/2026-08-04-issue-resolution-pilot-implementation-task-contract-completion-evidence-v1.md`
- Decision／Evidence SHA-256：`591b786b3128bde56d2d4c92af1b5883ec0c2323de5973758dab809f1b64d6f1`

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
- Claim `EC-051`：既存37要件と追加13要件の固定sourceと50 ID母集合を再照合した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-baseline-evidence-v1.md`、SHA-256
    `7fdc24c8063292871761af3c888824f3e3c715689df3a3924c28c7856f9c5a20`
  - 観測した事後状態：37＋13 IDと現行Planは欠落・余剰0、旧新ID重複0、候補`010/011`は母集合外だった。
- Claim `EC-052`：50要件のowner、停止、復旧、受入、対象外の形状を監査した。
  - Evidence：既存37要件の構造化record 2件、追加13要件差分、既存coverage audit
  - 観測した事後状態：owner欠落0、既存shape欠測0、追加shape欠測0、source trace未被覆0、専用Test
    `59 passed in 0.07s`だった。
- Claim `EC-053`：Requirement単位の新旧semantic coverage gapを識別した。
  - Evidence：同Baseline Evidence V1の6節
  - 観測した事後状態：37 Acceptance Testの継承表は存在するが、既存37 Requirementを
    `preserve | adapt | replace | defer`へ結ぶ37行matrixはなく、Work 3先頭checkboxを未完了で維持した。
- Claim `EC-054`：既存37 Requirementのdisposition／successor coverage matrix候補を作成した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-coverage-candidate-v1.json`、SHA-256
    `c529e1495a8ea5a84ac15ae651299a410f6aba627ee115b395a5940aa209cb7e`
  - 観測した事後状態：37 unique ID、`preserve: 15`、`adapt: 20`、`replace: 2`、`defer: 0`となった。
- Claim `EC-055`：候補を既存owner、Acceptance Test継承表、追加13 IDから独立照合した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-coverage-evidence-v1.md`、SHA-256
    `fa4dc0818ff4666a940b8347ee44af39b7262f09386cf903e9775165c5e31508`
  - 観測した事後状態：owner不一致0、旧／後継test不一致0、追加13 ID逆引き欠落0。初回に検出した
    `REQ-TRACE-004`旧test IDの転記ミス1件を訂正し、再監査は`matrix_audit: passed`だった。
- Claim `EC-056`：Humanが選択肢1としてWork 3 Coverage Matrix候補を承認した。
  - Decision：`records/development/2026-08-03-work-3-requirements-coverage-decision.json`、SHA-256
    `cb1c879e28b27fdec765fb9c37636ab59b6017e822b9e4315c33965a8823e54f`
  - 観測した事後状態：候補Digestと監査Evidenceへ承認を束縛し、Requirements／Plan本文は変更しなかった。
- Claim `EC-057`：Work 3先頭項目を完了Evidenceへ接続した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-coverage-completion-evidence-v1.md`、SHA-256
    `bcddaa3e5b4388adba958cc3198c2ac543b2977e8efdcb48c1d440f332023e61`
  - 観測した事後状態：先頭checkboxは`verified / completed`、Work 3残り3項目は未完了となった。
- Claim `EC-058`：sourceからBuild Artifactまでのidentity／stale規則をHuman判断候補へ固定した。
  - Evidence：`records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json`、SHA-256
    `e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc`
  - 観測した事後状態：Repository Binding、Source Snapshot、Change Set、Verification Run、Build Artifactの
    5 entityにowner、identity、stale、復旧、受入、対象外が揃った。
- Claim `EC-059`：5つの対象一致関門と固定sourceを独立監査した。
  - Evidence：`records/development/2026-08-03-work-3-source-identity-stale-evidence-v1.md`、SHA-256
    `3d04943d0174c323d9b5f1feb605eb70ff3e4dc3a779e681bf179d810db16812`
  - 観測した事後状態：entity 5件、gate 5件、source Digest 6件、relation 7段階、欠落・未知参照・
    Digest不一致0で`AUDIT_OK`。候補は`proposed_only`、checkboxはHuman判断前のため未完了を維持した。
- Claim `EC-060`：追加13 Requirement構造化前の配置・命名・authority境界をHuman判断候補へ固定した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-artifact-layout-candidate-v1.json`、SHA-256
    `154a4f40487bc52537e87575d063f0c3e0e72b19fa13d2cdcee0e4fc0339e6ed`
  - 観測した事後状態：人向けsource、definition、candidate、Decision、Evidence、schema、authority bundleの
    7 classと、ID／version／Digest／Decisionによる正本解決規則を固定した。
- Claim `EC-061`：配置・authority候補を既存Requirements配置、legacy Approval、Layout規則へ照合した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-artifact-layout-evidence-v1.md`、SHA-256
    `25c7a61e99f04b78ab2732ef70bf507ec161f859085238579f6d0fcb09285871`
  - 観測した事後状態：artifact class 7、fixed source 10、stale rule 5、欠落・重複・Digest不一致0で
    `LAYOUT_AUTHORITY_AUDIT_OK`。既存37要件は未変更、提案directoryは未作成、追加13要件は未構造化である。
- Claim `EC-062`：HumanがA1としてidentity／stale候補を承認した。
  - Decision：`records/development/2026-08-03-work-3-source-identity-stale-decision.json`、SHA-256
    `1eba4807e9b1e5d5ff4fa38e8617e768c27cfe02c553572d91c86cd67366bae9`
  - 観測した事後状態：candidateとEvidence Digestへ承認を束縛し、CI／Build Artifact実装、provider操作、
    Requirements／Plan本文変更は承認範囲外に維持した。
- Claim `EC-063`：identity／stale checklist項目を完了Evidenceへ接続した。
  - Evidence：`records/development/2026-08-03-work-3-source-identity-stale-completion-evidence-v1.md`、SHA-256
    `e0c450b3ec7758f46a9056620513bfa023e8ca8dc8ad78e2e4eb1c65871edb06`
  - 観測した事後状態：5 entity、5 gate、7 relationは`verified / completed`となった。
- Claim `EC-064`：HumanがB1としてRequirements配置・authority候補を承認した。
  - Decision：`records/development/2026-08-03-work-3-requirements-artifact-layout-decision.json`、SHA-256
    `516caf5214bd9bfe840d96a7f1249593c2844da26b511432a8cee12ff91e336e`
  - 観測した事後状態：7 artifact class、命名、version、Digest、authority、stale、legacy移行規則を承認し、
    directory／schema作成、追加13構造化、既存37移動は承認範囲外に維持した。
- Claim `EC-065`：Requirements配置・authority checklist項目を完了Evidenceへ接続した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-artifact-layout-completion-evidence-v1.md`、SHA-256
    `1aac602366fbe3e5c6a04ec9e509119bcd7472ef54cc627b7af44411f3822725`
  - 観測した事後状態：配置規則は`verified / completed`、次はdirectory、schema、validator、fixture、
    legacy binding inventoryのtest-first実装となった。
- Claim `EC-066`：Requirements artifact runtimeの正常、負例、境界例を固定Test 12件へ先行固定した。
  - Evidence：`records/development/2026-08-03-work-3-requirements-artifact-runtime-red-evidence-v1.md`、SHA-256
    `9c6ec0d66f3bda56deee59e1a410694dd5c60a0ad2dd30fc68125c6efb97d373`
  - 観測した事後状態：Test SHA-256
    `49df58714f901cf83c11594a9ac0f5f77567ac445e3977f81a1c756d9325a6a9`、fixture SHA-256
    `8d063195352ac6b376b16cea32fc4bcb7584ac98a52ada83f50979dbb5b4c59c`を固定し、module未実装により
    `12 errors in 0.07s`の期待どおりのREDとなった。
- Claim `EC-067`：承認済みdirectory、最小schema、validator、legacy binding inventoryを実装した。
  - Evidence：`tools/requirements/artifact_layout.py`、SHA-256
    `8e96086c9a6cb9aee7d8db87377afffb8a8cd41092aa49967a65b5b9fd350ac2`、schema SHA-256
    `cd8d5f69565b17c9ec2753dadab841ca2dd58cb7f401b3223bea61ef73b035ff`、legacy inventory SHA-256
    `8daec571041b8a70dab3055922b05fab58be49f270ad63438397dfda47a0e792`
  - 観測した事後状態：5 artifact kind、Digest、locator、authority chain、legacy 37 ID／6 sourceを検査でき、
    追加13 definitionと既存37要件の移動・書換えは0だった。
- Claim `EC-068`：固定Testを変更せずRequirements artifact runtimeをgreenにした。
  - Evidence：`records/development/2026-08-03-work-3-requirements-artifact-runtime-green-evidence-v1.md`、SHA-256
    `b213de7ae162879dfe7a73bae0aa69d6ccc9a2633dfb08091ebe20ca6dd515f2`
  - 観測した事後状態：targeted `12 passed`、Requirements関連`71 passed`、全`448 passed`、独立JSON Schema
    `artifacts=6`。初回2不一致はTestを変えずREADME固定句と`@v1` schema patternを修正して閉じた。
- Claim `EC-069`：追加13 Requirementを不変definitionへ構造化し、一つのcandidate manifestへ束縛した。
  - Evidence：`records/requirements/candidates/rc3-requirements-added-13-2026-08-03-v1.json`、file SHA-256
    `c3d6497516fcbabd18fdffe88279b1095eec8a140f32e8ca8c7f1d6e3c8d2525`、candidate digest
    `89ee1908ec3c0cafd6b4c5d5fe244b7098745265dcc3f247b554a5abe1494773`
  - 観測した事後状態：definition 13件、definition ref 13件で、source、feature owner、停止、復旧、受入、
    対象外を保持した。既存37 Requirementは移動・書換え0件だった。
- Claim `EC-070`：追加13 definitionとcandidateをschema、source、reference Digest、50件coverageへ照合した。
  - Evidence：`records/requirements/evidence/rc3-requirements-added-13-evidence-2026-08-03-v1.json`、file SHA-256
    `f57a5cdaeb4cf37a0285218e73c6e5342b417d822878d919c29bd0c13d810f55`、evidence digest
    `4f5d76d4606627e47b98f8408cdac437d9cb8235e9d2be72f2114fc582d227ca`
  - 観測した事後状態：独立schema `artifacts=15`、source alignment `definitions=13 fields=8`、参照Digest
    `definition_refs=13 fixed_refs=7 schema_refs=1`、coverage `37+13=50、重複0、除外2`に合格し、
    Requirements関連Testは`75 passed`、全Testは`448 passed`だった。Human Decisionとauthority bundleは
    未作成である。
- Claim `EC-071`：Humanが追加13 Requirement candidateのpromotionを承認した。
  - Decision：`records/requirements/decisions/dec-requirements-added-13-2026-08-03-v1.json`、file SHA-256
    `5489b4b45baa8a9078f97540cc154363157c14e8c5cc56f151ca4d8259b46aff`、record digest
    `707c306a19d82cfe94b1140bde884974973e9bf5daeb13d0d8b0f6376f632e31`
  - 観測した事後状態：Decisionはexact candidate／Evidence Digestへ束縛され、outcome `approved`、authority
    `human`となった。未採用候補、要件本文変更、現行Plan変更、実装完了は承認範囲外に維持した。
- Claim `EC-072`：既存37 legacy bindingと追加13 definitionを50 Requirement authority bundleへ接続した。
  - Evidence：`records/development/2026-08-03-work-3-added-requirements-promotion-completion-evidence-v1.md`、SHA-256
    `dc945ec1d2eae4fe4c8c3293b9f1390fe4c527094e5dc209082dafc6f3b80649`
  - 観測した事後状態：authority bundle digest
    `497bcc4374e3224acbfbb08e38c7d9f3d4e5373f59df505179b6a19bc035a02c`、authority chain `effective`、
    50 IDの欠落・重複0、独立schema 17 artifact、全Test `448 passed`だった。
- Claim `EC-073`：50 Requirementの必須非機能義務を19 Verification Profileへ接続する候補を作成した。
  - Evidence：`records/development/2026-08-03-work-3-nfr-verification-profile-candidate-v1.json`、file SHA-256
    `08d5159a483d16507c5652857e5245993b42559ed3bcc24c9434e70b0d5c2381`、candidate digest
    `c93f9336790fc8641f3f89687f94fcff3baa23254936545ed9cb85c15c25d3a6`
  - 観測した事後状態：NFR接続29 Requirement、functional／control only 21 Requirement、重複・欠落0。
    Profileは初期必須8、実測後閾値6、deployment defer 5となった。
- Claim `EC-074`：Profile形状、7品質属性、authority境界、未被覆停止、既知違反を監査した。
  - Evidence：`records/development/2026-08-03-work-3-nfr-verification-profile-evidence-v1.md`、SHA-256
    `e0800a9832798df5ab50a83203c42b16a2728488ff0f8942eb86e919740d2a12`
  - 観測した事後状態：必須field 18、未知Requirement参照0、Policy rule候補6、負例6件を監査し、
    `not_compilable`、数値非発明、deferの`not_applicable`、stale規則に合格した。全Testは`448 passed`。
    承認済みArchitecture Policy recordは存在しないため、Plan由来ruleをPolicy authorityにしていない。
- Claim `EC-075`：HumanがNFR Verification Profile接続候補を承認した。
  - Decision：`records/development/2026-08-03-work-3-nfr-verification-profile-decision.json`、SHA-256
    `6cdb1f74c8b92bcc7257bf8087158f78e8c980428d1b0fa725a20e2dd8e96373`
  - 観測した事後状態：exact candidate／Evidence Digestと19 Profileの3分類へ承認を束縛し、Architecture
    Policy昇格0、数値閾値承認0、Requirement変更0を維持した。
- Claim `EC-076`：NFR Verification Profile接続項目を完了Evidenceへ接続した。
  - Evidence：`records/development/2026-08-03-work-3-nfr-verification-profile-completion-evidence-v1.md`、SHA-256
    `c8c99ca93d9eb29c112febbc18fa53fbf5476d703399a07888b7733cb9fb379f`
  - 観測した事後状態：Decision binding、Profile分類、authority境界に合格し、全Testは`448 passed`。
    本項目は`verified / completed`、次の未完了項目はdeferred候補の暗黙依存確認となった。
- Claim `EC-077`：deferred能力13件のowner、成果、論理配置、有効化条件、初期非依存境界を候補へ固定した。
  - Evidence：`records/development/2026-08-03-work-3-deferred-scope-candidate-v1.json`、file SHA-256
    `01da1ea0c6c4f6adad8fdcd09085f97b387ea4639d01b0811b80dc5957916210`、candidate digest
    `8993a6e4671679ab8cfe665322efdaf862cf085a8f1fab7d500d15f5fd7deb84`
  - 観測した事後状態：明示延期9、条件付きPilot 2、新Evidenceなしには不採用2、ID重複0、必須field欠落0、
    未知Requirement／Profile参照0、全13件のrelease effectは`nonblocking`だった。
- Claim `EC-078`：50 RequirementからStage G／releaseまで9 consumerのscope leakを監査した。
  - Evidence：`records/development/2026-08-03-work-3-deferred-scope-evidence-v1.md`、SHA-256
    `1c24269e36d2baa2a4e22d39162e7bb85b7c5e513c55a5035fa55efa54029b71`
  - 観測した事後状態：scope leak 0、release blocker 0、既知違反6件の負例監査は全件検出した。
    `REQ-CONTRACT-008`はeffectiveだが自身の初期範囲外規則により初期Contract／releaseをblockしない。
    初回監査のbundle ID取得誤りは実形状へ合わせて監査側だけを修正し、候補内容は変更していない。
- Claim `EC-079`：恒久対策の共通reader、機械移行、policy Test runnerをtest-firstで固定した。
  - Evidence：`records/development/2026-08-03-work-3-permanent-remediation-red-evidence-v1.md`、SHA-256
    `700a26c69af875ad44e1df446ae79212fc4f3e6de0f552fa529624a70957ea2d`
  - 観測した事後状態：未実装を理由に`2 failed, 12 passed, 8 errors`のREDとなり、既存12件はgreenだった。
- Claim `EC-080`：旧37要件を単一definition形式へ決定的に機械移行した。
  - Evidence：`records/requirements/candidates/rc3-requirements-unified-50-2026-08-03-v1.json`、file SHA-256
    `c82144375fecc22c088d06d510d9e041fe9c607a0d6e4eb353b034467654ca16`、candidate digest
    `cc4ba8f872973f8035b798042f4a5335005394cca339ec6f0121cf16c8c533b4`
  - 観測した事後状態：旧37＋既存13＝50 unique ID、意味field不一致0、schema不一致0、初回38 write、
    2回目と`--check`は`written 0 / unchanged 38`だった。旧authorityとlegacy bindingは未変更である。
- Claim `EC-081`：公式Testを版付きpolicy、preflight、fallback禁止、receipt必須のmachine runnerへ統一した。
  - Evidence：`records/development/2026-08-03-work-3-permanent-remediation-full-test-receipt-v2.json`、SHA-256
    `8405cdb8c9b7d74b4c5cb12d9c71c3f2baee8e900627c5fd023ae6f17f35cef4`
  - 観測した事後状態：Python `3.9.6`、pytest `8.4.2`、fallback `false`、全`462 passed in 2.27s`。
- Claim `EC-082`：統一candidateをformal Evidenceへ機械接続した。
  - Evidence：`records/requirements/evidence/rc3-requirements-unified-50-evidence-2026-08-03-v2.json`、file SHA-256
    `dce1994d194ef8f4c03d32a7fe66fe1764a2456b013270a79d93c261a074ba7f`、evidence digest
    `5b42979ab79699b2da950bae4788f582b023211c5c919571209a7f43bb5492fe`
  - 観測した事後状態：50 definition＋candidateの51 subject、result `passed`。Human Decisionとauthority
    bundle v2は未作成である。
- Claim `EC-083`：receipt自己参照境界をpost-writeで検出し、回帰Test後に修正した。
  - Evidence：`records/development/2026-08-03-work-3-permanent-remediation-green-evidence-v1.md`、SHA-256
    `096e91d786293b5d01f1a14717f49c2b0806c48a8ea8d3b76439108a7ec6af0c`
  - 観測した事後状態：指定receipt outputだけをsource state計算から除外し、関連26件と全462件がgreen。
    旧receipt v1とformal Evidence v1はstaleな経過記録として判断対象外にした。
- Claim `EC-084`：LLMと機械処理の責務境界、手戻りの機械化候補報告を開発Policy v5へ固定した。
  - Decision：`records/development/development-policy-v5.json`、SHA-256
    `88af550d5bc77406cd796e4c78efc20225134473d3d87251942854e6dc57fe98`
  - 観測した事後状態：LLM許可は文章操作・意味分析、決定的処理はmachine必須、手作業による手戻りは
    `manual_rework_candidate`、手戻り前でも境界違反は`manual_operation_candidate`となった。
- Claim `EC-085`：Policy evaluatorへexecutor境界と手戻り報告fieldの機械判定を実装した。
  - Evidence：`records/development/2026-08-03-development-policy-v5-green-test-receipt-v2.json`、SHA-256
    `e974b1afbfcc95b20b6fe734d731375d19164b5b4a5fdec01b0a3b0611bd66ca`
  - 観測した事後状態：実装前は新規5件だけが失敗し、実装後はpolicy runnerで全`467 passed`だった。
- Claim `EC-086`：現行Planのdevelopment policy参照をPolicy v5へ再束縛した。
  - Evidence：`docs/current/reviewcompass3-plan-current.md`、SHA-256
    `911d0c49d1646f308a733e45d0af6071cd7206dd80b31e123369e921b0b490db`
  - 観測した事後状態：policy本文、config、v5 recordの現行Digestへ更新した。旧Plan Digestを固定sourceに持つ
    NFR／deferred候補はidentity再検証までstaleとして扱う。
- Claim `EC-087`：Humanが統一50 Requirement candidateのpromotionを承認した。
  - Decision：`records/requirements/decisions/dec-requirements-unified-50-2026-08-03-v1.json`、file SHA-256
    `dd8b5dd15197da0a3463b3981d607da6edcb8318e17d91038786de7edc9eff27`、record digest
    `b8cce324d5693a2bf4c8e5b9acb8adbf023f726069407e137faebcaa765442d8`
  - 観測した事後状態：exact candidate／Evidence Digestへ承認を束縛し、要件本文、Acceptance truth、Plan、
    製品実装、NFR／deferred判断を承認範囲外に維持した。
- Claim `EC-088`：Decisionとdefinition-only authority v2の決定的生成をtest-firstで実装した。
  - Evidence：`records/development/2026-08-03-work-3-unified-requirements-promotion-red-evidence-v1.md`、SHA-256
    `e887072e94e459711f91b38873f3e3e4c21aac412ab11705c419542b2bbb93dd`
  - 観測した事後状態：実装前は新規1件だけが失敗し、負例追加時は新規2件だけが失敗した。拒否関門実装後は
    全`470 passed`、再生成は`written 0 / unchanged 2`だった。
- Claim `EC-089`：50 definitionだけを持つauthority bundle v2を現行authorityへ昇格した。
  - Evidence：`records/development/2026-08-03-work-3-unified-requirements-promotion-completion-evidence-v1.md`、SHA-256
    `c151019466bdcca66236646f6e635cc729b96585ffa43e68eacac975f3470e80`
  - 観測した事後状態：bundle digest
    `79a69d921bb00eb2b321e3d1adb073b88a527eb938398d1813567009255bd688`、authority `effective`、
    definition 50、legacy binding 0、v1とのeffective ID差分0、独立JSON Schema 54 artifact合格だった。
- Claim `EC-090`：authority／Plan identity変更後のNFR／deferred候補を再検証した。
  - Evidence：`records/development/2026-08-03-work-3-unified-requirements-revalidation-evidence-v1.md`、SHA-256
    `933af699185c27df4a7e4ea80fd15153c5ae9927df4fbdb98e10ae66a8523108`
  - 観測した事後状態：NFRは既承認target、scope、Acceptance truth変更0によりfreshへ復旧した。deferredは
    Requirement／Profile未知参照0、scope leak 0、release blocker 0で再合格し、Human判断待ちを維持した。
- Claim `EC-091`：Humanが再検証済みdeferred scope候補を承認した。
  - Decision：`records/development/2026-08-03-work-3-deferred-scope-decision.json`、SHA-256
    `fc1aba9c31b612939c5e62fec3327ab1b65449257f044a2a7206f2c564cd7873`
  - 観測した事後状態：exact candidate、旧監査Evidence、再検証Evidence、authority v2へ承認を束縛し、
    実装・有効化、個別Pilot開始、Work 3段完了を承認範囲外に維持した。
- Claim `EC-092`：deferred候補の初期非依存境界を完了Evidenceへ接続した。
  - Evidence：`records/development/2026-08-03-work-3-deferred-scope-completion-evidence-v1.md`、SHA-256
    `2f79c3f8005967670b97c0597d86e3aeb17b5151ba7ebd260e201a3c66a893fe`
  - 観測した事後状態：13件すべて`nonblocking`、scope leak 0、release blocker 0、全Test `470 passed`で、
    Work 3最後のcheckboxを`verified / completed`へ更新した。
- Claim `EC-093`：Work 3の7個別項目と固定Completion Evidenceを段完了候補へ接続した。
  - Evidence：`records/development/2026-08-03-work-3-completion-candidate-v1.md`、SHA-256
    `aff0f3977a50f0e4aee9a2937b16518665d0267f44094780b75eba65991d7788`
  - 観測した事後状態：checklist `7/7 completed`、未完了0、blocker 0、completionを阻害するstale 0。
    Work 3段完了はHuman判断待ちとして維持した。
- Claim `EC-094`：HumanがWork 3段完了を明示承認した。
  - Decision：`records/development/2026-08-03-work-3-completion-decision.json`、SHA-256
    `5cf7bb52e5cff547e06581ed6c8b57e8b77eaedc352615e5a063f422467dcf45`
  - 観測した事後状態：Decisionはexact Completion Candidateへ束縛され、Work 3完了関門を閉じた。Work 4の
    成果物変更、commit、push、releaseは承認範囲外に維持した。
- Claim `EC-095`：Work 3の7固定Completion Evidence、Human Decision、現行authority、公式Testを段完了Evidenceへ
  接続した。
  - Evidence：`records/development/2026-08-03-work-3-completion-evidence-v1.md`、SHA-256
    `e602092b3236f62697b2f24d2b706095dda6b8c83e22e5b6211fb539542c7221`
  - 観測した事後状態：Work 3は`verified / completed`、公式全Testは`470 passed in 2.35s`、fallback
    `false`、blocker 0、完了を阻害するstale 0で、次の未完了工程はWork 4となった。
- Claim `EC-096`：HumanがCodex 2形式の実装とClaudeを考慮した共通入口を承認した。
  - Decision：`records/development/2026-08-03-session-transcript-source-formats-decision.json`、SHA-256
    `a8810356db36ec9483880c300e59ad7919d3716ff488723c433591a12e065bfe`
  - 観測した事後状態：承認範囲を3 source kindの解析境界へ限定し、実private logのcopy、hook有効化、
    retention変更、commit、push、Work 4開始を対象外に維持した。
- Claim `EC-097`：Claude、`codex_exec_json`、`codex_rollout`の共通source adapter契約をtest-firstで固定した。
  - Evidence：`records/development/2026-08-03-session-transcript-source-formats-red-evidence-v1.md`、SHA-256
    `a40dc78d848e7c067652b3cc1f7b051c98ba8c88f4354bdd1e1e5eb6130b453c`
  - 観測した事後状態：実装前は新境界の欠落だけを理由として`11 failed, 12 passed in 0.20s`となった。
- Claim `EC-098`：Codex 2形式とClaudeの共通解析境界を実装し、実Desktop rollout shapeと公式Testを検証した。
  - Evidence：
    `records/development/2026-08-03-session-transcript-source-formats-completion-evidence-v1.md`、SHA-256
    `bf8aba264810f19bb8ac495ce579412d6df589e286a72484f83efc88ed3f8fd4`
  - 観測した事後状態：実rolloutは`codex_rollout`、unknown issue 0、公式全Testは
    `477 passed in 2.38s`、fallback `false`だった。private本文は表示またはGit保存していない。
- Claim `EC-099`：Humanが終了hook非依存のeventual preservationを設計方向として承認した。
  - Decision：`records/development/2026-08-03-session-transcript-eventual-preservation-decision.json`、SHA-256
    `620fde82dc424141f4f5a9e8ce383fd9669506149e764eceebff0ada6addfcba`
  - 観測した事後状態：継続回収、定期／起動時再照合、機械的cursor／重複排除／Digest、hookの補助trigger化を
    approved directionへ固定し、実装、activation、保存場所、retentionを承認範囲外に維持した。
- Claim `EC-100`：eventual preservationの保証、artifact、状態、復旧、責務、Acceptanceを設計文書へ固定した。
  - Evidence：
    `records/development/2026-08-03-session-transcript-eventual-preservation-documentation-evidence-v1.md`、SHA-256
    `cf2aad73102777057cf8e29b2829b18e1d7cb1eb7fcfa7d85a07217d3279182e`
  - 観測した事後状態：byte-exact raw、private verbatim、redacted派生物を分離し、現行再利用候補8責務と
    未実装のdurable cursor、startup reconcile、artifact分離を区別した。公式全Testは
    `477 passed in 2.42s`、fallback `false`だった。
- Claim `EC-101`：Humanがeventual preservationのfixture実装と限定実ログ保存までを承認した。
  - Decision：
    `records/development/2026-08-03-session-transcript-eventual-preservation-implementation-decision.json`、SHA-256
    `1fe3c2a6cf8a3430ffb9a290a437dbc34777d2514beac910a26f52a419732262`
  - 観測した事後状態：collector、cursor、reconcile、artifact分離、復旧Test、保存候補、Human判断後の
    現session 1件保存をscopeへ固定し、hook／watcher／scheduler、外部送信、Work 4を対象外に維持した。
- Claim `EC-102`：Task Contractと初回REDを固定した。
  - Evidence：`records/development/2026-08-04-session-transcript-eventual-preservation-red-evidence-v1.md`、SHA-256
    `f7e8649c2ebff2d9941716d67c531990664b53364c20d2c70f70166a3f6938a1`
  - 観測した事後状態：module未実装10件、CLI入口未実装1件だけを理由として`11 failed in 0.16s`となった。
- Claim `EC-103`：manual collector、durable cursor、startup-compatible reconcile、private artifact分離を実装した。
  - Evidence：
    `records/development/2026-08-04-session-transcript-eventual-preservation-implementation-checkpoint-evidence-v1.md`、
    SHA-256 `134a00b9ba94dca600b4f26f4b0ce132099fc2eabd72648cda8e30e4f3c8479a`
  - 観測した事後状態：同一再実行、追記、部分行、中断、divergence、3形式、missing／unknown、単一source CLIが
    greenとなり、session-log全Testは`171 passed`だった。
- Claim `EC-104`：private permissionとOS標準pathの実環境不足をnegative testで修復した。
  - Evidence：同Implementation Checkpoint Evidence V1の4節
  - 観測した事後状態：directory `0700`、file `0600`へ固定し、optional `platformdirs`がないmacOSでも
    標準library fallbackでpath解決した。公式全Testは`490 passed in 2.19s`、fallback `false`だった。
- Claim `EC-105`：現session 1件だけを保存するstorage／operation候補をHuman判断へ固定した。
  - Candidate：`records/development/2026-08-04-session-transcript-eventual-preservation-storage-candidate-v1.json`、
    SHA-256 `0c712308275cd321870fe2c203b0b53207bc817108a9fba3910da6ee730a5fdc`
  - 観測した事後状態：推奨は`option_1_os_standard_limited_pilot`。実private logは未copy、automationは未有効で、
    Task Contractは`human_storage_decision_pending`を維持した。
- Claim `EC-106`：Humanが選択肢1としてOS標準rootへの限定pilotを承認した。
  - Decision：`records/development/2026-08-04-session-transcript-eventual-preservation-storage-decision.json`、
    SHA-256 `79c9e7aa781d09cb4afe477919889e12583ae1d8e57b15317046cff5c1e74953`
  - 観測した事後状態：現在のCodex Desktop task 1件と5 private artifactだけを承認し、過去履歴、Claude、
    redacted transcript、automation、外部送信、Git保存を対象外に維持した。
- Claim `EC-107`：現在のCodex rolloutを限定保存し、同一即時再実行と完全性を検証した。
  - Receipt：
    `records/development/2026-08-04-session-transcript-eventual-preservation-limited-capture-receipt-v1.json`、
    SHA-256 `ef351d6a7e9754d5206a5a5183d8e2230bd90c156d9763473985331e3cb5f77e`
  - 観測した事後状態：初回`created`、再実行`unchanged`、event 2595、issue 0、source prefix一致、
    5 artifactのDigest結線合格、directory `0700`、file `0600`、一時／lock残留0、Git混入0だった。
- Claim `EC-108`：Task Contractを限定captureの完了Evidenceへ接続した。
  - Evidence：
    `records/development/2026-08-04-session-transcript-eventual-preservation-completion-evidence-v1.md`、SHA-256
    `194c302277299cb3ab8853951f8db8d5d64424d4f16c1798e0a82f40eb41740a`
  - 観測した事後状態：公式全Testは`490 passed in 2.54s`、fallback `false`、correctiveは
    `verified / completed`となり、次の未完了工程はWork 4である。
- Claim `EC-109`：Humanがcommit後のTODO転記による追加commitを廃止する方針変更を承認した。
  - Decision：`records/development/2026-08-04-commit-handoff-stability-decision.json`、SHA-256
    `3569bbdcfdc2cfa0181951aeb0699f2409aa4ed675be5f33ce8afb36dbaf8428`
  - 観測した事後状態：commit前のcommit安定形式、Git状態の機械取得、commit後read-only照合をscopeへ固定し、
    guarded commit、amend、hook、履歴書換えを対象外にした。
- Claim `EC-110`：commit安定TODO validatorの正常、負例、境界例をtest-firstで固定した。
  - Evidence：`records/development/2026-08-04-commit-handoff-stability-red-evidence-v1.md`、SHA-256
    `b3fdf564af7cfa51321da721b6534321cf79ef1b8cec64b909ca21a3b32305ed`
  - 観測した事後状態：初回はmodule未実装だけで`6 failed`、実装後は旧template／TODOだけで
    `5 passed, 1 failed`となった。
- Claim `EC-111`：policy、AGENTS、checklist、template、現行TODOと機械validatorをcommit安定形式へ統一した。
  - Evidence：`records/development/2026-08-04-commit-handoff-stability-completion-evidence-v1.md`、SHA-256
    `a0e03f686c9879416798ed58a56e610f59e0fb775a9c4c73fb61a16a623ea077`
  - 観測した事後状態：自己SHA、数値付きahead／behind、push済否、未コミットsnapshotを拒否し、現行TODOと
    templateのCLI検査はfinding 0だった。
- Claim `EC-112`：commit handoff恒久対策をGREEN Evidenceへ接続した。
  - Evidence：同Completion Evidence V1
  - 観測した事後状態：targeted `6 passed`、公式全Test `496 passed in 2.57s`、fallback `false`で、候補を
    `manual_rework_candidate / resolved_by_commit_stable_todo_validator`として閉じた。
- Claim `EC-113`：Humanがwork unit commit reminderのdevelopment限定Pilotを承認した。
  - Decision：`records/development/2026-08-04-work-unit-commit-reminder-pilot-decision.json`、SHA-256
    `327cdf74c4cedfa2230a906fbe4e75f24b2cff1da6a00c06a6c3ea03c1cdb64b`
  - 観測した事後状態：完了済み・未コミット時の次作業停止を承認し、自動commit、push、hook、
    guarded commit、履歴書換えを対象外に維持した。
- Claim `EC-114`：正常、負例、境界、Git状態取得、CLIをtest-firstで固定した。
  - Evidence：`records/development/2026-08-04-work-unit-commit-reminder-red-evidence-v1.md`、SHA-256
    `2fabf5401ef44c1fbcf92758215855b941d8ef5de30178dea0b2763870e31f0b`
  - 観測した事後状態：初回は遷移preflight未実装だけで`5 failed`、実装後は`5 passed`となった。
- Claim `EC-115`：遷移preflight、policy、AGENTS、checklist、templateをPilot運用へ接続した。
  - Evidence：`records/development/2026-08-04-work-unit-commit-reminder-completion-evidence-v1.md`、SHA-256
    `b7f8e91520b2664ede24347144004b724c5654d23c5cb318864c1a8530ab35d0`
  - 観測した事後状態：`completed`とdirtyの同時成立だけを`completed_work_unit_uncommitted`として停止し、
    `in_progress` dirtyは誤停止しない。
- Claim `EC-116`：このthreadで当初順序外に追加した作業をPlanとchecklistへ正式に反映した。
  - Evidence：`records/development/2026-08-04-thread-added-work-plan-checklist-reconciliation-v1.md`、SHA-256
    `e86539f3b3034ec6f3a6f6650ae78aed7295f1e3a99e2bbcfbf9a2d891a7d0fa`
  - 観測した事後状態：session transcript保全、Layout／Project Artifact、ReviewCompass Issue Resolution早期Pilot、
    commit／handoff安定化をWork 3後・Work 4前のinter-work列へ配置し、完了／未完了境界をcheckboxへ写像した。
- Claim `EC-117`：Plan Digest変更のstale閉包を確認した。
  - Evidence：`records/development/2026-08-04-plan-reconciliation-stale-closure-evidence-v1.md`、SHA-256
    `652390b74d0c78bd1b12d8cc5be6be4c6258c5ef68f6ee86f8dd86c5938b127b`
  - 観測した事後状態：変更は現在地、inter-work節、初期実装順に限定され、Requirement、NFR接続、
    deferred disposition、Acceptance truthは変更していない。Work 4／7／8を完了扱いにしていない。
- Claim `EC-118`：Issue Resolution早期Pilotの限定再開Decision、固定Observation、Task Contractを作成した。
  - Evidence：`records/task-contract/issue-resolution-early-pilot-v1.json`、SHA-256
    `69e2c73167f930cab48abdcf3bd4d1eafa938aa9b3abaa714d6c3ad5e41c4ed7`
  - 観測した事後状態：Pilot subjectはTODO肥大化一件、固定source 9件、Issue上限1件である。Observationは
    Candidate／Issueではなく、TODO compaction前の不変測定値として保持した。
- Claim `EC-119`：Candidate／Human Triage Decisionの暫定形状とvalidatorをtest-firstで固定した。
  - Evidence：`records/development/2026-08-04-issue-resolution-pilot-bootstrap-completion-evidence-v1.md`、SHA-256
    `1f2b981301e9a249226de4253f504586cea6f6dc23c5c1d780c53e4ec84b1f37`
  - 観測した事後状態：同じ15 Testを変更せずREDからGREENへし、固定source 9件と空bootstrap配置をCLIで
    再検証した。Candidate、Decision、Issueはまだ作成していない。
- Claim `EC-120`：単一Candidateを作成し、Humanが選択肢1としてIssue昇格を承認した。
  - Evidence：`records/development/2026-08-04-issue-resolution-pilot-candidate-triage-completion-evidence-v1.md`、
    SHA-256 `9ebfe80bb351f6c09a0d27508c70988ce1fe24593324209423e94e9d94bea523`
  - 観測した事後状態：DecisionはCandidateのID、version、file Digest、content Digestへ束縛され、
    `ISSUE-PILOT-TODO-GROWTH-001 / nonblocking`を承認した。Issue RecordとPlanは未作成である。
- Claim `EC-121`：承認済みIssue一件とResolution Plan一件を別identityで作成した。
  - Evidence：`records/development/2026-08-04-issue-resolution-pilot-issue-plan-completion-evidence-v1.md`、
    SHA-256 `a1efb8ff5bb7027f604774a27cc5681bc4d6f6e0cf1931727407361803d7fa61`
  - 観測した事後状態：IssueはObservation、Candidate、Human DecisionへDigest付きで接続された。Planは
    Issue obligation 5件、Work Item 5件、Acceptance 6件、oracle 6件、rollback 2件を持ち、Challenge未承認である。
- Claim `EC-122`：Plan Challenge v1のblocking FindingをHuman Decisionへ接続し、Plan v2とChallenge v2を作成した。
  - Evidence：`records/development/2026-08-04-issue-resolution-pilot-plan-revision-red-evidence-v1.md`、SHA-256
    `ef17d136479a2f3e8fb6da4c43d8390a3bbd0e8d845672b7429a18d9cf5b3557`
  - 観測した事後状態：Plan v2はderived state closure、12288／12289 bytes境界、link-only Claude入口を持つ。
    Challenge v2は10基準合格、blocking Finding 0、`ready_for_human_approval`で、Human最終判断を先取りしていない。
- Claim `EC-123`：HumanがPlan v2を最終承認した。
  - Decision：`records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v2-decision.json`、SHA-256
    `07e6d865d27c86d9f039b5742092efcf1429656f38ec4ac3ddfc23e697d4f892`
  - 観測した事後状態：DecisionはPlan v2とChallenge v2のversion、file SHA-256、content Digestへ接続された。
    実装Task Contract作成だけを次作業として許可し、TODO compaction、Issue解決、Work 4開始は先取りしていない。
- Claim `EC-124`：Task Contract作成前にPlan v2のderived state境界欠落を検出し、作成を停止した。
  - Candidate：`records/development/2026-08-04-issue-resolution-pilot-task-contract-state-gap-candidate-v1.json`、SHA-256
    `b8300b13fed8af8c95cee424a1478aaedfaa085a27d9dcb6512c48ea15c6e632`
  - 観測した事後状態：repository内の定義はTask Contract未作成の`task_contract_pending`とactive Taskの
    `implementation_in_progress`だけで、作成・検証済みかつ未commit／未開始の状態は存在しない。Task Contract、
    WI-001、snapshot、TODO compactionは未作成・未開始のままである。
- Claim `EC-125`：Humanが推奨案Aを承認し、Plan v3とChallenge v3を作成・検証した。
  - Evidence：`records/development/2026-08-04-issue-resolution-pilot-plan-v3-red-evidence-v1.md`、SHA-256
    `591523aafa4ded9f46042351a213d191b8b6636d2a0365cf38869ecaec93a55f`
  - 観測した事後状態：Plan v3は`task_contract_commit_pending`、`implementation_ready`、
    `implementation_in_progress`をcontaining commitとWI-001 RED開始で分離した。Challenge v3は10基準合格、
    blocking Finding 0、`ready_for_human_approval`で、Task Contractは未作成である。
- Claim `EC-126`：HumanがPlan v3を最終承認した。
  - Decision：`records/development/2026-08-04-issue-resolution-pilot-plan-challenge-v3-decision.json`、SHA-256
    `31abfa394605915d4abe4fe6f121816a1229669d9c9144b8184edad34d093b95`
  - 観測した事後状態：DecisionはPlan v3、Challenge v3、公式全557 Test receiptへ結線された。承認作業単位の
    commit後にTask Contract作成を許可し、WI-001、snapshot、TODO compaction、Issue解決は先取りしていない。
- Claim `EC-127`：Plan v3に結線した実装Task Contractを作成・検証した。
  - Evidence：`records/development/2026-08-04-issue-resolution-pilot-implementation-task-contract-completion-evidence-v1.md`、
    SHA-256 `591b786b3128bde56d2d4c92af1b5883ec0c2323de5973758dab809f1b64d6f1`
  - 観測した事後状態：6 Work Itemの順序・coverageはPlan v3と一致し、三状態をworking tree、containing commit、
    WI-001 RED Evidenceから導出する。専用`5 passed`、公式全`562 passed`、fallback `false`。WI-001は未開始である。

### reported_unverified／contradicted

- `report_execution_mismatch`：Work 2を`verified / human_decision_pending`とした報告は、candidateの
  `generated_at`が事後状態と一致しないため無効だった。`EC-045`と`EC-046`で修復し、旧candidate Digestと
  session `001`をsuperseded、新candidateとsession `002`をcurrentとして閉じた。

### 手戻り・機械化候補

- 既知候補：authority bundleのRequirement ID列挙は期待executor `machine`に対し一度LLMの個別走査となり、
  0件誤判定の手戻りが発生した。Evidenceはdeferred scope監査Evidence、機械処理候補はmixed authority
  reader、routeは恒久対策commit `f9adef4`で実装済み。
- 既知候補：Test実行環境選択は期待executor `machine`に対しLLMが`.venv` pathを選び、存在しないpathで
  手戻りが発生した。Evidenceは恒久対策GREEN Evidence、機械処理候補はpolicy Test runner、routeは
  commit `f9adef4`で実装済み。
- 今回の候補：checklistへPolicy v5説明を挿入する際、期待executorは構造見出しを解決する`machine`、
  実executorはLLMによるexact anchor選択となり、実fileと一致せず`apply_patch verification failed`が1回発生した。
  再読込後のpatchは成功した。機械処理候補は見出しidentityからのlocator自動解決、routeは
  `manual_rework_candidate / checkpoint`とし、同種再発時に共通patch helperのTask Contract候補へ昇格する。
- 今回の候補：commit後の引き継ぎ照合で、固定receipt v2の全Test時間`2.26s`に対し、TODOへ`2.29s`と
  手入力されていた転記差を検出した。期待executorはreceiptからGit／Test欄を生成する`machine`、実executorは
  手入力であり、固定Evidenceの値へ訂正した。機械処理候補はreceipt projection、routeは
  `manual_rework_candidate / checkpoint`とし、同種再発時にTODO更新helperのTask Contract候補へ昇格する。
- 今回の観測：promotion事前監査の初回表示は50件全体の`acceptance_truth_changed=true`を13件と集計し、
  旧37件の移行結果との区分が分かりにくかった。実executorと期待executorはともに`machine`で手作業因果はない。
  旧37件0、既承認追加13件13へ再集計して解消した。機械処理候補はcohort別監査出力、routeは
  `machine_report_ambiguity / checkpoint`とする。
- 今回の候補：正常系GREEN後にCompletion Evidenceを作成し、その後の高risk負例追加で最終Verification時刻が
  後ろへ移ったため、完了記録の`recorded_at`を訂正した。期待executorは全必須Verification終了後に時刻を確定する
  `machine`、実executorはLLMによる文書作成と途中時刻の採用だった。Evidenceはnegative RED／GREEN receipt、
  機械処理候補はcompletion finalizer、routeは`manual_rework_candidate / checkpoint`とする。
- 今回の候補：Work 3段完了の最終照合で、一時監査スクリプトがauthority v2のfieldを`requirements`／`status`と
  仮定し、`KeyError`で1回停止した。期待executorは承認済みschemaと共通resolverを使う`machine`、実executorは
  LLMが組み立てた一時スクリプトだった。成果物不良ではなく、実fieldを機械取得後、既存の
  `resolve_effective_requirement_ids()`へ切り替えて`effective / 50 / legacy binding 0`に合格した。機械処理候補は
  段完了監査から共通resolverを直接呼ぶverification commandの定型化、routeは
  `manual_operation_candidate / resolved_by_existing_machine_reader`とする。
- 今回の観測：session transcript実装後の最初の公式全Testで、不正UTF-8を既存どおり
  `UnicodeDecodeError`にする契約がunknown sourceへ変わる回帰を1件検出した。実executorと期待executorはともに
  `machine`で、手作業因果はない。decode errorを変換せず伝播させ、関連`30 passed`、全`477 passed`へ復旧した。
  既存機械Testが回帰を閉じており、routeは`machine_regression / closed_by_existing_contract`とする。
- 今回の文書化では失敗、手戻り、手入力転記訂正は発生しなかった。path存在、見出し、JSON、Digest、Testを
  機械処理で照合し、新しい`manual_rework_candidate`／`manual_operation_candidate`はない。
- 今回の実装調査で、並列`functions.exec`のJavaScript出力区切りをLLMが誤記し、構文エラーが1回発生した。
  期待executorはtool-call schemaを検査する`machine`、実executorはLLM直接組立てだった。成果物影響はない。
  機械処理候補はcomposition lint、routeは`manual_operation_candidate / checkpoint`とする。
- 今回のcompile確認はworkspace外cacheへの書込みをsandboxが拒否した。実／期待executorはともに`machine`で
  手作業因果はない。task専用`PYTHONPYCACHEPREFIX`で合格した。機械処理候補はcompile runnerのcache固定、
  routeは`machine_environment_mismatch / checkpoint`とする。
- 今回の限定capture後の補助検索で、検索語中のbacktickをshellが解釈し、一部検索だけが1回失敗した。
  成果物、capture、Testへの影響はない。期待executorは構造化argvを渡す`machine`、実executorはLLMによる
  shell文字列の直接組立てだった。引用を修正して再検索した。機械処理候補はshell非経由のargv実行または
  composition lint、routeは`manual_operation_candidate / checkpoint`とする。
- 今回のcommit作業で、権限定義から`.git`がread-onlyだと事前に分かっていたにもかかわらず、最初の
  `git add`を通常権限で実行し、`.git/index.lock`を作成できず1回停止した。file内容またはGit状態の問題ではなく、
  Git書込み権限で同じstageを再実行して解消した。期待executorはcommand種別とpermission profileから実行経路を
  決定する`machine`、実executorはLLMが通常権限を選択した。恒久対策はread-only Git操作を通常権限、Git metadata
  書込み操作を初回からGit書込み権限へ機械routingし、試行失敗後の権限切替を廃止する。guarded commitは使用しない。
  routeは`manual_operation_candidate / checkpoint`とする。
- 今回のcommit後照合では、TODOへ自己SHA、clean、remote状態を転記するための追加commitが発生した。期待executorは
  commit前に安定handoffを検査する`machine`、実executorはLLMによるpost-commit転記だった。恒久対策として
  commit安定TODO validator、policy、template、checklist、AGENTSを実装し、targeted／全Testに合格した。routeは
  `manual_rework_candidate / resolved_by_commit_stable_todo_validator`とする。
- 今回のPlan／checklist最終照合で、LLMがzshの特殊変数`path`をloop変数へ使用し、command検索PATHを上書きして
  `shasum`が1回だけ`command not found`になった。成果物変更前のread-only照合であり、成果物への影響はない。
  期待executorはshell予約・特殊変数を検査した構造化command、実executorはLLMによるshell文字列組立てだった。
  `artifact_path`へ変更して同一照合を再実行する。機械処理候補はshell composition lintと予約変数検査、routeは
  `manual_operation_candidate / checkpoint`とし、Issue Resolution Pilotのdurable Candidate経路が利用可能に
  なった後の昇格候補とする。

### 未実施

- Task Contract containing commit確認、WI-001以降、TODO snapshot／compaction、Resolution Verdict
- Deployment Manifest、package builder、原子的切替、rollbackのWork 7実装
- Work 4のDesign差分、代表シナリオ、最初のvertical sliceの選定
- Project Bindingのdurable保存
- 実施報告照合の自動Claim抽出、Provenance対応、完了state結線
- private transcriptの長期retention、削除、application-layer暗号化、backupの運用判断
- session hook／Desktop監視／Claude hook／scheduler／background serviceの有効化

### 残余risk

- operational保存物はproject外の一時development rootにあり、Completion CandidateへidentityとDigestを固定した。
- Layout validatorはWork 1A固定規則のbootstrap oracleであり、正式製品Runtimeではない。
- documentation revision v16は`digest-only`の履歴として残るが、現行固定入力とWork 1A Evidenceは
  Gitから再構築可能である。
- Intent／用語集候補のfrontmatterはpromotion前snapshotである。現行authorityは外部Approval Decisionと
  承認対象Digestであり、候補fileを第二正本にはしない。
- session `001`と旧candidate Digestは問題発生Evidenceとして保持し、current判断関門には使用しない。
- 現行Planと追加13要件はprovisional／review-candidateであり、baseline確認だけで承認済みにしない。
- coverage matrixの現行authorityは外部Approval Decisionであり、候補fileを第二正本にしない。
- identity／stale規則とRequirements配置規則の現行authorityは外部Decisionと承認対象Digestであり、候補fileを
  第二正本にしない。CI adapter、Build Artifact実装、provider操作は引き続き対象外である。
- B1に従いdirectory、schema、validator、legacy inventory、50 definition、candidate、Evidence、Human
  Decision、authority bundle v2を作成した。旧legacy bindingとauthority v1はsuperseded履歴として保持し、
  現行authority chainは50 definitionだけで`effective`である。
- NFR Profile接続はHuman Decisionで承認済みである。effective Requirementを初期Profileのauthorityとし、Planの
  Architecture Policy rule 6件は`proposed_policy_rule_not_authoritative`としてWork 4へ分離した。数値閾値、
  Architecture Policy、shared／distributed scopeは承認・実装していない。
- deferred scope候補はHuman承認済みで、13件すべてを初期releaseの`nonblocking`へ固定し、9 consumerの
  scope leakは0だった。各機能の実装・有効化は別Task ContractとHuman判断まで開始しない。
- 旧37 Requirementは機械移行済みで、現行effective authority v2は50 definition、legacy binding 0である。
  authority v1とlegacy bindingはsuperseded履歴として保持し、削除または上書きしない。
- 公式Testはpolicy runner経由へ変更した。raw `python3 -m pytest -q`はrunner内部commandであり、今後の完了
  Evidenceにはrunner receiptを要求する。
- Policy v5により、今後の作業後報告は手戻りと手作業の因果、期待／実executor、Evidence、機械処理候補、
  routeを含む。決定的処理をLLMが行った場合は、手戻りがなくても改善候補として報告する。
- eventual preservationのmanual collector、durable cursor、reconcile、artifact分離と限定captureは完了した。
  capture後に追記された会話は次のmanual reconcile対象である。自動実行は未実装・未有効化であり、
  hook／watcherをcorrectness pathにはしない。

## 次に行う一作業

実装Task Contract作成・検証作業単位をcommitし、commit後のread-only照合で同一bytesがHEADに存在すること、
worktree clean、work unit transition合格を確認する。WI-001は開始しない。

開始条件：

- Task Contract SHA-256が`661df56b9f2c78a261e3b345e727bf9cd47bbf09225186c529cceadf32eb56cd`、
  Completion Evidence SHA-256が`591b786b3128bde56d2d4c92af1b5883ec0c2323de5973758dab809f1b64d6f1`である。
- Plan v3 SHA-256が`07cd477a463e4536f6aa208153d6fdf401cfd0d8c00909cdc61fea5fdc26c304`、
  Challenge v3 SHA-256が`6a640598a715f4e7dea81e7891da5836a1ee0cf47f962ca9a02fb6eec18e2e67`である。

完了条件：

- Task ContractとCompletion Evidenceが同じcontaining commitからbyte-identicalに読める。
- commit後read-only照合で`implementation_ready`を導出し、worktreeがclean、transitionが`passed`になる。
- WI-001、snapshot、TODO圧縮、Issue解決を先取りしない。

後続作業：containing commit確認後だけ`implementation_ready`へ進み、別作業単位でWI-001のREDを開始する。

## blocker・Human判断待ち

- blocker：work unit transition preflightを正本とする。完了済み作業単位とdirty worktreeが同時に成立する間は、
  `completed_work_unit_uncommitted`として次作業へ移行しない。
- Human判断待ち：現在の次作業に対する追加判断なし
- 実行保留：WI-001、milestone snapshot、TODO compaction。Task Contract作業単位のcommit後に再開する
- 後続Human判断待ち：2026-09-03のretention review、暗号化、automation activation
- 再開条件：work unit transition preflight合格とTask Contract、Completion Evidence、Test receiptの一致を確認する

## stale・deferred

- stale：permanent remediation receipt v1とunified formal Evidence v1はrunner修正前stateのため判断対象外。
  currentはreceipt v2とformal Evidence v2。promotion GREEN receipt v1は負例追加前stateで、currentはv2。
  authority v1はv2にsupersededされた。NFR／deferred候補のidentity再検証は合格し、双方freshでHuman承認済み。
  Plan v2、Challenge v2、Plan v2 Approval Decisionはstate gap発見前の履歴として保持し、Task Contract判断には
  Plan v3、Challenge v3、Plan v3 Approval Decisionを使用する。
  その他の旧candidate／sessionは従来どおりsuperseded保持する。
- deferred：画面UI、As-Built projection、AI判断委譲、shared／distributed deployment、改善候補・
  Issue Resolution・実施報告照合の正式automation、汎用Task Registry／plugin system。Issue Resolutionの
  development限定早期PilotはIssue／Plan作成まで完了したが、正式schemaまたはWork 8正式Pilotを前倒ししない。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- private raw／逐語録／cursor／Provenance／ledgerはrepository外で、Git対象外
- 直近の関連検証：実装Task Contract専用`5 passed in 0.02s`
- 直近の全Test：`562 passed in 2.57s`、fallback `false`
- 差分検査：`git diff --check`合格

## 更新規則

- session終了時に、現在位置、実施報告照合、未実施、次の一作業、blocker、stale、Git／Test、
  参照Digestを更新する。
- 報告だけでClaimを`verified`にせず、Evidenceと観測した事後状態を記録する。
- 手戻り時は手作業との因果を確認し、原因または原因候補なら機械処理候補とrouteを記録する。
- TODOは現行handoffだけを保持し、過去sessionの時系列logにしない。
- Stage変更、長期中断、大きな計画改定など、独立保持する価値がある場合だけ
  `records/session-handoffs/`へ日付付きの不変snapshotを作る。
- 通常のsession履歴と完了EvidenceはSession Evidence、Decision、Provenance、Gitへ保存する。
