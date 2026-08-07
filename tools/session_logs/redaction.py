"""セッションログの機微情報伏字化。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
import math
import re
import socket
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
class EnvironmentRule:
  """環境依存値の規則。実値を持たず、役割の名前だけを持つ。

  実値を規則へ書くと、規則file自体が環境情報の記録になり、配置換えで当たらなくなった
  うえ古い環境情報だけが残る。値は実行のたびに解決する。
  """

  label: str
  environment_role: str
  pattern: str = None


@dataclasses.dataclass(frozen=True)
class ResolvedEnvironmentRule:
  """解決済みの環境規則。patternに実値を含むため、記録経路へ渡してはならない。

  digest計算では役割名だけを使う（`redaction_rules_digest_payload`が種別で判別する）。
  誤って解決済み規則を渡しても実値がdigestへ入らないようにするための型である。
  """

  label: str
  pattern: str
  environment_role: str


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


DEFAULT_PATTERN_RULES = (
  Rule(
    label="email",
    pattern=r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
  ),
  Rule(
    label="bearer_token",
    pattern=r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{16,}=*",
  ),
  Rule(
    label="api_key_assignment",
    pattern=(
      r"(?i)\b(?:api[_-]?key|secret|token|password)\b\s*[=:]\s*"
      r"[\"']?[A-Za-z0-9._~+/-]{12,}[\"']?"
    ),
  ),
  Rule(
    label="private_key_block",
    pattern=r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----",
  ),
  Rule(
    label="aws_access_key_id",
    pattern=r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b",
  ),
)

ENVIRONMENT_RULES = (
  EnvironmentRule(label="home_directory", environment_role="home_directory"),
  EnvironmentRule(label="user_name", environment_role="user_name"),
  EnvironmentRule(label="host_name", environment_role="host_name"),
)


def default_pattern_rules() -> tuple:
  """承認済みの初版pattern規則。網羅ではなく出発点である。"""

  return DEFAULT_PATTERN_RULES


def environment_reference_rules() -> tuple:
  """環境依存参照の規則。役割名だけを持ち、実値は持たない。"""

  return ENVIRONMENT_RULES


def _resolve_environment_role(role) -> str:
  if role == "home_directory":
    return str(Path.home())
  if role == "user_name":
    return Path.home().name
  if role == "host_name":
    return socket.gethostname()
  raise ValueError("unknown environment role")


def resolve_environment_rules(rules) -> tuple:
  """実行時に環境から値を解決し、patternを持つRuleへ変換する。

  解決した値は戻り値の中にしか現れず、規則fileへは書き戻さない。
  """

  resolved = []
  for rule in rules:
    value = _resolve_environment_role(rule.environment_role)
    if not value:
      continue
    resolved.append(ResolvedEnvironmentRule(
      label=rule.label,
      pattern=re.escape(value),
      environment_role=rule.environment_role,
    ))
  # 長い値から先に消す。短い値（ユーザー名）が長い値（home path）の一部を
  # 先に置換すると、結果が入力順に依存してしまう。
  resolved.sort(key=lambda rule: len(rule.pattern), reverse=True)
  return tuple(resolved)


def redaction_rules_digest_payload(rules, *, allow_patterns=()) -> str:
  """digestの入力を返す。環境依存規則は役割名だけを入れ、解決値を入れない。"""

  entries = []
  for rule in rules:
    # 宣言済み規則も解決済み規則も、digestへ入れるのは役割名だけとする。
    # 解決済みを誤って渡しても実値がdigestの入力にならない。
    if isinstance(rule, (EnvironmentRule, ResolvedEnvironmentRule)):
      entries.append({
        "label": rule.label,
        "environment_role": rule.environment_role,
      })
    else:
      entries.append({"label": rule.label, "pattern": rule.pattern})
  payload = {
    "rules": entries,
    "allow_patterns": list(allow_patterns),
  }
  return json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
  )


def redaction_rules_digest(rules, *, allow_patterns=()) -> str:
  encoded = redaction_rules_digest_payload(
    rules,
    allow_patterns=allow_patterns,
  ).encode("utf-8")
  return hashlib.sha256(encoded).hexdigest()


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


def redact_with_environment(
  text,
  *,
  pattern_rules=None,
  environment_rules=None,
  allow_patterns=(),
  strict=False,
) -> RedactionResult:
  """環境依存参照とpattern規則を決定的な順序で適用する。

  順序は(1)環境依存参照（長い値から先に）、(2)pattern規則、(3)strictなら高entropy網。
  置換先には役割名・labelだけが出るため、実値は結果テキストへ残らない。
  """

  resolved = resolve_environment_rules(
    environment_rules if environment_rules is not None else ENVIRONMENT_RULES
  )
  patterns = (
    pattern_rules if pattern_rules is not None else DEFAULT_PATTERN_RULES
  )
  ordered = tuple(resolved) + tuple(patterns)
  if strict:
    return redact_text_strict(text, ordered, allow_patterns=allow_patterns)
  return redact_text(text, ordered)


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
