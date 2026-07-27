"""Windows Task Schedulerによる定期保全。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import os
import subprocess
import xml.etree.ElementTree as ElementTree
from pathlib import Path


TASK_NAME = "ReviewCompass3-SessionLogPreservation"
TASK_NAMESPACE = (
  "http://schemas.microsoft.com/windows/2004/02/mit/task"
)


class WindowsScheduleError(Exception):
  """所有していないWindowsタスク定義の操作を拒否する。"""


def _absolute_path(value):
  path = Path(value)
  if not path.is_absolute():
    raise WindowsScheduleError(
      "Unsafe Windows schedule inputs"
    )
  return path


def build_windows_task(
  *,
  definition_path,
  python_executable,
  config_path,
  interval_seconds,
):
  definition = _absolute_path(definition_path)
  if definition.suffix.lower() != ".xml":
    raise WindowsScheduleError(
      "Unsafe Windows schedule inputs"
    )
  python_path = _absolute_path(python_executable)
  config = _absolute_path(config_path)
  if (
    isinstance(interval_seconds, bool)
    or not isinstance(interval_seconds, int)
    or interval_seconds <= 0
  ):
    raise WindowsScheduleError(
      "Unsafe Windows schedule inputs"
    )
  for value in (python_path, config):
    if any(
      character in str(value)
      for character in ("\0", "\n", "\r")
    ):
      raise WindowsScheduleError(
        "Unsafe Windows schedule inputs"
      )
  ElementTree.register_namespace("", TASK_NAMESPACE)
  tag = lambda name: "{%s}%s" % (TASK_NAMESPACE, name)
  task = ElementTree.Element(tag("Task"), {"version": "1.4"})
  triggers = ElementTree.SubElement(task, tag("Triggers"))
  time_trigger = ElementTree.SubElement(
    triggers,
    tag("TimeTrigger"),
  )
  ElementTree.SubElement(
    time_trigger,
    tag("StartBoundary"),
  ).text = "2000-01-01T00:00:00"
  repetition = ElementTree.SubElement(
    time_trigger,
    tag("Repetition"),
  )
  ElementTree.SubElement(
    repetition,
    tag("Interval"),
  ).text = "PT%dS" % interval_seconds
  ElementTree.SubElement(
    repetition,
    tag("StopAtDurationEnd"),
  ).text = "false"
  ElementTree.SubElement(
    time_trigger,
    tag("Enabled"),
  ).text = "true"
  settings = ElementTree.SubElement(task, tag("Settings"))
  ElementTree.SubElement(
    settings,
    tag("StartWhenAvailable"),
  ).text = "true"
  ElementTree.SubElement(
    settings,
    tag("Enabled"),
  ).text = "true"
  actions = ElementTree.SubElement(
    task,
    tag("Actions"),
    {"Context": "Author"},
  )
  execute = ElementTree.SubElement(actions, tag("Exec"))
  ElementTree.SubElement(
    execute,
    tag("Command"),
  ).text = str(python_path)
  entry_path = Path(__file__).with_name("entry.py").resolve()
  ElementTree.SubElement(
    execute,
    tag("Arguments"),
  ).text = subprocess.list2cmdline([
    str(entry_path),
    "preserve",
    "--config",
    str(config),
  ])
  return ElementTree.tostring(
    task,
    encoding="utf-8",
    xml_declaration=True,
  )


def _expected(request):
  return build_windows_task(
    definition_path=request["definition_path"],
    python_executable=request["python_executable"],
    config_path=request["config_path"],
    interval_seconds=request["interval_seconds"],
  )


def _install(request):
  path = Path(request["definition_path"])
  expected = _expected(request)
  if path.exists():
    try:
      return (
        "unchanged"
        if path.read_bytes() == expected
        else "preserved"
      )
    except OSError as error:
      raise WindowsScheduleError(
        "Cannot inspect Windows task definition"
      ) from error
  temporary_path = path.with_name(path.name + ".tmp")
  try:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_bytes(expected)
    os.replace(temporary_path, path)
  except OSError as error:
    raise WindowsScheduleError(
      "Cannot install Windows task definition"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)
  return "installed"


def _validate_owned(request):
  path = Path(request["definition_path"])
  try:
    if (
      not path.is_file()
      or path.read_bytes() != _expected(request)
    ):
      raise WindowsScheduleError(
        "Unowned Windows task definition"
      )
  except OSError as error:
    raise WindowsScheduleError(
      "Cannot inspect Windows task definition"
    ) from error
  return path


def _schtasks(runner, *arguments):
  try:
    return runner(
      ["schtasks.exe", *arguments],
      capture_output=True,
      check=False,
      text=True,
    )
  except Exception as error:
    raise WindowsScheduleError(
      "Cannot execute schtasks"
    ) from error


def _is_registered(runner):
  return _schtasks(
    runner,
    "/Query",
    "/TN",
    TASK_NAME,
  ).returncode == 0


def _print_result(operation, action, status, reason=None):
  payload = {
    "action": action,
    "operation": operation,
    "status": status,
  }
  if reason is not None:
    payload["reason"] = reason
  print(json.dumps(payload, sort_keys=True))


def run(argv=None, *, runner=subprocess.run) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "operation",
    choices=(
      "install",
      "activate",
      "status",
      "deactivate",
      "uninstall",
    ),
  )
  parser.add_argument("--definition", required=True)
  parser.add_argument("--python", required=True)
  parser.add_argument("--config", required=True)
  parser.add_argument("--interval", required=True, type=int)
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args(argv)
  request = {
    "definition_path": args.definition,
    "python_executable": args.python,
    "config_path": args.config,
    "interval_seconds": args.interval,
  }
  try:
    _expected(request)
    if args.dry_run:
      _print_result(args.operation, "planned", "ok")
      return 0
    if args.operation == "install":
      action = _install(request)
      status = "error" if action == "preserved" else "ok"
    else:
      path = _validate_owned(request)
      if args.operation == "status":
        action = "inspected"
        status = (
          "running"
          if _is_registered(runner)
          else "stopped"
        )
      elif args.operation == "activate":
        if _is_registered(runner):
          action = "unchanged"
          status = "running"
        else:
          result = _schtasks(
            runner,
            "/Create",
            "/TN",
            TASK_NAME,
            "/XML",
            str(path),
            "/F",
          )
          action = "activated" if result.returncode == 0 else "failed"
          status = "running" if result.returncode == 0 else "stopped"
      elif args.operation == "deactivate":
        if not _is_registered(runner):
          action = "unchanged"
          status = "stopped"
        else:
          result = _schtasks(
            runner,
            "/Delete",
            "/TN",
            TASK_NAME,
            "/F",
          )
          action = "deactivated" if result.returncode == 0 else "failed"
          status = "stopped" if result.returncode == 0 else "running"
      else:
        path.unlink()
        action = "uninstalled"
        status = "ok"
  except Exception as error:
    _print_result(
      args.operation,
      "failed",
      "error",
      type(error).__name__,
    )
    return 5
  _print_result(args.operation, action, status)
  return 5 if action in ("failed", "preserved") else 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
