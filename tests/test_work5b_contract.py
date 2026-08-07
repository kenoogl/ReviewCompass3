"""Work 5B：内部Implementation Task Contractの結線を固定するTest。

承認：DEC-WORK5B-START-001
Contract実体：records/development/2026-08-07-work5b-implementation-task-contract-v1.json
"""

import hashlib
import json
from pathlib import Path

CONTRACT_PATH = Path(
    "records/development/2026-08-07-work5b-implementation-task-contract-v2.json"
)
ATTESTATION_PATH = Path(
    "records/development/2026-08-07-declaration-red-map-checker-reuse-search-attestation-v1.json"
)
DATA_ROOT = (
    Path.home() / ".reviewcompass3/projects/reviewcompass3/development/data"
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


def test_contract_fixed_sources_resolve_by_reference_kind():
    """参照種別ごとに検証を変える（DEC-FIXED-SOURCE-KIND-001）。

    不変recordは指紋一致を要求する。上流の可変文書は作業開始時点のpinであり、
    実在の確認までを要求する——改定によって現行と一致しなくなるのは正常である。
    """

    contract = _contract()
    kinds = set()
    for source in contract["fixed_sources"]:
        path = Path(source["path"])
        assert path.is_file(), f"fixed source missing: {source['path']}"
        kind = source["reference_kind"]
        kinds.add(kind)
        assert kind in ("immutable_record", "pinned_at_start")
        if kind == "immutable_record":
            assert _sha256(path) == source["sha256"], f"digest drift: {source['path']}"
    assert kinds == {"immutable_record", "pinned_at_start"}


def test_contract_supersedes_the_first_version():
    contract = _contract()
    superseded = contract["supersedes"]
    assert superseded["task_contract_version"] == 1
    assert contract["task_contract_version"] == 2
    previous = Path(superseded["path"])
    assert previous.is_file(), "the superseded version is kept as history"
    assert _sha256(previous) == superseded["sha256"]


def test_contract_binds_reuse_search_gate():
    """gateの束縛は、外部化後は証明書経由で解決する（構成C）。"""

    contract = _contract()
    binding = contract["reuse_search_gate"]
    attestation = json.loads(ATTESTATION_PATH.read_text(encoding="utf-8"))
    assert binding["record_content_digest"] == attestation["external"]["content_digest"]

    from tools.development import reuse_search_record as rsr

    expected = {
        key: attestation["source_identity"][key]
        for key in ("profile_run_id", "discovery_run_id", "source_content_id")
    }
    gate = rsr.gate_check_attested(
        attestation_path=ATTESTATION_PATH,
        data_root=DATA_ROOT,
        expected_identity=expected,
    )
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
