"""証拠閉包と材料被覆の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _bundle(repository, entries):
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )
  material_bundle = importlib.import_module(
    "tools.bootstrap.material_bundle"
  )
  return material_bundle.build_material_bundle(
    repository,
    review_materials.classify_materials(entries),
  )


def test_reports_complete_closed_and_covered_materials(tmp_path):
  repository = tmp_path / "repository"
  repository.mkdir()
  for identifier in ("target.md", "reference.md", "required.md"):
    (repository / identifier).write_text(
      identifier + "\n",
      encoding="utf-8",
    )
  bundle = _bundle(repository, (
    {
      "identifier": "target.md",
      "role": "target",
      "route": "main",
    },
    {
      "identifier": "reference.md",
      "role": "reference",
      "route": "independent",
    },
    {
      "identifier": "required.md",
      "role": "required",
      "route": "main",
    },
  ))
  evidence_closure = importlib.import_module(
    "tools.bootstrap.evidence_closure"
  )

  assert evidence_closure.assess_evidence_closure(
    ("target.md", "reference.md", "required.md"),
    bundle,
    required_identifiers=("required.md",),
  ) == evidence_closure.EvidenceClosure(
    status="complete",
    missing_required=(),
    uncovered_source=(),
    main_materials=("required.md", "target.md"),
    independent_materials=("reference.md",),
    missing_routes=(),
  )


def test_reports_formal_insufficient_materials(tmp_path):
  repository = tmp_path / "repository"
  repository.mkdir()
  (repository / "target.md").write_text("target\n", encoding="utf-8")
  bundle = _bundle(repository, (
    {
      "identifier": "target.md",
      "role": "target",
      "route": "main",
    },
  ))
  evidence_closure = importlib.import_module(
    "tools.bootstrap.evidence_closure"
  )

  assert evidence_closure.assess_evidence_closure(
    ("required.md", "reference.md", "target.md"),
    bundle,
    required_identifiers=("required.md",),
  ) == evidence_closure.EvidenceClosure(
    status="insufficient",
    missing_required=("required.md",),
    uncovered_source=("reference.md", "required.md"),
    main_materials=("target.md",),
    independent_materials=(),
    missing_routes=("independent",),
  )


def test_rejects_material_outside_source_universe(tmp_path):
  repository = tmp_path / "repository"
  repository.mkdir()
  (repository / "outside.md").write_text("outside\n", encoding="utf-8")
  bundle = _bundle(repository, (
    {
      "identifier": "outside.md",
      "role": "reference",
      "route": "independent",
    },
  ))
  evidence_closure = importlib.import_module(
    "tools.bootstrap.evidence_closure"
  )

  with pytest.raises(evidence_closure.EvidenceClosureError):
    evidence_closure.assess_evidence_closure(
      ("target.md",),
      bundle,
      required_identifiers=(),
    )
