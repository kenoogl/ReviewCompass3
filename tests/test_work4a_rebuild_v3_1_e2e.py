"""Work 4A v3.1設計§13 I1〜I21の受入test。

正本：docs/design/2026-08-04-work-4a-rebuild-design-v3-1-amendment.md
承認：DEC-WORK4A-REBUILD-DESIGN-004
"""

import importlib
import json
import shutil
import types
from pathlib import Path

import pytest


UNIVERSE_ID = "SRCU-WORK4A-TOOLS-PY-V1"
POLICY_ID = "POL-WORK4A-FRESHNESS"
PROJECT_ID = "reviewcompass3"
HEAD_A = "a" * 40
CAPTURED_AT = "2026-08-04T20:00:00+09:00"
GENERATED_AT = "2026-08-05T10:00:00+09:00"

ALPHA = "tools/development/alpha.py:alpha_one"
ALPHA_NESTED = "tools/development/alpha.py:alpha_one.<locals>.inner_helper"
ALPHA_PRIVATE = "tools/development/alpha.py:_alpha_private"
BETA_CLASS = "tools/development/beta.py:BetaError"
BETA_HOLDER = "tools/development/beta.py:BetaHolder"
BETA_METHOD = "tools/development/beta.py:BetaHolder.compute"
BETA_STATIC = "tools/development/beta.py:BetaHolder.build"

ALPHA_SOURCE = '''def alpha_one(document):
    """alphaの入口。"""
    def inner_helper(value):
        return value + 1

    return inner_helper(len(document))


def _alpha_private(path):
    return path.read_text(encoding="utf-8")


DOUBLE = lambda value: value * 2
'''

BETA_SOURCE = '''class BetaError(Exception):
    """betaの失敗。"""


class BetaHolder:
    """betaの保持。"""

    def compute(self, document):
        return len(document)

    @staticmethod
    def build(path):
        return BetaHolder()
'''

COLLIDING_SOURCE = '''def duplicated(flag):
    if flag:
        def worker(value):
            return value
    else:
        def worker(value):
            return value + 1
    return worker
'''


@pytest.fixture
def rebuild():
    return importlib.import_module("tools.development.work4a_rebuild_v3")


def _manifest(project_id):
    return {
        "artifact_roots": {
            "contracts": ".reviewcompass/contracts",
            "design_decisions": ".reviewcompass/design-decisions",
            "policies": ".reviewcompass/policies",
            "reuse": ".reviewcompass/reuse",
        },
        "document_links": [],
        "project_id": project_id,
        "schema_version": 2,
    }


def _project(tmp_path, *, extra_sources=None):
    root = tmp_path / "project"
    (root / "tools" / "development").mkdir(parents=True)
    (root / "docs" / "development").mkdir(parents=True)
    for name in ("contracts", "design-decisions", "policies", "reuse"):
        (root / ".reviewcompass" / name).mkdir(parents=True)
    (root / ".reviewcompass" / "project-manifest.json").write_text(
        json.dumps(_manifest(PROJECT_ID), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / "tools" / "development" / "alpha.py").write_text(ALPHA_SOURCE, encoding="utf-8")
    (root / "tools" / "development" / "beta.py").write_text(BETA_SOURCE, encoding="utf-8")
    for name, text in (extra_sources or {}).items():
        (root / "tools" / "development" / name).write_text(text, encoding="utf-8")
    development = root / "docs" / "development" / "development-policy.md"
    development.write_text("development policy v1\n", encoding="utf-8")
    return root, development


def _profile_chain(rebuild, tmp_path, *, extra_sources=None):
    root, development = _project(tmp_path, extra_sources=extra_sources)
    runtime = tmp_path / "runtime"
    universe = rebuild.write_source_universe(
        project_root=root,
        universe_id=UNIVERSE_ID,
        universe_version=1,
        development_policy_path=development,
    )
    policy = rebuild.write_freshness_policy_v2(
        project_root=root,
        policy_id=POLICY_ID,
        policy_version=2,
        development_policy_path=development,
        change_class="ordinary",
    )
    observation = rebuild.capture_observation(
        project_root=root,
        runtime_root=runtime,
        profile="development",
        universe=universe,
        policy=policy,
        head=HEAD_A,
        tool_version="v3.1",
        captured_at=CAPTURED_AT,
    )
    profile = rebuild.build_routine_profile(observation=observation, policy=policy)
    return types.SimpleNamespace(
        root=root,
        development=development,
        runtime=runtime,
        universe=universe,
        policy=policy,
        observation=observation,
        profile=profile,
    )


def _profile_document(chain):
    return json.loads(chain.profile.path.read_text(encoding="utf-8"))


def _symbol_ids(document):
    return [item["symbol_id"] for item in document["routines"]]


def _proposal_document(chain, *, overrides=None):
    profile = _profile_document(chain)
    document = {
        "record_kind": "work4a_disposition_proposal",
        "schema_version": 1,
        "digest_algorithm": "sha256",
        "advisory": True,
        "proposal_run_id": "0" * 64,
        "routine_profile_run_id": chain.profile.profile_run_id,
        "observation_snapshot_id": chain.observation.snapshot_id,
        "source_content_id": chain.observation.source_content_id,
        "generation_provenance": {
            "provider": "anthropic",
            "model": "claude-opus-5",
            "template_id": "WORK4A-DISPOSITION-PROPOSAL-TEMPLATE",
            "template_version": 1,
            "template_digest": "1" * 64,
            "routine_profile_content_digest": profile["content_digest"],
            "generated_at": GENERATED_AT,
            "output_digest": "2" * 64,
        },
        "proposals": [
            {
                "symbol_id": ALPHA,
                "responsibility_summary": "alphaの入口。",
                "input_summary": "document。",
                "output_summary": "長さに1を足した値。",
                "semantic_dependencies": [ALPHA_NESTED],
                "similar_routines": [],
                "merge_candidates": [],
                "recommended_disposition": "as_is",
                "alternative_dispositions": ["reuse"],
                "confidence": "medium",
                "reason": "入口であり責務は単一。",
                "human_review_point": "nested helperを外に出すかは呼出側次第。",
                "human_review_required": False,
                "evidence_refs": [
                    {
                        "kind": "routine_profile_field",
                        "symbol_id": ALPHA,
                        "field": "internal_reference_count",
                    }
                ],
            }
        ],
        "content_digest": "3" * 64,
    }
    for key, value in (overrides or {}).items():
        document[key] = value
    return document


# I1〜I4：Routine Profile（機械事実のみ）


def test_i1_routine_profile_covers_all_declared_constructs(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _profile_document(chain)
    symbols = _symbol_ids(document)
    for expected in (ALPHA, ALPHA_NESTED, ALPHA_PRIVATE, BETA_CLASS, BETA_HOLDER,
                     BETA_METHOD, BETA_STATIC):
        assert expected in symbols
    kinds = {item["symbol_id"]: item["symbol_kind"] for item in document["routines"]}
    assert kinds[ALPHA] == "function"
    assert kinds[ALPHA_NESTED] == "nested_function"
    assert kinds[BETA_CLASS] == "class"
    assert kinds[BETA_METHOD] == "method"
    assert kinds[BETA_STATIC] == "static_method"
    excluded = {item["construct"]: item for item in document["excluded_constructs"]}
    assert excluded["lambda"]["count"] == 1
    assert excluded["lambda"]["reason"] == "no_stable_identifier"
    assert excluded["lambda"]["locations"]
    assert document["extraction_rule_version"] == 2


def test_i2_marker_detection_flag_must_be_true(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _profile_document(chain)
    assert document["marker_detection"]["absence_does_not_imply_no_effect"] is True
    document["marker_detection"]["absence_does_not_imply_no_effect"] = False
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_routine_profile_document(document, project_root=chain.root)
    assert error.value.code == "marker_detection_flag_missing"


def test_i3_unknown_effect_marker_is_rejected(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _profile_document(chain)
    document["routines"][0]["syntactic_effect_markers"] = ["telepathy"]
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_routine_profile_document(document, project_root=chain.root)
    assert error.value.code == "summary_vocabulary_violation"


def test_i4_llm_field_in_routine_profile_is_rejected(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _profile_document(chain)
    document["routines"][0]["description"] = {"text": "LLMの説明", "source": "llm_generated"}
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_routine_profile_document(document, project_root=chain.root)
    assert error.value.code == "unknown_field"


# I5〜I8：Disposition Proposal（非権威）


def test_i5_non_advisory_proposal_is_rejected(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _proposal_document(chain, overrides={"advisory": False})
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_disposition_proposal_document(
            document, routine_profile_document=_profile_document(chain), policy=chain.policy
        )
    assert error.value.code == "advisory_used_as_authority"


def test_i6_provenance_fields_are_required_and_bound(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    profile_document = _profile_document(chain)

    missing = _proposal_document(chain)
    del missing["generation_provenance"]["template_digest"]
    with pytest.raises(rebuild.V3ValidationError) as first:
        rebuild.validate_disposition_proposal_document(
            missing, routine_profile_document=profile_document, policy=chain.policy
        )
    assert first.value.code == "identity_mismatch"

    mismatched = _proposal_document(chain)
    mismatched["generation_provenance"]["routine_profile_content_digest"] = "9" * 64
    with pytest.raises(rebuild.V3ValidationError) as second:
        rebuild.validate_disposition_proposal_document(
            mismatched, routine_profile_document=profile_document, policy=chain.policy
        )
    assert second.value.code == "content_digest_mismatch"


def test_i7_unresolved_proposal_is_accepted_when_marked(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _proposal_document(chain)
    document["proposals"][0]["recommended_disposition"] = None
    document["proposals"][0]["human_review_required"] = True
    document["proposals"][0]["confidence"] = "low"
    validated = rebuild.validate_disposition_proposal_document(
        document, routine_profile_document=_profile_document(chain), policy=chain.policy
    )
    assert validated["proposals"][0]["recommended_disposition"] is None


def test_i8_proposal_cannot_authorize_entry_disposition(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.build_entry_documents(
            project_root=chain.root,
            policy=chain.policy,
            assignments=(
                {
                    "entry_id": "RRL-ALPHA-ONE",
                    "symbol_id": ALPHA,
                    "responsibility": "alpha",
                    "responsibility_class": "public_responsibility",
                    "disposition": "as_is",
                    "disposition_source": "disposition_proposal",
                    "applied_group_rule_id": None,
                },
            ),
        )
    assert error.value.code == "advisory_used_as_authority"


# I9〜I10：Attestationとの結線


def test_i9_snapshot_mismatch_stops(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _profile_document(chain)
    document["observation_snapshot_id"] = "4" * 64
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_attestation_sections(
            attestation_snapshot_id=chain.observation.snapshot_id,
            routine_profile_document=document,
            disposition_proposal_document=None,
        )
    assert error.value.code == "unlinked_candidate"


def test_i10_missing_external_records_do_not_block_current(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    candidates = rebuild.build_candidate_run(observation=chain.observation)
    attestation = rebuild.write_attestation(
        project_root=chain.root,
        observation=chain.observation,
        candidates=candidates,
        routine_profile=chain.profile,
    )
    decision = rebuild.write_operational_decision(
        project_root=chain.root,
        decision_id="DEC-WORK4A-OPS-101",
        attestation=attestation,
        approved_targets=({"symbol_id": ALPHA, "disposition": "as_is"},),
        human_id="kenoogl",
        decided_at=GENERATED_AT,
    )
    baseline = rebuild.append_baseline(
        project_root=chain.root,
        attestation=attestation,
        decision=decision,
        policy=chain.policy,
        universe=chain.universe,
        entries=(
            {
                "entry_id": "RRL-ALPHA-ONE",
                "symbol_id": ALPHA,
                "responsibility": "alpha",
                "side_effects": "none",
                "disposition": "as_is",
            },
        ),
        relations=(),
        prior=None,
    )
    assert baseline.baseline_version == 1
    document = json.loads(attestation.path.read_text(encoding="utf-8"))
    assert document["schema_version"] == 2
    assert document["routine_profile"]["profile_run_id"] == chain.profile.profile_run_id

    shutil.rmtree(chain.runtime)
    state = rebuild.validate_current(
        project_root=chain.root, runtime_root=chain.runtime, profile="development"
    )
    assert state.baseline_version == 1
    assert "locator_unresolved" in state.annotations


# I11〜I13：group判断


def test_i11_uncovered_routine_stops_expansion(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.expand_group_rules(
            routine_profile_document=_profile_document(chain),
            policy=chain.policy,
            group_rules=(
                {
                    "group_rule_id": "GRP-CLASS",
                    "conditions": [
                        {"field": "symbol_kind", "operator": "equals", "value": "class"}
                    ],
                    "responsibility_class": "ownership_unclear",
                    "disposition": "as_is",
                },
            ),
            explicit_targets=(),
        )
    assert error.value.code == "group_coverage_incomplete"


def test_i12_expansion_records_group_rule_id(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    assignments = rebuild.expand_group_rules(
        routine_profile_document=_profile_document(chain),
        policy=chain.policy,
        group_rules=(
            {
                "group_rule_id": "GRP-ALL",
                "conditions": [
                    {"field": "candidate_classification", "operator": "equals", "value": "unknown"}
                ],
                "responsibility_class": "ownership_unclear",
                "disposition": "as_is",
            },
        ),
        explicit_targets=(
            {
                "symbol_id": ALPHA,
                "responsibility_class": "public_responsibility",
                "disposition": "reuse",
            },
        ),
    )
    by_symbol = {item["symbol_id"]: item for item in assignments}
    assert by_symbol[ALPHA]["applied_group_rule_id"] is None
    assert by_symbol[ALPHA]["disposition"] == "reuse"
    assert by_symbol[BETA_CLASS]["applied_group_rule_id"] == "GRP-ALL"
    assert all(item["disposition_source"] == "human_decision" for item in assignments)


def test_i13_human_value_overrides_machine_proposal(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    document = _profile_document(chain)
    proposals = {item["symbol_id"]: item["responsibility_class_proposal"]
                 for item in document["routines"]}
    assert proposals[BETA_CLASS] == "ownership_unclear"
    assert proposals[ALPHA_NESTED] == "implementation_detail"
    assignments = rebuild.expand_group_rules(
        routine_profile_document=document,
        policy=chain.policy,
        group_rules=(
            {
                "group_rule_id": "GRP-ALL",
                "conditions": [
                    {"field": "candidate_classification", "operator": "equals", "value": "unknown"}
                ],
                "responsibility_class": "public_responsibility",
                "disposition": "as_is",
            },
        ),
        explicit_targets=(),
    )
    by_symbol = {item["symbol_id"]: item for item in assignments}
    assert by_symbol[BETA_CLASS]["responsibility_class"] == "public_responsibility"


# I14〜I16：抽出規則と構造一致


def test_i14_rule_v2_creates_new_candidate_run(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    first = rebuild.build_candidate_run(observation=chain.observation)
    second = rebuild.build_candidate_run(
        observation=chain.observation, extraction_rule_version=2
    )
    assert first.candidate_run_id != second.candidate_run_id
    assert first.path.exists() and second.path.exists()
    assert json.loads(first.path.read_text(encoding="utf-8"))["candidate_run_id"] == first.candidate_run_id


def test_i15_schema_version_one_attestation_is_readable(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    candidates = rebuild.build_candidate_run(observation=chain.observation)
    attestation = rebuild.write_attestation(
        project_root=chain.root, observation=chain.observation, candidates=candidates
    )
    document = json.loads(attestation.path.read_text(encoding="utf-8"))
    assert document["schema_version"] == 1
    assert "routine_profile" not in document
    policy_document = json.loads(chain.policy.path.read_text(encoding="utf-8"))
    rebuild.validate_attestation_document(
        document,
        project_id=PROJECT_ID,
        disposition_classes=policy_document["disposition_classes"],
    )


def test_i16_structural_match_group_is_shared_by_identical_structure(rebuild, tmp_path):
    twin = '''def twin_one(value):
    return value + 1


def twin_two(other):
    return other + 1
'''
    chain = _profile_chain(rebuild, tmp_path, extra_sources={"twin.py": twin})
    document = _profile_document(chain)
    groups = {item["symbol_id"]: item["structural_match_group_id"]
              for item in document["routines"]}
    digests = {item["symbol_id"]: item["structure_digest"] for item in document["routines"]}
    one = "tools/development/twin.py:twin_one"
    two = "tools/development/twin.py:twin_two"
    assert digests[one] == digests[two]
    assert groups[one] == groups[two]
    assert groups[one] != groups[ALPHA]


# I17：symbol_id重複


def test_i17_symbol_id_collision_stops(rebuild, tmp_path):
    with pytest.raises(Exception) as error:
        _profile_chain(rebuild, tmp_path, extra_sources={"collide.py": COLLIDING_SOURCE})
    assert getattr(error.value, "code", None) == "symbol_id_collision"
    detail = getattr(error.value, "detail", "")
    assert "worker" in detail
    assert detail.count("collide.py") >= 2


# I18〜I21：参照範囲と根拠


def test_i18_out_of_scope_reference_stops(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    profile_document = _profile_document(chain)

    unknown = _proposal_document(chain)
    unknown["proposals"][0]["similar_routines"] = ["tools/development/ghost.py:missing"]
    with pytest.raises(rebuild.V3ValidationError) as first:
        rebuild.validate_disposition_proposal_document(
            unknown, routine_profile_document=profile_document, policy=chain.policy
        )
    assert first.value.code == "advisory_reference_unresolved"

    self_reference = _proposal_document(chain)
    self_reference["proposals"][0]["merge_candidates"] = [ALPHA]
    with pytest.raises(rebuild.V3ValidationError) as second:
        rebuild.validate_disposition_proposal_document(
            self_reference, routine_profile_document=profile_document, policy=chain.policy
        )
    assert second.value.code == "advisory_reference_unresolved"


def test_i19_missing_evidence_stops(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    profile_document = _profile_document(chain)

    empty = _proposal_document(chain)
    empty["proposals"][0]["evidence_refs"] = []
    with pytest.raises(rebuild.V3ValidationError) as first:
        rebuild.validate_disposition_proposal_document(
            empty, routine_profile_document=profile_document, policy=chain.policy
        )
    assert first.value.code == "advisory_evidence_missing"

    unknown_kind = _proposal_document(chain)
    unknown_kind["proposals"][0]["evidence_refs"] = [{"kind": "hunch", "symbol_id": ALPHA}]
    with pytest.raises(rebuild.V3ValidationError) as second:
        rebuild.validate_disposition_proposal_document(
            unknown_kind, routine_profile_document=profile_document, policy=chain.policy
        )
    assert second.value.code == "advisory_evidence_missing"


def test_i20_code_reference_mismatch_stops(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    profile_document = _profile_document(chain)
    reference = next(
        item["code_reference"] for item in profile_document["routines"]
        if item["symbol_id"] == ALPHA
    )
    document = _proposal_document(chain)
    document["proposals"][0]["evidence_refs"] = [
        {
            "kind": "code_reference",
            "symbol_id": ALPHA,
            "relative_path": reference["relative_path"],
            "start_line": reference["start_line"] + 5,
            "end_line": reference["end_line"],
        }
    ]
    with pytest.raises(rebuild.V3ValidationError) as error:
        rebuild.validate_disposition_proposal_document(
            document, routine_profile_document=profile_document, policy=chain.policy
        )
    assert error.value.code == "advisory_reference_unresolved"


def test_i21_valid_code_reference_evidence_is_accepted(rebuild, tmp_path):
    chain = _profile_chain(rebuild, tmp_path)
    profile_document = _profile_document(chain)
    reference = next(
        item["code_reference"] for item in profile_document["routines"]
        if item["symbol_id"] == ALPHA
    )
    document = _proposal_document(chain)
    document["proposals"][0]["evidence_refs"] = [
        {
            "kind": "code_reference",
            "symbol_id": ALPHA,
            "relative_path": reference["relative_path"],
            "start_line": reference["start_line"],
            "end_line": reference["end_line"],
        }
    ]
    validated = rebuild.validate_disposition_proposal_document(
        document, routine_profile_document=profile_document, policy=chain.policy
    )
    assert validated["proposals"][0]["evidence_refs"][0]["kind"] == "code_reference"
