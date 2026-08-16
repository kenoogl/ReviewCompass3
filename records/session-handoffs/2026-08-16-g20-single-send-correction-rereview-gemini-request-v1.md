# 外部レビュア一回送信 訂正3点の限定再確認依頼record v1（Claude→Gemini・Human中継）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・訂正担当）
- 依頼先：Gemini（暫定体制。本repositoryのディレクトリを共有しており、対象fileを直接読める）
- 体制根拠：`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`
- レビュー種別：**限定再確認**（完了レビューの指摘3件に対する訂正の閉じと、退行の有無**だけ**を確認する。
  全面再レビューではない。読取り専用・repositoryへの書込みなし）
- 先行判定（修正要・あなた自身の前回判定）：
  `records/development/2026-08-16-external-reviewer-single-send-completion-review-v1.md`
  - SHA-256：`e429f167e57883aae04a72ad85a82416a7aa5801ec4bfc108facdf61a0d12aa9`

## 1. 対象と固定

- 訂正commit：`cfb0698`（変更は次の3 fileだけ：送信核1行・対象試験・訂正Evidence新規）
- 訂正Evidence：`records/development/2026-08-16-external-reviewer-single-send-correction-evidence-v1.md`
  - SHA-256：`1f10f9c37350bb1acd0173a6753d917b1baddfd670cba66baa546df28b153262`
- 訂正後の製品成果物：

| path | SHA-256 |
| --- | --- |
| `tools/external_review/gemini_send.py` | `1cb2de0c155a450fb3ca827005c2ea81fcb303728a2a85fdb18a8d63353c5538` |
| `tests/test_gemini_send.py` | `bba82572456376257d1b24f4a2a4422996a250a60709d8c29d1b82fd5f991c60` |

`gemini_send_entry.py`・`__init__.py`・`pyproject.toml`は訂正で変更していない（前回依頼record v2の
記載値のまま）。

## 2. 開始時の鮮度検査（Gemini（あなた）が最初に行う）

1. §1の3 file（訂正Evidence・製品成果物2件）のSHA-256を機械計算し、本record記載値との一致を確認する。
2. 可能なら`git show --stat cfb0698`で訂正commitの変更fileが§1記載の3 fileだけであることを確認する。
3. 不一致の場合は、確認せずその旨を判定文へ書いて停止する。

## 3. 依頼内容：訂正3点の閉じと退行の有無だけ

前回のあなたの指摘それぞれについて、訂正が最小修正案の趣旨どおり閉じているかを確認してください。

1. **指摘1の閉じ**：`tests/test_gemini_send.py`の`_install_transport`が
   `urllib.request.OpenerDirector.open`だけの差し替えになり、`_send_request`本体
   （`Request`生成・`_build_opener()`の実構成適用・`HTTPError`処理・読取り上限）が試験の実行域に
   入ったか。非200を実挙動と同型の`HTTPError`として返す模擬が妥当か。
2. **指摘2の閉じ**：正例試験`test_positive_send_lands_attempt_response_result`に、契約v5 §9の固定形から
   実装を参照せず独立に組み立てた期待payloadとの照合（`payload_sha256`・`payload_bytes`）が入ったか。
3. **指摘3の閉じ**：`gemini_send.py`の応答保存呼出しが`_publish(data, ...)`へ整理され、保存bytesが
   訂正前後で同一か。
4. **退行の有無**：前回`0件`と判定した範囲（未接続・禁止作用・上位目的への悪影響）への新たな干渉が
   訂正によって生じていないか。訂正Evidence§3の機械確認（対象49件・egress 107件・各製品・正規全試験
   2,362件の全緑）と矛盾する点がないか。

範囲外：前回判定で扱い済みの論点の再審、新規の全面レビュー。

## 4. 判定の形式（あなたに求める出力）

- 判定：`verified`（3訂正が閉じ・退行なし）または`修正要`（閉じていない訂正と最小修正案を明示）
- 各主張に根拠（fileの関数名・行の内容、契約の節番号）を付ける
- 判定文の冒頭にあなたのmodel名を記載する

## 5. 手順（Human・Claude向け）

1. 利用者がGeminiへ本依頼recordのpath
   （`records/session-handoffs/2026-08-16-g20-single-send-correction-rereview-gemini-request-v1.md`）を伝える。
2. Geminiは§2の鮮度検査→§3の限定確認を行い、§4の形式で判定文を返す。
3. 利用者が判定文をClaudeへ貼り戻す。Claudeが判定record
   `records/development/2026-08-16-external-reviewer-single-send-correction-rereview-v1.md`へ転記・commitし、
   根拠と実物の整合を機械照合する。
4. `verified`なら利用者へ実送信E2E（受入条件13）の実施判断を求める。`修正要`なら停止して利用者へ諮る。
