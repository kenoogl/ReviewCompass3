# 無工具Claude疎通 ユーザー指定モデル GREEN Evidence v1

- 日付：2026-08-11
- Human裁定：`2026-08-11-claude-bootstrap-model-selection-human-decision-v1.md`
- RED commit：`3238e03`

## 変更

- 要求モデルを送信目録から読み、Human送信承認と一回限りtokenへ同じ値を要求する。
- 今回の要求モデルを`claude-fable-5`とする。
- 許容実応答モデルを`claude-fable-5`、`claude-opus-5`、`claude-opus-4-8`に限定する。
- payloadごとの実応答モデルを検査し、receiptへ保存する。
- 許容外、空、識別不一致、first-party以外の実応答モデルを成功扱いにしない。

## 単独試験

```text
.venv/bin/pytest -q tests/test_claude_bootstrap.py::test_human_selected_fable_allows_only_approved_response_models tests/test_claude_bootstrap.py::test_response_model_outside_human_approved_set_stops
```

- RED：終了1、5 failed。現実装の`manifest_contract_mismatch`により失敗。
- GREEN：終了0、5 passed。

```text
.venv/bin/pytest -q tests/test_claude_bootstrap.py::test_user_selected_model_is_loaded_from_approved_manifest
```

- 終了0、1 passed。

```text
.venv/bin/pytest -q tests/test_claude_bootstrap.py tests/test_claude_bootstrap_cli.py tests/test_claude_bootstrap_adversarial.py tests/test_claude_bootstrap_entrypoints.py
```

- 終了0、41 passed。

## 外部処理

Claude process、認証確認、外部送信、実model応答確認は行っていない。
