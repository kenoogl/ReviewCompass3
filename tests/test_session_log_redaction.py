"""セッションログ機微情報伏字化の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_redacts_known_patterns_and_reports_only_label_and_count():
  redaction = importlib.import_module("tools.session_logs.redaction")
  rules = (
    redaction.Rule(
      label="anthropic_key",
      pattern=r"sk-ant-[A-Za-z0-9_-]+",
    ),
  )
  secret_1 = "sk-ant-first_secret"
  secret_2 = "sk-ant-second_secret"
  text = "first=%s\nsafe=value\nsecond=%s\n" % (secret_1, secret_2)

  result = redaction.redact_text(text, rules)

  assert result.text == (
    "first=[REDACTED:anthropic_key]\n"
    "safe=value\n"
    "second=[REDACTED:anthropic_key]\n"
  )
  assert result.findings == (
    redaction.Finding(label="anthropic_key", count=2),
  )
  assert secret_1 not in repr(result)
  assert secret_2 not in repr(result)


def test_detects_high_entropy_without_returning_secret_value():
  redaction = importlib.import_module("tools.session_logs.redaction")
  secret = "A9fK2mQ7xR4vT8pL3nC6sW1yH5jD0bZ"

  findings = redaction.find_high_entropy("token=%s" % secret)

  assert len(findings) == 1
  assert findings[0].length == len(secret)
  assert findings[0].entropy >= 3.5
  assert secret not in repr(findings)


def test_strict_redaction_fails_closed_without_leaking_secret():
  redaction = importlib.import_module("tools.session_logs.redaction")
  secret = "A9fK2mQ7xR4vT8pL3nC6sW1yH5jD0bZ"

  with pytest.raises(redaction.SensitiveDataRemaining) as error:
    redaction.redact_text_strict("token=%s" % secret, ())

  assert secret not in repr(error.value)
  assert error.value.count == 1

  safe = "repeated=%s" % ("a" * 40)
  assert redaction.redact_text_strict(safe, ()).text == safe
