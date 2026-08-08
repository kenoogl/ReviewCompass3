"""task専用のPython bytecode cache rootを解決し、明示的にだけ初期化する。

承認：`DEC-MACHINE-OPERATION-ROUTING-TASK-PYTHON-CACHE-001`
対象Issue：`ISSUE-HTC-C9F6C917`

配置・所有・保持はここで新しく決めない。Human承認済みのLayout v3をそのまま使う。

- 正本：`records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json`
- 外部root：`<runtime_root>/projects/<project_id>/development/cache/`
- cacheはproject外、Git管理外、runtime所有、再生成できる区分である。

このmoduleが持つ責任は3つだけである。

1. 解決（read-only）。pathを決めるだけで、directoryを一切作らない。
2. 初期化（明示）。Layout v3のcache rootと、そのtask directoryだけを作る。
3. 環境mappingの生成。`PYTHONPYCACHEPREFIX`だけを持つmappingを返す。
   実行中processの環境は変更しない。呼び出す側が子Python processへ明示的に渡す。

削除、保持期限の自動判断、既存runnerへの接続はこのmoduleに置かない。
"""

import dataclasses
import json
import re
from pathlib import Path
from tools.common.errors import FailClosedError

from tools.layout import baseline as layout_baseline


#: Layout v3の正本record。project root基準の相対pathである。
LAYOUT_BASELINE_RECORD = (
    "records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json"
)

#: 現在対象のprofile。承認範囲は`development`だけである。
CACHE_PROFILE = "development"
ALLOWED_PROFILES = frozenset({CACHE_PROFILE})

#: cache root配下でPython bytecodeだけを置くdirectory名。
BYTECODE_DIRECTORY_NAME = "python-bytecode"

#: Pythonがbytecode cacheの出力先を決める環境変数。
BYTECODE_VARIABLE = "PYTHONPYCACHEPREFIX"

#: Project Manifestのpath。project root基準の相対pathである。
PROJECT_MANIFEST_PATH = ".reviewcompass/project-manifest.json"

STOP_CODES = (
    "project_root_invalid",
    "project_manifest_invalid",
    "project_id_invalid",
    "layout_baseline_invalid",
    "profile_invalid",
    "task_id_invalid",
    "runtime_root_invalid",
    "runtime_root_overlaps_project",
    "cache_target_symlink",
    "cache_target_not_directory",
    "cache_initialization_failed",
)

_IDENTIFIER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class TaskPythonCacheError(FailClosedError):
    """task専用cacheを安全に扱えない。判断できない入力はここで止める。"""


@dataclasses.dataclass(frozen=True)
class TaskPythonCacheResolution:
    """副作用なしに決めたtask専用cacheの配置。"""

    project_root: Path
    project_id: str
    profile: str
    task_id: str
    runtime_root: Path
    cache_root: Path
    bytecode_root: Path
    task_directory: Path
    layout_resolution: object


def _identifier(value, *, code):
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise TaskPythonCacheError(code, repr(value))
    return value


def _load_project_id(project_root):
    """project IDはProject Manifestの固定値からだけ読む。

    callerが任意のproject IDを渡して別projectのcacheへ書けないようにする。
    """

    path = project_root / PROJECT_MANIFEST_PATH
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeDecodeError) as error:
        raise TaskPythonCacheError("project_manifest_invalid", str(path)) from error
    if not isinstance(manifest, dict):
        raise TaskPythonCacheError("project_manifest_invalid", str(path))
    return _identifier(manifest.get("project_id"), code="project_id_invalid")


def _overlaps(left, right):
    return _inside(left, right) or _inside(right, left)


def _inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_task_cache(*, project_root, runtime_root, task_id, profile=CACHE_PROFILE):
    """task専用cacheのpathを決めるだけで、directoryは一切作らない。"""

    root = Path(project_root)
    if not root.is_absolute() or not root.is_dir():
        raise TaskPythonCacheError("project_root_invalid", str(project_root))
    root = root.resolve()

    if profile not in ALLOWED_PROFILES:
        raise TaskPythonCacheError("profile_invalid", repr(profile))
    _identifier(task_id, code="task_id_invalid")

    runtime = Path(runtime_root)
    if not runtime.is_absolute():
        raise TaskPythonCacheError("runtime_root_invalid", str(runtime_root))
    runtime = _existing_ancestor_resolved(runtime)
    if _overlaps(runtime, root):
        raise TaskPythonCacheError("runtime_root_overlaps_project", str(runtime))

    project_id = _load_project_id(root)

    record = root / LAYOUT_BASELINE_RECORD
    try:
        baseline = layout_baseline.load_layout_baseline(record)
        resolution = layout_baseline.resolve_project_runtime_layout(
            baseline,
            runtime_root=runtime,
            project_id=project_id,
            profile=profile,
        )
    except layout_baseline.LayoutError as error:
        raise TaskPythonCacheError("layout_baseline_invalid", str(error)) from error

    cache_root = resolution.roots["cache"]
    bytecode_root = cache_root / BYTECODE_DIRECTORY_NAME
    return TaskPythonCacheResolution(
        project_root=root,
        project_id=project_id,
        profile=profile,
        task_id=task_id,
        runtime_root=resolution.runtime_root,
        cache_root=cache_root,
        bytecode_root=bytecode_root,
        task_directory=bytecode_root / task_id,
        layout_resolution=resolution,
    )


def _existing_ancestor_resolved(path):
    """まだ無いpathでも、実在する祖先まで辿って絶対pathへ正規化する。"""

    if path.exists():
        return path.resolve()
    for ancestor in path.parents:
        if ancestor.exists():
            return ancestor.resolve() / path.relative_to(ancestor)
    return path


def initialize_task_cache(resolution):
    """Layout v3のcache rootと、そのtask directoryだけを作る。

    他のroot種別（data、state、logs、evaluation、sensitive）とconfig rootは作らない。
    既にあるものはそのまま使う。symlink、通常file、root脱出は作る前に拒否する。
    """

    if not isinstance(resolution, TaskPythonCacheResolution):
        raise TaskPythonCacheError("cache_initialization_failed", "resolution required")
    if not _inside(resolution.task_directory, resolution.cache_root):
        raise TaskPythonCacheError(
            "cache_initialization_failed", str(resolution.task_directory)
        )

    _reject_unsafe_targets(resolution)

    try:
        layout_baseline.initialize_project_runtime_layout(
            resolution.layout_resolution, requested_kinds=["cache"]
        )
        resolution.task_directory.mkdir(parents=True, exist_ok=True)
    except (layout_baseline.LayoutError, OSError) as error:
        raise TaskPythonCacheError("cache_initialization_failed", str(error)) from error
    return resolution.task_directory


def _reject_unsafe_targets(resolution):
    """作る前に、経路上のsymlinkとdirectoryでない通常fileを拒否する。"""

    current = resolution.runtime_root
    steps = [current]
    for part in resolution.task_directory.relative_to(current).parts:
        current = current / part
        steps.append(current)
    for step in steps:
        if step.is_symlink():
            raise TaskPythonCacheError("cache_target_symlink", str(step))
        if step.exists() and not step.is_dir():
            raise TaskPythonCacheError("cache_target_not_directory", str(step))


def bytecode_environment(resolution):
    """`PYTHONPYCACHEPREFIX`だけを持つmappingを返す。

    実行中processの環境は変更しない。呼び出す側が子Python processへ明示的に渡す。
    """

    if not isinstance(resolution, TaskPythonCacheResolution):
        raise TaskPythonCacheError("cache_initialization_failed", "resolution required")
    return {BYTECODE_VARIABLE: str(resolution.task_directory)}
