"""RQ1（Contract completeness）計測装置。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

作業票：docs/development/2026-08-17-rq1-apparatus-work-ticket-v1.md（§4の指標定義を実装する）。
既存task_contract部品（bind・build・compile・coverage）を読み取り専用で呼び、指標を機械集計
する。新しい検証ロジックは持たない（改竄検出はcommonのcanonical_content_digest照合を使う）。
"""

import argparse
import json
from pathlib import Path

from tools.common.digests import canonical_content_digest
from tools.task_contract import contract as contract_module

CONTRACT_ID = "TC-RQ1-FIXTURE"
TARGET = "docs/review-target.md"
COMPILE_REPETITIONS = 3

CLEAN_DOCUMENT = "# 見出し\n\n## 目的\n\n本文である。\n"
ALT_DOCUMENT = "# 別見出し\n\n## 別目的\n\n別の本文である。\n"

_FULL_REQUIREMENTS = tuple(sorted(contract_module.REQUIREMENT_OBLIGATIONS))
_PARTIAL_REQUIREMENTS = _FULL_REQUIREMENTS[:8]
_UNKNOWN_REQUIREMENT = "REQ-NOPE-001"

# 契約の義務欄→Plan viewの静的写像（_plan_viewsのコード構造の対応表。
# obligation_to_plan_coverage＝viewへ値が渡った欄÷全欄）。
_OBLIGATION_PLAN_MAP = (
    ("boundary", "context_acquisition", "target_paths"),
    ("context_obligations", "context_acquisition", "material_roles"),
    ("responsibility", "review_execution", "reviewer"),
    ("allowed_capabilities", "harness_and_capability", None),
    ("acceptance", "verification", "conformance_owner"),
    ("provenance_obligations", "provenance_capture", "capture_plan"),
    ("escalation", "human_interaction", "decision_owner"),
)


def _canonical_bytes(document):
    return json.dumps(
        document, ensure_ascii=False, sort_keys=True
    ).encode("utf-8")


def _reason(error):
    return "%s:%s" % (type(error).__name__, error)


def _write_definition(root, requirement_id, *, version=1):
    path = root / "records" / "requirements" / "definitions" / (
        "%s--v1.json" % requirement_id.lower()
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "artifact_kind": "requirement_definition",
                "requirement_id": requirement_id,
                "requirement_version": version,
                "statement": "%sの固定文" % requirement_id,
            },
            ensure_ascii=False, sort_keys=True, indent=2,
        ) + "\n",
        encoding="utf-8",
    )


def _project(
    base_dir,
    name,
    *,
    definition_ids,
    body=CLEAN_DOCUMENT,
    make_definitions_dir=True,
):
    root = Path(base_dir) / name / "project"
    (root / "docs").mkdir(parents=True)
    (root / TARGET).write_text(body, encoding="utf-8")
    if make_definitions_dir:
        (root / "records" / "requirements" / "definitions").mkdir(
            parents=True
        )
        for requirement_id in definition_ids:
            _write_definition(root, requirement_id)
    return root


def _obligation_plan_coverage(contract_document, plan_bundle):
    views = plan_bundle["views"]
    mapped = 0
    for section, view_name, view_key in _OBLIGATION_PLAN_MAP:
        if not contract_document.get(section):
            continue
        view = views.get(view_name)
        if not view:
            continue
        if view_key is None or view.get(view_key):
            mapped += 1
    return mapped / len(_OBLIGATION_PLAN_MAP)


def _observe_chain(
    name,
    group,
    root,
    requirement_ids,
    *,
    allow_unreceived=False,
    mutate_contract=None,
    full_binding=False,
):
    observation = {"name": name, "group": group}
    try:
        binding = contract_module.bind_requirements(
            project_root=root,
            requirement_ids=requirement_ids,
            allow_unreceived=allow_unreceived,
        )
    except Exception as error:
        observation.update(
            {"outcome": "stopped", "stage": "bind", "reason": _reason(error)}
        )
        return observation
    try:
        built = contract_module.build_review_task_contract(
            contract_id=CONTRACT_ID,
            contract_version=1,
            requirement_binding=binding,
            target_paths=(TARGET,),
        )
    except Exception as error:
        observation.update(
            {"outcome": "stopped", "stage": "build", "reason": _reason(error)}
        )
        return observation
    contract_document = (
        built if mutate_contract is None else mutate_contract(dict(built))
    )
    verdicts = []
    try:
        for _ in range(COMPILE_REPETITIONS):
            verdicts.append(
                contract_module.compile_contract(
                    contract=contract_document,
                    requirement_binding=binding,
                )
            )
    except Exception as error:
        observation.update(
            {
                "outcome": "stopped",
                "stage": "compile",
                "reason": _reason(error),
            }
        )
        return observation
    first = verdicts[0]
    observation["regeneration"] = {
        "repetitions": COMPILE_REPETITIONS,
        "byte_identical": all(
            _canonical_bytes(verdict) == _canonical_bytes(first)
            for verdict in verdicts[1:]
        ),
    }
    if first.get("status") != "compiled":
        observation.update(
            {
                "outcome": "blocking",
                "stage": "compile",
                "reason": str(first.get("reason")),
            }
        )
        return observation
    coverage = contract_module.check_requirement_coverage(
        contract=contract_document, requirement_binding=binding
    )
    observation["outcome"] = "succeeded"
    if full_binding:
        received = len(_FULL_REQUIREMENTS) - len(
            coverage["unreceived_requirement_ids"]
        )
        observation["requirement_to_obligation_coverage"] = (
            received / len(_FULL_REQUIREMENTS)
        )
    observation["obligation_to_plan_coverage"] = _obligation_plan_coverage(
        contract_document, first["plan_bundle"]
    )
    return observation


def _seal_tamper_observation(name, group, root, requirement_ids, *, field):
    observation = {"name": name, "group": group}
    binding = contract_module.bind_requirements(
        project_root=root, requirement_ids=requirement_ids
    )
    built = contract_module.build_review_task_contract(
        contract_id=CONTRACT_ID,
        contract_version=1,
        requirement_binding=binding,
        target_paths=(TARGET,),
    )
    if field == "binding":
        tampered = dict(binding)
        tampered["requirements"] = list(tampered["requirements"])[:-1]
    else:
        tampered = dict(built)
        tampered["responsibility"] = {"goal": "改竄された目標"}
    intact = (
        canonical_content_digest(tampered) == tampered.get("content_digest")
    )
    observation.update(
        {
            "outcome": "succeeded" if intact else "blocking",
            "stage": "seal_verification",
            "reason": "content_digest_mismatch" if not intact else "",
        }
    )
    return observation


def _rebind_drift_observation(name, group, root, requirement_ids):
    observation = {"name": name, "group": group}
    first = contract_module.bind_requirements(
        project_root=root, requirement_ids=requirement_ids
    )
    _write_definition(root, requirement_ids[0], version=2)
    second = contract_module.bind_requirements(
        project_root=root, requirement_ids=requirement_ids
    )
    drift = _canonical_bytes(first) != _canonical_bytes(second)
    observation.update(
        {
            "outcome": "blocking" if drift else "succeeded",
            "stage": "rebind_comparison",
            "reason": "binding_drift" if drift else "",
        }
    )
    return observation


def _fixture_normal_full(base_dir):
    root = _project(
        base_dir, "normal-full-binding", definition_ids=_FULL_REQUIREMENTS
    )
    return _observe_chain(
        "normal-full-binding",
        "normal",
        root,
        _FULL_REQUIREMENTS,
        full_binding=True,
    )


def _fixture_normal_partial(base_dir):
    root = _project(
        base_dir,
        "normal-partial-binding",
        definition_ids=_PARTIAL_REQUIREMENTS,
    )
    return _observe_chain(
        "normal-partial-binding", "normal", root, _PARTIAL_REQUIREMENTS
    )


def _fixture_normal_alt_document(base_dir):
    root = _project(
        base_dir,
        "normal-alt-document",
        definition_ids=_FULL_REQUIREMENTS,
        body=ALT_DOCUMENT,
    )
    return _observe_chain(
        "normal-alt-document", "normal", root, _FULL_REQUIREMENTS
    )


def _fixture_missing_definition(base_dir):
    definition_ids = _FULL_REQUIREMENTS[1:]
    root = _project(
        base_dir, "missing-definition-file", definition_ids=definition_ids
    )
    return _observe_chain(
        "missing-definition-file", "missing", root, _FULL_REQUIREMENTS
    )


def _fixture_missing_definitions_dir(base_dir):
    root = _project(
        base_dir,
        "missing-definitions-directory",
        definition_ids=(),
        make_definitions_dir=False,
    )
    return _observe_chain(
        "missing-definitions-directory", "missing", root, _FULL_REQUIREMENTS
    )


def _fixture_missing_contract_section(base_dir):
    root = _project(
        base_dir,
        "missing-contract-section",
        definition_ids=_FULL_REQUIREMENTS,
    )

    def _drop_section(document):
        document["acceptance"] = {}
        return document

    return _observe_chain(
        "missing-contract-section",
        "missing",
        root,
        _FULL_REQUIREMENTS,
        mutate_contract=_drop_section,
    )


def _fixture_conflict_unknown(base_dir):
    definition_ids = _FULL_REQUIREMENTS + (_UNKNOWN_REQUIREMENT,)
    root = _project(
        base_dir, "conflict-unknown-requirement", definition_ids=definition_ids
    )
    return _observe_chain(
        "conflict-unknown-requirement",
        "conflict",
        root,
        definition_ids,
    )


def _fixture_conflict_unknown_allowed(base_dir):
    definition_ids = _FULL_REQUIREMENTS + (_UNKNOWN_REQUIREMENT,)
    root = _project(
        base_dir,
        "conflict-unknown-allowed",
        definition_ids=definition_ids,
    )
    return _observe_chain(
        "conflict-unknown-allowed",
        "conflict",
        root,
        definition_ids,
        allow_unreceived=True,
    )


def _fixture_conflict_orphan(base_dir):
    root = _project(
        base_dir,
        "conflict-orphan-obligation",
        definition_ids=_FULL_REQUIREMENTS,
    )

    def _inject_orphan(document):
        document["context_obligations"] = list(
            document["context_obligations"]
        ) + ["OBL-NOPE"]
        return document

    return _observe_chain(
        "conflict-orphan-obligation",
        "conflict",
        root,
        _FULL_REQUIREMENTS,
        mutate_contract=_inject_orphan,
    )


def _fixture_stale_binding_tamper(base_dir):
    root = _project(
        base_dir,
        "stale-binding-tamper",
        definition_ids=_FULL_REQUIREMENTS,
    )
    return _seal_tamper_observation(
        "stale-binding-tamper",
        "stale",
        root,
        _FULL_REQUIREMENTS,
        field="binding",
    )


def _fixture_stale_contract_tamper(base_dir):
    root = _project(
        base_dir,
        "stale-contract-tamper",
        definition_ids=_FULL_REQUIREMENTS,
    )
    return _seal_tamper_observation(
        "stale-contract-tamper",
        "stale",
        root,
        _FULL_REQUIREMENTS,
        field="contract",
    )


def _fixture_stale_definition_rewrite(base_dir):
    root = _project(
        base_dir,
        "stale-definition-rewrite",
        definition_ids=_FULL_REQUIREMENTS,
    )
    return _rebind_drift_observation(
        "stale-definition-rewrite",
        "stale",
        root,
        _FULL_REQUIREMENTS,
    )


_FIXTURES = (
    ("normal-full-binding", "normal", _fixture_normal_full),
    ("normal-partial-binding", "normal", _fixture_normal_partial),
    ("normal-alt-document", "normal", _fixture_normal_alt_document),
    ("missing-definition-file", "missing", _fixture_missing_definition),
    (
        "missing-definitions-directory",
        "missing",
        _fixture_missing_definitions_dir,
    ),
    ("missing-contract-section", "missing", _fixture_missing_contract_section),
    ("conflict-unknown-requirement", "conflict", _fixture_conflict_unknown),
    ("conflict-unknown-allowed", "conflict", _fixture_conflict_unknown_allowed),
    ("conflict-orphan-obligation", "conflict", _fixture_conflict_orphan),
    ("stale-binding-tamper", "stale", _fixture_stale_binding_tamper),
    ("stale-contract-tamper", "stale", _fixture_stale_contract_tamper),
    ("stale-definition-rewrite", "stale", _fixture_stale_definition_rewrite),
)

_NEGATIVE_GROUPS = ("missing", "conflict", "stale")


def fixture_registry():
    return tuple((name, group) for name, group, _ in _FIXTURES)


def run_fixture(name, base_dir):
    for fixture_name, _, builder in _FIXTURES:
        if fixture_name == name:
            return builder(base_dir)
    raise KeyError("unknown fixture: %s" % name)


def aggregate_metrics(observations):
    normals = [
        item for item in observations if item.get("group") == "normal"
    ]
    negatives = [
        item
        for item in observations
        if item.get("group") in _NEGATIVE_GROUPS
    ]
    regenerations = [
        item for item in observations if "regeneration" in item
    ]
    coverage_values = [
        item["requirement_to_obligation_coverage"]
        for item in observations
        if "requirement_to_obligation_coverage" in item
    ]
    plan_values = [
        item["obligation_to_plan_coverage"]
        for item in observations
        if "obligation_to_plan_coverage" in item
    ]

    def _rate(numerator, denominator):
        return (numerator / denominator) if denominator else None

    return {
        "requirement_to_obligation_coverage": (
            max(coverage_values) if coverage_values else None
        ),
        "obligation_to_plan_coverage": (
            max(plan_values) if plan_values else None
        ),
        "regeneration_match_rate": _rate(
            sum(
                1
                for item in regenerations
                if item["regeneration"]["byte_identical"]
            ),
            len(regenerations),
        ),
        "negative_detection_rate": _rate(
            sum(
                1
                for item in negatives
                if item.get("outcome") in ("stopped", "blocking")
            ),
            len(negatives),
        ),
        "false_stop_rate": _rate(
            sum(
                1
                for item in normals
                if item.get("outcome") != "succeeded"
            ),
            len(normals),
        ),
    }


def collect(base_dir):
    observations = [builder(base_dir) for _, _, builder in _FIXTURES]
    counts = {}
    for _, group, _ in _FIXTURES:
        counts[group] = counts.get(group, 0) + 1
    return {
        "record_kind": "rq1_contract_completeness_metrics",
        "fixture_counts": counts,
        "metrics": aggregate_metrics(observations),
        "observations": observations,
        "provenance": {
            "compile_repetitions": COMPILE_REPETITIONS,
            "fixture_total": len(_FIXTURES),
            "generator": "tools.evaluation.rq1_contract_completeness",
            "source_modules": [
                "tools.task_contract.contract",
            ],
        },
    }


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", required=True)
    args = parser.parse_args(argv)
    payload = collect(Path(args.base_dir))
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    return 0


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
