"""承認済み材料束からの閉鎖payload生成。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json

from tools.bootstrap.bundle_verification import (
  BundleVerificationError,
  verify_material_bundle,
)
from tools.bootstrap.evidence_closure import EvidenceClosure
from tools.bootstrap.material_bundle import (
  MaterialBundle,
  calculate_bundle_digest,
)
from tools.bootstrap.review_materials import MaterialRole


class ClosedPayloadError(Exception):
  """現在有効な承認済み閉鎖payloadを生成できない。"""


@dataclasses.dataclass(frozen=True)
class PayloadApproval:
  approved: bool
  bundle_digest: str
  target_digest: str


@dataclasses.dataclass(frozen=True)
class ClosedPayload:
  content: str
  digest: str
  bundle_digest: str
  target_digest: str
  material_identifiers: tuple


def _material_document(material):
  return {
    "content": material.content,
    "content_sha256": material.content_sha256,
    "identifier": material.identifier,
    "role": material.role.value,
    "route": material.route.value,
  }


def calculate_target_digest(bundle) -> str:
  if not isinstance(bundle, MaterialBundle):
    raise ClosedPayloadError(
      "Target digest requires a material bundle"
    )
  targets = tuple(
    material
    for material in bundle.materials
    if material.role == MaterialRole.TARGET
  )
  if not targets:
    raise ClosedPayloadError(
      "Closed payload requires at least one target"
    )
  encoded = json.dumps(
    {
      "schema_version": 1,
      "targets": [
        _material_document(material)
        for material in targets
      ],
    },
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode("utf-8")
  return hashlib.sha256(encoded).hexdigest()


def _verify_closure(bundle, closure):
  if (
    not isinstance(closure, EvidenceClosure)
    or closure.status != "complete"
    or closure.missing_required
    or closure.uncovered_source
    or closure.missing_routes
  ):
    raise ClosedPayloadError(
      "Closed payload requires complete evidence closure"
    )
  bundled = {
    material.identifier
    for material in bundle.materials
  }
  main = set(closure.main_materials)
  independent = set(closure.independent_materials)
  if (
    main & independent
    or main | independent != bundled
  ):
    raise ClosedPayloadError(
      "Evidence closure does not match the material bundle"
    )


def _verify_approval(bundle, approval, target_digest):
  if (
    not isinstance(approval, PayloadApproval)
    or approval.approved is not True
    or approval.bundle_digest != bundle.digest
    or approval.target_digest != target_digest
  ):
    raise ClosedPayloadError(
      "Closed payload requires approval for current digests"
    )


def build_closed_payload(
  repository_root,
  bundle,
  closure,
  approval,
) -> ClosedPayload:
  if (
    not isinstance(bundle, MaterialBundle)
    or calculate_bundle_digest(bundle.materials) != bundle.digest
  ):
    raise ClosedPayloadError(
      "Closed payload requires an intact material bundle"
    )
  _verify_closure(bundle, closure)
  try:
    verification = verify_material_bundle(
      repository_root,
      bundle,
    )
  except BundleVerificationError as error:
    raise ClosedPayloadError(
      "Closed payload requires a verifiable material bundle"
    ) from error
  if verification.status != "matches":
    raise ClosedPayloadError(
      "Closed payload refuses stale source materials"
    )

  target_digest = calculate_target_digest(bundle)
  _verify_approval(bundle, approval, target_digest)
  document = {
    "bundle_digest": bundle.digest,
    "materials": [
      _material_document(material)
      for material in bundle.materials
    ],
    "schema_version": 1,
    "target_digest": target_digest,
  }
  content = json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  )
  return ClosedPayload(
    content=content,
    digest=hashlib.sha256(
      content.encode("utf-8")
    ).hexdigest(),
    bundle_digest=bundle.digest,
    target_digest=target_digest,
    material_identifiers=tuple(
      material.identifier
      for material in bundle.materials
    ),
  )
