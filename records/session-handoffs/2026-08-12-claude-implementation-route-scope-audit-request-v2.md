# Claude実装委譲経路 範囲固定 指示品質監査依頼 v2

- 状態：`fixed_request`
- 周回：2（上限2）
- 対象commit：`67e37f0d72bbb36cc8d9d01ce419aff71530c5ca`
- 監査担当：新しい会話状態の`gpt-5.6-terra`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定対象

- 範囲固定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v2.md`
- 範囲固定SHA-256：`9881f7df526c3aef8c21e665f75927329608d1b0518e343db0ac5c89f954a024`
- Human裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-finding-human-decision-v1.md`
- Human裁定SHA-256：`0565a68c8c9c363d3998f50225e78ff7b97aaff6b9e0e57662b8d48f05a71b37`
- 前周所見：`PA-CD-001`
- 前周判定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-audit-judgment-result-v1.md`
- 選択裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-selection-human-decision-v1.md`
- 上流文書：`docs/development/pilot-specific-claude-codex-collaboration.md`
- レビュー規則：`docs/development/work-review-protocol.md`

## 2. 監査範囲

`PA-CD-001`がHuman裁定どおり解消されたか確認し、v2の変更が新しい矛盾、欠落、誘導、対象違い、
材料不足、範囲逸脱を作っていないか確認する。`AC-CD-001`〜`007`、`NG-CD-001`〜`007`、
`ST-CD-001`〜`006`、`OUT-CD-001`〜`005`の25件を固定順で一度ずつ確認する。

実装方法の細部、将来拡張、一般的な強化案は所見にしない。blockingは
`docs/development/work-review-protocol.md` §11.1の4類型だけとする。同じ種類の所見を前周の言い換えで
繰り返さない。

## 3. 出力

最終応答は説明文なしの単一JSON objectとし、v1監査依頼§3の構造に次を加える。

- `round`: `2`
- `resolved_prior_findings`: `[ {"finding_id":"PA-CD-001", "status":"resolved | unresolved", "evidence":"..."} ]`

`target_sha256`はv2のSHA-256、`auditor_model`は`gpt-5.6-terra`とする。新規所見IDは
`PA-CD-R2-001`から連番にする。要求結果は25件を固定順で一度ずつ列挙する。fileを変更せず、Claude、
外部CLI、外部送信を起動しない。
