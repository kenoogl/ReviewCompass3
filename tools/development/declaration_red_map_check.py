"""宣言→RED対応表検査器（Work 5B対象helper）。

承認：DEC-WORK5B-START-001、DEC-WORK5B-IMPLEMENTATION-READY-001
Contract：TC-WORK5B-DECLARATION-RED-MAP-CHECK-001

対応表JSONとtest fileを読み、次を機械判定して決定的な結果を返す。

1. 列挙されたtest関数の実在（AST解析による）
2. testの無い宣言が0件であること
3. 宣言に結ばれないtestが0件であること

判定はfail-closedであり、対応表またはtest fileの欠落・解析不能は不合格とする。
hook、自動実行、commit連動は持たない。対応表を書き換えない。
"""

import ast
import json
from pathlib import Path


class DeclarationRedMapCheckError(Exception):
    """検査器の使用方法自体が不正な場合の失敗。"""


def _collect_test_functions(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    }


def _result(status, findings, machine_count):
    return {
        "status": status,
        "findings": sorted(findings),
        "machine_count": machine_count,
    }


def check_declaration_red_map(*, map_path, project_root="."):
    """対応表を検査し、status、findings、machine_countを返す。fail-closed。"""

    findings = []
    machine_count = {
        "declarations": 0,
        "declarations_without_tests": 0,
        "listed_tests_missing_in_file": 0,
        "tests_unmapped_to_declarations": 0,
    }

    map_file = Path(map_path)
    try:
        document = json.loads(map_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        findings.append(f"map_unreadable: {map_file} ({type(error).__name__})")
        return _result("failed", findings, machine_count)
    if not isinstance(document, dict):
        findings.append(f"map_unreadable: {map_file} (not a mapping)")
        return _result("failed", findings, machine_count)

    test_files = document.get("test_files")
    declarations = document.get("declarations")
    if not isinstance(test_files, dict) or not isinstance(declarations, dict):
        findings.append(
            f"map_unreadable: {map_file} (test_files or declarations is missing)"
        )
        return _result("failed", findings, machine_count)

    machine_count["declarations"] = len(declarations)

    bound = {}
    for key in sorted(declarations):
        entry = declarations[key]
        tests = entry.get("tests") if isinstance(entry, dict) else None
        if not isinstance(tests, list) or not tests:
            machine_count["declarations_without_tests"] += 1
            findings.append(f"declaration_without_tests: {key}")
            continue
        for item in tests:
            reference = item.get("test") if isinstance(item, dict) else None
            if not isinstance(reference, str) or "::" not in reference:
                machine_count["listed_tests_missing_in_file"] += 1
                findings.append(f"listed_test_reference_invalid: {key}: {reference}")
                continue
            file_part, name = reference.split("::", 1)
            bound.setdefault(file_part, set()).add(name)

    universe_files = sorted(set(test_files) | set(bound))
    actual = {}
    for relative in universe_files:
        target = Path(project_root) / relative
        try:
            actual[relative] = _collect_test_functions(target)
        except (OSError, SyntaxError, ValueError) as error:
            actual[relative] = None
            findings.append(
                f"test_file_unreadable: {relative} ({type(error).__name__})"
            )

    listed_by_file = {}
    for relative in sorted(test_files):
        listed = test_files[relative]
        if not isinstance(listed, list):
            findings.append(f"test_file_listing_invalid: {relative}")
            continue
        listed_by_file[relative] = set(listed)

    for relative in universe_files:
        functions = actual.get(relative)
        referenced = bound.get(relative, set()) | listed_by_file.get(relative, set())
        if functions is not None:
            for name in sorted(referenced):
                if name not in functions:
                    machine_count["listed_tests_missing_in_file"] += 1
                    findings.append(f"listed_test_missing: {relative}::{name}")
        for name in sorted(listed_by_file.get(relative, set())):
            if name not in bound.get(relative, set()):
                machine_count["tests_unmapped_to_declarations"] += 1
                findings.append(f"test_unmapped_to_declarations: {relative}::{name}")

    status = "passed" if not findings else "failed"
    return _result(status, findings, machine_count)
