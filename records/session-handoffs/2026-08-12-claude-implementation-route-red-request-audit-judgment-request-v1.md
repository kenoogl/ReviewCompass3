# Claude実装委譲経路 RED試験依頼 監査判定依頼 v1

- 状態：`fixed_request`
- 対象依頼SHA-256：`5f86733ca8c89eb30ce228ce24acea6860776f47445ad806d901f697c46333c7`
- 監査未加工結果：`2026-08-12-claude-implementation-route-red-request-audit-raw-v1.json`
- 監査未加工結果SHA-256：`cfff17d60ea21b486029395266e7a8a765fcbe5e645107456d12201e5135e582`
- 判定担当：監査担当とは別の新しい`gpt-5.6-terra`
- 変更権限・外部送信権限：なし

## 判定対象

監査所見`PA-CD-RED-001`〜`003`を、範囲固定v3、RED開始裁定、権限裁定、RED試験作成依頼に照らして
全件一度ずつ判定する。各所見へ`adopt`、`reject`、`hold`の推奨を付ける。blocking類型は
`docs/development/work-review-protocol.md`§11.1の`1`〜`4`または`not_blocking`だけを使う。

新しい所見、一般的な強化案、実装詳細を追加しない。Humanの最終採否を代理しない。

最終応答は説明文なしの単一JSON objectとし、`schema_version`、`kind`、`target_sha256`、
`audit_raw_sha256`、`judge_model`、`coverage`、`judgments`、`verdict`を持つ。`coverage`は期待・実際とも
3所見を固定順で持ち、`exact_once`を示す。`judgments`は各所見ID、推奨、blocking類型、理由を持つ。
