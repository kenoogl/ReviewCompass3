"""セッションログの機微情報伏字化。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
import math
import re
from pathlib import Path


HIGH_ENTROPY_TOKEN = re.compile(
  r"(?<![A-Za-z0-9_-])[A-Za-z0-9_-]{24,}(?![A-Za-z0-9_-])"
)


class SensitiveDataRemaining(Exception):
  """伏字化後も機微情報候補が残っている。"""

  def __init__(self, findings):
    self.findings = tuple(findings)
    self.count = len(self.findings)
    super().__init__(
      "High-entropy sensitive data remains: %d candidate(s)" % self.count
    )


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


@dataclasses.dataclass(frozen=True)
class HighEntropyFinding:
  start: int
  end: int
  length: int
  entropy: float


def _entropy(value) -> float:
  length = len(value)
  return -sum(
    (count / length) * math.log2(count / length)
    for count in {character: value.count(character) for character in value}.values()
  )


def find_high_entropy(
  text,
  *,
  minimum_length=24,
  minimum_entropy=3.5,
  allow_patterns=(),
) -> tuple:
  findings = []
  for match in HIGH_ENTROPY_TOKEN.finditer(text):
    candidate = match.group(0)
    if len(candidate) < minimum_length:
      continue
    if any(re.fullmatch(pattern, candidate) for pattern in allow_patterns):
      continue
    entropy = _entropy(candidate)
    if entropy >= minimum_entropy:
      findings.append(HighEntropyFinding(
        start=match.start(),
        end=match.end(),
        length=len(candidate),
        entropy=entropy,
      ))
  return tuple(findings)


def redact_text(text, rules) -> RedactionResult:
  redacted = text
  findings = []
  for rule in rules:
    replacement = "[REDACTED:%s]" % rule.label
    redacted, count = re.subn(rule.pattern, replacement, redacted)
    if count:
      findings.append(Finding(label=rule.label, count=count))
  return RedactionResult(text=redacted, findings=tuple(findings))


def redact_text_strict(text, rules, *, allow_patterns=()) -> RedactionResult:
  result = redact_text(text, rules)
  remaining = find_high_entropy(
    result.text,
    allow_patterns=allow_patterns,
  )
  if remaining:
    raise SensitiveDataRemaining(remaining)
  return result


def write_sensitive_report(path, error, *, source_path):
  report_path = Path(path)
  report_path.parent.mkdir(parents=True, exist_ok=True)
  report = {
    "source_path": source_path,
    "count": error.count,
    "findings": [
      dataclasses.asdict(finding)
      for finding in error.findings
    ],
  }
  report_path.write_text(
    json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
  )
