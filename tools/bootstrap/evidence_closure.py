"""証拠閉包と材料被覆の機械判定。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses

from tools.bootstrap.material_bundle import (
  MaterialBundle,
  calculate_bundle_digest,
)
from tools.bootstrap.review_materials import MaterialRole, SelectionRoute


class EvidenceClosureError(Exception):
  """証拠閉包を安全に判定できない。"""


@dataclasses.dataclass(frozen=True)
class EvidenceClosure:
  status: str
  missing_required: tuple
  uncovered_source: tuple
  main_materials: tuple
  independent_materials: tuple
  missing_routes: tuple


def _unique_identifiers(values, label):
  identifiers = tuple(values)
  if (
    len(set(identifiers)) != len(identifiers)
    or any(
      not isinstance(identifier, str)
      or not identifier
      for identifier in identifiers
    )
  ):
    raise EvidenceClosureError(
      "%s identifiers must be unique strings" % label
    )
  return set(identifiers)


def assess_evidence_closure(
  source_universe,
  bundle,
  *,
  required_identifiers,
) -> EvidenceClosure:
  universe = _unique_identifiers(
    source_universe,
    "Source universe",
  )
  required = _unique_identifiers(
    required_identifiers,
    "Required material",
  )
  if not required <= universe:
    raise EvidenceClosureError(
      "Required materials must belong to the source universe"
    )
  if (
    not isinstance(bundle, MaterialBundle)
    or calculate_bundle_digest(bundle.materials) != bundle.digest
  ):
    raise EvidenceClosureError(
      "Evidence closure requires an intact material bundle"
    )

  bundled = {
    material.identifier
    for material in bundle.materials
  }
  if not bundled <= universe:
    raise EvidenceClosureError(
      "Bundled materials must belong to the source universe"
    )
  bundled_required = {
    material.identifier
    for material in bundle.materials
    if material.role == MaterialRole.REQUIRED
  }
  if bundled_required != required & bundled:
    raise EvidenceClosureError(
      "Required material roles must match the required scope"
    )

  main_materials = tuple(
    material.identifier
    for material in bundle.materials
    if material.route == SelectionRoute.MAIN
  )
  independent_materials = tuple(
    material.identifier
    for material in bundle.materials
    if material.route == SelectionRoute.INDEPENDENT
  )
  missing_routes = tuple(
    route
    for route, materials in (
      ("main", main_materials),
      ("independent", independent_materials),
    )
    if not materials
  )
  missing_required = tuple(sorted(required - bundled))
  uncovered_source = tuple(sorted(universe - bundled))
  status = (
    "complete"
    if not missing_required
    and not uncovered_source
    and not missing_routes
    else "insufficient"
  )
  return EvidenceClosure(
    status=status,
    missing_required=missing_required,
    uncovered_source=uncovered_source,
    main_materials=main_materials,
    independent_materials=independent_materials,
    missing_routes=missing_routes,
  )
