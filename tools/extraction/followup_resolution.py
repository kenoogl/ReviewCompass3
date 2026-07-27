"""抽出台帳follow_upの再検証。"""

import dataclasses


@dataclasses.dataclass(frozen=True)
class DecisionSourceVerification:
  status: str
  primary_reference_count: int
  required_action: object


@dataclasses.dataclass(frozen=True)
class RuleRecountVerification:
  status: str
  actual_source_count: int
  raw_count: int
  kept_count: int
  fragment_count: int
  substring_count: int
  uncategorized_count: int
  discrepancies: tuple


def verify_decision_source_chain(
  *,
  inventory_reference,
  primary_references,
  user_reconfirmed,
):
  references = tuple(primary_references)
  if not inventory_reference or not references:
    return DecisionSourceVerification(
      "follow_up",
      len(references),
      "primary_evidence",
    )
  if user_reconfirmed is not True:
    return DecisionSourceVerification(
      "follow_up",
      len(references),
      "user_reconfirmation",
    )
  return DecisionSourceVerification("resolved", len(references), None)


def verify_rule_recount(
  records,
  *,
  claimed_source_count,
  claimed_raw,
  claimed_kept,
  claimed_frag,
  claimed_sub,
):
  values = tuple(records)
  keys = ("raw", "kept", "frag", "sub")
  if any(
    not isinstance(value, dict)
    or any(
      not isinstance(value.get(key), int)
      or value[key] < 0
      for key in keys
    )
    for value in values
  ):
    raise ValueError("rule recount records require non-negative counts")
  totals = {
    key: sum(value[key] for value in values)
    for key in keys
  }
  discrepancies = []
  if len(values) != claimed_source_count:
    discrepancies.append("source_count")
  if totals["raw"] != (
    totals["kept"] + totals["frag"] + totals["sub"]
  ):
    discrepancies.append("raw_partition")
  claims = {
    "raw": claimed_raw,
    "kept": claimed_kept,
    "frag": claimed_frag,
    "sub": claimed_sub,
  }
  if totals != claims:
    discrepancies.append("claimed_totals")
  uncategorized = (
    totals["raw"]
    - totals["kept"]
    - totals["frag"]
    - totals["sub"]
  )
  return RuleRecountVerification(
    status="follow_up" if discrepancies else "resolved",
    actual_source_count=len(values),
    raw_count=totals["raw"],
    kept_count=totals["kept"],
    fragment_count=totals["frag"],
    substring_count=totals["sub"],
    uncategorized_count=uncategorized,
    discrepancies=tuple(discrepancies),
  )
