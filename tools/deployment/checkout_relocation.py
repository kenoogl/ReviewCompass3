"""Work 7A第2項 前駆slice：read-only Gitによる捕捉とcheckout移動後照合。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

実Git checkoutからRepository Binding・Source Snapshot・Change Setを値として捕捉し、
checkout移動・別checkout後にidentityと状態を照合する。production APIはread-only Gitの
subcommandだけを使い、objects・refs・index・worktreeを変更しない。

`repository_id`は本前駆slice限定の**暫定lineage ID**（HEAD履歴のroot commit群の
辞書順連結のSHA-256）であり、耐久repository identityではない。耐久Binding保存・
Verification Run復元は後続sliceとする（再評価record条件1）。

捕捉recordは永続保存しないin-memory値であり、fieldsはWork 3承認authorityに従う。
例外は安定stop codeだけを持ち、host pathや未検査内容を文言に含めない。
"""

import datetime
import hashlib
import os
import subprocess
from pathlib import Path

from tools.common.digests import canonical_content_digest, file_sha256
from tools.layout import baseline as layout_baseline


SCM_KIND = "git"
_BINDING_FIELDS = (
    "project_id",
    "repository_id",
    "binding_id",
    "scm_kind",
    "repository_root",
    "checkout_or_worktree",
)
_SNAPSHOT_FIELDS = (
    "repository_binding_id",
    "base_commit",
    "head_commit",
    "index_state",
    "tracked_changes",
    "included_untracked_files",
    "content_manifest_digest",
    "dependency_lock_identity",
    "capture_time",
    "exclusion_rules_and_reasons",
)
_CHANGE_SET_FIELDS = (
    "base_snapshot_id",
    "candidate_snapshot_id",
    "added_modified_deleted_renamed_items",
    "changed_files_and_symbols",
    "work_item_id",
    "task_contract_id",
    "change_semantics",
    "merge_split_supersedes_relations",
)
_CHANGE_KINDS = {"A": "add", "M": "modify", "D": "delete"}
# rename検出thresholdとNUL区切りは利用者configに依存させず明示する。
_DIFF_ARGUMENTS = ("diff", "--name-status", "-z", "--find-renames=50%")


class RelocationError(Exception):
    """checkoutのidentity・状態を安全に捕捉・照合できない。

    例外文は安定stop codeだけを持ち、pathや未検査内容を含めない。
    """

    def __init__(self, stop_code):
        self.stop_code = stop_code
        super().__init__(stop_code)


_ENVIRONMENT_INJECTION_KEYS = (
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_NAMESPACE",
    "GIT_CEILING_DIRECTORIES",
    "GIT_COMMON_DIR",
)


def _git_environment():
    # identity導出が呼出し環境のGit設定に依存しないよう、file config
    # （GIT_CONFIG_GLOBAL／SYSTEM）だけでなくcommand-scope注入
    # （GIT_CONFIG_COUNT／KEY_*／VALUE_*）とrepository位置の差替え変数も除去する。
    environment = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_CONFIG")
        and name not in _ENVIRONMENT_INJECTION_KEYS
    }
    environment.update({
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
    })
    return environment


def _run_git(checkout_root, *arguments):
    # --no-optional-locksはglobal optionとしてsubcommandの前に置く。
    return subprocess.run(
        ["git", "--no-optional-locks", "-C", str(checkout_root), *arguments],
        capture_output=True,
        text=True,
        env=_git_environment(),
    )


def _git_query(checkout_root, *arguments):
    completed = _run_git(checkout_root, *arguments)
    if completed.returncode != 0:
        raise RelocationError("git_query_failed")
    return completed.stdout


def _fail_closed(operation, stop_code):
    """予期しない例外を、連鎖を残さずに安定stop codeへ変換して実行する。"""

    try:
        return True, operation()
    except RelocationError:
        raise
    except (OSError, RuntimeError, subprocess.SubprocessError, ValueError):
        succeeded = False
    if not succeeded:
        raise RelocationError(stop_code)


def _canonical_checkout_root(value):
    path = Path(value)
    if not path.is_absolute():
        raise RelocationError("checkout_invalid")
    resolved = path.resolve()
    if not resolved.is_dir():
        raise RelocationError("checkout_invalid")
    toplevel = _git_query(resolved, "rev-parse", "--show-toplevel").strip()
    if not toplevel or Path(toplevel).resolve() != resolved:
        raise RelocationError("checkout_invalid")
    return resolved


def _project_id(checkout_root):
    loaded = None
    try:
        loaded = layout_baseline._load_project_manifest(checkout_root)
    except layout_baseline.LayoutError:
        loaded = None
    if loaded is None:
        raise RelocationError("project_manifest_invalid")
    manifest, _digest = loaded
    return manifest["project_id"]


def _repository_id(checkout_root):
    output = _git_query(checkout_root, "rev-list", "--max-parents=0", "HEAD")
    roots = sorted(line.strip() for line in output.splitlines() if line.strip())
    if not roots:
        raise RelocationError("checkout_invalid")
    return hashlib.sha256("\n".join(roots).encode("utf-8")).hexdigest()


def _checkout_identity(checkout_root):
    git_dir = _git_query(checkout_root, "rev-parse", "--absolute-git-dir").strip()
    if not git_dir:
        raise RelocationError("checkout_invalid")
    return str(Path(git_dir).resolve())


def _resolve_commit(checkout_root, revision):
    if not isinstance(revision, str) or not revision:
        raise RelocationError("commit_not_found")
    completed = _run_git(
        checkout_root,
        "rev-parse",
        "--verify",
        "--quiet",
        revision + "^{commit}",
    )
    resolved = completed.stdout.strip()
    if completed.returncode != 0 or not resolved:
        raise RelocationError("commit_not_found")
    return resolved


def _check_record_digest(record, fields):
    if not isinstance(record, dict) or "content_digest" not in record:
        raise RelocationError("record_digest_mismatch")
    if any(field not in record for field in fields):
        raise RelocationError("record_digest_mismatch")
    if canonical_content_digest(record) != record["content_digest"]:
        raise RelocationError("record_digest_mismatch")


def _status_entries(checkout_root):
    """`git status`から(staged, worktree, untracked)を機械取得する。"""

    output = _git_query(
        checkout_root,
        "status",
        "--porcelain",
        "-z",
        "--untracked-files=all",
    )
    tokens = output.split("\0")
    staged = []
    worktree = []
    untracked = set()
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if not token:
            index += 1
            continue
        if len(token) < 3:
            raise RelocationError("git_query_failed")
        states, relative = token[:2], token[3:]
        index += 1
        if states[0] in ("R", "C"):
            if index >= len(tokens):
                raise RelocationError("git_query_failed")
            index += 1
        if states == "??":
            untracked.add(relative)
            continue
        if states[0] not in (" ", "?"):
            staged.append({"relative_path": relative, "status": states[0]})
        if states[1] not in (" ", "?"):
            worktree.append({"relative_path": relative, "status": states[1]})
    staged.sort(key=lambda item: item["relative_path"])
    worktree.sort(key=lambda item: item["relative_path"])
    return staged, worktree, untracked


def _tracked_changes(checkout_root, staged, worktree):
    """staged／worktree変更を、内容identity付きの決定的な列挙にする。"""

    index_oids = _index_entries(checkout_root)
    changes = []
    for item in staged:
        changes.append({
            "relative_path": item["relative_path"],
            "location": "index",
            "status": item["status"],
            "content_identity": index_oids.get(item["relative_path"]),
        })
    for item in worktree:
        path = checkout_root / item["relative_path"]
        if path.is_symlink():
            # Gitはsymlinkのlink payloadをtracked contentとして追跡する。
            # 参照先fileは読まず、payload自体を種別接頭辞付きで識別する。
            payload = os.readlink(path)
            identity = "symlink:" + hashlib.sha256(
                os.fsencode(payload)
            ).hexdigest()
        elif path.is_file():
            identity = "file:" + file_sha256(path)
        else:
            identity = None
        changes.append({
            "relative_path": item["relative_path"],
            "location": "worktree",
            "status": item["status"],
            "content_identity": identity,
        })
    changes.sort(key=lambda item: (item["relative_path"], item["location"]))
    return changes


def _safe_included_untracked(checkout_root, relative, untracked_now):
    if not isinstance(relative, str) or not relative:
        raise RelocationError("snapshot_path_escape")
    pure = Path(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise RelocationError("snapshot_path_escape")
    path = checkout_root / relative
    if path.is_symlink():
        raise RelocationError("snapshot_path_escape")
    resolved = path.resolve()
    try:
        resolved.relative_to(checkout_root)
    except ValueError:
        raise RelocationError("snapshot_path_escape") from None
    if relative not in untracked_now or not resolved.is_file():
        raise RelocationError("untracked_state_mismatch")
    return {"relative_path": relative, "sha256": file_sha256(resolved)}


def _head_tree(checkout_root):
    output = _git_query(checkout_root, "ls-tree", "-r", "-z", "HEAD")
    tree = {}
    for token in output.split("\0"):
        if not token:
            continue
        meta, _tab, relative = token.partition("\t")
        parts = meta.split()
        if len(parts) != 3 or not relative:
            raise RelocationError("git_query_failed")
        tree[relative] = parts[2]
    return tree


def _index_entries(checkout_root):
    output = _git_query(checkout_root, "ls-files", "-s", "-z")
    entries = {}
    for token in output.split("\0"):
        if not token:
            continue
        meta, _tab, relative = token.partition("\t")
        parts = meta.split()
        if len(parts) != 3 or not relative:
            raise RelocationError("git_query_failed")
        entries[relative] = parts[1]
    return entries


def _content_manifest_digest(
    checkout_root,
    tracked_changes,
    included_untracked,
):
    manifest = {
        "head_tree": _head_tree(checkout_root),
        "index_entries": _index_entries(checkout_root),
        "tracked_changes": tracked_changes,
        "included_untracked_files": included_untracked,
    }
    return canonical_content_digest(manifest)


def _capture_repository_binding(checkout_root):
    root = _canonical_checkout_root(checkout_root)
    binding = {
        "project_id": _project_id(root),
        "repository_id": _repository_id(root),
        "scm_kind": SCM_KIND,
        "repository_root": str(root),
        "checkout_or_worktree": _checkout_identity(root),
    }
    binding["binding_id"] = canonical_content_digest({
        "project_id": binding["project_id"],
        "repository_id": binding["repository_id"],
        "scm_kind": binding["scm_kind"],
        "checkout_or_worktree": binding["checkout_or_worktree"],
    })
    binding["content_digest"] = canonical_content_digest(binding)
    return binding


def capture_repository_binding(checkout_root):
    """実GitからRepository Binding値を捕捉する。何も作成・変更しない。"""

    return _fail_closed(
        lambda: _capture_repository_binding(checkout_root),
        "checkout_invalid",
    )[1]


def _capture_source_snapshot(
    checkout_root,
    binding,
    base_commit,
    head_commit,
    included_untracked_files,
):
    root = _canonical_checkout_root(checkout_root)
    _check_record_digest(binding, _BINDING_FIELDS)
    if _repository_id(root) != binding["repository_id"]:
        raise RelocationError("repository_identity_mismatch")
    base = _resolve_commit(root, base_commit)
    head = _resolve_commit(root, head_commit)
    # head_commitはcaller期待値であり、実HEADと一致しない捕捉を作らない。
    if head != _resolve_commit(root, "HEAD"):
        raise RelocationError("head_commit_mismatch")
    staged, worktree, untracked_now = _status_entries(root)
    included = [
        _safe_included_untracked(root, relative, untracked_now)
        for relative in included_untracked_files
    ]
    included.sort(key=lambda item: item["relative_path"])
    tracked_changes = _tracked_changes(root, staged, worktree)
    snapshot = {
        "repository_binding_id": binding["binding_id"],
        "base_commit": base,
        "head_commit": head,
        "index_state": {
            "clean": not staged and not worktree,
            "staged_paths": [item["relative_path"] for item in staged],
        },
        "tracked_changes": tracked_changes,
        "included_untracked_files": included,
        "content_manifest_digest": _content_manifest_digest(
            root,
            tracked_changes,
            included,
        ),
        "dependency_lock_identity": {
            "status": "not_applicable",
            "reason": "no_dependency_lock_in_precursor_slice",
        },
        "capture_time": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(timespec="seconds"),
        "exclusion_rules_and_reasons": [
            {
                "rule": "untracked_files_only_by_explicit_selection",
                "reason": "caller_selected_untracked_files_are_the_scope",
            },
        ],
    }
    snapshot["content_digest"] = canonical_content_digest(snapshot)
    return snapshot


def capture_source_snapshot(
    checkout_root,
    *,
    binding,
    base_commit,
    head_commit,
    included_untracked_files=(),
):
    """実GitからSource Snapshot値を捕捉する。commitは実repositoryで存在検証する。"""

    return _fail_closed(
        lambda: _capture_source_snapshot(
            checkout_root,
            binding,
            base_commit,
            head_commit,
            included_untracked_files,
        ),
        "checkout_invalid",
    )[1]


def _diff_items(checkout_root, base, candidate):
    output = _git_query(checkout_root, *_DIFF_ARGUMENTS, base, candidate)
    tokens = output.split("\0")
    items = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        if not status:
            index += 1
            continue
        kind = status[0]
        if kind in ("R", "C"):
            if index + 2 >= len(tokens):
                raise RelocationError("git_query_failed")
            items.append({
                "change_kind": "rename",
                "previous_path": tokens[index + 1],
                "relative_path": tokens[index + 2],
            })
            index += 3
            continue
        if kind not in _CHANGE_KINDS:
            raise RelocationError("unsupported_change_kind")
        if index + 1 >= len(tokens):
            raise RelocationError("git_query_failed")
        items.append({
            "change_kind": _CHANGE_KINDS[kind],
            "relative_path": tokens[index + 1],
        })
        index += 2
    items.sort(key=lambda item: (item["relative_path"], item["change_kind"]))
    return items


def _changed_files(items):
    files = set()
    for item in items:
        files.add(item["relative_path"])
        if "previous_path" in item:
            files.add(item["previous_path"])
    return sorted(files)


_STATE_KIND_BY_STATUS = {"A": "add", "M": "modify", "D": "delete", "T": "modify"}
_STATE_KIND_BY_LOST_STATUS = {
    "A": "delete",
    "M": "modify",
    "D": "add",
    "T": "modify",
}


def _snapshot_state(snapshot):
    state = {}
    for entry in snapshot["tracked_changes"]:
        state[("tracked", entry["relative_path"], entry["location"])] = (
            entry["status"],
            entry.get("content_identity"),
        )
    for item in snapshot["included_untracked_files"]:
        state[("untracked", item["relative_path"], "untracked")] = (
            item["sha256"],
        )
    return state


def _merge_state_kind(previous, kind):
    if previous is None or previous == kind:
        return kind
    if "add" in (previous, kind):
        return "add"
    if "delete" in (previous, kind):
        return "delete"
    return "modify"


def _state_delta_kinds(base_snapshot, candidate_snapshot):
    """commitに現れないindex・worktree・対象untrackedの実内容差をpath別kindへ写す。"""

    base_state = _snapshot_state(base_snapshot)
    candidate_state = _snapshot_state(candidate_snapshot)
    kinds_by_path = {}
    for key in set(base_state) | set(candidate_state):
        if base_state.get(key) == candidate_state.get(key):
            continue
        category, relative = key[0], key[1]
        if key in candidate_state:
            if category == "untracked":
                kind = "add" if key not in base_state else "modify"
            else:
                kind = _STATE_KIND_BY_STATUS.get(candidate_state[key][0])
        elif category == "untracked":
            kind = "delete"
        else:
            kind = _STATE_KIND_BY_LOST_STATUS.get(base_state[key][0])
        if kind is None:
            raise RelocationError("unsupported_change_kind")
        kinds_by_path[relative] = _merge_state_kind(
            kinds_by_path.get(relative),
            kind,
        )
    return kinds_by_path


def _combined_change_items(checkout_root, base_snapshot, candidate_snapshot):
    """base／candidate Snapshotの実内容差からChange Set項目を導出する。

    commit間のfile delta（A/M/D/R）に、両Snapshotが記録したindex・worktree・
    対象untrackedの状態差を合成する。同一pathはcommit側のkindを優先する。
    """

    base = _resolve_commit(checkout_root, base_snapshot["head_commit"])
    candidate = _resolve_commit(checkout_root, candidate_snapshot["head_commit"])
    combined = {}
    for item in _diff_items(checkout_root, base, candidate):
        combined[item["relative_path"]] = item
    for relative, kind in sorted(
        _state_delta_kinds(base_snapshot, candidate_snapshot).items()
    ):
        if relative not in combined:
            combined[relative] = {
                "change_kind": kind,
                "relative_path": relative,
            }
    items = sorted(
        combined.values(),
        key=lambda item: (item["relative_path"], item["change_kind"]),
    )
    return items


def _derive_change_set(
    checkout_root,
    base_snapshot,
    candidate_snapshot,
    work_item_id,
    task_contract_id,
    change_semantics,
):
    root = _canonical_checkout_root(checkout_root)
    _check_record_digest(base_snapshot, _SNAPSHOT_FIELDS)
    _check_record_digest(candidate_snapshot, _SNAPSHOT_FIELDS)
    if (
        base_snapshot["repository_binding_id"]
        != candidate_snapshot["repository_binding_id"]
    ):
        raise RelocationError("change_set_binding_mismatch")
    items = _combined_change_items(root, base_snapshot, candidate_snapshot)
    change_set = {
        "base_snapshot_id": base_snapshot["content_digest"],
        "candidate_snapshot_id": candidate_snapshot["content_digest"],
        "added_modified_deleted_renamed_items": items,
        "changed_files_and_symbols": {
            "files": _changed_files(items),
            "symbols": {"status": "deferred"},
        },
        "work_item_id": work_item_id,
        "task_contract_id": task_contract_id,
        "change_semantics": change_semantics,
        "merge_split_supersedes_relations": [],
    }
    change_set["content_digest"] = canonical_content_digest(change_set)
    return change_set


def derive_change_set(
    checkout_root,
    *,
    base_snapshot,
    candidate_snapshot,
    work_item_id,
    task_contract_id,
    change_semantics,
):
    """固定したbase／candidate Snapshotから、A/M/D/Rを区別したChange Setを導出する。"""

    return _fail_closed(
        lambda: _derive_change_set(
            checkout_root,
            base_snapshot,
            candidate_snapshot,
            work_item_id,
            task_contract_id,
            change_semantics,
        ),
        "checkout_invalid",
    )[1]


def _rebind_relocated_checkout(checkout_root, prior_binding):
    _check_record_digest(prior_binding, _BINDING_FIELDS)
    current = _capture_repository_binding(checkout_root)
    if current["project_id"] != prior_binding["project_id"]:
        raise RelocationError("project_identity_mismatch")
    if current["repository_id"] != prior_binding["repository_id"]:
        raise RelocationError("repository_identity_mismatch")
    return current


def rebind_relocated_checkout(checkout_root, *, prior_binding):
    """移動・複製後のcheckoutで、lineageとprojectを照合した新Bindingを導出する。"""

    return _fail_closed(
        lambda: _rebind_relocated_checkout(checkout_root, prior_binding),
        "checkout_invalid",
    )[1]


def _verify_source_snapshot(checkout_root, binding, snapshot):
    root = _canonical_checkout_root(checkout_root)
    _check_record_digest(binding, _BINDING_FIELDS)
    _check_record_digest(snapshot, _SNAPSHOT_FIELDS)
    if snapshot["repository_binding_id"] != binding["binding_id"]:
        raise RelocationError("snapshot_binding_mismatch")
    if _repository_id(root) != binding["repository_id"]:
        raise RelocationError("repository_identity_mismatch")
    if _project_id(root) != binding["project_id"]:
        raise RelocationError("project_identity_mismatch")
    _resolve_commit(root, snapshot["base_commit"])
    head = _resolve_commit(root, snapshot["head_commit"])
    if _git_query(root, "rev-parse", "--verify", "HEAD").strip() != head:
        raise RelocationError("checkout_state_mismatch")
    staged, worktree, untracked_now = _status_entries(root)
    if (
        _tracked_changes(root, staged, worktree) != snapshot["tracked_changes"]
        or {
            "clean": not staged and not worktree,
            "staged_paths": [item["relative_path"] for item in staged],
        }
        != snapshot["index_state"]
    ):
        raise RelocationError("checkout_state_mismatch")
    for item in snapshot["included_untracked_files"]:
        recorded_path = item["relative_path"]
        current = None
        if recorded_path in untracked_now:
            current = _safe_included_untracked(
                root,
                recorded_path,
                untracked_now,
            )
        if current is None or current["sha256"] != item["sha256"]:
            raise RelocationError("untracked_state_mismatch")
    recomputed = _content_manifest_digest(
        root,
        snapshot["tracked_changes"],
        snapshot["included_untracked_files"],
    )
    if recomputed != snapshot["content_manifest_digest"]:
        raise RelocationError("checkout_state_mismatch")
    return True


def verify_source_snapshot(checkout_root, *, binding, snapshot):
    """捕捉済みSnapshotを現在のcheckout状態と照合する。読取りだけを行う。"""

    return _fail_closed(
        lambda: _verify_source_snapshot(checkout_root, binding, snapshot),
        "checkout_invalid",
    )[1]


def _verify_change_set(
    checkout_root,
    change_set,
    base_snapshot,
    candidate_snapshot,
):
    root = _canonical_checkout_root(checkout_root)
    _check_record_digest(change_set, _CHANGE_SET_FIELDS)
    _check_record_digest(base_snapshot, _SNAPSHOT_FIELDS)
    _check_record_digest(candidate_snapshot, _SNAPSHOT_FIELDS)
    if (
        change_set["base_snapshot_id"] != base_snapshot["content_digest"]
        or change_set["candidate_snapshot_id"]
        != candidate_snapshot["content_digest"]
    ):
        raise RelocationError("change_set_binding_mismatch")
    if _combined_change_items(root, base_snapshot, candidate_snapshot) != (
        change_set["added_modified_deleted_renamed_items"]
    ):
        raise RelocationError("change_set_state_mismatch")
    return True


def verify_change_set(
    checkout_root,
    *,
    change_set,
    base_snapshot,
    candidate_snapshot,
):
    """Change Setが束縛先Snapshotと実Git deltaに一致することを照合する。"""

    return _fail_closed(
        lambda: _verify_change_set(
            checkout_root,
            change_set,
            base_snapshot,
            candidate_snapshot,
        ),
        "checkout_invalid",
    )[1]
