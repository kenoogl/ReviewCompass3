# 外部レビュア一回送信 実装成功Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008 / v5`（採用済み）
- 採用判断：v4採用`records/development/2026-08-16-external-reviewer-single-send-adoption-decision-v1.md`、
  v5軽微訂正の直接承認`records/development/2026-08-16-external-reviewer-single-send-v5-adoption-decision-v1.md`
  （commit `7baf82c`）
- 実装担当：Claude
- 方式：テスト駆動（失敗試験の固定→最小実装→契約内矛盾の発見と停止→v5訂正承認→再配置→全緑）

## 1. 失敗試験の固定（RED）

【記録】対象試験`tests/test_gemini_send.py`をcommit `6f3e528`（試験1 fileのみ）へ固定した。実装未存在の
段階でRED 48件失敗を確認した（前sessionの実測。TODO_NEXT_SESSION.md 2026-08-16版の現在位置欄）。

## 2. 契約内矛盾の発見と訂正（v4→v5）

【記録】v4 §11の置き場所`tools/egress/`と、§12.11が成功を要求する既存敵対試験
`tests/test_egress_adversarial.py`の不変条件「`tools/egress/`配下に通信手段なし」が両立せず、実装fileの
存在時だけ敵対1件が不合格になることを実測して停止した。置き場所だけを新package`tools/external_review/`へ
変える契約候補v5を作成し、利用者が軽微訂正として直接承認した（安全境界・schema・検査・台帳の定義は不変）。

## 3. 最小実装（GREEN・v5の置き場所）

【実測】契約v5 §11の変更上限内の5 fileだけを変更・新設した。

1. 送信核`tools/external_review/gemini_send.py`（新規。検査→payload機械構成→試行record→一回送信→
   応答保存→結果record）
2. 入口`tools/external_review/gemini_send_entry.py`（新規。`send --order <絶対path>`だけ）
3. package宣言`tools/external_review/__init__.py`（新規）
4. `pyproject.toml`へ実行名`reviewcompass3-gemini-send = "tools.external_review.gemini_send_entry:main"`一件
5. 対象試験`tests/test_gemini_send.py`のimport先・実行名期待値をv5の置き場所へ更新（opener試験の実態合わせ
   を含む。通信は全模擬）

既存egress 7 moduleは変更していない（§4で差分0を機械確認）。

## 4. 機械確認（各単独command・終了コード個別判定）

【実測】

- 対象試験：49件成功、終了コード0
- egress関連：107件成功、終了コード0（敵対試験の不変条件「`tools/egress/`配下に通信手段なし」の回復を確認）
- G02対象158件・G08対象107件・G24対象111件・実行器75件・G30基盤e2e 38件：各単独成功、終了コード0
- 保護path（基準commit `aac1f90`からの差分：egress 7 module・redaction.py・task_contract 5 file・
  受入済み4製品とその試験）：差分0、終了コード0
- 正規全試験（既存の禁止認証隔離条件：`FORBIDDEN_AUTH_ENVIRONMENT`6変数を環境から外す）：2,362件成功、
  終了コード0（前回2,313件＋対象49件）
- 通常host環境では実行器の安全拒否12件（`api_key_environment_forbidden`）が失敗する既知事象で、退行なし
- `git diff --check`：終了コード0

## 5. 配布後実行名の判定系列E2E（受入条件10相当・送信なし）

【実測】`pip install -e .`で配置した正式実行名`reviewcompass3-gemini-send`を、repository内とrepository外
（scratchpad）の2つの現在位置から、鍵なし環境（`GEMINI_API_KEY`・`OPENAI_API_KEY`・`ANTHROPIC_API_KEY`を
外す）で同一の合成送信指示（`ORD-G20-E2E-DRY-001`、由来file `pyproject.toml`）に対して実行した。

- 両方とも終了コード2、標準エラー0 bytes、標準出力bytes完全一致（`cmp`）
- 判定：`{"external_send_approved":false,"reason":"invalid_output_root","source":"ledger","status":"stopped"}`
  ——台帳root`.reviewcompass/egress-ledger/`不存在による契約§7.3・§10.3どおりの送信前停止（通信なし）

## 6. 未実施

- 独立完了レビュー（受入条件12。暫定体制：Gemini・Human中継、5段手続きの下ごしらえつき）
- 実送信E2E一回（受入条件13。利用者指示による。前提として台帳rootの初回commit用意が必要）
- 製品受入（受入条件14）
- 応答解析・監査自動化・旧設計統合（後続契約）
