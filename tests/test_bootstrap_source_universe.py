"""source universe機械列挙の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import subprocess

import pytest


def _git(repository, *arguments):
  return subprocess.run(
    ["git", "-C", str(repository), *arguments],
    capture_output=True,
    check=True,
  )


def test_enumerates_tracked_regular_files_in_deterministic_order(tmp_path):
  repository = tmp_path / "repository"
  repository.mkdir()
  _git(repository, "init")

  generated = repository / "generated" / "report.json"
  generated.parent.mkdir()
  generated.write_text("{}\n", encoding="utf-8")
  (repository / "z.py").write_text("z = 1\n", encoding="utf-8")
  (repository / "a.txt").write_text("a\n", encoding="utf-8")
  (repository / "untracked.txt").write_text("outside\n", encoding="utf-8")
  (repository / "linked.py").symlink_to(repository / "z.py")
  _git(
    repository,
    "add",
    "generated/report.json",
    "z.py",
    "a.txt",
    "linked.py",
  )

  source_universe = importlib.import_module(
    "tools.bootstrap.source_universe"
  )

  assert source_universe.enumerate_source_universe(repository) == (
    "a.txt",
    "generated/report.json",
    "z.py",
  )


@pytest.mark.parametrize("repository_kind", ("missing", "non_git"))
def test_rejects_invalid_repository_boundary(tmp_path, repository_kind):
  repository = tmp_path / "repository"
  if repository_kind == "non_git":
    repository.mkdir()

  source_universe = importlib.import_module(
    "tools.bootstrap.source_universe"
  )

  with pytest.raises(source_universe.SourceUniverseError):
    source_universe.enumerate_source_universe(repository)
