"""危険度からレビュー計画を機械生成する入口の受入試験。"""

import hashlib
import importlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).parents[1]


def _git(repository, *arguments):
    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _repository(tmp_path, paths=None):
    if paths is None:
        paths = ["tools/example.py", "tests/test_example.py"]
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "review-plan@example.invalid")
    _git(repository, "config", "user.name", "Review Plan")
    policy_path = repository / "config/development-policy.json"
    policy_path.parent.mkdir()
    policy_path.write_bytes((ROOT / "config/development-policy.json").read_bytes())
    for value in paths:
        path = repository / value
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("before\n", encoding="utf-8")
    _git(repository, "add", ".")
    _git(repository, "commit", "-q", "-m", "base")
    base = _git(repository, "rev-parse", "HEAD")
    for value in paths:
        (repository / value).write_text("after\n", encoding="utf-8")
    _git(repository, "add", ".")
    _git(repository, "commit", "-q", "-m", "target")
    target = _git(repository, "rev-parse", "HEAD")
    return repository, base, target


def _classification(repository, targets=None, actions=()):
    if targets is None:
        targets = [
            {"path": "tests/test_example.py", "kind": "test_code"},
            {"path": "tools/example.py", "kind": "product_code"},
        ]
    path = repository / "review-targets.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "targets": targets,
                "actions": list(actions),
            }
        ),
        encoding="utf-8",
    )
    return path


def _module():
    return importlib.import_module("tools.development.review_plan")


def _without_digest(plan):
    return {key: value for key, value in plan.items() if key != "plan_sha256"}


def test_high_risk_completion_has_one_independent_review_and_fixed_checks(tmp_path):
    repository, base, target = _repository(tmp_path)
    classification = _classification(repository)

    plan = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=target,
        risk="high",
        stage="completion",
        classification_path=classification,
    )

    assert plan["changed_paths"] == ["tests/test_example.py", "tools/example.py"]
    assert plan["schema_version"] == 2
    assert [group["target_kind"] for group in plan["review_groups"]] == [
        "product_code",
        "test_code",
    ]
    assert plan["verification_requirements"] == [
        "relevant_automated_tests",
        "full_test_suite",
        "mutation_or_equivalent_fault_injection",
        "representative_data_validation",
        "independent_review",
    ]
    assert plan["semantic_assignments"] == [
        {"round": 1, "role": "independent_reviewer", "sequence": 1}
    ]
    assert plan["semantic_call_count"] == 1
    assert plan["round_limit"] == 1
    assert plan["blocking_classes"] == [
        "authority_conflict",
        "human_boundary_missing",
        "demonstrable_false_verdict",
        "scope_or_schema_violation",
    ]
    assert plan["scope_expansion"] == "forbidden"


def test_low_and_medium_risk_do_not_add_an_llm_review(tmp_path):
    repository, base, target = _repository(tmp_path)
    classification = _classification(repository)

    low = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=target,
        risk="low",
        stage="completion",
        classification_path=classification,
    )
    medium = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=target,
        risk="medium",
        stage="completion",
        classification_path=classification,
    )

    assert low["semantic_assignments"] == []
    assert low["semantic_call_count"] == 0
    assert low["verification_requirements"] == ["relevant_automated_tests"]
    assert medium["semantic_assignments"] == []
    assert medium["semantic_call_count"] == 0
    assert medium["verification_requirements"] == [
        "relevant_automated_tests",
        "full_test_suite",
    ]


def test_plan_is_deterministic_and_digest_covers_the_whole_plan(tmp_path):
    repository, base, target = _repository(tmp_path)
    classification = _classification(repository)
    arguments = {
        "base_commit": base,
        "target_commit": target,
        "risk": "high",
        "stage": "scope",
        "classification_path": classification,
    }

    first = _module().build_review_plan(repository, **arguments)
    second = _module().build_review_plan(repository, **arguments)
    encoded = json.dumps(
        _without_digest(first),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    assert first == second
    assert first["classification_sha256"] == hashlib.sha256(
        classification.read_bytes()
    ).hexdigest()
    assert first["plan_sha256"] == hashlib.sha256(encoded).hexdigest()


def test_unknown_risk_stage_non_ancestor_and_empty_change_stop(tmp_path):
    repository, base, target = _repository(tmp_path)
    classification = _classification(repository)
    review_plan = _module()

    for values in (
        {"base_commit": base, "target_commit": target, "risk": "urgent", "stage": "completion"},
        {"base_commit": base, "target_commit": target, "risk": "high", "stage": "draft"},
        {"base_commit": target, "target_commit": base, "risk": "high", "stage": "completion"},
        {"base_commit": target, "target_commit": target, "risk": "high", "stage": "completion"},
    ):
        try:
            review_plan.build_review_plan(
                repository,
                classification_path=classification,
                **values,
            )
        except review_plan.ReviewPlanStop:
            pass
        else:
            raise AssertionError(f"unsafe plan accepted: {values}")


def test_cli_returns_one_json_line_and_rejects_plan_overrides(tmp_path, monkeypatch, capsys):
    repository, base, target = _repository(tmp_path)
    classification = _classification(repository)
    cli = importlib.import_module("tools.development.review_plan_cli")
    monkeypatch.chdir(repository)

    exit_code = cli.run([
        "--base-commit", base,
        "--target-commit", target,
        "--risk", "high",
        "--stage", "completion",
        "--classification", str(classification),
    ])
    output = capsys.readouterr()
    document = json.loads(output.out)

    assert exit_code == 0
    assert output.err == ""
    assert output.out.endswith("\n") and output.out.count("\n") == 1
    assert document["semantic_call_count"] == 1

    rejected = cli.run([
        "--base-commit", base,
        "--target-commit", target,
        "--risk", "high",
        "--stage", "completion",
        "--classification", str(classification),
        "--round-limit", "9",
    ])
    stopped = json.loads(capsys.readouterr().out)

    assert rejected == 2
    assert stopped["result"] == "stopped"
    assert stopped["stop_code"] == "input_invalid"


def test_cli_entrypoint_and_discovery_prompt_exist():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    prompt = (
        ROOT / "docs/development/prompts/review-plan-run.md"
    ).read_text(encoding="utf-8")
    pilot_prompt = (
        ROOT / "docs/development/prompts/pilot-collaboration-run.md"
    ).read_text(encoding="utf-8")

    assert pyproject.count("reviewcompass3-review-plan =") == 1
    assert (
        'reviewcompass3-review-plan = "tools.development.review_plan_cli:main"'
        in pyproject
    )
    assert "reviewcompass3-review-plan" in prompt
    assert "--classification" in prompt
    assert "警告" in prompt
    assert "review-plan-run.md" in pilot_prompt


def test_target_kinds_keep_their_own_review_processes(tmp_path):
    paths = [
        "docs/guide.md",
        "tools/validator.py",
        "config/example.json",
        "records/example.json",
    ]
    repository, base, target = _repository(tmp_path, paths)
    classification = _classification(
        repository,
        targets=[
            {"path": "docs/guide.md", "kind": "documentation"},
            {"path": "tools/validator.py", "kind": "validator_code"},
            {"path": "config/example.json", "kind": "configuration"},
            {"path": "records/example.json", "kind": "structured_data"},
        ],
        actions=["external_send"],
    )

    plan = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=target,
        risk="low",
        stage="scope",
        classification_path=classification,
    )
    groups = {group["target_kind"]: group for group in plan["review_groups"]}

    assert list(groups) == [
        "documentation",
        "validator_code",
        "configuration",
        "structured_data",
    ]
    assert groups["documentation"]["verification_requirements"] == [
        "document_consistency_check"
    ]
    assert groups["validator_code"]["effective_risk"] == "high"
    assert "validator_mutation_or_fault_injection" in groups[
        "validator_code"
    ]["verification_requirements"]
    assert "configuration_impact_check" in groups[
        "configuration"
    ]["verification_requirements"]
    assert "default_behavior_check" in groups[
        "configuration"
    ]["verification_requirements"]
    assert "schema_identity_reference_check" in groups[
        "structured_data"
    ]["verification_requirements"]
    assert "missing_duplicate_tamper_cases" in groups[
        "structured_data"
    ]["verification_requirements"]
    assert plan["human_approval_actions"] == ["external_send"]
    assert plan["approval_status"] == "approval_required"
    assert plan["semantic_call_count"] == 1


def test_classification_mismatches_warn_without_defaulting_to_code(tmp_path):
    paths = ["docs/guide.md", "tools/validator.py"]
    repository, base, target = _repository(tmp_path, paths)
    classification = _classification(
        repository,
        targets=[
            {"path": "docs/guide.md", "kind": "documentation"},
            {"path": "tools/validator.py", "kind": "future_kind"},
            {"path": "docs/extra.md", "kind": "documentation"},
        ],
    )
    added = repository / "tests/test_product.py"
    added.parent.mkdir()
    added.write_text("new\n", encoding="utf-8")
    _git(repository, "add", "tests/test_product.py")
    _git(repository, "commit", "-q", "-m", "new target")
    new_target = _git(repository, "rev-parse", "HEAD")

    plan = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=new_target,
        risk="high",
        stage="completion",
        classification_path=classification,
    )

    assert plan["result"] == "completed_with_warnings"
    assert plan["warnings"] == [
        "unclassified_paths",
        "extra_paths",
        "unknown_target_kinds",
    ]
    assert plan["unclassified_paths"] == ["tests/test_product.py"]
    assert plan["extra_paths"] == ["docs/extra.md"]
    assert plan["unknown_targets"] == [
        {"path": "tools/validator.py", "kind": "future_kind"}
    ]
    assert [group["target_kind"] for group in plan["review_groups"]] == [
        "documentation"
    ]
    assert plan["verification_requirements"] == [
        "document_consistency_check"
    ]
    assert target != new_target


def test_invalid_classification_documents_stop(tmp_path):
    repository, base, target = _repository(tmp_path)
    invalid_documents = [
        "not json",
        {"schema_version": 2, "targets": [], "actions": []},
        {
            "schema_version": 1,
            "targets": [
                {"path": "tools/example.py", "kind": "product_code"},
                {"path": "tools/example.py", "kind": "test_code"},
            ],
            "actions": [],
        },
        {
            "schema_version": 1,
            "targets": [{"path": "../outside.py", "kind": "product_code"}],
            "actions": [],
        },
        {
            "schema_version": 1,
            "targets": [{"path": "tools/example.py", "kind": 1}],
            "actions": [],
        },
    ]

    for index, document in enumerate(invalid_documents):
        path = repository / f"invalid-{index}.json"
        if isinstance(document, str):
            path.write_text(document, encoding="utf-8")
        else:
            path.write_text(json.dumps(document), encoding="utf-8")
        try:
            _module().build_review_plan(
                repository,
                base_commit=base,
                target_commit=target,
                risk="low",
                stage="scope",
                classification_path=path,
            )
        except _module().ReviewPlanStop as error:
            assert error.code == "classification_invalid"
        else:
            raise AssertionError(f"invalid classification accepted: {document}")
