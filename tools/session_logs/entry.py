"""cwdに依存しないセッションログ固定実行入口。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import importlib
import importlib.util
import sys
from pathlib import Path


def _load_roots():
  # file直接起動（hook・scheduler）ではpackage importが未確立のため、兄弟package
  # 位置のroots.pyをfile位置から読み込む。root深度の知識はroots.py側だけが持つ。
  location = Path(__file__).resolve().parent.parent / "common" / "roots.py"
  specification = importlib.util.spec_from_file_location(
    "_session_log_entry_roots", location
  )
  module = importlib.util.module_from_spec(specification)
  specification.loader.exec_module(module)
  return module


PROJECT_ROOT = _load_roots().repo_root()


def _load_module(name):
  root = str(PROJECT_ROOT)
  if root not in sys.path:
    sys.path.insert(0, root)
  return importlib.import_module(name)


def run(argv=None) -> int:
  arguments = list(sys.argv[1:] if argv is None else argv)
  if arguments and arguments[0] == "schedule":
    scheduler = _load_module("tools.session_logs.scheduler")
    return scheduler.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "validate-private":
    validation = _load_module(
      "tools.session_logs.private_validation"
    )
    return validation.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "audit-stage-zero":
    gate = _load_module("tools.session_logs.stage_gate")
    return gate.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "preflight":
    preflight = _load_module(
      "tools.session_logs.deployment_preflight"
    )
    return preflight.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "init-config":
    portable = _load_module(
      "tools.session_logs.portable_config"
    )
    return portable.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "deployment":
    lifecycle = _load_module(
      "tools.session_logs.deployment_lifecycle"
    )
    return lifecycle.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "validate-distribution":
    validation = _load_module(
      "tools.session_logs.distribution_validation"
    )
    return validation.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "validate-native":
    validation = _load_module(
      "tools.session_logs.native_validation"
    )
    return validation.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "aggregate-native-evidence":
    evidence = _load_module(
      "tools.session_logs.native_evidence"
    )
    return evidence.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "prepare-deployment-approval":
    approval = _load_module(
      "tools.session_logs.limited_approval"
    )
    return approval.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "limited-deployment":
    deployment = _load_module(
      "tools.session_logs.limited_deployment"
    )
    return deployment.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "collect-eventual":
    collection = _load_module(
      "tools.session_logs.eventual_preservation"
    )
    return collection.run(tuple(arguments[1:]))
  if arguments and arguments[0] == "record-run":
    record_run = _load_module("tools.session_logs.record_run")
    return record_run.run(tuple(arguments[1:]))
  parser = argparse.ArgumentParser()
  subcommands = parser.add_subparsers(dest="command", required=True)
  hook_parser = subcommands.add_parser("hook")
  hook_parser.add_argument("phase", choices=("start", "end"))
  hook_parser.add_argument("--config", required=True)
  hook_parser.add_argument("--event-log")
  preserve_parser = subcommands.add_parser("preserve")
  preserve_parser.add_argument("--config", required=True)
  args = parser.parse_args(arguments)

  if args.command == "hook":
    hooks = _load_module("tools.session_logs.hooks")
    hook_arguments = [
      args.phase,
      "--config",
      args.config,
    ]
    if args.event_log is not None:
      hook_arguments.extend([
        "--event-log",
        args.event_log,
      ])
    return hooks.run(tuple(hook_arguments))

  cli = _load_module("tools.session_logs.cli")
  return cli.run((
    "--config",
    args.config,
    "--preserve-only",
    "--json-lines",
  ))


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
