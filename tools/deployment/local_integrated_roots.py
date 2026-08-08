"""Work 7A：install／project／runtime／sensitiveの4種root分離。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

Layout Baseline v3を唯一のauthorityとして再利用し、4種root identityを
副作用なしで解決する。sensitiveはLayout v3どおりruntime rootの子であり、
新しいroot schemaは作らない。
"""

import dataclasses
from pathlib import Path

from tools.layout import baseline as layout_baseline


ROOT_KINDS = ("install", "project", "runtime", "sensitive")
_PROFILE = "runtime"


class RootSeparationError(Exception):
    """4種rootを安全に解決・検査・初期化できない。

    例外文は安定stop codeだけを持ち、project manifest等の未検査内容を含めない。
    """

    def __init__(self, stop_code):
        self.stop_code = stop_code
        super().__init__(stop_code)


@dataclasses.dataclass(frozen=True)
class LocalIntegratedRoots:
    """解決済みの4種root。解決だけではdirectoryもfileも作らない。"""

    install_root: Path
    project_root: Path
    runtime_root: Path
    sensitive_root: Path
    project_id: str
    profile: str
    runtime_layout: layout_baseline.ProjectRuntimeLayoutResolution


def _canonical_root(value, *, stop_code, require_directory):
    path = Path(value)
    if not path.is_absolute():
        raise RootSeparationError(stop_code)
    resolved = path.resolve()
    if require_directory:
        if not resolved.is_dir():
            raise RootSeparationError(stop_code)
    elif resolved.exists() and not resolved.is_dir():
        raise RootSeparationError(stop_code)
    return resolved


def _inside(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _overlaps(left, right):
    return _inside(left, right) or _inside(right, left)


def resolve_local_integrated_roots(
    *,
    layout_record_path,
    install_root,
    project_root,
    runtime_root,
):
    """4種rootをLayout v3から副作用なしで解決する。

    project_idはproject内のProject Manifestから読み、profileは`runtime`に
    固定する。callerからproject_idやprofileを受け取らない。
    """

    install = _canonical_root(
        install_root,
        stop_code="install_root_invalid",
        require_directory=True,
    )
    project = _canonical_root(
        project_root,
        stop_code="project_root_invalid",
        require_directory=True,
    )
    runtime = _canonical_root(
        runtime_root,
        stop_code="runtime_root_invalid",
        require_directory=False,
    )
    pairs = (
        (install, project),
        (install, runtime),
        (project, runtime),
    )
    for left, right in pairs:
        if _overlaps(left, right):
            raise RootSeparationError("root_overlap")

    try:
        baseline = layout_baseline.load_layout_baseline(layout_record_path)
    except layout_baseline.LayoutError as error:
        raise RootSeparationError("layout_baseline_invalid") from error
    try:
        layout_baseline.validate_deployment_package_layout(install, baseline)
    except layout_baseline.LayoutError as error:
        raise RootSeparationError("install_package_invalid") from error
    try:
        manifest, _digest = layout_baseline._load_project_manifest(project)
    except layout_baseline.LayoutError as error:
        raise RootSeparationError("project_manifest_invalid") from error
    try:
        runtime_layout = layout_baseline.resolve_project_runtime_layout(
            baseline,
            runtime_root=runtime,
            project_id=manifest["project_id"],
            profile=_PROFILE,
        )
    except layout_baseline.LayoutError as error:
        raise RootSeparationError("runtime_layout_invalid") from error

    sensitive = runtime_layout.roots["sensitive"]
    if (
        not _inside(sensitive, runtime_layout.runtime_root)
        or _inside(sensitive, install)
        or _inside(sensitive, project)
    ):
        raise RootSeparationError("sensitive_root_invalid")
    return LocalIntegratedRoots(
        install_root=install,
        project_root=project,
        runtime_root=runtime_layout.runtime_root,
        sensitive_root=sensitive,
        project_id=runtime_layout.project_id,
        profile=runtime_layout.profile,
        runtime_layout=runtime_layout,
    )


def validate_root_write_target(roots, *, root_kind, target):
    """write targetが宣言root kindの配下だけにあることを検査する。

    検査だけを行い、targetを作成しない。runtime一般writeのsensitive混入は
    拒否し、symlink経由の許可root外へのescapeもcanonical化で拒否する。
    """

    if not isinstance(roots, LocalIntegratedRoots):
        raise RootSeparationError("root_resolution_required")
    if root_kind not in ROOT_KINDS:
        raise RootSeparationError("unknown_root_kind")
    path = Path(target)
    if not path.is_absolute():
        raise RootSeparationError("write_target_invalid")
    canonical = path.resolve()
    bases = {
        "install": roots.install_root,
        "project": roots.project_root,
        "runtime": roots.runtime_root,
        "sensitive": roots.sensitive_root,
    }
    if not _inside(canonical, bases[root_kind]):
        raise RootSeparationError("write_target_outside_root")
    if root_kind == "runtime" and _inside(canonical, roots.sensitive_root):
        raise RootSeparationError("runtime_write_target_in_sensitive")
    return canonical


def _sensitive_component_chain(runtime_root, sensitive_root):
    chain = [runtime_root]
    current = runtime_root
    for part in sensitive_root.relative_to(runtime_root).parts:
        current = current / part
        chain.append(current)
    return chain


def _revalidate_initialization_targets(roots):
    """初期化の最初の副作用より前に、root identityをread-onlyで再検査する。

    解決後から初期化呼出し前に完了したsymlink差替え・identity差替え・
    root escapeを検出してfail-closedに停止する。初期化syscallと同時の
    別processとの競合を防ぐ原子的protocolは後続であり、ここでは扱わない。
    """

    layout = roots.runtime_layout
    if (
        not isinstance(layout, layout_baseline.ProjectRuntimeLayoutResolution)
        or roots.runtime_root != layout.runtime_root
        or roots.sensitive_root != layout.roots.get("sensitive")
        or roots.project_id != layout.project_id
        or roots.profile != layout.profile
        or roots.profile != _PROFILE
    ):
        raise RootSeparationError("runtime_initialization_target_invalid")
    for stored in (roots.install_root, roots.project_root):
        if (
            not stored.is_absolute()
            or stored.is_symlink()
            or not stored.is_dir()
            or stored.resolve() != stored
        ):
            raise RootSeparationError("runtime_initialization_target_invalid")
    runtime = roots.runtime_root
    sensitive = roots.sensitive_root
    if (
        not runtime.is_absolute()
        or not _inside(sensitive, runtime)
        or runtime.resolve() != runtime
        or sensitive.resolve() != sensitive
        or _overlaps(runtime, roots.install_root)
        or _overlaps(runtime, roots.project_root)
    ):
        raise RootSeparationError("runtime_initialization_target_invalid")
    for component in _sensitive_component_chain(runtime, sensitive):
        if component.is_symlink():
            raise RootSeparationError("runtime_initialization_target_invalid")
        if component.exists() and not component.is_dir():
            raise RootSeparationError("runtime_initialization_target_invalid")


def initialize_local_integrated_roots(roots):
    """runtime rootの必要な祖先とsensitive rootだけを明示作成する。

    installとproject、同じruntime profileの他kind、configは作成・変更しない。
    filesystemへの最初の副作用より前にroot identityを再検査し、不合格なら
    Layout初期化を呼ばずに停止する。
    """

    if not isinstance(roots, LocalIntegratedRoots):
        raise RootSeparationError("root_resolution_required")
    try:
        _revalidate_initialization_targets(roots)
    except RootSeparationError:
        raise
    except (OSError, RuntimeError):
        # 原因例外はhost pathや未検査内容を文言に含み得るため、__cause__にも
        # __context__にも残さない。handler内で連結せず、handler外でraiseする。
        revalidation_failed = True
    else:
        revalidation_failed = False
    if revalidation_failed:
        raise RootSeparationError("runtime_initialization_target_invalid")
    try:
        created = layout_baseline.initialize_project_runtime_layout(
            roots.runtime_layout,
            requested_kinds=["sensitive"],
        )
    except layout_baseline.LayoutError as error:
        raise RootSeparationError("runtime_initialization_failed") from error
    return created
