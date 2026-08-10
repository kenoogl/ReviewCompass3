"""共通部品errors/paths/output（DEC-SHARED-FUNCTION-POLICY-001、B/D/E系統）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib
import json
import os
import unicodedata

import pytest

_EXCEPTION_MEMBERS = [
    ("tools.development.issue_intake_v4", "IntakeError"),
    ("tools.development.python_ast_boundary_check", "PythonAstBoundaryError"),
    ("tools.development.structured_argv_executor", "StructuredArgvExecutorError"),
    ("tools.development.task_python_cache", "TaskPythonCacheError"),
    ("tools.development.todo_record_generation", "TodoRecordGenerationError"),
    ("tools.development.todo_update_path", "TodoUpdatePathError"),
    ("tools.task_contract.identity", "ContractError"),
]

_WITHIN_MEMBERS = [
    "tools.session_logs.distribution_validation",
    "tools.session_logs.private_validation",
    "tools.session_logs.eventual_preservation",
    "tools.session_logs.native_validation",
]


def _common(name):
    return importlib.import_module(f"tools.common.{name}")


class TestFailClosedError:
    def test_message_with_detail(self):
        errors = _common("errors")
        error = errors.FailClosedError("code_x", "detail_y")
        assert str(error) == "code_x: detail_y"
        assert error.code == "code_x"
        assert error.detail == "detail_y"

    def test_message_without_detail_and_empty_detail(self):
        errors = _common("errors")
        assert str(errors.FailClosedError("code_x")) == "code_x"
        assert str(errors.FailClosedError("code_x", "")) == "code_x"
        assert errors.FailClosedError("code_x").detail is None

    @pytest.mark.parametrize("module_name, class_name", _EXCEPTION_MEMBERS)
    def test_members_inherit_and_do_not_redefine_init(self, module_name, class_name):
        errors = _common("errors")
        cls = getattr(importlib.import_module(module_name), class_name)
        assert issubclass(cls, errors.FailClosedError)
        assert cls.__init__ is errors.FailClosedError.__init__
        raised = cls("c1", "d1")
        assert str(raised) == "c1: d1"
        assert (raised.code, raised.detail) == ("c1", "d1")


class TestWithin:
    def test_behavior(self, tmp_path):
        paths = _common("paths")
        inner = tmp_path / "a" / "b.txt"
        inner.parent.mkdir()
        inner.write_text("x", encoding="utf-8")
        assert paths.within(inner, tmp_path) is True
        assert paths.within(tmp_path, tmp_path) is True
        assert paths.within(tmp_path.parent, tmp_path) is False

    @pytest.mark.parametrize("module_name", _WITHIN_MEMBERS)
    def test_members_bind_to_the_shared_function(self, module_name):
        paths = _common("paths")
        module = importlib.import_module(module_name)
        assert module._within is paths.within


class TestPrintJson:
    def test_output_is_canonical(self, capsys):
        output = _common("output")
        output.print_json({"b": 1, "a": "文"})
        printed = capsys.readouterr().out
        assert printed == '{"a": "文", "b": 1}\n'
        assert json.loads(printed) == {"a": "文", "b": 1}

    @pytest.mark.parametrize(
        "module_name, attribute",
        [
            ("tools.session_logs.cli", "_print_json"),
            ("tools.session_logs.private_validation", "_print_result"),
            ("tools.development.todo_update_path", "_report"),
        ],
    )
    def test_members_bind_to_the_shared_function(self, module_name, attribute):
        output = _common("output")
        module = importlib.import_module(module_name)
        assert getattr(module, attribute) is output.print_json


class TestWithinHandlesPathAliases:
    """F-A2反証：case差・Unicode正規化差だけの実在pathをroot外と誤判定しない。"""

    def _paths(self):
        return importlib.import_module("tools.common.paths")

    def test_case_alias_matches_samefile(self, tmp_path):
        paths = self._paths()
        root = tmp_path / "Root"
        root.mkdir()
        alias = tmp_path / "root"
        if not os.path.exists(alias):
            pytest.skip("case-insensitive filesystem is required")
        assert os.path.samefile(alias, root) is True
        assert paths.within(alias, root) is True

    def test_unicode_form_alias_matches_samefile(self, tmp_path):
        paths = self._paths()
        composed = tmp_path / unicodedata.normalize("NFC", "ガ")
        composed.mkdir()
        decomposed = tmp_path / unicodedata.normalize("NFD", "ガ")
        if not os.path.exists(decomposed):
            pytest.skip("unicode-normalising filesystem is required")
        assert os.path.samefile(decomposed, composed) is True
        assert paths.within(decomposed, composed) is True

    def test_child_under_case_alias_is_inside(self, tmp_path):
        paths = self._paths()
        root = tmp_path / "Root"
        root.mkdir()
        child = root / "inner.txt"
        child.write_text("x", encoding="utf-8")
        alias_child = tmp_path / "root" / "inner.txt"
        if not os.path.exists(alias_child):
            pytest.skip("case-insensitive filesystem is required")
        assert paths.within(alias_child, root) is True

    def test_outside_path_is_still_rejected(self, tmp_path):
        paths = self._paths()
        root = tmp_path / "root"
        root.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        assert paths.within(outside, root) is False
        assert paths.within(tmp_path, root) is False

    def test_missing_path_falls_back_to_resolved_comparison(self, tmp_path):
        paths = self._paths()
        root = tmp_path / "root"
        root.mkdir()
        assert paths.within(root / "absent" / "file.txt", root) is True
        assert paths.within(tmp_path / "absent-outside.txt", root) is False
