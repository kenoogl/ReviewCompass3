"""セッション開始・終了時に呼び出す安全な入口。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import shlex

from tools.session_logs.cli import run as run_cli


@dataclasses.dataclass(frozen=True)
class HookResult:
  action: str
  exit_code: int


@dataclasses.dataclass(frozen=True)
class HookCommands:
  start: str
  end: str


def build_hook_commands(python_executable, config_path) -> HookCommands:
  base = [
    str(python_executable),
    "-m",
    "tools.session_logs.hooks",
  ]
  config_arguments = ["--config", str(config_path)]
  return HookCommands(
    start=shlex.join(base + ["start"] + config_arguments),
    end=shlex.join(base + ["end"] + config_arguments),
  )


def run_start_hook(config_path, *, enabled=True) -> HookResult:
  if not enabled or config_path is None:
    return HookResult(action="skipped", exit_code=0)
  exit_code = run_cli((
    "--config",
    str(config_path),
    "--dry-run",
  ))
  return HookResult(action="checked", exit_code=exit_code)


def run_end_hook(config_path, *, enabled=True) -> HookResult:
  if not enabled or config_path is None:
    return HookResult(action="skipped", exit_code=0)
  exit_code = run_cli(("--config", str(config_path)))
  return HookResult(action="stored", exit_code=exit_code)


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("phase", choices=("start", "end"))
  parser.add_argument("--config", required=True)
  args = parser.parse_args(argv)
  if args.phase == "start":
    return run_start_hook(args.config).exit_code
  return run_end_hook(args.config).exit_code


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
