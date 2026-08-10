"""送信payloadの構成と由来の解決（出口設計v4 §3・§5条件1〜2）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def _payload():
  return importlib.import_module("tools.egress.payload")


def _write_source(tmp_path, relative_path, lines):
  target = tmp_path / relative_path
  target.parent.mkdir(parents=True, exist_ok=True)
  target.write_text("\n".join(lines) + "\n", encoding="utf-8")
  return target


def _routine(relative_path, start_line, end_line, **overrides):
  base = {
    "symbol_id": f"{relative_path}:sample",
    "code_reference": {
      "relative_path": relative_path,
      "start_line": start_line,
      "end_line": end_line,
    },
    "signature": {"parameters": [{"name": "x"}], "returns_annotation": None},
    "return_count": 1,
    "raise_count": 0,
    "raised_exception_names": [],
    "branch_count": 2,
    "line_count": end_line - start_line + 1,
    "max_nesting_depth": 1,
    "complexity_signal": "low",
    "public_api_signal": "medium",
    "docstring_first_line": "この説明文は外へ出てはならない。",
    "responsibility_class_proposal": "ownership_unclear",
  }
  base.update(overrides)
  return base


class TestCutCodeFragment:
  def test_cut_matches_file_lines_and_digest(self, tmp_path):
    payload = _payload()
    _write_source(
      tmp_path, "pkg/mod.py", ["line1", "line2", "line3", "line4"]
    )
    fragment = payload.cut_code_fragment(
      tmp_path,
      {"relative_path": "pkg/mod.py", "start_line": 2, "end_line": 3},
    )
    assert fragment.content == "line2\nline3"
    assert fragment.content_sha256 == hashlib.sha256(
      "line2\nline3".encode("utf-8")
    ).hexdigest()

  def test_out_of_range_is_rejected(self, tmp_path):
    payload = _payload()
    _write_source(tmp_path, "pkg/mod.py", ["line1", "line2"])
    for start, end in ((0, 1), (1, 3), (2, 1)):
      with pytest.raises(payload.PayloadError):
        payload.cut_code_fragment(
          tmp_path,
          {
            "relative_path": "pkg/mod.py",
            "start_line": start,
            "end_line": end,
          },
        )

  def test_escape_paths_are_rejected(self, tmp_path):
    payload = _payload()
    _write_source(tmp_path, "pkg/mod.py", ["line1"])
    for relative in ("../outside.py", "/etc/passwd"):
      with pytest.raises(payload.PayloadError):
        payload.cut_code_fragment(
          tmp_path,
          {"relative_path": relative, "start_line": 1, "end_line": 1},
        )

  def test_missing_file_is_rejected(self, tmp_path):
    payload = _payload()
    with pytest.raises(payload.PayloadError):
      payload.cut_code_fragment(
        tmp_path,
        {"relative_path": "pkg/none.py", "start_line": 1, "end_line": 1},
      )


class TestMachineFeatures:
  def test_free_text_fields_never_pass(self, tmp_path):
    payload = _payload()
    features = payload.build_machine_features(
      _routine("pkg/mod.py", 1, 2)
    )
    assert set(features) <= set(payload.MACHINE_FEATURE_ALLOWLIST)
    assert "docstring_first_line" not in features
    assert "responsibility_class_proposal" not in features
    assert "この説明文は外へ出てはならない。" not in json.dumps(
      features, ensure_ascii=False
    )

  def test_parameter_count_is_derived(self):
    payload = _payload()
    features = payload.build_machine_features(_routine("pkg/mod.py", 1, 2))
    assert features["parameter_count"] == 1
    assert features["line_count"] == 2


class TestQuestionTemplate:
  def test_approved_template_resolves(self):
    payload = _payload()
    text = payload.resolve_question("impl-sameness-v1")
    assert "同じ処理を実装しているか" in text
    assert "相違点" in text

  def test_unknown_template_is_rejected(self):
    payload = _payload()
    with pytest.raises(payload.PayloadError):
      payload.resolve_question("free-form-question")


class TestBuildPairPayload:
  def _build(self, tmp_path):
    payload = _payload()
    _write_source(tmp_path, "pkg/a.py", ["def a():", "  return 1"])
    _write_source(tmp_path, "pkg/b.py", ["def b():", "  return 2"])
    return payload.build_pair_payload(
      repository_root=tmp_path,
      routine_a=_routine("pkg/a.py", 1, 2),
      routine_b=_routine("pkg/b.py", 1, 2),
      question_id="impl-sameness-v1",
    )

  def test_content_holds_exactly_the_three_kinds(self, tmp_path):
    built = self._build(tmp_path)
    document = json.loads(built.content)
    assert set(document) == {
      "schema_version",
      "question_id",
      "question_text",
      "fragment_a",
      "fragment_b",
      "machine_features_a",
      "machine_features_b",
    }
    assert "この説明文は外へ出てはならない。" not in built.content

  def test_digest_is_deterministic(self, tmp_path):
    first = self._build(tmp_path)
    second = self._build(tmp_path)
    assert first.digest == second.digest
    assert first.digest == hashlib.sha256(
      first.content.encode("utf-8")
    ).hexdigest()


class TestFragmentProvenance:
  def test_untouched_fragment_passes(self, tmp_path):
    payload = _payload()
    _write_source(tmp_path, "pkg/mod.py", ["line1", "line2"])
    fragment = payload.cut_code_fragment(
      tmp_path,
      {"relative_path": "pkg/mod.py", "start_line": 1, "end_line": 2},
    )
    payload.verify_fragment_provenance(tmp_path, fragment)

  def test_modified_source_is_detected(self, tmp_path):
    payload = _payload()
    target = _write_source(tmp_path, "pkg/mod.py", ["line1", "line2"])
    fragment = payload.cut_code_fragment(
      tmp_path,
      {"relative_path": "pkg/mod.py", "start_line": 1, "end_line": 2},
    )
    target.write_text("changed\nlines\n", encoding="utf-8")
    with pytest.raises(payload.PayloadError):
      payload.verify_fragment_provenance(tmp_path, fragment)


class TestFragmentContentIsBoundToSource:
  """F-E2反証：断片本文がsource外へ差し替えられたものは通らない。"""

  def test_content_replaced_with_outside_text_is_detected(self, tmp_path):
    import dataclasses

    payload = _payload()
    _write_source(tmp_path, "pkg/mod.py", ["line1", "line2"])
    fragment = payload.cut_code_fragment(
      tmp_path,
      {"relative_path": "pkg/mod.py", "start_line": 1, "end_line": 2},
    )
    forged = dataclasses.replace(
      fragment, content="source外の自由文がここから漏れる。"
    )
    with pytest.raises(payload.PayloadError):
      payload.verify_fragment_provenance(tmp_path, forged)

  def test_declared_line_range_must_match_content(self, tmp_path):
    import dataclasses

    payload = _payload()
    _write_source(tmp_path, "pkg/mod.py", ["line1", "line2", "line3"])
    fragment = payload.cut_code_fragment(
      tmp_path,
      {"relative_path": "pkg/mod.py", "start_line": 1, "end_line": 2},
    )
    forged = dataclasses.replace(fragment, start_line=2, end_line=3)
    with pytest.raises(payload.PayloadError):
      payload.verify_fragment_provenance(tmp_path, forged)
