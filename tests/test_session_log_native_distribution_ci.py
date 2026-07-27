"""3 OSネイティブ配布CIの暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

from pathlib import Path


REPOSITORY_ROOT = Path(__file__).parents[1]
WORKFLOW_PATH = (
  REPOSITORY_ROOT
  / ".github"
  / "workflows"
  / "native-deployment-validation.yml"
)


def test_native_ci_installs_package_and_records_value_free_evidence():
  workflow = WORKFLOW_PATH.read_text(encoding="utf-8")

  assert "ubuntu-latest" in workflow
  assert "macos-latest" in workflow
  assert "windows-latest" in workflow
  assert '"3.9"' in workflow
  assert "python -m pip install ." in workflow
  assert (
    "reviewcompass3-session-logs validate-native "
    "--check package"
  ) in workflow
  assert "actions/upload-artifact@" in workflow
  assert "native-package-${{ runner.os }}-" in workflow
