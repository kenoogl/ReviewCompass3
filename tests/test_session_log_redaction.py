"""セッションログ機微情報伏字化の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


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
