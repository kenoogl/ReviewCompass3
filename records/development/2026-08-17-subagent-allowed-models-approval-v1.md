# 契約012 subagent許可model一覧の利用者承認record v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：契約012 §5.1-5「空の直書き定数で開始し、実E2E前に利用者承認recordで値を確定して
  固定する（契約010と同型）」の履行

## 1. 承認文言【記録】

> 案1（claude-opus-5）を承認する。実測→承認record→定数固定→回帰試験まで進めて

（2026-08-17 chat。Claudeが提示した候補3案——案1 `claude-opus-5`・案2 `claude-sonnet-5`・
案3 `claude-fable-5`——のうち、推奨案1「`claude-opus-5`の1値のみ」の全文承認）

## 2. 根拠となった機械出力【記録：Claude実測】

実測は計測専用script（scratchpad一時領域。製品コードは無変更）で行い、引数は契約012 §7.2の
固定引数組み立て`build_claude_arguments("claude", <最小prompt>, "claude-opus-5")`、子環境は
`_child_environment(CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT)`をそのまま用いた。claude CLIは2.1.220。
以下のJSONはscriptの出力の機械転記である。

### 2.1 第1回（契約固定引数どおり・子環境も契約どおり）：起動不成立

```json
{
  "requested_model": "claude-opus-5",
  "exit_code": 1,
  "models_observed": [],
  "event_count": 0,
  "environment_keys": [
    "HOME",
    "LC_CTYPE",
    "PATH"
  ],
  "stderr_tail": "Error: When using --print, --output-format=stream-json requires --verbose\n"
}
```

### 2.2 第2回（`--verbose`をstream-json直後へ補い・子環境は契約どおり）：認証失敗・init表記を取得

```json
{
  "requested_model": "claude-opus-5",
  "argument_deviation": "--verbose inserted after stream-json",
  "exit_code": 1,
  "models_observed": [
    "<synthetic>",
    "claude-opus-5"
  ],
  "event_count": 3,
  "environment_keys": [
    "HOME",
    "LC_CTYPE",
    "PATH"
  ],
  "stderr_tail": ""
}
```

（`<synthetic>`はCLIがエラー通知用に合成したassistantメッセージの表記。応答本文は
「Not logged in · Please run /login」・`error: "authentication_failed"`）

### 2.3 第3回（`--verbose`補い・環境を剥がさない診断起動）：成功・応答表記を取得

```json
{
  "requested_model": "claude-opus-5",
  "deviations": [
    "--verbose inserted after stream-json",
    "environment not stripped (diagnostic)"
  ],
  "exit_code": 0,
  "models_observed": [
    "claude-opus-5"
  ],
  "event_count": 5,
  "stderr_tail": ""
}
```

成功runのstream該当2行（機械転記）：

```json
{"type":"system","subtype":"init","cwd":"/Users/Daily/Development/ReviewCompass3","session_id":"641b2b78-cf9c-4a3b-b2e9-3536b587d277","tools":["Glob","Grep","Read"],"mcp_servers":[],"model":"claude-opus-5","permissionMode":"dontAsk","slash_commands":[],"apiKeySource":"none","claude_code_version":"2.1.220","output_style":"default","agents":["claude","claude-code-guide","Explore","general-purpose","Plan","statusline-setup"],"skills":[],"plugins":[],"capabilities":["interrupt_receipt_v1","interrupt_cancel_queued_v1","msg_lifecycle_v1"],"analytics_disabled":false,"product_feedback_disabled":false,"uuid":"d5094fc3-c4df-4546-adf6-f73ef141766d","memory_paths":{"auto":"/Users/keno/.claude/projects/-Users-Daily-Development-ReviewCompass3/memory/"},"fast_mode_state":"off","fast_mode_disabled_reason":"sdk_opt_in_required"}
```

```json
{"type":"assistant","message":{"model":"claude-opus-5","id":"msg_011Ce7PjH5HjVaJVZ7bFEyhM","type":"message","role":"assistant","content":[{"type":"text","text":"OK"}],"stop_reason":null,"stop_sequence":null,"stop_details":null,"usage":{"input_tokens":2,"cache_creation_input_tokens":5050,"cache_read_input_tokens":2800,"cache_creation":{"ephemeral_5m_input_tokens":0,"ephemeral_1h_input_tokens":5050},"output_tokens":1,"service_tier":"standard","inference_geo":"not_available"},"diagnostics":null,"context_management":null},"parent_tool_use_id":null,"session_id":"641b2b78-cf9c-4a3b-b2e9-3536b587d277","uuid":"fe070c96-01ff-4eff-a43c-49bd07fe9cd2","timestamp":"2026-08-17T00:42:36.417Z","request_id":"req_011Ce7PjGADuGYmbiyYU98wo"}
```

（result行は`"is_error":false`・`"terminal_reason":"completed"`。第3回の逸脱2点は計測・診断のためで、
製品コードと本番起動条件には適用しない）

## 3. 確定事項

1. `tools/reviewer_launch/core.py`の契約固定定数を
   `SUBAGENT_ALLOWED_RESPONSE_MODELS = ("claude-opus-5",)`へ固定する（1件のみ・最も厳格な一覧）。
2. 和集合`ALLOWED_RESPONSE_MODELS`は`("gemini-3.1-pro-high", "claude-opus-5")`となる（agy値が
   先頭のまま。契約011対象試験は先頭要素と所属検査だけを使うため無変更で緑を維持——契約012 §9-7）。
3. 以後の一覧変更は契約改定として扱う（契約012 §5.1-5）。
4. 選定理由：操縦役（claude-fable-5）と別modelであり、残余risk「Tier 3は同一model系で見落としの
   相関が残り得る」（契約012 §7.4-1）への実効的な緩和になる。レビュー品質も上位model。
5. 表記の確定：initイベントと認証成功時のassistant応答の両方が`claude-opus-5`の同一表記（§2.2・
   §2.3）。契約010が残した「stream内model表記がCLI識別子か表示名か不明」に相当する不確実性は、
   本契約では実測で解消済み。日付つき別表記は観測されていない。

## 4. 実測で判明した付随事実【記録のみ・処置は別途Human判断】

1. **`--verbose`の列挙漏れ**：契約012 §7.2の固定引数列挙に`--verbose`が無く、claude CLI 2.1.220は
   `--print`＋`--output-format=stream-json`で`--verbose`を必須とするため、契約どおりでは起動不成立
   （§2.1）。設計流用元の実行器`tools/development/claude_implementation_executor.py`の引数列には
   `--verbose`が存在する（stream-json直後）。§10停止条件「claude CLIのheadless起動が読み取り専用の
   固定引数で成立しない」に該当し得るため、§7.2への`--verbose`追加は契約訂正としてHuman判断へ諮る。
   本record時点で製品コード（`build_claude_arguments`）は変更していない。
2. **操縦環境の認証**：操縦環境（Claude CodeのBash）では、契約の子環境（通過7変数のみ）でclaude CLIが
   未login扱いとなる（§2.2）。環境を剥がさない診断起動は成功する（§2.3）ため、本文脈の認証は
   環境変数由来と判別される。永続login状態（keychain・認証file）の有無はこの文脈からの点検が権限
   分類器で遮断され未確認。§9-8実E2Eの起動文脈（永続loginの有無・起動場所）は実E2E指示の前に
   利用者と確認する。

## 5. 未実施

- §7.2固定引数の契約訂正（`--verbose`。判断待ち）、実E2E（利用者の明示指示待ち）、§9-10完了レビュー、
  §9-11製品受入。
