"""複製禁止の掃討と恒久guard（反証レビュー処置1〜4）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import re
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _digests():
    return importlib.import_module("tools.common.digests")


class TestFileSha256:
    def test_matches_oracle(self, tmp_path):
        digests = _digests()
        target = tmp_path / "x.bin"
        target.write_bytes(b"\x00abc")
        assert digests.file_sha256(target) == hashlib.sha256(b"\x00abc").hexdigest()

    @pytest.mark.parametrize(
        "module_name, attribute",
        [
            ("tools.development.reuse_search_record", "file_sha256"),
            ("tools.development.candidate_ranking", "file_sha256"),
            ("tools.development.integration_exclusions", "file_sha256"),
            ("tools.development.work4a_rebuild_v3", "_file_sha256"),
            ("tools.task_contract.identity", "file_sha256"),
        ],
    )
    def test_members_bind(self, module_name, attribute):
        digests = _digests()
        module = importlib.import_module(module_name)
        assert getattr(module, attribute) is digests.file_sha256


class TestCanonicalSweep:
    @pytest.mark.parametrize(
        "module_name, attribute",
        [
            ("tools.development.todo_compaction", "_canonical_digest"),
            ("tools.development.issue_resolution_pilot", "_canonical_digest"),
            ("tools.development.issue_resolution_post_write", "canonical_digest"),
            ("tools.development.operation_routing", "canonical_digest"),
            ("tools.development.work4a_rebuild_v3", "_content_digest"),
            ("tools.task_contract.identity", "content_digest"),
        ],
    )
    def test_members_bind(self, module_name, attribute):
        digests = _digests()
        module = importlib.import_module(module_name)
        assert getattr(module, attribute) is digests.canonical_content_digest

    def test_frozen_residual_canonical_stays_identical(self):
        digests = _digests()
        snapshot = importlib.import_module("tools.development.todo_snapshot")
        document = {"b": 1, "content_digest": "x", "た": "文"}
        assert snapshot._canonical_digest(dict(document)) == (
            digests.canonical_content_digest(document)
        )


class TestWithinSweep:
    def test_config_binds(self):
        paths = importlib.import_module("tools.common.paths")
        config = importlib.import_module("tools.session_logs.config")
        assert config._within is paths.within


class TestSiblingIsolation:
    def test_except_one_does_not_catch_another(self):
        intake = importlib.import_module("tools.development.issue_intake_v4")
        identity = importlib.import_module("tools.task_contract.identity")
        with pytest.raises(identity.ContractError):
            try:
                raise identity.ContractError("c", "d")
            except intake.IntakeError:
                pytest.fail("IntakeErrorが他moduleの例外を誤捕捉した")


class TestNoRecreation:
    """再発明の恒久走査。複製禁止（DEC-SHARED-FUNCTION-POLICY-001）の機械化。"""

    _ALLOW = {"tools/common/digests.py", "tools/development/todo_snapshot.py"}

    def _sources(self):
        for path in sorted(PROJECT_ROOT.glob("tools/**/*.py")):
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            if relative in self._ALLOW:
                continue
            yield relative, path.read_text(encoding="utf-8")

    def test_no_canonical_copies(self):
        hits = [r for r, s in self._sources() if 'if key != "content_digest"' in s]
        assert hits == []

    def test_no_single_line_sha256_helpers(self):
        pattern = re.compile(
            r"def \w+\([a-z_]+\):\n\s+(?:\"\"\"[^\n]*\"\"\"\n\s+)?"
            r"return hashlib\.sha256\([a-z_]+\)\.hexdigest\(\)\n"
        )
        hits = [r for r, s in self._sources() if pattern.search(s)]
        assert hits == []

    def test_no_file_read_sha256_helpers(self):
        needle = "hashlib.sha256(Path(path).read_bytes()).hexdigest()"
        hits = [r for r, s in self._sources() if needle in s]
        assert hits == []

    def test_no_file_path_launch_strings(self):
        hits = [
            r for r, s in self._sources() if "python3 tools/" in s
        ]
        assert hits == []


class TestModuleLaunchReach:
    @pytest.mark.parametrize(
        "module_name",
        [
            "tools.session_logs.cli",
            "tools.session_logs.private_validation",
            "tools.session_logs.native_validation",
            "tools.session_logs.distribution_validation",
            "tools.session_logs.eventual_preservation",
            "tools.development.todo_update_path",
        ],
    )
    def test_dash_m_reaches_main(self, module_name):
        result = subprocess.run(
            [sys.executable, "-m", module_name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 2, result.stderr
        assert "ModuleNotFoundError" not in result.stderr
