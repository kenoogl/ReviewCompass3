"""第2段の既知正例再発見に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


KNOWN_POSITIVE_GROUP_IDS = (
  "absolute_path_contamination_lint",
  "current_advantages_inventory",
  "extracted_1416_rules",
  "known_failures_and_mutation_knowledge",
  "review_material_lifecycle",
  "session_log_implementation_and_tests",
  "user_decisions_ud_001_093",
)


def _fixture_population():
  return (
    "ReviewCompass2:tools/session_capture/capture.py",
    "ReviewCompass2:tests/test_session_capture_command.py",
    "ReviewCompass2:tools/lint/deployment_independence_lint.py",
    "ReviewCompass2:tests/test_deployment_independence_lint.py",
    "ReviewCompass2:docs/design/2026-user-decisions-inventory.md",
    "ReviewCompass2:.reviewcompass/evidence/reviews/extract-user-decisions.py",
    "ReviewCompass2:docs/design/2026-current-advantages-inventory.md",
    "ReviewCompass2:.reviewcompass/evidence/reviews/collect-rules-pass1.py",
    "ReviewCompass2:.reviewcompass/evidence/reviews/ref-impl-enforced-rules.json",
    "ReviewCompass:tools/check_workflow_action/mutation_gate.py",
    "ReviewCompass:tests/tools/test_t023_mutation_gate.py",
    "ReviewCompass:templates/hooks/mutation-gate-precheck.sh.template",
    "ReviewCompass:tools/api_providers/source_bundle.py",
    "ReviewCompass:tools/api_providers/run_risk_review.py",
    "ReviewCompass:tools/api_providers/risk_review_store.py",
    "ReviewCompass:tools/api_providers/tests/test_run_risk_review.py",
  )


def test_rediscovers_plan_groups_by_responsibility_contract():
  known_positives = importlib.import_module(
    "tools.extraction.known_positives"
  )

  result = known_positives.rediscover_known_positives(
    _fixture_population()
  )

  assert result.status == "complete"
  assert tuple(
    group.identifier
    for group in result.groups
  ) == KNOWN_POSITIVE_GROUP_IDS
  session_group = next(
    group
    for group in result.groups
    if group.identifier
    == "session_log_implementation_and_tests"
  )
  assert tuple(
    evidence.responsibility
    for evidence in session_group.evidence
  ) == ("implementation", "tests")
  assert session_group.evidence[0].candidates == (
    "ReviewCompass2:tools/session_capture/capture.py",
  )
  assert len(result.digest) == 64


def test_fails_closed_with_group_and_responsibility_when_evidence_is_missing():
  known_positives = importlib.import_module(
    "tools.extraction.known_positives"
  )
  population = tuple(
    identifier
    for identifier in _fixture_population()
    if identifier
    != "ReviewCompass2:tests/test_session_capture_command.py"
  )

  with pytest.raises(
    known_positives.MissingKnownPositiveError
  ) as error:
    known_positives.rediscover_known_positives(population)

  assert error.value.missing_requirements == (
    "session_log_implementation_and_tests:tests",
  )


@pytest.mark.parametrize(
  "population",
  (
    (
      "ReviewCompass2:tools/session_capture/capture.py",
      "ReviewCompass2:tools/session_capture/capture.py",
    ),
    ("missing-source-separator.py",),
    ("ReviewCompass2:/absolute/path.py",),
    ("ReviewCompass2:nested/../escape.py",),
  ),
)
def test_rejects_ambiguous_or_unsafe_population_identifiers(population):
  known_positives = importlib.import_module(
    "tools.extraction.known_positives"
  )

  with pytest.raises(
    known_positives.KnownPositiveRediscoveryError
  ):
    known_positives.rediscover_known_positives(population)


def test_default_group_ids_match_the_rebuild_plan():
  known_positives = importlib.import_module(
    "tools.extraction.known_positives"
  )

  assert known_positives.KNOWN_POSITIVE_GROUP_IDS == (
    KNOWN_POSITIVE_GROUP_IDS
  )
