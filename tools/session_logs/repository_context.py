"""明示Git範囲から安全な要約材料を収集する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import subprocess
from pathlib import Path

from tools.session_logs.redaction import redact_text_strict


class RepositoryContextError(Exception):
  """明示されたGit範囲から要約材料を収集できない。"""


@dataclasses.dataclass(frozen=True)
class RepositoryContext:
  commits: tuple
  changed_files: tuple


def _run_git(repository_root, arguments, runner):
  try:
    result = runner(
      ["git", "-C", str(repository_root), *arguments],
      capture_output=True,
      check=False,
      text=True,
    )
  except Exception as error:
    raise RepositoryContextError(
      "Cannot collect repository summary context"
    ) from error
  if result.returncode != 0:
    raise RepositoryContextError(
      "Cannot collect repository summary context"
    )
  return tuple(
    line
    for line in result.stdout.splitlines()
    if line
  )


def _redact_values(values, rules, allow_patterns):
  return tuple(
    redact_text_strict(
      value,
      rules,
      allow_patterns=allow_patterns,
    ).text
    for value in values
  )


def collect_repository_context(
  repository_root,
  revision_range,
  *,
  rules,
  allow_patterns=(),
  runner=subprocess.run,
) -> RepositoryContext:
  root = Path(repository_root).resolve()
  if (
    not (root / ".git").exists()
    or not isinstance(revision_range, str)
    or not revision_range
    or revision_range.startswith("-")
    or "\x00" in revision_range
    or "\n" in revision_range
  ):
    raise RepositoryContextError(
      "Unsafe repository summary context"
    )
  commits = _run_git(
    root,
    [
      "log",
      "--format=%h %s",
      "--reverse",
      revision_range,
      "--",
    ],
    runner,
  )
  changed_files = _run_git(
    root,
    [
      "diff",
      "--name-only",
      "--diff-filter=ACDMRTUXB",
      revision_range,
      "--",
    ],
    runner,
  )
  return RepositoryContext(
    commits=_redact_values(
      commits,
      rules,
      allow_patterns,
    ),
    changed_files=_redact_values(
      changed_files,
      rules,
      allow_patterns,
    ),
  )
