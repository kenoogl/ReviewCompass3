# Reviewer起動アダプタ 判定record（機械転記） rq2b2-case-001-b

- Reviewer：provider `google`／model `gemini-3.1-pro-high`（アダプタ照合済み）
- 独立性：Tier 1（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `antigravity-cli`）
- 依頼record：`records/session-handoffs/2026-08-17-rq2-case-001-b-request-v1.md`（SHA-256 `41f197a033aa8465bf9fd38341f88b9e46231ecf170bd357695003a384413d55`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `250faa3a5733cd056274bbf90a70f5897fc73c4b57c253f291f1975fa70b0393`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`rq2b2-case-001-b`
- 判定：**rejected**
- 判定要旨：対象の2つのmaterialを検査しました。前置recordの正準列の定義（contract-canonical-sequence.md）において、queue-operationの必須欄としてcontentの存在が要求されていますが、観測記録（observation-prefix-record-shapes.md）ではdequeueの場合にcontentが存在しないことが示されており、内部矛盾があります。このままでは実際のdequeueレコードが非対応として弾かれるため、受入をブロックする所見として報告します。また、startedレコードの実物基準に関する記述が観測記録側に欠落している点を非ブロックの所見として挙げています。
- 鮮度（Reviewer申告）：not_computable（expected `41f197a033aa8465bf9fd38341f88b9e46231ecf170bd357695003a384413d55`／observed ``）。理由：端末commandの実行が禁止されているため、読取りによる対象の確認は行いましたが、SHA-256 digestを機械計算できません。
- 未検査：対象依頼recordのSHA-256 digestの実測と照合（端末command実行不可のため）

## findings

- contradiction-queue-operation-content（severity: error／blocking: true）：contract-canonical-sequence.md（15行目）ではqueue-operationの必須欄としてcontentの存在を要求していますが、observation-prefix-record-shapes.md（15行目）ではoperationがdequeueの場合にcontent欄が存在しないことが示されています。このままでは、観測された76件のdequeueレコードが必須欄を満たさず非対応として扱われてしまう内部矛盾（事実の食い違い）が生じます。（根拠：`docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md` L15）
- missing-evidence-started（severity: warning／blocking: false）：contract-canonical-sequence.md（18行目）では4種目の前置recordとしてstartedが定義されていますが、全数調査であるobservation-prefix-record-shapes.mdの表にはstartedが出現していません。enqueueのように別系統での採取に関する補足説明もないため、startedの実物基準となる根拠記述が欠落しています。（根拠：`docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md` L18）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": true,
      "claim": "contract-canonical-sequence.md（15行目）ではqueue-operationの必須欄としてcontentの存在を要求していますが、observation-prefix-record-shapes.md（15行目）ではoperationがdequeueの場合にcontent欄が存在しないことが示されています。このままでは、観測された76件のdequeueレコードが必須欄を満たさず非対応として扱われてしまう内部矛盾（事実の食い違い）が生じます。",
      "evidence_location": "L15",
      "evidence_path": "docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md",
      "identifier": "contradiction-queue-operation-content",
      "severity": "error"
    },
    {
      "blocking": false,
      "claim": "contract-canonical-sequence.md（18行目）では4種目の前置recordとしてstartedが定義されていますが、全数調査であるobservation-prefix-record-shapes.mdの表にはstartedが出現していません。enqueueのように別系統での採取に関する補足説明もないため、startedの実物基準となる根拠記述が欠落しています。",
      "evidence_location": "L18",
      "evidence_path": "docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md",
      "identifier": "missing-evidence-started",
      "severity": "warning"
    }
  ],
  "freshness": {
    "expected": "41f197a033aa8465bf9fd38341f88b9e46231ecf170bd357695003a384413d55",
    "observed": "",
    "reason": "端末commandの実行が禁止されているため、読取りによる対象の確認は行いましたが、SHA-256 digestを機械計算できません。",
    "result": "not_computable"
  },
  "reviewer": {
    "model": "Gemini 3.1 Pro (High)",
    "provider": "Google"
  },
  "summary": "対象の2つのmaterialを検査しました。前置recordの正準列の定義（contract-canonical-sequence.md）において、queue-operationの必須欄としてcontentの存在が要求されていますが、観測記録（observation-prefix-record-shapes.md）ではdequeueの場合にcontentが存在しないことが示されており、内部矛盾があります。このままでは実際のdequeueレコードが非対応として弾かれるため、受入をブロックする所見として報告します。また、startedレコードの実物基準に関する記述が観測記録側に欠落している点を非ブロックの所見として挙げています。",
  "target": {
    "commit": "unknown",
    "path": "records/session-handoffs/2026-08-17-rq2-case-001-b-request-v1.md"
  },
  "unexamined": [
    "対象依頼recordのSHA-256 digestの実測と照合（端末command実行不可のため）"
  ],
  "verdict": "rejected"
}
```
