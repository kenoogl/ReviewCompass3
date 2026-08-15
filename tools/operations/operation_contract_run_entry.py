"""最小運用契約実行の正式命令入口。"""

import json
import sys

from tools.operations.operation_contract_run import (
    OperationContractStop,
    canonical_json_bytes,
    run_operation_contract,
)


_KNOWN_REASONS = frozenset(
    (
        "invalid_arguments",
        "invalid_path",
        "unreadable_input",
        "size_limit_exceeded",
        "invalid_utf8",
        "invalid_schema",
        "sensitive_data_remaining",
        "invalid_output_root",
        "part_stopped",
        "binding_mismatch",
        "record_write_failed",
        "partial_cleanup_failed",
    )
)
_KNOWN_SOURCES = frozenset(("arguments", "contract", "part", "output", "none"))
_EXIT_CODES = {
    "sensitive_data_remaining": 3,
    "record_write_failed": 4,
    "part_stopped": 5,
    "partial_cleanup_failed": 6,
}


def _is_absolute_lexical_path(value):
    if not isinstance(value, str) or not value.startswith("/"):
        return False
    if value == "/":
        return True
    return all(part not in ("", ".", "..") for part in value.split("/")[1:])


def _parse_arguments(arguments):
    if not isinstance(arguments, (list, tuple)) or len(arguments) != 3:
        return None, "invalid_arguments"
    if arguments[0] != "run" or arguments[1] != "--contract":
        return None, "invalid_arguments"
    contract_path = arguments[2]
    if not isinstance(contract_path, str):
        return None, "invalid_arguments"
    if not _is_absolute_lexical_path(contract_path):
        return None, "invalid_path"
    return contract_path, None


def _stop_result(reason, source, extra=None):
    result = {
        "external_send_approved": False,
        "reason": reason,
        "source": source,
        "status": "stopped",
    }
    if extra:
        result.update(extra)
    return result


def _write_payload(output, payload):
    output.write(payload)


def main(arguments=None, *, output=None):
    """固定引数を処理し、正準JSON一件と終了コードを返す。"""

    selected_arguments = sys.argv[1:] if arguments is None else arguments
    selected_output = sys.stdout.buffer if output is None else output
    contract_path, argument_error = _parse_arguments(selected_arguments)
    if argument_error is not None:
        _write_payload(
            selected_output,
            canonical_json_bytes(_stop_result(argument_error, "arguments"))
            + b"\n",
        )
        return 2

    try:
        record_bytes = run_operation_contract(contract_path)
    except OperationContractStop as stop:
        extra = stop.extra if isinstance(stop.extra, dict) else None
        if stop.reason not in _KNOWN_REASONS or stop.source not in _KNOWN_SOURCES:
            _write_payload(
                selected_output,
                canonical_json_bytes(_stop_result("internal_failure", "none"))
                + b"\n",
            )
            return 4
        _write_payload(
            selected_output,
            canonical_json_bytes(_stop_result(stop.reason, stop.source, extra))
            + b"\n",
        )
        return _EXIT_CODES.get(stop.reason, 2)
    except Exception:
        _write_payload(
            selected_output,
            canonical_json_bytes(_stop_result("internal_failure", "none"))
            + b"\n",
        )
        return 4

    _write_payload(selected_output, record_bytes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
