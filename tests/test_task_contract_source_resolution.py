"""Task Contract固定sourceの状態解決をv1／v2で統一するAcceptance Test。

指示：records/session-handoffs/
      2026-08-05-codex-to-claude-repair-historical-task-contract-source-resolution.md

歴史状態は受理時点のGit blobで照合し、現在有効状態はworking treeで照合し、
`active_stale`はsource pinで有効化しない。この三状態をv1とv2で同じ意味とcodeで扱う。
"""

import hashlib
import importlib
import json
import subprocess
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = "docs/development/2026-08-02-development-policy.md"
ACCEPTED_POLICY_SHA = "9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0"
ACCEPTED_POLICY_COMMIT = "063236512845bde1bc8574c9507bba77f917fade"
EARLY_PILOT = PROJECT_ROOT / "records/task-contract/issue-resolution-early-pilot-v1.json"
COMPACTION_V1 = (
    PROJECT_ROOT
    / "records/task-contract/issue-resolution-todo-compaction-implementation-v1.json"
)
COMPACTION_V2 = (
    PROJECT_ROOT
    / "records/task-contract/issue-resolution-todo-compaction-implementation-v2.json"
)
TRANSCRIPT_CONTRACT = (
    PROJECT_ROOT / "records/task-contract/session-transcript-eventual-preservation-v1.json"
)
HISTORICAL_CONTRACTS = (EARLY_PILOT, COMPACTION_V1, COMPACTION_V2)


def _module():
    return importlib.import_module("tools.development.issue_resolution_pilot")


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _canonical_digest(document):
    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return _sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode(
            "utf-8"
        )
    )


def _write_record(path, document):
    document["content_digest"] = _canonical_digest(document)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def _git(root, *arguments):
    return subprocess.run(
        ("git", *arguments), cwd=str(root), capture_output=True, text=True, check=True
    ).stdout.strip()


def _two_source_repository(tmp_path):
    """固定sourceを二件持つ最小repositoryを作る。片方だけをpinの対象にできる。"""

    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    (root / "records" / "task-contract").mkdir(parents=True)
    (root / "records" / "development").mkdir(parents=True)
    policy = root / "docs" / "policy.md"
    stable = root / "docs" / "stable.md"
    policy.write_text("policy v1\n", encoding="utf-8")
    stable.write_text("stable\n", encoding="utf-8")
    _git(root.parent, "init", "-q", str(root))
    _git(root, "add", "-A")
    _git(
        root, "-c", "user.email=test@example.com", "-c", "user.name=test",
        "commit", "-q", "-m", "accept sources",
    )
    commit = _git(root, "rev-parse", "HEAD")

    contract = {
        "task_contract_id": "TC-FIXTURE-TWO-SOURCE-2026-08-05-V1",
        "status": "active",
        "goal": "fixture",
        "fixed_sources": [
            {"path": "docs/policy.md", "sha256": _sha256(b"policy v1\n")},
            {"path": "docs/stable.md", "sha256": _sha256(b"stable\n")},
        ],
        "in_scope": ["fixture scope"],
    }
    contract_path = root / "records" / "task-contract" / "fixture-two-source-v1.json"
    contract_path.write_text(
        json.dumps(contract, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return root, contract_path, commit


def _status(root, contract_path, status):
    return _write_record(
        root / "records" / "development" / "fixture-status.json",
        {
            "record_kind": "task_contract_lifecycle_status",
            "schema_version": 1,
            "digest_algorithm": "sha256",
            "status_record_id": "TCLS-FIXTURE-TWO-SOURCE-V1",
            "status_record_version": 1,
            "recorded_at": "2026-08-05",
            "task_contract_id": "TC-FIXTURE-TWO-SOURCE-2026-08-05-V1",
            "task_contract_path": "records/task-contract/fixture-two-source-v1.json",
            "task_contract_sha256": _sha256(contract_path.read_bytes()),
            "lifecycle_status": status,
            "grounds": [],
            "effect": "fixture",
        },
    )


def _pin(root, contract_path, *, commit, sha256, unpinned_policy, name="fixture-pin.json"):
    document = {
        "record_kind": "task_contract_source_pin",
        "schema_version": 1,
        "digest_algorithm": "sha256",
        "pin_record_id": f"TCSP-FIXTURE-{name}",
        "pin_record_version": 1,
        "recorded_at": "2026-08-05",
        "task_contract_id": "TC-FIXTURE-TWO-SOURCE-2026-08-05-V1",
        "task_contract_path": "records/task-contract/fixture-two-source-v1.json",
        "task_contract_sha256": _sha256(contract_path.read_bytes()),
        "applicable_lifecycle_statuses": [
            "completed", "completed_carried_forward", "superseded", "historical",
        ],
        "pins": [
            {"path": "docs/policy.md", "sha256": sha256, "commit": commit, "reason": "fixture"}
        ],
        "effect": "fixture",
    }
    if unpinned_policy is not None:
        document["unpinned_source_policy"] = unpinned_policy
    return _write_record(root / "records" / "development" / name, document)


# ---------------------------------------------------------------- 1. 歴史状態のv1


def test_historical_v1_contract_passes_when_policy_changed_in_working_tree():
    pilot = _module()
    working = _sha256((PROJECT_ROOT / POLICY_PATH).read_bytes())
    assert working != ACCEPTED_POLICY_SHA, "この検証は方針文書が更新済みであることを前提にする"

    count, resolved = pilot.validate_fixed_sources_for_contract(
        EARLY_PILOT, project_root=PROJECT_ROOT
    )
    assert count == 9
    assert resolved >= 2

    count, resolved = pilot.validate_fixed_sources_for_contract(
        COMPACTION_V1, project_root=PROJECT_ROOT
    )
    assert count == 3
    assert resolved == 1


# ---------------------------------------------------------------- 2. 歴史状態のv2


def test_historical_v2_contract_passes_under_the_same_condition():
    pilot = _module()
    working = _sha256((PROJECT_ROOT / POLICY_PATH).read_bytes())
    assert working != ACCEPTED_POLICY_SHA

    record = json.loads(COMPACTION_V2.read_text(encoding="utf-8"))
    result = pilot.validate_implementation_task_contract_v2(
        record, project_root=PROJECT_ROOT
    )
    assert result.record_id == "TC-RC3-ISSUE-RESOLUTION-TODO-COMPACTION-2026-08-04-V2"

    count, resolved = pilot.validate_fixed_sources_for_contract(
        COMPACTION_V2, project_root=PROJECT_ROOT
    )
    assert count == 3
    assert resolved == 1


# ------------------------------------------------- 3. pinの無いsourceの扱い


def test_historical_source_without_pin_and_without_explicit_policy_stops(tmp_path):
    pilot = _module()
    root, contract_path, commit = _two_source_repository(tmp_path)
    _status(root, contract_path, "historical")
    _pin(
        root, contract_path, commit=commit, sha256=_sha256(b"policy v1\n"),
        unpinned_policy=None,
    )
    (root / "docs" / "policy.md").write_text("policy v2\n", encoding="utf-8")

    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "pin_unresolvable" in str(error.value)


def test_unpinned_source_uses_working_tree_only_with_explicit_policy(tmp_path):
    pilot = _module()
    root, contract_path, commit = _two_source_repository(tmp_path)
    _status(root, contract_path, "historical")
    _pin(
        root, contract_path, commit=commit, sha256=_sha256(b"policy v1\n"),
        unpinned_policy="verify_working_tree",
    )
    (root / "docs" / "policy.md").write_text("policy v2\n", encoding="utf-8")

    count, resolved = pilot.validate_fixed_sources_for_contract(
        contract_path, project_root=root
    )
    assert count == 2
    assert resolved == 1

    (root / "docs" / "stable.md").write_text("stable v2\n", encoding="utf-8")
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "stale" in str(error.value)


def test_unknown_unpinned_source_policy_stops(tmp_path):
    pilot = _module()
    root, contract_path, commit = _two_source_repository(tmp_path)
    _status(root, contract_path, "historical")
    _pin(
        root, contract_path, commit=commit, sha256=_sha256(b"policy v1\n"),
        unpinned_policy="trust_me",
    )
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "pin_unresolvable" in str(error.value)


# ------------------------------------------------- 4. pinの不一致


def test_pin_digest_differing_from_fixed_source_stops(tmp_path):
    pilot = _module()
    root, contract_path, commit = _two_source_repository(tmp_path)
    _status(root, contract_path, "historical")
    _pin(
        root, contract_path, commit=commit, sha256="4" * 64,
        unpinned_policy="verify_working_tree",
    )
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "source_pin_mismatch" in str(error.value)


def test_pin_pointing_at_a_commit_without_that_blob_stops(tmp_path):
    pilot = _module()
    root, contract_path, _commit = _two_source_repository(tmp_path)
    _status(root, contract_path, "historical")
    (root / "docs" / "policy.md").write_text("policy v2\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(
        root, "-c", "user.email=test@example.com", "-c", "user.name=test",
        "commit", "-q", "-m", "change policy",
    )
    later = _git(root, "rev-parse", "HEAD")
    _pin(
        root, contract_path, commit=later, sha256=_sha256(b"policy v1\n"),
        unpinned_policy="verify_working_tree",
    )
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "source_pin_mismatch" in str(error.value)


def test_pin_bound_to_another_contract_digest_stops(tmp_path):
    pilot = _module()
    root, contract_path, commit = _two_source_repository(tmp_path)
    _status(root, contract_path, "historical")
    pin_path = _pin(
        root, contract_path, commit=commit, sha256=_sha256(b"policy v1\n"),
        unpinned_policy="verify_working_tree",
    )
    document = json.loads(pin_path.read_text(encoding="utf-8"))
    document["task_contract_sha256"] = "5" * 64
    _write_record(pin_path, document)
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "source_pin_mismatch" in str(error.value)


# ------------------------------------------------- 5. activeとactive_stale


def test_active_contract_stops_on_working_tree_mismatch(tmp_path):
    pilot = _module()
    root, contract_path, _commit = _two_source_repository(tmp_path)
    (root / "docs" / "policy.md").write_text("policy v2\n", encoding="utf-8")
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "stale" in str(error.value)


def test_active_stale_stops_even_when_pins_exist(tmp_path):
    pilot = _module()
    root, contract_path, commit = _two_source_repository(tmp_path)
    _status(root, contract_path, "active_stale")
    _pin(
        root, contract_path, commit=commit, sha256=_sha256(b"policy v1\n"),
        unpinned_policy="verify_working_tree",
    )
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(contract_path, project_root=root)
    assert "stale_fixed_source" in str(error.value)


def test_session_transcript_contract_keeps_its_active_stale_meaning():
    pilot = _module()
    record = pilot.load_task_contract_lifecycle_status(
        TRANSCRIPT_CONTRACT, project_root=PROJECT_ROOT
    )
    assert record["lifecycle_status"] == "active_stale"
    with pytest.raises(pilot.PilotValidationError) as error:
        pilot.validate_fixed_sources_for_contract(
            TRANSCRIPT_CONTRACT, project_root=PROJECT_ROOT
        )
    assert "stale_fixed_source" in str(error.value)

    pins = [
        document
        for document in pilot.development_records(
            PROJECT_ROOT, "task_contract_source_pin"
        )
        if document.get("task_contract_path")
        == "records/task-contract/session-transcript-eventual-preservation-v1.json"
    ]
    assert pins == []


# ------------------------------------------------- 6. repositoryの三契約


def test_repository_historical_contracts_resolve_every_fixed_source():
    pilot = _module()
    for contract_path in HISTORICAL_CONTRACTS:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        status_record = pilot.load_task_contract_lifecycle_status(
            contract_path, project_root=PROJECT_ROOT
        )
        assert status_record is not None
        assert status_record["lifecycle_status"] in pilot.HISTORICAL_LIFECYCLE_STATUSES
        assert status_record["grounds"], "歴史状態の根拠を空にしない"

        count, resolved = pilot.validate_fixed_sources_for_contract(
            contract_path, project_root=PROJECT_ROOT
        )
        assert count == len(contract["fixed_sources"])
        assert resolved >= 1

        pinned_paths = set()
        for document in pilot.development_records(
            PROJECT_ROOT, "task_contract_source_pin"
        ):
            if document.get("task_contract_path") != contract_path.relative_to(
                PROJECT_ROOT
            ).as_posix():
                continue
            assert document.get("unpinned_source_policy") == "verify_working_tree"
            pinned_paths.update(pin["path"] for pin in document["pins"])
        assert POLICY_PATH in pinned_paths

        for reference in contract["fixed_sources"]:
            if reference["path"] in pinned_paths:
                continue
            actual = _sha256((PROJECT_ROOT / reference["path"]).read_bytes())
            assert actual == reference["sha256"]


def test_policy_source_pins_use_the_accepted_commit_blob():
    pilot = _module()
    for contract_path in HISTORICAL_CONTRACTS:
        relative = contract_path.relative_to(PROJECT_ROOT).as_posix()
        pins = [
            pin
            for document in pilot.development_records(
                PROJECT_ROOT, "task_contract_source_pin"
            )
            if document.get("task_contract_path") == relative
            for pin in document["pins"]
            if pin["path"] == POLICY_PATH
        ]
        assert len(pins) == 1
        assert pins[0]["sha256"] == ACCEPTED_POLICY_SHA
        assert pins[0]["commit"] == ACCEPTED_POLICY_COMMIT
        blob = subprocess.run(
            ("git", "cat-file", "blob", f"{pins[0]['commit']}:{POLICY_PATH}"),
            cwd=str(PROJECT_ROOT), capture_output=True, check=True,
        ).stdout
        assert _sha256(blob) == ACCEPTED_POLICY_SHA
