# 測定ブロック：契約016（モデル選択＋照合＋登録定型化）事前走査の実測

- captured_at：2026-08-20T20:39:14+09:00
- 実行環境：macOS-26.5.1-arm64-arm-64bit-Mach-O
- 宣言file：`records/development/2026-08-20-model-selection-correspondence-prescan-commands-v1.json`（SHA-256 `3f0c86cb4006c95f29a4bf04eb5fe7fa789ba10554562dadb3dd342a57ec63d2`）
- 生成tool：`tools/development/measurement_block.py`（機械生成file。手編集禁止。各entryは二重実行の一致検査つき）

## 契約候補が参照するfileのdigest固定

- argv：`["shasum", "-a", "256", "tools/request_builder/core.py", "tools/request_builder/entry.py", "tools/reviewer_launch/core.py", "tools/reviewer_launch/entry.py", "tests/test_request_builder.py", "tests/test_reviewer_launch.py", "docs/development/prompts/request-builder-run.md", "docs/development/prompts/reviewer-launch-run.md", "records/development/2026-08-20-codex-cli-backend-product-acceptance-decision-v1.md", "records/development/2026-08-20-codex-allowed-models-approval-v1.md", "records/development/2026-08-17-request-builder-union-model-check-observation-v1.json", "records/development/2026-08-17-improvement-candidates-triage-decision-v1.md", "records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md", "records/development/2026-08-20-model-selection-correspondence-reuse-search-plan-v1.json", "records/development/2026-08-20-model-selection-correspondence-reuse-search-attestation-v1.json"]`
- 実行体：/usr/bin/shasum
- exit：0・elapsed：0.016s
- 完全性：二重実行一致

- stdout：

```text
e61215eddc0e7f50468c87a9b17c2cba6825fd2470a80d0bac3eca72c0e3907d  tools/request_builder/core.py
2873e17b5e94ab1fb7f353b747a5098f1b29174a457dfc23f531034344ea0d1c  tools/request_builder/entry.py
88d3dab9bebafc87a7a3757c8216710f7517cffe4b6101fca6d4cb08b1ab2684  tools/reviewer_launch/core.py
946e5fc4291ee9cb8f6ae179a11017d87e7b95da5848f5e1a436b13b276f6f9d  tools/reviewer_launch/entry.py
c40e954147f8ec77dcb299da10fb2a26678aeb6e2ce9ccfb19019db92fb89f81  tests/test_request_builder.py
c7c5364ab72f5097557a00f086fdcc0cc5c555bb93bc1cfb5186645af8a04330  tests/test_reviewer_launch.py
6b2f3493ffec7cd7674dfbaf79fa8ad3f893a81c0675ef4896117867117b474f  docs/development/prompts/request-builder-run.md
8cf52d9f7dc0d9f70d93b34035deeaad65a72ebe58372be037d906133ec65cd0  docs/development/prompts/reviewer-launch-run.md
482e2dbae54c6a576f5a692b9c3e5c171a38778128cf6f9c182c9e014a1695d6  records/development/2026-08-20-codex-cli-backend-product-acceptance-decision-v1.md
f0f0536ccda07d942e06c1d96fa75c2781387763f63afd0439a5d9c9f7d67c99  records/development/2026-08-20-codex-allowed-models-approval-v1.md
ea3cdc0d048d9604272c7c918287856e8ec3a6013856b5cde66410b262432517  records/development/2026-08-17-request-builder-union-model-check-observation-v1.json
34f7ca163645fe50770734f92b48ad41b6415983ab1eda61c57efc104be8a162  records/development/2026-08-17-improvement-candidates-triage-decision-v1.md
ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
90ae5d5c77efe41d344e99147aab017c8b41dd0ccdb151289ad6fbb822a80086  records/development/2026-08-20-model-selection-correspondence-reuse-search-plan-v1.json
52a8c157a3b3698b62b7dd7fe72438238793dce00e1024e7c28d4ab6e4870c1a  records/development/2026-08-20-model-selection-correspondence-reuse-search-attestation-v1.json

```

## 組み立て器のmodel・依頼先行の固定点

- argv：`["grep", "-nE", "_MODEL_PATTERN|依頼先：Reviewer|許可model|ALLOWED_RESPONSE_MODELS|model_not_allowed", "tools/request_builder/core.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.004s
- 完全性：二重実行一致

- stdout：

```text
4:核（redaction・digests・縦Bの命名導出・許可model定数）は共有部品を
14:from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
79:_MODEL_PATTERN = re.compile(r"許可model `([^`]+)`")
139:        "- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、"
140:        "許可model `%s`）\n"
257:    if not ALLOWED_RESPONSE_MODELS:
268:        model=ALLOWED_RESPONSE_MODELS[0],
439:    model_match = _MODEL_PATTERN.search(text)
442:    if model_match.group(1) not in ALLOWED_RESPONSE_MODELS:
443:        raise BuilderStop("model_not_allowed")

```

## 組み立て入口の引数固定点（backend・model旗の不在確認を含む）

- argv：`["grep", "-nE", "\"--type\"|\"--slug\"|\"--target\"|\"--backend\"|\"--model\"|repeated", "tools/request_builder/entry.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.004s
- 完全性：二重実行一致

- stdout：

```text
25:def _parse_flags(arguments, required, repeated=(), optional=()):
27:    lists = {flag: [] for flag in repeated}
28:    known = set(required) | set(repeated) | set(optional)
91:            ("--type", "--slug", "--title"),
92:            repeated=("--target",),
95:        if values is None or not values["--target"]:
101:                request_type=values["--type"],
104:                slug=values["--slug"],
106:                target_paths=values["--target"],

```

## 起動側のmodel選択点と入口旗の固定点

- argv：`["grep", "-nE", "requested_model = |_LAUNCH_FLAGS|\"--backend\"|\"--model\"|\"--accept-tier\"", "tools/reviewer_launch/core.py", "tools/reviewer_launch/entry.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.005s
- 完全性：二重実行一致

- stdout：

```text
tools/reviewer_launch/core.py:430:        "--model",
tools/reviewer_launch/core.py:887:    requested_model = allowed_models[0]
tools/reviewer_launch/entry.py:16:_LAUNCH_FLAGS = (
tools/reviewer_launch/entry.py:70:        ("--backend",),
tools/reviewer_launch/entry.py:75:    backend_name = values.get("--backend", "antigravity-cli")
tools/reviewer_launch/entry.py:139:        backend_name=values.get("--backend", "antigravity-cli"),
tools/reviewer_launch/entry.py:141:        accept_tier=values.get("--accept-tier"),
tools/reviewer_launch/entry.py:198:        _LAUNCH_FLAGS,
tools/reviewer_launch/entry.py:200:            "--backend",
tools/reviewer_launch/entry.py:201:            "--accept-tier",
tools/reviewer_launch/entry.py:210:    if "--accept-tier" in values:
tools/reviewer_launch/entry.py:212:            values["--accept-tier"] = int(values["--accept-tier"])

```

## RQ2装置の起動形（明示旗列＝任意旗追加の無影響確認）

- argv：`["grep", "-n", "reviewer_entry.main", "tools/evaluation/rq2_paired_trial.py"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.004s
- 完全性：二重実行一致

- stdout：

```text
179:    code = reviewer_entry.main(

```

## 両moduleのimport元（全一致行）

- argv：`["grep", "-rnE", "--include=*.py", "tools\\.request_builder|tools\\.reviewer_launch", "tools", "tests"]`
- 実行体：/usr/bin/grep
- exit：0・elapsed：0.061s
- 完全性：二重実行一致

- stdout：

```text
tools/operations/operation_contract_run.py:14:from tools.request_builder.entry import g30_main as request_builder_check_main
tools/operations/operation_contract_run.py:15:from tools.reviewer_launch.entry import g30_main as reviewer_launch_prepare_main
tools/evaluation/reviewer_bridge.py:17:from tools.request_builder import core as request_builder
tools/evaluation/rq2_paired_trial.py:176:    from tools.reviewer_launch import entry as reviewer_entry
tools/evaluation/operational_metrics.py:309:  from tools.request_builder import core
tools/request_builder/core.py:14:from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
tools/request_builder/core.py:15:from tools.reviewer_launch.record import verdict_record_relative_path
tools/request_builder/entry.py:12:from tools.request_builder import core
tools/reviewer_launch/core.py:32:from tools.reviewer_launch.record import VerdictInvalid, validate_verdict
tools/reviewer_launch/entry.py:12:from tools.reviewer_launch import core
tools/reviewer_launch/entry.py:13:from tools.reviewer_launch import record as record_module
tools/reviewer_launch/record.py:190:    from tools.reviewer_launch.core import BACKENDS
tests/test_reviewer_launch.py:27:    return importlib.import_module("tools.reviewer_launch.core")
tests/test_reviewer_launch.py:31:    return importlib.import_module("tools.reviewer_launch.record")
tests/test_reviewer_launch.py:35:    return importlib.import_module("tools.reviewer_launch.entry")
tests/test_reviewer_bridge.py:99:    request_builder = importlib.import_module("tools.request_builder.core")
tests/test_request_builder.py:23:    return importlib.import_module("tools.request_builder.core")
tests/test_request_builder.py:27:    return importlib.import_module("tools.request_builder.entry")
tests/test_request_builder.py:150:    from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
tests/test_request_builder.py:151:    from tools.reviewer_launch.record import verdict_record_relative_path
tests/test_request_builder.py:379:    from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
tests/test_rq2_paired_trial.py:132:    request_builder = importlib.import_module("tools.request_builder.core")

```

## 主題語の一致file数（tracked全体）

- argv：`["sh", "-c", "for t in 許可model ALLOWED_RESPONSE_MODELS 依頼先 requested_model; do c=$(git grep -l -- \"$t\" | wc -l | tr -d ' '); echo \"$t $c\"; done"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.315s
- 完全性：二重実行一致

- stdout：

```text
許可model 83
ALLOWED_RESPONSE_MODELS 36
依頼先 72
requested_model 9

```

## reviewer_launch試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_reviewer_launch.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.113s
- 完全性：二重実行一致

- stdout：

```text
94

```

## request_builder試験の収集件数

- argv：`["sh", "-c", ".venv/bin/python3 -m pytest tests/test_request_builder.py --collect-only -q -p no:cacheprovider 2>/dev/null | grep -c ::"]`
- 実行体：/bin/sh
- exit：0・elapsed：0.101s
- 完全性：二重実行一致

- stdout：

```text
42

```
