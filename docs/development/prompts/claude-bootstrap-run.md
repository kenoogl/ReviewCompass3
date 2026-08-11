# 無工具Claude疎通の実行入口

この入口は、Codex主担当が固定済みの二つの非機密payloadでClaude Codeとの疎通だけを確認する場合に使う。
実装委譲、一般対話、任意prompt送信には使わない。

正本は
`records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v3.md`
である。実行入口は次の一つだけとする。

```text
reviewcompass3-pilot bootstrap --manifest-digest <sha256> --approval-id <id>
```

実送信の前には、完了レビューが`verified`であることと、送信対象へ束縛した別のHuman承認を確認する。
RED開始承認を送信承認として扱わない。

完了レビュー担当は、上流から受入条件を独立導出し、実装fixtureにない反証を最低一件作る。所見は共通
レビュープロトコルの次の閉じた四類型へ分類する。

- `scope_deviation`
- `missing_acceptance_evidence`
- `unresolved_regression`
- `insufficient_independence`

Claudeのprocess作成、認証確認、実送信は、完全に束縛したHuman承認がある実行時だけ行う。試験とレビューでは
標準ライブラリの模擬processだけを使用する。
