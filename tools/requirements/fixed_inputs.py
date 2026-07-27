"""第4段の固定入力照合。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


class FixedInputError(Exception):
  """固定入力契約そのものが不正である。"""


@dataclasses.dataclass(frozen=True)
class FixedInputEntry:
  path: str
  expected_sha256: str
  actual_sha256: object
  assertions: tuple


@dataclasses.dataclass(frozen=True)
class FixedInputMismatch:
  path: str
  kind: str
  pointer: object
  expected: object
  actual: object


@dataclasses.dataclass(frozen=True)
class FixedInputVerification:
  status: str
  entries: tuple
  mismatches: tuple
  digest: str


_DIGEST = re.compile(r"[0-9a-f]{64}")
_FIELDS = {"path", "sha256", "assertions"}
_ASSERTION_FIELDS = {"pointer", "expected"}


def _valid_relative_path(value):
  if (
    not isinstance(value, str)
    or not value
    or "\\" in value
  ):
    return False
  path = PurePosixPath(value)
  return (
    not path.is_absolute()
    and "." not in path.parts
    and ".." not in path.parts
  )


def _parse_pointer(pointer):
  if not isinstance(pointer, str) or not pointer.startswith("/"):
    raise FixedInputError(
      "assertion pointer must be an absolute JSON pointer"
    )
  return tuple(
    part.replace("~1", "/").replace("~0", "~")
    for part in pointer[1:].split("/")
  )


def _resolve_pointer(document, pointer):
  current = document
  for part in _parse_pointer(pointer):
    if isinstance(current, dict):
      current = current[part]
    elif isinstance(current, list):
      current = current[int(part)]
    else:
      raise KeyError(part)
  return current


def _parse_assertions(value):
  if not isinstance(value, (list, tuple)):
    raise FixedInputError(
      "assertions must be a sequence"
    )
  result = []
  pointers = []
  for assertion in value:
    if (
      not isinstance(assertion, dict)
      or set(assertion) != _ASSERTION_FIELDS
    ):
      raise FixedInputError(
        "assertions require pointer and expected"
      )
    _parse_pointer(assertion["pointer"])
    pointers.append(assertion["pointer"])
    result.append({
      "expected": assertion["expected"],
      "pointer": assertion["pointer"],
    })
  if len(set(pointers)) != len(pointers):
    raise FixedInputError(
      "assertion pointers must be unique"
    )
  return tuple(sorted(
    result,
    key=lambda item: item["pointer"],
  ))


def _parse_input(value):
  if (
    not isinstance(value, dict)
    or set(value) != _FIELDS
    or not _valid_relative_path(value["path"])
    or not isinstance(value["sha256"], str)
    or _DIGEST.fullmatch(value["sha256"]) is None
  ):
    raise FixedInputError(
      "fixed inputs require a safe path and SHA-256"
    )
  return {
    "assertions": _parse_assertions(value["assertions"]),
    "path": value["path"],
    "sha256": value["sha256"],
  }


def _mismatch(path, kind, *, pointer=None, expected=None, actual=None):
  return FixedInputMismatch(
    path=path,
    kind=kind,
    pointer=pointer,
    expected=expected,
    actual=actual,
  )


def verify_fixed_inputs(*, root, inputs):
  root_path = Path(root).resolve()
  parsed = tuple(_parse_input(value) for value in inputs)
  paths = tuple(value["path"] for value in parsed)
  if len(set(paths)) != len(paths):
    raise FixedInputError(
      "fixed input paths must be unique"
    )
  entries = []
  mismatches = []
  for value in sorted(parsed, key=lambda item: item["path"]):
    relative_path = value["path"]
    path = (root_path / relative_path).resolve()
    try:
      path.relative_to(root_path)
    except ValueError as error:
      raise FixedInputError(
        "fixed input resolved outside root"
      ) from error
    if not path.is_file():
      entries.append(FixedInputEntry(
        path=relative_path,
        expected_sha256=value["sha256"],
        actual_sha256=None,
        assertions=value["assertions"],
      ))
      mismatches.append(_mismatch(
        relative_path,
        "missing",
        expected=value["sha256"],
      ))
      continue
    content = path.read_bytes()
    actual_digest = hashlib.sha256(content).hexdigest()
    entries.append(FixedInputEntry(
      path=relative_path,
      expected_sha256=value["sha256"],
      actual_sha256=actual_digest,
      assertions=value["assertions"],
    ))
    if actual_digest != value["sha256"]:
      mismatches.append(_mismatch(
        relative_path,
        "sha256",
        expected=value["sha256"],
        actual=actual_digest,
      ))
      continue
    if not value["assertions"]:
      continue
    try:
      document = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError):
      mismatches.append(_mismatch(
        relative_path,
        "assertion",
        expected="valid JSON",
        actual="invalid JSON",
      ))
      continue
    for assertion in value["assertions"]:
      pointer = assertion["pointer"]
      try:
        actual = _resolve_pointer(document, pointer)
      except (KeyError, IndexError, TypeError, ValueError):
        actual = None
      if actual != assertion["expected"]:
        mismatches.append(_mismatch(
          relative_path,
          "assertion",
          pointer=pointer,
          expected=assertion["expected"],
          actual=actual,
        ))
  result_document = {
    "entries": [
      {
        "actual_sha256": entry.actual_sha256,
        "assertions": list(entry.assertions),
        "expected_sha256": entry.expected_sha256,
        "path": entry.path,
      }
      for entry in entries
    ],
    "mismatches": [
      dataclasses.asdict(mismatch)
      for mismatch in mismatches
    ],
    "schema_version": 1,
  }
  digest = hashlib.sha256(
    json.dumps(
      result_document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return FixedInputVerification(
    status="ready" if not mismatches else "stale",
    entries=tuple(entries),
    mismatches=tuple(mismatches),
    digest=digest,
  )
