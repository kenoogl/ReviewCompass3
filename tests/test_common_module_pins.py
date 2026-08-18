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
    "tools/common/digests.py": "fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7",
    "tools/common/errors.py": "1d2fefcc075080138f3ab9a8b19775e0ff0fb333e811d6918a06c6730236c4c0",
    "tools/common/paths.py": "039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec",
    "tools/common/roots.py": "478476817a5fcc755c7e96f33cfe2a68f093e0a4dd26ae3405cbac2ff8d33791",
    "tools/common/output.py": "77990e9d7781cb843f4fa2d9d1074776be6369efd4ced4a79c5f632719901d9b",
}


@pytest.mark.parametrize("relative, expected", sorted(_PINS.items()))
def test_common_module_is_pinned(relative, expected):
    actual = hashlib.sha256((PROJECT_ROOT / relative).read_bytes()).hexdigest()
    assert actual == expected, (
        f"{relative}が変更されている。正本の変更はHuman承認事項であり、"
        "承認記録とともに本pinを更新すること"
    )
