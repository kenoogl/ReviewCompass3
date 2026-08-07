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
import re
import subprocess
import sys
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


def _result(status, findings, machine_count, red_verification=None):
    document = {
        "status": status,
        "findings": sorted(findings),
        "machine_count": machine_count,
    }
    if red_verification is not None:
        document["red_verification"] = red_verification
    return document


_OUTCOME_LINE = re.compile(
    r"^(?P<outcome>PASSED|FAILED|ERROR|SKIPPED)\s+(?P<node>\S+::\S+)"
)
_COLLECTION_ERROR_LINE = re.compile(r"^ERROR\s+(?P<file>\S+\.py)\s*$")


def parse_pytest_outcomes(output, *, node_ids):
    """pytestの報告からnode idごとの結果を読む。

    収集エラー（ImportErrorなど）ではtest単位の行が出ないため、そのfileに属する
    node idをすべてerrorとして扱う。実装未着手のREDを`unknown`と取り違えない。
    """

    outcomes = {}
    failed_files = set()
    for line in output.splitlines():
        stripped = line.strip()
        matched = _OUTCOME_LINE.match(stripped)
        if matched:
            outcomes[matched.group("node")] = matched.group("outcome").lower()
            continue
        collection = _COLLECTION_ERROR_LINE.match(stripped)
        if collection:
            failed_files.add(collection.group("file"))
    for node_id in node_ids:
        if node_id in outcomes:
            continue
        if node_id.split("::", 1)[0] in failed_files:
            outcomes[node_id] = "error"
    return outcomes


def pytest_runner(node_ids, *, project_root):
    """node idごとの結果を返す既定runner。判定はpytestの報告に従う。"""

    if not node_ids:
        return {}
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-rA", *sorted(node_ids)],
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )
    return parse_pytest_outcomes(completed.stdout, node_ids=sorted(node_ids))


def _verify_red_claims(*, declarations, project_root, runner):
    """宣言のred_now主張を実行結果と突き合わせる。不明はfail-closedで扱う。

    red_now: trueは対象testが実際に失敗していること、falseは実際に成功して
    いることを要求する。結果を得られないtestは合格と見なさない。
    """

    claims = {}
    for key in sorted(declarations):
        entry = declarations[key]
        for item in entry.get("tests") or []:
            if isinstance(item, dict) and isinstance(item.get("test"), str):
                claims[item["test"]] = (key, bool(item.get("red_now")))

    outcomes = runner(sorted(claims), project_root=project_root)
    findings = []
    verified = mismatched = unknown = 0
    for node_id in sorted(claims):
        declaration_key, expects_red = claims[node_id]
        outcome = outcomes.get(node_id)
        if outcome is None:
            unknown += 1
            findings.append(f"red_outcome_unknown: {declaration_key}: {node_id}")
            continue
        actually_red = outcome in ("failed", "error")
        if actually_red == expects_red:
            verified += 1
        else:
            mismatched += 1
            code = "red_claim_unmet" if expects_red else "boundary_claim_unmet"
            findings.append(f"{code}: {declaration_key}: {node_id}: {outcome}")
    summary = {
        "checked": len(claims),
        "verified": verified,
        "mismatched": mismatched,
        "unknown": unknown,
    }
    return summary, findings


def check_declaration_red_map(
    *, map_path, project_root=".", verify_red=False, runner=None
):
    """対応表を検査し、status、findings、machine_countを返す。fail-closed。

    `verify_red=True`のとき、宣言のred_now主張を実際のtest実行と突き合わせる
    （反証C-4の処置）。既定は静的検査のみで、testを実行しない。
    """

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

    # scope欄は判定対象の広さを宣言する。欄が無い対応表はcompleteとして扱い、
    # 黙って範囲を狭められないようにする（反証C-1）。
    scope = document.get("scope") or {}
    scope_kind = scope.get("kind", "complete")
    if scope_kind not in ("complete", "partial"):
        findings.append(f"scope_kind_invalid: {scope_kind}")
        scope_kind = "complete"
    if scope_kind == "partial" and not str(scope.get("reason", "")).strip():
        findings.append("scope_reason_missing: partial scope requires a reason")

    machine_count["declarations"] = len(declarations)

    bound = {}
    owner = {}
    for key in sorted(declarations):
        entry = declarations[key]
        tests = entry.get("tests") if isinstance(entry, dict) else None
        if isinstance(entry, dict) and not str(entry.get("summary", "")).strip():
            findings.append(f"declaration_summary_empty: {key}")
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
            # 一つのtestを複数の宣言で使い回すと、宣言の数だけ被覆があるように
            # 見えて実際には一つしか検査していない。
            if reference in owner:
                findings.append(
                    f"shared_test_across_declarations: {reference}: "
                    f"{owner[reference]},{key}"
                )
            else:
                owner[reference] = key

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
        listed = listed_by_file.get(relative, set())
        declared = bound.get(relative, set())
        if functions is not None:
            for name in sorted(listed | declared):
                if name not in functions:
                    machine_count["listed_tests_missing_in_file"] += 1
                    findings.append(f"listed_test_missing: {relative}::{name}")
        # completeを宣言した対応表は、fileに実在するtest全体を判定対象にする。
        # partialは列挙分だけを対象にし、範囲を狭めた理由をrecordへ残す。
        if scope_kind == "complete" and functions is not None:
            for name in sorted(set(functions) - declared - listed):
                machine_count["tests_unmapped_to_declarations"] += 1
                findings.append(f"test_unmapped_to_declarations: {relative}::{name}")
        # test_files欄と宣言側のtest集合は双方向で一致しなければならない。
        for name in sorted(listed - declared):
            machine_count["tests_unmapped_to_declarations"] += 1
            findings.append(f"test_unmapped_to_declarations: {relative}::{name}")
        for name in sorted(declared - listed):
            machine_count["tests_unmapped_to_declarations"] += 1
            findings.append(f"test_missing_from_listing: {relative}::{name}")

    red_verification = None
    if verify_red:
        red_verification, red_findings = _verify_red_claims(
            declarations=declarations,
            project_root=project_root,
            runner=runner or pytest_runner,
        )
        findings.extend(red_findings)

    status = "passed" if not findings else "failed"
    return _result(status, findings, machine_count, red_verification)
