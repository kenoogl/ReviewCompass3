# Work 4A Rebuild Design v2 Proposal

状態：`superseded_for_implementation`
対象：Work 4A Reusable Routine Ledger

> `DEC-WORK4A-REBUILD-DESIGN-003`により、実装の正本は
> `docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md`へ移った。
> 本文書は履歴として保持する。外部`DATA_ROOT`参照方式（§1の`ref`定義と§4・§5の結線）に設計矛盾があり、
> この方式を実装、actual artifact、Work 4A完了の根拠に使わない。
> v3が継承した規則（canonical Digest、source universe、Policy、new-only、current Baseline導出、
> legacy Task Contract）はv3 §3に明記する。

これはv1で未定義だったPolicy、source universe、legacy Task Contract、current Baselineを固定する改訂案である。
Human承認によりv1を`superseded_for_implementation`とし、このv2だけを実装の正本にする。
承認は`DEC-WORK4A-REBUILD-DESIGN-002`に記録する。
それまでは、`c4bfb57`の試作実装とそのE2E testをactual artifactまたはWork 4A完了の根拠に使わない。

## 1. Scopeと用語

用語は次へ固定する。

- `record`：versionを持つ不変JSON文書。
- `content_digest`：`content_digest`自身を除いたJSONを、UTF-8、キー昇順、空白なし、改行なしで直列化したSHA-256。
- `file_sha256`：保存済みUTF-8 file bytesのSHA-256。
- `ref`：`record_id`、`version`、project相対`path`、`file_sha256`の四項目。
- `current`：検証済みBaseline seriesで最大の連続versionを持つBaseline。一つでも欠番、重複、Digest不一致があれば存在しない。

recordを書き出す時は表示用JSONの整形に依存せず、`content_digest`と`file_sha256`を区別する。

## 2. 初期source universe

初期のsource universeは`SRCU-WORK4A-TOOLS-PY-V1`とする。

| 項目 | 固定値 |
| --- | --- |
| 含めるroot | `<PROJECT_ROOT>/tools/` |
| 含めるfile | `**/*.py`。symbolic link、binary、構文不正fileは拒否 |
| 除外 | `tests/`、`.venv/`、`.git/`、`.reviewcompass/`、`docs/`、`records/`、`DATA_ROOT`、cache、state、log、sensitive data |
| path表現 | source rootからのPOSIX相対path、byte順昇順 |
| source content | universe ID、各path、各file bytesのSHA-256をcanonical JSONでDigest化 |

このため、台帳、Decision、records、設計文書をcommitしても`source_content_id`は変わらない。
universeの追加・除外・glob変更は`source_universe_id`を新versionにし、全Baselineを`stale`にする。
`tests/`の共通helperを台帳化する必要が生じた場合は、新しいuniverseをHumanが承認する別Workとする。

## 3. Policy artifactとrisk判定

Work 4Aで使うPolicyは、`<PROJECT_ROOT>/<artifact_roots.policies>/work4a-freshness-policy-v1.json`を正本とする。
このrecordには少なくとも次を入れる。

- `policy_id`、`policy_version`、`content_digest`
- 本Policyが解釈するDevelopment Policyのpathと`file_sha256`
- `ordinary`、`security`、`authority`、`irreversible`の閉じたchange class
- `revalidation_required`となるclass：`security`、`authority`、`irreversible`

BaselineにはPolicyの`ref`を保存する。fresh判定は、現行Policy fileのDigestがrefと一致し、change classが
`ordinary`である場合だけ継続できる。Policy artifactがない、読めない、閉じた語彙外、またはDigest不一致なら
`invalid`または`revalidation_required`で停止する。文字列を呼出側から渡して判定してはならない。

## 4. 配置とDecision authority

| record | 配置 | authority |
| --- | --- | --- |
| Source Observation、Index、Candidate Run | `DATA_ROOT/projects/<project_id>/reuse/` | 機械生成した観測。Git外 |
| Operational Human Decision | `<PROJECT_ROOT>/<artifact_roots.design_decisions>/` | actual Ledgerを許可するproject artifact |
| Entry、Relation、Baseline | `<PROJECT_ROOT>/<artifact_roots.reuse>/reusable-routine-ledger/` | Operational Decisionと機械検証で束縛されるproject artifact |
| Historical Contract Status | `<PROJECT_ROOT>/<artifact_roots.contracts>/historical-status/` | target projectのContract状態 |
| Development Decision／revert map／legacy inventory | `records/development/` | このrepositoryの開発証跡。Operational Decisionではない |

設計承認を記録する`records/development/`と、routine採用を許可するOperational Human Decisionは同じものではない。
Baselineは後者だけを参照できる。

## 5. Observation、Candidate、Baselineの結線

1. Source Observationは`source_universe_id`、`source_content_id`、HEAD、tool version、file listを保存する。
2. Candidate Runは同一Observationの`ref`と、candidate結果の`content_digest`を保存する。
3. Operational DecisionはCandidate Runの`ref`、decision vocabulary、Human identityを保存する。
4. BaselineはObservation、Candidate Run、Operational Decision、Policyの各`ref`、Entry ref、Relation refを保存する。
5. 新Baselineを作る時、ObservationとCandidate Runの`source_content_id`は一致しなければならない。`DATA_ROOT`内に存在するだけの古いObservationは参照できない。

fresh判定では、Baselineに結ばれたすべてのrefを再読込してfile SHA-256を照合する。再採取したObservationの
`source_universe_id`と`source_content_id`が一致する時だけfreshである。HEAD差だけはstale理由にならない。

## 6. immutable Ledgerとcurrent Baseline

EntryとRelationはnew-onlyであり、意味が変わる時だけ対象recordのversionを上げる。
新routineを一件追加する時は、新Entry、新Relation（必要な件数）、新Baselineだけを書く。既存Entry・Relationの
file bytesを書換え・複製してはならない。

Baseline filenameは`ledger-baseline--v<positive-integer>.json`とする。writerは次を満たさなければ停止する。

1. 既存Baseline versionが`1..n`で欠番なく一つずつ存在する。
2. currentは、検証済み最大versionの`ledger-baseline--v<n>.json`である（`n=0`ならcurrentなし）。
3. 新規は必ず`v<n+1>`だけをnew-only作成する。
4. 既存Baseline、Entry、Relation、Decision、Policyのrefを再読込し、Digest不一致なら書込み前に停止する。

current pointer用の可変fileは作らない。最大連続versionと全Digest照合からcurrentを導くため、pointer書換えによる
第二の状態を持たない。

## 7. legacy Task Contractの扱い

既存`records/task-contract/`はimmutableな開発履歴であり、移動・書換えない。まず全recordについて、status field、
status value、creation provenance field、creation Policy Digestの有無をinventoryとして`records/development/`へ記録する。

Historical Contract Statusを`completed_historical`にできるのは、対象Contractのfile SHA-256、作成commit、作成時Policy
artifactのrefがすべて存在し、Humanが承認した場合だけである。

一つでも欠けるlegacy Contractは`evidence_insufficient`とする。この状態は「完了済み」でも「現行開始を許す」でもなく、
Humanの追加根拠またはrisk受容を待つ。推測、現在のPolicyからの逆算、status語彙の自動変換で`completed_historical`にしてはならない。

従って、v2の最初のactual artifactではlegacy Contractをhistoricalへ移行しない。受入範囲は、欠落した根拠を拒否する負例までとする。

## 8. v2 E2E acceptance

以下を同じtest群でREDから確認する。

1. `SRCU-WORK4A-TOOLS-PY-V1`だけからObservation、Index、Candidate Runを生成する。
2. Policy artifactとOperational Human DecisionがないBaseline書込みを拒否する。
3. 新Entry一件と新Relation一件を追加しても、既存Entryと既存Relationのfile SHA-256が変わらない。
4. EntryまたはRelationの改竄、Candidate／Decision／Policy refの不一致、unsafe root、欠番Baselineを拒否する。
5. 同一source contentでHEADだけを変えた再採取はfresh、source内容またはuniverse変更はstaleにする。
6. `security`、`authority`、`irreversible` Policy変更は`revalidation_required`にする。
7. creation Policy Digestまたはcreation commitが欠けるlegacy Contractは`completed_historical`を拒否し、
   `evidence_insufficient`だけを許可する。

actual artifactは、このtest群がGREENで、source universeの初回Observationとcandidateを機械生成し、対象routineと
dispositionをHumanが承認した後にだけ作る。

## 9. revert実施記録

v1のrevertは`3bca31c`、`474a0d5`、`7963039`で実施済みである。実装再開前に、各revert commitについて
「戻した元commit、対象file、保持したLayout v3 commit、外部`DATA_ROOT`を操作しなかったこと」を示すrevert mapを
`records/development/`へnew-only保存する。commit subjectだけを実施根拠にしない。

## 10. 実装開始条件

このv2のHuman承認、Policy artifact schema、source universeのHuman承認、revert mapがそろうまで、
試作moduleを拡張せず、actual artifactを作成しない。
