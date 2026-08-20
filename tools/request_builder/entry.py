"""依頼組み立て器の入口（単体CLIとG30操作）。

契約011 §5.1-5。終了コードは成功0・停止2・内部失敗1。
出力は正準JSON一行（bytes）である。
"""

import sys
from datetime import datetime
from pathlib import Path

from tools.bootstrap.immutable_result_store import canonical_json_bytes
from tools.request_builder import core


def _write(output, document):
    output.write(canonical_json_bytes(document) + b"\n")


def _stop(output, reason, source):
    _write(
        output, {"status": "stopped", "reason": reason, "source": source}
    )


def _parse_flags(arguments, required, repeated=(), optional=()):
    values = {}
    lists = {flag: [] for flag in repeated}
    known = set(required) | set(repeated) | set(optional)
    index = 0
    while index < len(arguments):
        flag = arguments[index]
        if flag not in known or index + 1 >= len(arguments):
            return None
        value = arguments[index + 1]
        if flag in lists:
            lists[flag].append(value)
        else:
            if flag in values:
                return None
            values[flag] = value
        index += 2
    if any(flag not in values for flag in required):
        return None
    values.update(lists)
    return values


def g30_main(arguments=None, *, output=None):
    """G30操作`request_builder_check`の入口（check形式・完全local）。"""

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
    try:
        result = core.check(
            repository=values["--input-root"],
            request_relative_path=values["--request"],
        )
    except core.BuilderStop as stop:
        _stop(selected_output, stop.reason, "request")
        return 2
    except Exception:
        _stop(selected_output, "internal_failure", "none")
        return 1
    _write(selected_output, result)
    return 0


def main(argv=None, *, output=None):
    """単体入口。subcommand：assemble（草稿生成）・check（機械検査）。"""

    selected_arguments = sys.argv[1:] if argv is None else list(argv)
    selected_output = sys.stdout.buffer if output is None else output
    if not selected_arguments:
        _stop(selected_output, "invalid_arguments", "arguments")
        return 2
    subcommand = selected_arguments[0]
    if subcommand == "assemble":
        values = _parse_flags(
            selected_arguments[1:],
            ("--type", "--slug", "--title"),
            repeated=("--target",),
            optional=("--repository", "--date", "--backend", "--model"),
        )
        if values is None or not values["--target"]:
            _stop(selected_output, "invalid_arguments", "arguments")
            return 2
        try:
            result = core.assemble(
                repository=values.get("--repository") or str(Path.cwd()),
                request_type=values["--type"],
                record_date=values.get("--date")
                or datetime.now().astimezone().date().isoformat(),
                slug=values["--slug"],
                title=values["--title"],
                target_paths=values["--target"],
                backend=values.get("--backend"),
                model=values.get("--model"),
            )
        except core.BuilderStop as stop:
            _stop(selected_output, stop.reason, "assemble")
            return 2
        except Exception:
            _stop(selected_output, "internal_failure", "none")
            return 1
        _write(selected_output, result)
        return 0
    if subcommand == "check":
        values = _parse_flags(
            selected_arguments[1:],
            ("--request",),
            optional=("--repository",),
        )
        if values is None:
            _stop(selected_output, "invalid_arguments", "arguments")
            return 2
        try:
            result = core.check(
                repository=values.get("--repository") or str(Path.cwd()),
                request_relative_path=values["--request"],
            )
        except core.BuilderStop as stop:
            _stop(selected_output, stop.reason, "request")
            return 2
        except Exception:
            _stop(selected_output, "internal_failure", "none")
            return 1
        _write(selected_output, result)
        return 0
    _stop(selected_output, "invalid_arguments", "arguments")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
