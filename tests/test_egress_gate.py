"""出口関門と段階1送信係（出口設計v4 §5・§8）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def _gate():
  return importlib.import_module("tools.egress.gate")


def _sender():
  return importlib.import_module("tools.egress.sender")


def _payload_module():
  return importlib.import_module("tools.egress.payload")


NOW = "2026-08-07T12:00:00+09:00"


def _build_payload(tmp_path):
  payload = _payload_module()
  source = tmp_path / "pkg" / "mod.py"
  source.parent.mkdir(parents=True, exist_ok=True)
  source.write_text(
    "def a():\n  return 1\ndef b():\n  return 2\n", encoding="utf-8"
  )
  routine = {
    "code_reference": {
      "relative_path": "pkg/mod.py",
      "start_line": 1,
      "end_line": 2,
    },
    "signature": {"parameters": [], "returns_annotation": None},
    "return_count": 1,
    "raise_count": 0,
    "raised_exception_names": [],
    "branch_count": 0,
    "line_count": 2,
    "max_nesting_depth": 0,
    "complexity_signal": "low",
    "public_api_signal": "low",
  }
  other = dict(routine)
  other["code_reference"] = {
    "relative_path": "pkg/mod.py",
    "start_line": 3,
    "end_line": 4,
  }
  return payload.build_pair_payload(
    repository_root=tmp_path,
    routine_a=routine,
    routine_b=other,
    question_id="impl-sameness-v1",
  )


def _approval_record(list_digest):
  return {
    "schema_version": "egress-approval-v1",
    "approved_by": "user",
    "payload_list_digest": list_digest,
    "provider": "anthropic-api",
    "model": "claude-sonnet-5",
    "expires_at": "2026-08-08T00:00:00+09:00",
    "purpose": "implementation_sameness_judgment",
    "material_policy": {
      "require_secret_scan": True,
      "forbid_credentials": True,
      "forbid_personal_identifiers": True,
    },
    "consumed": False,
  }


def _run(tmp_path, **overrides):
  gate = _gate()
  approval = importlib.import_module("tools.egress.approval")
  built = overrides.pop("payload", None) or _build_payload(tmp_path)
  list_digest = overrides.pop(
    "list_digest", approval.payload_list_digest([built.digest])
  )
  arguments = {
    "payload": built,
    "repository_root": tmp_path,
    "approved_payload_digests": [built.digest],
    "approval_record": _approval_record(list_digest),
    "provider": "anthropic-api",
    "model": "claude-sonnet-5",
    "redaction_hook": lambda text: text,
    "now": NOW,
  }
  arguments.update(overrides)
  return gate.run_egress_gate(**arguments)


class TestGateAllows:
  def test_conforming_payload_passes_all_conditions(self, tmp_path):
    result = _run(tmp_path)
    assert result.allowed is True
    assert result.reasons == ()


class TestGateBlocks:
  def test_unlisted_payload_is_blocked_with_recovery(self, tmp_path):
    gate = _gate()
    result = _run(tmp_path, approved_payload_digests=["f" * 64])
    assert result.allowed is False
    assert result.reasons
    assert result.recovery

  def test_list_digest_mismatch_is_blocked(self, tmp_path):
    result = _run(tmp_path, list_digest="0" * 64)
    assert result.allowed is False

  def test_modified_source_is_blocked(self, tmp_path):
    built = _build_payload(tmp_path)
    (tmp_path / "pkg" / "mod.py").write_text(
      "changed\ncontent\nhere\nnow\n", encoding="utf-8"
    )
    result = _run(tmp_path, payload=built)
    assert result.allowed is False

  def test_redaction_masking_anything_is_blocked(self, tmp_path):
    result = _run(
      tmp_path, redaction_hook=lambda text: text.replace("return", "***")
    )
    assert result.allowed is False

  def test_missing_redaction_hook_is_blocked(self, tmp_path):
    result = _run(tmp_path, redaction_hook=None)
    assert result.allowed is False

  def test_oversized_payload_is_blocked(self, tmp_path):
    result = _run(tmp_path, size_limit_kb=0)
    assert result.allowed is False

  def test_every_block_carries_recovery_guidance(self, tmp_path):
    result = _run(tmp_path, redaction_hook=None, size_limit_kb=0)
    assert result.allowed is False
    assert len(result.recovery) >= 1


class TestStageOneSender:
  def test_gate_passing_payload_still_cannot_send(self, tmp_path):
    sender = _sender()
    approval = importlib.import_module("tools.egress.approval")
    built = _build_payload(tmp_path)
    runner = sender.build_stage_one_runner(
      repository_root=tmp_path,
      approved_payload_digests=[built.digest],
      approval_record=_approval_record(
        approval.payload_list_digest([built.digest])
      ),
      provider="anthropic-api",
      model="claude-sonnet-5",
      redaction_hook=lambda text: text,
      now=NOW,
    )
    with pytest.raises(sender.EgressSendingNotApproved):
      runner("primary", built)

  def test_gate_failing_payload_raises_gate_error(self, tmp_path):
    sender = _sender()
    built = _build_payload(tmp_path)
    runner = sender.build_stage_one_runner(
      repository_root=tmp_path,
      approved_payload_digests=["f" * 64],
      approval_record=_approval_record("0" * 64),
      provider="anthropic-api",
      model="claude-sonnet-5",
      redaction_hook=lambda text: text,
      now=NOW,
    )
    with pytest.raises(sender.EgressGateRefusal) as caught:
      runner("primary", built)
    assert "外部送信せず停止" in str(caught.value)
