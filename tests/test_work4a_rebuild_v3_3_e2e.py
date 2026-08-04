"""Work 4A v3.3設計§9 K1〜K12の受入test。

正本：docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md
承認：DEC-WORK4A-REBUILD-DESIGN-006
参照方向：Comparison Discovery → Routine Profileの一方向だけ。
"""

import importlib
import json
import types
from pathlib import Path

import pytest


UNIVERSE_ID = "SRCU-WORK4A-TOOLS-PY-V1"
POLICY_ID = "POL-WORK4A-FRESHNESS"
PROJECT_ID = "reviewcompass3"
HEAD_A = "a" * 40
CAPTURED_AT = "2026-08-05T12:00:00+09:00"

CORE = "tools/core/engine.py"
HELPER = "tools/core/helper.py"
CLIENT = "tools/client/runner.py"

CORE_SOURCE = '''"""engine."""


class EngineError(Exception):
    """engineの失敗。"""


def run_engine(document):
    """engineを実行する。"""
    if not document:
        raise EngineError("empty")
    return normalize(document)


def normalize(document):
    return document.strip()


def compact(document):
    return document.strip()
'''

HELPER_SOURCE = '''def normalize_text(document):
    return document.strip()


def guard(value):
    try:
        return int(value)
    except ValueError:
        raise EngineError("bad")


def relay(document):
    return normalize(document)
'''

CLIENT_SOURCE = '''from tools.core import engine


def main(document):
    if not document:
        raise EngineError("empty")
    return engine.run_engine(document)


def secondary(document):
    return engine.run_engine(document)
'''

TEST_SOURCE = '''from tools.core.engine import run_engine, normalize


def test_engine():
    assert run_engine("x") == normalize("x")
'''


@pytest.fixture
def rebuild():
    return importlib.import_module("tools.development.work4a_rebuild_v3")


def _project(tmp_path):
    root = tmp_path / "project"
    (root / "tools" / "core").mkdir(parents=True)
    (root / "tools" / "client").mkdir(parents=True)
    (root / "tests").mkdir(parents=True)
    (root / "docs" / "development").mkdir(parents=True)
    for name in ("contracts", "design-decisions", "policies", "reuse"):
        (root / ".reviewcompass" / name).mkdir(parents=True)
    (root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(
            {
                "artifact_roots": {
                    "contracts": ".reviewcompass/contracts",
                    "design_decisions": ".reviewcompass/design-decisions",
                    "policies": ".reviewcompass/policies",
                    "reuse": ".reviewcompass/reuse",
                },
                "document_links": [],
                "project_id": PROJECT_ID,
                "schema_version": 2,
            },
            ensure_ascii=False, indent=2, sort_keys=True,
        ) + "\n",
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
    policy = rebuild.write_freshness_policy_v4(
        project_root=root, policy_id=POLICY_ID, policy_version=4,
        development_policy_path=development, change_class="ordinary",
    )
    observation = rebuild.capture_observation(
        project_root=root, runtime_root=runtime, profile="development",
        universe=universe, policy=policy, head=HEAD_A, tool_version="v3.3",
        captured_at=CAPTURED_AT,
    )
    profile = rebuild.build_routine_profile_v3(observation=observation, policy=policy)
    discovery = rebuild.build_comparison_discovery(
        observation=observation, routine_profile=profile, policy=policy
    )
    return types.SimpleNamespace(
        root=root, development=development, runtime=runtime, universe=universe,
        policy=policy, observation=observation, profile=profile, discovery=discovery,
    )


def _documents(chain):
    profile = json.loads(chain.profile.path.read_text(encoding="utf-8"))
    discovery = json.loads(chain.discovery.path.read_text(encoding="utf-8"))
    return profile, discovery


# K1：groupは同一Profile内のmemberだけを持ち、全memberを切り捨てない


def test_k1_groups_hold_all_members_from_the_same_profile(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)
    known = {item["symbol_id"] for item in profile["routines"]}
    assert discovery["schema_version"] == 1
    assert discovery["routine_profile_run_id"] == profile["profile_run_id"]
    assert discovery["routine_profile_content_digest"] == profile["content_digest"]
    assert discovery["source_content_id"] == profile["source_content_id"]
    assert discovery["groups"]
    for group in discovery["groups"]:
        assert set(group["member_symbol_ids"]) <= known
        assert group["member_symbol_ids"] == sorted(group["member_symbol_ids"])
        assert group["member_count"] == len(group["member_symbol_ids"])
        assert group["member_count"] >= 2


def test_k1_member_outside_profile_is_rejected(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)
    discovery["groups"][0]["member_symbol_ids"] = ["tools/ghost.py:missing"]
    discovery["groups"][0]["member_count"] = 1
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_comparison_discovery_document(
            discovery, routine_profile_document=profile, policy=chain.policy
        )
    assert error.value.code in ("profile_reference_unresolved", "member_truncation_detected")


# K2：代表は最大3件、memberは全件保持


def test_k2_representatives_are_capped_without_truncating_members(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)
    for group in discovery["groups"]:
        assert len(group["representative_symbol_ids"]) <= 3
        assert set(group["representative_symbol_ids"]) <= set(group["member_symbol_ids"])
        assert group["representative_symbol_ids"] == sorted(group["representative_symbol_ids"])

    tampered = json.loads(json.dumps(discovery))
    group = tampered["groups"][0]
    group["member_symbol_ids"] = group["member_symbol_ids"][:1]
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_comparison_discovery_document(
            tampered, routine_profile_document=profile, policy=chain.policy
        )
    assert error.value.code == "member_truncation_detected"


# K3：一routineが複数の根拠groupへ所属できる


def test_k3_routine_can_belong_to_multiple_bases(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    _profile, discovery = _documents(chain)
    membership = {}
    for group in discovery["groups"]:
        for member in group["member_symbol_ids"]:
            membership.setdefault(member, set()).add(group["basis_kind"])
    assert any(len(kinds) >= 2 for kinds in membership.values())
    assert f"{CORE}:normalize" in membership


# K4：同一package・同じ引数個数だけではgroupを作らない


def test_k4_package_or_arity_alone_does_not_form_a_group(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    _profile, discovery = _documents(chain)
    allowed = set(rebuild.BASIS_KINDS)
    for group in discovery["groups"]:
        assert group["basis_kind"] in allowed
        assert group["basis_kind"] not in ("same_package", "same_parameter_count")
        evidence = group["basis_evidence"]
        assert set(evidence) - {"package", "parameter_count"}


def test_k4_unknown_basis_kind_is_rejected(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)
    discovery["groups"][0]["basis_kind"] = "same_package"
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_comparison_discovery_document(
            discovery, routine_profile_document=profile, policy=chain.policy
        )
    assert error.value.code == "summary_vocabulary_violation"


# K5：各basis_kindの根拠と限界をrecordへ保持する


def test_k5_basis_evidence_and_limits_are_recorded(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    _profile, discovery = _documents(chain)
    kinds = {group["basis_kind"] for group in discovery["groups"]}
    assert "structural_exact_match" in kinds
    assert "shared_exception_contract" in kinds
    assert "shared_test_reference" in kinds
    for group in discovery["groups"]:
        assert group["basis_evidence"]
        assert group["is_semantic_conclusion"] is False
        assert group["basis_limitation"]
    limits = discovery["basis_limitations"]
    for kind in rebuild.BASIS_KINDS:
        assert kind in limits


# K6：presentation classを決定的に付ける


def test_k6_presentation_class_is_deterministic(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)
    for group in discovery["groups"]:
        count = group["member_count"]
        expected = "focused" if count <= 12 else "broad" if count <= 50 else "mass"
        assert group["presentation_class"] == expected

    again = rebuild.build_comparison_discovery(
        observation=chain.observation, routine_profile=chain.profile, policy=chain.policy
    )
    assert again.discovery_run_id == chain.discovery.discovery_run_id

    discovery["groups"][0]["presentation_class"] = "narrow"
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_comparison_discovery_document(
            discovery, routine_profile_document=profile, policy=chain.policy
        )
    assert error.value.code == "summary_vocabulary_violation"


# K7：構造一致groupやDiscovery groupだけからmergeを確定できない


def test_k7_discovery_never_concludes_merge(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    _profile, discovery = _documents(chain)
    assert discovery["is_semantic_conclusion"] is False
    assert discovery["produces_disposition"] is False
    serialized = json.dumps(discovery, ensure_ascii=False)
    assert '"disposition"' not in serialized
    assert '"recommended_disposition"' not in serialized
    for group in discovery["groups"]:
        assert "disposition" not in group


# K8：Profile digest・source content ID不一致を拒否する


def test_k8_profile_mismatch_is_rejected(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)

    digest_mismatch = json.loads(json.dumps(discovery))
    digest_mismatch["routine_profile_content_digest"] = "0" * 64
    with pytest.raises(rebuild.V3ValidationError) as first:
        rebuild.validate_comparison_discovery_document(
            digest_mismatch, routine_profile_document=profile, policy=chain.policy
        )
    assert first.value.code == "discovery_profile_mismatch"

    source_mismatch = json.loads(json.dumps(discovery))
    source_mismatch["source_content_id"] = "1" * 64
    with pytest.raises(rebuild.V3ValidationError) as second:
        rebuild.validate_comparison_discovery_document(
            source_mismatch, routine_profile_document=profile, policy=chain.policy
        )
    assert second.value.code == "discovery_profile_mismatch"

    run_mismatch = json.loads(json.dumps(discovery))
    run_mismatch["routine_profile_run_id"] = "2" * 64
    with pytest.raises(rebuild.V3ValidationError) as third:
        rebuild.validate_comparison_discovery_document(
            run_mismatch, routine_profile_document=profile, policy=chain.policy
        )
    assert third.value.code == "discovery_profile_mismatch"


# K9：bounded seedを根拠に使おうとすると拒否する


def test_k9_bounded_seed_cannot_be_a_basis(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, _discovery = _documents(chain)
    for routine in profile["routines"]:
        assert "semantic_comparison_candidate_ids" not in routine
        assert "semantic_candidate_selection_reason" not in routine

    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.reject_bounded_seed_basis(
            [
                {
                    "kind": "routine_profile_field",
                    "symbol_id": f"{CORE}:normalize",
                    "field": "semantic_comparison_candidate_ids",
                }
            ],
            policy=chain.policy,
        )
    assert error.value.code == "bounded_seed_not_a_basis"


def test_k9_profile_v3_must_not_reference_discovery(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, _discovery = _documents(chain)
    assert "comparison_discovery_ref" not in profile
    assert "comparison_discovery_run_id" not in profile
    for routine in profile["routines"]:
        assert "comparison_discovery_ref" not in routine

    profile["comparison_discovery_ref"] = {"discovery_run_id": "3" * 64}
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_routine_profile_v3_document(profile, policy=chain.policy)
    assert error.value.code == "unknown_field"


# K10：LLMの初期入力は判断カードとgroup要約だけ


def test_k10_initial_llm_input_has_no_source_bodies(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)
    payload = rebuild.build_llm_initial_input(
        routine_profile_document=profile,
        comparison_discovery_document=discovery,
        symbol_id=f"{CORE}:normalize",
    )
    assert set(payload) == {"decision_card", "comparison_groups", "whole_source_tree",
                            "includes_source_body"}
    assert payload["whole_source_tree"] is False
    assert payload["includes_source_body"] is False
    for group in payload["comparison_groups"]:
        assert set(group) == {
            "group_id", "basis_kind", "basis_evidence", "basis_limitation",
            "member_count", "presentation_class", "representative_symbol_ids",
            "member_record_reference",
        }
        assert len(group["representative_symbol_ids"]) <= 3
        assert "member_symbol_ids" not in group


# K11：追加読込はgroup、理由、symbol IDをprovenanceへ残す


def test_k11_additional_read_requires_provenance(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile, discovery = _documents(chain)
    group_id = discovery["groups"][0]["group_id"]
    provenance = rebuild.record_additional_read(
        routine_profile_document=profile,
        comparison_discovery_document=discovery,
        symbol_id=f"{CORE}:normalize",
        group_ids=[group_id],
        reason="focused groupの責務差を確認する",
    )
    assert provenance["group_ids"] == [group_id]
    assert provenance["reason"]
    assert provenance["symbol_ids"]
    assert provenance["whole_source_tree"] is False
    assert all(path.startswith("tools/") or path.startswith("tests/")
               for path in provenance["source_paths"])

    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.record_additional_read(
            routine_profile_document=profile,
            comparison_discovery_document=discovery,
            symbol_id=f"{CORE}:normalize",
            group_ids=[group_id],
            reason="",
        )
    assert error.value.code == "advisory_evidence_missing"

    with pytest.raises(rebuild.V3ValidationError) as unknown:
        rebuild.record_additional_read(
            routine_profile_document=profile,
            comparison_discovery_document=discovery,
            symbol_id=f"{CORE}:normalize",
            group_ids=["CG-UNKNOWN-9999"],
            reason="範囲外group",
        )
    assert unknown.value.code == "profile_reference_unresolved"


# K12：Profile v2、Profile v3、Discoveryを併存させ、いずれも書き換えない


def test_k12_profiles_and_discovery_coexist(rebuild, tmp_path):
    chain = _chain(rebuild, tmp_path)
    profile_v2 = rebuild.build_routine_profile_v2(
        observation=chain.observation, policy=chain.policy
    )
    v2_bytes = profile_v2.path.read_bytes()
    v3_bytes = chain.profile.path.read_bytes()
    discovery_bytes = chain.discovery.path.read_bytes()

    assert profile_v2.path != chain.profile.path != chain.discovery.path
    again = rebuild.build_routine_profile_v3(observation=chain.observation, policy=chain.policy)
    assert again.path == chain.profile.path
    assert chain.profile.path.read_bytes() == v3_bytes
    assert profile_v2.path.read_bytes() == v2_bytes
    assert chain.discovery.path.read_bytes() == discovery_bytes

    v2_document = json.loads(profile_v2.path.read_text(encoding="utf-8"))
    v3_document = json.loads(chain.profile.path.read_text(encoding="utf-8"))
    assert v2_document["schema_version"] == 2
    assert v3_document["schema_version"] == 3
    assert v3_document["extraction_rule_version"] == 4
    assert "semantic_comparison_candidate_ids" in v2_document["routines"][0]
    rebuild.validate_routine_profile_v3_document(v3_document, policy=chain.policy)
