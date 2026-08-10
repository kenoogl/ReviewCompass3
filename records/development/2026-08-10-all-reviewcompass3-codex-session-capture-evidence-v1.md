---
evidence_id: RC3-ALL-REVIEWCOMPASS3-CODEX-SESSION-CAPTURE-2026-08-10-V1
recorded_at: 2026-08-10T23:57:41+09:00
status: verified_with_live_boundary
workflow_state: reconciled
confidentiality_class: project-internal-value-safe
---

# ReviewCompass3 Codexセッション全件保存 Evidence V1

## 1. 実施と結果

Humanの「ReviewCompass3に属する未記録分をすべて記録して」という指示に基づき、Codex rolloutの
`session_meta.payload.cwd`がReviewCompass3のrepository rootまたはその子孫を指す81件を選択した。
別projectのCodexログとClaudeログは選択していない。

既存の保存済み2件は元ログのbyte-exact prefixであり、divergenceは0件だった。1回目の保存では79件を
新規作成し、2件を追記更新した。全81件が`reconciled`、event 25,545件、parse issue 0件となった。
直後の2回目は81件すべて`unchanged`で、重複保存はなかった。

保存時点のraw合計は204,915,411 bytes、private verbatim transcript合計は73,704,951 bytesだった。
raw、verbatim、cursor、private Provenanceは各81件、integrity ledgerは1件である。redacted transcriptは
今回のscope外であり0件である。

## 2. Authority

| role | path | SHA-256 |
| --- | --- | --- |
| Human scope Decision | `records/development/2026-08-10-all-reviewcompass3-codex-session-capture-decision-v1.json` | `6d1367e121959197cd71a8e33a2e9aa45a95b20b18decc20688c708ef68ecbc6` |
| Task Contract v3 | `records/task-contract/session-transcript-eventual-preservation-v3.json` | `4e9498e3514aa5efcf4a9803b2ca49ba16e774500e5be51b571c728d74bd480f` |
| Capture receipt | `records/development/2026-08-10-all-reviewcompass3-codex-session-capture-receipt-v1.json` | `01772320b3575c13d1244254c6adac848b8b7ea7c45cbdbbf65b1ee9a84fd767` |

Task Contractの固定source 10件は保存前に機械照合し、全件一致した。対象相対path 81件のmanifest
SHA-256は`6814e2002b0a42dc906fe5b1598d4565f8945d606b30a0e552f6009168cbd298`である。
private absolute path、session本文、prompt、response、Tool引数・結果本文は本Evidenceとreceiptへ記録していない。

## 3. 変換処理のTDD

最初の全件保存は、2件目のログに未対応形式が156件あったため、rawを保全した後に安全停止した。
内訳は`inter_agent_communication_metadata` 77件、`agent_message` 77件、`tool_search_call` 1件、
`tool_search_output` 1件だった。Humanの「変換処理を対応させればよい」という指示を受け、保存処理を
拡張せずCodex rollout parserだけをTDDで変更した。

- RED commit：`aba54c73ef21f184d65d55981b906994b7d3c47c`
- RED結果：`1 failed, 2 passed`、exit code 1
- GREEN commit：`1a37d3d0c542570582ca36abea3cb29d454c76b0`
- GREEN結果：parser targeted `3 passed`、exit code 0

エージェント間メッセージはauthor、recipient、平文contentを逐語記録へ残す。既知の暗号化内部contentは
逐語記録へ出さない。Tool search call／outputは同じcall IDを持つTool Call／Tool Resultとして変換する。
変更後に実ログ81件を読取りだけで全件変換し、未対応形式0件、parse issue 0件を確認した。

## 4. 保存後の独立照合

保存処理の出力とは別に81件を再読込し、次を確認した。

- 必須artifact欠落：0件
- rawからのverbatim再生成不一致：0件
- parse issue：0件
- sourceとrawのdivergence：0件
- `0700`でないprivate directory：0件
- `0600`でないprivate file：0件
- temporary file／lock file残留：0件
- repository内private artifact：0件

同期的な保存処理が返った時点ではsourceとrawは81件すべて一致した。その後、この実行中Codex task自身が
保存結果と検証操作を追記したため、2026-08-10T23:57:41+09:00の再観測では80件が完全一致、現在の1件だけに
36,083 bytesの純粋な追記があった。これは既存rawとのprefix関係を維持しており、divergenceではない。
実行中taskは最終報告まで増えるため、同期処理だけで最終byteまで閉じることはできない。既存81件の
保存完了判断とは分離し、live boundaryとして明示する。

## 5. Testとrepository境界

各commandは単独実行し、終了コードを直接確認した。

| command | result | exit code |
| --- | --- | --- |
| `.venv/bin/python3 -m pytest -q tests/test_session_log_parse_codex_rollout.py` | `3 passed` | 0 |
| parser／adapter／regeneration／preservation／mutation assurance 5 file | `28 passed` | 0 |
| `.venv/bin/python3 -m pytest -q tests/test_session_log_*.py` | `177 passed` | 0 |
| `.venv/bin/python3 -m pytest -q` | `1470 passed in 13.92s` | 0 |

private artifactはrepository外にあり、Gitへstageしていない。外部送信、別projectのsession取得、Claude取得、
redaction、scheduler／hook／watcher／background service有効化、retention削除、backupは実施していない。

## 6. 判断

固定した81件はraw原本、逐語記録、cursor、Provenance、integrity ledgerへ保存され、変換issue 0件、
再生成不一致0件、divergence 0件、同一再実行時の重複0件である。したがって本作業を
`verified_with_live_boundary / reconciled`と判断する。
