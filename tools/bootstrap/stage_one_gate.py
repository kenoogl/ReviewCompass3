"""第1段完了関門の値なし機械監査。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses


GATE_IDS = (
  "source_universe",
  "known_candidates",
  "material_insufficiency",
  "selection_routes",
  "stale_rejection",
  "digest_chain",
  "approval_binding",
  "immutable_resume",
)


class StageOneGateError(Exception):
  """第1段関門証拠を安全に監査できない。"""


@dataclasses.dataclass(frozen=True)
class GateResult:
  identifier: str
  status: str


@dataclasses.dataclass(frozen=True)
class StageOneAudit:
  status: str
  gates: tuple
  passed_gate_count: int
  unresolved_gates: tuple
  user_approved: bool


def audit_stage_one(evidence, *, user_approved) -> StageOneAudit:
  if (
    not isinstance(evidence, dict)
    or set(evidence) != set(GATE_IDS)
    or any(
      type(evidence[identifier]) is not bool
      for identifier in GATE_IDS
    )
    or type(user_approved) is not bool
  ):
    raise StageOneGateError(
      "Stage one evidence must exactly match all fixed gates"
    )
  gates = tuple(
    GateResult(
      identifier,
      "passed" if evidence[identifier] else "unresolved",
    )
    for identifier in GATE_IDS
  )
  unresolved = tuple(
    gate.identifier
    for gate in gates
    if gate.status != "passed"
  )
  passed_count = len(gates) - len(unresolved)
  if unresolved:
    status = "blocked"
  elif user_approved:
    status = "ready"
  else:
    status = "candidate"
  return StageOneAudit(
    status=status,
    gates=gates,
    passed_gate_count=passed_count,
    unresolved_gates=unresolved,
    user_approved=user_approved,
  )


def audit_document(audit):
  if not isinstance(audit, StageOneAudit):
    raise StageOneGateError(
      "Expected a stage one audit"
    )
  return {
    "gates": [
      {
        "id": gate.identifier,
        "status": gate.status,
      }
      for gate in audit.gates
    ],
    "lifecycle": "provisional",
    "normative_status": "non-normative",
    "passed_gate_count": audit.passed_gate_count,
    "promotion_required": True,
    "record_version": 1,
    "status": audit.status,
    "unresolved_gate_count": len(audit.unresolved_gates),
    "user_approved": audit.user_approved,
  }
