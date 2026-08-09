"""Work 7A第2項 前駆slice：read-only Git捕捉とcheckout移動後照合の受入テスト。

範囲固定：records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md
再評価（条件付きverified）：records/session-handoffs/2026-08-09-codex-scope-reevaluation-work7a-checkout-relocation-v1.md

固定するのは次である。

- 呼出し側の申告値ではなく、実Gitからidentityと状態（base・HEAD・index・dirty・
  tracked・staged・untracked）を取得する。
- checkout移動・別checkout（clone・worktree）後もproject／repositoryの同一性を照合し、
  checkoutごとにBindingを区別する。
- Change Setはadd／modify／delete／renameを区別し、base Snapshotとcandidate Snapshotの
  2 recordへ束縛され、不一致を拒否する（再評価条件2）。
- symlink逸脱・不正commit・untracked欠落・dirty／index不一致・record改竄を
  fail-closedに拒否する。

`repository_id`は本前駆slice限定の**暫定lineage ID**であり、耐久repository identityでは
ない（再評価条件1）。fixture構築に限り`tmp_path`内でgit init・add・commit・worktree等を
使い（scope §7-4）、production APIはread-only Gitのみを使う。実ホーム・既存repositoryへ
はaccessしない。
"""

import hashlib
import importlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest


PROJECT_ID = "project-alpha"
BINDING_FIELDS = {
    "project_id",
    "repository_id",
    "binding_id",
    "scm_kind",
    "repository_root",
    "checkout_or_worktree",
}


def _module():
    return importlib.import_module("tools.deployment.checkout_relocation")


def _git_environment():
    environment = dict(os.environ)
    environment.update({
        "GIT_AUTHOR_NAME": "fixture",
        "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "fixture",
        "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
    })
    return environment


def _git(cwd, *arguments):
    """fixture構築と期待値算出の専用Git実行。production APIはこれを使わない。"""

    completed = subprocess.run(
        ["git", "-C", str(cwd), *arguments],
        capture_output=True,
        text=True,
        check=True,
        env=_git_environment(),
    )
    return completed.stdout.strip()


def _write_manifest(checkout, project_id=PROJECT_ID):
    manifest_dir = checkout / ".reviewcompass"
    manifest_dir.mkdir(parents=True, exist_ok=True)
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


def _make_checkout(base, name="checkout-a", project_id=PROJECT_ID):
    checkout = base / name
    checkout.mkdir(parents=True)
    _write_manifest(checkout, project_id)
    (checkout / "a.txt").write_text("alpha\n", encoding="utf-8")
    (checkout / "b.txt").write_text("beta\n", encoding="utf-8")
    (checkout / "c.txt").write_text(
        "gamma-line-1\ngamma-line-2\ngamma-line-3\ngamma-line-4\n",
        encoding="utf-8",
    )
    _git(checkout, "init")
    _git(checkout, "add", ".")
    _git(checkout, "commit", "-m", "commit-1")
    return checkout


def _head(checkout):
    return _git(checkout, "rev-parse", "HEAD")


def _expected_repository_id(checkout):
    """暫定lineage ID：HEAD履歴のroot commit群の辞書順連結のSHA-256。"""

    roots = _git(checkout, "rev-list", "--max-parents=0", "HEAD").splitlines()
    joined = "\n".join(sorted(roots))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()


def _capture_clean(module, checkout):
    binding = module.capture_repository_binding(checkout)
    head = _head(checkout)
    snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=head,
        head_commit=head,
    )
    return binding, snapshot


def test_captures_identity_and_states_from_real_git(tmp_path):
    """正例1：識別と状態を申告値でなく実Gitから取得する。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    commit_1 = _head(checkout)
    (checkout / "staged.txt").write_text("staged\n", encoding="utf-8")
    _git(checkout, "add", "staged.txt")
    (checkout / "a.txt").write_text("alpha dirty\n", encoding="utf-8")
    (checkout / "untracked.txt").write_text("untracked\n", encoding="utf-8")

    binding = module.capture_repository_binding(checkout)
    snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=commit_1,
        head_commit="HEAD",
        included_untracked_files=("untracked.txt",),
    )

    assert set(binding) == BINDING_FIELDS | {"content_digest"}
    assert binding["scm_kind"] == "git"
    assert binding["project_id"] == PROJECT_ID
    assert binding["repository_id"] == _expected_repository_id(checkout)
    assert Path(binding["repository_root"]) == checkout.resolve()
    assert snapshot["repository_binding_id"] == binding["binding_id"]
    assert snapshot["base_commit"] == commit_1
    assert snapshot["head_commit"] == commit_1
    assert snapshot["index_state"]["clean"] is False
    assert "staged.txt" in snapshot["index_state"]["staged_paths"]
    tracked = {
        (item["relative_path"], item["location"])
        for item in snapshot["tracked_changes"]
    }
    assert ("staged.txt", "index") in tracked
    assert ("a.txt", "worktree") in tracked
    untracked = {
        item["relative_path"]: item["sha256"]
        for item in snapshot["included_untracked_files"]
    }
    assert untracked == {
        "untracked.txt": hashlib.sha256(b"untracked\n").hexdigest(),
    }
    assert snapshot["dependency_lock_identity"]["status"] == "not_applicable"
    assert "exclusion_rules_and_reasons" in snapshot
    assert "capture_time" in snapshot


def test_recapture_is_deterministic_except_capture_time(tmp_path):
    """正例2：同一状態の再捕捉はcapture_timeを除き同じnormalized identityを生む。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    first_binding, first_snapshot = _capture_clean(module, checkout)
    second_binding, second_snapshot = _capture_clean(module, checkout)

    assert first_binding == second_binding

    def _normalized(snapshot):
        return {
            key: value
            for key, value in snapshot.items()
            if key not in ("capture_time", "content_digest")
        }

    assert _normalized(first_snapshot) == _normalized(second_snapshot)


def test_other_checkouts_share_lineage_with_distinct_bindings(tmp_path):
    """正例3：同じcommitを共有するclone・worktreeは、同一lineage・別binding_id。"""

    module = _module()
    original = _make_checkout(tmp_path)
    clone = tmp_path / "clone-b"
    _git(tmp_path, "clone", str(original), str(clone))
    worktree = tmp_path / "worktree-c"
    _git(original, "worktree", "add", str(worktree))

    bindings = [
        module.capture_repository_binding(checkout)
        for checkout in (original, clone, worktree)
    ]

    assert len({binding["binding_id"] for binding in bindings}) == 3
    assert len({binding["checkout_or_worktree"] for binding in bindings}) == 3
    assert {binding["repository_id"] for binding in bindings} == {
        bindings[0]["repository_id"],
    }
    assert {binding["project_id"] for binding in bindings} == {PROJECT_ID}


def test_relocated_checkout_rebinds_and_verifies_snapshot(tmp_path):
    """正例4：checkout移動後にlineageとprojectを保持した新Bindingを導出し、照合が成立する。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    binding, snapshot = _capture_clean(module, checkout)
    moved = tmp_path / "moved" / "checkout-a"
    moved.parent.mkdir()
    shutil.move(str(checkout), str(moved))

    rebound = module.rebind_relocated_checkout(moved, prior_binding=binding)

    assert rebound["repository_id"] == binding["repository_id"]
    assert rebound["project_id"] == binding["project_id"]
    assert rebound["binding_id"] != binding["binding_id"]
    assert rebound["checkout_or_worktree"] != binding["checkout_or_worktree"]
    assert module.verify_source_snapshot(
        moved,
        binding=binding,
        snapshot=snapshot,
    ) is True


def test_change_set_distinguishes_kinds_and_binds_snapshots(tmp_path):
    """正例5＋再評価条件2：A/M/D/Rの区別と、base／candidate Snapshotへの束縛。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    commit_1 = _head(checkout)
    binding = module.capture_repository_binding(checkout)
    base_snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=commit_1,
        head_commit=commit_1,
    )
    (checkout / "added.txt").write_text("added\n", encoding="utf-8")
    (checkout / "a.txt").write_text("alpha modified\n", encoding="utf-8")
    _git(checkout, "rm", "--quiet", "b.txt")
    _git(checkout, "mv", "c.txt", "renamed.txt")
    _git(checkout, "add", "-A")
    _git(checkout, "commit", "-m", "commit-2")
    commit_2 = _head(checkout)
    candidate_snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=commit_1,
        head_commit=commit_2,
    )

    change_set = module.derive_change_set(
        checkout,
        base_snapshot=base_snapshot,
        candidate_snapshot=candidate_snapshot,
        work_item_id="WORK-7A-2-PRECURSOR",
        task_contract_id="none",
        change_semantics="precursor-fixture",
    )

    items = change_set["added_modified_deleted_renamed_items"]
    kinds = {
        (item["change_kind"], item["relative_path"])
        for item in items
    }
    assert ("add", "added.txt") in kinds
    assert ("modify", "a.txt") in kinds
    assert ("delete", "b.txt") in kinds
    renames = [
        (item["previous_path"], item["relative_path"])
        for item in items
        if item["change_kind"] == "rename"
    ]
    assert renames == [("c.txt", "renamed.txt")]
    assert change_set["base_snapshot_id"] == base_snapshot["content_digest"]
    assert change_set["candidate_snapshot_id"] == (
        candidate_snapshot["content_digest"]
    )
    assert change_set["work_item_id"] == "WORK-7A-2-PRECURSOR"
    assert change_set["task_contract_id"] == "none"
    assert change_set["change_semantics"] == "precursor-fixture"
    assert change_set["merge_split_supersedes_relations"] == []
    assert change_set["changed_files_and_symbols"]["symbols"] == {
        "status": "deferred",
    }
    assert set(change_set["changed_files_and_symbols"]["files"]) == {
        "a.txt",
        "added.txt",
        "b.txt",
        "c.txt",
        "renamed.txt",
    }
    assert module.verify_change_set(
        checkout,
        change_set=change_set,
        base_snapshot=base_snapshot,
        candidate_snapshot=candidate_snapshot,
    ) is True


def test_change_set_rejects_snapshot_binding_mismatch(tmp_path):
    """再評価条件2：束縛先と異なるSnapshotでの照合を拒否する。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    commit_1 = _head(checkout)
    binding = module.capture_repository_binding(checkout)
    base_snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=commit_1,
        head_commit=commit_1,
    )
    (checkout / "added.txt").write_text("added\n", encoding="utf-8")
    _git(checkout, "add", "-A")
    _git(checkout, "commit", "-m", "commit-2")
    commit_2 = _head(checkout)
    candidate_snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=commit_1,
        head_commit=commit_2,
    )
    change_set = module.derive_change_set(
        checkout,
        base_snapshot=base_snapshot,
        candidate_snapshot=candidate_snapshot,
        work_item_id="WORK-7A-2-PRECURSOR",
        task_contract_id="none",
        change_semantics="precursor-fixture",
    )
    other_snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=commit_2,
        head_commit=commit_2,
    )

    with pytest.raises(module.RelocationError) as error:
        module.verify_change_set(
            checkout,
            change_set=change_set,
            base_snapshot=other_snapshot,
            candidate_snapshot=candidate_snapshot,
        )

    assert error.value.stop_code == "change_set_binding_mismatch"


@pytest.mark.parametrize("bogus_field", ("base", "head"))
def test_rejects_commits_absent_from_repository(tmp_path, bogus_field):
    """負例6：実repositoryに存在しないbase／head commitを拒否する。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    commit_1 = _head(checkout)
    binding = module.capture_repository_binding(checkout)
    bogus = "f" * 40
    base_commit = bogus if bogus_field == "base" else commit_1
    head_commit = bogus if bogus_field == "head" else commit_1

    with pytest.raises(module.RelocationError) as error:
        module.capture_source_snapshot(
            checkout,
            binding=binding,
            base_commit=base_commit,
            head_commit=head_commit,
        )

    assert error.value.stop_code == "commit_not_found"


def test_rejects_symlink_escape_without_ingesting_content(tmp_path):
    """負例7：checkout内symlinkのcheckout外参照を拒否し、外部内容を取り込まない。"""

    module = _module()
    checkout = _make_checkout(tmp_path / "inner")
    head = _head(checkout)
    binding = module.capture_repository_binding(checkout)
    marker = "OUTSIDE-CONTENT-MARKER"
    outside = tmp_path / "outside-secret.txt"
    outside.write_text(marker + "\n", encoding="utf-8")
    (checkout / "escape.txt").symlink_to(outside)

    with pytest.raises(module.RelocationError) as error:
        module.capture_source_snapshot(
            checkout,
            binding=binding,
            base_commit=head,
            head_commit=head,
            included_untracked_files=("escape.txt",),
        )

    assert error.value.stop_code == "snapshot_path_escape"
    chained = error.value
    while chained is not None:
        assert marker not in str(chained)
        assert str(tmp_path) not in str(chained)
        chained = chained.__cause__


def test_verification_fails_when_included_untracked_file_is_missing(tmp_path):
    """負例8：manifestへ記録した対象untracked fileの欠落を照合失敗にする。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    head = _head(checkout)
    binding = module.capture_repository_binding(checkout)
    (checkout / "untracked.txt").write_text("untracked\n", encoding="utf-8")
    snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=head,
        head_commit=head,
        included_untracked_files=("untracked.txt",),
    )
    (checkout / "untracked.txt").unlink()

    with pytest.raises(module.RelocationError) as error:
        module.verify_source_snapshot(
            checkout,
            binding=binding,
            snapshot=snapshot,
        )

    assert error.value.stop_code == "untracked_state_mismatch"


@pytest.mark.parametrize("mismatch", ("staged", "dirty"))
def test_verification_fails_on_index_or_dirty_mismatch(tmp_path, mismatch):
    """負例9：記録したindex／dirty状態と実状態の不一致を照合失敗にする。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    binding, snapshot = _capture_clean(module, checkout)
    (checkout / "a.txt").write_text("alpha changed\n", encoding="utf-8")
    if mismatch == "staged":
        _git(checkout, "add", "a.txt")

    with pytest.raises(module.RelocationError) as error:
        module.verify_source_snapshot(
            checkout,
            binding=binding,
            snapshot=snapshot,
        )

    assert error.value.stop_code == "checkout_state_mismatch"


@pytest.mark.parametrize("manifest_case", ("missing", "tampered"))
def test_rejects_missing_or_tampered_project_manifest(tmp_path, manifest_case):
    """負例10：Manifest欠落・project_id改変での捕捉・再bindを拒否する。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    if manifest_case == "missing":
        (checkout / ".reviewcompass" / "project-manifest.json").unlink()
        (checkout / ".reviewcompass").rmdir()
        with pytest.raises(module.RelocationError) as error:
            module.capture_repository_binding(checkout)
        assert error.value.stop_code == "project_manifest_invalid"
        return

    binding = module.capture_repository_binding(checkout)
    _write_manifest(checkout, project_id="project-other")
    with pytest.raises(module.RelocationError) as error:
        module.rebind_relocated_checkout(checkout, prior_binding=binding)
    assert error.value.stop_code == "project_identity_mismatch"


def test_branch_rename_and_move_keep_lineage_identity(tmp_path):
    """負例11：branch名とfilesystem pathはdurable identityではない。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    binding = module.capture_repository_binding(checkout)
    assert set(binding) == BINDING_FIELDS | {"content_digest"}
    _git(checkout, "branch", "-m", "renamed-line")
    moved = tmp_path / "moved" / "checkout-a"
    moved.parent.mkdir()
    shutil.move(str(checkout), str(moved))

    rebound = module.rebind_relocated_checkout(moved, prior_binding=binding)

    assert rebound["repository_id"] == binding["repository_id"]
    assert rebound["project_id"] == binding["project_id"]


def test_clean_clones_share_content_manifest_digest(tmp_path):
    """境界12：clean・同一HEADのclone間でcontent_manifest_digestが一致する。"""

    module = _module()
    original = _make_checkout(tmp_path)
    clone = tmp_path / "clone-b"
    _git(tmp_path, "clone", str(original), str(clone))
    _original_binding, original_snapshot = _capture_clean(module, original)
    _clone_binding, clone_snapshot = _capture_clean(module, clone)

    assert original_snapshot["content_manifest_digest"] == (
        clone_snapshot["content_manifest_digest"]
    )


@pytest.mark.parametrize("record_kind", ("binding", "snapshot", "change_set"))
def test_rejects_tampered_capture_records(tmp_path, record_kind):
    """境界13：捕捉recordのcontent digest改竄を照合で拒否する。"""

    module = _module()
    checkout = _make_checkout(tmp_path)
    commit_1 = _head(checkout)
    binding = module.capture_repository_binding(checkout)
    snapshot = module.capture_source_snapshot(
        checkout,
        binding=binding,
        base_commit=commit_1,
        head_commit=commit_1,
    )

    if record_kind == "binding":
        tampered = dict(binding)
        tampered["repository_root"] = str(tmp_path / "elsewhere")
        with pytest.raises(module.RelocationError) as error:
            module.rebind_relocated_checkout(checkout, prior_binding=tampered)
    elif record_kind == "snapshot":
        tampered = dict(snapshot)
        tampered["head_commit"] = "f" * 40
        with pytest.raises(module.RelocationError) as error:
            module.verify_source_snapshot(
                checkout,
                binding=binding,
                snapshot=tampered,
            )
    else:
        (checkout / "added.txt").write_text("added\n", encoding="utf-8")
        _git(checkout, "add", "-A")
        _git(checkout, "commit", "-m", "commit-2")
        commit_2 = _head(checkout)
        candidate_snapshot = module.capture_source_snapshot(
            checkout,
            binding=binding,
            base_commit=commit_1,
            head_commit=commit_2,
        )
        change_set = module.derive_change_set(
            checkout,
            base_snapshot=snapshot,
            candidate_snapshot=candidate_snapshot,
            work_item_id="WORK-7A-2-PRECURSOR",
            task_contract_id="none",
            change_semantics="precursor-fixture",
        )
        tampered = dict(change_set)
        tampered["work_item_id"] = "WORK-TAMPERED"
        with pytest.raises(module.RelocationError) as error:
            module.verify_change_set(
                checkout,
                change_set=tampered,
                base_snapshot=snapshot,
                candidate_snapshot=candidate_snapshot,
            )

    assert error.value.stop_code == "record_digest_mismatch"
