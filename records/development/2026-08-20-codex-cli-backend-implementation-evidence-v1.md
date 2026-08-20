# 契約015 実装Evidence（RED先行→最小実装→GREEN） v1

- 実施日：2026-08-20
- 担当：Claude
- 契約：`TC-RC3-PRODUCT-CODEX-CLI-BACKEND-015` v2＋訂正record
  `DEC-CODEX-MODEL-OBSERVATION-CORRECTION-2026-08-20-V1`
- 実測の正本：測定ブロック
  `records/development/2026-08-20-contract-015-green-measurements-v1.md`（宣言
  `records/development/2026-08-20-contract-015-green-commands-v1.json`。11項目・二重実行一致・
  非決定0件）。本文の数値は同fileを参照し転記しない（例外は§1のRED確認のみ）

## 1. RED先行の確認【実測・例外転記】

失敗試験を先に固定した（新規21本＋和集合pin更新）。実装前の実行結果（例外転記の理由：実装後は
再現不能のため。揺れは実行時間のみ）：

- 再現コマンド：`.venv/bin/python3 -m pytest tests/test_reviewer_launch.py -q --tb=no`
- 末尾出力：`21 failed, 70 passed in 3.88s`
- 内訳の読み：新規21本のうち20本が失敗＋和集合pin更新1本が失敗（期待どおりの赤）。既存69本と、
  設計上改修前でも通るgolden試験（生成promptのbyte基準pin）1本が合格。

## 2. 途中の是正2件（試験側。製品コードの手戻りではない）

1. 契約010期の和集合pin試験がもう1本あり（`test_allowed_models_fixed_to_approved_value`）、
   4値へ更新した（契約015 §5.1-5・承認record 2026-08-20の帰結。agy先頭値の不変assertを追加）。
2. codex禁止環境変数試験が、起動helperの事前delenvで検査対象の変数まで消していたため、
   直接組み立てへ書き直した（検出：GREEN確認1回目の失敗2件）。

## 3. GREEN【実測＝測定ブロック参照】

- 対象・関連4 suiteの収集件数と単独終了コード射影：reviewer_launch／request_builder（契約011
  対象）／G30契約操作／RQ2装置——いずれも終了コード射影`exit=0`（各節参照）。
- **name分岐の消滅**：起動核の`backend_name == `固定点は0（§9-3の機械確認）。
- **生成promptのbyte不変**：改修後のgolden digest再計算が改修前の機械取得値（試験内のpin値）と
  一致（view_file・Readの2種とも。§9-2のbyte不変golden成立）。
- 変更成果物4 fileのdigestは測定ブロック末尾節で固定。

## 4. 実装内容（変更上限内・4 file）

1. `tools/reviewer_launch/core.py`：backend登録簿の深化（読取り指示ブロック・引数組み立て関数・
   stream解析関数・許可model（callable＝起動時にmodule定数を読む）・禁止／通過環境・注入・
   project束縛要否を登録）、name分岐6箇所の登録参照化、codex-cli追加（openai・Tier 1・
   固定引数＝訂正record確定列）、openai遮断4種、rollout観測（`_codex_observed_models`）、
   agent_message抽出（`_codex_extract_verdict`）、stdin遮断（全backend共通）、prompt骨格の
   分割（現行値の逐語移設）。
2. `tools/reviewer_launch/entry.py`：g30 prepareのprompt組み立てを登録簿経由へ（1呼び出し）。
3. `tests/test_reviewer_launch.py`：契約015節の追加21本＋和集合pin 2本の4値化更新。
4. `docs/development/prompts/reviewer-launch-run.md`：codex-cli起動の使い方を追記。

## 5. 契約受入条件との対応

- §9-1 RED先行＝§1で確認。§9-2 agy・claude互換＝既存69本無変更全緑＋byte不変golden一致。
  §9-3 分岐消滅＝固定点0。§9-4 危険旗不在両向き・§9-5 遮断・§9-6 合成stream両向き＝新規試験で
  固定し全緑。§9-7 和集合4値（先頭＝agy値不変）＋契約011対象42件無変更全緑。
- 【判断】和集合pin試験2本のliteral更新は、契約015 §5.1-5（利用者承認済みの4値化）が明示的に
  変える値のpinであり、§9-2「既存試験caseの無変更」の対象（agy・claude経路の挙動試験）にも
  §10停止条件「互換が保てない」（互換＝先頭要素と所属検査の意味維持）にも該当しないと整理した。
  懸念があれば完了レビュー（agy）のfindingsで検出される位置に置く。

## 6. 未実施

- §9-8 実E2E（codex起動＝利用者の明示指示待ち）。§9-9 正規全試験（禁止認証隔離条件）は受入段で
  実行。§9-10 完了レビュー（agy）。§9-11 残余risk 6点の確認と製品受入。
