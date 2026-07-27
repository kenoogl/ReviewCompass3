"""既知移植候補の発見保証に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import subprocess

import pytest


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


def _git(repository, *arguments):
  return subprocess.run(
    ["git", "-C", str(repository), *arguments],
    capture_output=True,
    check=True,
    text=True,
  ).stdout.strip()


def _initialize_repository(repository, files):
  repository.mkdir()
  _git(repository, "init")
  _git(repository, "config", "user.name", "Bootstrap Test")
  _git(repository, "config", "user.email", "bootstrap@example.invalid")
  for relative_path in files:
    path = repository / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(relative_path + "\n", encoding="utf-8")
  _git(repository, "add", ".")
  _git(repository, "commit", "-m", "Add fixed reference files")
  return _git(repository, "rev-parse", "HEAD")


def test_discovers_candidates_from_fixed_commit_trees_without_worktree_changes(
  tmp_path,
):
  first_repository = tmp_path / "first"
  first_commit = _initialize_repository(
    first_repository,
    ("tools/source_bundle.py", "notes.txt"),
  )
  second_repository = tmp_path / "second"
  second_commit = _initialize_repository(
    second_repository,
    ("nested/trusted_review_send.py",),
  )
  (first_repository / "tools" / "source_bundle.py").unlink()
  (first_repository / "run_risk_review.py").write_text(
    "untracked\n",
    encoding="utf-8",
  )
  statuses_before = (
    _git(first_repository, "status", "--porcelain"),
    _git(second_repository, "status", "--porcelain"),
  )
  migration_candidates = importlib.import_module(
    "tools.bootstrap.migration_candidates"
  )
  sources = (
    migration_candidates.ReferenceSource(
      name="reviewcompass",
      repository_root=first_repository,
      commit=first_commit,
    ),
    migration_candidates.ReferenceSource(
      name="reviewcompass2",
      repository_root=second_repository,
      commit=second_commit,
    ),
  )

  assert migration_candidates.discover_migration_candidates(
    sources,
    required_names=(
      "trusted_review_send.py",
      "source_bundle.py",
    ),
  ) == (
    migration_candidates.MigrationCandidate(
      source="reviewcompass",
      relative_path="tools/source_bundle.py",
      matched_name="source_bundle.py",
    ),
    migration_candidates.MigrationCandidate(
      source="reviewcompass2",
      relative_path="nested/trusted_review_send.py",
      matched_name="trusted_review_send.py",
    ),
  )
  assert statuses_before == (
    _git(first_repository, "status", "--porcelain"),
    _git(second_repository, "status", "--porcelain"),
  )


def test_fails_closed_with_sorted_missing_known_names(tmp_path):
  repository = tmp_path / "reference"
  commit = _initialize_repository(
    repository,
    ("tools/source_bundle.py",),
  )
  migration_candidates = importlib.import_module(
    "tools.bootstrap.migration_candidates"
  )
  source = migration_candidates.ReferenceSource(
    name="reference",
    repository_root=repository,
    commit=commit,
  )

  with pytest.raises(
    migration_candidates.MissingMigrationCandidateError
  ) as error:
    migration_candidates.discover_migration_candidates(
      (source,),
      required_names=(
        "trusted_review_send.py",
        "source_bundle.py",
        "assurance_pipeline.py",
      ),
    )

  assert error.value.missing_names == (
    "assurance_pipeline.py",
    "trusted_review_send.py",
  )


def test_default_known_names_match_the_stage_one_plan():
  migration_candidates = importlib.import_module(
    "tools.bootstrap.migration_candidates"
  )

  assert migration_candidates.KNOWN_MIGRATION_FILES == (
    KNOWN_MIGRATION_FILES
  )
