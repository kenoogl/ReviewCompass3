"""レビュー材料区分の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_classifies_roles_and_selection_routes_deterministically():
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )

  materials = review_materials.classify_materials((
    {
      "identifier": "references/context.md",
      "role": "reference",
      "route": "independent",
    },
    {
      "identifier": "requirements/target.md",
      "role": "target",
      "route": "main",
    },
    {
      "identifier": "rules/required.md",
      "role": "required",
      "route": "main",
    },
  ))

  assert materials == (
    review_materials.MaterialSelection(
      identifier="references/context.md",
      role=review_materials.MaterialRole.REFERENCE,
      route=review_materials.SelectionRoute.INDEPENDENT,
    ),
    review_materials.MaterialSelection(
      identifier="requirements/target.md",
      role=review_materials.MaterialRole.TARGET,
      route=review_materials.SelectionRoute.MAIN,
    ),
    review_materials.MaterialSelection(
      identifier="rules/required.md",
      role=review_materials.MaterialRole.REQUIRED,
      route=review_materials.SelectionRoute.MAIN,
    ),
  )


@pytest.mark.parametrize(
  "entry",
  (
    {
      "identifier": "material.md",
      "role": "unknown",
      "route": "main",
    },
    {
      "identifier": "material.md",
      "role": "target",
      "route": "unknown",
    },
    {
      "identifier": "../outside.md",
      "role": "target",
      "route": "main",
    },
  ),
)
def test_rejects_unknown_or_unsafe_material_values(entry):
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )

  with pytest.raises(review_materials.MaterialClassificationError):
    review_materials.classify_materials((entry,))


def test_rejects_duplicate_material_identifiers():
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )
  entries = (
    {
      "identifier": "material.md",
      "role": "target",
      "route": "main",
    },
    {
      "identifier": "material.md",
      "role": "reference",
      "route": "independent",
    },
  )

  with pytest.raises(review_materials.MaterialClassificationError):
    review_materials.classify_materials(entries)
