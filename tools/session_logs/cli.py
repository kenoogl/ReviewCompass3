"""セッションログ基盤の暫定CLI。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
from pathlib import Path

from tools.session_logs.config import load_config
from tools.session_logs.discovery import discover_raw_logs
from tools.session_logs.pipeline import (
  UnsupportedSourceKind,
  prepare_artifact,
)
from tools.session_logs.redaction import (
  SensitiveDataRemaining,
  write_sensitive_report,
)
from tools.session_logs.storage import store_artifact


EXIT_OK = 0
EXIT_SENSITIVE_DATA = 2
EXIT_NO_TARGETS = 3
EXIT_UNSUPPORTED = 4
EXIT_FAILED = 5


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--config", required=True)
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args(argv)
  try:
    config = load_config(args.config)
    relative_paths = discover_raw_logs(config.raw_root)
  except Exception:
    return EXIT_FAILED

  if not relative_paths:
    return EXIT_NO_TARGETS

  exit_value = EXIT_OK

  for relative_path in relative_paths:
    raw_log = config.raw_root / relative_path
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
