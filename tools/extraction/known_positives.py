"""第2段の既知正例再発見。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
from pathlib import PurePosixPath
import re


class KnownPositiveRediscoveryError(Exception):
  """既知正例を安全に再発見できない。"""


class MissingKnownPositiveError(
  KnownPositiveRediscoveryError
):
  """計画上の既知正例に必要な証拠を再発見できない。"""

  def __init__(self, missing_requirements):
    self.missing_requirements = tuple(
      sorted(missing_requirements)
    )
    super().__init__(
      "Missing known positive requirements: %s"
      % ", ".join(self.missing_requirements)
    )


@dataclasses.dataclass(frozen=True)
class KnownPositiveRequirement:
  responsibility: str
  source: str
  path_pattern: str


@dataclasses.dataclass(frozen=True)
class KnownPositiveGroup:
  identifier: str
  requirements: tuple


@dataclasses.dataclass(frozen=True)
class KnownPositiveEvidence:
  responsibility: str
  candidates: tuple


@dataclasses.dataclass(frozen=True)
class RediscoveredKnownPositive:
  identifier: str
  evidence: tuple


@dataclasses.dataclass(frozen=True)
class KnownPositiveReport:
  status: str
  groups: tuple
  digest: str


KNOWN_POSITIVE_GROUPS = (
  KnownPositiveGroup(
    identifier="absolute_path_contamination_lint",
    requirements=(
      KnownPositiveRequirement(
        "implementation",
        "ReviewCompass2",
        r"tools/(?:lint/)?deployment_independence_lint\.py",
      ),
      KnownPositiveRequirement(
        "tests",
        "ReviewCompass2",
        r"tests/test_deployment_independence_lint\.py",
      ),
    ),
  ),
  KnownPositiveGroup(
    identifier="current_advantages_inventory",
    requirements=(
      KnownPositiveRequirement(
        "inventory",
        "ReviewCompass2",
        r"docs/design/[^/]*current-advantages-inventory\.md",
      ),
    ),
  ),
  KnownPositiveGroup(
    identifier="extracted_1416_rules",
    requirements=(
      KnownPositiveRequirement(
        "extraction",
        "ReviewCompass2",
        (
          r"\.reviewcompass/evidence/reviews/"
          r"[^/]*(?:collect|recount)-rules[^/]*\.py"
        ),
      ),
      KnownPositiveRequirement(
        "ledger",
        "ReviewCompass2",
        (
          r"\.reviewcompass/evidence/reviews/"
          r"[^/]*ref-impl-(?:enforced|uncovered)-rules"
          r"(?:-recount)?\.json"
        ),
      ),
    ),
  ),
  KnownPositiveGroup(
    identifier="known_failures_and_mutation_knowledge",
    requirements=(
      KnownPositiveRequirement(
        "implementation",
        "ReviewCompass",
        r"tools/check_workflow_action/mutation_gate\.py",
      ),
      KnownPositiveRequirement(
        "tests",
        "ReviewCompass",
        r"tests/tools/test_t023_mutation_gate\.py",
      ),
      KnownPositiveRequirement(
        "precheck",
        "ReviewCompass",
        r"templates/hooks/mutation-gate-precheck\.sh\.template",
      ),
    ),
  ),
  KnownPositiveGroup(
    identifier="review_material_lifecycle",
    requirements=(
      KnownPositiveRequirement(
        "preparation",
        "ReviewCompass",
        (
          r"tools/api_providers/(?:source_bundle|"
          r"source_scope_assurance|source_scope_guard|"
          r"review_input_guard|change_inventory|"
          r"risk_review_contracts|risk_review_materializer)\.py"
        ),
      ),
      KnownPositiveRequirement(
        "execution",
        "ReviewCompass",
        (
          r"tools/api_providers/(?:assurance_pipeline|"
          r"run_risk_review|trusted_review_send)\.py"
        ),
      ),
      KnownPositiveRequirement(
        "recording",
        "ReviewCompass",
        r"tools/api_providers/risk_review_store\.py",
      ),
      KnownPositiveRequirement(
        "tests",
        "ReviewCompass",
        (
          r"tools/api_providers/tests/test_(?:source_bundle|"
          r"source_scope|review_input|change_inventory|"
          r"risk_review|run_risk_review|assurance_pipeline|"
          r"trusted_review)"
          r"[^/]*\.py"
        ),
      ),
    ),
  ),
  KnownPositiveGroup(
    identifier="session_log_implementation_and_tests",
    requirements=(
      KnownPositiveRequirement(
        "implementation",
        "ReviewCompass2",
        r"tools/session_capture/(?!__init__)[^/]+\.py",
      ),
      KnownPositiveRequirement(
        "tests",
        "ReviewCompass2",
        r"tests/test_session_capture_[^/]+\.py",
      ),
    ),
  ),
  KnownPositiveGroup(
    identifier="user_decisions_ud_001_093",
    requirements=(
      KnownPositiveRequirement(
        "inventory",
        "ReviewCompass2",
        r"docs/design/[^/]*user-decisions-inventory\.md",
      ),
      KnownPositiveRequirement(
        "extraction",
        "ReviewCompass2",
        (
          r"\.reviewcompass/evidence/reviews/"
          r"[^/]*extract-user-decisions\.py"
        ),
      ),
    ),
  ),
)

KNOWN_POSITIVE_GROUP_IDS = tuple(
  group.identifier
  for group in KNOWN_POSITIVE_GROUPS
)


def _parse_population(population):
  values = tuple(population)
  if len(set(values)) != len(values):
    raise KnownPositiveRediscoveryError(
      "Population identifiers must be unique"
    )
  parsed = []
  for identifier in values:
    if (
      not isinstance(identifier, str)
      or identifier.count(":") != 1
      or "\x00" in identifier
      or "\n" in identifier
    ):
      raise KnownPositiveRediscoveryError(
        "Population identifiers require source:path"
      )
    source, path_value = identifier.split(":", 1)
    path = PurePosixPath(path_value)
    if (
      not source
      or not path_value
      or path.is_absolute()
      or path_value != path.as_posix()
      or any(part in {"", ".", ".."} for part in path.parts)
    ):
      raise KnownPositiveRediscoveryError(
        "Population paths must be safe relative POSIX paths"
      )
    parsed.append((identifier, source, path_value))
  return tuple(parsed)


def _discover_group(group, population):
  evidence = []
  missing = []
  for requirement in group.requirements:
    candidates = tuple(sorted(
      identifier
      for identifier, source, path_value in population
      if (
        source == requirement.source
        and re.fullmatch(
          requirement.path_pattern,
          path_value,
        )
      )
    ))
    if not candidates:
      missing.append(
        f"{group.identifier}:{requirement.responsibility}"
      )
    evidence.append(KnownPositiveEvidence(
      responsibility=requirement.responsibility,
      candidates=candidates,
    ))
  return (
    RediscoveredKnownPositive(
      identifier=group.identifier,
      evidence=tuple(evidence),
    ),
    tuple(missing),
  )


def rediscover_known_positives(
  included_population,
  *,
  groups=KNOWN_POSITIVE_GROUPS,
) -> KnownPositiveReport:
  population = _parse_population(included_population)
  group_values = tuple(groups)
  identifiers = tuple(
    group.identifier
    for group in group_values
  )
  if (
    not group_values
    or len(set(identifiers)) != len(identifiers)
    or identifiers != tuple(sorted(identifiers))
  ):
    raise KnownPositiveRediscoveryError(
      "Known positive groups must be unique and sorted"
    )

  rediscovered = []
  missing = []
  for group in group_values:
    result, group_missing = _discover_group(
      group,
      population,
    )
    rediscovered.append(result)
    missing.extend(group_missing)
  if missing:
    raise MissingKnownPositiveError(missing)

  document = {
    "groups": [
      {
        "evidence": [
          {
            "candidates": list(evidence.candidates),
            "responsibility": evidence.responsibility,
          }
          for evidence in group.evidence
        ],
        "identifier": group.identifier,
      }
      for group in rediscovered
    ],
    "schema_version": 1,
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return KnownPositiveReport(
    status="complete",
    groups=tuple(rediscovered),
    digest=digest,
  )
