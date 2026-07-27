"""第2段の抽出母集団分類に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_classifies_every_source_into_exactly_one_partition():
  population = importlib.import_module(
    "tools.extraction.population"
  )
  universe = (
    "ReviewCompass:tools/main.py",
    "ReviewCompass:docs/decision.md",
    "ReviewCompass2:tests/test_main.py",
  )
  decisions = (
    {
      "identifier": "ReviewCompass:tools/main.py",
      "disposition": "include",
      "rationale": "implementation evidence",
    },
    {
      "identifier": "ReviewCompass:docs/decision.md",
      "disposition": "defer",
      "rationale": "await dependency expansion",
    },
    {
      "identifier": "ReviewCompass2:tests/test_main.py",
      "disposition": "exclude",
      "rationale": "duplicate fixture",
    },
  )

  result = population.classify_extraction_population(
    universe,
    decisions,
  )

  assert result.status == "complete"
  assert result.included == ("ReviewCompass:tools/main.py",)
  assert result.excluded == (
    "ReviewCompass2:tests/test_main.py",
  )
  assert result.deferred == (
    "ReviewCompass:docs/decision.md",
  )
  assert result.unknown == ()
  assert len(result.digest) == 64


def test_keeps_unclassified_sources_as_blocking_unknown():
  population = importlib.import_module(
    "tools.extraction.population"
  )

  result = population.classify_extraction_population(
    ("source:a.py", "source:b.md"),
    ({
      "identifier": "source:a.py",
      "disposition": "include",
      "rationale": "implementation evidence",
    },),
  )

  assert result.status == "blocked"
  assert result.unknown == ("source:b.md",)


def test_include_all_policy_keeps_non_code_evidence_in_population():
  population = importlib.import_module(
    "tools.extraction.population"
  )
  universe = (
    "source:tools/main.py",
    "source:tests/test_main.py",
    "source:docs/decision.md",
    "source:records/session.json",
  )

  result = population.include_entire_population(universe)

  assert result.status == "complete"
  assert result.included == tuple(sorted(universe))
  assert result.excluded == ()
  assert result.deferred == ()


@pytest.mark.parametrize(
  "decisions",
  (
    ({
      "identifier": "source:a.py",
      "disposition": "unknown",
      "rationale": "invalid",
    },),
    (
      {
        "identifier": "source:a.py",
        "disposition": "include",
        "rationale": "first",
      },
      {
        "identifier": "source:a.py",
        "disposition": "exclude",
        "rationale": "duplicate",
      },
    ),
    ({
      "identifier": "source:outside.py",
      "disposition": "include",
      "rationale": "outside",
    },),
  ),
)
def test_rejects_invalid_duplicate_or_outside_decisions(decisions):
  population = importlib.import_module(
    "tools.extraction.population"
  )

  with pytest.raises(population.PopulationClassificationError):
    population.classify_extraction_population(
      ("source:a.py",),
      decisions,
    )
