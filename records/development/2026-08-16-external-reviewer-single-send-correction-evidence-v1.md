# 外部レビュア一回送信 完了レビュー指摘3件の訂正Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5`
- 判定record（修正要・blocking 2件・non-blocking 1件）：
  `records/development/2026-08-16-external-reviewer-single-send-completion-review-v1.md`、
  SHA-256 `e429f167e57883aae04a72ad85a82416a7aa5801ec4bfc108facdf61a0d12aa9`
- 利用者判断：3指摘とも修正する（(A)裁定、2026-08-16 chat）。指摘3は先行裁定(A)
  「修正要判定が出た場合に他の指摘とまとめて1回で直す」の履行
- 訂正担当：Claude

## 1. 訂正内容

### 指摘1（blocking）：通信模擬の差し替え位置を下層へ変更

【実測】`tests/test_gemini_send.py`の`_install_transport`を、`_send_request`関数全体の差し替えから
`urllib.request.OpenerDirector.open`だけの差し替えへ変更した。これにより`_send_request`本体
（`urllib.request.Request`の生成、`_build_opener()`による実handler構成の適用、`HTTPError`処理、
読取り上限`_RESPONSE_LIMIT + 1`）が試験の実行域に入った。模擬の忠実度も実挙動へ寄せた：
非200応答は実urllibと同型の`urllib.error.HTTPError`として返し、redirect（3xx）も
`HTTPError`経路に入る。記録するheader名は`Request`の正規化差を吸収するため小文字へ統一し、
既存試験の期待key 1箇所（`Authorization`→`authorization`）を合わせた。

### 指摘2（blocking）：payloadの独立oracle照合を追加

【実測】正例試験`test_positive_send_lands_attempt_response_result`へ、契約§9の固定形（固定前文・
`----- FILE: {path} (sha256={digest}) -----`区切り行・file内容の改行連結）から**実装を参照せず**
独立に組み立てた期待payloadとの照合を追加した。`attempt["payload_sha256"]`が期待bytesのSHA-256と、
`attempt["payload_bytes"]`が期待bytes長と一致することを検査する。

### 指摘3（non-blocking）：602行の冗長式を整理

【実測】`tools/external_review/gemini_send.py`の応答保存呼出しを
`_publish(data if data.endswith(b"") else data, ...)`から`_publish(data, ...)`へ整理した。
保存されるbytesは訂正前後で同一（条件式は常に前者を選んでいた）。

## 2. 訂正後の内容識別値

| path | SHA-256 |
| --- | --- |
| `tools/external_review/gemini_send.py` | `1cb2de0c155a450fb3ca827005c2ea81fcb303728a2a85fdb18a8d63353c5538` |
| `tests/test_gemini_send.py` | `bba82572456376257d1b24f4a2a4422996a250a60709d8c29d1b82fd5f991c60` |

`gemini_send_entry.py`・`__init__.py`・`pyproject.toml`は訂正で変更していない。

## 3. 機械確認（各単独command・終了コード個別判定）

【実測】

- 対象試験：49件成功、終了コード0（強化後の下層模擬・独立oracleの下で現実装が全緑＝隠れた実装欠陥が
  なかったことが強化試験でも実証された）
- egress関連：107件成功、終了コード0（敵対試験の不変条件維持）
- G02対象158件・G08対象107件・G24対象111件・実行器75件・G30基盤e2e 38件：各単独成功、終了コード0
- 保護path（基準commitからの差分）：差分0、終了コード0
- 正規全試験（禁止認証隔離条件）：2,362件成功、終了コード0
- `git diff --check`：終了コード0

## 4. 未実施

- 限定再確認（修正点の閉じと退行の有無だけ。暫定体制：Gemini・Human中継）
- 実送信E2E（受入条件13）、製品受入（受入条件14）
