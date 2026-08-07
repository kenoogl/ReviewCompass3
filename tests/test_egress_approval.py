"""承認recordの機械検証（出口設計v4 §4）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json

import pytest


def _approval():
  return importlib.import_module("tools.egress.approval")


NOW = "2026-08-07T12:00:00+09:00"


def _record(**overrides):
  base = {
    "schema_version": "egress-approval-v1",
    "approved_by": "user",
    "payload_list_digest": "d" * 64,
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
  base.update(overrides)
  return base


def _validate(record):
  approval = _approval()
  approval.validate_approval_record(
    record,
    payload_list_digest="d" * 64,
    provider="anthropic-api",
    model="claude-sonnet-5",
    purpose="implementation_sameness_judgment",
    now=NOW,
  )


class TestValidateApprovalRecord:
  def test_valid_record_passes(self):
    _validate(_record())

  @pytest.mark.parametrize(
    "overrides",
    [
      {"schema_version": "other-v1"},
      {"approved_by": "llm"},
      {"payload_list_digest": "e" * 64},
      {"provider": "openai-api"},
      {"model": "claude-haiku-4-5"},
      {"expires_at": "2026-08-07T11:00:00+09:00"},
      {"expires_at": "2026-08-08T00:00:00"},
      {"purpose": "guard_module_review"},
      {
        "material_policy": {
          "require_secret_scan": True,
          "forbid_credentials": True,
          "forbid_personal_identifiers": False,
        }
      },
      {"consumed": True},
    ],
  )
  def test_each_violation_is_rejected(self, overrides):
    approval = _approval()
    with pytest.raises(approval.ApprovalError):
      _validate(_record(**overrides))


class TestPayloadListDigest:
  def test_digest_is_order_insensitive_and_deterministic(self):
    approval = _approval()
    first = approval.payload_list_digest(["a" * 64, "b" * 64])
    second = approval.payload_list_digest(["b" * 64, "a" * 64])
    assert first == second
    assert len(first) == 64

  def test_different_lists_differ(self):
    approval = _approval()
    assert approval.payload_list_digest(
      ["a" * 64]
    ) != approval.payload_list_digest(["b" * 64])


class TestOutboundScan:
  def test_clean_code_text_has_no_findings(self):
    approval = _approval()
    assert approval.scan_outbound_text("def add(a, b):\n  return a + b") == []

  @pytest.mark.parametrize(
    "text",
    [
      "api_key = sk-abcdefgHIJKLMNOP1234",
      "Authorization: Bearer abcdefghijklmnop.qrstuv",
      "contact: someone@example.com",
      "tel: +81 90-1234-5678",
    ],
  )
  def test_secrets_and_identifiers_are_detected(self, text):
    approval = _approval()
    assert approval.scan_outbound_text(text) != []


class TestConsumption:
  def test_claim_is_exclusive_while_held(self, tmp_path):
    approval = _approval()
    record_path = tmp_path / "approval.json"
    record_path.write_text(json.dumps(_record()), encoding="utf-8")
    with approval.approval_claim(record_path):
      with pytest.raises(approval.ApprovalError):
        with approval.approval_claim(record_path):
          pass

  def test_mark_consumed_is_permanent(self, tmp_path):
    approval = _approval()
    record_path = tmp_path / "approval.json"
    record_path.write_text(json.dumps(_record()), encoding="utf-8")
    approval.mark_consumed(record_path)
    stored = json.loads(record_path.read_text(encoding="utf-8"))
    assert stored["consumed"] is True
    with pytest.raises(approval.ApprovalError):
      _validate(stored)
