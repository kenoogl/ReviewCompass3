"""材料束の内部整合性・原文一致・stale検査。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
from pathlib import Path, PurePosixPath

from tools.bootstrap.material_bundle import (
  BundledMaterial,
  MaterialBundle,
  calculate_bundle_digest,
)


class BundleVerificationError(Exception):
  """材料束を安全に検査できない。"""


class BundleIntegrityError(BundleVerificationError):
  """材料束の内部整合性が壊れている。"""


@dataclasses.dataclass(frozen=True)
class BundleVerification:
  status: str
  stale_identifiers: tuple


def _safe_identifier(identifier):
  if not isinstance(identifier, str):
    return False
  path = PurePosixPath(identifier)
  return (
    bool(identifier)
    and "\\" not in identifier
    and "\x00" not in identifier
    and "\n" not in identifier
    and not path.is_absolute()
    and path.as_posix() == identifier
    and all(part not in ("", ".", "..") for part in path.parts)
  )


def _verify_bundle_integrity(bundle):
  if not isinstance(bundle, MaterialBundle):
    raise BundleIntegrityError(
      "Expected a material bundle"
    )
  identifiers = []
  for material in bundle.materials:
    if (
      not isinstance(material, BundledMaterial)
      or not _safe_identifier(material.identifier)
      or not isinstance(material.content, str)
      or hashlib.sha256(
        material.content.encode("utf-8")
      ).hexdigest() != material.content_sha256
    ):
      raise BundleIntegrityError(
        "Material body or digest is inconsistent"
      )
    identifiers.append(material.identifier)
  if (
    identifiers != sorted(identifiers)
    or len(set(identifiers)) != len(identifiers)
    or calculate_bundle_digest(bundle.materials) != bundle.digest
  ):
    raise BundleIntegrityError(
      "Material bundle digest or ordering is inconsistent"
    )


def _original_matches(root, material):
  path = root
  for part in PurePosixPath(material.identifier).parts:
    path = path / part
    if path.is_symlink():
      return False
  if not path.is_file():
    return False
  try:
    body = path.read_bytes()
  except OSError:
    return False
  return (
    body == material.content.encode("utf-8")
    and hashlib.sha256(body).hexdigest()
    == material.content_sha256
  )


def verify_material_bundle(repository_root, bundle) -> BundleVerification:
  _verify_bundle_integrity(bundle)
  root = Path(repository_root).resolve()
  if not root.is_dir():
    raise BundleVerificationError(
      "Verification root must be an existing directory"
    )
  stale_identifiers = tuple(
    material.identifier
    for material in bundle.materials
    if not _original_matches(root, material)
  )
  return BundleVerification(
    status="stale" if stale_identifiers else "matches",
    stale_identifiers=stale_identifiers,
  )
