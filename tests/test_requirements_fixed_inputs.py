"""第4段の固定入力照合に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def _write_json(path, value):
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(
    json.dumps(value, ensure_ascii=False),
    encoding="utf-8",
  )
  return hashlib.sha256(path.read_bytes()).hexdigest()


def _entry(path, digest, **overrides):
  value = {
    "path": path,
    "sha256": digest,
    "assertions": (),
  }
  value.update(overrides)
  return value


def test_verifies_digest_and_approved_values(tmp_path):
  fixed_inputs = importlib.import_module(
    "tools.requirements.fixed_inputs"
  )
  approval_path = tmp_path / "records" / "approval.json"
  digest = _write_json(
    approval_path,
    {
      "approval": {
        "approved": True,
        "material_digest": "a" * 64,
      },
    },
  )

  result = fixed_inputs.verify_fixed_inputs(
    root=tmp_path,
    inputs=(
      _entry(
        "records/approval.json",
        digest,
        assertions=(
          {
            "pointer": "/approval/approved",
            "expected": True,
          },
          {
            "pointer": "/approval/material_digest",
            "expected": "a" * 64,
          },
        ),
      ),
    ),
  )

  assert result.status == "ready"
  assert result.mismatches == ()
  assert len(result.digest) == 64


def test_marks_changed_input_stale(tmp_path):
  fixed_inputs = importlib.import_module(
    "tools.requirements.fixed_inputs"
  )
  path = tmp_path / "intent.md"
  path.write_text("changed", encoding="utf-8")

  result = fixed_inputs.verify_fixed_inputs(
    root=tmp_path,
    inputs=(
      _entry("intent.md", "b" * 64),
    ),
  )

  assert result.status == "stale"
  assert result.mismatches[0].kind == "sha256"
  assert result.mismatches[0].path == "intent.md"


def test_marks_changed_approval_value_stale(tmp_path):
  fixed_inputs = importlib.import_module(
    "tools.requirements.fixed_inputs"
  )
  path = tmp_path / "approval.json"
  digest = _write_json(
    path,
    {"approval": {"approved": False}},
  )

  result = fixed_inputs.verify_fixed_inputs(
    root=tmp_path,
    inputs=(
      _entry(
        "approval.json",
        digest,
        assertions=(
          {
            "pointer": "/approval/approved",
            "expected": True,
          },
        ),
      ),
    ),
  )

  assert result.status == "stale"
  assert result.mismatches[0].kind == "assertion"


@pytest.mark.parametrize(
  "path",
  (
    "/absolute.json",
    "../outside.json",
    "nested/../../outside.json",
  ),
)
def test_rejects_paths_outside_fixed_root(tmp_path, path):
  fixed_inputs = importlib.import_module(
    "tools.requirements.fixed_inputs"
  )

  with pytest.raises(fixed_inputs.FixedInputError):
    fixed_inputs.verify_fixed_inputs(
      root=tmp_path,
      inputs=(_entry(path, "c" * 64),),
    )


def test_rejects_duplicate_paths_or_invalid_digest(tmp_path):
  fixed_inputs = importlib.import_module(
    "tools.requirements.fixed_inputs"
  )
  path = tmp_path / "input.json"
  digest = _write_json(path, {})

  with pytest.raises(fixed_inputs.FixedInputError):
    fixed_inputs.verify_fixed_inputs(
      root=tmp_path,
      inputs=(
        _entry("input.json", digest),
        _entry("input.json", digest),
      ),
    )

  with pytest.raises(fixed_inputs.FixedInputError):
    fixed_inputs.verify_fixed_inputs(
      root=tmp_path,
      inputs=(_entry("input.json", "not-a-digest"),),
    )


def test_missing_input_is_stale_without_reading_outside_root(
  tmp_path,
):
  fixed_inputs = importlib.import_module(
    "tools.requirements.fixed_inputs"
  )

  result = fixed_inputs.verify_fixed_inputs(
    root=tmp_path,
    inputs=(_entry("missing.json", "d" * 64),),
  )

  assert result.status == "stale"
  assert result.mismatches[0].kind == "missing"
