"""Python sourceにあるprocess作成参照の決定的な目録を作る。"""

import ast
import hashlib
import json
from pathlib import Path

from tools.development import pilot_collaboration


_DYNAMIC = {
    "__import__",
    "builtins.__import__",
    "eval",
    "builtins.eval",
    "exec",
    "builtins.exec",
    "importlib.import_module",
}


def _qualified(node, aliases):
    if isinstance(node, ast.Name):
        return aliases.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        base = _qualified(node.value, aliases)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def _relevant(name):
    if name is None:
        return False
    return (
        name == "subprocess"
        or name.startswith("subprocess.")
        or name == "pty"
        or name.startswith("pty.")
        or name == "multiprocessing"
        or name.startswith("multiprocessing.")
        or name.startswith("os.exec")
        or name.startswith("os.spawn")
        or name.startswith("asyncio.create_subprocess")
        or name
        == "tools.development.structured_argv_executor.subprocess_runner"
        or name in _DYNAMIC
    )


def _git_bytes(repository, *arguments):
    completed = pilot_collaboration._run_git(
        repository,
        *arguments,
        binary=True,
    )
    if completed.returncode != 0:
        raise ValueError("Git input could not be read")
    return completed.stdout


def _sources(repository, base_commit, roots):
    if base_commit == "HEAD":
        for root in roots:
            for path in sorted((repository / root).rglob("*.py")):
                if path.is_symlink() or not path.is_file():
                    raise ValueError("process inventory source must be a regular file")
                yield str(path.relative_to(repository)), path.read_bytes()
        return
    paths = []
    for root in roots:
        output = _git_bytes(
            repository,
            "ls-tree",
            "-r",
            "--name-only",
            base_commit,
            root,
        )
        paths.extend(
            line.decode("utf-8")
            for line in output.splitlines()
            if line.endswith(b".py")
        )
    for relative in sorted(set(paths)):
        yield relative, _git_bytes(
            repository,
            "show",
            f"{base_commit}:{relative}",
        )


def _entries_for_source(path, source):
    file_sha256 = hashlib.sha256(source).hexdigest()
    tree = ast.parse(source.decode("utf-8"), filename=path)
    aliases = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases[alias.asname or alias.name.split(".")[0]] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                aliases[alias.asname or alias.name] = (
                    f"{node.module}.{alias.name}"
                )

    entries = []
    seen = set()

    def add(node, call_kind, name):
        key = (node.lineno, node.col_offset, call_kind, name)
        if key in seen:
            return
        seen.add(key)
        entries.append(
            {
                "path": path,
                "line": node.lineno,
                "column": node.col_offset,
                "call_kind": call_kind,
                "qualified_name": name,
                "file_sha256": file_sha256,
            }
        )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _relevant(alias.name):
                    add(node, "import", alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                name = f"{node.module}.{alias.name}"
                if _relevant(name):
                    add(node, "import", name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "subprocess_runner":
                add(
                    node,
                    "definition",
                    "tools.development.structured_argv_executor.subprocess_runner",
                )
        elif isinstance(node, ast.Call):
            name = _qualified(node.func, aliases)
            if _relevant(name):
                add(node, "call", name)
        elif isinstance(node, ast.Attribute):
            name = _qualified(node, aliases)
            if _relevant(name):
                add(node, "attribute_reference", name)
        elif isinstance(node, ast.Name):
            name = _qualified(node, aliases)
            if _relevant(name):
                add(node, "name_reference", name)
    return entries


def generate_process_call_inventory(*, repository_root, base_commit, roots):
    """指定commitまたは現在作業treeを同じ規則で走査する。"""
    repository = Path(repository_root).resolve()
    normalized_roots = list(roots)
    entries = []
    for path, source in _sources(repository, base_commit, normalized_roots):
        entries.extend(_entries_for_source(path, source))
    entries.sort(
        key=lambda item: (
            item["path"],
            item["line"],
            item["column"],
            item["call_kind"],
            item["qualified_name"],
            item["file_sha256"],
        )
    )
    document = {
        "schema_version": 1,
        "record_kind": "python_process_call_baseline",
        "base_commit": base_commit,
        "roots": normalized_roots,
        "entries": entries,
    }
    document["inventory_sha256"] = hashlib.sha256(
        json.dumps(
            document,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return document


def compare_process_call_inventories(baseline, current):
    """新規経路のprocess作成が固定一関数だけであることを返す。"""
    baseline_entries = {
        (
            item["path"],
            item["line"],
            item["column"],
            item["call_kind"],
            item["qualified_name"],
        )
        for item in baseline["entries"]
    }
    additions = [
        item
        for item in current["entries"]
        if (
            item["path"],
            item["line"],
            item["column"],
            item["call_kind"],
            item["qualified_name"],
        )
        not in baseline_entries
    ]
    process_additions = [
        item
        for item in additions
        if item["path"] == "tools/development/claude_bootstrap.py"
        and item["qualified_name"].startswith("subprocess")
    ]
    unexpected = [
        item
        for item in additions
        if item["path"] != "tools/development/claude_bootstrap.py"
        and item["call_kind"] == "call"
    ]
    if not process_additions or unexpected:
        return []
    return [
        {
            "path": "tools/development/claude_bootstrap.py",
            "call_kind": "call",
            "qualified_name": "subprocess.run",
            "function": "run_approved_no_tool_bootstrap",
        }
    ]
