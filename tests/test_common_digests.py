"""共通digest module（digest系統合、DEC-CONSOLIDATION-EVAL2-APPROVAL-001手順5）の暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest


def _digests():
    return importlib.import_module("tools.common.digests")


class TestSha256Hex:
    def test_known_vector(self):
        digests = _digests()
        assert digests.sha256_hex(b"abc") == (
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        )

    def test_matches_independent_oracle(self):
        digests = _digests()
        payload = "日本語もbytesで".encode("utf-8")
        assert digests.sha256_hex(payload) == hashlib.sha256(payload).hexdigest()


class TestCanonicalContentDigest:
    def test_matches_independent_oracle_and_excludes_digest_key(self):
        digests = _digests()
        document = {"b": 1, "a": [1, 2], "content_digest": "既存値", "た": "文"}
        expected = hashlib.sha256(
            json.dumps(
                {"b": 1, "a": [1, 2], "た": "文"},
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        assert digests.canonical_content_digest(document) == expected

    def test_digest_key_absence_gives_same_result(self):
        digests = _digests()
        with_key = {"x": 1, "content_digest": "zzz"}
        without_key = {"x": 1}
        assert digests.canonical_content_digest(with_key) == (
            digests.canonical_content_digest(without_key)
        )


class TestAliasBinding:
    """11定義が共通関数へ結線され、再分岐が型として起きないことを固定する。"""

    @pytest.mark.parametrize(
        "module_name, attribute",
        [
            ("tools.development.bootstrap_environment", "_sha256"),
            ("tools.development.issue_resolution_pilot", "_sha256_bytes"),
            ("tools.development.issue_resolution_post_write", "_sha256"),
            ("tools.development.session_log_bootstrap", "_sha256"),
            ("tools.development.todo_compaction", "_sha256"),
            ("tools.development.todo_snapshot", "_sha256"),
            ("tools.session_logs.eventual_preservation", "_sha256"),
        ],
    )
    def test_sha256_family_is_the_common_function(self, module_name, attribute):
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
    def test_canonical_family_is_the_common_function(self, module_name, attribute):
        digests = _digests()
        module = importlib.import_module(module_name)
        assert getattr(module, attribute) is digests.canonical_content_digest

    def test_public_wrapper_still_works(self):
        digests = _digests()
        intake = importlib.import_module("tools.development.issue_intake_v4")
        document = {"k": "v"}
        assert intake.canonical_digest(document) == (
            digests.canonical_content_digest(document)
        )
