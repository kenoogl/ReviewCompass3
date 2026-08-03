"""ClaudeとCodex 2形式を一つの入口から解析するadapter。"""

import dataclasses

from tools.session_logs import (
  parse_claude,
  parse_codex,
  parse_codex_rollout,
)
from tools.session_logs.source_kind import (
  identify_source_kind,
  identify_source_kind_bytes,
)


class UnsupportedSourceKind(Exception):
  """実装していない、または識別できない入力形式。"""


@dataclasses.dataclass(frozen=True)
class ParsedSource:
  source_kind: str
  parsed: object


_LOG_PARSERS = {
  "claude": parse_claude.parse_claude_log,
  "codex_exec_json": parse_codex.parse_codex_log,
  "codex_rollout": parse_codex_rollout.parse_codex_rollout_log,
}
_BYTE_PARSERS = {
  "claude": parse_claude.parse_claude_bytes,
  "codex_exec_json": parse_codex.parse_codex_bytes,
  "codex_rollout": parse_codex_rollout.parse_codex_rollout_bytes,
}


def _parse(source_kind, value, parsers):
  try:
    parser = parsers[source_kind]
  except KeyError as error:
    raise UnsupportedSourceKind(str(source_kind)) from error
  return ParsedSource(
    source_kind=source_kind,
    parsed=parser(value),
  )


def parse_source_log(path) -> ParsedSource:
  return _parse(
    identify_source_kind(path),
    path,
    _LOG_PARSERS,
  )


def parse_source_bytes(data) -> ParsedSource:
  return _parse(
    identify_source_kind_bytes(data),
    data,
    _BYTE_PARSERS,
  )
