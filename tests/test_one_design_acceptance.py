"""一件の設計・受入条件照合に関する製品試験。"""

import copy
import hashlib
import importlib
import json
import os
import stat
from types import SimpleNamespace

import pytest


def _module():
    return importlib.import_module("tools.design.one_design_acceptance")


def _json_bytes(value):
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _design(facts=None, **overrides):
    value = {
        "schema_version": 1,
        "design_identifier": "DESIGN-ONE",
        "facts": facts if facts is not None else [
            {"fact_id": "F-MODE", "subject": "mode", "value": "safe"},
        ],
    }
    value.update(overrides)
    return value


def _acceptance(conditions=None, **overrides):
    value = {
        "schema_version": 1,
        "acceptance_identifier": "ACCEPTANCE-ONE",
        "conditions": conditions if conditions is not None else [
            {
                "condition_id": "C-MODE",
                "subject": "mode",
                "operator": "equals",
                "expected": "safe",
            },
        ],
    }
    value.update(overrides)
    return value


def _compare(design=None, acceptance=None):
    module = _module()
    return module.compare_inputs(
        _json_bytes(_design() if design is None else design),
        _json_bytes(_acceptance() if acceptance is None else acceptance),
    )


@pytest.mark.parametrize(
    ("operator", "actual", "expected", "disposition"),
    (
        ("equals", "safe", "safe", "satisfied"),
        ("equals", "fast", "safe", "contradicted"),
        ("equals", 1, True, "contradicted"),
        ("not_equals", "fast", "safe", "satisfied"),
        ("not_equals", "safe", "safe", "contradicted"),
        ("contains_all", ["a", "b"], ["b"], "satisfied"),
        ("contains_all", ["a"], ["a", "b"], "contradicted"),
        ("contains_all", "a", ["a"], "contradicted"),
        ("contains_none", ["a"], ["b"], "satisfied"),
        ("contains_none", ["a", "b"], ["b"], "contradicted"),
        ("contains_none", "a", ["b"], "contradicted"),
    ),
)
def test_applies_each_fixed_comparison(
    operator,
    actual,
    expected,
    disposition,
):
    result = _compare(
        _design([{"fact_id": "F-X", "subject": "x", "value": actual}]),
        _acceptance([
            {
                "condition_id": "C-X",
                "subject": "x",
                "operator": operator,
                "expected": expected,
            },
        ]),
    )

    assert result["results"][0]["disposition"] == disposition


def test_distinguishes_missing_and_unreferenced_facts():
    result = _compare(
        _design([
            {"fact_id": "F-USED", "subject": "used", "value": True},
            {"fact_id": "F-EXTRA", "subject": "extra", "value": 3},
        ]),
        _acceptance([
            {
                "condition_id": "C-MISSING",
                "subject": "missing",
                "operator": "equals",
                "expected": True,
            },
            {
                "condition_id": "C-USED",
                "subject": "used",
                "operator": "equals",
                "expected": True,
            },
        ]),
    )

    by_id = {item["condition_id"]: item for item in result["results"]}
    assert by_id["C-MISSING"]["disposition"] == "missing"
    assert by_id["C-MISSING"]["fact_id"] is None
    assert by_id["C-MISSING"]["actual_value_sha256"] is None
    assert result["unreferenced_fact_ids"] == ["F-EXTRA"]
    assert result["counts"] == {
        "contradicted": 0,
        "missing": 1,
        "satisfied": 1,
        "unreferenced_fact": 1,
    }


def test_keeps_all_conditions_for_human_when_everything_matches():
    result = _compare()

    assert result["verdict"] == "conditions_met_pending_human_decision"
    assert result["decision_status"] == "pending_human_decision"
    assert result["human_decision_queue"] == [
        {"identifiers": ["C-MODE"], "kind": "satisfied"},
    ]
    assert result["external_send_approved"] is False


def test_orders_the_human_queue_by_fixed_kind_order():
    result = _compare(
        _design([
            {"fact_id": "F-A", "subject": "a", "value": 1},
            {"fact_id": "F-B", "subject": "b", "value": 2},
            {"fact_id": "F-D", "subject": "d", "value": 4},
        ]),
        _acceptance([
            {
                "condition_id": "C-A",
                "subject": "a",
                "operator": "equals",
                "expected": 9,
            },
            {
                "condition_id": "C-B",
                "subject": "b",
                "operator": "equals",
                "expected": 2,
            },
            {
                "condition_id": "C-C",
                "subject": "c",
                "operator": "equals",
                "expected": 3,
            },
        ]),
    )

    assert [item["kind"] for item in result["human_decision_queue"]] == [
        "contradicted",
        "missing",
        "satisfied",
        "unreferenced_fact",
    ]


def test_returns_only_the_fixed_normal_result_shape():
    result = _compare()

    assert set(result) == {
        "acceptance",
        "comparison_sha256",
        "counts",
        "decision_status",
        "design",
        "external_send_approved",
        "human_decision_queue",
        "results",
        "schema_version",
        "status",
        "unreferenced_fact_ids",
        "verdict",
    }
    assert set(result["design"]) == {"fact_count", "identifier", "sha256"}
    assert set(result["acceptance"]) == {
        "condition_count",
        "identifier",
        "sha256",
    }
    assert set(result["results"][0]) == {
        "actual_value_sha256",
        "condition_id",
        "disposition",
        "expected_value_sha256",
        "fact_id",
        "operator",
        "subject",
    }
    assert result["status"] == "comparison_completed"
    assert result["schema_version"] == 1


def test_does_not_return_input_values():
    secret_actual = "private-design-value"
    secret_expected = "private-acceptance-value"
    result = _compare(
        _design([{"fact_id": "F-X", "subject": "x", "value": secret_actual}]),
        _acceptance([
            {
                "condition_id": "C-X",
                "subject": "x",
                "operator": "equals",
                "expected": secret_expected,
            },
        ]),
    )
    encoded = _json_bytes(result)

    assert secret_actual.encode() not in encoded
    assert secret_expected.encode() not in encoded


def test_hashes_match_the_normalized_documents_and_result():
    module = _module()
    result = _compare()
    without_self = dict(result)
    comparison_sha256 = without_self.pop("comparison_sha256")

    assert comparison_sha256 == hashlib.sha256(
        module.canonical_json_bytes(without_self)
    ).hexdigest()
    assert len(result["design"]["sha256"]) == 64
    assert len(result["acceptance"]["sha256"]) == 64
    assert len(result["results"][0]["actual_value_sha256"]) == 64
    assert len(result["results"][0]["expected_value_sha256"]) == 64


def test_ignores_object_array_and_string_set_order():
    module = _module()
    first_design = _design([
        {"fact_id": "F-B", "subject": "b", "value": ["z", "a"]},
        {"fact_id": "F-A", "subject": "a", "value": True},
    ])
    first_acceptance = _acceptance([
        {
            "condition_id": "C-B",
            "subject": "b",
            "operator": "contains_all",
            "expected": ["z", "a"],
        },
        {
            "condition_id": "C-A",
            "subject": "a",
            "operator": "equals",
            "expected": True,
        },
    ])
    second_design = copy.deepcopy(first_design)
    second_design["facts"].reverse()
    second_design["facts"][1]["value"].reverse()
    second_acceptance = copy.deepcopy(first_acceptance)
    second_acceptance["conditions"].reverse()
    second_acceptance["conditions"][1]["expected"].reverse()

    first = _compare(first_design, first_acceptance)
    second = _compare(second_design, second_acceptance)

    assert first == second
    assert module.canonical_json_bytes(first) == module.canonical_json_bytes(second)


def test_one_value_change_changes_all_dependent_hashes():
    first = _compare()
    second_design = _design()
    second_design["facts"][0]["value"] = "changed"
    second = _compare(second_design, _acceptance())

    assert first["design"]["sha256"] != second["design"]["sha256"]
    assert (
        first["results"][0]["actual_value_sha256"]
        != second["results"][0]["actual_value_sha256"]
    )
    assert first["comparison_sha256"] != second["comparison_sha256"]


@pytest.mark.parametrize(
    ("raw", "source"),
    (
        (
            b'{"schema_version":999,"schema_version":1,'
            b'"design_identifier":"D","facts":[]}',
            "design",
        ),
        (
            b'{"schema_version":1,"design_identifier":"D","facts":['
            b'{"fact_id":"F","subject":"x","value":1,"value":2}]}',
            "design",
        ),
        (
            b'{"schema_version":1,"acceptance_identifier":"A",'
            b'"conditions":[{"condition_id":"C","subject":"x",'
            b'"\\u0073ubject":"y","operator":"equals","expected":1}]}',
            "acceptance",
        ),
    ),
)
def test_rejects_duplicate_json_members_before_normalization(raw, source):
    module = _module()
    design_bytes = _json_bytes(_design())
    acceptance_bytes = _json_bytes(_acceptance())
    if source == "design":
        design_bytes = raw
    else:
        acceptance_bytes = raw

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        module.compare_inputs(design_bytes, acceptance_bytes)

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == source


@pytest.mark.parametrize(
    ("design", "acceptance", "source"),
    (
        (_design(extra=True), _acceptance(), "design"),
        (_design(facts=[]), _acceptance(), "design"),
        (
            _design([
                {"fact_id": "F-1", "subject": "x", "value": 1},
                {"fact_id": "F-2", "subject": "x", "value": 2},
            ]),
            _acceptance(),
            "design",
        ),
        (
            _design([{"fact_id": "F-1", "subject": "x", "value": None}]),
            _acceptance(),
            "design",
        ),
        (
            _design(),
            _acceptance([
                {
                    "condition_id": "C-1",
                    "subject": "x",
                    "operator": "equals",
                    "expected": 1,
                },
                {
                    "condition_id": "C-2",
                    "subject": "x",
                    "operator": "equals",
                    "expected": 2,
                },
            ]),
            "acceptance",
        ),
        (
            _design(),
            _acceptance([
                {
                    "condition_id": "C-1",
                    "subject": "x",
                    "operator": "unknown",
                    "expected": 1,
                },
            ]),
            "acceptance",
        ),
        (
            _design(),
            _acceptance([
                {
                    "condition_id": "C-1",
                    "subject": "x",
                    "operator": "contains_all",
                    "expected": "not-an-array",
                },
            ]),
            "acceptance",
        ),
    ),
)
def test_rejects_invalid_closed_schemas(design, acceptance, source):
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        _compare(design, acceptance)

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == source


@pytest.mark.parametrize(
    "bad_identifier",
    ("", "starts with space", "/absolute", "a" * 129),
)
def test_rejects_invalid_safe_identifiers(bad_identifier):
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        _compare(_design(design_identifier=bad_identifier), _acceptance())

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == "design"


@pytest.mark.parametrize(
    "bad_value",
    (
        1.5,
        {},
        [["nested"]],
        [],
        ["duplicate", "duplicate"],
        9007199254740992,
        "",
        "nul\x00value",
    ),
)
def test_rejects_forbidden_value_types_and_bounds(bad_value):
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        _compare(
            _design([{"fact_id": "F-X", "subject": "x", "value": bad_value}]),
            _acceptance(),
        )

    assert caught.value.reason == "invalid_schema"
    assert caught.value.source == "design"


def test_rejects_more_than_256_facts_or_conditions():
    module = _module()
    facts = [
        {"fact_id": f"F-{index}", "subject": f"s-{index}", "value": index}
        for index in range(257)
    ]
    conditions = [
        {
            "condition_id": f"C-{index}",
            "subject": f"s-{index}",
            "operator": "equals",
            "expected": index,
        }
        for index in range(257)
    ]

    with pytest.raises(module.DesignAcceptanceStop):
        _compare(_design(facts), _acceptance())
    with pytest.raises(module.DesignAcceptanceStop):
        _compare(_design(), _acceptance(conditions))


def test_rejects_non_bytes_and_invalid_utf8_inputs():
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as non_bytes:
        module.compare_inputs("not-bytes", _json_bytes(_acceptance()))
    assert non_bytes.value.reason == "invalid_schema"
    assert non_bytes.value.source == "design"

    with pytest.raises(module.DesignAcceptanceStop) as invalid_utf8:
        module.compare_inputs(b"\xff", _json_bytes(_acceptance()))
    assert invalid_utf8.value.reason == "invalid_utf8"
    assert invalid_utf8.value.source == "design"


def _input_files(tmp_path):
    root = tmp_path / "input"
    root.mkdir()
    design_path = root / "design.json"
    acceptance_path = root / "acceptance.json"
    design_path.write_bytes(_json_bytes(_design()))
    acceptance_path.write_bytes(_json_bytes(_acceptance()))
    return root, design_path, acceptance_path


def _reader():
    return _module().read_input_pair


def test_reads_two_distinct_regular_files_from_the_explicit_root(tmp_path):
    root, design_path, acceptance_path = _input_files(tmp_path)

    design_bytes, acceptance_bytes = _reader()(
        str(root),
        str(design_path),
        str(acceptance_path),
    )

    assert design_bytes == design_path.read_bytes()
    assert acceptance_bytes == acceptance_path.read_bytes()


@pytest.mark.parametrize(
    "case",
    (
        "relative_root",
        "relative_design",
        "relative_acceptance",
        "outside_design",
        "dot_component",
        "dotdot_component",
        "empty_component",
        "same_path",
    ),
)
def test_rejects_lexically_invalid_or_ambiguous_paths(tmp_path, case):
    module = _module()
    reader = module.read_input_pair
    root, design_path, acceptance_path = _input_files(tmp_path)
    values = [str(root), str(design_path), str(acceptance_path)]
    if case == "relative_root":
        values[0] = "input"
    elif case == "relative_design":
        values[1] = "design.json"
    elif case == "relative_acceptance":
        values[2] = "acceptance.json"
    elif case == "outside_design":
        outside = tmp_path / "outside.json"
        outside.write_bytes(b"{}")
        values[1] = str(outside)
    elif case == "dot_component":
        values[1] = f"{root}/./design.json"
    elif case == "dotdot_component":
        values[1] = f"{root}/nested/../design.json"
    elif case == "empty_component":
        values[1] = f"{root}//design.json"
    else:
        values[2] = values[1]

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(*values)

    assert caught.value.reason == "invalid_path"
    assert caught.value.source == "arguments"


@pytest.mark.parametrize(
    "location",
    ("root_intermediate", "root", "file_intermediate", "file"),
)
def test_rejects_symlinks_at_every_path_layer(tmp_path, location):
    module = _module()
    reader = module.read_input_pair
    real_parent = tmp_path / "real-parent"
    real_parent.mkdir()
    root = real_parent / "input"
    root.mkdir()
    data = root / "data"
    data.mkdir()
    design_path = data / "design.json"
    acceptance_path = root / "acceptance.json"
    design_path.write_bytes(_json_bytes(_design()))
    acceptance_path.write_bytes(_json_bytes(_acceptance()))

    if location == "root_intermediate":
        alias = tmp_path / "parent-alias"
        alias.symlink_to(real_parent, target_is_directory=True)
        root = alias / "input"
        design_path = root / "data" / "design.json"
        acceptance_path = root / "acceptance.json"
    elif location == "root":
        alias = tmp_path / "root-alias"
        alias.symlink_to(root, target_is_directory=True)
        root = alias
        design_path = root / "data" / "design.json"
        acceptance_path = root / "acceptance.json"
    elif location == "file_intermediate":
        alias = root / "data-alias"
        alias.symlink_to(data, target_is_directory=True)
        design_path = alias / "design.json"
    else:
        alias = root / "design-alias.json"
        alias.symlink_to(design_path)
        design_path = alias

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert caught.value.reason == "unreadable_input"
    assert caught.value.source in {"design", "none"}


@pytest.mark.parametrize("kind", ("directory", "fifo", "socket"))
def test_rejects_non_regular_inputs_without_blocking(
    tmp_path,
    monkeypatch,
    kind,
):
    module = _module()
    reader = module.read_input_pair
    root, _, acceptance_path = _input_files(tmp_path)
    design_path = root / f"not-regular-{kind}"
    if kind == "directory":
        design_path.mkdir()
    elif kind == "fifo":
        os.mkfifo(design_path)
    else:
        design_path.write_bytes(b"socket-placeholder")
        real_fstat = module.os.fstat
        first_call = True

        def socket_fstat(file_descriptor):
            nonlocal first_call
            result = real_fstat(file_descriptor)
            if not first_call:
                return result
            first_call = False
            return SimpleNamespace(
                st_mode=stat.S_IFSOCK,
                st_size=result.st_size,
                st_dev=result.st_dev,
                st_ino=result.st_ino,
            )

        monkeypatch.setattr(module.os, "fstat", socket_fstat)

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert caught.value.reason == "unreadable_input"
    assert caught.value.source == "design"


def test_rejects_size_above_the_fixed_limit(tmp_path):
    module = _module()
    reader = module.read_input_pair
    root, design_path, acceptance_path = _input_files(tmp_path)
    design_path.write_bytes(b"x" * 262145)

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert caught.value.reason == "size_limit_exceeded"
    assert caught.value.source == "design"


def test_rejects_distinct_names_for_the_same_open_file(tmp_path):
    module = _module()
    reader = module.read_input_pair
    root, design_path, _ = _input_files(tmp_path)
    acceptance_path = root / "acceptance-hard-link.json"
    os.link(design_path, acceptance_path)

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert caught.value.reason == "invalid_path"
    assert caught.value.source == "arguments"


def test_rejects_symlink_substituted_after_lexical_validation(
    tmp_path,
    monkeypatch,
):
    module = _module()
    reader = module.read_input_pair
    root, design_path, acceptance_path = _input_files(tmp_path)
    real_open = module.os.open
    substituted = False

    def substituting_open(path, flags, *args, **kwargs):
        nonlocal substituted
        if path == "design.json" and kwargs.get("dir_fd") is not None:
            original = root / "design-original.json"
            design_path.rename(original)
            design_path.symlink_to(original)
            substituted = True
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(module.os, "open", substituting_open)

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert substituted is True
    assert caught.value.reason == "unreadable_input"
    assert caught.value.source == "design"


@pytest.mark.parametrize("changed_field", ("st_size", "st_dev", "st_ino"))
def test_rejects_file_change_observed_after_read(
    tmp_path,
    monkeypatch,
    changed_field,
):
    module = _module()
    reader = module.read_input_pair
    root, design_path, acceptance_path = _input_files(tmp_path)
    real_fstat = module.os.fstat
    regular_calls = 0

    def changing_fstat(file_descriptor):
        nonlocal regular_calls
        result = real_fstat(file_descriptor)
        if not os.path.isfile(f"/dev/fd/{file_descriptor}"):
            return result
        regular_calls += 1
        if regular_calls != 2:
            return result
        values = {
            "st_mode": result.st_mode,
            "st_size": result.st_size,
            "st_dev": result.st_dev,
            "st_ino": result.st_ino,
        }
        values[changed_field] += 1
        return SimpleNamespace(**values)

    monkeypatch.setattr(module.os, "fstat", changing_fstat)

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert caught.value.reason == "unreadable_input"
    assert caught.value.source == "design"


def test_rejects_short_read_even_when_metadata_size_is_unchanged(
    tmp_path,
    monkeypatch,
):
    module = _module()
    reader = module.read_input_pair
    root, design_path, acceptance_path = _input_files(tmp_path)
    real_read = module.os.read
    shortened = False

    def short_read(file_descriptor, byte_count):
        nonlocal shortened
        data = real_read(file_descriptor, byte_count)
        if not shortened and data:
            shortened = True
            return data[:-1]
        return data

    monkeypatch.setattr(module.os, "read", short_read)

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert caught.value.reason == "unreadable_input"
    assert caught.value.source == "design"


def test_opens_every_component_without_following_symlinks(
    tmp_path,
    monkeypatch,
):
    module = _module()
    reader = module.read_input_pair
    root, design_path, acceptance_path = _input_files(tmp_path)
    real_open = module.os.open
    calls = []

    def recording_open(path, flags, *args, **kwargs):
        calls.append((path, flags, kwargs.get("dir_fd")))
        return real_open(path, flags, *args, **kwargs)

    monkeypatch.setattr(module.os, "open", recording_open)

    reader(str(root), str(design_path), str(acceptance_path))

    assert calls[0][0] == "/"
    directory_calls = [call for call in calls if call[0] not in {
        "design.json",
        "acceptance.json",
    }]
    file_calls = [call for call in calls if call[0] in {
        "design.json",
        "acceptance.json",
    }]
    assert len(directory_calls) >= len(root.parts)
    assert all(flags & os.O_NOFOLLOW for _, flags, _ in directory_calls)
    assert all(flags & os.O_DIRECTORY for _, flags, _ in directory_calls)
    assert all(flags & os.O_NOFOLLOW for _, flags, _ in file_calls)
    assert all(flags & os.O_NONBLOCK for _, flags, _ in file_calls)
    assert all(not flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT) for _, flags, _ in calls)


def test_rejects_when_required_non_follow_flags_are_unavailable(
    tmp_path,
    monkeypatch,
):
    module = _module()
    reader = module.read_input_pair
    root, design_path, acceptance_path = _input_files(tmp_path)
    monkeypatch.setattr(module.os, "O_NOFOLLOW", 0)

    with pytest.raises(module.DesignAcceptanceStop) as caught:
        reader(str(root), str(design_path), str(acceptance_path))

    assert caught.value.reason == "unreadable_input"
    assert caught.value.source == "none"


def test_reading_does_not_change_input_tree(tmp_path):
    root, design_path, acceptance_path = _input_files(tmp_path)
    before = sorted(
        (str(path.relative_to(root)), path.stat().st_mode, path.read_bytes())
        for path in root.iterdir()
    )

    _reader()(str(root), str(design_path), str(acceptance_path))

    after = sorted(
        (str(path.relative_to(root)), path.stat().st_mode, path.read_bytes())
        for path in root.iterdir()
    )
    assert after == before


def test_stops_do_not_retain_lower_level_exception_details(tmp_path):
    module = _module()

    with pytest.raises(module.DesignAcceptanceStop) as malformed:
        module.compare_inputs(b'{"secret":', _json_bytes(_acceptance()))
    assert malformed.value.__cause__ is None
    assert malformed.value.__context__ is None

    root, design_path, acceptance_path = _input_files(tmp_path)
    design_path.unlink()
    with pytest.raises(module.DesignAcceptanceStop) as unreadable:
        module.read_input_pair(
            str(root),
            str(design_path),
            str(acceptance_path),
        )
    assert unreadable.value.__cause__ is None
    assert unreadable.value.__context__ is None
