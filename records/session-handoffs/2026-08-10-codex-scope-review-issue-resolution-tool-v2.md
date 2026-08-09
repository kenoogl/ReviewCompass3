# V4 Issue resolve tool 範囲レビュー結果 v2

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（範囲レビュー）
- 依頼された深さ：`high`
- risk判定：`high`（Human確定済み）
- 判定：`verified`
- execution state：`correctly_stopped_before_RED`
- Finding：blocking 0件、non-blocking 3件（すべて実装時確認事項）

【実測】起動時に表示されたmodel名とreasoning effortは
`gpt-5.6-sol`／`high`だった。

## 1. 固定対象と開始状態

- scope：`records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v2.md`
- scope SHA-256：`ddc4b312ca529f58c38f2ad90127e0ec5ef065b03ffb1af17c1b10076eff2ee7`
- SCOPE v2 commit：`21daf5e21b84590bfaf512bdbf1be3c364c67667`
- base：`9d8667f3d6a559d12703747e130d7e1a7b58cc41`
- branch：`main`
- 許可範囲：本判定recordの作成と単独commit
- 禁止範囲：実装、Test、既存record、config、schema、実workflow台帳、TODO、checklist、
  実Issueの状態変更、外部操作、RED開始
- 停止条件：固定入力不一致、正規検証との不両立、上流との矛盾、必要なHuman境界の欠落

【記録】今回のHuman裁定は、2026-08-10の
「#1 risk highを確定。案Bでscope v2を承認する。遷移元はregisteredのみとする」である。

【実測】SCOPE v2 commitの親は申告baseと一致し、変更pathはscope v2の1件だけだった。
レビュー開始時のworktreeとindexはcleanだった。本判定record予定pathの
`git check-ignore --no-index`は終了コード1で、ignore対象ではなかった。

【実測】scope v1の固定入力9件とscope v2で追加された2件は11／11でSHA-256が一致した。
scope v2自身も依頼値と一致し、`git diff --check 21daf5e^ 21daf5e`は終了コード0だった。

【実測】RED以後に予定されたtool、Test、GREEN Evidence、receipt、review requestの5 pathは
いずれも存在しなかった。SCOPE v2後の停止は維持されている。

## 2. 上流から独立導出した境界

主に次を、Pilotの実装案とは別の正しさの基準として照合した。

- `.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json`
  （SHA-256 `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231`）
- `.reviewcompass/workflow/triage-decisions-v4/dec-ic-v4-issue-resolution-persistence-gap-001--v1.json`
  （SHA-256 `01c3e15ab98cca964dc3776127f2205219e915a2c26bdb61ea8327a4e91db355`）
- `records/development/2026-08-09-deferred-items-triage-decision-v1.md`
  （SHA-256 `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91`）
- `docs/development/2026-08-02-development-policy.md`
- `docs/development/work-review-protocol.md`
- `config/development-issue-resolution-pilot-v4.json`
- `tools/development/issue_intake_v4.py`

【記録】正式改善候補のscopeは、Human裁定に基づく`resolved`／`rejected`遷移、既存Issue recordの
`state`と`content_digest`を正規永続化する明示CLI、二重解決・非Human裁定・stale入力・
同時active Issue不整合の拒否である。`non_scope`はV4 Issue schema変更と旧Pilot Resolution
Verdict chainの移植を除外する。

【記録】開発方針は保存と状態遷移を原則`high`とし、作業レビュープロトコルはDigest照合、
承認関門、改竄拒否などの守り役を既定で`high`とする。

【判断】上流から導出される必要境界は次のとおりである。

1. Human裁定に束縛されていない遷移、stale入力、二重解決、対象取り違えを不正なら停止する方式で拒否する。
2. 遷移元はHuman裁定どおり`registered`だけ、遷移先は`resolved`または`rejected`だけにする。
3. 更新後のrecord単体と台帳全体を現行の正規検証へ通し、失敗時は事前状態へ戻す。
4. V4 Issue schema、config、既存検証器を変更せず、解決根拠はnew-onlyの開発recordへ分離する。
5. 本sliceでは合成台帳だけを使い、実Issueの遷移はtool検証後の別作業単位に残す。
6. `high`の範囲レビュー合格後も、HumanのRED再開承認までは実装を開始しない。

## 3. 先行blocking Findingの解消確認

### IR-SCOPE-001：解消

【実測】scope v2 §1はriskを`high`としてHuman確定済みと記録し、§9は公式全Testと
Reviewerが新作する反証を完了レビューの検査として固定している。§10は本commit後、
HumanのRED再開承認待ちで停止すると定める。

【判断】先行レビューの類型1（上流authorityとの矛盾）と類型2（Human境界の欠落）は解消した。
`high`の分類、独立検査、RED前停止の三つが揃っている。

### IR-SCOPE-002：解消

【実測】現行の実Issue recordを隔離した台帳へ複製し、元の`registered`から`resolved`と
`rejected`へ一件ずつ変更した。file名と`issue_version`を保ち、`state`変更後に
`canonical_digest`で`content_digest`を再計算した両例は、次の二つに合格した。

- `validate_v4_issue_record`：2／2合格
- `validate_v4_issue_repository`：2／2合格

【実測】両例とも更新前後でdigestが変わり、台帳のfile集合と対象外Issueのbytesは不変だった。
terminal stateへ進めた対象は、台帳検証の返す有効な非terminal Issue集合から除外された。

【実測】Reviewerが新作した反証として、`state`だけを`resolved`へ変えてdigestを更新しないrecordを
`validate_v4_issue_record`へ渡した。終了コード0の確認script内で、検証器は
`v4_issue_digest_mismatch`を返して拒否した。正しいdigestへ直した同じrecordは合格した。

【実測】関連する現行検証器の回帰Testを次の単独commandで再実行した。

```text
.venv/bin/python3 -m pytest tests/test_issue_intake_v4.py tests/test_issue_intake_v4_single_candidate.py
```

結果は終了コード0、`49 passed`だった。さらに現行repositoryを
`validate_v4_issue_repository`で直接検証し、終了コード0、有効な非terminal Issue 8件だった。

【判断】案Bの「同じfile内でstateとdigestだけを更新する」形は、現行schemaと台帳identityを
変えずに正規検証へ合格できる。先行レビューで実証したnew-only複数versionの不両立を避けており、
IR-SCOPE-002の類型1・3・4は解消した。

### 遷移元`registered`限定：反映済み

【実測】scope v2 §1、§5.2、§6負例4は、遷移元を`registered`だけに限定し、`in_progress`、
`resolved`、`rejected`からの遷移を拒否すると明記している。二重解決も同じ拒否条件に含まれる。

【判断】許される状態遷移の境界はHuman裁定と一致する。具体的な例外型、停止コード、CLI optionは
境界そのものではないため、実装時確認事項へ回す。

## 4. 無変更保証と事後検証の判定

【実測】scope v2 §5.4は浅い検査を成功根拠から除外し、更新後にrecord単体とrepository全体の
正規検証を要求する。§5.5は書込み前の失敗だけでなく事後検証失敗でも元のIssue bytesへ戻し、
解決recordを残さない。§6正例3・負例9・境界例10・11は、正規検証、失敗時無変更、他recordの
byte不変、digest再計算を受入条件にしている。

【判断】事後検証は、field、path、参照、digestを検査する`validate_v4_issue_record`と、台帳集合、
terminal除外、重複、active上限を検査する`validate_v4_issue_repository`の組合せであり、今回の
上流境界に対して妥当である。失敗時にIssueと解決recordの両方を事前状態へ戻す受入条件も、
部分書込みを誤って成功扱いしない方向へ固定されている。

【判断】原子的filesystem競合防止一般へ拡張せずに、単一process内の失敗時無変更を要求する分離は、
保留中のdeferred #4を侵食しない。具体的な一時file、置換順序、rollback手順は実装方法の詳細であり、
今回のblocking対象ではない。

## 5. 上流scope／non_scopeとの整合

【判断】正式改善候補の各scopeは、scope v2へ次のように接続されている。

| 上流scope | scope v2での反映 |
| --- | --- |
| Human裁定に基づくterminal遷移 | §5.1、§5.2、§6正例1・2、負例5 |
| `state`と`content_digest`の正規永続化CLI | §5.3、§6正例1・3、境界例11 |
| 二重解決・非Human・staleの拒否 | §5.2、§6負例4〜6 |
| 同時active Issueとの整合 | §5.4のrepository正規検証、§6負例9、§9の関連回帰 |

【実測】scope v2 §5.6と§7はschema、config、既存toolの変更を禁止し、旧Pilot Resolution Verdict
chainを変更可能pathへ含めていない。解決根拠recordは`records/development/`へ置き、workflow schema
registryへ登録しない。

【判断】正式候補の`scope`と`non_scope`に矛盾はない。同時active Issue不整合を含む具体的な失敗fixtureは
実装時に固定する必要があるが、repository正規検証と失敗時無変更という受入方向は既に固定されている。
§11.2によりfixture構成はblockingにしない。

## 6. 実装時確認事項

以下はすべて`non-blocking`、確認段階は`implementation／completion`である。

1. 事後のrepository正規検証だけを意図的に失敗させ、Issue bytesが完全に元へ戻り、new-onlyの
   解決recordも残らないことを前後bytesとfile集合で確認する。同時active Issue不整合を代表例に含める。
2. Evidence pathは文字列上の相対pathだけでなく、symlinkを含む解決後pathがproject root外へ
   出ないことを確認する。new-only既存衝突でも既存fileを上書きしない。
3. `registered`以外の全宣言state、非Human根拠、stale digest、他Issue bytes改変を、PilotのTestと
   Reviewer新作反証の両方で確認する。CLI option、例外型、停止コード、一時fileと置換順序はこの段階で確認する。

## 7. 手戻り記録

【実測】最初の隔離probeは`.reviewcompass/workflow/`だけを複製したため、既存Issueが参照する
`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`を読めず、
`candidate_bundle_unavailable`で終了コード1になった。

- 対象操作：更新後repositoryの隔離検証
- 期待executor／実executor：Reviewerの機械script／Reviewerの機械script
- 手作業理由：なし
- 原因：隔離fixtureへ既存の参照先を含めていなかった
- 修復Evidence：`records/development/`も複製した再実行は終了コード0で、両terminal stateが合格
- 機械処理候補とroute：製品欠陥ではないため改善候補化しない。完了レビューの独立probeでは
  参照閉包を含む隔離fixtureを使う

## 8. 判定

判定：`verified`

変更範囲：SCOPE v2 commitはscope record 1件だけで、申告base、対象SHA-256、固定入力11件、
禁止path、停止地点と一致した。

独立再実行：現行V4検証器49 Test、現行repository正規検証、`resolved`／`rejected`への隔離in-place
遷移、digest未更新反証を機械実行した。すべて期待どおりで、blocking Findingはない。
実装前の範囲レビューであるため、新規toolのtargeted Testと公式全Testは未実施であり、scope v2 §9の
実装・完了oracleとして維持する。

Record照合：正式改善候補、Human defer Decision、deferred #1着手裁定、Humanの案B・risk・遷移元裁定、
現行config、schema相当のfield定義、正規検証器と照合した。

Human境界：`high`確定と案Bの意味的裁定は反映済みである。RED再開承認、実Issueのresolve、段完了承認は
未実施のまま維持されている。

未実施：RED、実装、新規Test、GREEN Evidence、receipt、review request、TODO、checklist、既存record、
config、schema、実workflow台帳の変更、実Issueのresolve、外部操作、次段作業。

次：HumanがSCOPE v2と本`verified`判定を確認し、RED再開を明示承認するか判断する。
