"""既知正例群の候補単位抽出被覆。"""

import dataclasses
import hashlib
import json


class GroupCoverageError(Exception):
  """既知正例群の抽出判断が完全でない。"""


@dataclasses.dataclass(frozen=True)
class GroupCoverage:
  status: str
  extracted: tuple
  not_selected: tuple
  covered_groups: tuple
  digest: str


def _text(value):
  return isinstance(value, str) and bool(value) and "\n" not in value


def cover_known_positive_groups(groups, resolutions):
  if (
    not isinstance(groups, dict)
    or not groups
    or any(
      not _text(group)
      or not isinstance(candidates, (list, tuple))
      or not candidates
      or len(set(candidates)) != len(candidates)
      for group, candidates in groups.items()
    )
  ):
    raise GroupCoverageError("groups require unique candidates")
  all_candidates = {
    candidate
    for candidates in groups.values()
    for candidate in candidates
  }
  if sum(len(values) for values in groups.values()) != len(all_candidates):
    raise GroupCoverageError("candidates cannot belong to multiple groups")
  values = tuple(resolutions)
  if any(
    not isinstance(value, dict)
    or set(value) != {
      "candidate", "action", "essence_id", "rationale",
    }
    or value["action"] not in {"extract", "not_selected"}
    or not _text(value["rationale"])
    for value in values
  ):
    raise GroupCoverageError("invalid candidate resolution")
  resolved = tuple(value["candidate"] for value in values)
  if (
    len(set(resolved)) != len(resolved)
    or set(resolved) != all_candidates
  ):
    raise GroupCoverageError("every candidate needs one resolution")
  extracted = []
  not_selected = []
  for value in sorted(values, key=lambda item: item["candidate"]):
    if value["action"] == "extract":
      if not _text(value["essence_id"]):
        raise GroupCoverageError("extraction requires essence id")
      extracted.append((value["candidate"], value["essence_id"]))
    else:
      if value["essence_id"] is not None:
        raise GroupCoverageError("not-selected cannot have essence id")
      not_selected.append(value["candidate"])
  document = {
    "extracted": extracted,
    "not_selected": not_selected,
    "schema_version": 1,
  }
  digest = hashlib.sha256(json.dumps(
    document,
    ensure_ascii=False,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return GroupCoverage(
    status="complete",
    extracted=tuple(extracted),
    not_selected=tuple(not_selected),
    covered_groups=tuple(sorted(groups)),
    digest=digest,
  )
