"""本文込みレビュー材料束とdigest。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
from pathlib import Path, PurePosixPath

from tools.bootstrap.review_materials import MaterialSelection


class MaterialBundleError(Exception):
  """安全な本文込み材料束を生成できない。"""


@dataclasses.dataclass(frozen=True)
class BundledMaterial:
  identifier: str
  role: object
  route: object
  content: str
  content_sha256: str


@dataclasses.dataclass(frozen=True)
class MaterialBundle:
  materials: tuple
  digest: str


def _material_document(material):
  return {
    "content": material.content,
    "content_sha256": material.content_sha256,
    "identifier": material.identifier,
    "role": material.role.value,
    "route": material.route.value,
  }


def canonical_bundle_bytes(materials) -> bytes:
  return json.dumps(
    {
      "materials": [
        _material_document(material)
        for material in materials
      ],
      "schema_version": 1,
    },
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode("utf-8")


def calculate_bundle_digest(materials) -> str:
  return hashlib.sha256(
    canonical_bundle_bytes(materials)
  ).hexdigest()


def _read_material(root, selection):
  if not isinstance(selection, MaterialSelection):
    raise MaterialBundleError(
      "Bundle inputs must be classified materials"
    )
  path = root
  for part in PurePosixPath(selection.identifier).parts:
    path = path / part
    if path.is_symlink():
      raise MaterialBundleError(
        "Bundle materials must not contain symbolic links"
      )
  if not path.is_file():
    raise MaterialBundleError(
      "Bundle material does not exist as a regular file"
    )
  try:
    body = path.read_bytes()
    content = body.decode("utf-8")
  except (OSError, UnicodeDecodeError) as error:
    raise MaterialBundleError(
      "Bundle materials must have readable UTF-8 bodies"
    ) from error
  return BundledMaterial(
    identifier=selection.identifier,
    role=selection.role,
    route=selection.route,
    content=content,
    content_sha256=hashlib.sha256(body).hexdigest(),
  )


def build_material_bundle(repository_root, selections) -> MaterialBundle:
  root = Path(repository_root).resolve()
  if not root.is_dir():
    raise MaterialBundleError(
      "Bundle root must be an existing directory"
    )
  selection_values = tuple(selections)
  identifiers = tuple(
    selection.identifier
    if isinstance(selection, MaterialSelection)
    else None
    for selection in selection_values
  )
  if len(set(identifiers)) != len(identifiers):
    raise MaterialBundleError(
      "Bundle material identifiers must be unique"
    )
  materials = tuple(sorted(
    (
      _read_material(root, selection)
      for selection in selection_values
    ),
    key=lambda material: material.identifier,
  ))
  return MaterialBundle(
    materials=materials,
    digest=calculate_bundle_digest(materials),
  )
