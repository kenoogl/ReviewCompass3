"""第0段セッションログ完了関門の機械監査テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
EVIDENCE_PATH = (
  REPOSITORY_ROOT
  / "records"
  / "stage-zero"
  / "session-log-gates.json"
)


def test_stage_zero_gate_maps_evidence_and_blocks_pending_external_checks(
  tmp_path,
  capsys,
):
  gate = importlib.import_module("tools.session_logs.stage_gate")

  result = gate.audit_stage_zero(EVIDENCE_PATH)

  assert result.status == "blocked"
  assert result.required_gate_count == 8
  assert result.passed_gate_count == 8
  assert result.unresolved == (
    "stage_zero_user_approval",
  )
  assert tuple(result.gates) == gate.REQUIRED_GATES
  for gate_result in result.gates.values():
    assert gate_result["status"] == "passed"
    assert gate_result["evidence_paths"]
    for evidence_path in gate_result["evidence_paths"]:
      assert (REPOSITORY_ROOT / evidence_path).is_file()

  report_path = tmp_path / "stage-zero-audit.json"
  entry = importlib.import_module("tools.session_logs.entry")
  assert entry.run((
    "audit-stage-zero",
    "--evidence",
    str(EVIDENCE_PATH),
    "--report",
    str(report_path),
  )) == 11
  output = json.loads(capsys.readouterr().out)
  assert output == json.loads(report_path.read_text(encoding="utf-8"))
  assert output["status"] == "blocked"
  assert output["passed_gate_count"] == 8
  assert output["required_gate_count"] == 8
  assert output["unresolved"] == list(result.unresolved)

  evidence = json.loads(
    EVIDENCE_PATH.read_text(encoding="utf-8")
  )
  native_check = evidence["external_checks"][
    "native_three_os_deployment_validation"
  ]
  assert native_check["status"] == "passed"
  assert native_check["evidence_paths"] == [
    "records/stage-zero/native-deployment-validation.json"
  ]
  assert (
    REPOSITORY_ROOT
    / native_check["evidence_paths"][0]
  ).is_file()
  native_evidence = json.loads((
    REPOSITORY_ROOT
    / native_check["evidence_paths"][0]
  ).read_text(encoding="utf-8"))
  assert native_evidence["status"] == "passed"

  environment_check = evidence["external_checks"][
    "user_environment_hook_schedule"
  ]
  assert environment_check["status"] == "passed"
  environment_evidence = json.loads((
    REPOSITORY_ROOT
    / environment_check["evidence_paths"][0]
  ).read_text(encoding="utf-8"))
  assert environment_evidence["status"] == (
    "limited_deployment_passed"
  )
  assert environment_evidence["retention"] == {
    "after_file_count": 652,
    "before_file_count": 652,
    "digest_match": True,
    "status": "passed",
  }


def test_stage_zero_gate_fails_closed_when_required_gate_is_missing(
  tmp_path,
):
  gate = importlib.import_module("tools.session_logs.stage_gate")
  data = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
  data["gates"].pop("raw_log_restore")
  incomplete_path = tmp_path / "incomplete-gates.json"
  incomplete_path.write_text(json.dumps(data), encoding="utf-8")

  result = gate.audit_stage_zero(
    incomplete_path,
    repository_root=REPOSITORY_ROOT,
  )

  assert result.status == "blocked"
  assert result.passed_gate_count == 7
  assert "raw_log_restore" in result.unresolved
