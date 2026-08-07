"""Work 5B：内部Implementation Task Contractの結線を固定するTest。

承認：DEC-WORK5B-START-001
Contract実体：records/development/2026-08-07-work5b-implementation-task-contract-v1.json
"""

import hashlib
import json
from pathlib import Path

CONTRACT_PATH = Path(
    "records/development/2026-08-07-work5b-implementation-task-contract-v1.json"
)
REUSE_SEARCH_PATH = Path(
    "records/development/2026-08-07-declaration-red-map-checker-reuse-search-v1.json"
)


def _contract():
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def test_contract_exists_with_expected_identity():
    contract = _contract()
    assert contract["record_kind"] == "work5b_implementation_task_contract"
    assert contract["schema_version"] == 1
    assert contract["task_contract_id"] == "TC-WORK5B-DECLARATION-RED-MAP-CHECK-001"
    assert contract["state_at_creation"] == "task_contract_commit_pending"


def test_contract_fixed_sources_resolve_and_match():
    contract = _contract()
    for source in contract["fixed_sources"]:
        path = Path(source["path"])
        assert path.is_file(), f"fixed source missing: {source['path']}"
        assert _sha256(path) == source["sha256"], f"digest drift: {source['path']}"


def test_contract_binds_reuse_search_gate():
    contract = _contract()
    binding = contract["reuse_search_gate"]
    assert binding["record_path"] == str(REUSE_SEARCH_PATH)
    record = json.loads(REUSE_SEARCH_PATH.read_text(encoding="utf-8"))
    assert binding["record_content_digest"] == record["content_digest"]

    from tools.development import reuse_search_record as rsr

    expected = {
        key: record["source_identity"][key]
        for key in ("profile_run_id", "discovery_run_id", "source_content_id")
    }
    gate = rsr.gate_check(record_path=REUSE_SEARCH_PATH, expected_identity=expected)
    assert gate["start_allowed"] is True


def test_contract_declares_work_items_in_order():
    contract = _contract()
    ids = [item["work_item_id"] for item in contract["work_items"]]
    assert ids == ["WI-5B-1", "WI-5B-2", "WI-5B-3", "WI-5B-4"]
    assert [item["sequence"] for item in contract["work_items"]] == [1, 2, 3, 4]
    for item in contract["work_items"]:
        assert item["status_at_creation"] == "not_started"


def test_contract_keeps_human_boundary_and_prohibitions():
    contract = _contract()
    prohibitions = "\n".join(contract["prohibitions"])
    assert "implementation_ready" in prohibitions
    assert "hook" in prohibitions
    assert contract["risk"] == "high"
    assert contract["human_gates"], "human gates must be declared"
