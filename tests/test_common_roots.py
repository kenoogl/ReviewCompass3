"""repository root解決の一元化の固定（配置依存3箇所の解消、デプロイ方針4b-1）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_repo_root_returns_repository_root():
  from tools.common import roots

  assert roots.repo_root() == PROJECT_ROOT
  assert (roots.repo_root() / "pyproject.toml").is_file()


def test_parent_traversal_lives_only_in_roots():
  hits = []
  for path in sorted((PROJECT_ROOT / "tools").glob("**/*.py")):
    if "parents[" in path.read_text(encoding="utf-8"):
      hits.append(path.relative_to(PROJECT_ROOT).as_posix())
  assert hits == ["tools/common/roots.py"]


def test_record_run_binds_to_roots():
  from tools.common import roots
  from tools.session_logs import record_run

  assert record_run.PROJECT_ROOT == roots.repo_root()


def test_entry_binds_to_roots():
  from tools.common import roots
  from tools.session_logs import entry

  assert entry.PROJECT_ROOT == roots.repo_root()


def test_trusted_transport_binds_to_roots():
  from tools.common import roots
  from tools.deployment import trusted_claude_transport

  assert trusted_claude_transport._source_root() == roots.repo_root()


def test_entry_resolves_root_from_any_cwd(tmp_path):
  entry_path = PROJECT_ROOT / "tools" / "session_logs" / "entry.py"
  completed = subprocess.run(
    [sys.executable, str(entry_path), "record-run", "--help"],
    cwd=tmp_path,
    capture_output=True,
    text=True,
    timeout=60,
  )
  assert completed.returncode == 0
  assert "usage" in completed.stdout
