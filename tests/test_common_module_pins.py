"""正本moduleの指紋pin（反証レビュー処置4）。

正本の変更はHuman承認事項（DEC-SHARED-FUNCTION-POLICY-001）。本pinの更新は
Human承認の記録を伴うこと。無断変更はこのテストが検出する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

_PINS = {
    "tools/common/__init__.py": "fdb99f627d54b0661d5b3d3f487c2a3e0266df9ac97ea642529c39e6b17774cd",
    "tools/common/digests.py": "db6b830592f5d57ef7b42b5ec32fd398f4c36957a978604166525fc54da3396f",
    "tools/common/errors.py": "1d2fefcc075080138f3ab9a8b19775e0ff0fb333e811d6918a06c6730236c4c0",
    "tools/common/paths.py": "daa325791b5bead80c240eb298c7084f6c26ff2d96ca850cc65449686cc4826d",
    "tools/common/output.py": "77990e9d7781cb843f4fa2d9d1074776be6369efd4ced4a79c5f632719901d9b",
}


@pytest.mark.parametrize("relative, expected", sorted(_PINS.items()))
def test_common_module_is_pinned(relative, expected):
    actual = hashlib.sha256((PROJECT_ROOT / relative).read_bytes()).hexdigest()
    assert actual == expected, (
        f"{relative}が変更されている。正本の変更はHuman承認事項であり、"
        "承認記録とともに本pinを更新すること"
    )
