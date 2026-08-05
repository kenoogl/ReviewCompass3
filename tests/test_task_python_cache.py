"""task専用Python cache rootの受入Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-implement-task-python-cache-slice.md
承認：DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001

配置・所有・保持は新しく決めない。Human承認済みのLayout v3をそのまま使う。
外部rootは`<runtime_root>/projects/<project_id>/development/cache/`である。

Testは一時directoryだけを使い、実際のホーム配下（`~/.reviewcompass3`）を作らない。
"""

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
BASELINE_RECORD = (
    "records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json"
)
PROJECT_ID = "project-alpha"
TASK_ID = "task-python-cache-slice"


@pytest.fixture
def cache_module():
    return importlib.import_module("tools.development.task_python_cache")


@pytest.fixture
def layout_module():
    return importlib.import_module("tools.layout.baseline")


def _fake_project(tmp_path, *, project_id=PROJECT_ID):
    """一時directoryだけで完結するprojectを作る。実projectへは書かない。"""

    project = tmp_path / "checkout"
    (project / ".reviewcompass").mkdir(parents=True)
    (project / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(
            {
                "artifact_roots": {"workflow": ".reviewcompass/workflow"},
                "document_links": [],
                "project_id": project_id,
                "schema_version": 2,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    target = project / BASELINE_RECORD
    target.parent.mkdir(parents=True)
    target.write_bytes((PROJECT_ROOT / BASELINE_RECORD).read_bytes())
    return project


def _expected(runtime_root, *, project_id=PROJECT_ID, task_id=TASK_ID):
    return (
        Path(runtime_root)
        / "projects"
        / project_id
        / "development"
        / "cache"
        / "python-bytecode"
        / task_id
    )


def _resolve(cache_module, tmp_path, **overrides):
    project = overrides.pop("project_root", None) or _fake_project(tmp_path)
    runtime_root = overrides.pop("runtime_root", None) or (
        tmp_path / "runtime" / ".reviewcompass3"
    )
    arguments = {
        "project_root": project,
        "runtime_root": runtime_root,
        "task_id": TASK_ID,
    }
    arguments.update(overrides)
    return cache_module.resolve_task_cache(**arguments)


# ------------------------------------------------------------ 1. 副作用なしの解決


def test_resolution_is_deterministic_and_writes_nothing(cache_module, tmp_path):
    project = _fake_project(tmp_path)
    runtime_root = tmp_path / "runtime" / ".reviewcompass3"

    first = _resolve(cache_module, tmp_path, project_root=project,
                     runtime_root=runtime_root)
    second = _resolve(cache_module, tmp_path, project_root=project,
                      runtime_root=runtime_root)

    assert first.project_id == PROJECT_ID
    assert first.profile == "development"
    assert first.task_directory == _expected(runtime_root)
    assert first.task_directory == second.task_directory
    assert first.cache_root == runtime_root / "projects" / PROJECT_ID / (
        "development"
    ) / "cache"
    assert first.task_directory.is_relative_to(first.cache_root) if hasattr(
        Path, "is_relative_to"
    ) else str(first.task_directory).startswith(str(first.cache_root))
    assert not runtime_root.exists(), "解決だけではdirectoryを作らない"


def test_project_identity_comes_from_the_manifest(cache_module, tmp_path):
    import inspect

    signature = inspect.signature(cache_module.resolve_task_cache)
    assert "project_id" not in signature.parameters, (
        "callerが任意のproject IDを渡して別projectのcacheへ書けないようにする"
    )

    project = _fake_project(tmp_path, project_id="project-beta")
    resolution = _resolve(cache_module, tmp_path, project_root=project)

    assert resolution.project_id == "project-beta"
    assert "project-beta" in resolution.task_directory.parts


# --------------------------------------------------------- 2. 明示初期化だけが作る


def test_initialization_creates_only_the_cache_and_task_directory(
    cache_module, tmp_path
):
    runtime_root = tmp_path / "runtime" / ".reviewcompass3"
    resolution = _resolve(cache_module, tmp_path, runtime_root=runtime_root)

    created = cache_module.initialize_task_cache(resolution)

    assert created == resolution.task_directory
    assert resolution.cache_root.is_dir()
    assert resolution.task_directory.is_dir()
    profile_root = runtime_root / "projects" / PROJECT_ID / "development"
    for kind in ("data", "state", "logs", "evaluation", "sensitive"):
        assert not (profile_root / kind).exists(), f"{kind} rootは作らない"
    assert not (runtime_root / "config").exists(), "config rootは作らない"


def test_initialization_is_repeatable(cache_module, tmp_path):
    resolution = _resolve(cache_module, tmp_path)

    first = cache_module.initialize_task_cache(resolution)
    (first / "marker").write_text("keep", encoding="utf-8")
    second = cache_module.initialize_task_cache(resolution)

    assert first == second
    assert (second / "marker").read_text(encoding="utf-8") == "keep"


# ------------------------------------------------------------------ 3. 環境値生成


def test_environment_mapping_holds_only_the_bytecode_prefix(cache_module, tmp_path):
    resolution = _resolve(cache_module, tmp_path)

    environment = cache_module.bytecode_environment(resolution)

    assert set(environment) == {"PYTHONPYCACHEPREFIX"}
    value = environment["PYTHONPYCACHEPREFIX"]
    assert value == str(resolution.task_directory)
    assert Path(value).is_absolute()


def test_environment_mapping_does_not_change_the_running_process(
    cache_module, tmp_path
):
    before = dict(os.environ)
    resolution = _resolve(cache_module, tmp_path)

    cache_module.bytecode_environment(resolution)

    assert "PYTHONPYCACHEPREFIX" not in os.environ
    assert dict(os.environ) == before


# ------------------------------------------------------------------ 4. 安全境界


def _blocked_initializer(monkeypatch, layout_module):
    """Layout v3の初期化が一度も呼ばれないことを固定する。"""

    calls = []

    def refuse(*arguments, **keywords):
        calls.append((arguments, keywords))
        raise AssertionError("初期化操作を呼んではならない")

    monkeypatch.setattr(
        layout_module, "initialize_project_runtime_layout", refuse
    )
    return calls


@pytest.mark.parametrize(
    "task_id",
    ["", ".", "..", "../escape", "a/b", "a\\b", ".hidden", "task id"],
)
def test_unsafe_task_identifier_is_rejected(
    cache_module, layout_module, monkeypatch, tmp_path, task_id
):
    calls = _blocked_initializer(monkeypatch, layout_module)

    with pytest.raises(cache_module.TaskPythonCacheError) as error:
        _resolve(cache_module, tmp_path, task_id=task_id)

    assert error.value.code in cache_module.STOP_CODES
    assert calls == []


@pytest.mark.parametrize("profile", ["", "runtime ", "../development", "staging"])
def test_unsafe_profile_is_rejected(
    cache_module, layout_module, monkeypatch, tmp_path, profile
):
    calls = _blocked_initializer(monkeypatch, layout_module)

    with pytest.raises(cache_module.TaskPythonCacheError):
        _resolve(cache_module, tmp_path, profile=profile)

    assert calls == []


def test_relative_runtime_root_is_rejected(
    cache_module, layout_module, monkeypatch, tmp_path
):
    calls = _blocked_initializer(monkeypatch, layout_module)

    with pytest.raises(cache_module.TaskPythonCacheError):
        _resolve(cache_module, tmp_path, runtime_root=Path("relative/.reviewcompass3"))

    assert calls == []


def test_runtime_root_inside_the_project_is_rejected(
    cache_module, layout_module, monkeypatch, tmp_path
):
    calls = _blocked_initializer(monkeypatch, layout_module)
    project = _fake_project(tmp_path)

    with pytest.raises(cache_module.TaskPythonCacheError) as error:
        _resolve(
            cache_module, tmp_path,
            project_root=project,
            runtime_root=project / ".reviewcompass3",
        )

    assert error.value.code in cache_module.STOP_CODES
    assert calls == []


def test_symlinked_cache_target_is_rejected(
    cache_module, layout_module, monkeypatch, tmp_path
):
    runtime_root = tmp_path / "runtime" / ".reviewcompass3"
    resolution = _resolve(cache_module, tmp_path, runtime_root=runtime_root)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    resolution.cache_root.parent.mkdir(parents=True)
    resolution.cache_root.symlink_to(elsewhere, target_is_directory=True)
    calls = _blocked_initializer(monkeypatch, layout_module)

    with pytest.raises(cache_module.TaskPythonCacheError) as error:
        cache_module.initialize_task_cache(resolution)

    assert error.value.code in cache_module.STOP_CODES
    assert calls == []
    assert not (elsewhere / "python-bytecode").exists()


def test_regular_file_in_the_cache_path_is_rejected(
    cache_module, layout_module, monkeypatch, tmp_path
):
    runtime_root = tmp_path / "runtime" / ".reviewcompass3"
    resolution = _resolve(cache_module, tmp_path, runtime_root=runtime_root)
    resolution.bytecode_root.parent.mkdir(parents=True)
    resolution.bytecode_root.write_text("not a directory", encoding="utf-8")
    calls = _blocked_initializer(monkeypatch, layout_module)

    with pytest.raises(cache_module.TaskPythonCacheError) as error:
        cache_module.initialize_task_cache(resolution)

    assert error.value.code in cache_module.STOP_CODES
    assert calls == []
    assert resolution.bytecode_root.is_file()


def test_missing_project_manifest_is_rejected(
    cache_module, layout_module, monkeypatch, tmp_path
):
    calls = _blocked_initializer(monkeypatch, layout_module)
    empty = tmp_path / "empty"
    empty.mkdir()

    with pytest.raises(cache_module.TaskPythonCacheError):
        _resolve(cache_module, tmp_path, project_root=empty)

    assert calls == []


# ------------------------------------------------------------------ 5. 保持境界


def test_module_has_no_deletion_or_retention_or_global_environment_change(
    cache_module,
):
    source = Path(cache_module.__file__).read_text(encoding="utf-8")

    for forbidden in (
        "shutil",
        "rmtree",
        "unlink",
        "os.remove",
        "os.rmdir",
        "os.environ",
        "putenv",
        "policy_test_runner",
        "structured_argv_executor",
        "subprocess",
        "time.time",
        "datetime",
    ):
        assert forbidden not in source, f"{forbidden} はこのmoduleに存在しない"

    for absent in ("cleanup", "purge", "evict", "expire"):
        assert not hasattr(cache_module, absent), f"{absent} はこのmoduleに存在しない"


def test_module_reuses_the_approved_layout_resolver(cache_module):
    source = Path(cache_module.__file__).read_text(encoding="utf-8")

    assert "resolve_project_runtime_layout" in source
    assert "initialize_project_runtime_layout" in source
    assert cache_module.LAYOUT_BASELINE_RECORD == BASELINE_RECORD
    assert cache_module.CACHE_PROFILE == "development"


# ---------------------------------------------------- 6. 実際のbytecode出力の隔離


def test_child_process_writes_bytecode_only_under_the_task_directory(
    cache_module, tmp_path
):
    project = _fake_project(tmp_path)
    runtime_root = tmp_path / "runtime" / ".reviewcompass3"
    resolution = _resolve(
        cache_module, tmp_path, project_root=project, runtime_root=runtime_root
    )
    cache_module.initialize_task_cache(resolution)

    module_path = project / "sample_module.py"
    module_path.write_text("VALUE = 1\n", encoding="utf-8")

    child_environment = dict(os.environ)
    child_environment.update(cache_module.bytecode_environment(resolution))
    completed = subprocess.run(
        [sys.executable, "-c", "import sample_module; print(sample_module.VALUE)"],
        cwd=str(project),
        env=child_environment,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "1"
    assert list(project.rglob("__pycache__")) == [], "project内にcacheを作らない"
    written = [
        path for path in resolution.task_directory.rglob("*.pyc") if path.is_file()
    ]
    assert written, "task directory配下にcache fileが作られる"
