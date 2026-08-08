"""共通digest正本とmodule起動（DEC-SHARED-FUNCTION-POLICY-001）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _digests():
    return importlib.import_module("tools.common.digests")


class TestSharedFunctions:
    def test_sha256_known_vector_and_oracle(self):
        digests = _digests()
        assert digests.sha256_hex(b"abc") == (
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        )
        payload = "日本語のbytes".encode("utf-8")
        assert digests.sha256_hex(payload) == hashlib.sha256(payload).hexdigest()

    def test_canonical_matches_oracle_and_excludes_digest_key(self):
        digests = _digests()
        document = {"b": 1, "a": [1, {"z": None}], "content_digest": "x", "た": "文"}
        expected = hashlib.sha256(
            json.dumps(
                {"b": 1, "a": [1, {"z": None}], "た": "文"},
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        assert digests.canonical_content_digest(document) == expected


class TestNoDuplication:
    """10定義が正本へ結線され、写しが型として存在しないことを固定する。"""

    @pytest.mark.parametrize(
        "module_name, attribute",
        [
            ("tools.development.bootstrap_environment", "_sha256"),
            ("tools.development.issue_resolution_pilot", "_sha256_bytes"),
            ("tools.development.issue_resolution_post_write", "_sha256"),
            ("tools.development.session_log_bootstrap", "_sha256"),
            ("tools.development.todo_compaction", "_sha256"),
            # todo_snapshot.pyは凍結契約のfile指紋固定により残置（凍結解除はHuman判断）
            ("tools.session_logs.eventual_preservation", "_sha256"),
        ],
    )
    def test_sha256_members_bind_to_the_shared_function(self, module_name, attribute):
        digests = _digests()
        module = importlib.import_module(module_name)
        assert getattr(module, attribute) is digests.sha256_hex

    @pytest.mark.parametrize(
        "module_name, attribute",
        [
            ("tools.development.candidate_ranking", "_content_digest"),
            ("tools.development.issue_intake_v4", "_canonical_digest"),
            ("tools.development.integration_exclusions", "content_digest"),
            ("tools.development.reuse_search_record", "_content_digest"),
        ],
    )
    def test_canonical_members_bind_to_the_shared_function(self, module_name, attribute):
        digests = _digests()
        module = importlib.import_module(module_name)
        assert getattr(module, attribute) is digests.canonical_content_digest

    def test_frozen_residual_copy_stays_identical(self):
        digests = _digests()
        snapshot = importlib.import_module("tools.development.todo_snapshot")
        for payload in (b"", b"abc", "日本語".encode("utf-8")):
            assert snapshot._sha256(payload) == digests.sha256_hex(payload)


class TestModuleLaunch:
    """documented手順のmodule起動（-m）がrepository根元から動くことを固定する。"""

    @pytest.mark.parametrize(
        "module_name",
        [
            "tools.development.todo_compaction",
            "tools.development.todo_handoff",
        ],
    )
    def test_dash_m_launch_succeeds(self, module_name):
        result = subprocess.run(
            [sys.executable, "-m", module_name, "TODO_NEXT_SESSION.md"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
