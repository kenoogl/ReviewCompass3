"""digest計算の正本（DEC-SHARED-FUNCTION-POLICY-001）。

canonical仕様（content_digest keyの除外、ensure_ascii=False、
separators=(",", ":")、sort_keys=True）は台帳の指紋計算の中核であり、
本moduleだけが正本である。意図的な複製は禁止（複製の禁止と共通関数化の
Human決定による）。変更はHuman承認事項。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import json


def sha256_hex(data):
    """bytesのSHA-256 hexdigestを返す。"""
    return hashlib.sha256(data).hexdigest()


def canonical_content_digest(document):
    """content_digest keyを除いたcanonical JSONのSHA-256 hexdigestを返す。"""
    payload = {
        key: value for key, value in document.items() if key != "content_digest"
    }
    return sha256_hex(
        json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    )
