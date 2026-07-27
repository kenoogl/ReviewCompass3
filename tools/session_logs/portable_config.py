"""OS標準配置からポータブル設定を生成する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import json
import os
from pathlib import Path


class PortableConfigError(Exception):
  """安全なポータブル設定を生成できない。"""


@dataclasses.dataclass(frozen=True)
class PortableConfig:
  config_file: Path
  payload: dict

  def render(self) -> str:
    return json.dumps(
      self.payload,
      ensure_ascii=False,
      indent=2,
      sort_keys=True,
    ) + "\n"


_ROOT_ENVIRONMENT = {
  "config_file": "REVIEWCOMPASS3_CONFIG_FILE",
  "data_root": "REVIEWCOMPASS3_DATA_ROOT",
  "state_root": "REVIEWCOMPASS3_STATE_ROOT",
  "log_root": "REVIEWCOMPASS3_LOG_ROOT",
}


def _select_path(name, default, *, environment, overrides):
  value = overrides.get(name)
  if value is None:
    value = environment.get(_ROOT_ENVIRONMENT[name], default)
  path = Path(value)
  if not path.is_absolute():
    raise PortableConfigError(
      "Portable config paths must be absolute"
    )
  return path


def build_portable_config(
  raw_root,
  *,
  deployment_paths,
  tool_version,
  environment=None,
  overrides=None,
  redaction_rules=(),
  allow_patterns=(),
) -> PortableConfig:
  environment_values = (
    os.environ
    if environment is None
    else environment
  )
  override_values = {} if overrides is None else dict(overrides)
  unknown_overrides = (
    set(override_values)
    - set(_ROOT_ENVIRONMENT)
  )
  if unknown_overrides:
    raise PortableConfigError(
      "Unknown portable config override"
    )
  raw_path = Path(raw_root)
  if not raw_path.is_absolute():
    raise PortableConfigError(
      "Portable config paths must be absolute"
    )
  config_file = _select_path(
    "config_file",
    deployment_paths.config_file,
    environment=environment_values,
    overrides=override_values,
  )
  data_root = _select_path(
    "data_root",
    deployment_paths.data_root,
    environment=environment_values,
    overrides=override_values,
  )
  state_root = _select_path(
    "state_root",
    deployment_paths.state_root,
    environment=environment_values,
    overrides=override_values,
  )
  log_root = _select_path(
    "log_root",
    deployment_paths.log_root,
    environment=environment_values,
    overrides=override_values,
  )
  payload = {
    "allow_patterns": list(allow_patterns),
    "backup_root": str(data_root / "backups"),
    "deployment": {
      "owner": "reviewcompass3",
      "schema_version": 1,
    },
    "hook_event_log_path": str(log_root / "hooks.jsonl"),
    "preservation_enabled": True,
    "preservation_ledger_path": str(
      state_root / "preservation-ledger.json"
    ),
    "provenance_root": str(data_root / "provenance"),
    "raw_root": str(raw_path),
    "redaction_rules": list(redaction_rules),
    "sensitive_report_root": str(
      state_root / "sensitive-reports"
    ),
    "summary_root": str(data_root / "summaries"),
    "tool_version": tool_version,
    "transcript_root": str(data_root / "transcripts"),
  }
  return PortableConfig(
    config_file=config_file,
    payload=payload,
  )
