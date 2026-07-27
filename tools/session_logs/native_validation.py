"""ネイティブ環境で配布境界を値なし検証する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import importlib
import json
import os
import sys
from pathlib import Path


class NativeValidationError(Exception):
  """ネイティブ配布検証を安全に完了できない。"""


def _platform_family():
  if sys.platform == "darwin":
    return "macos"
  if sys.platform.startswith("linux"):
    return "linux"
  if sys.platform == "win32":
    return "windows"
  raise NativeValidationError("Unsupported native platform")


def validate_installed_package():
  if sys.version_info < (3, 9):
    raise NativeValidationError("Unsupported Python version")
  try:
    entry = importlib.import_module("tools.session_logs.entry")
  except ImportError as error:
    raise NativeValidationError(
      "Installed entry is unavailable"
    ) from error
  if not callable(getattr(entry, "run", None)):
    raise NativeValidationError(
      "Installed entry is unavailable"
    )
  return {
    "check": "package",
    "entry_importable": True,
    "platform": _platform_family(),
    "python_supported": True,
    "status": "passed",
  }


def _write_evidence(path, payload):
  evidence_path = Path(path)
  if not evidence_path.is_absolute():
    raise NativeValidationError(
      "Native evidence path must be absolute"
    )
  temporary_path = evidence_path.with_name(
    evidence_path.name + ".tmp"
  )
  try:
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_text(
      json.dumps(payload, indent=2, sort_keys=True) + "\n",
      encoding="utf-8",
    )
    os.replace(temporary_path, evidence_path)
  except OSError as error:
    raise NativeValidationError(
      "Cannot write native evidence"
    ) from error
  finally:
    temporary_path.unlink(missing_ok=True)


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--check",
    required=True,
    choices=("package",),
  )
  parser.add_argument("--evidence", required=True)
  args = parser.parse_args(argv)
  try:
    result = validate_installed_package()
    _write_evidence(args.evidence, result)
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "failed",
    }, sort_keys=True))
    return 5
  print(json.dumps(result, sort_keys=True))
  return 0


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
