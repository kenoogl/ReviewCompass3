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
from tools.session_logs.preservation import preserve_raw_log
from tools.session_logs.provenance import Provenance
from tools.session_logs.redaction import (
  SensitiveDataRemaining,
  write_sensitive_report,
)
from tools.session_logs.regeneration import (
  RegenerationError,
  regenerate_transcript,
)
from tools.session_logs.storage import store_artifact


EXIT_OK = 0
EXIT_SENSITIVE_DATA = 2
EXIT_NO_TARGETS = 3
EXIT_UNSUPPORTED = 4
EXIT_FAILED = 5
EXIT_PRESERVATION_FAILED = 6
EXIT_VERIFICATION_MISMATCH = 7
EXIT_REGENERATION_FAILED = 8


def _print_json(payload):
  print(json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
  ))


def _verify_saved_artifact(relative_path, config) -> int:
  source_path = Path(relative_path)
  transcript_path = (
    config.transcript_root / source_path.with_suffix(".md")
  )
  provenance_path = (
    config.provenance_root / source_path.with_suffix(".json")
  )
  try:
    state = json.loads(provenance_path.read_text(encoding="utf-8"))
    record = Provenance(**state["provenance"])
    stored_text = transcript_path.read_text(encoding="utf-8")
    result = regenerate_transcript(
      record,
      raw_root=config.raw_root,
      stored_text=stored_text,
      rules=config.redaction_rules,
      allow_patterns=config.allow_patterns,
      tool_version=config.tool_version,
    )
  except RegenerationError as error:
    _print_json({
      "source_path": source_path.as_posix(),
      "status": "regeneration_failed",
      "reason": error.reason,
    })
    return EXIT_REGENERATION_FAILED
  except Exception as error:
    _print_json({
      "source_path": source_path.as_posix(),
      "status": "regeneration_failed",
      "reason": type(error).__name__,
    })
    return EXIT_REGENERATION_FAILED

  _print_json({
    "source_path": source_path.as_posix(),
    "status": result.status,
    "source_matches": result.source_matches,
    "provenance_matches": result.provenance_matches,
    "stored_matches": result.stored_matches,
    "rules_match": result.rules_match,
    "tool_version_matches": result.tool_version_matches,
  })
  return (
    EXIT_OK
    if result.status == "matches"
    else EXIT_VERIFICATION_MISMATCH
  )


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--config", required=True)
  mode = parser.add_mutually_exclusive_group()
  mode.add_argument("--dry-run", action="store_true")
  mode.add_argument("--verify", action="store_true")
  mode.add_argument("--preserve-only", action="store_true")
  args = parser.parse_args(argv)
  try:
    config = load_config(args.config)
    relative_paths = discover_raw_logs(config.raw_root)
  except Exception:
    return EXIT_FAILED

  if not relative_paths:
    return EXIT_NO_TARGETS

  if args.verify:
    return max(
      _verify_saved_artifact(relative_path, config)
      for relative_path in relative_paths
    )

  if args.preserve_only:
    if (
      not config.preservation_enabled
      or config.backup_root is None
    ):
      return EXIT_FAILED
    exit_value = EXIT_OK
    for relative_path in relative_paths:
      try:
        preserve_raw_log(
          config.raw_root / relative_path,
          raw_root=config.raw_root,
          backup_root=config.backup_root,
        )
      except Exception:
        exit_value = max(
          exit_value,
          EXIT_PRESERVATION_FAILED,
        )
    return exit_value

  exit_value = EXIT_OK

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
        )
      except Exception:
        exit_value = max(
          exit_value,
          EXIT_PRESERVATION_FAILED,
        )
    try:
      artifact = prepare_artifact(
        raw_log,
        raw_root=config.raw_root,
        rules=config.redaction_rules,
        tool_version=config.tool_version,
        allow_patterns=config.allow_patterns,
      )
    except UnsupportedSourceKind:
      exit_value = max(exit_value, EXIT_UNSUPPORTED)
      continue
    except SensitiveDataRemaining as error:
      exit_value = max(exit_value, EXIT_SENSITIVE_DATA)
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
    except Exception:
      exit_value = max(exit_value, EXIT_FAILED)
      continue

    if args.dry_run:
      print("planned %s" % Path(relative_path).as_posix())
      continue

    try:
      store_artifact(
        artifact,
        transcript_root=config.transcript_root,
        summary_root=config.summary_root,
        provenance_root=config.provenance_root,
      )
    except Exception:
      exit_value = max(exit_value, EXIT_FAILED)

  return exit_value


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
