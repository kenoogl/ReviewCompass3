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
import math
from pathlib import Path

from tools.common.errors import FailClosedError


class DigestInputError(FailClosedError):
    """Digest計算の入力がJSON互換ではない（fail-closed）。"""

    def __init__(self, detail=None):
        super().__init__("digest_input_not_json_compatible", detail)


def sha256_hex(data):
    """bytesのSHA-256 hexdigestを返す。"""
    return hashlib.sha256(data).hexdigest()


def require_json_compatible(value, _path="$"):
    """構造化正本がJSON互換の閉じたschemaであることを検査する。

    非文字列key・非JSON型（tuple・set・bytes等）・非有限数を拒否する。
    これらは`json.dumps`が黙って別表現へ潰し、異なるPython値が同一Digestに
    なる経路を作るため、Digest計算の前にfail-closedで止める。
    """
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise DigestInputError(f"{_path}: non-string key {key!r}")
            require_json_compatible(item, f"{_path}.{key}")
        return value
    if isinstance(value, list):
        for index, item in enumerate(value):
            require_json_compatible(item, f"{_path}[{index}]")
        return value
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise DigestInputError(f"{_path}: non-finite number")
        return value
    raise DigestInputError(f"{_path}: unsupported type {type(value).__name__}")


def canonical_json_bytes(value):
    """canonical JSONのbytes。JSON互換でない入力は拒否する。"""
    require_json_compatible(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
        allow_nan=False,
    ).encode("utf-8")


def canonical_content_digest(document):
    """content_digest keyを除いたcanonical JSONのSHA-256 hexdigestを返す。"""
    if not isinstance(document, dict):
        raise DigestInputError("document must be a mapping")
    payload = {
        key: value for key, value in document.items() if key != "content_digest"
    }
    return sha256_hex(canonical_json_bytes(payload))


def file_sha256(path):
    """fileの現在bytesのSHA-256 hexdigestを返す。"""
    return sha256_hex(Path(path).read_bytes())
