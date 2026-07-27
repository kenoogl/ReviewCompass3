"""複数担当の所見統合とtriage。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json

from tools.bootstrap.review_response_parser import ParsedReview


class ReviewTriageError(Exception):
  """parsedレビュー集合を安全にtriageできない。"""


@dataclasses.dataclass(frozen=True)
class TriagedFinding:
  identifier: str
  disposition: str
  severities: tuple
  titles: tuple
  descriptions: tuple
  material_identifiers: tuple
  reporters: tuple


@dataclasses.dataclass(frozen=True)
class ReviewTriage:
  contracted_payload_digest: str
  raw_digests: tuple
  parsed_digests: tuple
  findings: tuple
  digest: str


def _validate_reviews(parsed_reviews):
  reviews = tuple(parsed_reviews)
  if (
    not reviews
    or any(
      not isinstance(review, ParsedReview)
      for review in reviews
    )
  ):
    raise ReviewTriageError(
      "Triage requires parsed reviews"
    )
  assignment_names = tuple(
    review.assignment_name
    for review in reviews
  )
  routes = {
    review.route
    for review in reviews
  }
  payload_digests = {
    review.contracted_payload_digest
    for review in reviews
  }
  if (
    len(set(assignment_names)) != len(assignment_names)
    or routes != {"main", "independent"}
    or len(payload_digests) != 1
    or any(
      len(review.raw_digest) != 64
      or len(review.digest) != 64
      for review in reviews
    )
  ):
    raise ReviewTriageError(
      "Triage requires both routes on one contracted payload"
    )
  return tuple(sorted(
    reviews,
    key=lambda review: review.assignment_name,
  ))


def _triage_group(identifier, entries):
  signatures = {
    (
      finding.severity,
      finding.title,
      finding.description,
      finding.material_identifiers,
    )
    for _reporter, finding in entries
  }
  if len(entries) == 1:
    disposition = "single"
  elif len(signatures) == 1:
    disposition = "corroborated"
  else:
    disposition = "conflict"
  return TriagedFinding(
    identifier=identifier,
    disposition=disposition,
    severities=tuple(sorted({
      finding.severity
      for _reporter, finding in entries
    })),
    titles=tuple(sorted({
      finding.title
      for _reporter, finding in entries
    })),
    descriptions=tuple(sorted({
      finding.description
      for _reporter, finding in entries
    })),
    material_identifiers=tuple(sorted({
      material
      for _reporter, finding in entries
      for material in finding.material_identifiers
    })),
    reporters=tuple(sorted(
      reporter
      for reporter, _finding in entries
    )),
  )


def _finding_document(finding):
  return {
    "descriptions": list(finding.descriptions),
    "disposition": finding.disposition,
    "id": finding.identifier,
    "material_identifiers": list(
      finding.material_identifiers
    ),
    "reporters": list(finding.reporters),
    "severities": list(finding.severities),
    "titles": list(finding.titles),
  }


def triage_parsed_reviews(parsed_reviews) -> ReviewTriage:
  reviews = _validate_reviews(parsed_reviews)
  grouped = {}
  for review in reviews:
    for finding in review.findings:
      grouped.setdefault(finding.identifier, []).append((
        review.assignment_name,
        finding,
      ))
  findings = tuple(
    _triage_group(identifier, grouped[identifier])
    for identifier in sorted(grouped)
  )
  raw_digests = tuple(sorted(
    review.raw_digest
    for review in reviews
  ))
  parsed_digests = tuple(sorted(
    review.digest
    for review in reviews
  ))
  contracted_payload_digest = (
    reviews[0].contracted_payload_digest
  )
  document = {
    "contracted_payload_digest": contracted_payload_digest,
    "findings": [
      _finding_document(finding)
      for finding in findings
    ],
    "parsed_digests": list(parsed_digests),
    "raw_digests": list(raw_digests),
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return ReviewTriage(
    contracted_payload_digest=contracted_payload_digest,
    raw_digests=raw_digests,
    parsed_digests=parsed_digests,
    findings=findings,
    digest=digest,
  )
