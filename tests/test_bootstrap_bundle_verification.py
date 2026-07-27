"""材料束の原文一致・stale検査に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import importlib

import pytest


def _build_bundle(repository):
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )
  material_bundle = importlib.import_module(
    "tools.bootstrap.material_bundle"
  )
  materials = review_materials.classify_materials((
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
  ))
  return material_bundle.build_material_bundle(repository, materials)


def test_reports_matching_unchanged_original_materials(tmp_path):
  repository = tmp_path / "repository"
  repository.mkdir()
  (repository / "target.md").write_text("target\n", encoding="utf-8")
  (repository / "reference.md").write_text(
    "reference\n",
    encoding="utf-8",
  )
  bundle = _build_bundle(repository)
  bundle_verification = importlib.import_module(
    "tools.bootstrap.bundle_verification"
  )

  assert bundle_verification.verify_material_bundle(
    repository,
    bundle,
  ) == bundle_verification.BundleVerification(
    status="matches",
    stale_identifiers=(),
  )


@pytest.mark.parametrize("mutation", ("changed", "missing", "symlink"))
def test_reports_stale_original_materials(tmp_path, mutation):
  repository = tmp_path / "repository"
  repository.mkdir()
  target = repository / "target.md"
  target.write_text("target\n", encoding="utf-8")
  (repository / "reference.md").write_text(
    "reference\n",
    encoding="utf-8",
  )
  bundle = _build_bundle(repository)
  if mutation == "changed":
    target.write_text("changed\n", encoding="utf-8")
  elif mutation == "missing":
    target.unlink()
  else:
    target.unlink()
    outside = tmp_path / "outside.md"
    outside.write_text("target\n", encoding="utf-8")
    target.symlink_to(outside)
  bundle_verification = importlib.import_module(
    "tools.bootstrap.bundle_verification"
  )

  assert bundle_verification.verify_material_bundle(
    repository,
    bundle,
  ) == bundle_verification.BundleVerification(
    status="stale",
    stale_identifiers=("target.md",),
  )


@pytest.mark.parametrize("mutation", ("content", "bundle_digest"))
def test_rejects_internally_modified_bundle(tmp_path, mutation):
  repository = tmp_path / "repository"
  repository.mkdir()
  (repository / "target.md").write_text("target\n", encoding="utf-8")
  (repository / "reference.md").write_text(
    "reference\n",
    encoding="utf-8",
  )
  bundle = _build_bundle(repository)
  if mutation == "content":
    first = dataclasses.replace(
      bundle.materials[0],
      content="modified\n",
    )
    bundle = dataclasses.replace(
      bundle,
      materials=(first, *bundle.materials[1:]),
    )
  else:
    bundle = dataclasses.replace(bundle, digest="0" * 64)
  bundle_verification = importlib.import_module(
    "tools.bootstrap.bundle_verification"
  )

  with pytest.raises(bundle_verification.BundleIntegrityError):
    bundle_verification.verify_material_bundle(repository, bundle)
