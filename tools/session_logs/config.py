"""セッションログ基盤の暫定設定。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
from pathlib import Path

from tools.session_logs.redaction import Rule


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


def load_config(path) -> Config:
  config_path = Path(path)
  data = json.loads(config_path.read_text(encoding="utf-8"))
  base = config_path.parent
  repository_root = data.get("repository_root")
  report_root = data.get("sensitive_report_root")
  backup_root = data.get("backup_root")
  ledger_path = data.get("preservation_ledger_path")
  hook_event_log_path = data.get("hook_event_log_path")
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
    redaction_rules=tuple(
      Rule(label=item["label"], pattern=item["pattern"])
      for item in data.get("redaction_rules", ())
    ),
    allow_patterns=tuple(data.get("allow_patterns", ())),
  )
  _validate_storage_boundaries(config)
  return config
