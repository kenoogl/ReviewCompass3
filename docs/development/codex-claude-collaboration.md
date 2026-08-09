# CodexとClaudeの連携方法

## 基本の分担

1. HumanがCodexへ作業内容を伝える。
2. Codexが必要な設計・判断・固定資料を確認し、Claude向け指示書を
   `records/session-handoffs/YYYY-MM-DD-codex-to-claude-<work>.md`へ作る。
3. Codexは、HumanがそのままClaudeへ貼れる短いメッセージを出す。
4. HumanがメッセージをClaudeへ渡す。CodexからClaudeへ直接送信しない。
5. Claudeは指示書と指定資料を読み、指示された範囲だけを実施する。
6. Claudeは作業結果を
   `records/session-handoffs/YYYY-MM-DD-claude-to-codex-<work>.md`へ書き、停止する。
7. HumanがCodexへ「Claude作業終了」と知らせる。
8. Codexがcommit、差分、Test、Digest、停止境界を独立確認する。

## Claudeへ渡すメッセージ

```text
次の指示書を全文読み、記載された範囲、作業順序、コミット境界、停止条件に従って作業してください。

<Codexが作成した指示書のrepository-relative path>

作業完了後は、指示書に指定されたClaudeからCodexへの完了報告を作成して停止してください。
Codexによる独立確認が終わるまで、次の作業へ進まないでください。
```

## Claudeが途中で停止した場合

- Claudeは、停止理由、再現command、結果、未実施範囲を完了報告へ書く。
- HumanがCodexへ「Claude作業終了」と知らせる。
- Codexが停止理由を確認し、必要ならHumanがそのままClaudeへ貼れる追加指示を出す。
- 元の指示を推測で広げず、追加指示で変更を許可された範囲だけ再開する。

## 注意

- 本手順は、Pilot起動・record正本方式（`docs/development/pilot-driven-record-handoff.md`）が
  使えない場合（CLI不通・認証切れ・未対応の役割割り当て）のfallback経路を兼ねる。
- HumanがClaudeとCodexの受け渡しを行う。
- Claudeの実装中にCodexは同じfileを変更しない。
- Claudeの報告だけで完了とせず、Codexがrepositoryの事後状態を確認する。
- push、外部送信、不可逆操作、意味的判断は、それぞれ必要なHuman承認なしに行わない。
