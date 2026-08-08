"""セッションログ基盤の暫定CLI。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
from pathlib import Path

from tools.session_logs.config import load_config
from tools.session_logs.discovery import discover_raw_logs
from tools.session_logs.pipeline import (
  UnsupportedSourceKind,
  prepare_artifact,
)
from tools.session_logs.preservation import (
  PreservationIntegrityError,
  preserve_raw_log,
  restore_raw_log,
)
from tools.session_logs.provenance import Provenance
from tools.session_logs.redaction import (
  SensitiveDataRemaining,
  write_sensitive_report,
)
from tools.session_logs.regeneration import (
  RegenerationError,
  regenerate_artifact,
)
from tools.session_logs.repository_context import (
  collect_repository_context,
)
from tools.session_logs.source_kind import identify_auxiliary_kind
from tools.session_logs.storage import store_artifact


EXIT_OK = 0
EXIT_SENSITIVE_DATA = 2
EXIT_NO_TARGETS = 3
EXIT_UNSUPPORTED = 4
EXIT_FAILED = 5
EXIT_PRESERVATION_FAILED = 6
EXIT_VERIFICATION_MISMATCH = 7
EXIT_REGENERATION_FAILED = 8
EXIT_RESTORE_PRESERVED = 9
EXIT_RESTORE_INTEGRITY_FAILED = 10


from tools.common.output import print_json as _print_json


class _JsonLinesReporter:
  def __init__(self, mode, *, enabled):
    self.mode = mode
    self.enabled = enabled
    self.counts = {
      "failed": 0,
      "preserved": 0,
      "succeeded": 0,
    }

  def result(
    self,
    source_path,
    *,
    action,
    status="ok",
    reason=None,
  ):
    if status == "error":
      self.counts["failed"] += 1
    elif action == "preserved":
      self.counts["preserved"] += 1
    else:
      self.counts["succeeded"] += 1
    if not self.enabled:
      return
    payload = {
      "action": action,
      "kind": "result",
      "mode": self.mode,
      "source_path": Path(source_path).as_posix(),
      "status": status,
    }
    if reason is not None:
      payload["reason"] = reason
    _print_json(payload)

  def finish(self):
    if not self.enabled:
      return
    successful = (
      self.counts["succeeded"]
      + self.counts["preserved"]
    )
    if self.counts["failed"] and successful:
      status = "partial"
    elif self.counts["failed"]:
      status = "error"
    else:
      status = "ok"
    _print_json({
      "counts": self.counts,
      "kind": "summary",
      "mode": self.mode,
      "status": status,
    })


def _verify_saved_artifact(relative_path, config, reporter=None) -> int:
  source_path = Path(relative_path)
  transcript_path = (
    config.transcript_root / source_path.with_suffix(".md")
  )
  provenance_path = (
    config.provenance_root / source_path.with_suffix(".json")
  )
  summary_path = (
    config.summary_root / source_path.with_suffix(".md")
  )
  try:
    state = json.loads(provenance_path.read_text(encoding="utf-8"))
    record = Provenance(**state["provenance"])
    stored_text = transcript_path.read_text(encoding="utf-8")
    stored_summary = summary_path.read_text(encoding="utf-8")
    result = regenerate_artifact(
      record,
      raw_root=config.raw_root,
      stored_text=stored_text,
      stored_summary=stored_summary,
      rules=config.redaction_rules,
      allow_patterns=config.allow_patterns,
      tool_version=config.tool_version,
    )
  except RegenerationError as error:
    if reporter is None:
      _print_json({
        "source_path": source_path.as_posix(),
        "status": "regeneration_failed",
        "reason": error.reason,
      })
    else:
      reporter.result(
        source_path,
        action="regeneration_failed",
        status="error",
        reason=error.reason,
      )
    return EXIT_REGENERATION_FAILED
  except Exception as error:
    if reporter is None:
      _print_json({
        "source_path": source_path.as_posix(),
        "status": "regeneration_failed",
        "reason": type(error).__name__,
      })
    else:
      reporter.result(
        source_path,
        action="regeneration_failed",
        status="error",
        reason=type(error).__name__,
      )
    return EXIT_REGENERATION_FAILED

  if reporter is None:
    _print_json({
      "source_path": source_path.as_posix(),
      "status": result.status,
      "source_matches": result.source_matches,
      "provenance_matches": result.provenance_matches,
      "stored_matches": result.stored_matches,
      "summary_provenance_matches": (
        result.summary_provenance_matches
      ),
      "summary_stored_matches": result.summary_stored_matches,
      "rules_match": result.rules_match,
      "tool_version_matches": result.tool_version_matches,
    })
  else:
    reporter.result(
      source_path,
      action=result.status,
      status=(
        "ok"
        if result.status == "matches"
        else "error"
      ),
    )
  return (
    EXIT_OK
    if result.status == "matches"
    else EXIT_VERIFICATION_MISMATCH
  )


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--config", required=True)
  parser.add_argument("--json-lines", action="store_true")
  mode = parser.add_mutually_exclusive_group()
  mode.add_argument("--dry-run", action="store_true")
  mode.add_argument("--verify", action="store_true")
  mode.add_argument("--preserve-only", action="store_true")
  mode.add_argument("--list-backups", action="store_true")
  mode.add_argument("--restore")
  args = parser.parse_args(argv)
  try:
    config = load_config(args.config)
  except Exception:
    return EXIT_FAILED

  if args.list_backups:
    if config.backup_root is None:
      return EXIT_FAILED
    try:
      backup_paths = discover_raw_logs(config.backup_root)
    except Exception:
      return EXIT_FAILED
    if not backup_paths:
      return EXIT_NO_TARGETS
    for backup_path in backup_paths:
      print(Path(backup_path).as_posix())
    return EXIT_OK

  if args.restore is not None:
    if config.backup_root is None:
      return EXIT_FAILED
    try:
      restored = restore_raw_log(
        args.restore,
        raw_root=config.raw_root,
        backup_root=config.backup_root,
        ledger_path=config.preservation_ledger_path,
      )
    except PreservationIntegrityError:
      return EXIT_RESTORE_INTEGRITY_FAILED
    except Exception:
      return EXIT_FAILED
    return (
      EXIT_RESTORE_PRESERVED
      if restored.action == "preserved"
      else EXIT_OK
    )

  try:
    relative_paths = discover_raw_logs(config.raw_root)
  except Exception:
    return EXIT_FAILED

  if not relative_paths:
    return EXIT_NO_TARGETS

  if args.verify:
    reporter = _JsonLinesReporter(
      "verify",
      enabled=args.json_lines,
    )
    exit_value = max(
      _verify_saved_artifact(
        relative_path,
        config,
        reporter=reporter if args.json_lines else None,
      )
      for relative_path in relative_paths
    )
    reporter.finish()
    return exit_value

  if args.preserve_only:
    if (
      not config.preservation_enabled
      or config.backup_root is None
    ):
      return EXIT_FAILED
    reporter = _JsonLinesReporter(
      "preserve",
      enabled=args.json_lines,
    )
    exit_value = EXIT_OK
    for relative_path in relative_paths:
      try:
        result = preserve_raw_log(
          config.raw_root / relative_path,
          raw_root=config.raw_root,
          backup_root=config.backup_root,
          ledger_path=config.preservation_ledger_path,
        )
      except Exception as error:
        exit_value = max(
          exit_value,
          EXIT_PRESERVATION_FAILED,
        )
        reporter.result(
          relative_path,
          action="preservation_failed",
          status="error",
          reason=type(error).__name__,
        )
      else:
        reporter.result(
          relative_path,
          action=result.action,
        )
    reporter.finish()
    return exit_value

  reporter = _JsonLinesReporter(
    "dry-run" if args.dry_run else "process",
    enabled=args.json_lines,
  )
  exit_value = EXIT_OK
  commits = ()
  changed_files = ()
  if config.summary_revision_range is not None:
    if config.repository_root is None:
      return EXIT_FAILED
    try:
      repository_context = collect_repository_context(
        config.repository_root,
        config.summary_revision_range,
        rules=config.redaction_rules,
        allow_patterns=config.allow_patterns,
      )
    except SensitiveDataRemaining:
      return EXIT_SENSITIVE_DATA
    except Exception:
      return EXIT_FAILED
    commits = repository_context.commits
    changed_files = repository_context.changed_files

  for relative_path in relative_paths:
    raw_log = config.raw_root / relative_path
    if (
      not args.dry_run
      and config.preservation_enabled
      and config.backup_root is not None
    ):
      try:
        preserve_raw_log(
          raw_log,
          raw_root=config.raw_root,
          backup_root=config.backup_root,
          ledger_path=config.preservation_ledger_path,
        )
      except Exception as error:
        exit_value = max(
          exit_value,
          EXIT_PRESERVATION_FAILED,
        )
        reporter.result(
          relative_path,
          action="preservation_failed",
          status="error",
          reason=type(error).__name__,
        )
    try:
      if identify_auxiliary_kind(raw_log) is not None:
        continue
      artifact = prepare_artifact(
        raw_log,
        raw_root=config.raw_root,
        rules=config.redaction_rules,
        tool_version=config.tool_version,
        allow_patterns=config.allow_patterns,
        commits=commits,
        changed_files=changed_files,
      )
    except UnsupportedSourceKind as error:
      exit_value = max(exit_value, EXIT_UNSUPPORTED)
      reporter.result(
        relative_path,
        action="unsupported",
        status="error",
        reason=type(error).__name__,
      )
      continue
    except SensitiveDataRemaining as error:
      exit_value = max(exit_value, EXIT_SENSITIVE_DATA)
      reporter.result(
        relative_path,
        action="sensitive_data",
        status="error",
        reason=type(error).__name__,
      )
      if (
        not args.dry_run
        and config.sensitive_report_root is not None
      ):
        relative_report_path = Path(relative_path).with_suffix(".json")
        report_path = (
          config.sensitive_report_root
          / relative_report_path
        )
        write_sensitive_report(
          report_path,
          error,
          source_path=Path(relative_path).as_posix(),
        )
      continue
    except Exception as error:
      exit_value = max(exit_value, EXIT_FAILED)
      reporter.result(
        relative_path,
        action="failed",
        status="error",
        reason=type(error).__name__,
      )
      continue

    if args.dry_run:
      if args.json_lines:
        reporter.result(relative_path, action="planned")
      else:
        print("planned %s" % Path(relative_path).as_posix())
      continue

    try:
      result = store_artifact(
        artifact,
        transcript_root=config.transcript_root,
        summary_root=config.summary_root,
        provenance_root=config.provenance_root,
      )
    except Exception as error:
      exit_value = max(exit_value, EXIT_FAILED)
      reporter.result(
        relative_path,
        action="failed",
        status="error",
        reason=type(error).__name__,
      )
    else:
      reporter.result(
        relative_path,
        action=result.action,
      )

  reporter.finish()
  return exit_value


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
