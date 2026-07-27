"""第2段の7軸初回抽出に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


AXES = (
  "user_decision",
  "capability",
  "procedure",
  "invariant",
  "contract",
  "recovery",
  "empirical_finding",
)


def _candidate(index, axis, **overrides):
  value = {
    "identifier": f"ESS-{index:04d}",
    "statement": f"{axis}の抽出項目",
    "axis": axis,
    "evidence": (
      "ReviewCompass:docs/source.md#L1-L3",
    ),
    "dependencies": (),
  }
  value.update(overrides)
  return value


def test_extracts_all_seven_axes_with_resolved_evidence():
  extraction = importlib.import_module(
    "tools.extraction.seven_axes"
  )
  candidates = [
    _candidate(index, axis)
    for index, axis in enumerate(AXES, start=1)
  ]
  candidates[1]["dependencies"] = ("ESS-0001",)

  result = extraction.extract_initial_essences(
    candidates,
    source_materials=("ReviewCompass:docs/source.md",),
  )

  assert result.status == "complete"
  assert tuple(
    item.axis.value
    for item in result.accepted
  ) == AXES
  assert result.rejected == ()
  assert result.missing_axes == ()
  assert result.accepted[1].dependencies == ("ESS-0001",)
  assert len(result.digest) == 64


def test_blocks_and_isolates_unclassifiable_or_unsubstantiated_candidates():
  extraction = importlib.import_module(
    "tools.extraction.seven_axes"
  )
  candidates = [
    _candidate(index, axis)
    for index, axis in enumerate(AXES, start=1)
  ]
  candidates.append(_candidate(
    8,
    "unknown",
  ))
  candidates.append(_candidate(
    9,
    "contract",
    evidence=(),
  ))
  candidates.append(_candidate(
    10,
    "recovery",
    evidence=("ReviewCompass:missing.md#L1",),
  ))
  candidates.append(_candidate(
    11,
    "procedure",
    dependencies=("ESS-9999",),
  ))

  result = extraction.extract_initial_essences(
    candidates,
    source_materials=("ReviewCompass:docs/source.md",),
  )

  assert result.status == "blocked"
  assert tuple(
    candidate.identifier
    for candidate in result.rejected
  ) == (
    "ESS-0008",
    "ESS-0009",
    "ESS-0010",
    "ESS-0011",
  )
  assert tuple(
    candidate.reason
    for candidate in result.rejected
  ) == (
    "unknown_axis",
    "missing_evidence",
    "unresolved_evidence",
    "unresolved_dependency",
  )
  assert all(
    item.identifier
    not in {
      "ESS-0008",
      "ESS-0009",
      "ESS-0010",
      "ESS-0011",
    }
    for item in result.accepted
  )


def test_reports_missing_axis_coverage():
  extraction = importlib.import_module(
    "tools.extraction.seven_axes"
  )

  result = extraction.extract_initial_essences(
    (_candidate(1, "user_decision"),),
    source_materials=("ReviewCompass:docs/source.md",),
  )

  assert result.status == "blocked"
  assert result.missing_axes == (
    "capability",
    "procedure",
    "invariant",
    "contract",
    "recovery",
    "empirical_finding",
  )


def test_rejects_duplicate_candidate_identifiers():
  extraction = importlib.import_module(
    "tools.extraction.seven_axes"
  )

  with pytest.raises(extraction.SevenAxisExtractionError):
    extraction.extract_initial_essences(
      (
        _candidate(1, "user_decision"),
        _candidate(1, "capability"),
      ),
      source_materials=("ReviewCompass:docs/source.md",),
    )
