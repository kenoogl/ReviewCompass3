# 機微検査精密化 実用文書E2E Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-EXTERNAL-SEND-SCAN-REFINEMENT-009 / v2`（受入条件8）
- 利用者指示：「推奨どおり観測recordで実送信E2Eを実施せよ」（2026-08-16 chat）
- 実施担当：Claude（送信コマンドの実行を含む。鍵は`~/.zshrc`経由でプロセス内のみ）

## 1. 実施内容

【実測】精密化前は高乱雑性誤検知で送信不能だった実用文書——本契約を生んだ観測record
`records/development/2026-08-16-egress-sensitive-scan-false-positive-observation-v1.json`
（長いhyphen連結file名・乱雑度数値・ID記載を含むJSON、commit `9dac36c`済み）——を資料とする
送信指示`ORD-G20-REAL-DOC-001`を、改名後の実行名`reviewcompass3-external-review-send`で一回実行した。

## 2. 結果

【実測】

- 終了コード0、`status: response_stored`、HTTP 200、`completed_at: 2026-08-16T10:58:44Z`
- 台帳着地：試行record→未加工応答（15,236 bytes）→結果recordの順。試行record計数2件（累計上限100の内）
- `payload_sha256`：`82012fe5b481358fe77d8e0f08d3e9862697365bf0877fc57787896c036c5999`
- `response_sha256`：`90b117ab9a4acca33c16b0caaafb36017050bddf026f52db5b8f45f7c443b259`
- 台帳3 fileはcommit `28ae24c`で履歴へ固定

## 3. 機械検証

【実測】

- attempt・resultの`record_sha256`：独立再計算と一致
- 応答fileのSHA-256：結果recordと一致
- 鍵の非出現：台帳3 file＋送信指示の全bytes走査で0件
- 応答model：指定どおり`gemini-3.1-pro-preview`（応答内`modelVersion`）
- 応答本文：資料（依頼記述を含まないJSON）の性質をGeminiが正しく認識し、「依頼記述が存在しない」旨と
  参考評価を日本語で返した（経路実証としては資料が届き読解されたことを示す）

## 4. 契約対応

受入条件8「実用文書を資料とする実送信E2Eを一回行い、精密化後の経路で実文書が送れることを実環境で
確認する」を充足した。**精密化の実用価値（誤検知で止まっていた文書が送れる）が実環境で実証された**。

## 5. 未実施

- 製品受入（受入条件9。残余risk 3点の最終受容を含む）。次に一判断として提示する。
