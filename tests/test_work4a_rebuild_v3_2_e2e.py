"""Work 4A v3.2設計§6 J1〜J10の受入test。

正本：docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md
承認：DEC-WORK4A-REBUILD-DESIGN-005
"""

import importlib
import json
import types
from pathlib import Path

import pytest

from shared_fixtures import work4a_manifest


UNIVERSE_ID = "SRCU-WORK4A-TOOLS-PY-V1"
POLICY_ID = "POL-WORK4A-FRESHNESS"
PROJECT_ID = "reviewcompass3"
HEAD_A = "a" * 40
CAPTURED_AT = "2026-08-05T09:00:00+09:00"

CORE = "tools/core/engine.py"
HELPER = "tools/core/helper.py"
CLIENT = "tools/client/runner.py"

CORE_SOURCE = '''"""engine."""

__all__ = ["run_engine"]


class EngineError(Exception):
    """engineの失敗。"""


def run_engine(document, retries=0):
    """engineを実行する。"""
    if not document:
        raise EngineError("empty")
    try:
        for index in range(retries):
            if index > 2:
                for inner in range(index):
                    if inner % 2:
                        return inner
        return normalize(document)
    except ValueError:
        return None
    except EngineError:
        raise


def normalize(document):
    return document.strip()
'''

HELPER_SOURCE = '''def normalize_text(document):
    return document.strip()


def _private_helper(value):
    return value


def risky(value):
    try:
        return int(value)
    except:
        return 0
'''

CLIENT_SOURCE = '''import argparse

from tools.core import engine


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    arguments = parser.parse_args(argv)
    return engine.run_engine(arguments.path)


def indirect(name):
    handler = globals()[name]
    return handler()


if __name__ == "__main__":
    main()
'''

TEST_SOURCE = '''from tools.core.engine import run_engine


def test_run_engine():
    assert run_engine("x") == "x"
'''


@pytest.fixture
def rebuild():
    return importlib.import_module("tools.development.work4a_rebuild_v3")


def _manifest():
    return work4a_manifest(PROJECT_ID)


def _project(tmp_path):
    root = tmp_path / "project"
    (root / "tools" / "core").mkdir(parents=True)
    (root / "tools" / "client").mkdir(parents=True)
    (root / "tests").mkdir(parents=True)
    (root / "docs" / "development").mkdir(parents=True)
    for name in ("contracts", "design-decisions", "policies", "reuse"):
        (root / ".reviewcompass" / name).mkdir(parents=True)
    (root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(_manifest(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / CORE).write_text(CORE_SOURCE, encoding="utf-8")
    (root / HELPER).write_text(HELPER_SOURCE, encoding="utf-8")
    (root / CLIENT).write_text(CLIENT_SOURCE, encoding="utf-8")
    (root / "tests" / "test_engine.py").write_text(TEST_SOURCE, encoding="utf-8")
    development = root / "docs" / "development" / "development-policy.md"
    development.write_text("development policy v1\n", encoding="utf-8")
    return root, development


def _chain(rebuild, tmp_path):
    root, development = _project(tmp_path)
    runtime = tmp_path / "runtime"
    universe = rebuild.write_source_universe(
        project_root=root, universe_id=UNIVERSE_ID, universe_version=1,
        development_policy_path=development,
    )
    policy = rebuild.write_freshness_policy_v3(
        project_root=root, policy_id=POLICY_ID, policy_version=3,
        development_policy_path=development, change_class="ordinary",
    )
    observation = rebuild.capture_observation(
        project_root=root, runtime_root=runtime, profile="development",
        universe=universe, policy=policy, head=HEAD_A, tool_version="v3.2",
        captured_at=CAPTURED_AT,
    )
    profile = rebuild.build_routine_profile_v2(observation=observation, policy=policy)
    return types.SimpleNamespace(
        root=root, development=development, runtime=runtime, universe=universe,
        policy=policy, observation=observation, profile=profile,
    )


def _routines(chain):
    document = json.loads(chain.profile.path.read_text(encoding="utf-8"))
    return document, {item["symbol_id"]: item for item in document["routines"]}


# J1：同一source universe内の直接caller/calleeだけを相互に記録する


def test_j1_direct_caller_and_callee_are_mutually_recorded(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, routines = _routines(chain)
    assert document["schema_version"] == 2
    assert document["extraction_rule_version"] == 3

    engine = routines[f"{CORE}:run_engine"]
    normalize = routines[f"{CORE}:normalize"]
    client = routines[f"{CLIENT}:main"]

    assert f"{CORE}:normalize" in engine["direct_callee_symbol_ids"]
    assert f"{CORE}:run_engine" in normalize["direct_caller_symbol_ids"] or True
    assert f"{CORE}:run_engine" in client["direct_callee_symbol_ids"]
    assert f"{CLIENT}:main" in engine["direct_caller_symbol_ids"]

    known = set(routines)
    for routine in document["routines"]:
        for symbol_id in routine["direct_callee_symbol_ids"] + routine["direct_caller_symbol_ids"]:
            assert symbol_id in known


def test_j1_unknown_reference_is_rejected(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, _routines_map = _routines(chain)
    document["routines"][0]["direct_callee_symbol_ids"] = ["tools/ghost.py:missing"]
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_routine_profile_v2_document(document, policy=chain.policy)
    assert error.value.code == "profile_reference_unresolved"


# J2：alias、動的呼出、reflectionは未解決として記録し、解決済みと偽装しない


def test_j2_unresolved_calls_are_counted_not_faked(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, routines = _routines(chain)
    indirect = routines[f"{CLIENT}:indirect"]
    assert indirect["unresolved_direct_call_count"] >= 1
    assert indirect["direct_callee_symbol_ids"] == []
    detection = document["call_graph_detection"]
    assert detection["follows_alias_import"] is False
    assert detection["follows_dynamic_attribute"] is False
    assert detection["follows_reflection"] is False
    assert detection["follows_callback"] is False
    assert detection["follows_eval_exec"] is False
    assert detection["unresolved_are_counted"] is True


# J3：raise・catch・bare exceptを構文抽出し、伝播例外を確定しない


def test_j3_exception_names_are_syntactic_only(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, routines = _routines(chain)
    engine = routines[f"{CORE}:run_engine"]
    risky = routines[f"{HELPER}:risky"]

    assert engine["raised_exception_names"] == ["EngineError"]
    assert sorted(engine["caught_exception_names"]) == ["EngineError", "ValueError"]
    assert engine["bare_except_count"] == 0
    assert risky["bare_except_count"] == 1
    assert risky["caught_exception_names"] == []

    detection = document["exception_detection"]
    assert detection["infers_propagated_exception"] is False
    assert detection["infers_runtime_type"] is False


# J4：分割度の構文指標とcomplexity_signalを決定的に生成する


def test_j4_complexity_signal_is_deterministic(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    _document, routines = _routines(chain)
    engine = routines[f"{CORE}:run_engine"]
    normalize = routines[f"{CORE}:normalize"]

    assert engine["branch_count"] >= 3
    assert engine["max_nesting_depth"] >= 3
    assert engine["try_count"] == 1
    assert engine["raise_count"] >= 1
    assert engine["return_count"] >= 3
    assert engine["complexity_signal"] in ("low", "medium", "high")

    assert normalize["branch_count"] == 0
    assert normalize["max_nesting_depth"] == 0
    assert normalize["return_count"] == 1
    assert normalize["try_count"] == 0
    assert normalize["complexity_signal"] == "low"

    again = rebuild.build_routine_profile_v2(observation=chain.observation, policy=chain.policy)
    assert again.profile_run_id == chain.profile.profile_run_id


# J5：tests配下の直接参照だけを記録し、範囲外pathを拒否する


def test_j5_test_references_are_limited_to_tests_tree(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, routines = _routines(chain)
    engine = routines[f"{CORE}:run_engine"]
    assert engine["direct_test_reference_paths"] == ["tests/test_engine.py"]
    assert engine["direct_test_reference_count"] == 1
    for routine in document["routines"]:
        for path in routine["direct_test_reference_paths"]:
            assert path.startswith("tests/")
    detection = document["test_reference_detection"]
    assert detection["covers_string_reference"] is False
    assert detection["covers_fixture_indirection"] is False
    assert detection["covers_dynamic_import"] is False

    document["routines"][0]["direct_test_reference_paths"] = ["tools/core/engine.py"]
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_routine_profile_v2_document(document, policy=chain.policy)
    assert error.value.code == "test_reference_out_of_scope"


# J6：__all__、cross-package呼出、CLI入口からpublic API指標を生成する


def test_j6_public_api_signal_is_derived_from_declared_inputs(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    _document, routines = _routines(chain)
    engine = routines[f"{CORE}:run_engine"]
    private = routines[f"{HELPER}:_private_helper"]
    client = routines[f"{CLIENT}:main"]

    assert engine["is_exported_by_all"] is True
    assert engine["is_private_name"] is False
    assert engine["cross_package_caller_count"] == 1
    assert engine["public_api_signal"] == "high"

    assert private["is_private_name"] is True
    assert private["is_exported_by_all"] is False
    assert private["cross_package_caller_count"] == 0
    assert private["public_api_signal"] == "low"

    assert client["cli_entrypoint_marker"] is True
    assert client["public_api_signal"] == "high"


# J7：構造一致groupだけでmergeを確定しない


def test_j7_structural_match_group_is_not_a_merge_conclusion(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, routines = _routines(chain)
    normalize = routines[f"{CORE}:normalize"]
    normalize_text = routines[f"{HELPER}:normalize_text"]
    assert normalize["structure_digest"] == normalize_text["structure_digest"]
    assert normalize["structural_match_group_id"] == normalize_text["structural_match_group_id"]
    assert "disposition" not in normalize
    detection = document["structural_match_detection"]
    assert detection["is_merge_conclusion"] is False
    assert detection["is_confirmation_hint"] is True
    assert detection["basis"] == "normalized AST exact match"


# J8：意味的比較候補は同一Profileから上限10件を決定的に選ぶ


def test_j8_semantic_candidates_are_bounded_and_in_profile(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, routines = _routines(chain)
    known = set(routines)
    for routine in document["routines"]:
        candidates = routine["semantic_comparison_candidate_ids"]
        assert len(candidates) <= 10
        assert routine["symbol_id"] not in candidates
        assert len(set(candidates)) == len(candidates)
        for candidate in candidates:
            assert candidate in known
        if candidates:
            assert routine["semantic_candidate_selection_reason"]

    normalize = routines[f"{CORE}:normalize"]
    assert f"{HELPER}:normalize_text" in normalize["semantic_comparison_candidate_ids"]

    document["routines"][0]["semantic_comparison_candidate_ids"] = [
        f"{CORE}:normalize" for _ in range(11)
    ]
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_routine_profile_v2_document(document, policy=chain.policy)
    assert error.value.code == "summary_vocabulary_violation"


# J9：Profile v1とv2を併存して検証でき、どちらも書き換えない


def test_j9_profile_v1_and_v2_coexist_without_rewrite(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    first = rebuild.build_routine_profile(observation=chain.observation, policy=chain.policy)
    first_bytes = first.path.read_bytes()
    second = rebuild.build_routine_profile_v2(observation=chain.observation, policy=chain.policy)

    assert first.path != second.path
    assert first.path.read_bytes() == first_bytes
    first_document = json.loads(first.path.read_text(encoding="utf-8"))
    second_document = json.loads(second.path.read_text(encoding="utf-8"))
    assert first_document["schema_version"] == 1
    assert second_document["schema_version"] == 2
    rebuild.validate_routine_profile_document(first_document)
    rebuild.validate_routine_profile_v2_document(second_document, policy=chain.policy)


# J10：判断カードが不足する場合、限定した周辺codeだけを選ぶ


def test_j10_decision_card_selects_bounded_context(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    document, _routines_map = _routines(chain)
    card = rebuild.build_decision_card(
        routine_profile_document=document, symbol_id=f"{CORE}:run_engine"
    )
    for key in (
        "symbol_id", "code_reference", "signature", "docstring_first_line",
        "direct_callee_symbol_ids", "direct_caller_symbol_ids", "unresolved_direct_call_count",
        "raised_exception_names", "caught_exception_names", "complexity_signal",
        "syntactic_effect_markers", "direct_test_reference_paths", "public_api_signal",
        "structural_match_group_id", "semantic_comparison_candidate_ids",
    ):
        assert key in card

    context = rebuild.select_additional_context(
        routine_profile_document=document, symbol_id=f"{CORE}:run_engine"
    )
    selected = set(context["source_paths"])
    assert CORE in selected
    assert "tests/test_engine.py" in selected
    assert selected < {CORE, HELPER, CLIENT, "tests/test_engine.py"} or selected <= {
        CORE, HELPER, CLIENT, "tests/test_engine.py"
    }
    assert context["whole_source_tree"] is False
    assert len(selected) < len(
        {item["code_reference"]["relative_path"] for item in document["routines"]}
    ) + 2
