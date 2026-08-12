import ast
import hashlib
import importlib
import json
from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "e54fcdaec38ab4b755f67371dbbdd20604447b95"
RED_START_COMMIT = "df6364448c2f24c6f931d17893bd0483b4e2eec9"
MANIFEST_ROOT = Path(
    "records/development/2026-08-11-claude-bootstrap-manifests"
)
MAP_PATH = MANIFEST_ROOT / "declaration-red-map-v1.json"
BASELINE_PATH = MANIFEST_ROOT / "process-call-baseline-v1.json"
REQUIREMENT_IDS = (
    [f"AC-CB-{index:03d}" for index in range(1, 14)]
    + [f"NG-CB-{index:03d}" for index in range(1, 8)]
    + [f"ST-CB-{index:03d}" for index in range(1, 8)]
    + [f"OUT-CB-{index:03d}" for index in range(1, 6)]
)
EGRESS_FILES = (
    "tools/egress/approval.py",
    "tools/egress/dry_run.py",
    "tools/egress/gate.py",
    "tools/egress/payload.py",
    "tools/egress/prefilter.py",
    "tools/egress/sender.py",
)


def _git(*arguments):
    return subprocess.run(
        ["git", *arguments],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=False,
    ).stdout


def _sha256(path):
    return hashlib.sha256((PROJECT_ROOT / path).read_bytes()).hexdigest()


def test_process_inventory_baseline_matches_fixed_commit():
    inventory = importlib.import_module("tools.development.process_call_inventory")
    baseline = json.loads((PROJECT_ROOT / BASELINE_PATH).read_text(encoding="utf-8"))

    generated = inventory.generate_process_call_inventory(
        repository_root=PROJECT_ROOT,
        base_commit=BASE_COMMIT,
        roots=["tools"],
    )

    assert generated == baseline


def test_existing_pilot_commands_and_six_egress_files_remain_unchanged():
    cli = importlib.import_module("tools.development.pilot_collaboration_cli")

    assert set(cli.COMMAND_FLAGS) == {"prepare", "ingest", "status", "bootstrap"}
    assert cli.COMMAND_FLAGS["prepare"] == ("config", "private-root")
    assert cli.COMMAND_FLAGS["ingest"] == (
        "private-root",
        "run-id",
        "stage",
        "attempt-id",
        "raw-file",
        "launch-record",
    )
    assert cli.COMMAND_FLAGS["status"] == ("private-root", "run-id")
    for path in EGRESS_FILES:
        assert _git("show", f"{BASE_COMMIT}:{path}") == (PROJECT_ROOT / path).read_bytes()


def test_red_suite_uses_only_fake_process_and_never_launches_claude():
    helper = (
        PROJECT_ROOT / "tests/fixtures/claude_bootstrap/helpers.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(helper)
    process_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "run"
    ]
    assert len(process_calls) == 1
    assert '["git", *arguments]' in helper
    assert "class FakeClaudeProcess" in helper
    assert "claude --" not in helper


def test_scope_review_human_red_approval_and_all_fixed_inputs_are_pinned():
    expected = {
        "records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-v2.md": "3e0a6af442b7461858dfee94ac4dbd50687d5ca64778a03d1cad9b378b567189",
        "records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-v3-red-start-human-decision-v1.md": "7b0e7959df8acd589135ddf48406e8d57d0d59dafb3a601427879a63da317158",
        "records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v3.md": "02a4f6786875a9eeb87165e387ac1e65d520423930bf3849cb967249639861a7",
    }
    for path, digest in expected.items():
        assert _sha256(path) == digest
    review = (PROJECT_ROOT / next(iter(expected))).read_text(encoding="utf-8")
    decision = (
        PROJECT_ROOT
        / "records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-v3-red-start-human-decision-v1.md"
    ).read_text(encoding="utf-8")
    assert "verified" in review
    assert "high" in decision
    assert "未実装なら失敗する受入試験の作成開始を承認する" in decision


def test_real_send_requires_verified_completion_review_and_separate_bound_approval():
    module = importlib.import_module("tools.development.claude_bootstrap")

    assert module.REQUIRED_COMPLETION_REVIEW_STATUS == "verified"
    assert module.REQUIRED_SEND_APPROVAL_RECORD_KIND == (
        "human_claude_bootstrap_send_approval"
    )
    assert module.RED_START_APPROVAL_IS_NOT_SEND_APPROVAL is True


def test_declaration_map_keys_equal_scope_requirement_ids():
    document = json.loads((PROJECT_ROOT / MAP_PATH).read_text(encoding="utf-8"))
    actual = list(document["declarations"])

    assert len(actual) == 32
    assert len(set(actual)) == 32
    assert set(actual) == set(REQUIREMENT_IDS)
    assert set(actual) - set(REQUIREMENT_IDS) == set()
    assert set(REQUIREMENT_IDS) - set(actual) == set()


def test_red_evidence_keeps_green_fields_explicitly_unimplemented():
    evidence = (PROJECT_ROOT / MANIFEST_ROOT / "red-evidence-v1.md").read_text(
        encoding="utf-8"
    )

    assert "GREEN段階のproduction変更：未実施" in evidence
    assert "実Run：未実施" in evidence
    assert "Claude process作成：未実施" in evidence


def test_completion_review_entry_requires_upstream_derivation_new_counterexample_and_four_classes():
    path = PROJECT_ROOT / "docs/development/prompts/claude-bootstrap-run.md"
    text = path.read_text(encoding="utf-8")

    assert "上流から受入条件を独立導出" in text
    assert "実装fixtureにない反証" in text
    for finding_class in (
        "scope_deviation",
        "missing_acceptance_evidence",
        "unresolved_regression",
        "insufficient_independence",
    ):
        assert finding_class in text
