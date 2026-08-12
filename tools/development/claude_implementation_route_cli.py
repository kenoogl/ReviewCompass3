"""Claude実装委譲経路の機械向けCLI入口。"""

import json
from pathlib import Path
import sys

from tools.development.claude_implementation_route import (
    RouteStop,
    prepare,
    record_turn,
    status,
)


COMMAND_FLAGS = {
    "prepare": ("config", "private-root"),
    "record-turn": ("private-root", "run-id", "turn", "launch", "raw"),
    "status": ("private-root", "run-id"),
}
PATH_FLAGS = {
    "prepare": ("config", "private-root"),
    "record-turn": ("private-root", "launch", "raw"),
    "status": ("private-root",),
}


def _identifier(value):
    return (
        isinstance(value, str)
        and bool(value)
        and value[0].isalnum()
        and all(
            character.islower()
            or character.isdigit()
            or character in "._-"
            for character in value
        )
    )


def _known_run_id(arguments):
    if not arguments or arguments[0] not in ("record-turn", "status"):
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


def _parse(arguments):
    if not arguments or arguments[0] not in COMMAND_FLAGS:
        raise RouteStop("config_invalid")
    command = arguments[0]
    rest = list(arguments[1:])
    if len(rest) % 2:
        raise RouteStop("config_invalid")
    values = {}
    for index in range(0, len(rest), 2):
        flag = rest[index]
        value = rest[index + 1]
        if not flag.startswith("--"):
            raise RouteStop("config_invalid")
        name = flag[2:]
        if name not in COMMAND_FLAGS[command] or name in values:
            raise RouteStop("config_invalid")
        values[name] = value
    if set(values) != set(COMMAND_FLAGS[command]):
        raise RouteStop("config_invalid")
    if any(not Path(values[name]).is_absolute() for name in PATH_FLAGS[command]):
        raise RouteStop("config_invalid")
    if "run-id" in values and not _identifier(values["run-id"]):
        raise RouteStop("config_invalid")
    if command == "record-turn" and values["turn"] not in (
        "test",
        "implementation",
    ):
        raise RouteStop("config_invalid")
    return command, values


def _response(
    command,
    *,
    result,
    state=None,
    run_id=None,
    outcome=None,
    stop_code=None,
    detail=None,
):
    return {
        "schema_version": 1,
        "command": command,
        "result": result,
        "state": state,
        "run_id": run_id,
        "outcome": outcome,
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
        if command == "prepare":
            outcome = prepare(
                repository,
                values["config"],
                values["private-root"],
            )
        elif command == "record-turn":
            outcome = record_turn(
                repository,
                values["private-root"],
                values["run-id"],
                values["turn"],
                values["launch"],
                values["raw"],
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
            state=outcome.get("state"),
            run_id=outcome.get("run_id"),
            outcome=outcome,
        )
        exit_code = 0
    except RouteStop as error:
        response = _response(
            command,
            result="stopped",
            run_id=known_run_id,
            stop_code=error.code,
        )
        exit_code = 2
    except Exception:
        response = _response(
            command,
            result="failed",
            run_id=known_run_id,
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
