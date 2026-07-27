"""第4段の機能境界relationに関する暫定テスト。"""

import importlib

import pytest


def test_validates_complete_reciprocal_boundary_relations():
  boundaries = importlib.import_module(
    "tools.requirements.boundary_relations"
  )

  result = boundaries.validate_boundary_relations(
    records=(
      {
        "from": "REQ-PORTABLE-001",
        "relation": "provides_to",
        "to": "REQ-CONTEXT-001",
        "contract": "safe storage",
      },
      {
        "from": "REQ-CONTEXT-001",
        "relation": "depends_on",
        "to": "REQ-PORTABLE-001",
        "contract": "safe storage",
      },
    ),
    defined_requirement_ids=(
      "REQ-CONTEXT-001",
      "REQ-PORTABLE-001",
    ),
  )

  assert result.status == "complete"
  assert result.relation_count == 2
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "records",
  (
    (
      {
        "from": "REQ-PORTABLE-001",
        "relation": "provides_to",
        "to": "REQ-CONTEXT-001",
        "contract": "safe storage",
      },
    ),
    (
      {
        "from": "REQ-UNKNOWN-001",
        "relation": "depends_on",
        "to": "REQ-CONTEXT-001",
        "contract": "safe storage",
      },
    ),
    (
      {
        "from": "REQ-PORTABLE-001",
        "relation": "unknown",
        "to": "REQ-CONTEXT-001",
        "contract": "safe storage",
      },
    ),
  ),
)
def test_rejects_incomplete_or_unresolved_boundaries(records):
  boundaries = importlib.import_module(
    "tools.requirements.boundary_relations"
  )

  with pytest.raises(boundaries.BoundaryRelationError):
    boundaries.validate_boundary_relations(
      records=records,
      defined_requirement_ids=(
        "REQ-CONTEXT-001",
        "REQ-PORTABLE-001",
      ),
    )
