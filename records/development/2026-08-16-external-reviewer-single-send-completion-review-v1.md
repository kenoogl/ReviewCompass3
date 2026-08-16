# 外部レビュア一回送信 独立完了レビュー v1（Gemini・Human中継）

- Reviewer：Gemini 3.1 Pro (High)（利用者がディレクトリ共有のGeminiへ依頼recordのpathを伝達。
  判定文は利用者がchatへ貼り付け、Claudeが本recordへ転記した）
- 中継：Human中継（暫定体制`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`による）
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g20-single-send-completion-review-gemini-request-v2.md`
  - SHA-256：`4888796d5ce5c9242400065a85d2043a8cc00c67b13a07cd3ef3b73019013936`
- 対象：GREEN commit `2beb5c264171e94f5921a9f698caf532a0616496`の実装（契約v5受入条件12）
- 判定：`修正要`（blocking 2件・non-blocking 1件。未接続0件・禁止作用0件・上位目的への悪影響0件）
- 経緯注記：1回目の依頼はGemini側の作業directoryが別場所（`/Users/keno/Documents/`配下の空のgit入れ物、
  2026-07-27作成・commit 0件）を向いており、依頼record不存在の前提不一致で正しく停止した。本repository
  （`/Users/Daily/Development/ReviewCompass3`）を開き直した2回目で鮮度検査から実施された。

## 1. 判定の転記（要旨）

【記録】

- **鮮度検査：合格**。対象7 fileのSHA-256を機械計算しrecord記載値と完全一致、作業treeがcleanであることを確認。
- **指摘1（誤合格・blocking）**：試験の通信模擬が`_send_request`関数全体の差し替え
  （`tests/test_gemini_send.py`の`_install_transport`）であるため、`_send_request`本体の
  `urllib.request.Request`生成・`opener.open()`呼出しが試験で一度も実行されない。この部分に欠陥があっても
  試験は合格してしまう。最小修正案：より下層（`urllib.request.OpenerDirector.open`等）の差し替えへ変更し、
  `_send_request`本体を試験対象に含める。
- **指摘2（誤合格・blocking）**：`payload_sha256`の独立oracle再計算が試験にない。
  `test_positive_send_lands_attempt_response_result`は`result`と`attempt`の`payload_sha256`一致だけを
  確認しており、実装`_build_payload`が契約§9の固定形から逸脱しても検知できない。最小修正案：試験内で
  契約§9に従い期待payloadを独立に組み立て、そのSHA-256と`attempt["payload_sha256"]`の一致を確認する。
- **指摘3（開示済みSR-IMPL-1・non-blocking）**：`gemini_send.py`602行の無意味な条件式
  （`data if data.endswith(b"") else data`は常に前者）。機能への影響（退行）は一切なし。
  最小修正案：後続整理で`data`とだけ記述する。
- **未接続：0件**（各停止の入口停止JSON・終了コードまでの配線は正しい）。
- **禁止作用：0件**（再試行・URL鍵混入・proxy使用等の残存経路なし）。
- **上位目的への悪影響：0件**（`tools/egress/`の分離維持、Human承認境界の整合）。

## 2. Claudeによる機械照合

【実測】判定文が参照する根拠と実物の一致を確認した。

| 判定文の根拠 | 実物 | 一致 |
| --- | --- | --- |
| 契約v5 §12受入条件1「各内容識別値の独立oracle再計算」 | 契約候補v5 293行に文言あり | 一致 |
| `_install_transport`が`_send_request`を差し替え | `tests/test_gemini_send.py` 108行 | 一致 |
| `payload_sha256`は実装出力同士の一致検査のみ | 同 168行（独立再計算なし） | 一致 |
| 602行の無意味な条件式 | `tools/external_review/gemini_send.py` 602行 | 一致 |

指摘1・2は起草側自己レビュー（`records/development/2026-08-16-external-reviewer-single-send-impl-self-review-v1.md`）
が「限界」として挙げた模擬層の位置の論点を、受入条件1・7の要求水準（模擬層での実質確認・独立oracle）に照らして
blockingへ具体化したものであり、契約整合の観点で正当である。指摘3は利用者裁定(A)（2026-08-16 chat）の
「修正要判定が出た場合に他の指摘とまとめて1回で直す」に該当する。

## 3. 未実施・次

- 指摘への対応（試験の強化2件・実装1行の整理）は本record固定時点で未実施。利用者へ最小修正の扱いを諮り、
  停止する（依頼record§6手順5）。
- 修正後は限定再確認（修正点の閉じと退行の有無だけ）を暫定体制で受け、`verified`後に実送信E2E
  （受入条件13）の実施判断を利用者へ求める。
