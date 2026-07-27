"""クロスプラットフォーム配布検証の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]


def test_distribution_validation_installs_and_checks_three_profiles(
  tmp_path,
  capsys,
):
  raw_root = tmp_path / "raw"
  raw_root.mkdir()
  work_root = tmp_path / "distribution-validation"
  entry = importlib.import_module("tools.session_logs.entry")

  assert entry.run((
    "validate-distribution",
    "--project-root",
    str(REPOSITORY_ROOT),
    "--work-root",
    str(work_root),
    "--raw-root",
    str(raw_root),
  )) == 0

  output = capsys.readouterr().out
  assert json.loads(output) == {
    "backend_count": 3,
    "importable": True,
    "installed": True,
    "profile_count": 3,
    "status": "passed",
  }
  assert str(REPOSITORY_ROOT) not in output
  assert (
    work_root
    / "installed"
    / "tools"
    / "session_logs"
    / "entry.py"
  ).is_file()
  assert not (work_root / "darwin" / "schedule.plist").exists()
  assert not (work_root / "linux" / "schedule.timer").exists()
  assert not (work_root / "win32" / "schedule.xml").exists()
