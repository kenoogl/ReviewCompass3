"""最小運用契約実行に関する製品試験。"""

import copy
import hashlib
import importlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

import pytest


_REDACTION_PATH = Path("tools/session_logs/redaction.py")
_REDACTION_SHA256 = (
    "aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd"
)
_REUSED_FILES = {
    "tools/design/one_design_acceptance.py": (
        "b3af7fdf254b21e5d368f2a02cf2aba23a86233a67b4120e7c2b39a3fd4a5c14"
    ),
    "tools/design/one_design_acceptance_entry.py": (
        "7535aa6652514c6ce4dfd31facd2640944a356ddc04802b0df8ae63a9bec9823"
    ),
    "tools/requirements/one_requirement_feature_source.py": (
        "725c886a97bba63fc6d9d5c0d23a5fdc8e67f86eda2752ae587093c9bcdd14d7"
    ),
    "tools/requirements/one_requirement_feature_source_entry.py": (
        "db702231fbf179a16c2742e1335d1c7f8198743baae2263ee2b1844e09ca7bd6"
    ),
}
_AWS_KEY = "AKIA" + "ABCDEFGHIJKLMNOP"
_SEVEN_LISTS = (
    "inputs",
    "outputs",
    "stop_conditions",
    "recovery_conditions",
    "preserved_artifacts",
    "acceptance_criteria",
    "non_goals",
)


def _core():
    return importlib.import_module("tools.operations.operation_contract_run")


def _entry():
    return importlib.import_module(
        "tools.operations.operation_contract_run_entry"
    )


def _canonical(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _sha(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


@pytest.fixture()
def work_root():
    created = Path(tempfile.mkdtemp(prefix="g30-", dir="/private/tmp"))
    try:
        yield created
    finally:
        shutil.rmtree(created, ignore_errors=True)


def _design_inputs(root):
    design = {
        "schema_version": 1,
        "design_identifier": "DESIGN-RUN-ONE",
        "facts": [
            {"fact_id": "F-MODE", "subject": "mode", "value": "safe"},
        ],
    }
    acceptance = {
        "schema_version": 1,
        "acceptance_identifier": "ACCEPT-RUN-ONE",
        "conditions": [
            {
                "condition_id": "C-MODE",
                "subject": "mode",
                "operator": "equals",
                "expected": "safe",
            },
        ],
    }
    design_path = root / "design.json"
    acceptance_path = root / "acceptance.json"
    design_path.write_bytes(json.dumps(design).encode("utf-8"))
    acceptance_path.write_bytes(json.dumps(acceptance).encode("utf-8"))
    return {"design": str(design_path), "acceptance": str(acceptance_path)}


def _requirement_inputs(root):
    catalog = {
        "schema_version": 1,
        "catalog_identifier": "CAT-RUN-ONE",
        "sources": [
            {
                "source_id": "SRC-A",
                "sha256": hashlib.sha256(b"src-a").hexdigest(),
                "declared_status": "effective",
            },
        ],
    }
    requirement_id = "REQ-RUN-001"
    obligation_ids = [f"{requirement_id}#statement"] + [
        f"{requirement_id}#{field}.001" for field in _SEVEN_LISTS
    ]
    candidate = {
        "schema_version": 1,
        "candidate_identifier": "RC-RUN-001",
        "feature": {
            "feature_id": "FEAT-RUN",
            "name": "実行の合成例",
            "responsibility": "合成候補の検査",
            "non_goals": ["作成"],
        },
        "requirement": {
            "requirement_id": requirement_id,
            "feature_id": "FEAT-RUN",
            "statement": "合成候補一件を検査する。",
            "inputs": ["出典一覧"],
            "outputs": ["正準JSON"],
            "stop_conditions": ["機微候補"],
            "recovery_conditions": ["入力修正"],
            "preserved_artifacts": ["既存成果物"],
            "acceptance_criteria": ["全採否"],
            "non_goals": ["意味推測"],
        },
        "source_dispositions": [
            {
                "source_id": "SRC-A",
                "disposition": "selected",
                "rationale": "根拠資料",
            },
        ],
        "obligation_sources": [
            {"obligation_id": identifier, "source_ids": ["SRC-A"]}
            for identifier in obligation_ids
        ],
    }
    catalog_path = root / "catalog.json"
    candidate_path = root / "candidate.json"
    catalog_path.write_bytes(json.dumps(catalog).encode("utf-8"))
    candidate_path.write_bytes(
        json.dumps(candidate, ensure_ascii=False).encode("utf-8"),
    )
    return {"catalog": str(catalog_path), "candidate": str(candidate_path)}


def _part_payload(operation, root, inputs):
    if operation == "design_acceptance_check":
        module = importlib.import_module(
            "tools.design.one_design_acceptance_entry"
        )
        arguments = [
            "check",
            "--input-root",
            str(root),
            "--design",
            inputs["design"],
            "--acceptance",
            inputs["acceptance"],
        ]
    else:
        module = importlib.import_module(
            "tools.requirements.one_requirement_feature_source_entry"
        )
        arguments = [
            "check",
            "--input-root",
            str(root),
            "--catalog",
            inputs["catalog"],
            "--candidate",
            inputs["candidate"],
        ]
    buffer = io.BytesIO()
    code = module.main(arguments, output=buffer)
    return code, buffer.getvalue()


_BINDING_POSITIONS = {
    "design_acceptance_check": {
        "design": ("design", "sha256"),
        "acceptance": ("acceptance", "sha256"),
    },
    "requirement_candidate_check": {
        "catalog": ("catalog", "sha256"),
        "candidate": ("candidate", "sha256"),
    },
}


def _expected_bindings(operation, root, inputs):
    code, payload = _part_payload(operation, root, inputs)
    assert code == 0
    result = json.loads(payload[:-1].decode("utf-8"))
    bindings = {}
    for name, position in _BINDING_POSITIONS[operation].items():
        value = result
        for key in position:
            value = value[key]
        bindings[name] = value
    return bindings, result, payload


_SHORT_IDENTIFIERS = {
    "design_acceptance_check": "OC-G08-001",
    "requirement_candidate_check": "OC-G24-001",
}


def _operation_contract(operation, root, inputs, bindings, output_root):
    return {
        "schema_version": 1,
        "contract_identifier": _SHORT_IDENTIFIERS[operation],
        "human_approved": True,
        "operation": operation,
        "input_root": str(root),
        "inputs": inputs,
        "expected_bindings": bindings,
        "output_root": str(output_root),
    }


def _write_contract(root, contract, name="contract.json"):
    contract_path = root / name
    contract_path.write_bytes(
        json.dumps(contract, ensure_ascii=False).encode("utf-8"),
    )
    return contract_path


def _run(contract_path):
    buffer = io.BytesIO()
    code = _entry().main(["run", "--contract", str(contract_path)], output=buffer)
    return code, buffer.getvalue()


def _prepare(work_root, operation="design_acceptance_check"):
    inputs_root = work_root / "in"
    inputs_root.mkdir()
    output_root = work_root / "out"
    output_root.mkdir()
    if operation == "design_acceptance_check":
        inputs = _design_inputs(inputs_root)
    else:
        inputs = _requirement_inputs(inputs_root)
    bindings, part_result, part_payload = _expected_bindings(
        operation,
        inputs_root,
        inputs,
    )
    contract = _operation_contract(
        operation,
        inputs_root,
        inputs,
        bindings,
        output_root,
    )
    return contract, part_result, part_payload, output_root


def _final_path(contract, output_root):
    return output_root / f"{contract['contract_identifier']}--execution-v1.json"


def _partial_path(contract, output_root):
    return output_root / (
        f"{contract['contract_identifier']}--execution-v1.json.partial"
    )


def _expected_record(contract, part_result, part_payload):
    bindings = [
        {
            "name": name,
            "expected_sha256": contract["expected_bindings"][name],
            "reported_sha256": contract["expected_bindings"][name],
        }
        for name in sorted(contract["expected_bindings"])
    ]
    record = {
        "status": "operation_executed",
        "schema_version": 1,
        "contract": {
            "identifier": contract["contract_identifier"],
            "sha256": _sha(contract),
        },
        "operation": contract["operation"],
        "bindings": bindings,
        "part_exit_code": 0,
        "part_result": part_result,
        "part_result_sha256": hashlib.sha256(part_payload[:-1]).hexdigest(),
        "decision_status": "pending_human_decision",
        "external_send_approved": False,
    }
    record["record_sha256"] = _sha(record)
    return record


# ---------------------------------------------------------------------------
# 受入条件1〜5：正例と一意性
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "operation",
    ("design_acceptance_check", "requirement_candidate_check"),
)
def test_positive_run_lands_record_and_matches_stdout(work_root, operation):
    contract, part_result, part_payload, output_root = _prepare(
        work_root,
        operation,
    )
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 0
    final_path = _final_path(contract, output_root)
    assert final_path.exists()
    assert payload == final_path.read_bytes()
    assert payload == _canonical(
        _expected_record(contract, part_result, part_payload),
    ) + b"\n"
    assert not _partial_path(contract, output_root).exists()


def test_record_digests_match_independent_oracle(work_root):
    contract, part_result, part_payload, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)

    _, payload = _run(contract_path)
    record = json.loads(payload[:-1].decode("utf-8"))

    assert record["contract"]["sha256"] == _sha(contract)
    assert record["part_result_sha256"] == hashlib.sha256(
        part_payload[:-1],
    ).hexdigest()
    without_record = dict(record)
    del without_record["record_sha256"]
    assert record["record_sha256"] == _sha(without_record)
    assert record["part_result"] == part_result


def test_contract_member_order_does_not_change_record_bytes(work_root):
    contract, _, _, output_root = _prepare(work_root)
    ordered_path = _write_contract(work_root, contract, "ordered.json")
    reordered = {key: contract[key] for key in reversed(list(contract))}
    reordered_path = work_root / "reordered.json"
    reordered_path.write_bytes(
        json.dumps(reordered, ensure_ascii=False).encode("utf-8"),
    )

    _, first_payload = _run(ordered_path)
    _final_path(contract, output_root).unlink()
    _, second_payload = _run(reordered_path)

    assert first_payload == second_payload


# ---------------------------------------------------------------------------
# 受入条件6〜8：束縛照合とschema
# ---------------------------------------------------------------------------


def test_binding_mismatch_stops_without_files(work_root):
    contract, _, _, output_root = _prepare(work_root)
    contract["expected_bindings"]["design"] = hashlib.sha256(
        b"other",
    ).hexdigest()
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 2
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "reason": "binding_mismatch",
            "source": "contract",
            "status": "stopped",
        },
    ) + b"\n"
    assert not _final_path(contract, output_root).exists()
    assert not _partial_path(contract, output_root).exists()


@pytest.mark.parametrize("approved", (False, 1, "true", None))
def test_human_approved_variants_stop_invalid_schema(work_root, approved):
    contract, _, _, _ = _prepare(work_root)
    if approved is None:
        del contract["human_approved"]
    else:
        contract["human_approved"] = approved
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_schema"' in payload
    assert b'"contract"' in payload


@pytest.mark.parametrize(
    "mutate",
    (
        lambda contract: contract.update({"operation": "unknown_operation"}),
        lambda contract: contract["inputs"].pop("design"),
        lambda contract: contract["inputs"].update({"extra": "/tmp/x"}),
        lambda contract: contract["expected_bindings"].pop("design"),
        lambda contract: contract["expected_bindings"].update(
            {"extra": "a" * 64},
        ),
        lambda contract: contract.update({"input_root": "relative/path"}),
        lambda contract: contract.update({"output_root": 7}),
        lambda contract: contract.update({"unknown_member": "x"}),
        lambda contract: contract.update({"schema_version": 2}),
        lambda contract: contract.update({"schema_version": True}),
        lambda contract: contract.update({"contract_identifier": "白い空白 id"}),
        lambda contract: contract["inputs"].update({"design": "/x/../y"}),
    ),
)
def test_schema_violations_stop_invalid_schema(work_root, mutate):
    contract, _, _, _ = _prepare(work_root)
    mutate(contract)
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_schema"' in payload


def test_duplicate_member_stops_invalid_schema(work_root):
    contract, _, _, _ = _prepare(work_root)
    text = json.dumps(contract, ensure_ascii=False)
    duplicated = text[:-1] + ',"schema_version":1}'
    contract_path = work_root / "contract.json"
    contract_path.write_bytes(duplicated.encode("utf-8"))

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_schema"' in payload


def test_escaped_duplicate_member_stops_invalid_schema(work_root):
    contract, _, _, _ = _prepare(work_root)
    text = json.dumps(contract, ensure_ascii=False)
    duplicated = text[:-1] + ',"a":1,"\\u0061":2}'
    contract_path = work_root / "contract.json"
    contract_path.write_bytes(duplicated.encode("utf-8"))

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_schema"' in payload


@pytest.mark.parametrize(
    "value",
    (1.5, None, [["nested"]], "\ud800"),
)
def test_forbidden_values_stop_invalid_schema(work_root, value):
    contract, _, _, _ = _prepare(work_root)
    contract["inputs"]["design"] = value
    contract_path = work_root / "contract.json"
    contract_path.write_bytes(json.dumps(contract).encode("utf-8"))

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_schema"' in payload


# ---------------------------------------------------------------------------
# 受入条件10・11：機微情報候補と規則の照合
# ---------------------------------------------------------------------------


def test_aws_key_in_identifier_stops_sensitive(work_root):
    contract, _, _, output_root = _prepare(work_root)
    contract["contract_identifier"] = _AWS_KEY
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 3
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "reason": "sensitive_data_remaining",
            "source": "contract",
            "status": "stopped",
        },
    ) + b"\n"
    assert _AWS_KEY.encode() not in payload
    assert list(output_root.iterdir()) == []


def test_sensitive_value_under_unknown_member_stops_before_schema(work_root):
    contract, _, _, _ = _prepare(work_root)
    contract["unknown_member"] = "user@example.com"
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 3
    assert b'"sensitive_data_remaining"' in payload


def test_aws_key_as_binding_value_stops_sensitive(work_root):
    contract, _, _, _ = _prepare(work_root)
    contract["expected_bindings"]["design"] = _AWS_KEY
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 3
    assert b'"sensitive_data_remaining"' in payload


def test_hex_binding_values_are_not_flagged(work_root):
    contract, _, _, _ = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)

    code, _ = _run(contract_path)

    assert code == 0


def test_high_entropy_identifier_stops_sensitive(work_root):
    contract, _, _, _ = _prepare(work_root)
    contract["contract_identifier"] = hashlib.sha256(b"leak").hexdigest()
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 3
    assert b'"sensitive_data_remaining"' in payload


@pytest.mark.parametrize(
    "sensitive_value",
    (
        "Bearer abcdefabcdef0123456789",
        "api_key = abcdef123456789012",
        "-----BEGIN PRIVATE KEY-----\nZm9v\n-----END PRIVATE KEY-----",
    ),
)
def test_remaining_pattern_types_stop_sensitive(work_root, sensitive_value):
    contract, _, _, _ = _prepare(work_root)
    contract["unknown_member"] = sensitive_value
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 3
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "reason": "sensitive_data_remaining",
            "source": "contract",
            "status": "stopped",
        },
    ) + b"\n"


def test_registry_operation_names_are_not_flagged(work_root):
    contract, _, _, _ = _prepare(work_root, "requirement_candidate_check")
    contract_path = _write_contract(work_root, contract)

    code, _ = _run(contract_path)

    assert code == 0


def test_non_registry_operation_value_is_not_excluded(work_root):
    contract, _, _, _ = _prepare(work_root)
    contract["operation"] = hashlib.sha256(b"fake-operation").hexdigest()
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 3
    assert b'"sensitive_data_remaining"' in payload


def test_redaction_module_is_pinned_before_and_after_run(work_root):
    def current_digest():
        return hashlib.sha256(_REDACTION_PATH.read_bytes()).hexdigest()

    assert current_digest() == _REDACTION_SHA256
    redaction = importlib.import_module("tools.session_logs.redaction")
    assert callable(redaction.default_pattern_rules)
    assert callable(redaction.find_high_entropy)
    assert len(redaction.default_pattern_rules()) == 5

    contract, _, _, _ = _prepare(work_root)
    _run(_write_contract(work_root, contract))

    assert current_digest() == _REDACTION_SHA256


def test_reused_part_files_are_pinned():
    for path, expected in _REUSED_FILES.items():
        digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        assert digest == expected, path


# ---------------------------------------------------------------------------
# 受入条件12・13・15：契約file・出力先・引数の停止
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "arguments",
    (
        [],
        ["run"],
        ["check", "--contract", "/x"],
        ["run", "--contract", "/x", "--contract", "/x"],
        ["run", "--unknown", "/x"],
    ),
)
def test_malformed_arguments_stop(work_root, arguments):
    code, payload = _run_arguments(arguments)

    assert code == 2
    assert b'"invalid_arguments"' in payload
    assert b'"arguments"' in payload


def _run_arguments(arguments):
    buffer = io.BytesIO()
    code = _entry().main(arguments, output=buffer)
    return code, buffer.getvalue()


def test_relative_contract_path_stops_invalid_path(work_root):
    code, payload = _run_arguments(["run", "--contract", "contract.json"])

    assert code == 2
    assert b'"invalid_path"' in payload


@pytest.mark.parametrize(
    "contract_path_value",
    ("/x/with\x00nul.json", "/x/with\ud800surrogate.json"),
)
def test_nul_and_surrogate_paths_stop_before_reading(
    work_root,
    contract_path_value,
):
    code, payload = _run_arguments(
        ["run", "--contract", contract_path_value],
    )

    assert code == 2
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "reason": "invalid_path",
            "source": "arguments",
            "status": "stopped",
        },
    ) + b"\n"


def test_same_size_modification_during_read_stops(work_root, monkeypatch):
    contract, _, _, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    core = _core()
    original_read = os.read
    state = {"fired": False}

    def racing_read(descriptor, size):
        data = original_read(descriptor, size)
        if not state["fired"] and data:
            state["fired"] = True
            raw = contract_path.read_bytes()
            contract_path.write_bytes(bytes(reversed(raw)))
        return data

    monkeypatch.setattr(core.os, "read", racing_read)

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"unreadable_input"' in payload
    assert b'"contract"' in payload
    assert list(output_root.iterdir()) == []


def test_contract_symlink_stops_unreadable(work_root):
    contract, _, _, _ = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    link_path = work_root / "link.json"
    link_path.symlink_to(contract_path)

    code, payload = _run(link_path)

    assert code == 2
    assert b'"unreadable_input"' in payload
    assert b'"contract"' in payload


def test_contract_directory_stops_unreadable(work_root):
    directory = work_root / "directory.json"
    directory.mkdir()

    code, payload = _run(directory)

    assert code == 2
    assert b'"unreadable_input"' in payload


def test_contract_size_limit(work_root):
    contract_path = work_root / "contract.json"
    contract_path.write_bytes(b"x" * 262145)

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"size_limit_exceeded"' in payload


def test_contract_invalid_utf8(work_root):
    contract_path = work_root / "contract.json"
    contract_path.write_bytes(b"\xff\xfe broken")

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_utf8"' in payload


@pytest.mark.parametrize(
    "prepare_output",
    (
        lambda contract, output_root: shutil.rmtree(output_root),
        lambda contract, output_root: (
            shutil.rmtree(output_root),
            output_root.write_text("file"),
        ),
        lambda contract, output_root: _final_path(
            contract,
            output_root,
        ).write_text("existing"),
        lambda contract, output_root: _partial_path(
            contract,
            output_root,
        ).write_text("leftover"),
    ),
)
def test_output_root_violations_stop(work_root, prepare_output):
    contract, _, _, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    prepare_output(contract, output_root)

    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_output_root"' in payload
    assert b'"output"' in payload


def test_existing_final_is_not_overwritten(work_root):
    contract, _, _, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    final_path = _final_path(contract, output_root)
    final_path.write_text("existing")

    code, _ = _run(contract_path)

    assert code == 2
    assert final_path.read_text() == "existing"


# ---------------------------------------------------------------------------
# 受入条件14：部品停止の転記
# ---------------------------------------------------------------------------


def test_part_stop_is_translated_without_files(work_root):
    contract, _, _, output_root = _prepare(
        work_root,
        "requirement_candidate_check",
    )
    Path(contract["inputs"]["catalog"]).write_bytes(b"{}")
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 5
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "part_exit_code": 2,
            "part_reason": "invalid_schema",
            "part_source": "catalog",
            "reason": "part_stopped",
            "source": "part",
            "status": "stopped",
        },
    ) + b"\n"
    assert list(output_root.iterdir()) == []


def test_part_sensitive_stop_keeps_exit_three_in_part_field(work_root):
    contract, _, _, output_root = _prepare(
        work_root,
        "requirement_candidate_check",
    )
    catalog = json.loads(Path(contract["inputs"]["catalog"]).read_bytes())
    catalog["sources"][0]["source_id"] = _AWS_KEY
    Path(contract["inputs"]["catalog"]).write_bytes(
        json.dumps(catalog).encode("utf-8"),
    )
    contract["expected_bindings"]["catalog"] = hashlib.sha256(
        b"unused",
    ).hexdigest()
    contract_path = _write_contract(work_root, contract)

    code, payload = _run(contract_path)

    assert code == 5
    record = json.loads(payload[:-1].decode("utf-8"))
    assert record["part_reason"] == "sensitive_data_remaining"
    assert record["part_source"] == "catalog"
    assert record["part_exit_code"] == 3
    assert _AWS_KEY.encode() not in payload
    assert list(output_root.iterdir()) == []


# ---------------------------------------------------------------------------
# 受入条件16・16b・16c：書込み境界
# ---------------------------------------------------------------------------


def test_positive_run_leaves_only_final_file(work_root):
    contract, _, _, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    inputs_before = sorted(
        path.name for path in (work_root / "in").iterdir()
    )

    _run(contract_path)

    assert [path.name for path in output_root.iterdir()] == [
        _final_path(contract, output_root).name,
    ]
    assert sorted(
        path.name for path in (work_root / "in").iterdir()
    ) == inputs_before


def test_publish_failure_recovers_partial(work_root, monkeypatch):
    contract, _, _, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    core = _core()

    def failing_link(source, destination, **kwargs):
        raise OSError("injected link failure")

    monkeypatch.setattr(core.os, "link", failing_link)

    code, payload = _run(contract_path)

    assert code == 4
    assert b'"record_write_failed"' in payload
    assert b'"output"' in payload
    assert list(output_root.iterdir()) == []


def test_reread_mismatch_recovers_partial(work_root, monkeypatch):
    contract, _, _, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    core = _core()

    monkeypatch.setattr(
        core,
        "_read_back_bytes",
        lambda *args, **kwargs: b"corrupted",
    )

    code, payload = _run(contract_path)

    assert code == 4
    assert b'"record_write_failed"' in payload
    assert list(output_root.iterdir()) == []


def test_cleanup_failure_after_publish_keeps_final_as_record(
    work_root,
    monkeypatch,
):
    contract, part_result, part_payload, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    core = _core()

    def failing_unlink(path, **kwargs):
        raise OSError("injected unlink failure")

    monkeypatch.setattr(core.os, "unlink", failing_unlink)

    code, payload = _run(contract_path)

    assert code == 6
    assert payload == _canonical(
        {
            "external_send_approved": False,
            "reason": "partial_cleanup_failed",
            "source": "output",
            "status": "stopped",
        },
    ) + b"\n"
    final_path = _final_path(contract, output_root)
    partial_path = _partial_path(contract, output_root)
    assert final_path.exists()
    assert partial_path.exists()
    assert final_path.stat().st_ino == partial_path.stat().st_ino
    assert final_path.read_bytes() == _canonical(
        _expected_record(contract, part_result, part_payload),
    ) + b"\n"

    monkeypatch.undo()
    code, payload = _run(contract_path)

    assert code == 2
    assert b'"invalid_output_root"' in payload


# ---------------------------------------------------------------------------
# 受入条件16・17：禁止作用と別現在位置の同一bytes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module_path",
    (
        "tools/operations/operation_contract_run.py",
        "tools/operations/operation_contract_run_entry.py",
    ),
)
def test_modules_avoid_forbidden_capabilities(module_path):
    source = Path(module_path).read_text(encoding="utf-8")

    for forbidden in (
        "socket",
        "subprocess",
        "urllib",
        "requests",
        "environ",
        "getenv",
        "import time",
        "import random",
        "import datetime",
    ):
        assert forbidden not in source


def test_module_execution_from_other_directory_matches_bytes(work_root):
    contract, _, _, output_root = _prepare(work_root)
    contract_path = _write_contract(work_root, contract)
    _, direct_payload = _run(contract_path)
    _final_path(contract, output_root).unlink()
    execution_environment = dict(os.environ)
    execution_environment["PYTHONPATH"] = str(Path.cwd())

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "tools.operations.operation_contract_run_entry",
            "run",
            "--contract",
            str(contract_path),
        ],
        capture_output=True,
        cwd=work_root,
        env=execution_environment,
    )

    assert completed.returncode == 0
    assert completed.stdout == direct_payload
    assert completed.stderr == b""


def test_console_script_is_registered():
    with Path("pyproject.toml").open("rb") as stream:
        configuration = tomllib.load(stream)

    assert configuration["project"]["scripts"][
        "reviewcompass3-operation-run"
    ] == "tools.operations.operation_contract_run_entry:main"
