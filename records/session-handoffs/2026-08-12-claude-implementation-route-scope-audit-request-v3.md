# Claude実装委譲経路 範囲固定 指示品質再監査依頼 v3

- 状態：`fixed_request`
- 対象commit：`ecadd9b7cccb178e46265141c7983c2c7218927d`
- 監査担当：新しい会話状態の`gpt-5.6-terra`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定対象

- 範囲固定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v3.md`
- 範囲固定SHA-256：`063d4299e78c11c2060b012ff7f09d7feaa2eca318e879e35bd418a7015e689f`
- 権限裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-permission-finding-human-decision-v1.md`
- 権限裁定SHA-256：`49c705b5ddab15adc8b8dde2a2f402e6b4528301c8961f8e0cac26829490c106`
- 解消対象：`records/session-handoffs/2026-08-12-claude-implementation-route-pre-red-permission-finding-v1.md`
- 選択裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-selection-human-decision-v1.md`
- 開始裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-red-start-human-decision-v1.md`
- 上流文書：`docs/development/pilot-specific-claude-codex-collaboration.md`
- レビュー規則：`docs/development/work-review-protocol.md`

## 2. 監査範囲

権限所見がHuman裁定どおり解消されたか確認し、v3が新しい欠落、矛盾、誘導、対象違い、材料不足、
範囲逸脱を作っていないか確認する。特に、Claudeからcommand実行道具を外したこと、機械処理だけが固定
試験commandを実行すること、ターン分離、変更可能path、外部送信のHuman境界を確認する。

`AC-CD-001`〜`007`、`NG-CD-001`〜`007`、`ST-CD-001`〜`006`、`OUT-CD-001`〜`005`の25件を
固定順で一度ずつ確認する。実装方法の細部、将来拡張、一般的な強化案は所見にしない。blockingは
レビュー規則§11.1の4類型だけとする。

## 3. 出力

最終応答は説明文なしの単一JSON objectとし、
`records/session-handoffs/2026-08-12-claude-implementation-route-scope-audit-raw-v2.json`と同じ構造を使う。
`round`の代わりに`revalidation_cycle: 1`を持ち、次を一件だけ持つ。

```json
"resolved_pre_red_findings": [
  {"finding_id":"permission-command-boundary", "status":"resolved | unresolved", "evidence":"..."}
]
```

`target_sha256`はv3のSHA-256、`auditor_model`は`gpt-5.6-terra`とする。新規所見IDは
`PA-CD-V3-001`から連番にする。要求結果は25件を固定順で一度ずつ列挙する。fileを変更せず、Claude、
外部CLI、外部送信を起動しない。
