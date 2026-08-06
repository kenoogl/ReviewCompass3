"""セッションログ書庫のLayout v3移行（plan・execute・verify）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

正本はMigration Decision
`records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md`
の§4「実施方法の枠」。既存resolver
`tools.layout.baseline.resolve_project_runtime_layout`を再利用して
private rootを導出し、旧書庫には読み取り以外の操作を行わない。
返り値dictはvalue-safe（相対path・件数・真偽値・Digestのみ）とする。
"""

import hashlib
import json
import os
import shutil
import stat
import tempfile
from pathlib import Path

from tools.layout.baseline import resolve_project_runtime_layout
from tools.session_logs import eventual_preservation
from tools.session_logs.source_adapter import parse_source_bytes
from tools.session_logs.transcript import render_transcript


_METADATA_PREFIXES = ("cursors/", "provenance/", "state/ledgers/")
_TEMPORARY_PREFIX = ".tmp-"


class MigrationError(Exception):
    """値を表示せず書庫移行の失敗を伝える。"""


class MigrationConflictError(MigrationError):
    """targetに内容の異なる同名fileが存在するため停止した。"""


def resolve_preservation_private_root(
    baseline,
    *,
    runtime_root,
    project_id,
    profile,
):
    """既存resolverでv3 sensitive root配下の書庫private rootを導出する。

    副作用なし。directoryは作らない。
    """
    resolution = resolve_project_runtime_layout(
        baseline,
        runtime_root=runtime_root,
        project_id=project_id,
        profile=profile,
    )
    return resolution.roots["sensitive"] / "eventual-preservation"


def _scan_files(root):
    """root配下の通常fileを相対path順に走査しsizeとSHA-256を得る。"""
    base = Path(root)
    if not base.exists():
        return {}
    entries = {}
    for path in sorted(base.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        data = path.read_bytes()
        entries[path.relative_to(base).as_posix()] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data),
        }
    return entries


def plan_migration(*, source_root, target_root):
    """移行dry-run。衝突・容量・rollback可能性を報告し一切書き込まない。"""
    source_files = _scan_files(source_root)
    target_files = _scan_files(target_root)
    files = [
        {
            "relative_path": relative_path,
            "sha256": entry["sha256"],
            "size": entry["size"],
        }
        for relative_path, entry in sorted(source_files.items())
    ]
    conflicts = sorted(
        relative_path
        for relative_path, entry in source_files.items()
        if relative_path in target_files
        and target_files[relative_path]["sha256"] != entry["sha256"]
    )
    return {
        "conflicts": conflicts,
        "file_count": len(files),
        "files": files,
        "rollback": {"source_preserved": True},
        "total_bytes": sum(entry["size"] for entry in files),
    }


def _matches_target(source_files, target_files):
    return all(
        target_files.get(relative_path) == entry
        for relative_path, entry in source_files.items()
    )


def _secure_directory_chain(path, boundary):
    """boundary配下でfileの親directory連鎖を0700で用意する。"""
    parents = []
    current = Path(path).parent
    limit = Path(boundary)
    while current != limit:
        parents.append(current)
        current = current.parent
    for directory in reversed(parents):
        directory.mkdir(exist_ok=True, mode=0o700)
        directory.chmod(0o700)


def _copy_bundle(source_root, destination_root, source_files):
    """byte-exact copy。directory 0700・file 0600に固定する。"""
    source = Path(source_root)
    destination = Path(destination_root)
    destination.chmod(0o700)
    for relative_path in sorted(source_files):
        data = (source / relative_path).read_bytes()
        target_path = destination / relative_path
        _secure_directory_chain(target_path, destination)
        target_path.write_bytes(data)
        target_path.chmod(0o600)


def _verify_copied(destination_root, source_files):
    if _scan_files(destination_root) != source_files:
        raise MigrationError("Copied archive does not match the plan")


def _migrate_into_new_target(source, target, source_files):
    """一時directoryへcopy・検証後、atomicにtargetへ配置する。"""
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = Path(tempfile.mkdtemp(
        prefix=_TEMPORARY_PREFIX + target.name + "-",
        dir=target.parent,
    ))
    try:
        _copy_bundle(source, temporary, source_files)
        _verify_copied(temporary, source_files)
        os.rename(temporary, target)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def _complete_partial_target(source, target, source_files, target_files):
    """既存targetの一致済みfileへ触れず、不足fileだけ原子的に補完する。"""
    target.chmod(0o700)
    for relative_path, entry in sorted(source_files.items()):
        if target_files.get(relative_path) == entry:
            continue
        destination = target / relative_path
        _secure_directory_chain(destination, target)
        temporary = destination.with_name(
            _TEMPORARY_PREFIX + destination.name
        )
        try:
            temporary.write_bytes((source / relative_path).read_bytes())
            temporary.chmod(0o600)
            os.replace(temporary, destination)
            destination.chmod(0o600)
        finally:
            temporary.unlink(missing_ok=True)


def execute_migration(*, source_root, target_root):
    """dry-run再実行→衝突なら停止→byte-exact copyをatomicに配置する。

    sourceは読み取りのみ。target全件一致の再実行は`unchanged`で
    終わり、mtimeも変えない。
    """
    source = Path(source_root)
    target = Path(target_root)
    plan = plan_migration(source_root=source, target_root=target)
    if plan["conflicts"]:
        raise MigrationConflictError(
            "Migration target holds conflicting content"
        )
    source_files = {
        entry["relative_path"]: {
            "sha256": entry["sha256"],
            "size": entry["size"],
        }
        for entry in plan["files"]
    }
    report = {
        "file_count": plan["file_count"],
        "rollback": dict(plan["rollback"]),
        "total_bytes": plan["total_bytes"],
    }
    target_files = _scan_files(target)
    if target.exists() and _matches_target(source_files, target_files):
        return {"action": "unchanged", **report}
    if target.exists():
        _complete_partial_target(source, target, source_files, target_files)
    else:
        _migrate_into_new_target(source, target, source_files)
    return {"action": "migrated", **report}


def _raw_line_issues(data):
    """raw bytesのUTF-8 JSONL行検査。(valid, issue_count)を返す。"""
    try:
        lines = data.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return False, 1
    issues = 0
    for line in lines:
        try:
            record = json.loads(line)
        except ValueError:
            issues += 1
            continue
        if not isinstance(record, dict):
            issues += 1
    return issues == 0, issues


def _verbatim_checks(target):
    """target側rawの妥当性と、実rendererによるverbatim再生成byte一致。"""
    raw_root = target / "raw"
    verbatim_root = target / "verbatim"
    raw_valid = True
    issue_count = 0
    verbatim_match = True
    if not raw_root.is_dir():
        return raw_valid, issue_count, verbatim_match
    for raw_path in sorted(raw_root.rglob("*")):
        if raw_path.is_symlink() or not raw_path.is_file():
            continue
        data = raw_path.read_bytes()
        line_valid, line_issues = _raw_line_issues(data)
        raw_valid = raw_valid and line_valid
        issue_count += line_issues
        complete = eventual_preservation._complete_jsonl_prefix(data)
        try:
            parsed = parse_source_bytes(complete).parsed
        except Exception:
            verbatim_match = False
            continue
        issue_count += len(parsed.issues)
        rendered = render_transcript(parsed).encode("utf-8")
        verbatim_path = (
            verbatim_root / raw_path.relative_to(raw_root)
        ).with_suffix(".md")
        if (
            not verbatim_path.is_file()
            or verbatim_path.read_bytes() != rendered
        ):
            verbatim_match = False
    return raw_valid, issue_count, verbatim_match


def _metadata_paths(root):
    base = Path(root)
    if not base.exists():
        return []
    return sorted(
        path.relative_to(base).as_posix()
        for path in base.rglob("*")
        if path.is_file()
        and path.relative_to(base).as_posix().startswith(_METADATA_PREFIXES)
    )


def _metadata_identity_match(source, target):
    """cursor・provenance・ledgerをJSONとして読み、内容一致を確認する。"""
    source_paths = _metadata_paths(source)
    if source_paths != _metadata_paths(target):
        return False
    for relative_path in source_paths:
        try:
            source_payload = json.loads(
                (source / relative_path).read_text(encoding="utf-8")
            )
            target_payload = json.loads(
                (target / relative_path).read_text(encoding="utf-8")
            )
        except (OSError, ValueError):
            return False
        if source_payload != target_payload:
            return False
    return True


def _mode_checks(target):
    """target_root自身と配下のdirectory 0700・file 0600を確認する。"""
    if not target.is_dir():
        return False, False
    directories = [target] + [
        path for path in sorted(target.rglob("*")) if path.is_dir()
    ]
    files = [path for path in sorted(target.rglob("*")) if path.is_file()]
    directory_ok = all(
        stat.S_IMODE(path.stat().st_mode) == 0o700
        for path in directories
    )
    file_ok = all(
        stat.S_IMODE(path.stat().st_mode) == 0o600
        for path in files
    )
    return directory_ok, file_ok


def _residue_counts(target):
    """一時fileとlockの残留件数を数える。"""
    temporary = 0
    locks = 0
    if target.exists():
        for path in sorted(target.rglob("*")):
            if ".tmp" in path.name:
                temporary += 1
            if path.suffix == ".lock":
                locks += 1
    parent = target.parent
    if parent.exists():
        temporary += sum(
            1
            for path in sorted(parent.iterdir())
            if path != target and path.name.startswith(_TEMPORARY_PREFIX)
        )
    return temporary, locks


def verify_migration(*, source_root, target_root):
    """移行後の全件照合。value-safeなchecks dictで結果を返す。"""
    source = Path(source_root)
    target = Path(target_root)
    source_files = _scan_files(source)
    target_files = _scan_files(target)
    paths_match = set(source_files) == set(target_files)
    shared = sorted(set(source_files) & set(target_files))
    raw_valid, issue_count, verbatim_match = _verbatim_checks(target)
    directory_ok, file_ok = _mode_checks(target)
    temporary_count, lock_count = _residue_counts(target)
    checks = {
        "directory_mode_0700": directory_ok,
        "file_count_match": len(source_files) == len(target_files),
        "file_mode_0600": file_ok,
        "lock_residue_count": lock_count,
        "metadata_identity_match": _metadata_identity_match(source, target),
        "raw_jsonl_valid": raw_valid,
        "raw_parse_issue_count": issue_count,
        "relative_paths_match": paths_match,
        "sha256_match": paths_match and all(
            source_files[relative_path]["sha256"]
            == target_files[relative_path]["sha256"]
            for relative_path in shared
        ),
        "size_match": paths_match and all(
            source_files[relative_path]["size"]
            == target_files[relative_path]["size"]
            for relative_path in shared
        ),
        "temporary_residue_count": temporary_count,
        "verbatim_regenerated_match": verbatim_match,
    }
    passed = (
        all(
            value is True
            for key, value in checks.items()
            if not key.endswith("_count")
        )
        and issue_count == 0
        and temporary_count == 0
        and lock_count == 0
    )
    return {
        "checks": checks,
        "file_count": len(target_files),
        "status": "pass" if passed else "fail",
    }
