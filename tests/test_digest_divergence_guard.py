"""digest実装の分岐検出テスト（digest系統合のHuman判断(b)、2026-08-08）。

11か所のdigest実装の重複は、標準libraryだけで動く自己完結scriptという
設計の代償であり、統合しない（統合はscript起動を壊した実測による）。
代わりに本テストが「全実装の出力が同一であること」を機械的に固定し、
canonical仕様の分岐を即REDで検出する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib
import json

import pytest

_SHA256_MEMBERS = [
    ("tools.development.bootstrap_environment", "_sha256"),
    ("tools.development.issue_resolution_pilot", "_sha256_bytes"),
    ("tools.development.issue_resolution_post_write", "_sha256"),
    ("tools.development.session_log_bootstrap", "_sha256"),
    ("tools.development.todo_compaction", "_sha256"),
    ("tools.development.todo_snapshot", "_sha256"),
    ("tools.session_logs.eventual_preservation", "_sha256"),
]

_CANONICAL_MEMBERS = [
    ("tools.development.candidate_ranking", "_content_digest"),
    ("tools.development.issue_intake_v4", "_canonical_digest"),
    ("tools.development.integration_exclusions", "content_digest"),
    ("tools.development.reuse_search_record", "_content_digest"),
]


def _functions(members):
    return [
        getattr(importlib.import_module(name), attribute)
        for name, attribute in members
    ]


class TestSha256FamilyStaysIdentical:
    @pytest.mark.parametrize(
        "payload",
        [b"", b"abc", "日本語のbytes".encode("utf-8"), b"\x00\xff" * 33],
    )
    def test_all_members_agree_with_the_oracle(self, payload):
        expected = hashlib.sha256(payload).hexdigest()
        for function in _functions(_SHA256_MEMBERS):
            assert function(payload) == expected


class TestCanonicalFamilyStaysIdentical:
    @pytest.mark.parametrize(
        "document",
        [
            {},
            {"content_digest": "既存値"},
            {"b": 1, "a": [1, {"z": None}], "content_digest": "x", "た": "文"},
            {"nested": {"content_digest": "内側は残る"}, "n": 1.5},
        ],
    )
    def test_all_members_agree_with_the_oracle(self, document):
        payload = {
            key: value
            for key, value in document.items()
            if key != "content_digest"
        }
        expected = hashlib.sha256(
            json.dumps(
                payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            ).encode("utf-8")
        ).hexdigest()
        for function in _functions(_CANONICAL_MEMBERS):
            assert function(dict(document)) == expected
