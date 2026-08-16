# 外部レビュア一回送信 契約v5軽微訂正の直接承認・実装再開 利用者判断 v1

- 判断日：2026-08-16
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：契約訂正版の採用（軽微訂正としての直接承認）、実装再開の承認
- 契約：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5`

## 1. 承認文言

利用者は次の二択の提示（推奨(A)併記）を受け、chatで「軽微訂正として直接承認し、実装を再開する」と応えた。

提示の要旨：契約候補v5は置き場所だけの訂正である（§11の`tools/egress/`を新package
`tools/external_review/`へ変更。安全境界・schema・検査・台帳の定義は不変）。選択肢は
(A)軽微訂正として直接承認し実装を再開する、(B)Gemini限定再確認へ運搬してから採用判断する。
推奨(A)の理由：変更は置き場所の1点だけであり、v4はGemini限定再確認で`開始可`判定を得ており、
矛盾の解消方向は既存敵対試験（`tools/egress/`配下に通信手段なしの不変条件）を守る側である。

## 2. 承認が固定するもの

1. 契約v5の採用（Gemini限定再確認を経ない軽微訂正としての直接承認）
   - path：`records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v5.md`
   - SHA-256：`6fc7b37b07f65519e78353df23fc7277c1c9265956320e46d5e6e35608e9d165`
2. 実装の再開：stash`g20-v5-impl`（実装途中file 4件）を復元し、送信核・入口を
   `tools/external_review/`へ再配置（`__init__.py`追加・試験のimport先と実行名の更新）して
   対象試験49件を全緑にし、退行確認（egress敵対試験の回復を含む）の後にGREEN commitを行う。
3. v4採用判断（縮小境界の採用、送信ごとの人の確認なし、実装開始の承認：
   `records/development/2026-08-16-external-reviewer-single-send-adoption-decision-v1.md`）は、
   v5でも置き場所以外の内容が不変のため、継続して有効である。

## 3. 判断の前提Evidence

- 訂正根拠（契約内矛盾の発見）：契約v4 §11の置き場所`tools/egress/`と、§12.11が成功を要求する
  既存敵対試験`tests/test_egress_adversarial.py`の不変条件「`tools/egress/`配下に通信手段なし」の
  両立不能。実装fileが存在する間だけ敵対1件が不合格になることを実測済み（TODO_NEXT_SESSION.md
  2026-08-16版のGit・Test欄）。
- v4限定再確認（判定`開始可`、Gemini・Human中継）：
  `records/development/2026-08-16-external-reviewer-single-send-v4-limited-rereview-v1.md`、
  SHA-256 `75d483ca65c27ac6ece1363f4a708153912447f58254c997ad760aa06b90bc84`

## 4. 本承認に含まれないもの

- 独立完了レビュー（受入条件12）の省略。GREEN commit後に暫定体制（Gemini・Human中継、
  5段手続きの下ごしらえつき）で実施する。
- 実送信E2E（受入条件13）の実施指示。都度の利用者指示による。
- 実装完了の受入（受入条件14）。独立完了レビュー合格後に一判断として提示する。
