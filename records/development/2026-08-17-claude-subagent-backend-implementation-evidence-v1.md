# 契約012 claude-subagent backend 実装Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 契約：`TC-RC3-PRODUCT-CLAUDE-SUBAGENT-BACKEND-012 / v2`（採用済み。採用record
  `records/development/2026-08-17-claude-subagent-backend-contract-adoption-decision-v1.md`）
- 範囲：契約§9-1〜7相当（RED・実装・導線追記）。**subagent許可modelの承認・§9-8実E2E・§9-10完了
  レビュー・§9-11製品受入は未実施**

## 1. 実施（RED→実装→緑）【実測】

1. RED：`tests/test_reviewer_launch.py`へ新設16試験を先に固定し、実装前実行で**16失敗・既存35合格**を
   機械確認（既存caseの無変更維持＝agy値の不変移設の基準）。
2. 最小実装：`tools/reviewer_launch/core.py`（backend別定義・claude-subagent追加・tier受容・claude
   stream解析・和集合互換）と`entry.py`（`--accept-tier`・`--acceptance-ref`・g30 prepareの
   `--backend`任意引数）。
3. 緑：対象51件（既存35無変更＋新設16）、互換120件（契約011の32件無変更を含む）、正規全試験
   **2,458件**成功・各単独終了コード0。
4. 試験の訂正1件（理由の記録）：subagent系試験がhost環境のANTHROPIC系環境変数で
   `api_key_environment_forbidden`となったため、試験側でanthropic 6種を除去する形へ修正した。
   **認証遮断が実環境で実効であることの副次実証**であり、検査意図は不変。

## 2. 実装した中心仕様（契約§5.1・§7の写像）

- **backend別定義**：`BACKENDS`へ宣言tier・読取り道具名を追加。agyは`provider google／executable agy／
  declared_tier 1／read_tool_name view_file`で**値は不変移設**。claude-subagentは
  `anthropic／claude／3／Read`。
- **tier受容（§7.3）**：`_resolve_tier`＝provider相違でTier 1、同一providerは`accept_tier`が宣言tierと
  一致する場合だけ許可、欠落・不一致は従来どおり`reviewer_not_independent_tier`。Tier≠1では
  `acceptance_ref`（repo相対path）の実在を起動前に機械確認（不在は`acceptance_reference_missing`）。
  宣言tier・受容入力・受容根拠は起動recordへ記載。既存`judge_tier`は無変更（既存試験が直接使用）。
- **claude起動固定形（§7.2）**：`build_claude_arguments`＝`--print`・`stream-json`・
  `--tools Read,Glob,Grep`（Edit/Write無し）・`--allowedTools Read(/**)`・`--disallowedTools`
  （実行器`DISALLOWED_TOOLS`の読取り流用）・`--permission-mode dontAsk`・`--strict-mcp-config`空・
  `--disable-slash-commands`・`--no-chrome`・`--model`・prompt末尾。認証遮断は
  `CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT`6種（自前定数。**実行器定数との同値を試験で固定**）。
- **prompt共通雛形＋道具名差し込み（SR-C12-1）**：`build_prompt`へ`read_tool_name`引数（既定
  `view_file`＝agy不変）。claude起動時は`Read`を差し込む。
- **claude stream解析**：model照合（top levelとmessage内）・result本文からのJSON抽出
  （直接／```json fence／括弧範囲の順）・schema検証は既存`validate_verdict`共用。
- **和集合互換（§5.1-4）**：`ALLOWED_RESPONSE_MODELS`＝agy承認済み一覧＋subagent一覧（現在空）の
  和集合として名称・値を維持（`("gemini-3.1-pro-high",)`のまま）。`SUBAGENT_ALLOWED_RESPONSE_MODELS`は
  空定数で、**空の間はsubagent起動が`allowed_models_unfixed`で停止**（利用者承認recordで確定後に固定）。

## 3. 保護基準の確認【実測】

基準commit `6ba5519`（契約012候補v2の固定commit）からの差分：

- 保護対象（request_builder・bootstrap・redaction・digests・実行器4 file・send.py・egress・
  operation_contract_run.py・test_request_builder.py）：**差分0**。
- 許可された変更（§8上限内）：`tools/reviewer_launch/`（core・entry）・`tests/test_reviewer_launch.py`・
  `docs/development/prompts/reviewer-launch-run.md`のみ。

## 4. 成果物一覧

| 種別 | path | commit |
| --- | --- | --- |
| 採用判断record | `records/development/2026-08-17-claude-subagent-backend-contract-adoption-decision-v1.md` | `bac60b0` |
| 実装＋対象試験 | `tools/reviewer_launch/`（core・entry）・`tests/test_reviewer_launch.py`（51件） | `8809993` |
| 導線追記 | `docs/development/prompts/reviewer-launch-run.md` | `aa2cf0c` |

## 5. 未実施（契約の残り）

- subagent許可model一覧の利用者承認と定数固定（§5.1-5。空の間は起動が安全側で停止）。
- §9-8：実E2E 1回（`--accept-tier 3`＋受容根拠の明示。同一対象集合の別名依頼・2 oracle比較）。
- §9-10：完了レビュー（agy・Tier 1。依頼は契約011の正式経路で組み立て）。
- §9-11：製品受入（§7.4残余risk 4点の最終受容）。
- TODO更新（本Evidence直後に共通手順で実施）。
