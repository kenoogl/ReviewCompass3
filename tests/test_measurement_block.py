"""測定ブロック機械生成toolの固定。転記排除・new-only・fence耐性。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _declaration(tmp_path, entries, title="試験測定"):
  path = tmp_path / "commands.json"
  path.write_text(
    json.dumps({"title": title, "entries": entries}, ensure_ascii=False),
    encoding="utf-8",
  )
  return path


def _python_entry(label, code):
  return {"label": label, "argv": [sys.executable, "-c", code]}


def test_run_fixes_commands_and_outputs(tmp_path, capsys):
  from tools.development import measurement_block

  declaration = _declaration(tmp_path, [
    _python_entry("数える", "print(42)"),
  ])
  output = tmp_path / "block.md"
  exit_code = measurement_block.run((
    "--commands", str(declaration),
    "--output", str(output),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 0
  assert summary["status"] == "ok"
  assert summary["entry_count"] == 1
  assert summary["failed_count"] == 0
  text = output.read_text(encoding="utf-8")
  assert "数える" in text
  assert "42" in text
  assert "機械生成" in text
  assert "-c" in text


def test_run_refuses_existing_output(tmp_path, capsys):
  from tools.development import measurement_block

  declaration = _declaration(tmp_path, [_python_entry("a", "print(1)")])
  output = tmp_path / "block.md"
  output.write_text("既存", encoding="utf-8")
  exit_code = measurement_block.run((
    "--commands", str(declaration),
    "--output", str(output),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 2
  assert summary["status"] == "input_invalid"
  assert output.read_text(encoding="utf-8") == "既存"


def test_run_rejects_broken_declaration(tmp_path, capsys):
  from tools.development import measurement_block

  declaration = tmp_path / "commands.json"
  declaration.write_text("{", encoding="utf-8")
  exit_code = measurement_block.run((
    "--commands", str(declaration),
    "--output", str(tmp_path / "block.md"),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 2
  assert summary["status"] == "input_invalid"
  assert not (tmp_path / "block.md").exists()


def test_nonzero_command_is_data_not_tool_failure(tmp_path, capsys):
  from tools.development import measurement_block

  declaration = _declaration(tmp_path, [
    _python_entry("失敗する", "import sys; sys.exit(3)"),
  ])
  output = tmp_path / "block.md"
  exit_code = measurement_block.run((
    "--commands", str(declaration),
    "--output", str(output),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 0
  assert summary["failed_count"] == 1
  assert "exit：3" in output.read_text(encoding="utf-8")


def test_fence_in_output_does_not_break_structure(tmp_path, capsys):
  from tools.development import measurement_block

  adversarial = "print('```text\\n偽fence\\n```')"
  declaration = _declaration(tmp_path, [
    _python_entry("fence偽装", adversarial),
  ])
  output = tmp_path / "block.md"
  exit_code = measurement_block.run((
    "--commands", str(declaration),
    "--output", str(output),
  ))
  capsys.readouterr()
  assert exit_code == 0
  text = output.read_text(encoding="utf-8")
  assert "````" in text
  assert "```text\n偽fence\n```" in text


def test_oversized_stream_is_truncated_with_marker(tmp_path, capsys):
  from tools.development import measurement_block

  declaration = _declaration(tmp_path, [
    _python_entry("大出力", "print('a' * 200000)"),
  ])
  output = tmp_path / "block.md"
  exit_code = measurement_block.run((
    "--commands", str(declaration),
    "--output", str(output),
  ))
  capsys.readouterr()
  assert exit_code == 0
  text = output.read_text(encoding="utf-8")
  assert "切り詰め" in text
  assert len(text) < 150000


def test_spawn_failure_marks_measurement_incomplete(tmp_path, capsys):
  from tools.development import measurement_block

  declaration = _declaration(tmp_path, [
    {"label": "存在しない", "argv": [str(tmp_path / "no-such-command")]},
  ])
  output = tmp_path / "block.md"
  exit_code = measurement_block.run((
    "--commands", str(declaration),
    "--output", str(output),
  ))
  summary = json.loads(capsys.readouterr().out)
  assert exit_code == 1
  assert summary["status"] == "incomplete"
  assert "spawn_error" in output.read_text(encoding="utf-8")
