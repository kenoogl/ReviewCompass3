"""セッションログ書庫のLayout v3移行のAcceptance Test（RED）。

検証項目の正本はMigration Decision
`records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md`
の§4「実施方法の枠」。対象は未実装module
`tools.session_logs.preservation_migration`であり、本Testは
import失敗（ModuleNotFoundError）または属性不在で全件REDになる。
"""

import hashlib
import importlib
import json
import stat
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
BASELINE_V3_CANDIDATE = (
    PROJECT_ROOT
    / "records"
    / "development"
    / "2026-08-04-layout-baseline-v3-project-first-candidate.json"
)
_MARKER = "MIGRATION-FIXTURE-MARKER-20260806"


def _module():
    return importlib.import_module(
        "tools.session_logs.preservation_migration"
    )


def _write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = b"".join(
        (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
        for record in records
    )
    path.write_bytes(encoded)
    return encoded


def _claude_records():
    return (
        {
            "uuid": "user-1",
            "type": "user",
            "sessionId": "session-1",
            "message": {
                "role": "user",
                "content": "移行対象の会話 %s" % _MARKER,
            },
        },
        {
            "uuid": "assistant-1",
            "type": "assistant",
            "sessionId": "session-1",
            "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": "移行fixtureを保存しました。"}],
            },
        },
    )


def _build_archive(tmp_path):
    """実collectorで旧配置bundle（raw・verbatim・cursor・provenance・ledger）を合成する。"""
    repository = tmp_path / "repository"
    (repository / ".git").mkdir(parents=True)
    native_root = tmp_path / "native"
    raw_log = native_root / "claude" / "session.jsonl"
    _write_jsonl(raw_log, _claude_records())
    source_root = tmp_path / "old-archive"
    collector = importlib.import_module(
        "tools.session_logs.eventual_preservation"
    )
    result = collector.collect_source(
        raw_log,
        source_root=native_root,
        private_root=source_root,
        repository_root=repository,
        tool_version="migration-test-v1",
        run_id="run-1",
        observed_at="2026-08-06T10:00:00+09:00",
    )
    assert result.action == "created"
    assert result.state == "reconciled"
    return source_root


def _file_snapshot(root):
    base = Path(root)
    return {
        path.relative_to(base).as_posix(): {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "size": path.stat().st_size,
            "mode": stat.S_IMODE(path.stat().st_mode),
        }
        for path in sorted(base.rglob("*"))
        if path.is_file()
    }


def _directory_modes(root):
    base = Path(root)
    modes = {
        path.relative_to(base).as_posix(): stat.S_IMODE(path.stat().st_mode)
        for path in sorted(base.rglob("*"))
        if path.is_dir()
    }
    modes["."] = stat.S_IMODE(base.stat().st_mode)
    return modes


def _file_mtimes(root):
    base = Path(root)
    return {
        path.relative_to(base).as_posix(): path.stat().st_mtime_ns
        for path in sorted(base.rglob("*"))
        if path.is_file()
    }


def _residues(root):
    base = Path(root)
    if not base.exists():
        return []
    return [
        path.relative_to(base).as_posix()
        for path in sorted(base.rglob("*"))
        if ".tmp" in path.name or path.suffix == ".lock"
    ]


def test_resolves_v3_preservation_root_from_layout_resolver(tmp_path):
    """Decision §4: 既存resolver（resolve_project_runtime_layout）を再利用し、
    development/sensitive root配下の書庫private rootを導出する（重複resolverを実装しない）。"""
    layout = importlib.import_module("tools.layout.baseline")
    baseline = layout.load_layout_baseline(BASELINE_V3_CANDIDATE)
    runtime_root = tmp_path / ".reviewcompass3"
    module = _module()

    resolved = module.resolve_preservation_private_root(
        baseline,
        runtime_root=runtime_root,
        project_id="reviewcompass3",
        profile="development",
    )

    assert Path(resolved) == (
        runtime_root
        / "projects"
        / "reviewcompass3"
        / "development"
        / "sensitive"
        / "eventual-preservation"
    )
    assert not runtime_root.exists()


def test_dry_run_reports_files_and_no_conflicts_without_writing(tmp_path):
    """Decision §4: dry-run（衝突・容量・rollback可能性）を計画dictとして返し、
    target側にもsource側にも一切書込みをしない。"""
    source_root = _build_archive(tmp_path)
    target_root = tmp_path / "runtime-sensitive" / "eventual-preservation"
    before = _file_snapshot(source_root)
    module = _module()

    plan = module.plan_migration(
        source_root=source_root,
        target_root=target_root,
    )

    assert plan["file_count"] == len(before) == 5
    assert plan["total_bytes"] == sum(
        entry["size"] for entry in before.values()
    )
    assert plan["conflicts"] == []
    assert plan["rollback"]["source_preserved"] is True
    planned = {entry["relative_path"]: entry for entry in plan["files"]}
    assert set(planned) == set(before)
    for relative_path, entry in before.items():
        assert planned[relative_path]["size"] == entry["size"]
        assert planned[relative_path]["sha256"] == entry["sha256"]
    assert not target_root.exists()
    assert not target_root.parent.exists()
    assert _file_snapshot(source_root) == before


def test_migration_copies_byte_exact_and_verifies(tmp_path):
    """Decision §4: 一時領域へのbyte-exact copy→全件照合（file数・相対path・size・
    SHA-256・rawのUTF-8 JSONL妥当性・verbatim再生成byte一致・cursor/provenance/ledger
    identity一致・directory 0700・file 0600・一時／lock残留0）。"""
    source_root = _build_archive(tmp_path)
    target_root = tmp_path / "runtime-sensitive" / "eventual-preservation"
    source_files = _file_snapshot(source_root)
    module = _module()

    executed = module.execute_migration(
        source_root=source_root,
        target_root=target_root,
    )
    verification = module.verify_migration(
        source_root=source_root,
        target_root=target_root,
    )

    assert executed["action"] == "migrated"
    target_files = _file_snapshot(target_root)
    assert set(target_files) == set(source_files)
    for relative_path, entry in source_files.items():
        assert target_files[relative_path]["size"] == entry["size"]
        assert target_files[relative_path]["sha256"] == entry["sha256"]
        assert target_files[relative_path]["mode"] == 0o600
    assert all(
        mode == 0o700
        for mode in _directory_modes(target_root).values()
    )
    assert _residues(target_root.parent) == []
    for raw_path in sorted((target_root / "raw").rglob("*.jsonl")):
        for line in raw_path.read_bytes().decode("utf-8").splitlines():
            assert isinstance(json.loads(line), dict)
    assert verification["status"] == "pass"
    assert verification["file_count"] == len(source_files)
    checks = verification["checks"]
    assert checks["file_count_match"] is True
    assert checks["relative_paths_match"] is True
    assert checks["size_match"] is True
    assert checks["sha256_match"] is True
    assert checks["raw_jsonl_valid"] is True
    assert checks["raw_parse_issue_count"] == 0
    assert checks["verbatim_regenerated_match"] is True
    assert checks["metadata_identity_match"] is True
    assert checks["directory_mode_0700"] is True
    assert checks["file_mode_0600"] is True
    assert checks["temporary_residue_count"] == 0
    assert checks["lock_residue_count"] == 0


def test_second_run_is_unchanged(tmp_path):
    """Decision §4: 冪等再実行。targetがsourceと全件一致する再実行は
    `unchanged`で終わり、target側のfileを一切書き換えない。"""
    source_root = _build_archive(tmp_path)
    target_root = tmp_path / "runtime-sensitive" / "eventual-preservation"
    module = _module()

    first = module.execute_migration(
        source_root=source_root,
        target_root=target_root,
    )
    target_before = _file_snapshot(target_root)
    mtimes_before = _file_mtimes(target_root)
    second = module.execute_migration(
        source_root=source_root,
        target_root=target_root,
    )

    assert first["action"] == "migrated"
    assert second["action"] == "unchanged"
    assert _file_snapshot(target_root) == target_before
    assert _file_mtimes(target_root) == mtimes_before


def test_conflicting_target_stops_without_overwrite(tmp_path):
    """Decision §4: targetに異なる内容が存在する場合は上書きせず停止する
    （停止条件「target衝突」）。source・targetとも変更されない。"""
    source_root = _build_archive(tmp_path)
    target_root = tmp_path / "runtime-sensitive" / "eventual-preservation"
    source_before = _file_snapshot(source_root)
    relative_path = sorted(source_before)[0]
    conflicting = target_root / relative_path
    conflicting.parent.mkdir(parents=True)
    conflicting_bytes = b"conflicting-content\n"
    conflicting.write_bytes(conflicting_bytes)
    module = _module()

    with pytest.raises(module.MigrationConflictError):
        module.execute_migration(
            source_root=source_root,
            target_root=target_root,
        )

    assert conflicting.read_bytes() == conflicting_bytes
    target_files = [
        path.relative_to(target_root).as_posix()
        for path in sorted(target_root.rglob("*"))
        if path.is_file()
    ]
    assert target_files == [relative_path]
    assert _residues(target_root.parent) == []
    assert _file_snapshot(source_root) == source_before


def test_source_is_never_modified(tmp_path):
    """Decision §2・§4: 旧配置は削除せずrollback copyとして保持する。
    plan・execute・verifyのいずれもsourceのfile内容・permission・mtimeを変更しない。"""
    source_root = _build_archive(tmp_path)
    target_root = tmp_path / "runtime-sensitive" / "eventual-preservation"
    files_before = _file_snapshot(source_root)
    directories_before = _directory_modes(source_root)
    mtimes_before = _file_mtimes(source_root)
    module = _module()

    module.plan_migration(
        source_root=source_root,
        target_root=target_root,
    )
    module.execute_migration(
        source_root=source_root,
        target_root=target_root,
    )
    module.verify_migration(
        source_root=source_root,
        target_root=target_root,
    )

    assert _file_snapshot(source_root) == files_before
    assert _directory_modes(source_root) == directories_before
    assert _file_mtimes(source_root) == mtimes_before


def test_report_is_value_safe(tmp_path):
    """Decision §4: Migration ReceiptとEvidenceはvalue-safe。計画・実行・検証の
    返り値dictを文字列化しても、会話本文とprivate絶対pathを含まない
    （相対pathと論理表記のみ）。"""
    source_root = _build_archive(tmp_path)
    target_root = tmp_path / "runtime-sensitive" / "eventual-preservation"
    module = _module()

    plan = module.plan_migration(
        source_root=source_root,
        target_root=target_root,
    )
    executed = module.execute_migration(
        source_root=source_root,
        target_root=target_root,
    )
    verification = module.verify_migration(
        source_root=source_root,
        target_root=target_root,
    )

    for payload in (plan, executed, verification):
        text = json.dumps(payload, ensure_ascii=False, default=str)
        assert _MARKER not in text
        assert str(source_root) not in text
        assert str(target_root) not in text
        assert str(tmp_path) not in text
        assert str(Path.home()) not in text
