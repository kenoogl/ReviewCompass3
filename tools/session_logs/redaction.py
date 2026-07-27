"""セッションログの機微情報伏字化。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import re


@dataclasses.dataclass(frozen=True)
class Rule:
  label: str
  pattern: str


@dataclasses.dataclass(frozen=True)
class Finding:
  label: str
  count: int


@dataclasses.dataclass(frozen=True)
class RedactionResult:
  text: str
  findings: tuple


def redact_text(text, rules) -> RedactionResult:
  redacted = text
  findings = []
  for rule in rules:
    replacement = "[REDACTED:%s]" % rule.label
    redacted, count = re.subn(rule.pattern, replacement, redacted)
    if count:
      findings.append(Finding(label=rule.label, count=count))
  return RedactionResult(text=redacted, findings=tuple(findings))
