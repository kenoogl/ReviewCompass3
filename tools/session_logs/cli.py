"""セッションログ基盤の暫定CLI。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse

from tools.session_logs.config import load_config
from tools.session_logs.discovery import discover_raw_logs
from tools.session_logs.pipeline import prepare_artifact
from tools.session_logs.storage import store_artifact


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--config", required=True)
  args = parser.parse_args(argv)
  config = load_config(args.config)

  for relative_path in discover_raw_logs(config.raw_root):
    raw_log = config.raw_root / relative_path
    artifact = prepare_artifact(
      raw_log,
      raw_root=config.raw_root,
      rules=config.redaction_rules,
      tool_version=config.tool_version,
    )
    store_artifact(
      artifact,
      transcript_root=config.transcript_root,
      summary_root=config.summary_root,
      provenance_root=config.provenance_root,
    )
  return 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
