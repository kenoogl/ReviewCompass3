# 機械的レビュー計画とRED失敗理由照合 範囲固定 v1

- 日付：2026-08-11
- Human指示：`進めよ`
- 対象：CLI版レビューの最小機械処理
- 外部送信：禁止

## 1. 目的

レビューの対象、担当数、起動回数、終了条件をLLMに決めさせない。既存の開発方針とGit差分から、
プログラムが同じ入力に対して同じレビュー計画を生成する。

また、RED試験では「失敗した」という結果だけでなく、固定した理由で失敗したことを機械照合する。
試験収集、試験準備、環境不全による失敗を、期待したREDとして合格させない。

## 2. 要求

- `MRP-001`：危険度は`low | medium | high`、段階は`scope | completion`だけを受け付ける。
- `MRP-002`：確認項目は`config/development-policy.json`の`risk_verification`から読み、LLM出力を使わない。
- `MRP-003`：`independent_review`がある場合だけ独立レビュー担当を一人、最大一周とする。無い場合はLLM起動0件とする。
- `MRP-004`：blocking根拠は`work-review-protocol.md` §11.1の4類型へ固定し、範囲拡大は許可しない。
- `MRP-005`：対象pathはbase commitとtarget commitのGit差分から決定的に生成し、caller指定pathを受け付けない。
- `MRP-006`：計画は正規JSONとSHA-256を持ち、同じ入力から同じbytesを再生成できる。
- `MRP-007`：CLIは一行JSONだけを返し、成功0、安全停止2、内部失敗1を区別する。
- `RFR-001`：新しいRED照合形式では、収集・準備の`error`を期待REDとして合格させない。
- `RFR-002`：期待REDは失敗理由の固定文字列を持ち、実際の理由に含まれない場合は不合格とする。
- `RFR-003`：旧対応表は読取可能なまま残すが、新しい完了根拠には失敗理由付き形式を要求できる。
- `RFR-004`：今回見逃した親directory、模擬processによるGit巻き込み、保存権限、argv期待誤記を別理由の失敗として拒否できる。

## 3. 変更可能path

- `tools/development/review_plan.py`
- `tools/development/review_plan_cli.py`
- `tools/development/declaration_red_map_check.py`
- `tests/test_review_plan.py`
- `tests/test_declaration_red_reason.py`
- `tests/test_declaration_red_verification.py`
- `tests/test_red_verification_collection_error.py`
- `pyproject.toml`
- `docs/development/prompts/review-plan-run.md`
- `docs/development/prompts/pilot-collaboration-run.md`
- `records/development/2026-08-11-mechanical-review-plan-*`

既存のClaude疎通実装、`tools/egress/`、既存Workflow台帳、他の既存試験は変更しない。

## 4. 作業順序

1. 新規試験と、既存RED照合試験の新しい期待だけを作る。
2. 未実装の計画生成と未対応の失敗理由照合によって失敗することを確認し、試験だけをコミットする。
3. 固定した試験を変更せず実装する。
4. 対象試験、既存開発方針試験、公式全試験を各一度確認する。
5. 今回の疎通実装`d58ac5fdfc31836cc6937218a728410f0a10b8ca`のレビュー計画を生成する。

実レビュー、Claude起動、認証、外部通信、実送信、過去実装の一括再レビューは本範囲に含めない。
