"""ローカル事前分類（出口設計v4 §3.1）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def _prefilter():
  return importlib.import_module("tools.egress.prefilter")


def _routine(**overrides):
  base = {
    "signature": {"parameters": [], "returns_annotation": None},
    "return_count": 1,
    "raise_count": 0,
    "raised_exception_names": [],
    "branch_count": 2,
    "line_count": 10,
  }
  base.update(overrides)
  return base


class TestIdentifierTokens:
  def test_camel_case_is_split_and_lowered(self):
    prefilter = _prefilter()
    assert prefilter.identifier_tokens("BatchReassessmentResult") == frozenset(
      {"batch", "reassessment", "result"}
    )

  def test_snake_case_is_split(self):
    prefilter = _prefilter()
    assert prefilter.identifier_tokens("load_project_yaml") == frozenset(
      {"load", "project", "yaml"}
    )

  def test_reserved_words_and_short_tokens_are_dropped(self):
    prefilter = _prefilter()
    tokens = prefilter.identifier_tokens(
      "def _verify_bundle(self):\n  return None"
    )
    assert tokens == frozenset({"verify", "bundle"})


class TestJaccard:
  def test_both_empty_is_one(self):
    prefilter = _prefilter()
    assert prefilter.jaccard(frozenset(), frozenset()) == 1.0

  def test_one_empty_is_zero(self):
    prefilter = _prefilter()
    assert prefilter.jaccard(frozenset({"a"}), frozenset()) == 0.0

  def test_partial_overlap(self):
    prefilter = _prefilter()
    value = prefilter.jaccard(
      frozenset({"aa", "bb"}), frozenset({"bb", "cc"})
    )
    assert value == pytest.approx(1 / 3)


class TestFeatureMatch:
  def test_identical_routines_score_full(self):
    prefilter = _prefilter()
    assert prefilter.feature_match(_routine(), _routine()) == 1.0

  def test_two_differences_drop_two_sixths(self):
    prefilter = _prefilter()
    other = _routine(
      raised_exception_names=["ValueError"],
      branch_count=7,
    )
    assert prefilter.feature_match(_routine(), other) == pytest.approx(4 / 6)


class TestClassifyPair:
  def test_identical_pair_is_clearly_same(self):
    prefilter = _prefilter()
    result = prefilter.classify_pair(
      code_a="alpha_beta gamma",
      code_b="alpha_beta gamma",
      name_a="make_widget",
      name_b="make_widget",
      routine_a=_routine(),
      routine_b=_routine(),
    )
    assert result.band == "clearly_same"
    assert result.similarity == pytest.approx(1.0)

  def test_disjoint_pair_is_clearly_diff(self):
    prefilter = _prefilter()
    result = prefilter.classify_pair(
      code_a="alpha_beta gamma",
      code_b="delta_epsilon zeta",
      name_a="make_widget",
      name_b="restore_backup",
      routine_a=_routine(),
      routine_b=_routine(
        signature={"parameters": [{"name": "x"}], "returns_annotation": None},
        return_count=3,
        raise_count=2,
        raised_exception_names=["ValueError"],
        branch_count=9,
        line_count=40,
      ),
    )
    assert result.band == "clearly_diff"
    assert result.similarity <= 0.45

  def test_partial_overlap_is_ambiguous(self):
    prefilter = _prefilter()
    result = prefilter.classify_pair(
      code_a="aaa_bbb ccc",
      code_b="aaa_bbb ddd",
      name_a="make_widget",
      name_b="make_widget",
      routine_a=_routine(),
      routine_b=_routine(),
    )
    assert result.body_similarity == pytest.approx(0.5)
    assert result.similarity == pytest.approx(0.7)
    assert result.band == "ambiguous"

  def test_thresholds_are_the_approved_initial_values(self):
    prefilter = _prefilter()
    thresholds = prefilter.DEFAULT_THRESHOLDS
    assert thresholds.same_min == pytest.approx(0.85)
    assert thresholds.diff_max == pytest.approx(0.45)
    assert thresholds.body_weight == pytest.approx(0.6)
    assert thresholds.name_weight == pytest.approx(0.2)
    assert thresholds.feature_weight == pytest.approx(0.2)

  def test_threshold_override_changes_band(self):
    prefilter = _prefilter()
    lowered = prefilter.Thresholds(
      same_min=0.65,
      diff_max=0.45,
      body_weight=0.6,
      name_weight=0.2,
      feature_weight=0.2,
    )
    result = prefilter.classify_pair(
      code_a="aaa_bbb ccc",
      code_b="aaa_bbb ddd",
      name_a="make_widget",
      name_b="make_widget",
      routine_a=_routine(),
      routine_b=_routine(),
      thresholds=lowered,
    )
    assert result.band == "clearly_same"

  def test_invalid_routine_is_rejected(self):
    prefilter = _prefilter()
    with pytest.raises(prefilter.PrefilterError):
      prefilter.classify_pair(
        code_a="aaa",
        code_b="bbb",
        name_a="a_name",
        name_b="b_name",
        routine_a={"line_count": 1},
        routine_b=_routine(),
      )


class TestThresholdsAreValidated:
  """F-E4反証：非有限値・範囲外の閾値でHuman承認済み分類を迂回できない。"""

  def _classify(self, thresholds):
    prefilter = _prefilter()
    return prefilter.classify_pair(
      code_a="aaa_bbb ccc",
      code_b="aaa_bbb ccc",
      name_a="make_widget",
      name_b="make_widget",
      routine_a=_routine(),
      routine_b=_routine(),
      thresholds=thresholds,
    )

  def _thresholds(self, **overrides):
    prefilter = _prefilter()
    values = {
      "same_min": 0.85,
      "diff_max": 0.45,
      "body_weight": 0.6,
      "name_weight": 0.2,
      "feature_weight": 0.2,
    }
    values.update(overrides)
    return prefilter.Thresholds(**values)

  def test_default_thresholds_still_classify(self):
    prefilter = _prefilter()
    assert self._classify(prefilter.DEFAULT_THRESHOLDS).band == "clearly_same"

  def test_non_finite_weight_is_rejected(self):
    prefilter = _prefilter()
    with pytest.raises(prefilter.PrefilterError):
      self._classify(self._thresholds(body_weight=float("nan")))

  def test_infinite_threshold_is_rejected(self):
    prefilter = _prefilter()
    with pytest.raises(prefilter.PrefilterError):
      self._classify(self._thresholds(same_min=float("inf")))

  def test_out_of_range_threshold_is_rejected(self):
    prefilter = _prefilter()
    with pytest.raises(prefilter.PrefilterError):
      self._classify(self._thresholds(same_min=1.5))

  def test_negative_weight_is_rejected(self):
    prefilter = _prefilter()
    with pytest.raises(prefilter.PrefilterError):
      self._classify(self._thresholds(name_weight=-0.2, body_weight=0.8))

  def test_same_min_not_above_diff_max_is_rejected(self):
    prefilter = _prefilter()
    with pytest.raises(prefilter.PrefilterError):
      self._classify(self._thresholds(same_min=0.4, diff_max=0.45))

  def test_weights_not_summing_to_one_are_rejected(self):
    prefilter = _prefilter()
    with pytest.raises(prefilter.PrefilterError):
      self._classify(self._thresholds(body_weight=0.9))
