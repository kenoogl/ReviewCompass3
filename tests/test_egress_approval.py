"""承認recordの機械検証（出口設計v4 §4）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def _approval():
  return importlib.import_module("tools.egress.approval")


FUTURE = "2099-01-01T00:00:00+09:00"
PAST = "2020-01-01T00:00:00+09:00"


def _record(**overrides):
  base = {
    "schema_version": "egress-approval-v1",
    "approved_by": "user",
    "payload_list_digest": "d" * 64,
    "provider": "anthropic-api",
    "model": "claude-sonnet-5",
    "expires_at": FUTURE,
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
  )


def _write_record(directory, record, name="approval.json"):
  path = directory / name
  path.write_text(
    json.dumps(record, ensure_ascii=False, sort_keys=True), encoding="utf-8"
  )
  return path, hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path, sha256, **overrides):
  approval = _approval()
  arguments = {
    "sha256": sha256,
    "payload_list_digest": "d" * 64,
    "provider": "anthropic-api",
    "model": "claude-sonnet-5",
    "purpose": "implementation_sameness_judgment",
  }
  arguments.update(overrides)
  return approval.load_approval_file(path, **arguments)


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
      {"expires_at": PAST},
      {"expires_at": "2099-01-01T00:00:00"},
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


class TestExpiryUsesRealTime:
  """F-E1反証：caller提供の`now`で期限判定を迂回できない。"""

  def test_caller_supplied_now_is_not_accepted(self):
    approval = _approval()
    with pytest.raises(TypeError):
      approval.validate_approval_record(
        _record(expires_at=PAST),
        payload_list_digest="d" * 64,
        provider="anthropic-api",
        model="claude-sonnet-5",
        purpose="implementation_sameness_judgment",
        now="2019-01-01T00:00:00+09:00",
      )

  def test_expired_record_is_rejected_without_caller_clock(self):
    approval = _approval()
    with pytest.raises(approval.ApprovalError):
      _validate(_record(expires_at=PAST))


class TestConsumedFieldIsStrict:
  """F-E1反証：`consumed`の欠落・非boolを未消費として合格させない。"""

  @pytest.mark.parametrize(
    "overrides",
    [
      {"consumed": "false"},
      {"consumed": 0},
      {"consumed": None},
    ],
  )
  def test_non_boolean_consumed_is_rejected(self, overrides):
    approval = _approval()
    with pytest.raises(approval.ApprovalError):
      _validate(_record(**overrides))

  def test_missing_consumed_is_rejected(self):
    approval = _approval()
    record = _record()
    del record["consumed"]
    with pytest.raises(approval.ApprovalError):
      _validate(record)


class TestApprovalFileBinding:
  """F-E1反証：Human作成のrecord fileへ束縛されない承認は通らない。"""

  def test_matching_file_and_digest_is_accepted(self, tmp_path):
    path, digest = _write_record(tmp_path, _record())
    loaded = _load(path, digest)
    assert loaded["approved_by"] == "user"

  def test_digest_mismatch_is_rejected(self, tmp_path):
    approval = _approval()
    path, _digest = _write_record(tmp_path, _record())
    with pytest.raises(approval.ApprovalError):
      _load(path, "0" * 64)

  def test_missing_file_is_rejected(self, tmp_path):
    approval = _approval()
    with pytest.raises(approval.ApprovalError):
      _load(tmp_path / "absent.json", "0" * 64)

  def test_content_changed_after_digest_is_rejected(self, tmp_path):
    approval = _approval()
    path, digest = _write_record(tmp_path, _record())
    path.write_text(
      json.dumps(_record(approved_by="llm"), ensure_ascii=False),
      encoding="utf-8",
    )
    with pytest.raises(approval.ApprovalError):
      _load(path, digest)

  def test_unreadable_json_is_rejected(self, tmp_path):
    approval = _approval()
    path = tmp_path / "approval.json"
    path.write_text("not json", encoding="utf-8")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(approval.ApprovalError):
      _load(path, digest)


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

  @pytest.mark.parametrize(
    "text",
    [
      "aws = AKIAIOSFODNN7EXAMPLE",
      "aws_session = ASIAIOSFODNN7EXAMPLE",
      "gh = ghp_0123456789abcdefghijklmnopqrstuvwxyz",
      "-----BEGIN RSA PRIVATE KEY-----",
      "-----BEGIN OPENSSH PRIVATE KEY-----",
    ],
  )
  def test_approved_credential_formats_are_detected(self, text):
    """F-E3反証：Human承認済みの資格情報3形式を安全と誤判定しない。"""
    approval = _approval()
    assert approval.scan_outbound_text(text) != []

  @pytest.mark.parametrize(
    "digest",
    [
      "9" * 64,
      "1234567890abcdef" * 4,
      "0123456789012345678901234567890123456789012345678901234567890123",
    ],
  )
  def test_digest_hex_is_not_reported_as_personal_identifier(self, digest):
    """F-E3反証（正例）：64桁hexの数字列を個人識別子と誤検出しない。"""
    approval = _approval()
    assert approval.scan_outbound_text(
      'content_sha256: "%s"' % digest
    ) == []


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
