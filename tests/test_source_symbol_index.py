"""Work 4A Source Symbol IndexのAcceptance Test。"""

import dataclasses
import importlib
from pathlib import Path
import subprocess

import pytest


def _module():
    return importlib.import_module("tools.development.source_symbol_index")


def _git(project_root, *arguments):
    result = subprocess.run(
        ["git", *arguments],
        cwd=project_root,
        capture_output=True,
        check=False,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def _repository(tmp_path, files):
    project_root = tmp_path / "project"
    project_root.mkdir()
    for relative_path, content in files.items():
        path = project_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    _git(project_root, "init", "-q")
    _git(project_root, "config", "user.email", "test@example.invalid")
    _git(project_root, "config", "user.name", "Source Index Test")
    _git(project_root, "add", ".")
    _git(project_root, "commit", "-qm", "fixture")
    return project_root


def _universe(module):
    return module.SourceUniverse(
        primary_roots=("tools",),
        test_reference_roots=("tests",),
    )


def test_captures_clean_source_snapshot_deterministically(tmp_path):
    module = _module()
    project_root = _repository(
        tmp_path,
        {
            "tools/alpha.py": "def alpha(value):\n    return value\n",
            "tools/beta.py": "async def beta():\n    return None\n",
            "tests/test_alpha.py": "def test_alpha():\n    assert True\n",
        },
    )

    first = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )
    second = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )

    assert first.snapshot_id == second.snapshot_id
    assert [item.path for item in first.primary_files] == [
        "tools/alpha.py",
        "tools/beta.py",
    ]
    assert [item.path for item in first.test_reference_files] == [
        "tests/test_alpha.py",
    ]
    assert all(len(item.content_sha256) == 64 for item in first.primary_files)


def test_keeps_source_content_identity_when_only_non_source_commit_changes(
    tmp_path,
):
    module = _module()
    project_root = _repository(
        tmp_path,
        {
            "tools/alpha.py": "def alpha():\n    return 1\n",
            "tests/test_alpha.py": "def test_alpha():\n    assert True\n",
            "notes.md": "first\n",
        },
    )
    first = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )
    (project_root / "notes.md").write_text("second\n", encoding="utf-8")
    _git(project_root, "add", "notes.md")
    _git(project_root, "commit", "-qm", "non-source change")
    second = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )

    assert first.head != second.head
    assert first.snapshot_id != second.snapshot_id
    assert first.source_content_id == second.source_content_id


def test_rejects_dirty_or_untracked_source_before_snapshot_capture(tmp_path):
    module = _module()
    project_root = _repository(
        tmp_path,
        {"tools/alpha.py": "def alpha():\n    return 1\n"},
    )
    (project_root / "tools/untracked.py").write_text(
        "def untracked():\n    return 2\n",
        encoding="utf-8",
    )

    with pytest.raises(
        module.SourceSnapshotError,
        match="source_snapshot_dirty",
    ):
        module.capture_source_snapshot(
            project_root=project_root,
            universe=_universe(module),
        )


def test_excludes_ignored_paths_and_rejects_missing_file_digest(tmp_path):
    module = _module()
    project_root = _repository(
        tmp_path,
        {
            ".gitignore": ".venv/\n",
            "tools/alpha.py": "def alpha():\n    return 1\n",
            "tests/test_alpha.py": "def test_alpha():\n    assert True\n",
        },
    )
    ignored = project_root / ".venv/lib/python3.9/site-packages/ignored.py"
    ignored.parent.mkdir(parents=True)
    ignored.write_text("def ignored():\n    return None\n", encoding="utf-8")

    snapshot = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )
    assert "ignored.py" not in {
        item.path
        for item in (*snapshot.primary_files, *snapshot.test_reference_files)
    }
    missing_digest = dataclasses.replace(
        snapshot.primary_files[0],
        content_sha256="",
    )
    invalid_snapshot = dataclasses.replace(
        snapshot,
        primary_files=(missing_digest,),
    )

    with pytest.raises(
        module.SourceSnapshotError,
        match="source_snapshot_file_digest_missing",
    ):
        module.validate_source_snapshot(
            snapshot=invalid_snapshot,
            project_root=project_root,
        )


def test_indexes_all_function_and_method_symbols_with_unique_identity(tmp_path):
    module = _module()
    project_root = _repository(
        tmp_path,
        {
            "tools/alpha.py": (
                "def duplicate(value: int, enabled=True):\n"
                "    return value\n\n"
                "class Box:\n"
                "    def method(self, flag=False):\n"
                "        return flag\n\n"
                "async def run(value):\n"
                "    return value\n\n"
                "def outer():\n"
                "    def inner():\n"
                "        return None\n"
                "    return inner\n"
            ),
            "tools/beta.py": "def duplicate(value):\n    return value\n",
            "tests/test_alpha.py": "def test_placeholder():\n    assert True\n",
        },
    )

    snapshot = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )
    index = module.generate_source_symbol_index(snapshot=snapshot)
    entries = {entry.symbol_id: entry for entry in index.entries}

    assert index.snapshot_id == snapshot.snapshot_id
    assert set(entries) == {
        "py:tools/alpha.py:tools.alpha.duplicate:function",
        "py:tools/alpha.py:tools.alpha.Box.method:method",
        "py:tools/alpha.py:tools.alpha.run:async_function",
        "py:tools/alpha.py:tools.alpha.outer:function",
        "py:tools/alpha.py:tools.alpha.outer.inner:function",
        "py:tools/beta.py:tools.beta.duplicate:function",
    }
    assert entries[
        "py:tools/alpha.py:tools.alpha.duplicate:function"
    ].signature == "(value: int, enabled=True)"
    assert all(len(entry.content_sha256) == 64 for entry in entries.values())


def test_detects_content_change_without_reusing_snapshot_identity(tmp_path):
    module = _module()
    project_root = _repository(
        tmp_path,
        {"tools/alpha.py": "def alpha():\n    return 1\n"},
    )
    first_snapshot = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )
    first_index = module.generate_source_symbol_index(snapshot=first_snapshot)
    source = project_root / "tools/alpha.py"
    source.write_text("def alpha():\n    return 2\n", encoding="utf-8")
    _git(project_root, "add", "tools/alpha.py")
    _git(project_root, "commit", "-qm", "change alpha")

    second_snapshot = module.capture_source_snapshot(
        project_root=project_root,
        universe=_universe(module),
    )
    second_index = module.generate_source_symbol_index(snapshot=second_snapshot)
    first_entry = first_index.entries[0]
    second_entry = second_index.entries[0]

    assert first_snapshot.snapshot_id != second_snapshot.snapshot_id
    assert first_entry.symbol_id == second_entry.symbol_id
    assert first_entry.content_sha256 != second_entry.content_sha256
