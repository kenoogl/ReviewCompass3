"""Claude Codeフック導入処理の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json


def test_installs_idempotently_and_uninstalls_only_owned_hooks(tmp_path):
  settings_path = tmp_path / ".claude" / "settings.local.json"
  settings_path.parent.mkdir()
  existing = {
    "permissions": {"allow": ["Read"]},
    "hooks": {
      "PostToolUse": [
        {
          "matcher": "Edit",
          "hooks": [
            {
              "type": "command",
              "command": "existing-check",
            },
          ],
        },
      ],
    },
  }
  settings_path.write_text(json.dumps(existing), encoding="utf-8")
  installation = importlib.import_module(
    "tools.session_logs.hook_installation"
  )

  installed = installation.install_claude_hooks(
    settings_path,
    start_command="reviewcompass-session start",
    end_command="reviewcompass-session end",
  )
  repeated = installation.install_claude_hooks(
    settings_path,
    start_command="reviewcompass-session start",
    end_command="reviewcompass-session end",
  )

  assert installed.action == "installed"
  assert repeated.action == "unchanged"
  configured = json.loads(settings_path.read_text(encoding="utf-8"))
  assert configured["permissions"] == existing["permissions"]
  assert configured["hooks"]["PostToolUse"] == (
    existing["hooks"]["PostToolUse"]
  )
  assert configured["hooks"]["SessionStart"] == [
    {
      "matcher": "startup|resume",
      "hooks": [
        {
          "type": "command",
          "command": "reviewcompass-session start",
        },
      ],
    },
  ]
  assert configured["hooks"]["SessionEnd"] == [
    {
      "hooks": [
        {
          "type": "command",
          "command": "reviewcompass-session end",
        },
      ],
    },
  ]

  removed = installation.uninstall_claude_hooks(
    settings_path,
    start_command="reviewcompass-session start",
    end_command="reviewcompass-session end",
  )

  assert removed.action == "uninstalled"
  restored = json.loads(settings_path.read_text(encoding="utf-8"))
  assert restored == existing


def test_install_creates_missing_settings_without_touching_other_files(
  tmp_path,
):
  settings_path = tmp_path / ".claude" / "settings.local.json"
  unrelated = tmp_path / ".claude" / "settings.json"
  unrelated.parent.mkdir()
  unrelated.write_text('{"keep": true}\n', encoding="utf-8")
  installation = importlib.import_module(
    "tools.session_logs.hook_installation"
  )

  result = installation.install_claude_hooks(
    settings_path,
    start_command="start-command",
    end_command="end-command",
  )

  assert result.action == "installed"
  assert settings_path.is_file()
  assert unrelated.read_text(encoding="utf-8") == '{"keep": true}\n'
