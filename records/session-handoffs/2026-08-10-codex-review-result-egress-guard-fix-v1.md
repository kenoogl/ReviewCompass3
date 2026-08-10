# group E（外部送信・機微境界）修正 完了レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- レビュー段階：completion
- risk：`high`（Human確定済み）
- 判定：`verified`
- Finding：blocking 0件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象、許可範囲、開始状態

- 対象レビュー依頼：
  `records/session-handoffs/2026-08-10-claude-pilot-egress-guard-fix-review-request-v1.md`
  （commit `8d823cf3a8c4bccded8399759a68a9443e964c62`）
- 対象Finding：
  `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-e-v1.md`
  （commit `8a7da31`、blocking 7件）
- 有効な範囲固定：scope v2（`4b52776`）＋scope v3（`8d2f3a4`、RED定義の改定）
- 合格済み範囲レビュー：v2（`4e9ce51`、`verified`）
- 判定基準：`docs/development/work-review-protocol.md` §3、§4.7、§6、§11
- 許可範囲：読取り、一時領域での独立Test・反証・変異検査、本文書1件の新規作成と単独commit
- 禁止範囲：code、test、既存record、config、schema、上流設計、TODO、checklistの変更、
  実際の外部送信、push、tag、amend、rebase、reset、履歴書換え

【実測】開始branchは`main`、開始HEADは`8d823cf3a8c4bccded8399759a68a9443e964c62`、
開始時の`git status --short --branch`はbranch行だけで、tracked・untracked差分はなかった。
対象依頼commitの親は`2bd9d66559e05347e50f81d146d0369fcb033cee`で、依頼書1件の追加だけだった。

【実測】本recordの確定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test ! -e`は終了コード0で、ignore対象外かつnew-onlyだった。

## 2. 判定

【判断】判定は`verified`である。必須Evidenceが揃い、レビュー依頼のClaimとrepositoryの
事後状態が一致し、scope v2 §5とscope v3 §2〜§4の受入条件を満たした。

【判断】§4.7・§6の停止類型に該当する根拠はない。必須Evidenceまたは再現条件の不足がないため
`reported_unverified`ではなく、報告と事後状態の競合がないため`report_execution_mismatch`ではない。
停止条件への途中到達でも未実行でもないため、`blocked`、`not_executed`でもない。

## 3. Finding（§11の閉じた区分）

| 区分 | 段階 | 件数 | 根拠 |
| --- | --- | ---: | --- |
| blocking | completion | 0 | 【判断】類型1（上流矛盾）、類型2（Human境界欠落）、類型3（誤った合格）、類型4（禁止事項・scope・schema境界破り）の成立Evidenceなし |
| non-blocking | completion | 0 | 【判断】実装方式の好み、将来設計、scope外提案をFindingへ持ち込んでいない |
| defer | completion | 0 | 【判断】本レビューで新たな後続slice候補は導出していない |

【判断】group E判定recordのF-E1〜F-E7を止めていた11反証は全て不成立となり、7件のblockingは
本修正単位の受入条件として解消した。これは過去recordの履歴を書き換える判断ではなく、
commit `8d823cf`時点の完了判定である。

## 4. 反証11件の逐一照合

### 4.1 実行方法

【実測】前回反証script
`/private/tmp/codex_group_e_adversarial.py`は残存し、SHA-256
`7906a65a20cb70ee56640ee01165927faa879d07bc8d96fbdac0309aa78c7c79`でgroup E判定recordの
記載値と一致した。ただし修正後APIでは承認の呼出し契約が変わったため、攻撃入力を維持し、
正常な承認経路だけを新契約へ置き換えた独立scriptを一時領域に作成した。

【実測】独立scriptは
`/private/tmp/codex-egress-review.jXeydG/independent_adversarial.py`、SHA-256
`465f49f95fdbc6317c876ba12c66ef27bd491e4587397d9e2bbe7cf56ef2c811`だった。
各caseは別の`TemporaryDirectory`だけへsource、承認file、痕跡file、生ログ、backup、台帳を作り、
ネットワーク機能を使わず、各caseを単独commandで実行した。終了コード0を安全側の期待成立、1を
反証成立と定義した。

```text
env PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 \
  /private/tmp/codex-egress-review.jXeydG/independent_adversarial.py <ID>
```

### 4.2 結果

| ID | 同じ攻撃入力の照合結果 | 終了コード | 判定 |
| --- | --- | ---: | --- |
| A1 | 【実測】永続record pathのない承認辞書と旧`now`引数は、`approval_record`が未受付のため関数入口で`TypeError` | 0 | 不成立 |
| A2 | 【実測】`consumed`を欠いた辞書は`ApprovalError`。理由に`consumed must be present and boolean`を含み、期限切れも同時検出 | 0 | 不成立 |
| A3 | 【実測】caller指定の過去`now`は未受付で`TypeError`となり、比較時刻の逆行を注入できない | 0 | 不成立 |
| P1 | 【実測】断片本文だけを`OUT_OF_RANGE_PRIVATE_TEXT`へ替え、旧Digestを残した入力は`PayloadError` | 0 | 不成立 |
| G1 | 【実測】送信JSONの`fragment_a`を自由文だけの辞書へ替えた入力は、payload fieldとの不一致で`allowed=false` | 0 | 不成立 |
| G2 | 【実測】許可field名`line_count`へ自由文を入れた入力は、値の型違反で`allowed=false` | 0 | 不成立 |
| G3 | 【実測】合成AWS access key、GitHub token、PEM秘密鍵headerを含む入力は走査1件以上となり、伏字化変化と資格情報検出の両方で`allowed=false` | 0 | 不成立 |
| F1 | 【実測】`body_weight=NaN`は`PrefilterError`（`must be finite`） | 0 | 不成立 |
| S1 | 【実測】任意callbackはgateとstage-one runnerの双方で拒否。gate側・sender側の痕跡fileはいずれも存在せず、senderは`EgressGateRefusal`で停止 | 0 | 不成立。拒否前副作用なし |
| R1 | 【実測】改変backupの再保全は`PreservationIntegrityError`。台帳Digestは元値のまま、復元も拒否され、rawは再生成されなかった | 0 | 不成立 |
| R2 | 【実測】root外sourceを指すsymlink読取りと、backup root外を指す祖先symlink書込みを別々に拒否。root外fileは作成されなかった | 0 | 不成立 |

【判断】11／11件が同じ欠陥類型の入力に対して安全側となった。S1は例外発生だけでなく、拒否前の
外部観測可能な副作用が0であることまで機械確認した。

## 5. 正例とReviewer新作反証

【実測】64桁hexを2個含む通常の`EgressPayload`を組み立て、承認fileと許可された伏字化hookを結線した。
`scan_outbound_text`は0件、gateは`allowed=true`、単独commandは終了コード0だった。F-E3の
偽陽性側の正例は成立した。

【実測】`high` riskのReviewer新作反証として、PilotのG2 fixtureにない「整数allowlist fieldの
`line_count`へPythonのbool値`True`を入れ、送信JSONとpayload fieldの両方を自己整合させる」変種を試した。
boolを整数として合格させず、型違反で`allowed=false`、終了コード0だった。

## 6. REDと既存Testの検査性質

### 6.1 REDの独立再現

【実測】元repositoryを`git clone --no-hardlinks`で
`/private/tmp/codex-egress-review.jXeydG/tree`へ複製し、RED commitをそれぞれcheckoutして単独実行した。

| RED | command | 結果 | exit code |
| --- | --- | --- | ---: |
| RED-1 `ea7ccbb` | scope v3記載のegress 6 test file | 63 failed / 44 passed | 1 |
| RED-2 `f78a57e` | `pytest -q --tb=line tests/test_session_log_preservation.py` | 4 failed / 4 passed | 1 |

【実測】RED-1の63失敗は、旧`now`必須のため新呼出しが失敗する`TypeError`、
`load_approval_file`・`APPROVED_REDACTION_HOOK`の不在による`AttributeError`、資格情報見逃し・
64桁hex誤拒否・反証を拒否しない`AssertionError`／`DID NOT RAISE`だった。RED-2の4失敗は、
改変backup正当化とraw・backup・復元先のsymlink脱出を拒否しない`DID NOT RAISE`だった。
したがって失敗理由は反証または新契約の不在であり、環境不全や無関係な既存失敗ではない。

【実測】更新していない既存testはRED-1の`tests/test_egress_dry_run.py`が4 passed、RED-2の
既存4件が4 passedだった。

### 6.2 Evidence §2.1と実diffの照合

【実測】`ea7ccbb^..ea7ccbb`の実diffをEvidence §2.1と照合した。列挙された更新は次の全件と一致した。

- `TestValidateApprovalRecord`の正例・10違反と`TestConsumption::test_mark_consumed_is_permanent`：
  `now=`除去、正例期限を将来、期限切れ入力を過去へ更新
- `TestGateAllows` 1件、`TestGateBlocks` 5件、`TestStageOneSender` 2件：承認file path＋Digest、
  `APPROVED_REDACTION_HOOK`、`now=`除去へ更新
- `test_redaction_masking_anything_is_blocked`：許可された伏字化実装が内容を変更する入力へ更新
- `TestForgedContent` 3件：共通helperを新承認file契約へ更新

【実測】既存testの削除は0件だった。差分で削除された44行は旧呼出し引数・旧固定時刻・任意lambda・
重複した承認辞書構築であり、対応する検査本体は残っていた。追加は新規反証と新契約用helperだった。

【判断】`test_redaction_masking_anything_is_blocked`の旧版は、任意lambdaで本文を変更した場合の拒否を
確認していた。新契約では任意lambda自体を実行前拒否するため、同じ安全性質を検査するには、唯一許可された
伏字化実装が本文を変更した場合の拒否を確認する必要がある。置換後はこの形になっており、検査性質を
弱めていない。

【実測】上記の独立確認として、現行commitの対象test単独は1 passed、gateの
`masked != payload.content`時の拒否処理だけを一時複製から除く変異検査では1 failed、終了コード1だった。
対象testは「許可実装が内容を変えたら拒否する」処理の欠落を検出した。

## 7. commit境界と禁止path

| commit | 実際の変更path | scope v2 §6との照合 |
| --- | --- | --- |
| `ea7ccbb` RED-1 | 【実測】`tests/test_egress_adversarial.py`、`test_egress_approval.py`、`test_egress_gate.py`、`test_egress_payload.py`、`test_egress_prefilter.py` | 一致 |
| `e7c25fa` GREEN-1 | 【実測】`tools/egress/`の指定5 file、Evidence新規、slice 1 receipt新規 | 一致 |
| `f78a57e` RED-2 | 【実測】`tests/test_session_log_preservation.py`のみ | 一致 |
| `2bd9d66` GREEN-2 | 【実測】`tools/session_logs/preservation.py`、同一Evidence追記、slice 2 receipt新規 | 一致 |

【実測】4 commitはscope v3→RED-1→GREEN-1→RED-2→GREEN-2の直列親子関係だった。
各commitに対する単独`git diff --check <sha>^ <sha>`は全て終了コード0だった。

【実測】`git diff --name-status 8d2f3a4..2bd9d66 -- docs/design config schema schemas records/requirements`
は出力なしだった。上流設計、config、schema、Requirementsの変更はない。

## 8. Digest再計算

【実測】現行fileからSHA-256を再計算し、レビュー依頼§4とEvidence §6・§7.5の記載値に全件一致した。

| file | 再計算したSHA-256 |
| --- | --- |
| `tools/egress/approval.py` | `cb8f97e1d2b05f0ec7e9bad9e045c80b8378a03167be2d623f13853c3236b243` |
| `tools/egress/gate.py` | `ec611dfa65c0ff8f8ccf586ed491e944430cf80952a797861ea3b06a7f1de0c1` |
| `tools/egress/payload.py` | `daeb48b1ef3c00f7ae14ba1debfaba7efe564387808e505d57e4c15a14d34a1f` |
| `tools/egress/prefilter.py` | `c0b6a2da30923802eb419817d55bf8c2eb1f2e6a9a580074b1f90cd77773bf43` |
| `tools/egress/sender.py` | `05286fe21ee5baf264c80fe8518eccef3602de1c7ada6041e121dd4a2b5bbef8` |
| `tools/session_logs/preservation.py` | `645e2430c15fe8bd8c4cabc94a21349335902299abefc533e9b363b02725ea5e` |
| `tests/test_egress_approval.py` | `1cb52dc85a979a553b70964934dfd7544e8a34d9798f19006bb2e511c639dffb` |
| `tests/test_egress_gate.py` | `bd463b8013fe8df46598120c4aa329e765046b6c326d5076faebeaf0b199dfe4` |
| `tests/test_egress_payload.py` | `3bcac6b0fac87e93f878218d635a6621b9ff1184c6825ed72c58cbbc03e37f58` |
| `tests/test_egress_prefilter.py` | `6e44b223bd3b5b444832e0c5ac4d32b13b11d32099575ef1a7aa9ab9c429da1f` |
| `tests/test_egress_adversarial.py` | `e865785bbe30536adae69897cd63144e436dc290b5e27c61b76afada0f254da6` |
| `tests/test_session_log_preservation.py` | `bacb8ed2cff642269c2c3bd8762a043c07e4f5cd6f841dd3143e5bbddeff35f1` |
| Evidence | `b3b78f98fb3ee8e035ddcf983f0e1c17c619deac1b949c127a6d98e78dfb6394` |
| slice 1 receipt | `c4c1a9287483ddb925cae86634368d63e40c66f534794d0c8ae5a36fc55ef34a` |
| slice 2 receipt | `dfa98e0f5d01e877cc8654eeec957c9a1942b0aa2cb94bd858d7c7329e333b06` |

【実測】固定上流のDigestもscope v2記載値と一致した。出口設計v4は
`3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd`、Session Log保全設計は
`b387b9cf913b11a0d39e13cbd5aa6222527fdb4f801e478f1110683c3dd8d1fe`、group E判定recordは
`a4bc656cdfe73188b1def7bc107a98a1027daf289dc3b6ab254b9808d3c86a33`だった。

## 9. 独立Test再実行

| 区分 | 単独commandの対象 | 結果 | exit code |
| --- | --- | --- | ---: |
| targeted | egress 6 test file | 【実測】107 passed | 0 |
| targeted | `tests/test_session_log_preservation.py` | 【実測】8 passed | 0 |
| 関連回帰 | eventual preservation、migration、redaction登録保全経路、pipelineの4 file | 【実測】36 passed | 0 |
| 公式全Test | `policy_test_runner --suite full`、一時receipt | 【実測】1427 passed、failed 0、errors 0、skipped 0、status `passed` | 0 |

【実測】公式全TestはPython 3.9.6、pytest 8.4.2、fallback falseだった。一時receiptは
`/private/tmp/codex-egress-review.jXeydG/full-test-receipt.json`、SHA-256
`903955737f327939dce6ed5f095fcc2a032f0e508f82b004a61ab285f445df97`だった。実行後の元repositoryの
`git status --short --branch`もbranch行だけだった。

## 10. 上流設計、Human境界、禁止事項

【記録】出口設計v4 §3〜§6・§8は、送信物をcode断片・許可された機械特徴・定型文の3種へ閉じ、
現在sourceからの由来解決、送信物一覧とHuman承認recordの結線、秘密値走査、伏字化で内容が変わる場合の
停止、単一関門、段階1の送信不能を要求する。

【実測】F-E1〜F-E5の現行実装は、承認file path＋Digest、実時刻、厳密な`consumed`、送信JSONと
payload fieldの相互照合、資格情報3形式、64桁hex除外、閾値の有限性・範囲・関係、許可hookの実行前同一性
検査を持つ。11反証、正例、Reviewer新作反証、対象Testがこれらの境界を機械確認した。

【判断】F-E1〜F-E5は、新しい送信段階・payload種別・送信機能を導入せず、出口設計v4の既存要求へ適合する。

【記録】Session Log保全設計 §5.3・§8・§10は、rawの追記専用保全、prefix検査、atomic replace、lock、
integrity ledger不一致時の停止、許可したsource root外を探索しないことを要求する。

【実測】F-E6・F-E7の現行実装は、既存backupを台帳へ先に照合し、raw・backup・復元先を解決後rootへ
束縛する。R1・R2、保全対象Test、関連回帰が、台帳不一致停止、追記・復元、root外読書き拒否を確認した。

【判断】F-E6・F-E7は保全設計§5.3のprefix・atomic replace・lock・integrity ledgerを維持し、
同設計§8・§10の不一致停止と許可root境界へ適合する。

【実測】`tools/egress/`の通信facility検索は該当0件で`rg`終了コード1だった。本レビューでもsocket、HTTP、
provider API、外部connectorを呼んでいない。実際の外部送信は行っていない。段階1は正常関門通過後も
`EgressSendingNotApproved`となる既存testが合格した。

【判断】Humanのrisk確定、資格情報3形式、64桁hex除外、RED定義改定の承認境界は維持された。
group A〜D、TODO・checklist反映、段完了projectionは未実施のままである。

## 11. 結論と次の一作業

【判断】修正対象commit列とcommit `8d823cf`のレビュー依頼は`verified`である。group Eのblocking 7件は
本完了レビューの受入条件上解消し、次段判断の根拠に使える。

【提案】次の一作業は、Closerが本review resultを再読込みし、レビューとは別の作業単位・別commitで
完了Evidence、TODO、checklist、transitionを反映することである。本commitにはそれらを含めない。
