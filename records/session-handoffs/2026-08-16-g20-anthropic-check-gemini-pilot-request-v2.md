# anthropic-api経路確認 Gemini操縦実行依頼record v2（再実行・Claude準備→Gemini実行・Human中継）

- 作成日：2026-08-16
- supersedes：`records/session-handoffs/2026-08-16-g20-anthropic-check-gemini-pilot-request-v1.md`
- 再実行の根拠：v1実行は`record_write_failed`（終了コード4）で停止した。Claudeが台帳を機械確認した結果、
  試行record・応答・結果・一時fileのいずれも不存在＝**試行record作成の時点で失敗し、送信は起きていない**。
  台帳無傷のため、同一送信指示での再実行は二重送信にならない。原因はGemini環境のfile書込み権限と
  推定される（読取りコマンドは成功実績あり・書込みは初）。
- 実行担当：Gemini（**書込みを含むコマンドの実行になる。環境が書込みの承認を求めたら許可すること**）

## 1. 対象と固定（v1と同一）

- 送信指示：`records/development/2026-08-16-g20-anthropic-check-order-v1.json`
  - SHA-256：`99260adf7833bf7d319dc291b103596be6b6da43ba0e80d29bfe983c668430ab`
- 由来file：`docs/development/e2e-live-send-check.md`
  - SHA-256：`5469e359ec9baaf6522ade8ceca56b4723c11912494a377e8320702298f88d34`

## 2. あなた（Gemini）が行う手順

1. **鮮度検査**：§1の2 fileのSHA-256を機械計算し、記載値との一致を確認する。
2. **台帳の事前確認**：`ls /Users/Daily/Development/ReviewCompass3/.reviewcompass/egress-ledger/`に
   `ORD-G20-ANT-CHK-001`で始まるfileが**存在しない**ことを確認する（存在したら実行せず停止して報告）。
3. **一回だけ実行**（鍵の値を画面・報告へ出さない。環境が書込み承認を求めたら許可する）：

   ```
   ANTHROPIC_API_KEY=$(zsh -c 'source ~/.zshrc >/dev/null 2>&1; print -r -- "$ANTHROPIC_API_KEY"') /Users/Daily/Development/ReviewCompass3/.venv/bin/reviewcompass3-external-review-send send --order /Users/Daily/Development/ReviewCompass3/records/development/2026-08-16-g20-anthropic-check-order-v1.json
   ```

4. **報告**：標準出力のJSON一行と終了コードをそのまま貼る。失敗でも再実行しない。

## 3. 禁止事項（v1と同一）

- 鍵の値の表示・転記。送信指示・由来file・製品コードの変更。本record§2.3の1回を超える実行。

## 4. 後続（Human・Claude向け）

利用者が報告をClaudeへ貼り戻し、Claudeが台帳3 recordの着地・独立再計算・鍵非出現を機械確認して
commitへ固定する。
