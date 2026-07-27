"""セッションログ基盤の暫定設定。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
from pathlib import Path

from tools.session_logs.redaction import Rule


@dataclasses.dataclass(frozen=True)
class Config:
  raw_root: Path
  transcript_root: Path
  summary_root: Path
  provenance_root: Path
  sensitive_report_root: object
  backup_root: object
  preservation_enabled: bool
  tool_version: str
  redaction_rules: tuple
  allow_patterns: tuple


def _resolve(base, value):
  path = Path(value)
  return path if path.is_absolute() else base / path


def load_config(path) -> Config:
  config_path = Path(path)
  data = json.loads(config_path.read_text(encoding="utf-8"))
  base = config_path.parent
  report_root = data.get("sensitive_report_root")
  backup_root = data.get("backup_root")
  return Config(
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
