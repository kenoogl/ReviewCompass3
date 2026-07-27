"""本文込み材料束とdigestの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib

import pytest


def _classified_materials(review_materials):
  return review_materials.classify_materials((
    {
      "identifier": "target.md",
      "role": "target",
      "route": "main",
    },
    {
      "identifier": "references/context.md",
      "role": "reference",
      "route": "independent",
    },
  ))


def test_builds_deterministic_bundle_with_bodies_and_digests(tmp_path):
  repository = tmp_path / "repository"
  references = repository / "references"
  references.mkdir(parents=True)
  (repository / "target.md").write_text("target\n", encoding="utf-8")
  (references / "context.md").write_text("context\n", encoding="utf-8")
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )
  material_bundle = importlib.import_module(
    "tools.bootstrap.material_bundle"
  )
  materials = _classified_materials(review_materials)

  bundle = material_bundle.build_material_bundle(
    repository,
    tuple(reversed(materials)),
  )

  assert tuple(
    material.identifier
    for material in bundle.materials
  ) == (
    "references/context.md",
    "target.md",
  )
  assert bundle.materials[0].content == "context\n"
  assert bundle.materials[0].content_sha256 == hashlib.sha256(
    b"context\n"
  ).hexdigest()
  assert bundle.digest == material_bundle.build_material_bundle(
    repository,
    materials,
  ).digest
  assert len(bundle.digest) == 64
  assert str(repository) not in repr(bundle)


@pytest.mark.parametrize("invalid_kind", ("missing", "symlink", "non_utf8"))
def test_rejects_material_without_safe_utf8_body(tmp_path, invalid_kind):
  repository = tmp_path / "repository"
  repository.mkdir()
  material_path = repository / "target.md"
  if invalid_kind == "symlink":
    outside = tmp_path / "outside.md"
    outside.write_text("outside\n", encoding="utf-8")
    material_path.symlink_to(outside)
  elif invalid_kind == "non_utf8":
    material_path.write_bytes(b"\xff")
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
  ))

  with pytest.raises(material_bundle.MaterialBundleError):
    material_bundle.build_material_bundle(repository, materials)
