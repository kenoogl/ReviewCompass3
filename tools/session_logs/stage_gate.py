"""第0段セッションログ完了関門の機械監査。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import dataclasses
import json
import os
from pathlib import Path


REQUIRED_GATES = (
  "raw_log_restore",
  "idempotent_reingestion",
  "transcript_summary_tamper_detection",
  "raw_to_summary_provenance",
  "git_sensitive_data_absence",
  "hook_non_blocking",
  "periodic_preservation",
  "real_data_mutation_validation",
)

REQUIRED_EXTERNAL_CHECKS = (
  "private_real_log_validation",
  "stage_zero_user_approval",
  "user_environment_hook_schedule",
)


class StageGateError(Exception):
  """第0段関門の証拠を安全に監査できない。"""


@dataclasses.dataclass(frozen=True)
class StageGateResult:
  status: str
  required_gate_count: int
  passed_gate_count: int
  unresolved: tuple
  gates: dict


def _safe_evidence_path(repository_root, value):
  path = Path(value)
  if path.is_absolute() or ".." in path.parts:
    return None
  resolved = (repository_root / path).resolve()
  if (
    resolved != repository_root
    and repository_root not in resolved.parents
  ):
    return None
  return resolved


def audit_stage_zero(
  evidence_path,
  *,
  repository_root=None,
) -> StageGateResult:
  path = Path(evidence_path)
  try:
    data = json.loads(path.read_text(encoding="utf-8"))
  except (OSError, ValueError) as error:
    raise StageGateError("Cannot read stage zero evidence") from error
  if not isinstance(data, dict):
    raise StageGateError("Invalid stage zero evidence")
  if repository_root is None:
    root_value = data.get("repository_root")
    if not isinstance(root_value, str):
      raise StageGateError("Invalid stage zero evidence")
    root = (path.parent / root_value).resolve()
  else:
    root = Path(repository_root).resolve()
  if not (root / ".git").exists():
    raise StageGateError("Invalid stage zero repository")
  source_gates = data.get("gates")
  external_checks = data.get("external_checks")
  if (
    not isinstance(source_gates, dict)
    or not isinstance(external_checks, dict)
  ):
    raise StageGateError("Invalid stage zero evidence")

  gates = {}
  unresolved = []
  passed_gate_count = 0
  for gate_id in REQUIRED_GATES:
    item = source_gates.get(gate_id)
    evidence_paths = (
      item.get("evidence_paths")
      if isinstance(item, dict)
      else None
    )
    valid_paths = (
      isinstance(evidence_paths, list)
      and bool(evidence_paths)
      and all(
        isinstance(value, str)
        and (
          resolved := _safe_evidence_path(root, value)
        ) is not None
        and resolved.is_file()
        for value in evidence_paths
      )
    )
    passed = (
      isinstance(item, dict)
      and item.get("status") == "passed"
      and valid_paths
    )
    gates[gate_id] = {
      "evidence_paths": (
        list(evidence_paths)
        if isinstance(evidence_paths, list)
        else []
      ),
      "status": "passed" if passed else "failed",
    }
    if passed:
      passed_gate_count += 1
    else:
      unresolved.append(gate_id)

  for check_id in REQUIRED_EXTERNAL_CHECKS:
    item = external_checks.get(check_id)
    if (
      not isinstance(item, dict)
      or item.get("status") != "passed"
    ):
      unresolved.append(check_id)

  return StageGateResult(
    status="ready" if not unresolved else "blocked",
    required_gate_count=len(REQUIRED_GATES),
    passed_gate_count=passed_gate_count,
    unresolved=tuple(unresolved),
    gates=gates,
  )


def _report_payload(result):
  return {
    "gates": result.gates,
    "passed_gate_count": result.passed_gate_count,
    "required_gate_count": result.required_gate_count,
    "status": result.status,
    "unresolved": list(result.unresolved),
  }


def _write_report(path, payload):
  report_path = Path(path)
  temporary_path = report_path.with_name(report_path.name + ".tmp")
  try:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.write_text(
      json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
      ) + "\n",
      encoding="utf-8",
    )
    os.replace(temporary_path, report_path)
  except OSError as error:
    raise StageGateError("Cannot write stage zero report") from error
  finally:
    temporary_path.unlink(missing_ok=True)


def run(argv=None) -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("--evidence", required=True)
  parser.add_argument("--report", required=True)
  args = parser.parse_args(argv)
  try:
    if (
      not Path(args.evidence).is_absolute()
      or not Path(args.report).is_absolute()
    ):
      raise StageGateError("Unsafe stage zero audit paths")
    result = audit_stage_zero(args.evidence)
    payload = _report_payload(result)
    _write_report(args.report, payload)
  except Exception as error:
    print(json.dumps({
      "reason": type(error).__name__,
      "status": "failed",
    }, sort_keys=True))
    return 5
  print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
  return 0 if result.status == "ready" else 11


def main():
  raise SystemExit(run())


if __name__ == "__main__":
  main()
