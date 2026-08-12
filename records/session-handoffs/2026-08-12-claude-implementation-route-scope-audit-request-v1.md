# Claude実装委譲経路 範囲固定 指示品質監査依頼 v1

- 状態：`fixed_request`
- 対象commit：`3586ee6d23eab385d50e6586b834090afb8f94ce`
- 監査担当：新しい会話状態の`gpt-5.6-terra`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定対象

- 範囲固定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v1.md`
- 範囲固定SHA-256：`fccbad6f82a86363500ea16b1a347793fc514a566de362dd701acb408549497f`
- 選択裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-selection-human-decision-v1.md`
- 選択裁定SHA-256：`e50b1bc3c17ec56cd3c38ca61b4cc5abea566b921a7e7c316f173cddeddb6e4c`

参照する上流文書は次の2件とする。

- `docs/development/pilot-specific-claude-codex-collaboration.md`
- `docs/development/work-review-protocol.md`

## 2. 監査範囲

範囲固定v1が、Claude実装委譲経路を実装するための入力として、欠落、矛盾、誘導、対象違い、材料不足、
範囲逸脱を含まないか確認する。特に、Human承認境界、Claudeの認証・モデル・道具・読取・書込・Bash・
ネットワークの境界、REDとGREENの分離、保存結果、独立レビューを確認する。

実装方法の細部、将来拡張、一般的な強化案は所見にしない。blockingにする場合は
`docs/development/work-review-protocol.md` §11.1の4類型のどれかを示す。範囲外の提案は
`deferred`とし、現在の合否を止めない。

要求識別子は`AC-CD-001`〜`007`、`NG-CD-001`〜`007`、`ST-CD-001`〜`006`、
`OUT-CD-001`〜`005`の25件である。各識別子を一度ずつ確認する。

## 3. 出力

最終応答は説明文を付けず、次の構造を持つ単一JSON objectにする。

```json
{
  "schema_version": 1,
  "kind": "instruction_quality_audit",
  "target_sha256": "固定対象のSHA-256",
  "auditor_model": "gpt-5.6-terra",
  "verdict": "no_findings | findings_present | reported_unverified",
  "requirement_results": [
    {
      "requirement_id": "AC-CD-001",
      "status": "covered | finding",
      "evidence": "対象節または所見ID"
    }
  ],
  "findings": [
    {
      "finding_id": "PA-CD-001",
      "classification": "missing | contradictory | misleading | ambiguous | scope_escape | material_insufficient",
      "severity": "blocking | non_blocking",
      "review_stage": "scope",
      "blocking_type": "1 | 2 | 3 | 4 | null",
      "affected_requirement_ids": ["AC-CD-001"],
      "evidence": "対象文と問題の具体的説明",
      "proposed_correction": "必要最小限の訂正"
    }
  ],
  "deferred": [],
  "limits": []
}
```

`requirement_results`は25件を固定順で一度ずつ列挙する。所見IDは出現順に連番とし、所見0件なら
`findings`を空配列にする。監査担当はfileを変更せず、Claude、外部CLI、外部送信を起動しない。
