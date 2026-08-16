# 外部レビュア一回送信 製品受入 利用者判断 v1

- 判断日：2026-08-16
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：製品処理の受入（契約v5受入条件14）
- 契約：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5`

## 1. 承認文言

利用者は、限界2点の明示を含む受入提示を受け、chatで「限界を了解のうえ、製品処理を受け入れる」と応えた。

## 2. 受入が固定するもの

1. **正式の外部送信路の成立**：利用者の指示の下で、commit済みfile由来のレビュー依頼payloadを
   3 provider（Gemini・OpenAI・Anthropic）切り替え式に、機械的な守り（機微検査・path allowlist・
   digest束縛・`.git`実在検査・送信前試行record・累計100件上限・重複ID停止・鍵の非表示・
   リダイレクト／proxy／TLS無効化の3禁止）つきで一回送信し、未加工応答と台帳をrepository履歴へ残す
   経路（`tools/external_review/`・実行名`reviewcompass3-gemini-send`）。
2. **了解された限界**：
   - G20全体ではない最初の送信縦切りである。応答の解析・監査の自動化・旧egress設計との統合・複数送信は
     後続契約に残り、本受入だけでは候補5（G20）を完了にしない。
   - 機微検査の現水準では、長いhyphen連結名・digest記載を含む実用文書が高乱雑性誤検知で送信不能である
     （実測で確定した構造問題）。実用のレビュー依頼運搬には検査精密化の後続契約が必要であり、改善候補
     `IC-EGRESS-SENSITIVE-SCAN-FALSE-POSITIVE-001`として登録済み（Human仕分け待ち）。
   - 操縦LLMによる着地後の台帳file削除・改名の隠蔽は機械層で防げない（契約§2の受容済み限界）。

## 3. 判断の前提Evidence（一連の鎖）

| 段階 | record |
| --- | --- |
| 契約v5採用（軽微訂正の直接承認） | `records/development/2026-08-16-external-reviewer-single-send-v5-adoption-decision-v1.md` |
| 実装成功（GREEN・退行確認・判定系列E2E） | `records/development/2026-08-16-external-reviewer-single-send-green-evidence-v1.md` |
| 独立完了レビュー（修正要・blocking 2/non-blocking 1） | `records/development/2026-08-16-external-reviewer-single-send-completion-review-v1.md` |
| 指摘3件の訂正 | `records/development/2026-08-16-external-reviewer-single-send-correction-evidence-v1.md` |
| 限定再確認（verified） | `records/development/2026-08-16-external-reviewer-single-send-correction-rereview-v1.md` |
| 実送信E2E（初回承認済み外部送信・受入条件13） | `records/development/2026-08-16-external-reviewer-single-send-live-e2e-evidence-v1.md` |

## 4. 本受入に含まれないもの

- 候補5（G20）全体の完了判断。
- 応答解析（G02 organize接続）、抜き取り監査の自動化、旧設計統合、複数送信の一括（後続契約）。
- 機微検査精密化の実施（改善候補の仕分けと後続契約のHuman判断による）。
- 開発レビューの運搬をHuman中継から本経路へ移す運用判断（機微検査精密化の後に改めて判断する）。
