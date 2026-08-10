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


class TestJsonCompatibilityIsEnforced:
    """F-A1反証：JSON互換でないrecordを同一Digestで合格させない。"""

    def _identity(self):
        return importlib.import_module("tools.task_contract.identity")

    @pytest.mark.parametrize(
        "document",
        [
            {1: "value"},
            {"nested": {2: "value"}},
            {"items": (1, 2)},
            {"nested": {"items": (1, 2)}},
            {"value": float("nan")},
            {"value": float("inf")},
            {"value": float("-inf")},
            {"nested": {"value": float("nan")}},
            {"value": {1, 2}},
            {"value": b"bytes"},
        ],
    )
    def test_non_json_compatible_document_is_rejected(self, document):
        digests = _digests()
        with pytest.raises(Exception) as caught:
            digests.canonical_content_digest(document)
        assert not isinstance(caught.value, AssertionError)

    @pytest.mark.parametrize(
        "left, right",
        [
            ({1: "value"}, {"1": "value"}),
            ({"items": (1, 2)}, {"items": [1, 2]}),
        ],
    )
    def test_distinct_values_never_share_a_digest(self, left, right):
        digests = _digests()
        try:
            left_digest = digests.canonical_content_digest(left)
        except Exception:
            return
        right_digest = digests.canonical_content_digest(right)
        assert left_digest != right_digest

    def test_seal_rejects_non_json_compatible_record(self):
        identity = self._identity()
        document = {
            "record_kind": "requirement_binding",
            "record_id": "RB-1",
            "record_version": 1,
            "items": (1, 2),
        }
        with pytest.raises(identity.ContractError):
            identity.seal(document)

    def test_validate_record_rejects_non_json_compatible_record(self):
        """修正前のcanonical仕様で自己整合するNaN recordを拒否する。

        照合値を不一致にすると、JSON互換検査が無くてもDigest不一致だけで
        拒否されてしまい、対象欠陥を検出できない（完了レビューv1 F-CG-COMP-001）。
        修正前の仕様（allow_nan既定）で計算した正しいDigestを与える。
        """
        identity = self._identity()
        document = {
            "record_kind": "requirement_binding",
            "record_id": "RB-1",
            "record_version": 1,
            "value": float("nan"),
        }
        legacy_digest = hashlib.sha256(
            json.dumps(
                document,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        document["content_digest"] = legacy_digest
        with pytest.raises(identity.ContractError):
            identity.validate_record(document)

    def test_canonical_bytes_rejects_non_json_compatible_value(self):
        identity = self._identity()
        with pytest.raises(identity.ContractError):
            identity.canonical_bytes({"items": (1, 2)})


class TestExistingDigestValuesAreUnchanged:
    """正例：JSON互換な既存recordのDigest値は修正前と一致する。"""

    @pytest.mark.parametrize(
        "document",
        [
            {"b": 1, "a": [1, {"z": None}], "content_digest": "x", "た": "文"},
            {"値": "文字列", "flag": True, "none": None, "num": 1, "real": 1.5},
            {"nested": {"list": [1, "a", None, False]}},
        ],
    )
    def test_known_documents_keep_their_digest(self, document):
        digests = _digests()
        oracle = hashlib.sha256(
            json.dumps(
                {
                    key: value
                    for key, value in document.items()
                    if key != "content_digest"
                },
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        assert digests.canonical_content_digest(document) == oracle

    def test_real_ledger_records_keep_their_digest(self):
        """実台帳の代表recordが、修正後も宣言Digestと一致し続ける。"""
        digests = _digests()
        root = PROJECT_ROOT / "records" / "development"
        checked = 0
        for path in sorted(root.glob("*.json"))[:200]:
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if not isinstance(document, dict):
                continue
            declared = document.get("content_digest")
            if not isinstance(declared, str) or len(declared) != 64:
                continue
            assert digests.canonical_content_digest(document) == declared, path
            checked += 1
        assert checked >= 1
