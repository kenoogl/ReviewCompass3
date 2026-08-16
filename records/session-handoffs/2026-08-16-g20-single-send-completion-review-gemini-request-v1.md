# 外部レビュア一回送信 独立完了レビュー依頼record v1（Claude→Gemini・Human中継）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・実装担当）
- 依頼先：Gemini（暫定体制。利用者が本依頼と対象全文を手動でGemini chatへ運搬する）
- 体制根拠：`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`
- レビュー種別：実装完了後の独立完了レビュー（契約v5受入条件12。読取り専用・repositoryへのaccessなし）
- 5段手続き：第1・2段（起草側自己レビューと文脈整理）は
  `records/development/2026-08-16-external-reviewer-single-send-impl-self-review-v1.md`として固定済み

## 1. 対象と固定

- 実装commit（GREEN）：`2beb5c264171e94f5921a9f698caf532a0616496`
- 失敗試験固定commit（RED）：`6f3e528`（実装未存在で48件失敗を確認済み。その後の実態合わせで対象49件）
- 採用中の契約v5：`records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v5.md`
  - SHA-256：`6fc7b37b07f65519e78353df23fc7277c1c9265956320e46d5e6e35608e9d165`
- v5採用judgment：`records/development/2026-08-16-external-reviewer-single-send-v5-adoption-decision-v1.md`
  - SHA-256：`0d80690cb5f71150701d2f6d8613a205c9e5b37a1865e74bd6db377d4e13811f`
- 実装成功Evidence：`records/development/2026-08-16-external-reviewer-single-send-green-evidence-v1.md`
  - SHA-256：`51bd4d40e8d6fd3424bae6dac16ca1bc6006e86f95e37c66c93e3465b74cfd9a`
- 製品成果物：

| path | SHA-256 |
| --- | --- |
| `tools/external_review/__init__.py` | `f6e35bfc930c80dac54ed4b88f1795048c4fe31dd9148226613a45b827123622` |
| `tools/external_review/gemini_send.py` | `c1988daf786d93374a566764b57a368bd6bf99b3a6b6dd5298122a6e66a1f0fd` |
| `tools/external_review/gemini_send_entry.py` | `f89a5ea1c15db40a6ac7f225dfc3c7989e0951a8024bd924bc4cd53865d7c3b8` |
| `tests/test_gemini_send.py` | `94d967287d0ca01eca25b34f79bcec2b9fb2c94fa11388b612fa3b7cced5387d` |

`pyproject.toml`の変更は実行名1行
（`reviewcompass3-gemini-send = "tools.external_review.gemini_send_entry:main"`）だけである。

## 2. Gemini（あなた）への依頼：反証4点

あなたは独立したレビュアです。運搬文面に含まれる契約v5・実装3 file・対象試験・実装成功Evidenceを読み、
次の4点をそれぞれ反証的に検査し、判定を返してください。各主張には根拠（契約の節番号、fileの関数名・
行の内容）を付けてください。

1. **誤合格**：対象試験49件が、実装の欠陥を見逃す構成になっていないか。特に(a)通信の模擬が
   `_send_request`関数の差し替えで行われるため、それより外側（要求構成・opener構成）の欠陥を試験が
   検出できるか、(b)台帳recordの内容識別値の再計算が実装と独立したoracleになっているか、(c)試験の
   期待値が契約ではなく実装の都合へ合わせられていないか。
2. **未接続**：定義されたが呼ばれない検査、到達しない分岐、契約が要求するのに実装・試験のどちらにも
   ない守りがないか（例：§7〜§10の各停止が入口の停止JSONと終了コードまで正しく配線されているか）。
3. **禁止作用**：契約が禁じる振る舞いの残存経路がないか——自動再試行、固定host・固定経路以外への要求、
   URL・台帳・標準出力・例外への鍵混入、環境proxyの使用、リダイレクト追従、TLS検証の無効化、
   選択provider以外の環境変数の読取り、台帳の時刻記録以外での時刻取得、台帳root以外への着地。
4. **上位目的への悪影響**：旧`tools/egress/`の段階1不変条件（配下に通信手段なし）の維持、受入済み4製品への
   不干渉、および「利用者の指示の下でだけ送信が起きる」というHuman承認境界（契約§2）との整合が、
   実装で損なわれていないか。

起草側の開示：`gemini_send.py`602行に無意味な条件式（`data if data.endswith(b"") else data`——常に前者）が
残っている。応答は無条件・無加工で保存されるため機能への影響はないと起草側は判断しているが、この判断の
当否と扱いもあなたの判定に含めてよい。

## 3. 判定の形式（あなたに求める出力）

- 判定：`verified`（誤合格・未接続・禁止作用・上位目的への悪影響0件）または`修正要`
- `修正要`の場合：同じ原因の変種をまとめた最小数の指摘と、各指摘の最小修正案。blocking（受入を止める）と
  non-blocking（後続整理でよい）を区別する
- 実施できなかった検査があれば「未検査」として明示する（検査済みと区別する）

## 4. 判断済み・範囲外（蒸し返し不要）

- 判断済み：送信ごとの人の確認は行わない（利用者決定・契約§2）。宛先3 provider切り替えと独立性検査
  （利用者指示）。台帳のrepository内配置（契約§7.3）。置き場所`tools/external_review/`（v5軽微訂正・
  利用者承認）。module名`gemini_send`の残名（契約§11が後続整理と明記）。
- 範囲外（「無い」という指摘は不要）：応答の解析・判定抽出、監査の自動化、旧egress設計との統合、
  複数送信・連鎖、実送信E2E（受入条件13。本レビュー合格後に利用者指示で一回だけ実施）、
  製品受入（受入条件14）。
- 機械層で防げない限界として契約§2が受容済み：操縦LLMによる着地後の台帳file削除・改名の隠蔽。
- 事実の明示：対象試験内の`_AWS_KEY`は機微検査試験用の合成値（`"AKIA" + "ABCDEFGHIJKLMNOP"`の連結）で
  あり、実鍵ではない。実鍵の混入という指摘は不要である（合成値の選び方への指摘は妨げない）。

## 5. 運搬と取り込み（Human・Claude向けの手順）

1. Claudeが運搬文面（本record＋契約v5＋実装3 file＋対象試験＋実装成功Evidenceの連結。各部は
   `----- FILE: {path} (sha256={digest}) -----`区切り）を機械生成し、生成物のSHA-256を報告する。
2. 利用者が運搬文面をGemini chatへ貼り付け、返ってきた判定文をClaudeへ貼り戻す。
3. Claudeが判定文を判定record
   `records/development/2026-08-16-external-reviewer-single-send-completion-review-v1.md`へ転記・commitする。
   冒頭にReviewer（Gemini・利用者提供のmodel名）とHuman中継である旨を記載し、判定内容と契約の節参照の
   整合をClaudeが機械照合する。
4. `verified`なら利用者へ実送信E2E（受入条件13）の実施判断を求める。`修正要`なら停止して利用者へ
   最小修正の扱いを諮る。
