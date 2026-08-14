"""一件のSession記録を安全な項目だけで返す製品入口。

lifecycle: stable
normative_status: normative
promotion_required: false
"""

import argparse
import json
import re
import sys
from importlib import metadata
from pathlib import Path

from tools.session_logs.parse_claude import ParseError
from tools.session_logs.pipeline import prepare_artifact
from tools.session_logs.redaction import (
    SensitiveDataRemaining,
    default_pattern_rules,
)
from tools.session_logs.source_adapter import UnsupportedSourceKind


EXIT_OK = 0
EXIT_PARTIAL = 3
EXIT_STOPPED = 4

_POSIX_ABSOLUTE_PATH = re.compile(
    r"(?<![A-Za-z0-9._~:/-])/(?:[^/\s\"'<>]+/)*[^/\s\"'<>]+"
)
_WINDOWS_ABSOLUTE_PATH = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]|\\\\)[^\s\"'<>]+"
)


class EntryStop(Exception):
    """入力または安全境界により成功結果を返せない。"""

    def __init__(self, reason):
        self.reason = reason
        super().__init__(reason)


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


def _resolve_source(raw_root, raw_log):
    root_argument = Path(raw_root)
    log_argument = Path(raw_log)
    if not root_argument.is_absolute() or not log_argument.is_absolute():
        raise EntryStop("invalid_path")
    try:
        root = root_argument.resolve(strict=True)
        log = log_argument.resolve(strict=True)
    except OSError as error:
        raise EntryStop("unreadable_source") from error
    if not root.is_dir() or not log.is_file():
        raise EntryStop("unreadable_source")
    try:
        log.relative_to(root)
    except ValueError as error:
        raise EntryStop("source_outside_root") from error
    return root, log


def _safe_provenance(record):
    return {
        "end_line": record.end_line,
        "redaction_rules_sha256": record.redaction_rules_sha256,
        "source_path": record.source_path,
        "source_sha256": record.source_sha256,
        "start_line": record.start_line,
        "summary_changed_files": list(record.summary_changed_files),
        "summary_commits": list(record.summary_commits),
        "summary_sha256": record.summary_sha256,
        "tool_version": record.tool_version,
        "transcript_sha256": record.transcript_sha256,
    }


def _safe_findings(findings):
    return [
        {"count": finding.count, "label": finding.label}
        for finding in findings
    ]


def _safe_parse_issues(issues):
    return [
        {
            "block_index": issue.block_index,
            "kind": issue.kind,
            "line_no": issue.line_no,
        }
        for issue in issues
    ]


def _contains_absolute_path(value):
    if isinstance(value, str):
        return bool(
            _POSIX_ABSOLUTE_PATH.search(value)
            or _WINDOWS_ABSOLUTE_PATH.search(value)
        )
    if isinstance(value, dict):
        return any(
            _contains_absolute_path(key) or _contains_absolute_path(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return any(_contains_absolute_path(item) for item in value)
    return False


def _safe_result(artifact):
    parse_issues = _safe_parse_issues(artifact.parse_issues)
    result = {
        "external_send_approved": False,
        "parse_issues": parse_issues,
        "provenance": _safe_provenance(artifact.provenance),
        "redaction_findings": _safe_findings(
            artifact.redaction_findings
        ),
        "source_kind": artifact.source_kind,
        "status": "partial" if parse_issues else "ok",
        "summary": artifact.summary_text,
        "summary_redaction_findings": _safe_findings(
            artifact.summary_redaction_findings
        ),
        "transcript": artifact.text,
    }
    if _contains_absolute_path(result):
        raise EntryStop("absolute_path_remaining")
    return result


def _arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", required=True)
    parser.add_argument("--raw-log", required=True)
    return parser.parse_args(argv)


def run(argv=None):
    arguments = _arguments(sys.argv[1:] if argv is None else argv)
    try:
        raw_root, raw_log = _resolve_source(
            arguments.raw_root,
            arguments.raw_log,
        )
        artifact = prepare_artifact(
            raw_log,
            raw_root=raw_root,
            rules=default_pattern_rules(),
            tool_version=metadata.version("reviewcompass3"),
        )
        result = _safe_result(artifact)
    except EntryStop as error:
        _print_json(_stopped(error.reason))
        return EXIT_STOPPED
    except SensitiveDataRemaining:
        _print_json(_stopped("sensitive_data_remaining"))
        return EXIT_STOPPED
    except UnsupportedSourceKind:
        _print_json(_stopped("unsupported_source"))
        return EXIT_STOPPED
    except (OSError, ParseError, UnicodeError):
        _print_json(_stopped("unreadable_source"))
        return EXIT_STOPPED
    except Exception:
        _print_json(_stopped("internal_error"))
        return EXIT_STOPPED

    _print_json(result)
    return EXIT_PARTIAL if result["status"] == "partial" else EXIT_OK


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
