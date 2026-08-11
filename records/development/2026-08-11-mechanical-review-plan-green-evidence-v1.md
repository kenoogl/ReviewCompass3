# 機械的レビュー計画 実装証拠 v1

- 日付：2026-08-11
- 範囲正本：`records/development/2026-08-11-mechanical-review-plan-scope-v1.md`
- RED commit：`988b5f494676783cae19a22aa27466134afac361`
- 外部送信：なし

## 実装結果

- Git差分と`config/development-policy.json`から、レビュー対象、確認項目、担当数、最大周回数を機械生成する。
- 高危険度の完了確認は独立レビュー担当1人、最大1周に固定する。
- RED失敗は、pytestの収集・準備エラーを除外し、宣言した失敗理由との一致を機械照合する。
- LLM起動、Claude起動、認証、外部送信は行わない。

## 単独実行結果

- `python3 -m pytest -q tests/test_review_plan.py`：終了0、6件合格。
- `python3 -m pytest -q tests/test_declaration_red_reason.py`：終了0、5件合格。
- 関連試験（既存RED互換、開発方針、レビュー計画）：終了0、53件合格。
- 処理呼出し目録の対象試験：終了0、1件合格。
- 公式全試験：終了1、1601件合格、1件不合格。

公式全試験の不合格は、作業開始前から再現する
`tests/test_pilot_collaboration_entrypoints.py::test_change_scope_contains_only_v6_allowlisted_paths`だけである。
旧v6の許可一覧が後続の記録を受け付けない既知事象であり、本作業では変更していない。

## 生成した計画

- 対象：`df6364448c2f24c6f931d17893bd0483b4e2eec9`から`d58ac5fdfc31836cc6937218a728410f0a10b8ca`
- 危険度・段階：`high`、`completion`
- 変更path：24件（Git差分から生成）
- 意味レビュー：独立レビュー担当1人、最大1周
- 計画SHA-256：`268a1b1fb625dadf476d7c7370799a12520a0c51b4d7931adc5bae5597a9161d`
- 保存先：`records/development/2026-08-11-mechanical-review-plan-claude-bootstrap-v1.json`

## 未実施

実レビュー、Claude Code CLI起動、認証、通信、実送信、過去実装の一括再レビューは行っていない。
