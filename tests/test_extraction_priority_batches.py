"""優先度付き抽出batchに関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_builds_dependency_first_then_layered_batches():
  priority = importlib.import_module(
    "tools.extraction.priority_batches"
  )
  population = (
    "source:tools/dependency.py",
    "source:.reviewcompass/specs/unit.yaml",
    "source:tools/app.py",
    "source:tests/test_app.py",
    "source:docs/design/spec.md",
    "source:.reviewcompass/backlog/issues/issue.yaml",
    "source:docs/sessions/session.md",
    "source:.reviewcompass/evidence/tests/green.txt",
    "source:README.md",
  )

  result = priority.build_priority_batches(
    population,
    covered=("source:README.md",),
    dependency_materials=("source:tools/dependency.py",),
    batch_size=2,
  )

  assert result.status == "complete"
  assert tuple(batch.layer for batch in result.batches) == (
    "dependency_materials",
    "structured_materials",
    "implementation",
    "tests",
    "specifications",
    "issues",
    "sessions",
    "empirical_records",
  )
  assert result.batches[0].candidates == (
    "source:tools/dependency.py",
  )
  assert result.scheduled_count == 8
  assert result.unscheduled == ()


def test_resolves_every_candidate_in_one_batch():
  priority = importlib.import_module(
    "tools.extraction.priority_batches"
  )
  batch = priority.PriorityBatch(
    identifier="dependency_materials-0001",
    layer="dependency_materials",
    candidates=("source:a.py", "source:b.py"),
  )

  result = priority.resolve_priority_batch(
    batch,
    (
      {
        "candidate": "source:a.py",
        "action": "extract",
        "essence_id": "ESS-0014",
        "rationale": "独立したパス解決規約",
      },
      {
        "candidate": "source:b.py",
        "action": "not_selected",
        "essence_id": None,
        "rationale": "既存項目の関連テスト",
      },
    ),
  )

  assert result.status == "complete"
  assert result.extracted == (("source:a.py", "ESS-0014"),)
  assert result.not_selected == ("source:b.py",)
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "resolutions",
  (
    (),
    ({
      "candidate": "source:a.py",
      "action": "not_selected",
      "essence_id": None,
      "rationale": "",
    },),
    ({
      "candidate": "source:outside.py",
      "action": "extract",
      "essence_id": "ESS-0014",
      "rationale": "範囲外",
    },),
  ),
)
def test_rejects_incomplete_unreasoned_or_outside_batch(resolutions):
  priority = importlib.import_module(
    "tools.extraction.priority_batches"
  )
  batch = priority.PriorityBatch(
    identifier="dependency_materials-0001",
    layer="dependency_materials",
    candidates=("source:a.py",),
  )

  with pytest.raises(priority.PriorityBatchError):
    priority.resolve_priority_batch(batch, resolutions)
