"""セッション開始・終了時に呼び出す安全な入口。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses

from tools.session_logs.cli import run


@dataclasses.dataclass(frozen=True)
class HookResult:
  action: str
  exit_code: int


def run_start_hook(config_path, *, enabled=True) -> HookResult:
  if not enabled or config_path is None:
    return HookResult(action="skipped", exit_code=0)
  exit_code = run((
    "--config",
    str(config_path),
    "--dry-run",
  ))
  return HookResult(action="checked", exit_code=exit_code)


def run_end_hook(config_path, *, enabled=True) -> HookResult:
  if not enabled or config_path is None:
    return HookResult(action="skipped", exit_code=0)
  exit_code = run(("--config", str(config_path)))
  return HookResult(action="stored", exit_code=exit_code)
