# Claude実装委譲経路 第1縦切り 独立範囲レビュー依頼 v1

- 状態：`fixed_request`
- 対象commit：`3586ee6d23eab385d50e6586b834090afb8f94ce`
- レビュー担当：新しい会話状態の`gpt-5.6-terra`
- レビュー段階：`scope`
- 危険度：`high`
- 変更権限：なし
- 外部送信権限：なし

## 1. 固定対象

- 範囲固定：`records/session-handoffs/2026-08-12-claude-implementation-route-scope-v1.md`
- 範囲固定SHA-256：`fccbad6f82a86363500ea16b1a347793fc514a566de362dd701acb408549497f`
- 選択裁定：`records/session-handoffs/2026-08-12-claude-implementation-route-selection-human-decision-v1.md`
- 選択裁定SHA-256：`e50b1bc3c17ec56cd3c38ca61b4cc5abea566b921a7e7c316f173cddeddb6e4c`

上流文書：

- `docs/development/pilot-specific-claude-codex-collaboration.md`
- `docs/development/work-review-protocol.md`

## 2. 判定対象

次だけを確認する。

1. 選択裁定および上流文書と矛盾しない。
2. high riskが妥当で、Human承認と外部送信の境界を保持する。
3. 確認運転でReviewCompass3本体をClaudeへ送らず、合成repositoryだけを使う。
4. Claudeに必要な発見性を残しつつ、読取・書込・Bash・ネットワーク・外部道具の境界が、
   誤った合格を許さない方向で受入条件と停止条件へ接続される。
5. 25件の要求が、目的、実行順序、変更範囲、出力へつながる。

範囲レビューなので、command option、fixture構成、保存形式の細部はblockingにしない。blockingは
`docs/development/work-review-protocol.md` §11.1の4類型だけとする。同じ欠陥類型の変種はこの一周で
まとめる。範囲外の将来設計は`deferred`へ回す。

独立反証は1件までとし、「この範囲固定どおりの実装でも、禁止された読取・書込・送信またはHuman境界の
迂回が合格し得るか」を具体例で試す。codeやfileは変更しない。

## 3. 出力

最終応答は説明文を付けず、次の構造を持つ単一JSON objectにする。

```json
{
  "schema_version": 1,
  "kind": "scope_review",
  "target_sha256": "固定対象のSHA-256",
  "reviewer_model": "gpt-5.6-terra",
  "verdict": "verified | blocking_findings | reported_unverified",
  "requirement_results": [
    {
      "requirement_id": "AC-CD-001",
      "status": "satisfied | blocking | non_blocking",
      "evidence": "対象節または所見ID"
    }
  ],
  "findings": [
    {
      "finding_id": "SR-CD-001",
      "severity": "blocking | non_blocking",
      "review_stage": "scope",
      "blocking_type": "1 | 2 | 3 | 4 | null",
      "affected_requirement_ids": ["AC-CD-001"],
      "evidence": "対象文と問題の具体的説明",
      "required_correction": "必要最小限の訂正"
    }
  ],
  "counterexample": {
    "scenario": "試した具体例",
    "result": "rejected_by_scope | could_be_accepted | not_applicable",
    "evidence": "根拠"
  },
  "deferred": [],
  "limits": []
}
```

`requirement_results`は`AC-CD-001`〜`007`、`NG-CD-001`〜`007`、`ST-CD-001`〜`006`、
`OUT-CD-001`〜`005`を固定順で一度ずつ列挙する。レビュー担当はfileを変更せず、Claude、外部CLI、
外部送信を起動しない。
