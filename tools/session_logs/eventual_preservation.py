"""終了hookに依存しないsession logの継続回収と再照合。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import datetime
import hashlib
import json
import os
from pathlib import Path

from tools.session_logs.discovery import discover_raw_logs
from tools.session_logs.locking import LockError, LockHeld, exclusive_lock
from tools.session_logs.preservation import preserve_raw_log
from tools.session_logs.redaction import (
  redact_text_strict,
  redaction_rules_digest,
)
from tools.session_logs.source_adapter import (
  UnsupportedSourceKind,
  parse_source_bytes,
)
from tools.session_logs.transcript import render_transcript


class CollectionError(Exception):
  """値を表示せずsession log回収失敗を伝える。"""


class CollectionLocked(CollectionError):
  """同じsourceを別collectorが処理している。"""


class CursorIntegrityError(CollectionError):
  """durable cursorを安全に利用できない。"""


class UnsafeCollectionBoundary(CollectionError):
  """private出力またはsource境界が安全でない。"""


@dataclasses.dataclass(frozen=True)
class CollectionResult:
  action: str
  state: str
  source_kind: object
  source_id: str
  raw_path: Path
  verbatim_path: object
  redacted_path: object
  cursor_path: object
  provenance_path: object
  raw_size: int
  parsed_size: int
  event_count: int
  issue_count: int

  def report(self):
    return {
      "action": self.action,
      "event_count": self.event_count,
      "issue_count": self.issue_count,
      "source_id": self.source_id,
      "source_kind": self.source_kind,
      "state": self.state,
    }


@dataclasses.dataclass(frozen=True)
class ReconcileItem:
  action: str
  state: str
  source_kind: object
  source_id: str
  event_count: int = 0
  issue_count: int = 0
  reason: object = None

  def report(self):
    payload = {
      "action": self.action,
      "event_count": self.event_count,
      "issue_count": self.issue_count,
      "source_id": self.source_id,
      "source_kind": self.source_kind,
      "state": self.state,
    }
    if self.reason is not None:
      payload["reason"] = self.reason
    return payload


@dataclasses.dataclass(frozen=True)
class ReconcileResult:
  counts: dict
  items: tuple
  status: str

  def report(self):
    return {
      "counts": dict(self.counts),
      "items": [item.report() for item in self.items],
      "status": self.status,
    }


@dataclasses.dataclass(frozen=True)
class _Layout:
  namespace: str
  relative_path: Path
  raw_path: Path
  verbatim_path: Path
  redacted_path: Path
  cursor_path: Path
  provenance_path: Path
  ledger_path: Path
  lock_path: Path


def _within(path, root):
  target = Path(path).resolve()
  boundary = Path(root).resolve()
  return target == boundary or boundary in target.parents


def _validate_boundaries(
  source_path,
  source_root,
  private_root,
  repository_root,
):
  raw_source = Path(source_path)
  native_root = Path(source_root)
  private = Path(private_root)
  repository = Path(repository_root)
  if not all(
    value.is_absolute()
    for value in (raw_source, native_root, private, repository)
  ):
    raise UnsafeCollectionBoundary("Collection paths must be absolute")
  resolved_source = raw_source.resolve()
  resolved_native = native_root.resolve()
  resolved_private = private.resolve()
  resolved_repository = repository.resolve()
  if (
    not (resolved_repository / ".git").exists()
    or not _within(resolved_source, resolved_native)
    or _within(resolved_private, resolved_repository)
    or _within(resolved_private, resolved_native)
    or _within(resolved_native, resolved_private)
    or private.is_symlink()
  ):
    raise UnsafeCollectionBoundary("Unsafe session collection boundary")
  if (
    not resolved_source.is_file()
    or raw_source.is_symlink()
  ):
    raise UnsafeCollectionBoundary("Unsafe session source")
  try:
    relative_path = resolved_source.relative_to(resolved_native)
  except ValueError as error:
    raise UnsafeCollectionBoundary(
      "Unsafe session source boundary"
    ) from error
  return (
    resolved_source,
    resolved_native,
    resolved_private,
    relative_path,
  )


def _secure_parent_chain(path, private_root):
  private = Path(private_root)
  target = Path(path)
  try:
    private.mkdir(parents=True, exist_ok=True, mode=0o700)
    private.chmod(0o700)
    parents = []
    current = target.parent
    while current != private:
      if not _within(current, private):
        raise UnsafeCollectionBoundary("Unsafe private artifact path")
      parents.append(current)
      current = current.parent
    for directory in reversed(parents):
      directory.mkdir(exist_ok=True, mode=0o700)
      directory.chmod(0o700)
  except OSError as error:
    raise CollectionError("Cannot secure private directories") from error


def _secure_file(path, private_root):
  target = Path(path)
  _secure_parent_chain(target, private_root)
  if not target.exists():
    return
  try:
    if target.is_symlink() or not target.is_file():
      raise UnsafeCollectionBoundary("Unsafe private artifact")
    target.chmod(0o600)
  except OSError as error:
    raise CollectionError("Cannot secure private artifact") from error


def _namespace(source_root):
  return hashlib.sha256(
    str(Path(source_root).resolve()).encode("utf-8")
  ).hexdigest()[:16]


def _layout(source_root, relative_path, private_root):
  namespace = _namespace(source_root)
  relative = Path(relative_path)
  private = Path(private_root)
  base = Path(namespace) / relative
  return _Layout(
    namespace=namespace,
    relative_path=relative,
    raw_path=private / "raw" / base,
    verbatim_path=(private / "verbatim" / base).with_suffix(".md"),
    redacted_path=(private / "redacted" / base).with_suffix(".md"),
    cursor_path=(private / "cursors" / base).with_suffix(".json"),
    provenance_path=(
      private / "provenance" / base
    ).with_suffix(".json"),
    ledger_path=private / "state" / "ledgers" / (namespace + ".json"),
    lock_path=(
      private / "state" / "locks" / base
    ).with_suffix(".lock"),
  )


def _sha256(data):
  return hashlib.sha256(data).hexdigest()


def _json_bytes(payload):
  return (
    json.dumps(
      payload,
      ensure_ascii=False,
      indent=2,
      sort_keys=True,
    ) + "\n"
  ).encode("utf-8")


def _write_atomic(path, data, private_root):
  target = Path(path)
  temporary = target.with_name(target.name + ".tmp")
  try:
    _secure_parent_chain(target, private_root)
    temporary.write_bytes(data)
    temporary.chmod(0o600)
    os.replace(temporary, target)
    target.chmod(0o600)
  finally:
    temporary.unlink(missing_ok=True)


def _write_cursor(path, data, private_root):
  _write_atomic(path, data, private_root)


def _complete_jsonl_prefix(data):
  final_newline = data.rfind(b"\n")
  return b"" if final_newline < 0 else data[:final_newline + 1]


def _first_record_digest(data):
  for line in data.splitlines(keepends=True):
    if line.strip():
      return _sha256(line)
  return _sha256(b"")


def _source_id(namespace, relative_path, source_kind, first_digest):
  payload = {
    "first_record_sha256": first_digest,
    "namespace": namespace,
    "relative_path": Path(relative_path).as_posix(),
    "source_kind": source_kind,
  }
  return _sha256(_json_bytes(payload))


def _load_cursor(path):
  cursor_path = Path(path)
  if not cursor_path.exists():
    return None
  try:
    cursor = json.loads(cursor_path.read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    raise CursorIntegrityError("Cannot read durable cursor") from error
  required = {
    "artifacts",
    "last_successful_run",
    "parse",
    "raw",
    "schema_version",
    "source",
    "state",
  }
  if (
    not isinstance(cursor, dict)
    or set(cursor) != required
    or cursor.get("schema_version") != 1
    or not isinstance(cursor.get("source"), dict)
    or not isinstance(cursor.get("raw"), dict)
    or not isinstance(cursor.get("parse"), dict)
  ):
    raise CursorIntegrityError("Invalid durable cursor")
  return cursor


def _checkpoint(cursor):
  if cursor is None:
    return None
  return {
    key: value
    for key, value in cursor.items()
    if key != "last_successful_run"
  }


def _file_matches(path, data):
  target = Path(path)
  try:
    return target.is_file() and target.read_bytes() == data
  except OSError:
    return False


def _result_from_cursor(layout, cursor, *, action, state):
  return CollectionResult(
    action=action,
    state=state,
    source_kind=(
      cursor["source"].get("kind")
      if cursor is not None
      else None
    ),
    source_id=(
      cursor["source"].get("identity")
      if cursor is not None
      else _source_id(
        layout.namespace,
        layout.relative_path,
        "unknown",
        _sha256(b""),
      )
    ),
    raw_path=layout.raw_path,
    verbatim_path=(
      layout.verbatim_path
      if layout.verbatim_path.exists()
      else None
    ),
    redacted_path=(
      layout.redacted_path
      if layout.redacted_path.exists()
      else None
    ),
    cursor_path=(
      layout.cursor_path
      if layout.cursor_path.exists()
      else None
    ),
    provenance_path=(
      layout.provenance_path
      if layout.provenance_path.exists()
      else None
    ),
    raw_size=(
      layout.raw_path.stat().st_size
      if layout.raw_path.exists()
      else 0
    ),
    parsed_size=(
      cursor["parse"].get("committed_offset", 0)
      if cursor is not None
      else 0
    ),
    event_count=(
      cursor["parse"].get("event_count", 0)
      if cursor is not None
      else 0
    ),
    issue_count=(
      cursor["parse"].get("issue_count", 0)
      if cursor is not None
      else 0
    ),
  )


def _collect_locked(
  source_path,
  source_root,
  private_root,
  layout,
  *,
  redaction_rules,
  allow_patterns,
  tool_version,
  run_id,
  observed_at,
):
  cursor = _load_cursor(layout.cursor_path)
  try:
    preservation = preserve_raw_log(
      source_path,
      raw_root=source_root,
      backup_root=Path(private_root) / "raw" / layout.namespace,
      ledger_path=layout.ledger_path,
    )
  except Exception as error:
    raise CollectionError("Raw preservation failed") from error
  _secure_file(layout.raw_path, private_root)
  _secure_file(layout.ledger_path, private_root)

  if preservation.action == "preserved":
    return _result_from_cursor(
      layout,
      cursor,
      action="preserved",
      state="diverged",
    )

  try:
    raw_bytes = layout.raw_path.read_bytes()
  except OSError as error:
    raise CollectionError("Cannot read preserved raw") from error
  complete_bytes = _complete_jsonl_prefix(raw_bytes)
  if not complete_bytes:
    source_id = _source_id(
      layout.namespace,
      layout.relative_path,
      "unknown",
      _first_record_digest(raw_bytes),
    )
    return CollectionResult(
      action=preservation.action,
      state="parse_incomplete",
      source_kind=None,
      source_id=source_id,
      raw_path=layout.raw_path,
      verbatim_path=None,
      redacted_path=None,
      cursor_path=None,
      provenance_path=None,
      raw_size=len(raw_bytes),
      parsed_size=0,
      event_count=0,
      issue_count=0,
    )

  first_digest = _first_record_digest(complete_bytes)
  try:
    source = parse_source_bytes(complete_bytes)
  except UnsupportedSourceKind:
    return CollectionResult(
      action=preservation.action,
      state="unsupported",
      source_kind=None,
      source_id=_source_id(
        layout.namespace,
        layout.relative_path,
        "unsupported",
        first_digest,
      ),
      raw_path=layout.raw_path,
      verbatim_path=None,
      redacted_path=None,
      cursor_path=None,
      provenance_path=None,
      raw_size=len(raw_bytes),
      parsed_size=0,
      event_count=0,
      issue_count=0,
    )
  except Exception as error:
    raise CollectionError("Source parsing failed") from error

  parsed = source.parsed
  source_id = _source_id(
    layout.namespace,
    layout.relative_path,
    source.source_kind,
    first_digest,
  )
  verbatim_bytes = render_transcript(parsed).encode("utf-8")
  if redaction_rules is None:
    redacted_bytes = None
    rules_digest = None
  else:
    try:
      redacted = redact_text_strict(
        verbatim_bytes.decode("utf-8"),
        redaction_rules,
        allow_patterns=allow_patterns,
      )
    except Exception as error:
      raise CollectionError("Transcript redaction failed") from error
    redacted_bytes = redacted.text.encode("utf-8")
    rules_digest = redaction_rules_digest(
      redaction_rules,
      allow_patterns=allow_patterns,
    )

  issue_kinds = sorted({issue.kind for issue in parsed.issues})
  state = (
    "parse_issues"
    if parsed.issues
    else "parse_incomplete"
    if len(complete_bytes) != len(raw_bytes)
    else "reconciled"
  )
  artifacts = {
    "redacted_sha256": (
      _sha256(redacted_bytes)
      if redacted_bytes is not None
      else None
    ),
    "verbatim_sha256": _sha256(verbatim_bytes),
  }
  source_record = {
    "first_record_sha256": first_digest,
    "identity": source_id,
    "kind": source.source_kind,
    "namespace": layout.namespace,
    "relative_path": layout.relative_path.as_posix(),
  }
  raw_record = {
    "committed_offset": len(raw_bytes),
    "sha256": _sha256(raw_bytes),
  }
  parse_record = {
    "committed_offset": len(complete_bytes),
    "event_count": len(parsed.events),
    "issue_count": len(parsed.issues),
    "issue_kinds": issue_kinds,
    "sha256": _sha256(complete_bytes),
  }
  provenance = {
    "artifacts": artifacts,
    "parse": parse_record,
    "raw": raw_record,
    "redaction_rules_sha256": rules_digest,
    "schema_version": 1,
    "source": source_record,
    "tool_version": tool_version,
  }
  provenance_bytes = _json_bytes(provenance)
  cursor_payload = {
    "artifacts": artifacts,
    "last_successful_run": {
      "id": run_id,
      "observed_at": observed_at,
    },
    "parse": parse_record,
    "raw": raw_record,
    "schema_version": 1,
    "source": source_record,
    "state": state,
  }
  checkpoint = {
    key: value
    for key, value in cursor_payload.items()
    if key != "last_successful_run"
  }
  artifacts_match = (
    _file_matches(layout.verbatim_path, verbatim_bytes)
    and _file_matches(layout.provenance_path, provenance_bytes)
    and (
      redacted_bytes is None
      or _file_matches(layout.redacted_path, redacted_bytes)
    )
  )
  if cursor is None:
    action = "created"
  elif _checkpoint(cursor) != checkpoint:
    action = "updated"
  elif not artifacts_match:
    action = "repaired"
  else:
    action = "unchanged"

  if action != "unchanged":
    try:
      _write_atomic(layout.verbatim_path, verbatim_bytes, private_root)
      if redacted_bytes is not None:
        _write_atomic(layout.redacted_path, redacted_bytes, private_root)
      _write_atomic(layout.provenance_path, provenance_bytes, private_root)
      _write_cursor(
        layout.cursor_path,
        _json_bytes(cursor_payload),
        private_root,
      )
    except OSError as error:
      raise CollectionError("Artifact checkpoint failed") from error
  else:
    _secure_file(layout.verbatim_path, private_root)
    if redacted_bytes is not None:
      _secure_file(layout.redacted_path, private_root)
    _secure_file(layout.provenance_path, private_root)
    _secure_file(layout.cursor_path, private_root)

  return CollectionResult(
    action=action,
    state=state,
    source_kind=source.source_kind,
    source_id=source_id,
    raw_path=layout.raw_path,
    verbatim_path=layout.verbatim_path,
    redacted_path=(
      layout.redacted_path
      if redacted_bytes is not None
      else None
    ),
    cursor_path=layout.cursor_path,
    provenance_path=layout.provenance_path,
    raw_size=len(raw_bytes),
    parsed_size=len(complete_bytes),
    event_count=len(parsed.events),
    issue_count=len(parsed.issues),
  )


def collect_source(
  source_path,
  *,
  source_root,
  private_root,
  repository_root,
  tool_version,
  run_id,
  observed_at,
  redaction_rules=None,
  allow_patterns=(),
  lock_timeout_seconds=300,
) -> CollectionResult:
  (
    resolved_source,
    resolved_source_root,
    resolved_private,
    relative_path,
  ) = _validate_boundaries(
    source_path,
    source_root,
    private_root,
    repository_root,
  )
  layout = _layout(
    resolved_source_root,
    relative_path,
    resolved_private,
  )
  _secure_parent_chain(layout.raw_path, resolved_private)
  _secure_parent_chain(layout.lock_path, resolved_private)
  try:
    with exclusive_lock(
      layout.lock_path,
      timeout_seconds=lock_timeout_seconds,
    ):
      return _collect_locked(
        resolved_source,
        resolved_source_root,
        resolved_private,
        layout,
        redaction_rules=redaction_rules,
        allow_patterns=allow_patterns,
        tool_version=tool_version,
        run_id=run_id,
        observed_at=observed_at,
      )
  except LockHeld as error:
    raise CollectionLocked("Source collection is already locked") from error
  except LockError as error:
    raise CollectionError("Cannot manage source collection lock") from error


def _known_cursors(source_root, private_root):
  namespace = _namespace(source_root)
  cursor_root = Path(private_root) / "cursors" / namespace
  if not cursor_root.exists():
    return {}
  known = {}
  for path in sorted(cursor_root.rglob("*.json")):
    if not path.is_file() or path.is_symlink():
      continue
    try:
      cursor = _load_cursor(path)
      relative = cursor["source"]["relative_path"]
    except (CursorIntegrityError, KeyError, TypeError):
      continue
    known[relative] = cursor
  return known


def _item_from_result(result):
  return ReconcileItem(
    action=result.action,
    state=result.state,
    source_kind=result.source_kind,
    source_id=result.source_id,
    event_count=result.event_count,
    issue_count=result.issue_count,
  )


def _summarize_items(items):
  fixed_items = tuple(items)
  counts = {
    "failed": sum(
      item.state in ("diverged", "failed")
      for item in fixed_items
    ),
    "missing": sum(
      item.state == "source_missing"
      for item in fixed_items
    ),
    "succeeded": sum(
      item.state in ("parse_incomplete", "parse_issues", "reconciled")
      for item in fixed_items
    ),
    "unsupported": sum(
      item.state == "unsupported"
      for item in fixed_items
    ),
  }
  adverse = counts["failed"] + counts["missing"] + counts["unsupported"]
  if adverse == 0:
    status = "ok"
  elif counts["succeeded"]:
    status = "partial"
  else:
    status = "error"
  return ReconcileResult(
    counts=counts,
    items=tuple(sorted(fixed_items, key=lambda item: item.source_id)),
    status=status,
  )


def reconcile_source_root(
  source_root,
  *,
  private_root,
  repository_root,
  tool_version,
  run_id,
  observed_at,
  redaction_rules=None,
  allow_patterns=(),
) -> ReconcileResult:
  native_root = Path(source_root)
  private = Path(private_root)
  repository = Path(repository_root)
  if not all(path.is_absolute() for path in (native_root, private, repository)):
    raise UnsafeCollectionBoundary("Collection paths must be absolute")
  if _within(private, repository):
    raise UnsafeCollectionBoundary("Unsafe session collection boundary")
  try:
    relative_paths = discover_raw_logs(native_root)
  except Exception as error:
    raise CollectionError("Cannot discover session sources") from error

  items = []
  for relative_path in relative_paths:
    try:
      result = collect_source(
        native_root / relative_path,
        source_root=native_root,
        private_root=private,
        repository_root=repository,
        tool_version=tool_version,
        run_id=run_id,
        observed_at=observed_at,
        redaction_rules=redaction_rules,
        allow_patterns=allow_patterns,
      )
    except Exception as error:
      source_id = _source_id(
        _namespace(native_root),
        relative_path,
        "failed",
        _sha256(b""),
      )
      items.append(ReconcileItem(
        action="failed",
        state="failed",
        source_kind=None,
        source_id=source_id,
        reason=type(error).__name__,
      ))
    else:
      items.append(_item_from_result(result))

  discovered = set(relative_paths)
  for relative_path, cursor in _known_cursors(native_root, private).items():
    if relative_path in discovered:
      continue
    items.append(ReconcileItem(
      action="preserved",
      state="source_missing",
      source_kind=cursor["source"].get("kind"),
      source_id=cursor["source"].get("identity"),
      event_count=cursor["parse"].get("event_count", 0),
      issue_count=cursor["parse"].get("issue_count", 0),
    ))

  return _summarize_items(items)


def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument("--source-root", required=True)
  parser.add_argument("--private-root", required=True)
  parser.add_argument("--repository-root", required=True)
  parser.add_argument("--source-relative-path")
  parser.add_argument("--tool-version", required=True)
  parser.add_argument("--run-id")
  parser.add_argument("--observed-at")
  args = parser.parse_args(argv)
  now = datetime.datetime.now(datetime.timezone.utc).astimezone()
  run_id = args.run_id or now.strftime("manual-%Y%m%dT%H%M%S%z")
  observed_at = args.observed_at or now.isoformat(timespec="seconds")
  try:
    source_root = Path(args.source_root)
    if args.source_relative_path is None:
      result = reconcile_source_root(
        source_root,
        private_root=Path(args.private_root),
        repository_root=Path(args.repository_root),
        tool_version=args.tool_version,
        run_id=run_id,
        observed_at=observed_at,
      )
    else:
      relative_path = Path(args.source_relative_path)
      if relative_path.is_absolute() or ".." in relative_path.parts:
        raise UnsafeCollectionBoundary("Unsafe selected source path")
      collected = collect_source(
        source_root / relative_path,
        source_root=source_root,
        private_root=Path(args.private_root),
        repository_root=Path(args.repository_root),
        tool_version=args.tool_version,
        run_id=run_id,
        observed_at=observed_at,
      )
      result = _summarize_items((_item_from_result(collected),))
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "error",
    }, sort_keys=True))
    return 5
  print(json.dumps(
    result.report(),
    ensure_ascii=False,
    sort_keys=True,
  ))
  return 0 if result.status == "ok" else 5


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
