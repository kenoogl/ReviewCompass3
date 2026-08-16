"""Reviewer起動アダプタの入口（単体CLIとG30操作）。

契約010 §5.1-8。終了コードは成功0・停止2・内部失敗1。
出力は正準JSON一行（bytes）である。
"""

import hashlib
import sys
from pathlib import Path

from tools.bootstrap.immutable_result_store import canonical_json_bytes
from tools.reviewer_launch import core
from tools.reviewer_launch import record as record_module


_LAUNCH_FLAGS = (
    "--repository",
    "--request",
    "--expected-sha256",
    "--private-root",
    "--run-id",
)


def _write(output, document):
    output.write(canonical_json_bytes(document) + b"\n")


def _stop(output, reason, source):
    _write(output, {"status": "stopped", "reason": reason, "source": source})


def _parse_flags(arguments, required, optional=()):
    values = {}
    index = 0
    known = set(required) | set(optional)
    while index < len(arguments):
        flag = arguments[index]
        if flag not in known or index + 1 >= len(arguments):
            return None
        if flag in values:
            return None
        values[flag] = arguments[index + 1]
        index += 2
    if any(flag not in values for flag in required):
        return None
    return values


def g30_main(arguments=None, *, output=None):
    """G30操作`reviewer_launch_prepare`の入口（check形式・起動なし）。

    依頼recordの読取り・digest束縛・tier判定・固定promptのbyte検査だけを
    行う決定的処理である。外部起動（実質の外部送信）は行わない。
    """

    selected_arguments = (
        sys.argv[1:] if arguments is None else list(arguments)
    )
    selected_output = sys.stdout.buffer if output is None else output
    if not selected_arguments or selected_arguments[0] != "check":
        _stop(selected_output, "invalid_arguments", "arguments")
        return 2
    values = _parse_flags(
        selected_arguments[1:], ("--input-root", "--request")
    )
    if values is None:
        _stop(selected_output, "invalid_arguments", "arguments")
        return 2
    request_value = values["--request"]
    request_path = Path(request_value)
    if not request_path.is_absolute():
        request_path = Path(values["--input-root"]) / request_value
    try:
        data = request_path.read_bytes()
    except OSError:
        _stop(selected_output, "unreadable_input", "request")
        return 2
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        _stop(selected_output, "invalid_utf8", "request")
        return 2
    digest = hashlib.sha256(data).hexdigest()
    try:
        tier = core.judge_tier(
            core.BACKENDS["antigravity-cli"]["provider"]
        )
        prompt = core.build_prompt(
            str(Path(values["--input-root"]).resolve()),
            request_value,
            digest,
        )
    except core.LaunchStop as stop:
        _stop(selected_output, stop.reason, "request")
        return 2
    prompt_bytes = len(prompt.encode("utf-8"))
    if prompt_bytes > core.PROMPT_BYTE_LIMIT:
        _stop(
            selected_output, "prompt_payload_limit_exceeded", "request"
        )
        return 2
    _write(
        selected_output,
        {
            "status": "ok",
            "operation": "reviewer_launch_prepare",
            "backend": "antigravity-cli",
            "request": {"path": request_value, "sha256": digest},
            "tier": tier,
            "prompt_bytes": prompt_bytes,
        },
    )
    return 0


def _run_launch(values, output):
    repository = values["--repository"]
    request_relative = values["--request"]
    target_commit = record_module.current_commit(repository)
    result = core.launch_review(
        repository=repository,
        request_relative_path=request_relative,
        expected_sha256=values["--expected-sha256"],
        private_root=values["--private-root"],
        backend_name=values.get("--backend", "antigravity-cli"),
        run_id=values["--run-id"],
    )
    transcription = record_module.transcribe_verdict_record(
        repository=repository,
        request_relative_path=request_relative,
        request_sha256=values["--expected-sha256"],
        verdict=result["verdict"],
        tier=result["tier"],
        backend_name=result["backend"],
        model=result["model"],
        raw_digest=result["raw_digest"],
        raw_store_kind=result["raw_store_kind"],
        run_id=result["run_id"],
    )
    verification = record_module.post_verify(
        repository=repository,
        request_relative_path=request_relative,
        request_sha256=values["--expected-sha256"],
        record_relative_path=transcription["record_relative_path"],
        target_commit=target_commit,
        raw_digest=result["raw_digest"],
    )
    _write(
        output,
        {
            "status": "succeeded",
            "run_id": result["run_id"],
            "backend": result["backend"],
            "tier": result["tier"],
            "model": result["model"],
            "verdict": result["verdict"]["verdict"],
            "raw_digest": result["raw_digest"],
            "record_relative_path": transcription["record_relative_path"],
            "record_commit": transcription["commit"],
            "verification": verification,
        },
    )
    return 0


def main(argv=None, *, output=None):
    """単体入口。subcommand：launch（一往復）・check（G30 prepare形式）。"""

    selected_arguments = sys.argv[1:] if argv is None else list(argv)
    selected_output = sys.stdout.buffer if output is None else output
    if not selected_arguments:
        _stop(selected_output, "invalid_arguments", "arguments")
        return 2
    subcommand = selected_arguments[0]
    if subcommand == "check":
        return g30_main(selected_arguments, output=selected_output)
    if subcommand != "launch":
        _stop(selected_output, "invalid_arguments", "arguments")
        return 2
    values = _parse_flags(
        selected_arguments[1:], _LAUNCH_FLAGS, ("--backend",)
    )
    if values is None:
        _stop(selected_output, "invalid_arguments", "arguments")
        return 2
    try:
        return _run_launch(values, selected_output)
    except core.LaunchStop as stop:
        _stop(selected_output, stop.reason, "launch")
        return 2
    except record_module.TranscriptionStop as stop:
        _stop(selected_output, stop.reason, "record")
        return 2
    except record_module.VerdictInvalid:
        _stop(selected_output, "verdict_schema_nonconforming", "record")
        return 2
    except Exception:
        _stop(selected_output, "internal_failure", "none")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
