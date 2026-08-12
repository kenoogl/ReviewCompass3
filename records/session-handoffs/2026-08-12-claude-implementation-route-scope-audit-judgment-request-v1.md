# Claude実装委譲経路 範囲固定 指示品質判定依頼 v1

- 状態：`fixed_request`
- 判定担当：監査担当とは別の新しい会話状態の`gpt-5.6-terra`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定入力

- 対象：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v1.md`
- 対象SHA-256：`fccbad6f82a86363500ea16b1a347793fc514a566de362dd701acb408549497f`
- 選択裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-selection-human-decision-v1.md`
- 監査未加工結果：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-audit-raw-v1.json`
- 監査未加工結果SHA-256：`1abd99d8673f3927267c3054e9db043c0ea7992806352497c59f2a831512372f`
- 監査結果：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-audit-result-v1.md`
- 上流文書：`docs/development/pilot-specific-claude-codex-collaboration.md`
- レビュー規則：`docs/development/work-review-protocol.md`

監査所見集合は`PA-CD-001`の1件だけである。

## 2. 判定

所見が対象と上流文書に照らして成立するか確認し、`adopt`、`reject`、`hold`の推奨を1件だけ作る。
判定担当はHumanの最終採否を代理せず、対象fileを変更しない。新しい所見や一般的な改善案を追加しない。
blockingの成立を認める場合は、`docs/development/work-review-protocol.md` §11.1の類型を確認する。

## 3. 出力

最終応答は説明文を付けず、次の構造を持つ単一JSON objectにする。

```json
{
  "schema_version": 1,
  "kind": "instruction_quality_judgment",
  "target_sha256": "fccbad6f82a86363500ea16b1a347793fc514a566de362dd701acb408549497f",
  "audit_raw_sha256": "1abd99d8673f3927267c3054e9db043c0ea7992806352497c59f2a831512372f",
  "judge_model": "gpt-5.6-terra",
  "coverage": {
    "expected_finding_ids": ["PA-CD-001"],
    "actual_finding_ids": ["PA-CD-001"],
    "exact_once": true
  },
  "judgments": [
    {
      "finding_id": "PA-CD-001",
      "recommendation": "adopt | reject | hold",
      "blocking_type_assessment": "1 | 2 | 3 | 4 | not_blocking",
      "reason": "推奨理由"
    }
  ],
  "verdict": "complete | invalid"
}
```

判定担当はClaude、外部CLI、外部送信を起動しない。
