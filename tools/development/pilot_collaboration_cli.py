"""操縦者別連携pilotの共通CLI。"""

import json
from pathlib import Path
import sys

from tools.development.pilot_collaboration import (
    PilotStop,
    ingest,
    prepare,
    status,
)
from tools.development import claude_bootstrap_cli


COMMAND_FLAGS = {
    "bootstrap": ("manifest-digest", "approval-id"),
    "prepare": ("config", "private-root"),
    "ingest": (
        "private-root",
        "run-id",
        "stage",
        "attempt-id",
        "raw-file",
        "launch-record",
    ),
    "status": ("private-root", "run-id"),
}
PATH_FLAGS = {
    "bootstrap": (),
    "prepare": ("config", "private-root"),
    "ingest": ("private-root", "raw-file", "launch-record"),
    "status": ("private-root",),
}


def _identifier(value):
    if not isinstance(value, str) or not value:
        return False
    return all(character.islower() or character.isdigit() or character in "._-" for character in value) and value[0].isalnum()


def _known_run_id(arguments):
    if not arguments or arguments[0] not in ("ingest", "status"):
        return None
    positions = [
        index
        for index, value in enumerate(arguments[:-1])
        if value == "--run-id"
    ]
    if len(positions) != 1:
        return None
    candidate = arguments[positions[0] + 1]
    return candidate if _identifier(candidate) else None


def _parse(argv):
    if not argv or argv[0] not in COMMAND_FLAGS:
        raise PilotStop("config_invalid")
    command = argv[0]
    values = {}
    rest = list(argv[1:])
    if len(rest) % 2:
        raise PilotStop("config_invalid")
    for index in range(0, len(rest), 2):
        flag = rest[index]
        value = rest[index + 1]
        if not flag.startswith("--"):
            raise PilotStop("config_invalid")
        name = flag[2:]
        if name not in COMMAND_FLAGS[command] or name in values:
            raise PilotStop("config_invalid")
        values[name] = value
    if set(values) != set(COMMAND_FLAGS[command]):
        code = "stage_invalid" if command == "ingest" and "stage" in values and values["stage"] not in ("prompt_audit", "prompt_judgment") else "config_invalid"
        raise PilotStop(code)
    if command == "bootstrap":
        digest = values["manifest-digest"]
        approval_id = values["approval-id"]
        if (
            len(digest) != 64
            or any(character not in "0123456789abcdef" for character in digest)
            or not approval_id
            or any(
                not (
                    character.isalnum()
                    or character in "._-"
                )
                for character in approval_id
            )
        ):
            raise PilotStop("config_invalid")
    run_id = values.get("run-id")
    if run_id is not None and not _identifier(run_id):
        raise PilotStop("config_invalid")
    attempt_id = values.get("attempt-id")
    if attempt_id is not None and not _identifier(attempt_id):
        raise PilotStop("config_invalid", run_id=run_id)
    if command == "ingest" and values["stage"] not in ("prompt_audit", "prompt_judgment"):
        raise PilotStop("stage_invalid", run_id=run_id)
    if any(not Path(values[name]).is_absolute() for name in PATH_FLAGS[command]):
        raise PilotStop("config_invalid", run_id=run_id)
    return command, values


def _response(
    command,
    *,
    result,
    state=None,
    run_id=None,
    event_id=None,
    stop_code=None,
    detail=None,
):
    return {
        "schema_version": 1,
        "command": command,
        "result": result,
        "state": state,
        "run_id": run_id,
        "event_id": event_id,
        "stop_code": stop_code,
        "detail": detail,
    }


def run(argv=None):
    arguments = tuple(sys.argv[1:] if argv is None else argv)
    command = arguments[0] if arguments and arguments[0] in COMMAND_FLAGS else None
    known_run_id = _known_run_id(arguments)
    try:
        command, values = _parse(arguments)
        repository = Path.cwd().resolve()
        if command == "bootstrap":
            response, exit_code = claude_bootstrap_cli._run(
                values["manifest-digest"],
                values["approval-id"],
            )
            response = {"command": "bootstrap", **response}
            sys.stdout.write(
                json.dumps(
                    response,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            )
            return exit_code
        if command == "prepare":
            outcome = prepare(
                repository,
                values["config"],
                values["private-root"],
            )
        elif command == "ingest":
            outcome = ingest(
                repository,
                values["private-root"],
                values["run-id"],
                values["stage"],
                values["attempt-id"],
                values["raw-file"],
                values["launch-record"],
            )
        else:
            outcome = status(
                repository,
                values["private-root"],
                values["run-id"],
            )
        response = _response(
            command,
            result="completed",
            state=outcome["state"],
            run_id=outcome["run_id"],
            event_id=outcome["event_id"],
        )
        exit_code = 0
    except PilotStop as error:
        response_run_id = (
            error.run_id if error.run_id is not None else known_run_id
        )
        if command == "bootstrap":
            response = {
                "schema_version": 1,
                "command": "bootstrap",
                "result": "stopped",
                "stop_code": error.code,
                "payload_process_count": 0,
                "preflight_process_count": 0,
                "approval_state": "pending",
                "recovery": "入力とHuman承認を確認してください。",
            }
            exit_code = 2
        elif error.code == "internal_error":
            response = _response(
                command,
                result="failed",
                state=error.state,
                run_id=response_run_id,
                event_id=error.event_id,
                stop_code="internal_error",
                detail=error.detail,
            )
            exit_code = 1
        else:
            response = _response(
                command,
                result="stopped",
                state=error.state,
                run_id=response_run_id,
                event_id=error.event_id,
                stop_code=error.code,
                detail=error.detail,
            )
            exit_code = 2
    except Exception:
        response = _response(
            command,
            result="failed",
            stop_code="internal_error",
        )
        exit_code = 1
    sys.stdout.write(
        json.dumps(
            response,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    )
    return exit_code


def main():
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
