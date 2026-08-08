"""セッションログ基盤の暫定設定。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
from pathlib import Path

from tools.session_logs.redaction import (
  EnvironmentRule,
  Rule,
  environment_reference_rules,
)


class ConfigError(Exception):
  """保存区分を含む設定が安全ではない。"""


@dataclasses.dataclass(frozen=True)
class Config:
  repository_root: object
  raw_root: Path
  transcript_root: Path
  summary_root: Path
  provenance_root: Path
  sensitive_report_root: object
  backup_root: object
  preservation_ledger_path: object
  summary_revision_range: object
  hook_event_log_path: object
  preservation_enabled: bool
  tool_version: str
  redaction_rules: tuple
  allow_patterns: tuple
  environment_redaction_rules: tuple = ()


def _resolve(base, value):
  path = Path(value)
  return (
    path
    if path.is_absolute()
    else base / path
  ).resolve()


def _resolved(path):
  return Path(path).resolve()


from tools.common.paths import within as _within


def _validate_storage_boundaries(config):
  if config.repository_root is None:
    return
  repository_root = _resolved(config.repository_root)
  if not (repository_root / ".git").exists():
    raise ConfigError("Invalid repository boundary")
  private_roots = (
    ("raw_root", config.raw_root),
    ("transcript_root", config.transcript_root),
    ("sensitive_report_root", config.sensitive_report_root),
    ("backup_root", config.backup_root),
    ("hook_event_log_path", config.hook_event_log_path),
  )
  for name, path in private_roots:
    if path is not None and _within(path, repository_root):
      raise ConfigError("Unsafe Git storage boundary: %s" % name)
  git_roots = (
    ("summary_root", config.summary_root),
    ("provenance_root", config.provenance_root),
  )
  for name, path in git_roots:
    if not _within(path, repository_root):
      raise ConfigError("Unsafe Git storage boundary: %s" % name)


def _parse_redaction_rules(items):
  """pattern宣言とenvironment reference宣言を区別して読み込む。

  両方を持つ項目、どちらも持たない項目、未知roleはfail-closedとし、
  例外文に入力値を含めない。
  """

  known_roles = frozenset(
    rule.environment_role
    for rule in environment_reference_rules()
  )
  pattern_rules = []
  environment_rules = []
  for item in items:
    has_pattern = "pattern" in item
    has_role = "environment_role" in item
    if has_pattern == has_role:
      raise ConfigError("Invalid redaction rule declaration")
    if has_role:
      if item["environment_role"] not in known_roles:
        raise ConfigError("Unknown environment reference role")
      environment_rules.append(EnvironmentRule(
        label=item["label"],
        environment_role=item["environment_role"],
      ))
    else:
      pattern_rules.append(Rule(
        label=item["label"],
        pattern=item["pattern"],
      ))
  return tuple(pattern_rules), tuple(environment_rules)


def load_config(path) -> Config:
  config_path = Path(path)
  data = json.loads(config_path.read_text(encoding="utf-8"))
  base = config_path.parent
  repository_root = data.get("repository_root")
  report_root = data.get("sensitive_report_root")
  backup_root = data.get("backup_root")
  ledger_path = data.get("preservation_ledger_path")
  hook_event_log_path = data.get("hook_event_log_path")
  pattern_rules, environment_rules = _parse_redaction_rules(
    data.get("redaction_rules", ())
  )
  config = Config(
    repository_root=(
      _resolve(base, repository_root).resolve()
      if repository_root is not None
      else None
    ),
    raw_root=_resolve(base, data["raw_root"]),
    transcript_root=_resolve(base, data["transcript_root"]),
    summary_root=_resolve(base, data["summary_root"]),
    provenance_root=_resolve(base, data["provenance_root"]),
    sensitive_report_root=(
      _resolve(base, report_root)
      if report_root is not None
      else None
    ),
    backup_root=(
      _resolve(base, backup_root)
      if backup_root is not None
      else None
    ),
    preservation_ledger_path=(
      _resolve(base, ledger_path)
      if ledger_path is not None
      else None
    ),
    summary_revision_range=data.get("summary_revision_range"),
    hook_event_log_path=(
      _resolve(base, hook_event_log_path)
      if hook_event_log_path is not None
      else None
    ),
    preservation_enabled=bool(
      data.get("preservation_enabled", False)
    ),
    tool_version=data["tool_version"],
    redaction_rules=pattern_rules,
    allow_patterns=tuple(data.get("allow_patterns", ())),
    environment_redaction_rules=environment_rules,
  )
  _validate_storage_boundaries(config)
  return config
