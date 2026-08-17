"""Reviewer起動アダプタの起動核（読み取り専用headless起動・保存）。

契約010 §5.1・§7.1（起動の固定形）・§9-2〜4の実装。起動は完全機械であり、
自由文を含めない。認証は利用者のCLIログイン状態だけを使う。
"""

import hashlib
import json
import os
import re
from pathlib import Path
import subprocess as _subprocess

from tools.development.claude_implementation_executor import (
    DISALLOWED_TOOLS as _EXECUTOR_DISALLOWED_TOOLS,
)

from tools.bootstrap.immutable_result_store import (
    ImmutableResultStoreError,
    store_immutable_json,
)
from tools.bootstrap.raw_review_store import (
    RawReviewStoreError,
    store_raw_executions,
)
from tools.bootstrap.review_execution import (
    ReviewAssignment,
    ReviewExecution,
)
from tools.reviewer_launch.record import VerdictInvalid, validate_verdict


PILOT_PROVIDER = "anthropic"

# 契約§7.1：直書きの契約固定定数。設定file・環境変数・引数・送信指示から
# 追加・変更できない。禁止一覧はRED段の実測で追加だけを許す。
FORBIDDEN_AUTH_ENVIRONMENT = (
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_GENAI_API_KEY",
    "GOOGLE_APPLICATION_CREDENTIALS",
)

# 契約010 §7.1：agyの許可model一覧。利用者承認recordで確定した値だけを置く。変更は契約改定。
# 承認：records/development/2026-08-16-reviewer-launch-allowed-models-approval-v1.md
_AGY_ALLOWED_RESPONSE_MODELS = ("gemini-3.1-pro-high",)

# 契約012 §5.1-5：claude-subagentの許可model一覧。利用者承認recordで確定した値だけを置く。変更は契約改定。
# 承認：records/development/2026-08-17-subagent-allowed-models-approval-v1.md
SUBAGENT_ALLOWED_RESPONSE_MODELS = ("claude-opus-5",)

# 契約012 §5.1-4：全backend許可modelの和集合（互換記号。契約011が検査基準にimportする）。
ALLOWED_RESPONSE_MODELS = (
    _AGY_ALLOWED_RESPONSE_MODELS + SUBAGENT_ALLOWED_RESPONSE_MODELS
)

# 契約012 §7.2：claude-subagentの認証遮断（由来：実行器FORBIDDEN_AUTH_ENVIRONMENT。
# 同値性は試験で固定。変更は契約改定）。
CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_FOUNDRY_API_KEY",
    "ANTHROPIC_VERTEX_PROJECT_ID",
    "AWS_BEARER_TOKEN_BEDROCK",
)

PROMPT_BYTE_LIMIT = 16384
PRINT_TIMEOUT = "600s"
_PROCESS_TIMEOUT_SECONDS = 660
PASSTHROUGH_ENVIRONMENT = (
    "PATH",
    "HOME",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "NO_COLOR",
)

# 契約012 §7.2訂正：claude-subagentの通過変数一覧（由来：実行器ALLOWED_CHILD_ENVIRONMENT。
# 同値性は試験で固定。変更は契約改定）。USERは保存済みlogin読み出しの必要条件（実測）。
# 訂正record：records/development/
# 2026-08-17-claude-subagent-passthrough-environment-correction-decision-v1.md
CLAUDE_PASSTHROUGH_ENVIRONMENT = (
    "HOME",
    "USER",
    "PATH",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "NO_COLOR",
)

# 契約012 §7.2訂正：claude-subagentの子環境注入（由来：実行器_child_environmentの注入。
# 同値性は試験で固定。変更は契約改定）。自動更新・余分な通信と文脈読込み・背景処理・
# 自動再試行を抑止する。agyの子環境には注入しない。
# 訂正record：records/development/
# 2026-08-17-claude-subagent-child-injection-correction-decision-v1.md
CLAUDE_CHILD_ENVIRONMENT_INJECTIONS = {
    "CLAUDE_CODE_MAX_RETRIES": "0",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL": "1",
    "CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS": "1",
    "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1",
    "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1",
    "CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS": "1",
    "ENABLE_CLAUDEAI_MCP_SERVERS": "false",
    "DISABLE_AUTOUPDATER": "1",
}

BACKENDS = {
    "antigravity-cli": {
        "provider": "google",
        "executable": "agy",
        "declared_tier": 1,
        "read_tool_name": "view_file",
    },
    "claude-subagent": {
        "provider": "anthropic",
        "executable": "claude",
        "declared_tier": 3,
        "read_tool_name": "Read",
    },
}

ASSIGNMENT_NAME = "reviewer"
RAW_STORE_KIND = "private_root_immutable_store"

# agy CLIのproject設定の置き場所（e2e-010-006後の局所調査で実測）。
# 利用者が対話sessionで与えた恒久許可（permissionGrants）がここへ保存され、
# headless起動は--project束縛が無いと許可が適用されない。
PROJECTS_CONFIG_ROOT = Path.home() / ".gemini" / "config" / "projects"

VERDICT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "reviewer",
        "freshness",
        "target",
        "findings",
        "unexamined",
        "verdict",
        "summary",
    ],
    "properties": {
        "reviewer": {
            "type": "object",
            "required": ["provider", "model"],
            "properties": {
                "provider": {"type": "string"},
                "model": {"type": "string"},
            },
        },
        "freshness": {
            "type": "object",
            "required": ["expected", "observed", "result"],
            "properties": {
                "expected": {"type": "string"},
                "observed": {"type": "string"},
                "result": {
                    "enum": ["match", "mismatch", "not_computable"]
                },
                "reason": {"type": "string"},
            },
        },
        "target": {
            "type": "object",
            "required": ["path", "commit"],
            "properties": {
                "path": {"type": "string"},
                "commit": {"type": "string"},
            },
        },
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "required": [
                    "identifier",
                    "severity",
                    "blocking",
                    "claim",
                    "evidence_path",
                    "evidence_location",
                ],
                "properties": {
                    "identifier": {"type": "string"},
                    "severity": {"type": "string"},
                    "blocking": {"type": "boolean"},
                    "claim": {"type": "string"},
                    "evidence_path": {"type": "string"},
                    "evidence_location": {"type": "string"},
                },
            },
        },
        "unexamined": {"type": "array", "items": {"type": "string"}},
        "verdict": {
            "enum": [
                "verified",
                "verified_with_findings",
                "rejected",
                "stale_target",
                "unable",
            ]
        },
        "summary": {"type": "string"},
    },
}


class _SubprocessFacade:
    """試験差替えをこのmodule内だけに閉じるprocess入口。"""

    run = staticmethod(_subprocess.run)


subprocess = _SubprocessFacade()


class LaunchStop(Exception):
    """Reviewerを安全に起動または取込みできないため停止した。"""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def judge_tier(backend_provider):
    """独立性tierを機械判定する。本契約はTier 1以外を停止する。"""

    if not isinstance(backend_provider, str) or not backend_provider:
        raise LaunchStop("backend_unknown")
    if backend_provider == PILOT_PROVIDER:
        raise LaunchStop("reviewer_not_independent_tier")
    return 1


def build_prompt(
    repository_root,
    request_relative_path,
    expected_sha256,
    read_tool_name="view_file",
):
    """固定形式の起動promptを生成する。自由文・依頼内容の複製を含めない。

    実行環境は読み取り専用であり、端末commandの実行と書込みはできない
    （e2e-010-002実測：headlessでは道具許可が自動拒否され会話が終了する）。
    読取り道具のpath引数は絶対pathを要求する（e2e-010-004実測：引数名
    AbsolutePath。相対path指示は失敗し、領域外の絶対path推測で拒否死する）。
    """

    absolute_request = "%s/%s" % (repository_root, request_relative_path)
    return (
        "あなたは独立したReviewerです。次のcommit済み依頼recordだけを"
        "対象にレビューを実施してください。\n"
        "対象repository（作業領域）：%s\n"
        "対象依頼record：%s\n"
        "対象依頼recordの絶対path：%s\n"
        "期待SHA-256：%s\n"
        "この実行環境は読み取り専用です。端末commandの実行、repository"
        "への書込み、許可を求める道具の使用は行わず、fileの読取り道具"
        "だけを使ってください。\n"
        "読取り道具のpath引数には対象repository配下の絶対pathだけを"
        "渡し、対象repositoryの外（利用者のhome等）へは一切アクセス"
        "しないでください。領域外アクセスは自動拒否され、その時点で"
        "レビューが終了します。\n"
        "最初の操作として、読取り道具%sで対象依頼recordの"
        "絶対pathを開き、本依頼の対象であることを確認してください。"
        "digestの機械計算がこの環境で行えない場合、freshnessには"
        "expectedへ期待SHA-256を転記し、resultをnot_computableとして"
        "理由を記載してください（内容が明らかに別物ならmismatchとして"
        "判定せず停止）。\n"
        "レビューを完了し、最終応答は指定のJSON schemaに完全に従う"
        "構造化出力だけで返してください。検査できなかった事項は"
        "unexamined配列へ明示してください。\n"
        % (
            repository_root,
            request_relative_path,
            absolute_request,
            expected_sha256,
            read_tool_name,
        )
    )


def build_arguments(executable, prompt, model, project_id):
    """契約§7.1の固定引数を組み立てる。

    agyの旗解析はGo標準flag形式であり、`--print`は値（prompt本文）を取る
    （E2E e2e-010-001の実測。値旗は`--旗=値`形式で渡し、位置引数を作らない）。
    `--mode=plan`は読み取り専用相当の確定（契約§7.1がRED段の実測へ留保した
    事項。E2E e2e-010-002の実測：既定のrequest-review方式はheadlessで道具
    許可が自動拒否となり、読み取りすら成立しない）。書込みを許す
    `--mode=accept-edits`は使用禁止のまま。
    `--sandbox`（端末制限つきsandbox実行）は同じ留保事項の確定の続きで
    ある（e2e-010-005の実測：request-review方式ではrepository内の
    view_fileすら承認必須＝headlessで自動拒否となるため、制限を強める
    sandbox内での自動許可を検証する）。
    `--project=<id>`は利用者の対話sessionで保存済みの読取り恒久許可を
    headless起動へ結び付ける（e2e-010-006後の実測：許可はproject設定
    `permissionGrants`に保存され、project束縛の無い起動には適用されない）。
    """

    return [
        executable,
        "--output-format=stream-json",
        "--json-schema="
        + json.dumps(VERDICT_SCHEMA, ensure_ascii=False, sort_keys=True),
        "--model=" + model,
        "--mode=plan",
        "--sandbox",
        "--project=" + project_id,
        "--disable-slash-commands",
        "--print-timeout=" + PRINT_TIMEOUT,
        "--print=" + prompt,
    ]


def build_claude_arguments(executable, prompt, model):
    """契約012 §7.2のclaude-subagent固定引数（実行器設計の流用・読み取り専用）。

    `--verbose`はclaude CLIが`--print`＋`--output-format=stream-json`の組で
    必須とする旗（2.1.220実測）。位置は流用元実行器と同じstream-json直後。
    訂正record：records/development/
    2026-08-17-claude-subagent-verbose-argument-correction-decision-v1.md
    """

    return [
        executable,
        "--print",
        "--output-format",
        "stream-json",
        "--verbose",
        "--tools",
        "Read,Glob,Grep",
        "--allowedTools",
        "Read(/**)",
        "--disallowedTools",
        *_EXECUTOR_DISALLOWED_TOOLS,
        "--permission-mode",
        "dontAsk",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
        "--disable-slash-commands",
        "--no-chrome",
        "--model",
        model,
        prompt,
    ]


def _child_environment(forbidden_names, passthrough_names):
    for name in forbidden_names:
        if name in os.environ:
            raise LaunchStop("api_key_environment_forbidden")
    return {
        name: os.environ[name]
        for name in passthrough_names
        if name in os.environ
    }


def _resolve_tier(backend, accept_tier):
    """契約012 §7.3：tier判定と明示受容。受容が無ければ従来どおり停止。"""

    if backend["provider"] != PILOT_PROVIDER:
        return 1
    declared = backend["declared_tier"]
    if accept_tier == declared:
        return declared
    raise LaunchStop("reviewer_not_independent_tier")


def resolve_project_binding(repository):
    """repositoryに対応するagy projectを設定から機械解決する。

    利用者が対話sessionで与えた読取り恒久許可（`read_file(<repo>)`）を持つ
    projectのidを返す。projectが無ければ`project_binding_missing`、許可が
    無ければ`read_grant_missing`で起動前に停止する（許可の新設・迂回は
    行わない。許可を与えるのは利用者の対話sessionだけである）。
    """

    repo = Path(repository).resolve()
    folder_uri = "file://%s" % repo
    required_grant = "read_file(%s)" % repo
    try:
        candidates = sorted(PROJECTS_CONFIG_ROOT.glob("*.json"))
    except OSError:
        candidates = []
    for path in candidates:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(value, dict):
            continue
        resources = (
            (value.get("projectResources") or {}).get("resources") or []
        )
        matched = any(
            isinstance(resource, dict)
            and (resource.get("gitFolder") or {}).get("folderUri")
            == folder_uri
            for resource in resources
        )
        if not matched:
            continue
        identifier = value.get("id")
        if not isinstance(identifier, str) or not identifier:
            continue
        grants = (
            (value.get("permissionGrants") or {}).get("permissionGrants")
            or {}
        )
        allow = grants.get("allow") or []
        if required_grant not in allow:
            raise LaunchStop("read_grant_missing")
        return identifier
    raise LaunchStop("project_binding_missing")


def _validate_private_root(repository, private_root):
    repository_path = Path(repository).resolve()
    private_path = Path(private_root).resolve()
    if private_path == repository_path or repository_path in (
        private_path.parents
    ):
        raise LaunchStop("private_root_inside_repository")
    return private_path


def _parse_stream(stdout):
    events = []
    for line in stdout.splitlines():
        text = line.strip()
        if not text:
            continue
        try:
            value = json.loads(text)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def _observed_models(events):
    """agyのstream実形式（e2e-010-002実測）：initイベントのinit.modelを読む。"""

    models = []
    for event in events:
        init = event.get("init")
        if isinstance(init, dict):
            value = init.get("model")
            if isinstance(value, str) and value:
                models.append(value)
    return models


def _extract_verdict(events):
    """agyのstream実形式：event=\"result\"のresult.responseがJSON本文を持つ。"""

    candidate = None
    for event in events:
        if event.get("event") == "result" and isinstance(
            event.get("result"), dict
        ):
            candidate = event["result"]
    if candidate is None:
        raise LaunchStop("verdict_schema_nonconforming")
    response = candidate.get("response")
    if isinstance(response, str) and response.strip():
        try:
            value = json.loads(response)
        except (json.JSONDecodeError, ValueError) as error:
            raise LaunchStop("verdict_schema_nonconforming") from error
    elif "verdict" in candidate:
        value = candidate
    else:
        raise LaunchStop("verdict_schema_nonconforming")
    if not isinstance(value, dict):
        raise LaunchStop("verdict_schema_nonconforming")
    return value


_JSON_FENCE_PATTERN = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)


def _claude_observed_models(events):
    """claude CLIのstream形式：top levelまたはmessage内のmodel欄を読む。"""

    models = []
    for event in events:
        value = event.get("model")
        if isinstance(value, str) and value:
            models.append(value)
        message = event.get("message")
        if isinstance(message, dict):
            nested = message.get("model")
            if isinstance(nested, str) and nested:
                models.append(nested)
    return models


def _parse_json_text(text):
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except (json.JSONDecodeError, ValueError):
        pass
    match = _JSON_FENCE_PATTERN.search(text)
    if match is not None:
        try:
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError):
            pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if 0 <= start < end:
        try:
            return json.loads(stripped[start : end + 1])
        except (json.JSONDecodeError, ValueError):
            pass
    raise LaunchStop("verdict_schema_nonconforming")


def _claude_extract_verdict(events):
    """claude CLIのstream形式：type==resultのresult本文からJSONを抽出する。"""

    candidate = None
    for event in events:
        if event.get("type") == "result" and "result" in event:
            candidate = event["result"]
    if isinstance(candidate, dict):
        value = candidate
    elif isinstance(candidate, str) and candidate.strip():
        value = _parse_json_text(candidate)
    else:
        raise LaunchStop("verdict_schema_nonconforming")
    if not isinstance(value, dict):
        raise LaunchStop("verdict_schema_nonconforming")
    return value


def _store_outputs(
    private_root,
    run_id,
    provider,
    model,
    prompt_digest,
    status,
    raw_response,
    error,
    launch_document,
):
    assignment = ReviewAssignment(
        name=ASSIGNMENT_NAME,
        provider=provider,
        model=model,
        route="independent",
    )
    execution = ReviewExecution(
        assignment=assignment,
        status=status,
        raw_response=raw_response,
        error=error,
        contracted_payload_digest=prompt_digest,
    )
    try:
        stored = store_raw_executions(
            private_root, run_id, (execution,)
        )[0]
        document = dict(launch_document)
        document["raw_digest"] = stored.raw_digest
        document["raw_relative_path"] = stored.relative_path
        store_immutable_json(
            private_root, "%s/launch.json" % run_id, document
        )
    except (RawReviewStoreError, ImmutableResultStoreError) as error_value:
        raise LaunchStop("raw_store_failed") from error_value
    return stored


def launch_review(
    *,
    repository,
    request_relative_path,
    expected_sha256,
    private_root,
    backend_name,
    run_id,
    accept_tier=None,
    acceptance_ref=None,
):
    """読み取り専用レビュー一往復の起動・保存・判定取り出しを行う。

    契約012：backend別の禁止環境変数・許可model・tier受容を扱う。Tier 2／3は
    `accept_tier`の一致と`acceptance_ref`（実在するrecord path）が無ければ
    従来どおり停止する。
    """

    backend = BACKENDS.get(backend_name)
    if backend is None:
        raise LaunchStop("backend_unknown")
    if backend_name == "claude-subagent":
        forbidden_names = CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT
        allowed_models = SUBAGENT_ALLOWED_RESPONSE_MODELS
        passthrough_names = CLAUDE_PASSTHROUGH_ENVIRONMENT
        injections = CLAUDE_CHILD_ENVIRONMENT_INJECTIONS
    else:
        forbidden_names = FORBIDDEN_AUTH_ENVIRONMENT
        # 契約012 §7.1：agyの照合はagy専用一覧（和集合は契約011互換の記号のみ。
        # e2e-012-001判定F-1の修正）。
        allowed_models = _AGY_ALLOWED_RESPONSE_MODELS
        passthrough_names = PASSTHROUGH_ENVIRONMENT
        injections = {}
    environment = _child_environment(forbidden_names, passthrough_names)
    environment.update(injections)
    tier = _resolve_tier(backend, accept_tier)
    if tier != 1:
        if (
            not isinstance(acceptance_ref, str)
            or not acceptance_ref
            or not (Path(repository) / acceptance_ref).is_file()
        ):
            raise LaunchStop("acceptance_reference_missing")
    if not allowed_models:
        raise LaunchStop("allowed_models_unfixed")
    requested_model = allowed_models[0]
    if backend_name == "antigravity-cli":
        project_id = resolve_project_binding(repository)
    else:
        project_id = None
    private_path = _validate_private_root(repository, private_root)

    if not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise LaunchStop("request_record_stale")
    request_path = Path(repository) / request_relative_path
    try:
        request_bytes = request_path.read_bytes()
    except OSError as error:
        raise LaunchStop("request_record_unreadable") from error
    if hashlib.sha256(request_bytes).hexdigest() != expected_sha256:
        raise LaunchStop("request_record_stale")

    prompt = build_prompt(
        str(Path(repository).resolve()),
        request_relative_path,
        expected_sha256,
        read_tool_name=backend["read_tool_name"],
    )
    prompt_encoded = prompt.encode("utf-8")
    if len(prompt_encoded) > PROMPT_BYTE_LIMIT:
        raise LaunchStop("prompt_payload_limit_exceeded")
    prompt_digest = hashlib.sha256(prompt_encoded).hexdigest()
    if backend_name == "claude-subagent":
        arguments = build_claude_arguments(
            backend["executable"], prompt, requested_model
        )
    else:
        arguments = build_arguments(
            backend["executable"], prompt, requested_model, project_id
        )

    try:
        completed = subprocess.run(
            arguments,
            cwd=str(repository),
            env=environment,
            capture_output=True,
            text=True,
            timeout=_PROCESS_TIMEOUT_SECONDS,
        )
    except Exception as error:
        raise LaunchStop("launch_failed") from error

    stdout = completed.stdout if isinstance(completed.stdout, str) else ""
    stderr = completed.stderr if isinstance(completed.stderr, str) else ""
    events = _parse_stream(stdout)
    if backend_name == "claude-subagent":
        models = _claude_observed_models(events)
    else:
        models = _observed_models(events)
    launch_document = {
        "schema_version": 1,
        "run_id": run_id,
        "backend": backend_name,
        "provider": backend["provider"],
        "tier": tier,
        "requested_model": requested_model,
        "models_observed": sorted(set(models)),
        "exit_code": completed.returncode,
        "arguments": list(arguments),
        "environment_keys": sorted(environment),
        "request": {
            "path": request_relative_path,
            "sha256": expected_sha256,
        },
        "prompt_sha256": prompt_digest,
        "print_timeout": PRINT_TIMEOUT,
        "project_id": project_id,
        "accept_tier": accept_tier,
        "acceptance_reference": acceptance_ref,
        "read_tool": backend["read_tool_name"],
    }

    if completed.returncode != 0:
        error_text = "exit_code=%d; stderr=%s" % (
            completed.returncode,
            stderr[-4000:] or "(empty)",
        )
        _store_outputs(
            private_path,
            run_id,
            backend["provider"],
            requested_model,
            prompt_digest,
            "failed",
            None,
            error_text,
            launch_document,
        )
        raise LaunchStop("launch_failed")

    stored = _store_outputs(
        private_path,
        run_id,
        backend["provider"],
        requested_model,
        prompt_digest,
        "succeeded",
        stdout,
        None,
        launch_document,
    )

    if not models:
        raise LaunchStop("response_model_unobserved")
    if any(model not in allowed_models for model in models):
        raise LaunchStop("response_model_not_allowed")
    if backend_name == "claude-subagent":
        verdict = _claude_extract_verdict(events)
    else:
        verdict = _extract_verdict(events)
    try:
        validate_verdict(verdict)
    except VerdictInvalid as error:
        raise LaunchStop("verdict_schema_nonconforming") from error

    return {
        "status": "succeeded",
        "run_id": run_id,
        "backend": backend_name,
        "tier": tier,
        "model": models[-1],
        "raw_digest": stored.raw_digest,
        "raw_relative_path": stored.relative_path,
        "launch_record_relative_path": "%s/launch.json" % run_id,
        "raw_store_kind": RAW_STORE_KIND,
        "verdict": verdict,
    }
