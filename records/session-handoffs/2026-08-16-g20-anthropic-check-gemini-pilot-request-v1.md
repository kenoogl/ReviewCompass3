# anthropic-api経路確認 Gemini操縦実行依頼record v1（Claude準備→Gemini実行・Human中継）

- 作成日：2026-08-16
- 準備担当：Claude（送信指示JSONの下書きとcommit固定まで）
- 実行担当：Gemini（本repositoryのディレクトリを共有。**あなたが操縦者として一回の送信を実行する**）
- 利用者指示：anthropic-apiの実環境テスト（2026-08-16 chat。独立性検査をはずさない代替案として、
  Gemini操縦での送信を利用者が承認）
- 背景：送信指示の`pilot_provider`（操縦LLMの系列宣言）と宛先が同一だと`reviewer_not_independent`で
  停止する設計のため、Claude（anthropic系）操縦ではanthropic-apiへ送れない。あなた（gemini系）が
  実行することで、`pilot_provider: gemini-api`・宛先`anthropic-api`という**真実かつ検査適合**の
  組み合わせになる。

## 1. 対象と固定

- 送信指示：`records/development/2026-08-16-g20-anthropic-check-order-v1.json`
  - SHA-256：`99260adf7833bf7d319dc291b103596be6b6da43ba0e80d29bfe983c668430ab`
  - 内容：宛先`anthropic-api`／model `claude-sonnet-5`（実在を一覧APIで確認済み）／操縦宣言`gemini-api`／
    資料は確認用文書1件
- 由来file：`docs/development/e2e-live-send-check.md`
  - SHA-256：`5469e359ec9baaf6522ade8ceca56b4723c11912494a377e8320702298f88d34`

## 2. あなた（Gemini）が行う手順

1. **鮮度検査**：§1の2 file（送信指示・由来file）のSHA-256を機械計算し、本record記載値との一致を確認する。
   由来fileがGit管理下でcommit済みであること（`git log --format=%h -1 -- docs/development/e2e-live-send-check.md`が
   commitを返すこと）も確認する。不一致・未commitなら実行せず停止して報告する。
2. **送信指示の内容確認**：JSONを読み、宛先・model・資料・目的が本record§1の記載と一致することを確認する。
   **送信指示を書き換えてはならない**。
3. **一回だけ実行**：次のコマンドをそのまま実行する（鍵は`~/.zshrc`からプロセス内だけへ取り出す。
   **鍵の値を画面・報告へ出してはならない**）。

   ```
   ANTHROPIC_API_KEY=$(zsh -c 'source ~/.zshrc >/dev/null 2>&1; print -r -- "$ANTHROPIC_API_KEY"') /Users/Daily/Development/ReviewCompass3/.venv/bin/reviewcompass3-external-review-send send --order /Users/Daily/Development/ReviewCompass3/records/development/2026-08-16-g20-anthropic-check-order-v1.json
   ```

4. **報告**：標準出力のJSON一行と終了コードを、そのまま（書き換えずに）報告へ貼る。
   失敗（停止JSON）の場合も再実行せず、そのまま報告する。

## 3. 禁止事項

- 鍵の値の表示・転記。送信指示・由来file・製品コードの変更。2回以上の実行（再送は新しい送信指示を要する）。

## 4. 後続（Human・Claude向け）

1. 利用者がGeminiの報告（結果JSON・終了コード）をClaudeへ貼り戻す。
2. Claudeが台帳3 record（`ORD-G20-ANT-CHK-001--*`）の着地・内容識別値の独立再計算・鍵非出現を機械確認し、
   台帳をcommitへ固定して記録する。
