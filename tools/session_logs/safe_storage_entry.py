"""一件のSession記録を保存・再読込み・削除する製品入口。"""

import argparse
import json
import sys

from tools.session_logs.read_only_entry import prepare_safe_result
from tools.session_logs.safe_storage import (
    StorageStop,
    delete_record,
    load_derived,
    plan_delete,
    store_new,
)


EXIT_OK = 0
EXIT_STOPPED = 4


def _print_json(value):
    print(json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ))


def _stopped(reason):
    return {
        "error": reason,
        "external_send_approved": False,
        "status": "stopped",
    }


def _add_record_arguments(parser):
    parser.add_argument("--sensitive-root", required=True)
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--record-id", required=True)


def _arguments(argv):
    parser = argparse.ArgumentParser()
    operations = parser.add_subparsers(dest="operation", required=True)

    store = operations.add_parser("store")
    store.add_argument("--repository-root", required=True)
    store.add_argument("--raw-root", required=True)
    store.add_argument("--raw-log", required=True)
    store.add_argument("--sensitive-root", required=True)
    store.add_argument("--data-root", required=True)
    store.add_argument("--stored-at", required=True)
    store.add_argument("--retention-until", required=True)

    load = operations.add_parser("load-derived")
    _add_record_arguments(load)
    load.add_argument("--current-at", required=True)

    plan = operations.add_parser("plan-delete")
    _add_record_arguments(plan)
    plan.add_argument("--current-at")

    delete = operations.add_parser("delete")
    _add_record_arguments(delete)
    delete.add_argument("--confirmation-sha256", required=True)
    delete.add_argument("--deleted-at", required=True)
    delete.add_argument("--current-at")
    return parser.parse_args(argv)


def _execute(arguments):
    if arguments.operation == "store":
        source_exit_code, safe_result = prepare_safe_result(
            arguments.raw_root,
            arguments.raw_log,
        )
        if source_exit_code != EXIT_OK or safe_result.get("status") != "ok":
            raise StorageStop("unsafe_source_result")
        return store_new(
            repository_root=arguments.repository_root,
            raw_root=arguments.raw_root,
            raw_log=arguments.raw_log,
            sensitive_root=arguments.sensitive_root,
            data_root=arguments.data_root,
            safe_result=safe_result,
            stored_at=arguments.stored_at,
            retention_until=arguments.retention_until,
        )
    if arguments.operation == "load-derived":
        return load_derived(
            sensitive_root=arguments.sensitive_root,
            data_root=arguments.data_root,
            record_id=arguments.record_id,
            current_at=arguments.current_at,
        )
    if arguments.operation == "plan-delete":
        return plan_delete(
            sensitive_root=arguments.sensitive_root,
            data_root=arguments.data_root,
            record_id=arguments.record_id,
            current_at=arguments.current_at,
        )
    return delete_record(
        sensitive_root=arguments.sensitive_root,
        data_root=arguments.data_root,
        record_id=arguments.record_id,
        confirmation_sha256=arguments.confirmation_sha256,
        deleted_at=arguments.deleted_at,
        current_at=arguments.current_at,
    )


def run(argv=None):
    try:
        arguments = _arguments(sys.argv[1:] if argv is None else argv)
        result = _execute(arguments)
        exit_code = EXIT_OK
    except StorageStop as error:
        result = _stopped(error.reason)
        exit_code = EXIT_STOPPED
    except Exception:
        result = _stopped("internal_error")
        exit_code = EXIT_STOPPED
    _print_json(result)
    return exit_code


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
