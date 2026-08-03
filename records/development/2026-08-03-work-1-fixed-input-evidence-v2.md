---
evidence_id: RC3-WORK1-FIXED-INPUT-2026-08-03-V2
evidence_version: 2
recorded_at: 2026-08-03
work_id: Work 1
work_name: 固定入力と開発入口
status: verified
workflow_state: completed
confidentiality_class: project-internal
---

# Work 1 固定入力Evidence v2

## 1. 結果

Work 1 Evidence v1で検出したdocumentation revision v16のProvenance不一致を、v16を上書きせず
corrective snapshotへ記録した。corrective snapshotを含むcommitから固定入力を再読込し、manifest
13件、source catalog 10件、前身inventory 2件がすべて一致した。

この結果により、v16自体は`digest-only`として履歴に残し、Work 1が使用する固定入力はcommit
`ee60e3b4baf74c60da949a9d04d793fb83a61e69`から再構築できる。Work 1のblockerは解消し、次の一作業を
Work 1A「Layout Baseline」とする。

## 2. 先行Evidenceと修復authority

| role | path／identity | SHA-256／commit | 結果 |
|---|---|---|---|
| blocked Evidence | `records/development/2026-08-03-work-1-fixed-input-evidence.md` | `d07c5abdce7bc4b3322e7c6f973feb0e00d7218151dafe7013aff5d08148b879` | v1を上書きせず保持 |
| blocking candidate | `IC-WORK1-DOC-RECONSTRUCTABILITY-001` | `4206805e3066335c5a84a56baa839e4b074da4b5af1f8cd17b20bcbe22860404` | 修復routeを実行 |
| Human Decision | `WORK1-RECONSTRUCTABILITY-REPAIR-DEC-001` | `d8da18034eabaa38dcd80f2648a7484ed516ce0dfadce91f819ba436956e7576` | bounded repair承認 |
| corrective snapshot | `WORK1-CORRECTIVE-SNAPSHOT-2026-08-03-V1` | `08365d976f020b428c46d1f83b14d7b0861beb335103493cf81823a144cc25c4` | commitへ固定 |
| snapshot commit | `ee60e3b4baf74c60da949a9d04d793fb83a61e69` | tree `a887507515ff15293660d7c5df2080325f534049` | immutable source |
| post-commit verification | `WORK1-CORRECTIVE-SNAPSHOT-2026-08-03-V1-POST-COMMIT` | `a1cfb19122c94d7e0edbf37b61e30f0ecd69c2aca461f7aba66b4e7e60ff6ad8` | passed |

## 3. 固定入力

固定入力のidentityはcorrective snapshot manifestを正本とし、内容はsnapshot commitから解決する。

| category | fixed source | 検証 |
|---|---|---|
| Intent候補 | `docs/current/reviewcompass3-intent-current.md` | manifestとcommitのSHA-256一致 |
| 統合用語集候補 | `docs/current/reviewcompass3-glossary-current.md` | manifestとcommitのSHA-256一致 |
| 現行計画候補 | `docs/current/reviewcompass3-plan-current.md` | manifestとcommitのSHA-256一致 |
| operational policy／Decision | 開発方針と`development-policy-v4.json` | manifestとcommitのSHA-256一致 |
| source catalog | 10件のsource record | catalog記録Digestとcommit内容が全件一致 |
| predecessor baseline | ReviewCompass／ReviewCompass2固定commit、tree、inventory | inventory 2件一致 |
| historical reconstruction | v1〜v15 auditとv16 record | v16を`digest-only`として保持 |
| Work 1 repair chain | v1、candidate、Human Decision、corrective snapshot | manifestとcommitのSHA-256一致 |

Intent、用語集、計画はHuman承認前の候補であり、Work 1完了はpromotion、段完了または製品実装開始を
意味しない。

## 4. scope、非目標、confidentiality

### scope

- authority、baseline、source identity、適用範囲、非目標の固定。
- 既知Finding、未承認事項、Human判断、blocking conflictの列挙。
- 最小Evidence Extraction ContractとConsumption Closure。
- 固定入力変更時のstale化、停止、再開入口。
- v16 reconstructability gapの訂正とWork 1固定入力の再構築可能性回復。

### 非目標

- Intent、用語集、計画またはv16の意味変更・上書き。
- Work 1AのLayout Baseline、空配置fixture、root解決規則。
- Work 1BのSession Log BootstrapとCurrent Work Projection tooling。
- Requirements、Task Contract、schema、validator、製品codeの実装。
- 外部送信、外部source再取得、raw会話・raw reviewの取込み。
- AI判断委譲、shared／distributed deployment、画面UI、汎用Task Registry／plugin systemの前倒し。

### confidentiality

固定入力は`project-internal`として扱う。catalogが`digest-only`または`git-object-pinned`とするsourceは、
固定済み派生record、Digest、Git objectだけを使用する。端末上の原文再取得、raw内容の複製、外部送信は
行っていない。

## 5. 未承認事項と既知Finding

### 未承認事項

- Intent、統合用語集、現行計画、新しい第5段相当のHuman承認。
- Layout Baseline、Session Log Bootstrap、関数台帳baseline、最小Review Task Contractの作成・承認。
- Work 5Aの製品実装開始permit。

これらは後続関門であり、Work 1Aの配置文書・fixture作成を止めるblockerではない。

### 既知Finding

- v1〜v15のreconstructability auditに記録された`digest-only` revisionは履歴上の残余riskとして残る。
- v16の18件中5件不一致はcorrective snapshotで訂正した。v16を`git-reconstructable`へ昇格していない。
- rawを保持しない`digest-only` sourceは、catalog内の派生recordを越える主張に使用しない。

Work 1 scopeに残るblockingなIntent／Requirement／Plan競合または固定入力Provenance欠落はない。

## 6. Evidence Extraction Contract

| 項目 | 固定規則 |
|---|---|
| 開始集合 | corrective snapshot manifest 13件とsnapshot commit |
| 展開規則 | authorityの直接参照、source catalogの10 `record_path`、baselineの2 inventory、PlanのDeferred／停止／実装条件だけを一段展開する |
| 分類 | `adopt | adapt | reject | defer` |
| 終了条件 | Work 1の7確認項目と2完了関門へsourceまたは明示的な後続gateを割り当て、未分類候補が0件になる |
| 除外 | catalog外source、raw会話、raw review、外部再取得、製品code探索 |
| 完全性oracle | snapshot commitからmanifest 13件、catalog 10件、inventory 2件を再読込し、Digest不一致が0件である |

完全性oracleはpost-commit verificationで合格した。

## 7. Consumption Closure

source catalog 10件の`adapt`先はv1のConsumption Closureを維持する。修復で変更した消費関係は次のとおり。

| source／Finding | disposition | consumer／Outcome |
|---|---|---|
| v16 manifest不一致 | adapt | corrective snapshotでv16を`digest-only`へ訂正 |
| Human修復Decision | adopt | bounded provenance repairのauthority |
| corrective snapshot manifest | adopt | Work 1固定入力のimmutable source |
| post-commit verification | adopt | manifest 13件、catalog 10件、inventory 2件の合格Evidence |
| Human承認前authority | unresolved downstream gate | Work 2〜4とWork 5A前のHuman approval |
| Deferred Work | defer | 現行Plan 14節とchecklist後続節 |

必須sourceと採用Findingはconsumerまたは後続gateへ接続済みであり、Work 1のConsumption Closureは完了した。

## 8. stale化と再開規則

次のいずれかが変わった場合、本EvidenceとWork 1完了をstaleにする。

- snapshot commitまたはcorrective manifestのidentity。
- authority 3文書のpath、Digest、promotion状態または相互参照。
- source catalogのentry、record Digest、confidentiality、reconstructability。
- predecessor baselineのcommit、tree、inventoryまたは適用範囲。
- Work 1のscope、非目標、Deferred境界、停止条件。
- post-commit verificationの対象identity、oracleまたはverdict。

変更時はv2を上書きせず、新versionで影響閉包、manifest、catalog、inventoryを再照合する。不一致があれば
Work 1Aをpauseし、修復EvidenceまたはHuman Decisionが揃うまで再開しない。

## 9. 完了関門

| 関門 | 判定 | Evidence |
|---|---|---|
| 固定入力、scope、非目標、未解決事項を一つのEvidenceから確認できる | pass | 本文2〜8節 |
| blockingなIntent／Requirement／Plan競合がない、または停止理由が明示されている | pass | Work 1 scopeのblocking conflictなし |
| fixed-input snapshotをGitから再構築できる | pass | commit `ee60e3b`、post-commit verification |

Work 1は`verified / completed`である。次の一作業はWork 1AでLayout Baselineを固定することである。
