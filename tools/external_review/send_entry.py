"""外部レビュア一回送信の正式命令入口（契約008 v5・改名は契約009）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import sys

from tools.external_review.send import (
    SendStop,
    canonical_json_bytes,
    run_send_order,
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
        "invalid_repository_root",
        "source_file_rejected",
        "limit_exceeded",
        "duplicate_order",
        "missing_credentials",
        "reviewer_not_independent",
        "invalid_output_root",
        "record_write_failed",
        "partial_cleanup_failed",
        "http_error",
        "network_failure",
        "response_size_exceeded",
    )
)
_KNOWN_SOURCES = frozenset(
    ("arguments", "order", "source_file", "credentials", "ledger", "network", "none")
)
_EXIT_CODES = {
    "sensitive_data_remaining": 3,
    "record_write_failed": 4,
    "partial_cleanup_failed": 6,
    "http_error": 7,
    "network_failure": 7,
    "response_size_exceeded": 7,
}


def _is_absolute_lexical_path(value):
    if not isinstance(value, str) or not value.startswith("/"):
        return False
    if "\x00" in value or any(
        0xD800 <= ord(character) <= 0xDFFF for character in value
    ):
        return False
    if value == "/":
        return True
    return all(part not in ("", ".", "..") for part in value.split("/")[1:])


def _parse_arguments(arguments):
    if not isinstance(arguments, (list, tuple)) or len(arguments) != 3:
        return None, "invalid_arguments"
    if arguments[0] != "send" or arguments[1] != "--order":
        return None, "invalid_arguments"
    order_path = arguments[2]
    if not isinstance(order_path, str):
        return None, "invalid_arguments"
    if not _is_absolute_lexical_path(order_path):
        return None, "invalid_path"
    return order_path, None


def _stop_payload(reason, source, approved):
    return canonical_json_bytes(
        {
            "external_send_approved": approved,
            "reason": reason,
            "source": source,
            "status": "stopped",
        }
    ) + b"\n"


def main(arguments=None, *, output=None):
    """固定引数を処理し、正準JSON一件と終了コードを返す。"""

    selected_arguments = sys.argv[1:] if arguments is None else arguments
    selected_output = sys.stdout.buffer if output is None else output
    order_path, argument_error = _parse_arguments(selected_arguments)
    if argument_error is not None:
        selected_output.write(_stop_payload(argument_error, "arguments", False))
        return 2

    try:
        result_bytes = run_send_order(order_path)
    except SendStop as stop:
        if stop.reason not in _KNOWN_REASONS or stop.source not in _KNOWN_SOURCES:
            selected_output.write(_stop_payload("internal_failure", "none", False))
            return 4
        selected_output.write(
            _stop_payload(stop.reason, stop.source, bool(stop.after_attempt))
        )
        return _EXIT_CODES.get(stop.reason, 2)
    except Exception:
        selected_output.write(_stop_payload("internal_failure", "none", False))
        return 4

    selected_output.write(result_bytes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
