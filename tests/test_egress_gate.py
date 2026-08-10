"""出口関門と段階1送信係（出口設計v4 §5・§8）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def _gate():
  return importlib.import_module("tools.egress.gate")


def _sender():
  return importlib.import_module("tools.egress.sender")


def _payload_module():
  return importlib.import_module("tools.egress.payload")


FUTURE = "2099-01-01T00:00:00+09:00"


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


def _approval_record(list_digest, **overrides):
  record = {
    "schema_version": "egress-approval-v1",
    "approved_by": "user",
    "payload_list_digest": list_digest,
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
  record.update(overrides)
  return record


def _approval_file(directory, list_digest, **overrides):
  """Human作成の承認record fileを模す。pathとSHA-256の組で渡す。"""
  path = directory / "approval-record.json"
  path.write_text(
    json.dumps(
      _approval_record(list_digest, **overrides),
      ensure_ascii=False,
      sort_keys=True,
    ),
    encoding="utf-8",
  )
  return path, hashlib.sha256(path.read_bytes()).hexdigest()


def _run(tmp_path, **overrides):
  gate = _gate()
  approval = importlib.import_module("tools.egress.approval")
  built = overrides.pop("payload", None) or _build_payload(tmp_path)
  list_digest = overrides.pop(
    "list_digest", approval.payload_list_digest([built.digest])
  )
  record_path, record_digest = _approval_file(tmp_path, list_digest)
  arguments = {
    "payload": built,
    "repository_root": tmp_path,
    "approved_payload_digests": [built.digest],
    "approval_record_path": record_path,
    "approval_record_sha256": record_digest,
    "provider": "anthropic-api",
    "model": "claude-sonnet-5",
    "redaction_hook": gate.APPROVED_REDACTION_HOOK,
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

  def test_missing_redaction_hook_is_blocked(self, tmp_path):
    result = _run(tmp_path, redaction_hook=None)
    assert result.allowed is False

  def test_redaction_masking_anything_is_blocked(self, tmp_path):
    """許可実装の伏字化が内容を変えた＝本来入らない物が入っていた兆候。"""
    payload = _payload_module()
    approval = importlib.import_module("tools.egress.approval")
    source = tmp_path / "pkg" / "mod.py"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(
      'KEY = "AKIAIOSFODNN7EXAMPLE"\nDEF = 1\nX = 2\nY = 3\n',
      encoding="utf-8",
    )
    routine = {
      "code_reference": {
        "relative_path": "pkg/mod.py",
        "start_line": 1,
        "end_line": 2,
      },
      "signature": {"parameters": [], "returns_annotation": None},
      "return_count": 0,
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
    built = payload.build_pair_payload(
      repository_root=tmp_path,
      routine_a=routine,
      routine_b=other,
      question_id="impl-sameness-v1",
    )
    result = _run(
      tmp_path,
      payload=built,
      approved_payload_digests=[built.digest],
      list_digest=approval.payload_list_digest([built.digest]),
    )
    assert result.allowed is False
    assert any("伏字化" in reason for reason in result.reasons)

  def test_oversized_payload_is_blocked(self, tmp_path):
    result = _run(tmp_path, size_limit_kb=0)
    assert result.allowed is False

  def test_every_block_carries_recovery_guidance(self, tmp_path):
    result = _run(tmp_path, redaction_hook=None, size_limit_kb=0)
    assert result.allowed is False
    assert len(result.recovery) >= 1


class TestApprovalIsBoundToHumanRecordFile:
  """F-E1反証：承認はHuman作成record fileへ束縛される。"""

  def test_bare_dictionary_approval_is_not_accepted(self, tmp_path):
    gate = _gate()
    approval = importlib.import_module("tools.egress.approval")
    built = _build_payload(tmp_path)
    with pytest.raises(TypeError):
      gate.run_egress_gate(
        payload=built,
        repository_root=tmp_path,
        approved_payload_digests=[built.digest],
        approval_record=_approval_record(
          approval.payload_list_digest([built.digest])
        ),
        provider="anthropic-api",
        model="claude-sonnet-5",
        redaction_hook=gate.APPROVED_REDACTION_HOOK,
        now="2026-08-07T12:00:00+09:00",
      )

  def test_approval_file_digest_mismatch_is_blocked(self, tmp_path):
    result = _run(tmp_path, approval_record_sha256="0" * 64)
    assert result.allowed is False

  def test_missing_approval_file_is_blocked(self, tmp_path):
    result = _run(
      tmp_path, approval_record_path=tmp_path / "absent-approval.json"
    )
    assert result.allowed is False

  def test_expired_approval_file_is_blocked(self, tmp_path):
    gate = _gate()
    approval = importlib.import_module("tools.egress.approval")
    built = _build_payload(tmp_path)
    record_path, record_digest = _approval_file(
      tmp_path,
      approval.payload_list_digest([built.digest]),
      expires_at="2020-01-01T00:00:00+09:00",
    )
    result = gate.run_egress_gate(
      payload=built,
      repository_root=tmp_path,
      approved_payload_digests=[built.digest],
      approval_record_path=record_path,
      approval_record_sha256=record_digest,
      provider="anthropic-api",
      model="claude-sonnet-5",
      redaction_hook=gate.APPROVED_REDACTION_HOOK,
    )
    assert result.allowed is False


class TestPayloadJsonIsCrossChecked:
  """F-E2反証：送信JSONの入れ子とpayload fieldの相互照合。"""

  def test_fragment_replaced_by_free_text_is_blocked(self, tmp_path):
    import dataclasses

    built = _build_payload(tmp_path)
    document = json.loads(built.content)
    document["fragment_a"] = {"free_text": "内部の説明文がここから漏れる。"}
    content = json.dumps(
      document, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )
    forged = dataclasses.replace(
      built,
      content=content,
      digest=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )
    result = _run(
      tmp_path,
      payload=forged,
      approved_payload_digests=[forged.digest],
      list_digest=importlib.import_module(
        "tools.egress.approval"
      ).payload_list_digest([forged.digest]),
    )
    assert result.allowed is False

  def test_allowlisted_feature_with_free_text_value_is_blocked(self, tmp_path):
    import dataclasses

    built = _build_payload(tmp_path)
    document = json.loads(built.content)
    features = dict(document["machine_features_a"])
    features["line_count"] = "この関数は内部仕様を説明する自由文である。"
    document["machine_features_a"] = features
    content = json.dumps(
      document, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )
    forged = dataclasses.replace(
      built,
      machine_features_a=features,
      content=content,
      digest=hashlib.sha256(content.encode("utf-8")).hexdigest(),
    )
    result = _run(
      tmp_path,
      payload=forged,
      approved_payload_digests=[forged.digest],
      list_digest=importlib.import_module(
        "tools.egress.approval"
      ).payload_list_digest([forged.digest]),
    )
    assert result.allowed is False


class TestInjectedCallbackIsRejectedBeforeExecution:
  """F-E5反証：許可実装でないcallbackは実行される前に拒否される。"""

  def _marker_hook(self, marker):
    def hook(text):
      marker.write_text("executed", encoding="utf-8")
      return text

    return hook

  def test_gate_does_not_execute_unapproved_hook(self, tmp_path):
    marker = tmp_path / "hook-executed.marker"
    result = _run(tmp_path, redaction_hook=self._marker_hook(marker))
    assert result.allowed is False
    assert not marker.exists()

  def test_stage_one_runner_does_not_execute_unapproved_hook(self, tmp_path):
    sender = _sender()
    approval = importlib.import_module("tools.egress.approval")
    marker = tmp_path / "hook-executed.marker"
    built = _build_payload(tmp_path)
    record_path, record_digest = _approval_file(
      tmp_path, approval.payload_list_digest([built.digest])
    )
    runner = sender.build_stage_one_runner(
      repository_root=tmp_path,
      approved_payload_digests=[built.digest],
      approval_record_path=record_path,
      approval_record_sha256=record_digest,
      provider="anthropic-api",
      model="claude-sonnet-5",
      redaction_hook=self._marker_hook(marker),
    )
    with pytest.raises(sender.EgressGateRefusal):
      runner("primary", built)
    assert not marker.exists()


class TestStageOneSender:
  def test_gate_passing_payload_still_cannot_send(self, tmp_path):
    gate = _gate()
    sender = _sender()
    approval = importlib.import_module("tools.egress.approval")
    built = _build_payload(tmp_path)
    record_path, record_digest = _approval_file(
      tmp_path, approval.payload_list_digest([built.digest])
    )
    runner = sender.build_stage_one_runner(
      repository_root=tmp_path,
      approved_payload_digests=[built.digest],
      approval_record_path=record_path,
      approval_record_sha256=record_digest,
      provider="anthropic-api",
      model="claude-sonnet-5",
      redaction_hook=gate.APPROVED_REDACTION_HOOK,
    )
    with pytest.raises(sender.EgressSendingNotApproved):
      runner("primary", built)

  def test_gate_failing_payload_raises_gate_error(self, tmp_path):
    gate = _gate()
    sender = _sender()
    built = _build_payload(tmp_path)
    record_path, record_digest = _approval_file(tmp_path, "0" * 64)
    runner = sender.build_stage_one_runner(
      repository_root=tmp_path,
      approved_payload_digests=["f" * 64],
      approval_record_path=record_path,
      approval_record_sha256=record_digest,
      provider="anthropic-api",
      model="claude-sonnet-5",
      redaction_hook=gate.APPROVED_REDACTION_HOOK,
    )
    with pytest.raises(sender.EgressGateRefusal) as caught:
      runner("primary", built)
    assert "外部送信せず停止" in str(caught.value)
