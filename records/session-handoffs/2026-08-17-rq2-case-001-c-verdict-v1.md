# Reviewer起動アダプタ 判定record（機械転記） rq2b2-case-001-c

- Reviewer：provider `google`／model `gemini-3.1-pro-high`（アダプタ照合済み）
- 独立性：Tier 1（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `antigravity-cli`）
- 依頼record：`records/session-handoffs/2026-08-17-rq2-case-001-c-request-v1.md`（SHA-256 `6a2ab6867fe3547a7cf1ed4a94ab73eb5e57ffe2a70758446f8b596bc2296767`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `0521dd5e6501a335f154782c5e1211307e368e2e1d24358ade2b0ee0989cef77`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`rq2b2-case-001-c`
- 判定：**verified_with_findings**
- 判定要旨：対象材料2件（契約候補・観測記録）の記述を検査した結果、重大な内部矛盾と事実の誤りを3件発見しました。1点目は`queue-operation`における`content`欄必須要件と実態（`dequeue`には存在しない）の矛盾、2点目は網羅調査に存在しない`started`種別の指定、3点目は実測の連続数（3〜4個）と出現数データ（1ファイル平均1件）の食い違いです。これらは対象レコードの判定ロジックに直接影響するブロッキング要件であり、採用前に記述の修正が必要です。
- 鮮度（Reviewer申告）：not_computable（expected `6a2ab6867fe3547a7cf1ed4a94ab73eb5e57ffe2a70758446f8b596bc2296767`／observed `not_computable`）。理由：実行環境が読み取り専用であり、端末コマンド（shasum等）を実行できないため、ファイルのハッシュ値の機械的な計算が不可能です。
- 未検査：sha256 digestの機械的再計算・検証（環境制限のため）、対象材料以外の運用recordや関連文書の参照・整合性確認、実験そのものの是非（評価データ取得計画の妥当性）、対象materialが正しい複製元から複製されたものであるか、および版の新旧

## findings

- FND-001-QUEUE-OP-CONTENT（severity: high／blocking: true）：契約候補（L15）では`queue-operation`の必須欄として`content`の存在を求めているが、観測記録（observation-prefix-record-shapes.md L15, L20-L21）では`operation`が`dequeue`の場合に`content`欄が存在しないと報告されており、事実の誤りおよび内部矛盾がある。（根拠：`docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md` L15）
- FND-002-STARTED-MISSING（severity: medium／blocking: true）：契約候補（L18）では既知前置recordとして`started`を挙げているが、観測記録（observation-prefix-record-shapes.md L13-L18）の「実物形の網羅調査」の表には`started`が記載されておらず、事実の食い違いまたは必要な記述の欠落がある。（根拠：`docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md` L18）
- FND-003-CONSECUTIVE-COUNT（severity: medium／blocking: true）：契約候補（L22）には「実測の連続数3〜4個」と記載されているが、観測記録（observation-prefix-record-shapes.md L13-L18）の調査では81件のsource fileに対して前置recordの出現数合計が81件（1ファイル平均1件）となっており、実測データの事実と矛盾している。（根拠：`docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md` L22）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": true,
      "claim": "契約候補（L15）では`queue-operation`の必須欄として`content`の存在を求めているが、観測記録（observation-prefix-record-shapes.md L15, L20-L21）では`operation`が`dequeue`の場合に`content`欄が存在しないと報告されており、事実の誤りおよび内部矛盾がある。",
      "evidence_location": "L15",
      "evidence_path": "docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md",
      "identifier": "FND-001-QUEUE-OP-CONTENT",
      "severity": "high"
    },
    {
      "blocking": true,
      "claim": "契約候補（L18）では既知前置recordとして`started`を挙げているが、観測記録（observation-prefix-record-shapes.md L13-L18）の「実物形の網羅調査」の表には`started`が記載されておらず、事実の食い違いまたは必要な記述の欠落がある。",
      "evidence_location": "L18",
      "evidence_path": "docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md",
      "identifier": "FND-002-STARTED-MISSING",
      "severity": "medium"
    },
    {
      "blocking": true,
      "claim": "契約候補（L22）には「実測の連続数3〜4個」と記載されているが、観測記録（observation-prefix-record-shapes.md L13-L18）の調査では81件のsource fileに対して前置recordの出現数合計が81件（1ファイル平均1件）となっており、実測データの事実と矛盾している。",
      "evidence_location": "L22",
      "evidence_path": "docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md",
      "identifier": "FND-003-CONSECUTIVE-COUNT",
      "severity": "medium"
    }
  ],
  "freshness": {
    "expected": "6a2ab6867fe3547a7cf1ed4a94ab73eb5e57ffe2a70758446f8b596bc2296767",
    "observed": "not_computable",
    "reason": "実行環境が読み取り専用であり、端末コマンド（shasum等）を実行できないため、ファイルのハッシュ値の機械的な計算が不可能です。",
    "result": "not_computable"
  },
  "reviewer": {
    "model": "Gemini 3.1 Pro (High)",
    "provider": "Google"
  },
  "summary": "対象材料2件（契約候補・観測記録）の記述を検査した結果、重大な内部矛盾と事実の誤りを3件発見しました。1点目は`queue-operation`における`content`欄必須要件と実態（`dequeue`には存在しない）の矛盾、2点目は網羅調査に存在しない`started`種別の指定、3点目は実測の連続数（3〜4個）と出現数データ（1ファイル平均1件）の食い違いです。これらは対象レコードの判定ロジックに直接影響するブロッキング要件であり、採用前に記述の修正が必要です。",
  "target": {
    "commit": "unspecified",
    "path": "records/session-handoffs/2026-08-17-rq2-case-001-c-request-v1.md"
  },
  "unexamined": [
    "sha256 digestの機械的再計算・検証（環境制限のため）",
    "対象材料以外の運用recordや関連文書の参照・整合性確認",
    "実験そのものの是非（評価データ取得計画の妥当性）",
    "対象materialが正しい複製元から複製されたものであるか、および版の新旧"
  ],
  "verdict": "verified_with_findings"
}
```
