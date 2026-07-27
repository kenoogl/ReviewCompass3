"""閉鎖payload生成の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import importlib
import json

import pytest


def _review_state(repository):
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )
  material_bundle = importlib.import_module(
    "tools.bootstrap.material_bundle"
  )
  evidence_closure = importlib.import_module(
    "tools.bootstrap.evidence_closure"
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
  bundle = material_bundle.build_material_bundle(
    repository,
    materials,
  )
  closure = evidence_closure.assess_evidence_closure(
    ("reference.md", "target.md"),
    bundle,
    required_identifiers=(),
  )
  return bundle, closure


def test_builds_approved_closed_payload_with_all_material_bodies(tmp_path):
  repository = tmp_path / "repository"
  repository.mkdir()
  (repository / "target.md").write_text("target\n", encoding="utf-8")
  (repository / "reference.md").write_text(
    "reference\n",
    encoding="utf-8",
  )
  bundle, closure = _review_state(repository)
  closed_payload = importlib.import_module(
    "tools.bootstrap.closed_payload"
  )
  target_digest = closed_payload.calculate_target_digest(bundle)
  approval = closed_payload.PayloadApproval(
    approved=True,
    bundle_digest=bundle.digest,
    target_digest=target_digest,
  )

  payload = closed_payload.build_closed_payload(
    repository,
    bundle,
    closure,
    approval,
  )

  document = json.loads(payload.content)
  assert document["bundle_digest"] == bundle.digest
  assert document["target_digest"] == target_digest
  assert [
    material["identifier"]
    for material in document["materials"]
  ] == ["reference.md", "target.md"]
  assert [
    material["content"]
    for material in document["materials"]
  ] == ["reference\n", "target\n"]
  assert str(repository) not in payload.content
  assert payload.digest == hashlib.sha256(
    payload.content.encode("utf-8")
  ).hexdigest()


@pytest.mark.parametrize(
  "rejection",
  (
    "unapproved",
    "bundle_digest",
    "target_digest",
    "stale",
    "incomplete",
  ),
)
def test_rejects_payload_without_current_approved_closed_bundle(
  tmp_path,
  rejection,
):
  repository = tmp_path / "repository"
  repository.mkdir()
  target = repository / "target.md"
  target.write_text("target\n", encoding="utf-8")
  (repository / "reference.md").write_text(
    "reference\n",
    encoding="utf-8",
  )
  bundle, closure = _review_state(repository)
  closed_payload = importlib.import_module(
    "tools.bootstrap.closed_payload"
  )
  approval = closed_payload.PayloadApproval(
    approved=rejection != "unapproved",
    bundle_digest=(
      "0" * 64
      if rejection == "bundle_digest"
      else bundle.digest
    ),
    target_digest=(
      "0" * 64
      if rejection == "target_digest"
      else closed_payload.calculate_target_digest(bundle)
    ),
  )
  if rejection == "stale":
    target.write_text("changed\n", encoding="utf-8")
  if rejection == "incomplete":
    closure = dataclasses.replace(
      closure,
      status="insufficient",
      uncovered_source=("target.md",),
    )

  with pytest.raises(closed_payload.ClosedPayloadError):
    closed_payload.build_closed_payload(
      repository,
      bundle,
      closure,
      approval,
    )
