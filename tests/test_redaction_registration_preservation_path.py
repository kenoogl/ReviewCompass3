"""伏字化規則の設定登録と保全経路接続のAcceptance Test。

指示書：records/session-handoffs/2026-08-08-codex-to-claude-redaction-registration-preservation-path.md
設計：docs/design/2026-08-07-redaction-rules-design-proposal.md

核心は、承認済みのpattern規則5件とenvironment reference規則3件を宣言値のまま設定へ登録し、
設定→loader→実collectorの経路で実際にマスクが適用され、解決した環境値が設定・伏字化派生物・
Provenance digest入力・診断のどこにも漏れないことである。

実在の秘密、実在の保全データ、hostの実際のhome・user・hostnameは使わない。
`monkeypatch`と`tmp_path`による合成値だけを使う。
"""

import hashlib
import importlib
import json
from pathlib import Path

import pytest

from tools.session_logs import portable_config, redaction
from tools.session_logs.config import ConfigError, load_config
from tools.session_logs.eventual_preservation import (
  CollectionError,
  collect_source,
)


SYNTHETIC_USER = "synthuser"
SYNTHETIC_HOST = "synthetic-host.invalid"
SYNTHETIC_EMAIL = "sample.person@example.invalid"
SYNTHETIC_BEARER = "Bearer abcdefghijklmnopqrstuvwx"
SYNTHETIC_HIGH_ENTROPY = "Xq7Lm2Rt9Wz4Yb1Nc6Vd3KpEf8Gh5Jk"

APPROVED_PATTERN_LABELS = (
  "email",
  "bearer_token",
  "api_key_assignment",
  "private_key_block",
  "aws_access_key_id",
)
APPROVED_ENVIRONMENT_ROLES = (
  "home_directory",
  "user_name",
  "host_name",
)


def _synthetic_environment(
  tmp_path,
  monkeypatch,
  *,
  user=SYNTHETIC_USER,
  host=SYNTHETIC_HOST,
  base="synthetic-home",
):
  home = tmp_path / base / user
  home.mkdir(parents=True, exist_ok=True)
  monkeypatch.setattr(Path, "home", classmethod(lambda _cls: home))
  monkeypatch.setattr("socket.gethostname", lambda: host)
  return home


def _approved_declarations():
  return list(portable_config.default_redaction_rule_declarations())


def _expected_declarations():
  pattern_items = [
    {"label": rule.label, "pattern": rule.pattern}
    for rule in redaction.default_pattern_rules()
  ]
  environment_items = [
    {"label": rule.label, "environment_role": rule.environment_role}
    for rule in redaction.environment_reference_rules()
  ]
  return pattern_items + environment_items


def _write_config(tmp_path, rules):
  config_path = tmp_path / "config" / "session-logs.json"
  config_path.parent.mkdir(parents=True, exist_ok=True)
  payload = {
    "raw_root": str(tmp_path / "private" / "raw"),
    "transcript_root": str(tmp_path / "private" / "transcripts"),
    "summary_root": str(tmp_path / "repository" / "summaries"),
    "provenance_root": str(tmp_path / "repository" / "provenance"),
    "preservation_enabled": True,
    "tool_version": "test-v1",
    "redaction_rules": rules,
    "allow_patterns": [],
  }
  config_path.write_text(
    json.dumps(payload, ensure_ascii=False),
    encoding="utf-8",
  )
  return config_path


def _repository(tmp_path):
  repository = tmp_path / "repository"
  (repository / ".git").mkdir(parents=True, exist_ok=True)
  return repository


def _write_session(source_root, text):
  raw_log = source_root / "session.jsonl"
  raw_log.parent.mkdir(parents=True, exist_ok=True)
  records = (
    {
      "uuid": "user-1",
      "type": "user",
      "sessionId": "session-1",
      "message": {"role": "user", "content": text},
    },
    {
      "uuid": "assistant-1",
      "type": "assistant",
      "sessionId": "session-1",
      "message": {
        "role": "assistant",
        "content": [{"type": "text", "text": "了解しました。"}],
      },
    },
  )
  raw_log.write_bytes(b"".join(
    (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    for record in records
  ))
  return raw_log


def _collect_with_config(tmp_path, config, raw_log, *, run_id="run-1"):
  return collect_source(
    raw_log,
    source_root=tmp_path / "native",
    private_root=tmp_path / "private-collect",
    repository_root=_repository(tmp_path),
    tool_version=config.tool_version,
    run_id=run_id,
    observed_at="2026-08-08T10:00:00+09:00",
    redaction_rules=config.redaction_rules,
    environment_redaction_rules=config.environment_redaction_rules,
    allow_patterns=config.allow_patterns,
  )


def test_normal_new_config_registers_the_eight_approved_declarations(
  tmp_path,
  monkeypatch,
):
  """通常の新規設定生成が8宣言を宣言値のまま登録し、解決値を書かない。"""

  home = _synthetic_environment(tmp_path, monkeypatch)
  deployment_paths = importlib.import_module(
    "tools.session_logs.deployment_paths"
  )

  class FakePlatformDirs:
    user_config_path = tmp_path / "standard" / "config"
    user_data_path = tmp_path / "standard" / "data"
    user_state_path = tmp_path / "standard" / "state"
    user_log_path = tmp_path / "standard" / "log"
    user_cache_path = tmp_path / "standard" / "cache"

  monkeypatch.setattr(
    deployment_paths,
    "_default_platform_dirs_factory",
    lambda **_arguments: FakePlatformDirs(),
  )
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "init-config",
    "--raw-root",
    str(raw_root),
    "--tool-version",
    "test-v1",
  )) == 0

  config_file = tmp_path / "standard" / "config" / "session-logs.json"
  written = config_file.read_text(encoding="utf-8")
  payload = json.loads(written)
  assert payload["redaction_rules"] == _expected_declarations()
  assert str(home) not in written
  assert SYNTHETIC_USER not in written
  assert SYNTHETIC_HOST not in written

  loaded = load_config(config_file)
  assert tuple(
    rule.label for rule in loaded.redaction_rules
  ) == APPROVED_PATTERN_LABELS
  assert tuple(
    rule.environment_role for rule in loaded.environment_redaction_rules
  ) == APPROVED_ENVIRONMENT_ROLES


def test_loader_separates_pattern_and_environment_declarations(tmp_path):
  """loaderはpattern宣言をRule、environment宣言をEnvironmentRuleとして区別する。"""

  config_path = _write_config(tmp_path, _expected_declarations())

  config = load_config(config_path)

  assert len(config.redaction_rules) == 5
  assert all(
    isinstance(rule, redaction.Rule)
    for rule in config.redaction_rules
  )
  assert tuple(
    rule.label for rule in config.redaction_rules
  ) == APPROVED_PATTERN_LABELS
  assert len(config.environment_redaction_rules) == 3
  assert all(
    isinstance(rule, redaction.EnvironmentRule)
    for rule in config.environment_redaction_rules
  )
  assert tuple(
    rule.environment_role for rule in config.environment_redaction_rules
  ) == APPROVED_ENVIRONMENT_ROLES


def test_loader_keeps_pattern_only_configs_working(tmp_path):
  """既存のpattern-only設定と明示的な空listの意味を壊さない。"""

  pattern_only = _write_config(
    tmp_path / "pattern-only",
    [{"label": "secret", "pattern": "SECRET-[0-9]+"}],
  )
  empty = _write_config(tmp_path / "empty", [])

  pattern_config = load_config(pattern_only)
  empty_config = load_config(empty)

  assert pattern_config.redaction_rules == (
    redaction.Rule(label="secret", pattern="SECRET-[0-9]+"),
  )
  assert pattern_config.environment_redaction_rules == ()
  assert empty_config.redaction_rules == ()
  assert empty_config.environment_redaction_rules == ()


@pytest.mark.parametrize("declaration", (
  {
    "label": "mixed",
    "pattern": "MIXED-VALUE-[0-9]+",
    "environment_role": "home_directory",
  },
  {"label": "empty-declaration"},
  {"label": "unknown", "environment_role": "totally-bogus-role"},
))
def test_loader_fails_closed_on_invalid_declarations(tmp_path, declaration):
  """両方持つ・どちらも持たない・未知roleはConfigErrorで拒否し、値を例外文へ出さない。"""

  config_path = _write_config(tmp_path, [declaration])

  with pytest.raises(ConfigError) as error:
    load_config(config_path)

  message = str(error.value)
  assert "MIXED-VALUE" not in message
  assert "totally-bogus-role" not in message


def test_config_to_collector_path_masks_environment_and_pattern_values(
  tmp_path,
  monkeypatch,
):
  """設定→loader→実collectorの経路で、合成環境値とpattern対象が伏字化される。"""

  home = _synthetic_environment(tmp_path, monkeypatch)
  config = load_config(_write_config(tmp_path, _expected_declarations()))
  text = (
    "設定は %s/.reviewcompass3/config.json にある。"
    "利用者 %s が %s から接続し、連絡先は %s、"
    "認可は %s である。"
  ) % (home, SYNTHETIC_USER, SYNTHETIC_HOST, SYNTHETIC_EMAIL, SYNTHETIC_BEARER)
  raw_log = _write_session(tmp_path / "native", text)

  created = _collect_with_config(tmp_path, config, raw_log)
  repeated = _collect_with_config(
    tmp_path,
    config,
    raw_log,
    run_id="run-2",
  )

  assert created.action == "created"
  assert created.state == "reconciled"
  verbatim_text = created.verbatim_path.read_text(encoding="utf-8")
  assert str(home) in verbatim_text
  redacted_text = created.redacted_path.read_text(encoding="utf-8")
  for value in (
    str(home),
    SYNTHETIC_USER,
    SYNTHETIC_HOST,
    SYNTHETIC_EMAIL,
    "abcdefghijklmnopqrstuvwx",
  ):
    assert value not in redacted_text
  for label in (
    "home_directory",
    "user_name",
    "host_name",
    "email",
    "bearer_token",
  ):
    assert "[REDACTED:%s]" % label in redacted_text

  provenance = json.loads(
    created.provenance_path.read_text(encoding="utf-8")
  )
  assert provenance["artifacts"]["redacted_sha256"] == hashlib.sha256(
    created.redacted_path.read_bytes()
  ).hexdigest()
  assert provenance["artifacts"]["verbatim_sha256"] == hashlib.sha256(
    created.verbatim_path.read_bytes()
  ).hexdigest()
  digest = provenance["redaction_rules_sha256"]
  assert isinstance(digest, str) and len(digest) == 64
  provenance_text = created.provenance_path.read_text(encoding="utf-8")
  assert str(home) not in provenance_text
  assert SYNTHETIC_USER not in provenance_text
  assert SYNTHETIC_HOST not in provenance_text

  assert repeated.action == "unchanged"
  assert repeated.redacted_path.read_bytes() == (
    created.redacted_path.read_bytes()
  )
  repeated_provenance = json.loads(
    repeated.provenance_path.read_text(encoding="utf-8")
  )
  assert repeated_provenance["redaction_rules_sha256"] == digest


def test_rules_digest_is_stable_across_different_environments(
  tmp_path,
  monkeypatch,
):
  """規則digestは宣言から決定的に算出され、解決した環境値に依存しない。"""

  digests = []
  for index, (user, host) in enumerate((
    (SYNTHETIC_USER, SYNTHETIC_HOST),
    ("otheruser", "other-host.invalid"),
  )):
    work = tmp_path / ("environment-%d" % index)
    work.mkdir()
    _synthetic_environment(
      work,
      monkeypatch,
      user=user,
      host=host,
      base="synthetic-home-%d" % index,
    )
    config = load_config(_write_config(work, _expected_declarations()))
    raw_log = _write_session(
      work / "native",
      "利用者 %s の連絡先は %s である。" % (user, SYNTHETIC_EMAIL),
    )
    result = _collect_with_config(work, config, raw_log)
    provenance = json.loads(
      result.provenance_path.read_text(encoding="utf-8")
    )
    digests.append(provenance["redaction_rules_sha256"])

  assert digests[0] == digests[1]


def test_unmatched_high_entropy_value_fails_closed_without_leaking(
  tmp_path,
  monkeypatch,
):
  """patternで消えない高entropy合成値はfail-closedになり、値がどこにも出ない。"""

  _synthetic_environment(tmp_path, monkeypatch)
  config = load_config(_write_config(tmp_path, _expected_declarations()))
  raw_log = _write_session(
    tmp_path / "native",
    "残存候補の値 %s を含む。" % SYNTHETIC_HIGH_ENTROPY,
  )
  private_root = tmp_path / "private-collect"

  with pytest.raises(CollectionError) as error:
    _collect_with_config(tmp_path, config, raw_log)

  chained = error.value
  while chained is not None:
    assert SYNTHETIC_HIGH_ENTROPY not in str(chained)
    chained = chained.__cause__
  assert tuple((private_root / "raw").rglob("*.jsonl"))
  assert tuple((private_root / "redacted").rglob("*.md")) == ()
  assert tuple((private_root / "provenance").rglob("*.json")) == ()
  assert tuple((private_root / "cursors").rglob("*.json")) == ()
