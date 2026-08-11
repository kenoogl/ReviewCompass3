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


def _repository(tmp_path):
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "-q")
    _git(repository, "config", "user.email", "review-plan@example.invalid")
    _git(repository, "config", "user.name", "Review Plan")
    policy_path = repository / "config/development-policy.json"
    policy_path.parent.mkdir()
    policy_path.write_bytes((ROOT / "config/development-policy.json").read_bytes())
    target = repository / "tools/example.py"
    target.parent.mkdir()
    target.write_text("VALUE = 1\n", encoding="utf-8")
    _git(repository, "add", "config/development-policy.json", "tools/example.py")
    _git(repository, "commit", "-q", "-m", "base")
    base = _git(repository, "rev-parse", "HEAD")
    target.write_text("VALUE = 2\n", encoding="utf-8")
    second = repository / "tests/test_example.py"
    second.parent.mkdir()
    second.write_text("def test_value():\n    assert True\n", encoding="utf-8")
    _git(repository, "add", "tools/example.py", "tests/test_example.py")
    _git(repository, "commit", "-q", "-m", "target")
    target_commit = _git(repository, "rev-parse", "HEAD")
    return repository, base, target_commit


def _module():
    return importlib.import_module("tools.development.review_plan")


def _without_digest(plan):
    return {key: value for key, value in plan.items() if key != "plan_sha256"}


def test_high_risk_completion_has_one_independent_review_and_fixed_checks(tmp_path):
    repository, base, target = _repository(tmp_path)

    plan = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=target,
        risk="high",
        stage="completion",
    )

    assert plan["changed_paths"] == ["tests/test_example.py", "tools/example.py"]
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

    low = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=target,
        risk="low",
        stage="completion",
    )
    medium = _module().build_review_plan(
        repository,
        base_commit=base,
        target_commit=target,
        risk="medium",
        stage="completion",
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
    arguments = {
        "base_commit": base,
        "target_commit": target,
        "risk": "high",
        "stage": "scope",
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
    assert first["plan_sha256"] == hashlib.sha256(encoded).hexdigest()


def test_unknown_risk_stage_non_ancestor_and_empty_change_stop(tmp_path):
    repository, base, target = _repository(tmp_path)
    review_plan = _module()

    for values in (
        {"base_commit": base, "target_commit": target, "risk": "urgent", "stage": "completion"},
        {"base_commit": base, "target_commit": target, "risk": "high", "stage": "draft"},
        {"base_commit": target, "target_commit": base, "risk": "high", "stage": "completion"},
        {"base_commit": target, "target_commit": target, "risk": "high", "stage": "completion"},
    ):
        try:
            review_plan.build_review_plan(repository, **values)
        except review_plan.ReviewPlanStop:
            pass
        else:
            raise AssertionError(f"unsafe plan accepted: {values}")


def test_cli_returns_one_json_line_and_rejects_plan_overrides(tmp_path, monkeypatch, capsys):
    repository, base, target = _repository(tmp_path)
    cli = importlib.import_module("tools.development.review_plan_cli")
    monkeypatch.chdir(repository)

    exit_code = cli.run([
        "--base-commit", base,
        "--target-commit", target,
        "--risk", "high",
        "--stage", "completion",
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
    assert "review-plan-run.md" in pilot_prompt
