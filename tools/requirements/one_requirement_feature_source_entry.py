"""一件の要求候補整合検査の正式命令入口。"""

import sys

from tools.design.one_design_acceptance import DesignAcceptanceStop
from tools.design.one_design_acceptance import read_input_pair
from tools.requirements.one_requirement_feature_source import (
    RequirementCandidateStop,
    canonical_json_bytes,
    check_inputs,
)


_ARGUMENT_NAMES = frozenset(("--input-root", "--catalog", "--candidate"))
_KNOWN_REASONS = frozenset(
    (
        "invalid_arguments",
        "invalid_path",
        "unreadable_input",
        "size_limit_exceeded",
        "invalid_utf8",
        "invalid_schema",
        "sensitive_data_remaining",
        "unresolved_reference",
        "incomplete_coverage",
    )
)
_KNOWN_SOURCES = frozenset(("arguments", "catalog", "candidate", "none"))
_SOURCE_TRANSLATION = {"design": "catalog", "acceptance": "candidate"}


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


def _stop_exit_code(reason):
    if reason == "sensitive_data_remaining":
        return 3
    return 2


def main(arguments=None, *, output=None):
    """固定引数を処理し、正準JSON一件と終了コードを返す。"""

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
        catalog_bytes, candidate_bytes = read_input_pair(
            parsed["--input-root"],
            parsed["--catalog"],
            parsed["--candidate"],
        )
        result = check_inputs(catalog_bytes, candidate_bytes)
    except (DesignAcceptanceStop, RequirementCandidateStop) as stop:
        reason = stop.reason
        source = _SOURCE_TRANSLATION.get(stop.source, stop.source)
        if reason not in _KNOWN_REASONS or source not in _KNOWN_SOURCES:
            _write_result(
                selected_output,
                _stop_result("internal_failure", "none"),
            )
            return 4
        _write_result(selected_output, _stop_result(reason, source))
        return _stop_exit_code(reason)
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
