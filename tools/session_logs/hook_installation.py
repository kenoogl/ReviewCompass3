"""Claude Code設定へのフック導入と解除。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
import os
from pathlib import Path

from tools.session_logs.config import load_config
from tools.session_logs.hooks import build_hook_commands


class HookInstallationError(Exception):
  """フック設定を安全に更新できない。"""


@dataclasses.dataclass(frozen=True)
class HookInstallationResult:
  action: str
  settings_path: Path


def _load_settings(path):
  settings_path = Path(path)
  if not settings_path.exists():
    return {}
  try:
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    raise HookInstallationError("Cannot read hook settings") from error
  if not isinstance(settings, dict):
    raise HookInstallationError("Hook settings must be an object")
  return settings


def _write_settings(path, settings):
  settings_path = Path(path)
  temporary_path = settings_path.with_name(
    settings_path.name + ".tmp"
  )
  try:
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_text(
      json.dumps(
        settings,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
      ) + "\n",
      encoding="utf-8",
    )
    os.replace(temporary_path, settings_path)
  except OSError as error:
    raise HookInstallationError("Cannot write hook settings") from error
  finally:
    temporary_path.unlink(missing_ok=True)


def _event_groups(settings, event):
  hooks = settings.setdefault("hooks", {})
  if not isinstance(hooks, dict):
    raise HookInstallationError("hooks must be an object")
  groups = hooks.setdefault(event, [])
  if not isinstance(groups, list):
    raise HookInstallationError("%s hooks must be a list" % event)
  return groups


def _install_handler(settings, event, command, *, matcher=None) -> bool:
  groups = _event_groups(settings, event)
  group = next((
    item
    for item in groups
    if (
      isinstance(item, dict)
      and item.get("matcher") == matcher
      and ("matcher" in item) == (matcher is not None)
    )
  ), None)
  if group is None:
    group = {"hooks": []}
    if matcher is not None:
      group["matcher"] = matcher
    groups.append(group)
  handlers = group.get("hooks")
  if not isinstance(handlers, list):
    raise HookInstallationError("%s handlers must be a list" % event)
  handler = {
    "type": "command",
    "command": command,
  }
  if handler in handlers:
    return False
  handlers.append(handler)
  return True


def install_claude_hooks(
  settings_path,
  *,
  start_command,
  end_command,
) -> HookInstallationResult:
  path = Path(settings_path)
  settings = _load_settings(path)
  changed = _install_handler(
    settings,
    "SessionStart",
    start_command,
    matcher="startup|resume",
  )
  changed = _install_handler(
    settings,
    "SessionEnd",
    end_command,
  ) or changed
  if changed:
    _write_settings(path, settings)
  return HookInstallationResult(
    action="installed" if changed else "unchanged",
    settings_path=path,
  )


def install_configured_claude_hooks(
  settings_path,
  *,
  python_executable,
  config_path,
) -> HookInstallationResult:
  try:
    config = load_config(config_path)
  except Exception as error:
    raise HookInstallationError(
      "Cannot load configured hooks"
    ) from error
  if config.hook_event_log_path is None:
    raise HookInstallationError(
      "Hook observation path is not configured"
    )
  commands = build_hook_commands(
    python_executable,
    config_path,
    event_log_path=config.hook_event_log_path,
  )
  return install_claude_hooks(
    settings_path,
    start_command=commands.start,
    end_command=commands.end,
  )


def _remove_handler(settings, event, command) -> bool:
  hooks = settings.get("hooks")
  if not isinstance(hooks, dict):
    return False
  groups = hooks.get(event)
  if not isinstance(groups, list):
    return False
  handler = {
    "type": "command",
    "command": command,
  }
  changed = False
  kept_groups = []
  for group in groups:
    if not isinstance(group, dict):
      kept_groups.append(group)
      continue
    handlers = group.get("hooks")
    if not isinstance(handlers, list):
      kept_groups.append(group)
      continue
    kept_handlers = [
      item
      for item in handlers
      if item != handler
    ]
    if len(kept_handlers) != len(handlers):
      changed = True
    if kept_handlers:
      copied = dict(group)
      copied["hooks"] = kept_handlers
      kept_groups.append(copied)
  if kept_groups:
    hooks[event] = kept_groups
  else:
    hooks.pop(event, None)
  if not hooks:
    settings.pop("hooks", None)
  return changed


def uninstall_claude_hooks(
  settings_path,
  *,
  start_command,
  end_command,
) -> HookInstallationResult:
  path = Path(settings_path)
  if not path.exists():
    return HookInstallationResult(
      action="unchanged",
      settings_path=path,
    )
  settings = _load_settings(path)
  changed = _remove_handler(settings, "SessionStart", start_command)
  changed = _remove_handler(
    settings,
    "SessionEnd",
    end_command,
  ) or changed
  if changed:
    _write_settings(path, settings)
  return HookInstallationResult(
    action="uninstalled" if changed else "unchanged",
    settings_path=path,
  )
