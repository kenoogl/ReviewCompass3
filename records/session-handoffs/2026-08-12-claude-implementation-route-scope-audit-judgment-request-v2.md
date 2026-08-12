# Claude実装委譲経路 範囲固定 指示品質判定依頼 v2

- 状態：`fixed_request`
- 周回：2
- 判定担当：監査担当とは別の新しい会話状態の`gpt-5.6-terra`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定入力

- 対象：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v2.md`
- 対象SHA-256：`9881f7df526c3aef8c21e665f75927329608d1b0518e343db0ac5c89f954a024`
- 監査未加工結果：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-audit-raw-v2.json`
- 監査未加工結果SHA-256：`4831fa4b90bfcdd01e024920234f173f86eddfdc15f399b69deeb295ba930ff2`
- 監査結果：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-audit-result-v2.md`
- Human裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-finding-human-decision-v1.md`
- 上流文書：`docs/development/pilot-specific-claude-codex-collaboration.md`

監査の新規所見集合は空である。前周所見`PA-CD-001`の状態は`resolved`である。

## 2. 判定

監査結果の新規所見集合が実際に空で、前周所見の状態がHuman裁定とv2に一致するかだけを照合する。
新しい所見、一般的な改善案、実装詳細を追加しない。Human判断を代理しない。

## 3. 出力

最終応答は説明文なしの単一JSON objectにする。

```json
{
  "schema_version": 1,
  "kind": "instruction_quality_judgment",
  "round": 2,
  "target_sha256": "9881f7df526c3aef8c21e665f75927329608d1b0518e343db0ac5c89f954a024",
  "audit_raw_sha256": "4831fa4b90bfcdd01e024920234f173f86eddfdc15f399b69deeb295ba930ff2",
  "judge_model": "gpt-5.6-terra",
  "coverage": {
    "expected_finding_ids": [],
    "actual_finding_ids": [],
    "exact_once": true
  },
  "prior_findings": [
    {
      "finding_id": "PA-CD-001",
      "status": "resolved | unresolved",
      "evidence": "照合根拠"
    }
  ],
  "judgments": [],
  "verdict": "complete | invalid"
}
```

fileを変更せず、Claude、外部CLI、外部送信を起動しない。
