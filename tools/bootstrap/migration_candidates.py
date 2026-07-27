"""固定参照からの既知移植候補発見。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
from pathlib import Path, PurePosixPath
import re
import subprocess


KNOWN_MIGRATION_FILES = (
  "assurance_pipeline.py",
  "change_inventory.py",
  "review_input_guard.py",
  "risk_review_contracts.py",
  "risk_review_materializer.py",
  "risk_review_store.py",
  "run_risk_review.py",
  "source_bundle.py",
  "source_scope_assurance.py",
  "source_scope_guard.py",
  "trusted_review_send.py",
)

_COMMIT_PATTERN = re.compile(r"[0-9a-f]{40,64}")
_REGULAR_FILE_MODES = (b"100644", b"100755")


class MigrationCandidateError(Exception):
  """固定参照から候補を安全に発見できない。"""


class MissingMigrationCandidateError(MigrationCandidateError):
  """計画上の既知正例を発見できない。"""

  def __init__(self, missing_names):
    self.missing_names = tuple(sorted(missing_names))
    super().__init__(
      "Missing known migration candidates: %s"
      % ", ".join(self.missing_names)
    )


@dataclasses.dataclass(frozen=True)
class ReferenceSource:
  name: str
  repository_root: object
  commit: str


@dataclasses.dataclass(frozen=True)
class MigrationCandidate:
  source: str
  relative_path: str
  matched_name: str


def _validate_required_names(required_names):
  names = tuple(required_names)
  if (
    not names
    or len(set(names)) != len(names)
    or any(
      not isinstance(name, str)
      or not name
      or PurePosixPath(name).name != name
      for name in names
    )
  ):
    raise MigrationCandidateError(
      "Known migration candidate names must be unique basenames"
    )
  return names


def _validate_source(source):
  if (
    not isinstance(source, ReferenceSource)
    or not isinstance(source.name, str)
    or not source.name
    or not isinstance(source.commit, str)
    or _COMMIT_PATTERN.fullmatch(source.commit) is None
  ):
    raise MigrationCandidateError(
      "Reference source must have a name and fixed commit"
    )
  root = Path(source.repository_root).resolve()
  if not root.is_dir() or not (root / ".git").exists():
    raise MigrationCandidateError(
      "Reference source must be an existing Git repository"
    )
  return root


def _commit_tree_paths(source):
  root = _validate_source(source)
  try:
    result = subprocess.run(
      [
        "git",
        "-C",
        str(root),
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        source.commit,
      ],
      capture_output=True,
      check=False,
    )
  except OSError as error:
    raise MigrationCandidateError(
      "Cannot enumerate the fixed reference tree"
    ) from error
  if result.returncode != 0:
    raise MigrationCandidateError(
      "Cannot enumerate the fixed reference tree"
    )

  paths = []
  try:
    for record in result.stdout.split(b"\x00"):
      if not record:
        continue
      metadata, path_value = record.split(b"\t", 1)
      mode, object_type, _object_id = metadata.split(b" ", 2)
      if mode in _REGULAR_FILE_MODES and object_type == b"blob":
        paths.append(path_value.decode("utf-8"))
  except (UnicodeDecodeError, ValueError) as error:
    raise MigrationCandidateError(
      "Fixed reference tree contains an invalid entry"
    ) from error
  return tuple(paths)


def discover_migration_candidates(
  sources,
  *,
  required_names=KNOWN_MIGRATION_FILES,
) -> tuple:
  names = _validate_required_names(required_names)
  source_values = tuple(sources)
  source_names = tuple(source.name for source in source_values)
  if len(set(source_names)) != len(source_names):
    raise MigrationCandidateError(
      "Reference source names must be unique"
    )

  candidates = []
  for source in source_values:
    for relative_path in _commit_tree_paths(source):
      matched_name = PurePosixPath(relative_path).name
      if matched_name in names:
        candidates.append(MigrationCandidate(
          source=source.name,
          relative_path=relative_path,
          matched_name=matched_name,
        ))

  found_names = {
    candidate.matched_name
    for candidate in candidates
  }
  missing_names = set(names) - found_names
  if missing_names:
    raise MissingMigrationCandidateError(missing_names)

  return tuple(sorted(
    candidates,
    key=lambda candidate: (
      candidate.source,
      candidate.relative_path,
      candidate.matched_name,
    ),
  ))
