---
evidence_id: RC3-WORK3-SOURCE-IDENTITY-STALE-EVIDENCE-2026-08-03-V1
recorded_at: 2026-08-03T17:39:19+09:00
stage: initial-development
work: Work 3
status: verified_candidate
workflow_state: human_decision_pending
completion_authority: human
confidentiality_class: project-internal
---

# Work 3 Source Identity and Stale Candidate Evidence V1

## 1. 結果

Repository Binding、Source Snapshot、Change Set、Verification Run、Build Artifactの5種類について、
identity、stale条件、復旧、受入、対象外を構造化候補へ固定した。Test、review、Decision、commit、releaseの
5関門から必要なidentityを逆引きし、5種類すべてが1関門以上から参照されることを確認した。

本成果はHuman判断候補である。Requirements本文、現行Plan本文または製品codeは変更せず、Work 3の
2番目のcheckboxもHuman承認前は未完了のままとする。

## 2. 候補

| artifact | SHA-256／state |
|---|---|
| `records/development/2026-08-03-work-3-source-identity-stale-candidate-v1.json` | `e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc`／`human_decision_candidate` |

候補は固定source 6件のpathとDigestへ束縛した。全6件を再計算し、Digest不一致は0だった。

## 3. identity境界

| entity | 主owner | identityの中心 | 主なstale条件 |
|---|---|---|---|
| Repository Binding | `FEAT-PORTABLE-LIFECYCLE` | project、repository、binding、SCM、checkout／worktree | 別repositoryまたは別checkoutへ解決される |
| Source Snapshot | `FEAT-REVIEW-CONTEXT` | binding、base／HEAD、index、tracked／untracked、manifest、lock | 内容、dirty state、除外規則または上流bindingが変わる |
| Change Set | `FEAT-WORKFLOW-CONTROL` | base／candidate snapshot、差分、Work Item、Contract、意味、merge関係 | snapshot、実差分、意味またはmerge結果が変わる |
| Verification Run | `FEAT-HARNESSED-EXECUTION` | provider、Run／Attempt、source、selection、command、環境、raw／Evidence | source、selection、実行環境、rawまたは必須Testが変わる |
| Build Artifact | `FEAT-PORTABLE-LIFECYCLE` | content digest、source、Change Set、build、platform、Verification | artifact、source、build、platformまたはVerificationが変わる |

共通規則は次のとおりである。

- branch名は移動可能な参照であり、耐久identityにしない。
- dirty worktreeではcommit SHAだけをSource Snapshot identityにしない。
- untracked fileはmanifestへ含めるか、固定した除外規則と理由を持たせる。
- retry／rerunは旧Attemptを上書きせず、新しいidentityを作る。
- 古いEvidenceは削除または上書きせず、staleとして履歴に残す。
- CIのgreen表示をsource／Evidence照合なしにReviewCompass3の受入へ変換しない。

## 4. 対象一致関門

| gate | 必須binding | stale化の要点 |
|---|---|---|
| Test | Source Snapshot、Change Set、Verification Run | sourceまたは実行identityが変わる、必須Testがない |
| review | Source Snapshot、Change Set、Verification Run | 対象source、scope、criteria、materialsまたはVerificationが変わる |
| Decision | Source Snapshot、Change Set、Verification Run | 承認対象、Evidence、authority scopeまたは受入の真偽が変わる |
| commit | Repository Binding、Source Snapshot、Change Set、Verification Run | commit treeが承認snapshotと違う、未検証差分を含む |
| release | Source Snapshot、Change Set、Verification Run、Build Artifact | source、build、platform、promotionまたはartifactが違う |

必須の関係鎖は
`Requirement -> Task Contract -> Change Set -> Source Snapshot -> Verification Run -> Build Artifact -> Release`
の7段階とした。Build Artifact実装前でも、前段のidentityを後から接続できるfieldを初期schemaへ残す。

## 5. 機械監査

構造監査では次を確認した。

```text
candidate_sha256=e697ba20409bfe32094103a5a2fa4a68ee0b43f60f12dd440f8bd1e155b871fc
entities=5 gates=5 source_digests=6 relation_steps=7
AUDIT_OK
```

- entity IDは期待する5件と一致し、欠落・重複・余剰は0。
- 全entityにowner、関連Requirement、identity、stale、復旧、受入、対象外がある。
- gate IDは期待する5件と一致し、未知のentity参照は0。
- 5 entityは全件が1つ以上のgateから参照される。
- 固定source 6件のDigest不一致は0。
- candidateのauthorityは`proposed_only`、承認前の効果は`none`である。

最初の監査表示コマンドは集計用の引用符ミスで結果表示前に停止した。候補は変更せず、引用符依存を除いた
同じ監査を最初から再実行して上記`AUDIT_OK`を得た。これは候補内容または製品codeの不具合ではない。

## 6. 初期scopeとDeferred Work

初期scopeはSCM非依存の論理identity、read-onlyなlocal Git capture、local Verification Run、source不一致等の
negative fixture、および後続CI／Build Artifactへ必要なrelation fieldである。

CI adapterはlocal deployment E2Eと実project需要まで、Build Artifact実装とpromotionはWork 7Bまで、
push、pull request、merge queue、CI起動などのprovider操作は初期scope外とした。これらを今回実施したとは
扱わない。

## 7. Authorityと判断対象

- 候補は`proposed_only`であり、Human DecisionなしにRequirements authorityを変更しない。
- 承認対象は候補Digestに固定した5 entity、5 gate、7段階relation、初期／deferred境界である。
- 承認はRequirements／Plan本文改定、Work 3後続項目完了、製品実装、commitまたはpushを含まない。

Human判断候補は次の二択とする。

1. 現行候補を承認し、Work 3の2番目の項目を`verified / completed`とする。
2. 変更が必要なentity、gateまたは規則と修正内容を指定する。
