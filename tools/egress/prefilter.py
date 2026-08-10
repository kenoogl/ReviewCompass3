"""ローカル事前分類（出口設計v4 §3.1）。

外部送信の前段として、関数の組を手元の計算だけで
「明らかに同じ／明らかに別／曖昧」の3帯に分類する。
閾値と重みはHuman承認済みの初期値（DEC-EGRESS-GATE-V3-JUDGMENTS-001、
実測はEXP-LOCAL-PREFILTER-001）。値の変更はHuman承認事項。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import math
import re


class PrefilterError(Exception):
  """事前分類の入力が正しくない。"""


_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_STOP = frozenset({
  "self", "the", "an", "of", "and", "or", "in", "to", "is", "def",
  "return", "if", "else", "elif", "for", "while", "raise", "try",
  "except", "with", "as", "not", "none", "true", "false", "import",
  "from", "pass", "class", "dataclass", "dataclasses", "frozen", "str",
  "int", "bool", "float", "tuple", "list", "dict", "object", "optional",
})

_REQUIRED_ROUTINE_FIELDS = (
  "signature",
  "return_count",
  "raise_count",
  "raised_exception_names",
  "branch_count",
  "line_count",
)


@dataclasses.dataclass(frozen=True)
class Thresholds:
  same_min: float
  diff_max: float
  body_weight: float
  name_weight: float
  feature_weight: float


DEFAULT_THRESHOLDS = Thresholds(
  same_min=0.85,
  diff_max=0.45,
  body_weight=0.6,
  name_weight=0.2,
  feature_weight=0.2,
)


def _validate_thresholds(thresholds):
  """閾値と重みがHuman承認済みの形（有限・範囲内・重み合計1）であることを検査する。

  非有限値は比較が常に偽になり、既定の分類を迂回できるためfail-closedで拒否する。
  """
  if not isinstance(thresholds, Thresholds):
    raise PrefilterError("thresholds must be a Thresholds value")
  values = {
    "same_min": thresholds.same_min,
    "diff_max": thresholds.diff_max,
    "body_weight": thresholds.body_weight,
    "name_weight": thresholds.name_weight,
    "feature_weight": thresholds.feature_weight,
  }
  for name, value in values.items():
    if isinstance(value, bool) or not isinstance(value, (int, float)):
      raise PrefilterError(f"threshold {name} must be a number")
    if not math.isfinite(value):
      raise PrefilterError(f"threshold {name} must be finite")
    if not 0.0 <= value <= 1.0:
      raise PrefilterError(f"threshold {name} must be within 0..1")
  if not thresholds.diff_max < thresholds.same_min:
    raise PrefilterError("diff_max must be below same_min")
  weight_sum = (
    thresholds.body_weight
    + thresholds.name_weight
    + thresholds.feature_weight
  )
  if abs(weight_sum - 1.0) > 1e-9:
    raise PrefilterError("weights must sum to 1")


@dataclasses.dataclass(frozen=True)
class PairClassification:
  band: str
  similarity: float
  body_similarity: float
  name_similarity: float
  feature_similarity: float


def identifier_tokens(text):
  """識別子をsnake_case・CamelCaseで分解した小文字tokenの集合を返す。"""
  found = set()
  for identifier in _IDENT.findall(text):
    for part in identifier.split("_"):
      for word in _CAMEL.split(part):
        lowered = word.lower()
        if len(lowered) >= 2 and lowered not in _STOP:
          found.add(lowered)
  return frozenset(found)


def jaccard(left, right):
  """2つの集合のJaccard係数（共通部分÷和集合）。"""
  if not left and not right:
    return 1.0
  if not left or not right:
    return 0.0
  return len(left & right) / len(left | right)


def _validate_routine(routine):
  if not isinstance(routine, dict):
    raise PrefilterError("routine must be a mapping")
  missing = [
    field for field in _REQUIRED_ROUTINE_FIELDS if field not in routine
  ]
  if missing:
    raise PrefilterError(
      "routine is missing required fields: " + ", ".join(missing)
    )
  signature = routine["signature"]
  if not isinstance(signature, dict) or "parameters" not in signature:
    raise PrefilterError("routine signature must carry parameters")


def feature_match(routine_a, routine_b):
  """機械特徴6項目の一致率（0..1）。"""
  _validate_routine(routine_a)
  _validate_routine(routine_b)
  score = 0
  if len(routine_a["signature"]["parameters"]) == len(
    routine_b["signature"]["parameters"]
  ):
    score += 1
  if routine_a["return_count"] == routine_b["return_count"]:
    score += 1
  if routine_a["raise_count"] == routine_b["raise_count"]:
    score += 1
  if set(routine_a["raised_exception_names"]) == set(
    routine_b["raised_exception_names"]
  ):
    score += 1
  if routine_a["branch_count"] == routine_b["branch_count"]:
    score += 1
  longer = max(routine_a["line_count"], routine_b["line_count"])
  if abs(routine_a["line_count"] - routine_b["line_count"]) <= max(
    2, 0.2 * longer
  ):
    score += 1
  return score / 6


def classify_pair(
  *,
  code_a,
  code_b,
  name_a,
  name_b,
  routine_a,
  routine_b,
  thresholds=DEFAULT_THRESHOLDS,
):
  """組を3帯に分類する。外部送信の対象は「曖昧」帯のみである。"""
  _validate_thresholds(thresholds)
  body_similarity = jaccard(
    identifier_tokens(code_a), identifier_tokens(code_b)
  )
  name_similarity = jaccard(
    identifier_tokens(name_a), identifier_tokens(name_b)
  )
  feature_similarity = feature_match(routine_a, routine_b)
  similarity = (
    thresholds.body_weight * body_similarity
    + thresholds.name_weight * name_similarity
    + thresholds.feature_weight * feature_similarity
  )
  if similarity >= thresholds.same_min:
    band = "clearly_same"
  elif similarity <= thresholds.diff_max:
    band = "clearly_diff"
  else:
    band = "ambiguous"
  return PairClassification(
    band=band,
    similarity=similarity,
    body_similarity=body_similarity,
    name_similarity=name_similarity,
    feature_similarity=feature_similarity,
  )
