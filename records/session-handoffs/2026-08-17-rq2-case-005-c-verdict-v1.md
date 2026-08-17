# Reviewer起動アダプタ 判定record（機械転記） rq2b2-case-005-c

- Reviewer：provider `google`／model `gemini-3.1-pro-high`（アダプタ照合済み）
- 独立性：Tier 1（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `antigravity-cli`）
- 依頼record：`records/session-handoffs/2026-08-17-rq2-case-005-c-request-v1.md`（SHA-256 `d654bbc242ad05c047ebb4395cef8661528828de3ef02a16bab3116196c358e9`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `49810796e3de758454906389edce837a41c14f3525b622da507733962ab0116f`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`rq2b2-case-005-c`
- 判定：**verified_with_findings**
- 判定要旨：対象materialの記述を検査した結果、2件の指摘事項があります。1点目は事実の誤りで、20行目のcommit hashの略記が直前のJSONに含まれるハッシュと合致していません（e87d9f68 vs e87d9f60）。2点目は記述の欠落または曖昧さで、31行目で「読取り9件」と記載しながら列挙されている対象が7件分しかなく、計算が合いません。
- 鮮度（Reviewer申告）：not_computable（expected `d654bbc242ad05c047ebb4395cef8661528828de3ef02a16bab3116196c358e9`／observed `not_computable`）。理由：読み取り専用環境であり端末コマンドによるハッシュ値計算ができないため
- 未検査：commit hash（e87d9f60..., 6f3d55d, 41a705b）の実際の存在と差分（端末コマンド実行不可のため）、所要時間やトークン数などの実行ログの詳細（アクセス不可のため）

## findings

- factual-error-commit-hash-mismatch（severity: high／blocking: true）：20行目のcommit hashの略記（e87d9f68）が、17行目のJSON出力に含まれる実際のハッシュ（e87d9f60c357...）の先頭と一致しておらず、事実の誤りがあります。（根拠：`docs/evaluation/rq2-cases/case-005/reviewer-launch-e2e-evidence.md` 20行目）
- missing-description-read-count-mismatch（severity: medium／blocking: true）：31行目で「読取り9件」と記載されていますが、直後に列挙されている対象を数えると7件分（依頼record1、test1、tools3、operations1、Evidence1）しかなく、残りの2件分についての記述が欠落しているか、件数に誤りがあります。（根拠：`docs/evaluation/rq2-cases/case-005/reviewer-launch-e2e-evidence.md` 31行目）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": true,
      "claim": "20行目のcommit hashの略記（e87d9f68）が、17行目のJSON出力に含まれる実際のハッシュ（e87d9f60c357...）の先頭と一致しておらず、事実の誤りがあります。",
      "evidence_location": "20行目",
      "evidence_path": "docs/evaluation/rq2-cases/case-005/reviewer-launch-e2e-evidence.md",
      "identifier": "factual-error-commit-hash-mismatch",
      "severity": "high"
    },
    {
      "blocking": true,
      "claim": "31行目で「読取り9件」と記載されていますが、直後に列挙されている対象を数えると7件分（依頼record1、test1、tools3、operations1、Evidence1）しかなく、残りの2件分についての記述が欠落しているか、件数に誤りがあります。",
      "evidence_location": "31行目",
      "evidence_path": "docs/evaluation/rq2-cases/case-005/reviewer-launch-e2e-evidence.md",
      "identifier": "missing-description-read-count-mismatch",
      "severity": "medium"
    }
  ],
  "freshness": {
    "expected": "d654bbc242ad05c047ebb4395cef8661528828de3ef02a16bab3116196c358e9",
    "observed": "not_computable",
    "reason": "読み取り専用環境であり端末コマンドによるハッシュ値計算ができないため",
    "result": "not_computable"
  },
  "reviewer": {
    "model": "gemini-3.1-pro-high",
    "provider": "google"
  },
  "summary": "対象materialの記述を検査した結果、2件の指摘事項があります。1点目は事実の誤りで、20行目のcommit hashの略記が直前のJSONに含まれるハッシュと合致していません（e87d9f68 vs e87d9f60）。2点目は記述の欠落または曖昧さで、31行目で「読取り9件」と記載しながら列挙されている対象が7件分しかなく、計算が合いません。",
  "target": {
    "commit": "HEAD",
    "path": "records/session-handoffs/2026-08-17-rq2-case-005-c-request-v1.md"
  },
  "unexamined": [
    "commit hash（e87d9f60..., 6f3d55d, 41a705b）の実際の存在と差分（端末コマンド実行不可のため）",
    "所要時間やトークン数などの実行ログの詳細（アクセス不可のため）"
  ],
  "verdict": "verified_with_findings"
}
```
