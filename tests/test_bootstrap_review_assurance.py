"""ブートストラップreview独立変異・障害注入検査の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


def test_detects_all_independent_mutations_and_failures():
  review_assurance = importlib.import_module(
    "tools.bootstrap.review_assurance"
  )

  report = review_assurance.run_bootstrap_review_assurance()

  assert report.status == "passed"
  assert report.passed_count == 6
  assert report.failed_count == 0
  assert tuple(check.name for check in report.checks) == (
    "digest_mutation",
    "schema_mutation",
    "missing_route",
    "immutable_raw_store",
    "provider_partial_failure",
    "resume_preserves_success",
  )
  assert {
    check.status
    for check in report.checks
  } == {"detected"}


def test_reports_failed_when_independent_check_is_not_detected():
  review_assurance = importlib.import_module(
    "tools.bootstrap.review_assurance"
  )

  report = review_assurance.run_bootstrap_review_assurance(
    overrides={"digest_mutation": lambda: False},
  )

  assert report.status == "failed"
  assert report.passed_count == 5
  assert report.failed_count == 1
