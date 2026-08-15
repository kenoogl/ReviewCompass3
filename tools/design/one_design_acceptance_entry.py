"""一件の設計・受入条件照合の正式命令入口。"""

import sys

from tools.design import one_design_acceptance as core
from tools.design.one_design_acceptance import DesignAcceptanceStop
from tools.design.one_design_acceptance import canonical_json_bytes
from tools.design.one_design_acceptance import compare_inputs
from tools.design.one_design_acceptance import read_input_pair


_ARGUMENT_NAMES = frozenset(("--input-root", "--design", "--acceptance"))
_KNOWN_REASONS = frozenset(
    (
        "invalid_arguments",
        "invalid_path",
        "unreadable_input",
        "size_limit_exceeded",
        "invalid_utf8",
        "invalid_schema",
    )
)
_KNOWN_SOURCES = frozenset(("arguments", "design", "acceptance", "none"))


def _is_absolute_lexical_path(value):
    if not isinstance(value, str) or not value.startswith("/"):
        return False
    if value == "/":
        return True
    return all(part not in ("", ".", "..") for part in value.split("/")[1:])


def _parse_arguments(arguments):
    if not isinstance(arguments, (list, tuple)) or len(arguments) != 7:
        return None, "invalid_arguments"
    if arguments[0] != "check":
        return None, "invalid_arguments"
    parsed = {}
    for index in range(1, len(arguments), 2):
        name = arguments[index]
        value = arguments[index + 1]
        if name not in _ARGUMENT_NAMES or name in parsed or not isinstance(value, str):
            return None, "invalid_arguments"
        parsed[name] = value
    if set(parsed) != _ARGUMENT_NAMES:
        return None, "invalid_arguments"
    if any(not _is_absolute_lexical_path(value) for value in parsed.values()):
        return None, "invalid_path"
    return parsed, None


def _stop_result(reason, source):
    return {
        "external_send_approved": False,
        "reason": reason,
        "source": source,
        "status": "stopped",
    }


def _write_result(output, result):
    output.write(canonical_json_bytes(result) + b"\n")


def main(arguments=None, *, output=None):
    """固定引数を処理し、正準JSON一件の終了コードを返す。"""

    selected_arguments = sys.argv[1:] if arguments is None else arguments
    selected_output = sys.stdout.buffer if output is None else output
    parsed, argument_error = _parse_arguments(selected_arguments)
    if argument_error is not None:
        _write_result(
            selected_output,
            _stop_result(argument_error, "arguments"),
        )
        return 2

    try:
        design_bytes, acceptance_bytes = read_input_pair(
            parsed["--input-root"],
            parsed["--design"],
            parsed["--acceptance"],
        )
        result = compare_inputs(design_bytes, acceptance_bytes)
    except DesignAcceptanceStop as stop:
        if stop.reason not in _KNOWN_REASONS or stop.source not in _KNOWN_SOURCES:
            _write_result(
                selected_output,
                _stop_result("internal_failure", "none"),
            )
            return 4
        _write_result(selected_output, _stop_result(stop.reason, stop.source))
        return 2
    except Exception:
        _write_result(
            selected_output,
            _stop_result("internal_failure", "none"),
        )
        return 4

    _write_result(selected_output, result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
