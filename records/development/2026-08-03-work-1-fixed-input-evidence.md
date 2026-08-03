---
evidence_id: RC3-WORK1-FIXED-INPUT-2026-08-03-V1
evidence_version: 1
recorded_at: 2026-08-03
work_id: Work 1
work_name: 固定入力と開発入口
status: blocked
blocking_state: pause_and_triage
confidentiality_class: project-internal
---

# Work 1 固定入力Evidence

## 1. 結果

固定入力、scope、非目標、未解決事項、Evidence Extraction Contract、Consumption Closure、stale規則を
本Evidenceへ集約した。現行authority 3文書の相互参照とchecklist記載Digestは一致し、開始時のGit
worktreeはcleanだった。

ただし、前身documentation revision v16のimmutable snapshotを再構築できない不一致を検出した。
必須Provenanceとsource identityへ影響するため、Work 1の結果は通常完了ではなく`blocked`、routeは
`pause_and_triage`とする。停止Evidenceは
`records/development/2026-08-03-work-1-reconstructability-candidate.md`に固定する。

## 2. 固定入力

### 2.1 authority order

| 順位 | role | path | SHA-256 | 状態 |
|---:|---|---|---|---|
| 1 | Intent候補 | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` | `provisional`、Human承認前 |
| 2 | 統合用語集候補 | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` | `provisional`、Human承認前 |
| 3 | 現行計画候補 | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` | `provisional`、Human承認前 |

現行計画の`intent_ref`と`glossary_ref`、checklistの`authority_order`は上表と一致する。過去版を示す
`generated_from`は現行authority参照として使用しない。

### 2.2 operational inputs

| role | path | SHA-256 |
|---|---|---|
| 開発入口（Work開始時） | `docs/development/2026-08-03-initial-development-checklist.md` | `42dc7a0d2d1080a2297abeeaa0da79edd902c38f6d3572245b1d0e42026b44c9` |
| 開発方針 | `docs/development/2026-08-02-development-policy.md` | `a094926a5c9f981cdb1997b4a8e205da9a333fda51f2876b47e76d53fcf7dc1c` |
| 方針Decision | `records/development/development-policy-v4.json` | `87bd0460bce3ae471a598ae5ab2964d05e6ceb97701870f25b5cc9110133f24a` |
| source catalog | `records/sources/2026-08-02-source-catalog.json` | `1a40adcec2af6c9f2829af9f4a90cc33bfe6d9cb3fd0e1e305014d71356bd6bb` |
| 前身baseline | `records/reference-baselines/2026-07-27/baseline.toml` | `ba09b5da741482103373e524980ca0870da21f6b5d7cc2fc7c1d7d8094295f76` |
| reconstructability audit | `records/task-contract/2026-08-02-documentation-reconstructability-audit.json` | `771dcf1ff88ea3d8e6438b5b75579e0143229cd03362990c56767bcb189a008a` |
| documentation revision v16 | `records/task-contract/task-contract-centered-documentation-v16.json` | `7c60fe046bb65ca4137b1c3384b139ad53321380f7a12f7c3668962fbacdd35d` |

source catalogの10 entryは、全`record_path`について現行fileのSHA-256が`record_sha256`と一致した。
前身baselineの2 inventoryも、`baseline.toml`記載のSHA-256と一致した。

## 3. Repository baselineとChange Set

| 項目 | 固定値 |
|---|---|
| repository | `ReviewCompass3` |
| branch | `main` |
| Work開始時HEAD | `13347232f2f0c1b891d761840c4ae9d9382b354f` |
| Work開始時tree | `80069baf7a058437efd0ad38bc83bcb9ebd5b5b3` |
| Work開始時worktree | clean |
| active製品Task Contract／Work Item | なし |
| 製品実装code | 未着手 |

Work開始時に未コミット変更はなかった。本Evidence、改善候補、checklist、TODOの更新はWork 1の
出力Change Setであり、固定入力から除外する。commitはHumanの明示指示がないため本Workでは行わない。

前身baselineは次の固定Git treeだけを対象とし、記録時のworktree変更を含めない。

| repository | commit | tree | inventory SHA-256 | 制約 |
|---|---|---|---|---|
| ReviewCompass | `35ef8d4cc66b9a00aca9c6da10b645837b06564b` | `3ed415ccce6da39bf0edf8713714ec6ce68323f9` | `34fe974552a1572d5f383e9cd8d461e2a1df8836f92b5f1135a22463fecd52b8` | non-normative、provisional |
| ReviewCompass2 | `d6bbb01500002872c713412bfbd63b702a291c99` | `93401fe3448aff263078297a92e4998c4e519270` | `6bfa12351cb274e384c607f4dd01b3e1f0997589db523d91237146150cb23d2b` | frozen predecessor Evidence |

## 4. source universe、scope、非対象、機密性

### source universe

Work 1で探索・検査してよい母集合を次に限定した。

1. 2.1のauthority 3文書。
2. 2.2のoperational inputs。
3. source catalogが列挙する10件の派生source record。
4. 前身baselineが固定する2 repositoryのcommit、tree、inventory。
5. 現行計画が直接参照するWork 1、Deferred Work、停止条件、実装へ進む条件。
6. 現行文書が参照するv16 revision recordとreconstructability audit。

project全体、会話履歴、catalog外の端末file、外部source原文、raw review応答を暗黙に含めない。

### 今回の対象

- authority、baseline、source identity、適用範囲、非目標の固定。
- 既知Finding、未承認事項、Human判断待ち、blocking conflictの列挙。
- Work 1用の最小Evidence Extraction ContractとConsumption Closure。
- 固定入力変更時のstale化、停止、再開入口の定義。

### 今回の非対象

- Work 1AのLayout Baseline、root解決規則、空配置fixture。
- Work 1BのSession Log BootstrapとCurrent Work Projection tooling。
- Requirements、Task Contract、schema、validator、製品codeの実装。
- Human承認前候補のpromotionまたは段完了判断。
- 外部送信、外部sourceの再取得、生会話・raw記録のrepository取込み。
- 前身成果の一括移植、過去recordの上書き修正。

### confidentiality

全入力は`project-internal`として扱う。catalogが`digest-only`または`git-object-pinned`としたsourceは、
派生record、Digest、固定Git objectだけを使用する。端末固有絶対pathのsource原文を読み直さず、raw内容を
repositoryへ複製せず、外部へ送信しない。

## 5. 初期scopeとDeferred Work

初期開発は、`single_active_leaf`で固定入力、Layout、Session Log Bootstrap、上流文書、最小Review
Task Contract、negative path、内部Implementation Pilot、`local_integrated` deployment、評価、releaseを
小さな縦切りで進める。現在のactive範囲はWork 1だけである。

次は初期scopeへ前倒ししない。

- As-Built projection。
- AI判断委譲。初期releaseはHuman modeとする。
- `shared_runtime`、`distributed_hybrid`、複数project／machineの実並行。
- 改善候補、Issue Resolution、実施報告照合のautomation。
- 画面UI、汎用Task Registry、任意Task orchestration、plugin system。
- 外部software projectによるportability pilot。
- 全既存codeの一括整形。

## 6. 未承認事項、既知Finding、Human判断

### 未承認事項

- Intent統合最新版、統合用語集、現行計画、新しい第5段相当はHuman承認前である。
- Layout Baseline、Session Log Bootstrap、関数台帳baseline、最小Review Task Contractも未作成・未承認である。
- Work 5Aの製品実装開始permitは存在しない。

これらはWork 1の文書・Evidence作成自体を禁止しないが、段完了、promotion、製品実装開始には使用できない。

### 既知Finding

- reconstructability auditは、v1〜v15の多くが`digest-only`であるhigh severity findingを保持する。
- v16のforward ruleに対しても、同一commitのmanifest 18件中5件が不一致だった。詳細は
  `IC-WORK1-DOC-RECONSTRUCTABILITY-001`を参照する。
- source catalogにはrawを保持せず`digest-only`であるsourceがある。派生recordを越える主張には使わない。

### blocking conflictとHuman判断待ち

Intent、用語集、計画の現在内容間に、Work 1 scopeのblockingな意味競合は検出しなかった。しかし、v16の
Provenance再構築不能は固定入力の由来保証を損なうblocking conflictである。Work 1を
`pause_and_triage`し、corrective successor recordを作るか、digest-only riskを受容するかのHuman判断を待つ。

## 7. 最小Evidence Extraction Contract

| 項目 | 固定規則 |
|---|---|
| 開始集合 | 2.1と2.2のpath／Digest、現行PlanのWork 1 |
| 展開規則 | authorityの直接参照、source catalogの`record_path`、baselineのinventory、PlanのDeferred／停止／実装条件だけを一段展開する |
| 分類 | `adopt | adapt | reject | defer` |
| 終了条件 | Work 1の7確認項目と2完了関門へsourceまたは停止理由を割り当て、未分類候補が0件になる |
| 除外 | catalog外source、raw会話、raw review、外部再取得、製品code探索 |
| 完全性oracle | authority相互参照Digest、catalog 10 entry、baseline 2 inventory、Git状態、Deferred／停止条件、v16 manifestを機械照合する |

分類結果：

- `adopt`：現行authority 3文書をHuman承認前候補として、開発方針とchecklistをoperational ruleとして採用。
- `adapt`：前身baselineと10 source recordを規範ではなく経験・失敗Evidenceとして使用。
- `reject`：catalog外原文、全会話、前身の旧lane／旧gate／固定provider pathの直接移植。
- `defer`：5節のDeferred Work。

v16 manifest不一致により完全性oracleは不合格である。候補や不足を推測で補わず、停止結果を保持する。

## 8. Evidence Consumption Closure

| source／Finding | disposition | consumer／Outcome |
|---|---|---|
| `SRC-TASK-CONTRACT-DISCUSSION-001` | adapt | 現行Intent／PlanのTask Contract中心設計 |
| `SRC-LLMGP-HYBRID-001` | adapt | risk-based test-firstとreopen方針 |
| `SRC-RC2-SHARED-ROUTINE-001` | adapt | Work 4AのSource Symbol Index／Reusable Routine Ledger |
| `SRC-RC2-ISSUE-PLAN-001` | adapt | Work 8手作業PilotとDeferred 14.4 |
| `SRC-RC-CONFORMANCE-001` | adapt | Deferred As-Built projectionとconformance境界 |
| `SRC-RC2-TERMINOLOGY-001` | adapt | 統合用語集とRuntime統制defer |
| `SRC-DEPLOYMENT-TOPOLOGY-001` | adapt | Work 1A、`local_integrated`、後続deployment profile |
| `SRC-RC2-CHANGE-SCALED-001` | adapt | `impact_slice`、`expanded_scope`、`full_consistency` |
| `SRC-RC2-CROSS-CUTTING-LESSONS-001` | adapt | Extraction／Consumption／Assurance／post-write規律 |
| `SRC-PROJECT-PROGRESSION-DISCUSSION-001` | adapt | Work 4代表scenario、外部pilot defer |
| v1〜v15 reconstructability finding | adapt | forward immutable-snapshot rule |
| v16 manifest不一致 | unresolved blocking | `IC-WORK1-DOC-RECONSTRUCTABILITY-001`、Human triage |
| Human承認前authority | unresolved non-consumed gate | Work 2〜4とWork 5A開始前のHuman approval |
| Deferred Work | defer | 現行Plan 14節とchecklist後続節 |

必須sourceと採用Findingにはconsumerまたは未解決routeがある。v16不一致には消費済みOutcomeがないため、
Consumption Closureはblocking未完了である。

## 9. stale化と再開入口

次のいずれかが変わった場合、本EvidenceとWork 1 checklist結果をstaleにする。

- authority 3文書のpath、Digest、promotion状態または相互参照。
- source catalogのentry、record Digest、confidentiality、reconstructability。
- 前身baselineのcommit、tree、inventoryまたは適用範囲。
- Work 1のscope、非目標、Deferred境界、停止条件。
- v16不一致の修復Decision、corrective record、固定commitまたはpost-commit照合結果。

再開時は、旧Evidenceを上書きせず次versionを作る。変更した入力から影響閉包を取り、authority、catalog、
baseline、Git、manifestを再照合する。corrective recordを同一commitへ固定し、そのcommitからmanifest全件の
一致を確認したEvidence、またはHumanが明示的にriskを受容したDecisionがなければWork 1Aへ進まない。

## 10. 完了関門判定

| 関門 | 判定 | Evidence |
|---|---|---|
| 固定入力、scope、非目標、未解決事項を一つのEvidenceから確認できる | pass | 本文2〜9節 |
| blocking conflictがない、または停止理由が明示されている | pass-with-blocker | v16 manifest不一致、`IC-WORK1-DOC-RECONSTRUCTABILITY-001` |

Work 1のEvidence作成は完了したが、Workflow結果は`blocked`である。Human判断と修復Evidenceなしに
Work 1Aへ進まない。
