# 契約010 Reviewer起動アダプタ 実装Evidence v1

- 記録日：2026-08-16
- 記録者：Claude
- 契約：`TC-RC3-PRODUCT-REVIEWER-LAUNCH-ADAPTER-010 / v2`（採用済み。採用record
  `records/development/2026-08-16-reviewer-launch-adapter-contract-adoption-decision-v1.md`）
- 範囲：契約§9-1〜7（RED・実装・導線配備）。**§9-8実E2E・§9-10独立完了レビュー・§9-11製品受入は未実施**

## 1. 実施（RED→実装→緑）【実測】

1. RED：`tests/test_reviewer_launch.py`（31試験）を先に固定し、module不在の状態で実行。
   結果：`31 failed`（期待どおりの失敗）。
2. 最小実装：`tools/reviewer_launch/`（`__init__.py`・`core.py`・`record.py`・`entry.py`）と
   `_OPERATIONS`への`reviewer_launch_prepare`登録（`tools/operations/operation_contract_run.py`へ
   import 1行＋entry 9行）。
3. 緑：各単独実行の終了コード0で確認。
   - 対象試験：`tests/test_reviewer_launch.py` → `31 passed`
   - G30：`tests/test_operation_contract_run.py` → `75 passed`
   - layout：`tests/test_layout_baseline.py` → `13 passed`
4. 試験の訂正1件（理由の記録）：entry出力バッファの型をStringIOからBytesIOへ訂正。G30の
   `_run_part`は`io.BytesIO`を渡し、既存entry（`one_design_acceptance_entry`）も
   `canonical_json_bytes + b"\n"`を書く実装規約であることが実装点検で判明したため。要求の誤解の
   訂正であり、検査の意図（JSON一行・終了コード）は不変。

## 2. 実装した安全境界（契約§7の写像）

- 認証遮断：`GEMINI_API_KEY`・`GOOGLE_API_KEY`・`GOOGLE_GENAI_API_KEY`・
  `GOOGLE_APPLICATION_CREDENTIALS`の検出で起動前停止（`api_key_environment_forbidden`）。
- 固定引数：`--print --output-format stream-json --json-schema <契約schema> --model <許可model>
  --disable-slash-commands --print-timeout 600s`。`--dangerously-skip-permissions`・`--mode`は
  組み立てに存在しない（試験で不在を固定）。
- 許可model一覧：直書き定数`ALLOWED_RESPONSE_MODELS = ()`。**空の間は`allowed_models_unfixed`で
  起動前停止**（実E2E前に利用者承認recordで確定してから値を固定する）。
- byte上限：起動prompt 16,384 byte超で起動前停止。固定形式promptの実測は877 byte（下記§4）。
- 鮮度：起動直前の再計算照合（`request_record_stale`）と事後照合の再計算（二重再計算）。
- 保存：`store_raw_executions`再利用（route=`independent`単独）＋`launch.json`を
  `store_immutable_json`で不変保存。repo内私有root指定は`private_root_inside_repository`で停止。
- 転記：schema適合JSONだけを判定recordへ機械転記し、そのrecord 1件だけを単独commit。冒頭へ
  Reviewer（provider・model）・Tier（アダプタ判定値）・起動方式・未加工出力の保存先種別と
  SHA-256を記載。
- 事後照合4点：鮮度・単独commit（対象commitより後・ancestor検証）・根拠（raw digest・findings根拠
  pathの実在）・形式（schema再検証）。

## 3. 導線配備（§9-7）【実測】

- `pyproject.toml`へ`reviewcompass3-reviewer-launch = "tools.reviewer_launch.entry:main"`を登録し、
  `pip install -e`で有効化。
- 別の現在位置（session scratchpad）から`check`（起動なしの事前検査）を実行し、終了コード0・
  依頼record実digest一致・`tier: 1`・`prompt_bytes: 877`を確認：

```text
{"backend":"antigravity-cli","operation":"reviewer_launch_prepare","prompt_bytes":877,"request":{"path":"records/session-handoffs/2026-08-16-reviewer-launch-adapter-v2-review-gemini-request-v1.md","sha256":"390bc32868a2ee99f11e68d6bb9489826681674786d64b93ea207592399ac995"},"status":"ok","tier":1}
```

- G30操作`reviewer_launch_prepare`を登録（起動なしの事前検査のみ。外部起動は単体入口`launch`だけ）。
- run入口文書`docs/development/prompts/reviewer-launch-run.md`と`AGENTS.md` §1の入口1行を追加。

## 4. 保護基準の確認【実測】

基準commit `41a705b`（契約候補v2の固定commit）からの差分：

- 保護対象（raw_review_store・review_execution・実行器4 file・send.py・egress・session_logs・
  reviews・design・requirements・受入済み製品試験）：**差分0**。
- 許可された変更：`tools/operations/operation_contract_run.py`のみ（+9行。import 1行と登録entry）。

## 5. 全試験と手戻り記録【実測】

禁止認証隔離条件（実行器の禁止環境変数6種を除いた環境）の正規全試験で、新規31件を含め
`3 failed, 2403 passed`となった。失敗3件は同一原因：

- 事象：`TODO_NEXT_SESSION.md`の参照digest検証（`todo_handoff`・`todo_update_path`・
  `issue_resolution_post_write`）が、統合検討recordのagy訂正（利用者承認・commit `7beb7d8`）による
  digest変化で`reference_digest_mismatch`を報告。
- 対象操作：統合検討record訂正時のTODO整合確認。期待executor：TODO共通手順
  （`todo_handoff`単一入口）の機械検証。実executor：Claudeの判断で「handoff時に更新」と先送りし、
  layout試験だけで通過させた。
- 原因：TODOの参照digestが試験で常時機械検証されている事実の見落とし（手順の選択誤り）。
- 対処：本Evidence直後に共通手順（`docs/development/prompts/todo-handoff-update.md`）でTODOを
  現在値へ更新し、`todo_handoff`検証と全試験再実行で緑を確認する。
- 機械化候補：record訂正をTODOのEvidence節が参照している場合に`todo_handoff`検証を同一作業単位の
  必須検証へ含める（改善候補として保留列へ。既存経路で登録する）。

## 6. 成果物一覧

| 種別 | path | commit |
| --- | --- | --- |
| 実装 | `tools/reviewer_launch/`（`__init__.py`・`core.py`・`record.py`・`entry.py`） | `ef24299` |
| 対象試験 | `tests/test_reviewer_launch.py`（31件） | `ef24299` |
| G30登録 | `tools/operations/operation_contract_run.py`（+9行） | `ef24299` |
| 導線 | `pyproject.toml`・`docs/development/prompts/reviewer-launch-run.md`・`AGENTS.md` §1 | `3b871aa` |

## 7. 未実施（契約の残り）

- §9-8：実E2E 1回（利用者の明示指示待ち。前提：許可model一覧の利用者承認と定数への固定）。
- §9-10：独立完了レビュー（暫定体制）。
- §9-11：製品受入（§2承認境界と§7.4残余riskの最終受容）。
- TODO更新（本Evidence直後に共通手順で実施）。
