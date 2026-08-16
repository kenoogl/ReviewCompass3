# 3 provider実環境確認 Evidence v1

- 実施日：2026-08-16
- 位置づけ：受入済み送信路（契約008・009）の追加実環境確認（利用者指示）。契約の受入条件外の運用確認
- 利用者指示：「openai-apiの実環境確認を一回実施せよ。また、anthropic-apiは禁止条件をはずし、テストせよ」
  →Claudeが独立性検査をはずすことへ反対根拠を提示し、利用者が代替案（Gemini操縦）を承認（2026-08-16 chat）

## 1. 確認結果（全provider・本製品経路でHTTP 200）

| provider | model（応答内の実名） | 操縦（pilot宣言） | 実行者 | 応答bytes | 台帳識別子 |
| --- | --- | --- | --- | ---: | --- |
| gemini-api | gemini-3.1-pro-preview | anthropic-api | Claude | 4,905／15,236 | `ORD-G20-LIVE-E2E-001`／`ORD-G20-REAL-DOC-001` |
| openai-api | gpt-5-mini-2025-08-07 | anthropic-api | Claude | 1,098 | `ORD-G20-OPENAI-CHK-001` |
| anthropic-api | claude-sonnet-5 | **gemini-api** | **Gemini 3.1 Pro** | 2,647 | `ORD-G20-ANT-CHK-001` |

- 全件で試行record→未加工応答→結果recordの台帳着地、`record_sha256`独立再計算一致、応答digest一致、
  鍵の非出現走査0件を機械確認した。試行record計数4件（累計上限100の内）。
- model名は事前に各providerの一覧API（読取り専用GET）で実在確認した（鍵有効性の確認を兼ねる）。
- 同一資料（確認用文書）の`payload_sha256`が3送信で完全一致（`69da2e0a…`）——payload機械構成の決定性の実証。

## 2. anthropic-api確認の経緯（独立性検査を守った代替案）

1. 利用者の当初指示は「禁止条件をはずしてテスト」だったが、独立性検査（操縦LLMと同系列への送信禁止）は
   契約008の中心的な守りであり、はずすには契約改定・実装変更・試験書換え・独立レビューが必要と説明した。
2. 代替案として、**Gemini操縦での送信**（`pilot_provider: gemini-api`・宛先`anthropic-api`＝真実かつ
   検査適合の組み合わせ）を提案し、利用者が承認した。
3. Gemini実行の1回目は`record_write_failed`（終了コード4）で停止。Claudeが台帳を機械確認し、試行record・
   一時fileとも不存在＝**送信ゼロ**を確定（原因はGemini環境の書込み権限）。台帳無傷の根拠つきで
   再実行依頼v2を出し、書込み許可後の再実行で成功した。停止→切り分け→根拠つき再実行の全経緯は
   依頼record v1・v2（`records/session-handoffs/`）に固定した。

## 3. 副次的な観測（改善候補の種・未登録）

【実測】1回目のGemini実行の停止JSONは`external_send_approved: true`を表示したが、実際は試行record
着地前の失敗で送信は起きていない。実装（`_publish`）が台帳書込み失敗を一律`after_attempt=True`と
するため、契約008 v5 §10.3「試行record着地後の停止だけ`true`」と表示が微妙に不一致（安全側への
倒れ方だが、試行record作成自体の失敗では`false`が正確）。実害は小さいが、台帳監査の解釈を誤らせ得る。
本線の区切りで観測record→改善候補の正規経路へ登録するかをHumanへ諮る。

## 4. 到達点

**3 provider全てで、本製品経路（機微検査・digest束縛・台帳・鍵非表示）の実環境送信が確認された**。
独立性検査は一度も緩めていない。operator切り替え（Claude操縦→Gemini操縦）の実運用も初めて実証された。
