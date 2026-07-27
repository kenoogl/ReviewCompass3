"""レビュー材料の区分と選定経路。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import enum
from pathlib import PurePosixPath


class MaterialClassificationError(Exception):
  """レビュー材料を安全に型付けできない。"""


class MaterialRole(enum.Enum):
  TARGET = "target"
  REFERENCE = "reference"
  REQUIRED = "required"


class SelectionRoute(enum.Enum):
  MAIN = "main"
  INDEPENDENT = "independent"


@dataclasses.dataclass(frozen=True)
class MaterialSelection:
  identifier: str
  role: MaterialRole
  route: SelectionRoute


def _safe_identifier(value):
  if not isinstance(value, str):
    return False
  path = PurePosixPath(value)
  return (
    bool(value)
    and "\\" not in value
    and "\x00" not in value
    and "\n" not in value
    and not path.is_absolute()
    and path.as_posix() == value
    and all(part not in ("", ".", "..") for part in path.parts)
  )


def _classify_entry(entry):
  if (
    not isinstance(entry, dict)
    or set(entry) != {"identifier", "role", "route"}
    or not _safe_identifier(entry.get("identifier"))
  ):
    raise MaterialClassificationError(
      "Material entries require a safe relative identifier"
    )
  try:
    role = MaterialRole(entry["role"])
    route = SelectionRoute(entry["route"])
  except (TypeError, ValueError) as error:
    raise MaterialClassificationError(
      "Unknown material role or selection route"
    ) from error
  return MaterialSelection(
    identifier=entry["identifier"],
    role=role,
    route=route,
  )


def classify_materials(entries) -> tuple:
  materials = tuple(
    _classify_entry(entry)
    for entry in entries
  )
  identifiers = tuple(
    material.identifier
    for material in materials
  )
  if len(set(identifiers)) != len(identifiers):
    raise MaterialClassificationError(
      "Material identifiers must be unique"
    )
  return tuple(sorted(
    materials,
    key=lambda material: (
      material.identifier,
      material.role.value,
      material.route.value,
    ),
  ))
