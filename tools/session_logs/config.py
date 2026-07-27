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
  tool_version: str
  redaction_rules: tuple


def _resolve(base, value):
  path = Path(value)
  return path if path.is_absolute() else base / path


def load_config(path) -> Config:
  config_path = Path(path)
  data = json.loads(config_path.read_text(encoding="utf-8"))
  base = config_path.parent
  return Config(
    raw_root=_resolve(base, data["raw_root"]),
    transcript_root=_resolve(base, data["transcript_root"]),
    summary_root=_resolve(base, data["summary_root"]),
    provenance_root=_resolve(base, data["provenance_root"]),
    tool_version=data["tool_version"],
    redaction_rules=tuple(
      Rule(label=item["label"], pattern=item["pattern"])
      for item in data.get("redaction_rules", ())
    ),
  )
