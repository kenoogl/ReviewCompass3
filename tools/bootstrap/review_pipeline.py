"""ブートストラップreview pipelineの固定統括。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses

from tools.bootstrap.closed_payload import build_closed_payload
from tools.bootstrap.evidence_closure import assess_evidence_closure
from tools.bootstrap.material_bundle import build_material_bundle
from tools.bootstrap.raw_review_store import store_raw_executions
from tools.bootstrap.review_contract import materialize_review_contract
from tools.bootstrap.review_execution import execute_review_assignments
from tools.bootstrap.review_response_parser import parse_raw_review_record
from tools.bootstrap.review_triage import triage_parsed_reviews


class ReviewPipelineError(Exception):
  """固定review pipelineを安全に実行できない。"""


@dataclasses.dataclass(frozen=True)
class PipelineStage:
  name: str
  status: str


@dataclasses.dataclass(frozen=True)
class ReviewPipelineResult:
  status: str
  stages: tuple
  stop_reason: object
  contracted_payload_digest: object
  raw_records: tuple
  parsed_reviews: tuple
  triage: object


def run_review_pipeline(
  *,
  repository_root,
  source_universe,
  selections,
  required_identifiers,
  approval,
  assignments,
  storage_root,
  attempt_id,
  runner,
) -> ReviewPipelineResult:
  stages = []
  try:
    bundle = build_material_bundle(
      repository_root,
      selections,
    )
    stages.append(PipelineStage("bundle", "completed"))
    closure = assess_evidence_closure(
      source_universe,
      bundle,
      required_identifiers=required_identifiers,
    )
    stages.append(PipelineStage("closure", closure.status))
    if closure.status != "complete":
      return ReviewPipelineResult(
        "blocked",
        tuple(stages),
        "insufficient_materials",
        None,
        (),
        (),
        None,
      )
    closed = build_closed_payload(
      repository_root,
      bundle,
      closure,
      approval,
    )
    contracted = materialize_review_contract(closed)
    stages.append(PipelineStage("contract", "completed"))
    executions = execute_review_assignments(
      contracted,
      assignments,
      runner=runner,
    )
    stages.append(PipelineStage("execute", "completed"))
    records = store_raw_executions(
      storage_root,
      attempt_id,
      executions,
    )
    stages.append(PipelineStage("raw_store", "completed"))
    parsed = tuple(
      parse_raw_review_record(storage_root, record)
      for record in records
      if record.status == "succeeded"
    )
    stages.append(PipelineStage("parse", "completed"))
    if any(
      execution.status == "failed"
      for execution in executions
    ):
      return ReviewPipelineResult(
        "blocked",
        tuple(stages),
        "assignment_failed",
        contracted.digest,
        records,
        parsed,
        None,
      )
    triage = triage_parsed_reviews(parsed)
    stages.append(PipelineStage("triage", "completed"))
    return ReviewPipelineResult(
      "completed",
      tuple(stages),
      None,
      contracted.digest,
      records,
      parsed,
      triage,
    )
  except Exception as error:
    raise ReviewPipelineError(
      "Review pipeline failed before a structured stop"
    ) from error
