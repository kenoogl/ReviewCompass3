"""Work 7A：install／project／runtime／sensitiveの4種root分離の受入テスト。

指示書：records/session-handoffs/2026-08-08-codex-to-claude-work7a-four-root-separation.md
authority：Layout Baseline v3（records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json）

固定するのは、(1)副作用なしの4種root解決、(2)宣言rootを越えるwrite targetの
fail-closed拒否、(3)明示初期化がruntime root祖先とsensitive rootだけを作ること。
Testは公開APIの入出力とfilesystem上の事後状態だけをoracleにし、`tmp_path`の
合成fixture（install package、Project Manifest v2付きproject、未作成runtime root）のみ使う。
"""

import hashlib
import importlib
import json
import os
import stat
import traceback
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
BASELINE_V3_RECORD = (
    PROJECT_ROOT
    / "records"
    / "development"
    / "2026-08-04-layout-baseline-v3-project-first-candidate.json"
)
ROOT_KINDS = ("install", "project", "runtime", "sensitive")


def _module():
    return importlib.import_module(
        "tools.deployment.local_integrated_roots"
    )


def _write_install_package(base, name="install"):
    package = base / name
    (package / "tools").mkdir(parents=True)
    (package / "tools" / "entry.py").write_text(
        "print('installed tool')\n",
        encoding="utf-8",
    )
    (package / "VERSION").write_text("0.0.1\n", encoding="utf-8")
    return package


def _write_project(base, name="project", project_id="project-alpha"):
    project = base / name
    manifest_dir = project / ".reviewcompass"
    manifest_dir.mkdir(parents=True)
    manifest = {
        "schema_version": 2,
        "project_id": project_id,
        "artifact_roots": {
            "contracts": "artifacts/contracts",
            "design_decisions": "artifacts/design-decisions",
            "policies": "artifacts/policies",
            "requirement_maps": "artifacts/requirement-maps",
            "reuse": "artifacts/reuse",
            "verified_artifacts": "artifacts/verified",
            "workflow": "artifacts/workflow",
        },
        "document_links": [],
    }
    (manifest_dir / "project-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    (project / "README.md").write_text(
        "synthetic target project\n",
        encoding="utf-8",
    )
    return project


def _fixture(tmp_path):
    install = _write_install_package(tmp_path)
    project = _write_project(tmp_path)
    runtime = tmp_path / "runtime-home" / ".reviewcompass3"
    return install, project, runtime


def _resolve(module, install, project, runtime):
    return module.resolve_local_integrated_roots(
        layout_record_path=BASELINE_V3_RECORD,
        install_root=install,
        project_root=project,
        runtime_root=runtime,
    )


def _inventory(root):
    entries = {}
    for path in sorted(Path(root).rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_file():
            entries[relative] = (
                "file",
                hashlib.sha256(path.read_bytes()).hexdigest(),
                path.stat().st_mtime_ns,
            )
        else:
            entries[relative] = ("dir", path.stat().st_mtime_ns)
    return entries


def test_resolves_four_roots_twice_without_side_effects(tmp_path):
    """正例1・境界例3：解決は2回とも一致し、何も作成・変更しない。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    install_before = _inventory(install)
    project_before = _inventory(project)

    first = _resolve(module, install, project, runtime)
    second = _resolve(module, install, project, runtime)

    assert first == second
    assert first.install_root == install.resolve()
    assert first.project_root == project.resolve()
    assert first.runtime_root == runtime.parent.resolve() / runtime.name
    assert first.project_id == "project-alpha"
    assert first.profile == "runtime"
    assert first.sensitive_root == (
        first.runtime_root / "projects" / "project-alpha" / "runtime" / "sensitive"
    )
    assert not runtime.exists()
    assert _inventory(install) == install_before
    assert _inventory(project) == project_before


def test_sensitive_is_inside_runtime_but_distinct_from_other_kinds(tmp_path):
    """境界例2：sensitiveはruntimeの子として解決され、他のruntime配下kindと異なる。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)

    roots = _resolve(module, install, project, runtime)

    assert roots.sensitive_root.relative_to(roots.runtime_root)
    layout_roots = roots.runtime_layout.roots
    assert roots.sensitive_root == layout_roots["sensitive"]
    for kind in ("data", "state", "cache", "logs", "evaluation"):
        assert roots.sensitive_root != layout_roots[kind]


@pytest.mark.parametrize("root_kind", ROOT_KINDS)
def test_allows_targets_directly_under_each_root_kind(tmp_path, root_kind):
    """正例2：各root kind直下の合成targetはそのroot kindで許可される。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    bases = {
        "install": roots.install_root,
        "project": roots.project_root,
        "runtime": roots.runtime_root,
        "sensitive": roots.sensitive_root,
    }
    target = bases[root_kind] / "synthetic-write-target.txt"

    allowed = module.validate_root_write_target(
        roots,
        root_kind=root_kind,
        target=target,
    )

    assert Path(allowed).is_absolute()
    assert not target.exists()


def test_initialization_creates_only_sensitive_and_runtime_ancestors(tmp_path):
    """正例3：明示初期化はsensitiveと必要なruntime祖先だけを作る。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    install_before = _inventory(install)
    project_before = _inventory(project)

    created = module.initialize_local_integrated_roots(roots)

    assert created == {"sensitive": roots.sensitive_root}
    assert roots.runtime_root.is_dir()
    assert roots.sensitive_root.is_dir()
    layout_roots = roots.runtime_layout.roots
    for kind in ("data", "state", "cache", "logs", "evaluation"):
        assert not layout_roots[kind].exists()
    assert not roots.runtime_layout.config_root.exists()
    if os.name != "nt":
        assert stat.S_IMODE(roots.runtime_root.stat().st_mode) == 0o700
        assert stat.S_IMODE(roots.sensitive_root.stat().st_mode) == 0o700
    assert _inventory(install) == install_before
    assert _inventory(project) == project_before


@pytest.mark.parametrize("overlap", (
    "same_install_project",
    "project_inside_install",
    "runtime_inside_project",
    "runtime_inside_install",
    "install_inside_runtime",
    "symlink_alias_install_project",
))
def test_rejects_overlapping_roots(tmp_path, overlap):
    """負例1：同一・parent／child・symbolic link別名のroot overlapを拒否する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    if overlap == "same_install_project":
        arguments = (project, project, runtime)
    elif overlap == "project_inside_install":
        nested = _write_project(install, name="nested-project")
        arguments = (install, nested, runtime)
    elif overlap == "runtime_inside_project":
        arguments = (install, project, project / "runtime")
    elif overlap == "runtime_inside_install":
        arguments = (install, project, install / "runtime")
    elif overlap == "install_inside_runtime":
        runtime_parent = tmp_path / "runtime-owner"
        nested_install = _write_install_package(
            runtime_parent,
            name="pkg",
        )
        arguments = (nested_install, project, runtime_parent)
    else:
        alias = tmp_path / "install-alias"
        alias.symlink_to(project, target_is_directory=True)
        arguments = (alias, project, runtime)

    with pytest.raises(module.RootSeparationError) as error:
        _resolve(module, *arguments)

    assert error.value.stop_code == "root_overlap"


@pytest.mark.parametrize("root_kind", ROOT_KINDS)
def test_rejects_write_targets_in_any_other_root(tmp_path, root_kind):
    """負例2：各root kindから他rootへのwrite targetを全て拒否する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    bases = {
        "install": roots.install_root,
        "project": roots.project_root,
        "runtime": roots.runtime_root,
        "sensitive": roots.sensitive_root,
    }

    for other_kind, base in bases.items():
        if other_kind == root_kind:
            continue
        if root_kind == "runtime" and other_kind == "sensitive":
            continue
        target = base / "cross-root-target.txt"
        with pytest.raises(module.RootSeparationError) as error:
            module.validate_root_write_target(
                roots,
                root_kind=root_kind,
                target=target,
            )
        assert error.value.stop_code == "write_target_outside_root"


def test_rejects_runtime_write_target_inside_sensitive(tmp_path):
    """負例2：runtime一般writeのsensitive混入を拒否する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    target = roots.sensitive_root / "leak.md"

    with pytest.raises(module.RootSeparationError) as error:
        module.validate_root_write_target(
            roots,
            root_kind="runtime",
            target=target,
        )

    assert error.value.stop_code == "runtime_write_target_in_sensitive"


def test_rejects_symlink_target_escaping_allowed_root(tmp_path):
    """負例3：許可root内のsymlinkがroot外を指すtargetを拒否する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    outside = tmp_path / "outside"
    outside.mkdir()
    escape = install / "escape-link"
    escape.symlink_to(outside, target_is_directory=True)

    with pytest.raises(module.RootSeparationError) as error:
        module.validate_root_write_target(
            roots,
            root_kind="install",
            target=escape / "file.txt",
        )

    assert error.value.stop_code == "write_target_outside_root"


def test_rejects_prefix_sibling_of_declared_root(tmp_path):
    """境界例1：`runtime-other`のような文字列prefixをroot配下と誤判定しない。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    sibling = roots.runtime_root.parent / (roots.runtime_root.name + "-other")

    with pytest.raises(module.RootSeparationError) as error:
        module.validate_root_write_target(
            roots,
            root_kind="runtime",
            target=sibling / "file.txt",
        )

    assert error.value.stop_code == "write_target_outside_root"


def test_rejects_relative_paths_and_unknown_root_kind(tmp_path):
    """負例4：relative path・未知root kindを拒否する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)

    for arguments, stop_code in (
        (
            (Path("relative-install"), project, runtime),
            "install_root_invalid",
        ),
        (
            (install, Path("relative-project"), runtime),
            "project_root_invalid",
        ),
        (
            (install, project, Path("relative-runtime")),
            "runtime_root_invalid",
        ),
    ):
        with pytest.raises(module.RootSeparationError) as error:
            _resolve(module, *arguments)
        assert error.value.stop_code == stop_code

    roots = _resolve(module, install, project, runtime)
    with pytest.raises(module.RootSeparationError) as error:
        module.validate_root_write_target(
            roots,
            root_kind="workspace",
            target=roots.runtime_root / "file.txt",
        )
    assert error.value.stop_code == "unknown_root_kind"
    with pytest.raises(module.RootSeparationError) as error:
        module.validate_root_write_target(
            roots,
            root_kind="runtime",
            target=Path("relative-target.txt"),
        )
    assert error.value.stop_code == "write_target_invalid"


def test_rejects_missing_install_or_project(tmp_path):
    """負例4：存在しないinstall／projectを拒否する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)

    with pytest.raises(module.RootSeparationError) as error:
        _resolve(module, tmp_path / "no-install", project, runtime)
    assert error.value.stop_code == "install_root_invalid"

    with pytest.raises(module.RootSeparationError) as error:
        _resolve(module, install, tmp_path / "no-project", runtime)
    assert error.value.stop_code == "project_root_invalid"


@pytest.mark.parametrize("manifest_case", (
    "missing",
    "broken_json",
    "unknown_keys",
    "invalid_project_id",
))
def test_rejects_invalid_or_missing_project_manifest(tmp_path, manifest_case):
    """負例4：不正／欠落Project Manifestを拒否し、未検査内容を例外文へ出さない。"""

    module = _module()
    install = _write_install_package(tmp_path)
    runtime = tmp_path / "runtime-home" / ".reviewcompass3"
    project = tmp_path / "broken-project"
    manifest_path = project / ".reviewcompass" / "project-manifest.json"
    manifest_path.parent.mkdir(parents=True)
    marker = "UNTRUSTED-MANIFEST-CONTENT-MARKER"
    if manifest_case == "missing":
        manifest_path.parent.rmdir()
        project.mkdir(exist_ok=True)
    elif manifest_case == "broken_json":
        manifest_path.write_text(
            "{not json %s" % marker,
            encoding="utf-8",
        )
    elif manifest_case == "unknown_keys":
        manifest_path.write_text(
            json.dumps({"unexpected": marker}),
            encoding="utf-8",
        )
    else:
        manifest_path.write_text(
            json.dumps({
                "schema_version": 2,
                "project_id": "../" + marker,
                "artifact_roots": {},
                "document_links": [],
            }),
            encoding="utf-8",
        )

    with pytest.raises(module.RootSeparationError) as error:
        _resolve(module, install, project, runtime)

    assert error.value.stop_code == "project_manifest_invalid"
    chained = error.value
    while chained is not None:
        assert marker not in str(chained)
        chained = getattr(chained, "__cause__", None)


@pytest.mark.parametrize("package_case", (
    "project_artifact",
    "runtime_root",
))
def test_rejects_install_package_containing_prohibited_paths(
    tmp_path,
    package_case,
):
    """負例4：Project Artifactまたはruntime rootを内包するinstall packageを拒否する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    if package_case == "project_artifact":
        prohibited = install / ".reviewcompass" / "project-manifest.json"
        prohibited.parent.mkdir()
        prohibited.write_text("{}", encoding="utf-8")
    else:
        (install / ".reviewcompass3" / "projects").mkdir(parents=True)

    with pytest.raises(module.RootSeparationError) as error:
        _resolve(module, install, project, runtime)

    assert error.value.stop_code == "install_package_invalid"


def _state_snapshot(root):
    """root自身を含むmode・mtime・種別・内容Digestの読み取り専用snapshot。"""

    base = Path(root)
    entries = {}
    for path in [base, *sorted(base.rglob("*"))]:
        info = path.lstat()
        relative = "." if path == base else path.relative_to(base).as_posix()
        if path.is_symlink():
            kind = "symlink"
        elif path.is_file():
            kind = (
                "file",
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
        else:
            kind = "dir"
        entries[relative] = (
            stat.S_IMODE(info.st_mode),
            info.st_mtime_ns,
            kind,
        )
    return entries


@pytest.mark.parametrize("swap_case", (
    "runtime_root_symlink",
    "component_symlink",
    "ancestor_symlink",
))
def test_initialization_rejects_post_resolution_symlink_swaps(
    tmp_path,
    monkeypatch,
    swap_case,
):
    """負例：解決後のsymlink差替えを初期化の副作用より前にfail-closedで停止する。

    runtime root本体、下位component（projects）、解決時未作成だった祖先の3態様。
    Layout初期化APIが呼ばれず、install・projectのinventory・Digest・mode・mtimeが
    不変で、symlink先にsensitiveやその祖先が作られないことを機械確認する。
    """

    module = _module()
    layout = importlib.import_module("tools.layout.baseline")
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)

    if swap_case == "runtime_root_symlink":
        runtime.parent.mkdir(parents=True)
        runtime.symlink_to(install, target_is_directory=True)
        forbidden = install / "projects"
    elif swap_case == "component_symlink":
        runtime.mkdir(parents=True)
        (runtime / "projects").symlink_to(
            install,
            target_is_directory=True,
        )
        forbidden = install / "project-alpha"
    else:
        runtime.parent.symlink_to(install, target_is_directory=True)
        forbidden = install / ".reviewcompass3"

    calls = []
    original = layout.initialize_project_runtime_layout

    def recording_initializer(*args, **kwargs):
        calls.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(
        layout,
        "initialize_project_runtime_layout",
        recording_initializer,
    )
    install_before = _state_snapshot(install)
    project_before = _state_snapshot(project)

    with pytest.raises(module.RootSeparationError) as error:
        module.initialize_local_integrated_roots(roots)

    assert error.value.stop_code == "runtime_initialization_target_invalid"
    assert calls == []
    assert _state_snapshot(install) == install_before
    assert _state_snapshot(project) == project_before
    assert not forbidden.exists()
    assert not roots.sensitive_root.exists()
    marker = str(tmp_path)
    chained = error.value
    while chained is not None:
        assert marker not in str(chained)
        chained = getattr(chained, "__cause__", None)


def _rendered_exception(error):
    return "".join(traceback.format_exception(
        type(error),
        error,
        error.__traceback__,
    ))


def _install_initializer_spy(monkeypatch):
    layout = importlib.import_module("tools.layout.baseline")
    calls = []
    original = layout.initialize_project_runtime_layout

    def recording_initializer(*args, **kwargs):
        calls.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(
        layout,
        "initialize_project_runtime_layout",
        recording_initializer,
    )
    return calls


def test_initialization_symlink_loop_stops_without_leaking_cause(
    tmp_path,
    monkeypatch,
):
    """負例：自己参照symlink loopでも、例外連鎖・tracebackへpathを漏らさず停止する。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    runtime.parent.mkdir(parents=True)
    runtime.symlink_to(runtime)
    calls = _install_initializer_spy(monkeypatch)
    install_before = _state_snapshot(install)
    project_before = _state_snapshot(project)

    with pytest.raises(module.RootSeparationError) as error:
        module.initialize_local_integrated_roots(roots)

    assert error.value.stop_code == "runtime_initialization_target_invalid"
    assert error.value.__cause__ is None
    assert error.value.__context__ is None
    rendered = _rendered_exception(error.value)
    assert str(tmp_path) not in rendered
    assert "Symlink loop" not in rendered
    assert calls == []
    assert _state_snapshot(install) == install_before
    assert _state_snapshot(project) == project_before
    assert runtime.is_symlink()
    assert sorted(runtime.parent.iterdir()) == [runtime]


def test_initialization_forced_runtime_error_stops_without_leaking_cause(
    tmp_path,
    monkeypatch,
):
    """負例：再検査中の合成marker入りRuntimeErrorも、連鎖・tracebackへ漏らさない。"""

    module = _module()
    install, project, runtime = _fixture(tmp_path)
    roots = _resolve(module, install, project, runtime)
    marker = "SYNTHETIC-EXCEPTION-PATH-MARKER"

    def failing_resolve(self, strict=False):
        raise RuntimeError("synthetic failure at %s" % marker)

    calls = _install_initializer_spy(monkeypatch)
    install_before = _state_snapshot(install)
    project_before = _state_snapshot(project)
    monkeypatch.setattr(Path, "resolve", failing_resolve)

    with pytest.raises(module.RootSeparationError) as error:
        module.initialize_local_integrated_roots(roots)

    monkeypatch.undo()
    assert error.value.stop_code == "runtime_initialization_target_invalid"
    assert error.value.__cause__ is None
    assert error.value.__context__ is None
    rendered = _rendered_exception(error.value)
    assert marker not in rendered
    assert str(tmp_path) not in rendered
    assert calls == []
    assert _state_snapshot(install) == install_before
    assert _state_snapshot(project) == project_before
    assert not runtime.exists()
    assert not runtime.parent.exists()
