"""ブートストラップreview pipeline統括の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def _inputs(repository):
  review_materials = importlib.import_module(
    "tools.bootstrap.review_materials"
  )
  material_bundle = importlib.import_module(
    "tools.bootstrap.material_bundle"
  )
  closed_payload = importlib.import_module(
    "tools.bootstrap.closed_payload"
  )
  review_execution = importlib.import_module(
    "tools.bootstrap.review_execution"
  )
  selections = review_materials.classify_materials((
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
    selections,
  )
  approval = closed_payload.PayloadApproval(
    True,
    bundle.digest,
    closed_payload.calculate_target_digest(bundle),
  )
  assignments = (
    review_execution.ReviewAssignment(
      "main",
      "fixture",
      "main-model",
      "main",
    ),
    review_execution.ReviewAssignment(
      "independent",
      "fixture",
      "independent-model",
      "independent",
    ),
  )
  return selections, approval, assignments


@pytest.mark.parametrize("failed_assignment", (None, "independent"))
def test_runs_fixed_pipeline_or_stops_with_preserved_raw(
  tmp_path,
  failed_assignment,
):
  repository = tmp_path / "repository"
  repository.mkdir()
  (repository / "target.md").write_text("target\n", encoding="utf-8")
  (repository / "reference.md").write_text(
    "reference\n",
    encoding="utf-8",
  )
  selections, approval, assignments = _inputs(repository)
  review_pipeline = importlib.import_module(
    "tools.bootstrap.review_pipeline"
  )
  response = json.dumps({
    "schema_version": 1,
    "findings": [],
    "summary": "ok",
  })

  def runner(assignment, _content):
    if assignment.name == failed_assignment:
      raise RuntimeError("provider unavailable")
    return response

  result = review_pipeline.run_review_pipeline(
    repository_root=repository,
    source_universe=("reference.md", "target.md"),
    selections=selections,
    required_identifiers=(),
    approval=approval,
    assignments=assignments,
    storage_root=tmp_path / "raw",
    attempt_id="attempt-001",
    runner=runner,
  )

  assert len(result.raw_records) == 2
  assert tuple(stage.name for stage in result.stages)[:4] == (
    "bundle",
    "closure",
    "contract",
    "execute",
  )
  if failed_assignment is None:
    assert result.status == "completed"
    assert result.stop_reason is None
    assert result.triage is not None
  else:
    assert result.status == "blocked"
    assert result.stop_reason == "assignment_failed"
    assert result.triage is None
    assert len(result.parsed_reviews) == 1
