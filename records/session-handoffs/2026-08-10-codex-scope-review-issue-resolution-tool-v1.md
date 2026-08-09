# V4 Issue resolve tool 範囲レビュー結果 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（範囲レビュー）
- 依頼された深さ：`medium`の簡易範囲レビュー
- risk判定：`high`（Pilot提案`medium`は過小）
- 判定：`reported_unverified`
- execution state：`correctly_stopped_before_RED`
- Finding：blocking 2件、non-blocking 2件

【実測】起動時に表示されたmodel名とreasoning effortは
`gpt-5.6-sol`／`high`だった。

## 1. 固定対象

- scope：`records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v1.md`
- scope SHA-256：`81c3d8f1741052e46505b3101c8b58f58d11e4a0dcaf54a0680d4d59533c8f86`
- SCOPE commit：`c0ad0ee8fad679b6ba989fef84c690ea555cfb30`
- base：`8fee3856fefc6331a4eee1167963112105117a0f`
- branch：`main`
- 許可範囲：本判定recordの作成と単独commit
- 禁止範囲：実装、Test、既存record、config、schema、TODO、checklist、Decisionその他の変更、
  実Issueの状態変更、外部操作、RED開始

【実測】SCOPE commitの親は申告baseと一致し、変更pathはscope 1件だけだった。レビュー開始時の
worktreeとindexはcleanだった。本判定record予定pathの
`git check-ignore --no-index`は終了コード1で、管理対象外ではなかった。

【実測】scopeに固定された9 fileのSHA-256は9／9一致し、scope自身も依頼値と一致した。
`git diff --check 8fee385 c0ad0ee`は終了コード0だった。

## 2. 上流authorityから独立導出した境界

Pilotの実装案とTest案を正しさの基準にせず、主に次を照合した。

- `.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json`
  （SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`）
- `.reviewcompass/workflow/triage-decisions-v4/dec-ic-v4-issue-resolution-persistence-gap-001--v1.json`
  （SHA-256 `01c3e15ab98cca964dc3776127f2205219e915a2c26bdb61ea8327a4e91db355`）
- `records/development/2026-08-09-deferred-items-triage-decision-v1.md`
  （SHA-256 `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91`）
- `docs/development/2026-08-02-development-policy.md`
- `config/development-issue-resolution-pilot-v4.json`
- `tools/development/issue_intake_v4.py`

【記録】正式改善候補のscopeは、Human裁定に基づく`resolved`／`rejected`遷移、Issueのstateと
`content_digest`を正規永続化する明示CLI、二重解決・非Human裁定・stale入力・同時active Issueとの
不整合の拒否である。`non_scope`はV4 Issue schema変更と旧Pilot Resolution Verdict chainの移植を
明示的に除外している。

【記録】2026-08-08のHuman triage Decisionは実装を`defer`した。その後の
`2026-08-09-deferred-items-triage-decision-v1.md`はdeferred #1の着手を承認したが、schema変更、
現行台帳検証の意味変更、またはrisk受容を承認していない。

【判断】上流から導出される最小境界は次のとおりである。

1. Human裁定に束縛されていない状態遷移を拒否し、Issueの状態を誤ってterminalへ進めない。
2. stale、改竄、二重解決、Issue identityの取り違えをfail-closed（不明または不正なら停止）で拒否する。
3. 永続化後もV4台帳の正規検証に合格し、最新版を一意に決められる。
4. V4 Issue schemaを変更しない。既存schemaで成立しない場合は実装へ進まずHuman裁定へ戻す。
5. riskは、現行開発方針と守り役判定を適用して決め、Humanが確定するまでREDを開始しない。

## 3. Finding

### IR-SCOPE-001：`medium`提案は、状態遷移・保存・Human承認関門を`high`とする上流方針に反する

- 分類：`blocking`
- 確認段階：`scope`
- blocking根拠：`work-review-protocol.md` §11.1類型1（上流authorityとの矛盾）、
  類型2（必要なHumanのrisk確定と再開承認が未成立）

【記録】`docs/development/2026-08-02-development-policy.md`は、保存と状態遷移を原則`high`とする。
`work-review-protocol.md` §3は、Digest照合、承認関門、改竄拒否など、誤りが「誤った合格」として
現れる守り役のcodeを既定で`high`とする。role-neutral memo §3は分類競合や上位riskの疑いが残る場合、
`high`として停止するよう定める。

【実測】scope §5は、Human裁定の有無とDigest、Issue recordの改竄、最新版、terminal state、
Evidence参照、同時active Issueを検査し、通過した場合だけ`resolved`／`rejected`を永続化する。

【判断】このtoolは単なるnew-only書込み補助ではない。Humanの解決承認と台帳identityを判定する関門であり、
誤りは未承認またはstaleなIssueを正しい解決として永続化する。new-onlyで復旧可能なことは不可逆性を
下げるが、状態遷移、保存、authority、必須Provenance、identityに対する`high`根拠を打ち消さない。

【判断】本依頼は`medium`の簡易範囲レビューに限定されているため、このrecordを`high`範囲レビューの
代用にはしない。Pilotはriskを`high`へ訂正したscope v2を固定し、`high`に必要な独立oracle、
代表データ、Pilot fixtureにない反証を完了レビュー計画へ含める必要がある。その後もHumanがriskと
RED再開を明示確認するまで停止を維持する。

### IR-SCOPE-002：schema不変のままnew-only複数versionを正規台帳へ置く受入経路が成立していない

- 分類：`blocking`
- 確認段階：`scope`
- blocking根拠：§11.1類型1（上流のschema非変更境界と正規永続化要求との未解消競合）、
  類型3（誤った合格を生む受入条件の欠陥）、類型4（scope・schema境界の破り）

【実測】現行`issue_record_v2.record_fields`は、`record_kind`、`schema_version`、`issue_id`、
`issue_version`、`created_at`、`state`、`problem`、`candidate_ref`、`triage_decision_ref`、
`content_digest`だけである。解決時のHuman裁定参照またはEvidence参照を載せるfieldはない。
`triage_decision_ref`は、Issueを作成した元のpromotion Decisionとcandidateへの一致を厳密に要求するため、
解決裁定参照へ意味を差し替えられない。

【実測】現行Issueへ仮の`resolution_ref`を加えてDigestを再計算した反証を
`validate_v4_issue_record`へ渡すと、`v4_issue_field_unknown`で拒否された。したがってscope §6の
「既存fieldsで表現できる場合」という条件は、固定入力を読んだ時点ですでに成立しない。

【実測】さらに、現行v1と同じIssue IDの`issue_version: 2`／`state: resolved`を合成し、正しいpathと
Digestで検証した反証では、v2単体の`validate_v4_issue_record`は合格した一方、v1とv2を並べた
`validate_v4_issue_repository`は`v4_issue_identity_invalid`で拒否した。現行台帳検証は同じIssue IDの
複数versionを正規状態として受け付けない。

【実測】scope受入条件3が挙げる`validate_issue_record`はrecord kind、schema version、stateだけを確認し、
`validate_issue_set`は`in_progress`件数だけを確認する。unknown field、Digest、参照、path、version、
同一Issue IDの複数fileを検査しない。そのため、この2関数への合格だけでは、実台帳が正規であることを
示せない。

【判断】これはCLI optionやfixture構成の詳細ではなく、何を正規なV4 Issue履歴とするかというschemaと
台帳identityの境界である。scopeは`issue_intake_v4.py`、config、schemaの変更を禁止しているため、
実装中の工夫だけでは受入条件1〜3を同時に満たせない。

【判断】scope v2の前にHumanは、少なくとも次の意味的選択を行う必要がある。

1. schema非変更を維持し、解決根拠は書込み時の許可確認だけに使うのか、永続的なProvenanceとして
   Issueへ束縛するのかを決める。
2. new-only複数versionをV4台帳の正規形にするなら、最新版選択と過去version保持を許す検証規則、
   変更可能path、必要な上流改定を承認する。承認しない場合は、候補の正規永続化方法を再裁定する。
3. 修正後の受入条件では、浅い`validate_issue_record`／`validate_issue_set`だけでなく、永続化した
   台帳全体を正規検証するoracleを固定する。

同じ受入欠陥類型の確認として、遷移元を`registered`だけに限定するのか、全非terminal stateを許すのかも
scope v2で明示する。これは実装方式ではなく、許される状態遷移の範囲である。

## 4. 妥当だった境界

【判断】次の方向は上流と整合しており、scope v2でも維持するのが妥当である。

- 実Issueへのresolve適用をtool検証後の別作業単位に分ける。
- 既存recordを上書き・削除せず、schemaまたは許可pathの拡張が必要なら停止する。
- 二重解決、非Human裁定、stale入力、参照Digest不一致、部分書込みを負例にする。
- 実台帳、TODO、checklist、既存toolを本sliceで無承認変更しない。
- SCOPE後に停止し、risk確定と再開をHuman境界として残す。

【実測】PilotはSCOPE commit後、RED、実装、Test、Evidence、review request、実Issue変更を作らず停止している。

## 5. 実装時確認事項

次は§11.2の比例原則により、今回の追加blocking理由にはしない。修正scopeの承認後、実装・完了レビューで
確認する。

1. Evidence pathは文字列上の相対path検査だけでなく、symlinkを含む解決後pathがproject root外へ
   出ないことを確認する。
2. CLI option、stop codeの細かな割当、時刻入力、fixture構成、成功時の書込み手順をTestと実装で固定する。
   ただし既存targetの非上書きと失敗時の無変更はnew-only境界として必ず確認する。deferred #4の
   原子的filesystem競合防止一般へは本作業を拡張しない。

いずれも`non-blocking`、確認段階は`implementation／completion`である。

## 6. 判定

判定：`reported_unverified`

変更範囲：SCOPE commit自体は一致し、scope record 1件だけである。

独立確認：固定入力9／9、scope Digest、Git親子関係、diff check、現行V4 schemaと台帳検証を機械照合した。
合成した新version単体は合格したが、v1との併存台帳は拒否され、追加した解決根拠fieldも拒否された。
実装前の簡易範囲レビューであるため、製品Testと公式全Testは実行していない。

Record照合：正式改善候補、Human triage Decision、deferred着手裁定、動機Issue、V4 config、
現行`issue_intake_v4.py`と照合した。

Human境界：SCOPE後の停止は維持されている。`high` riskの確定、schema／台帳version規則の意味的裁定、
修正scopeへの再開承認は未実施である。

未実施：RED、実装、Test、Evidence、receipt、review request、TODO、checklist、既存record、config、schema、
実台帳の変更、実Issueのresolve、外部操作、次段作業。

次：HumanがIR-SCOPE-002のschema／version境界を裁定し、Pilotがrisk `high`とその裁定を反映したscope v2を
新規commitして停止する。その後、Reviewerが`high`の範囲レビューを行う。
