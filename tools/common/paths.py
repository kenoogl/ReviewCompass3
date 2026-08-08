"""path境界判定の正本（DEC-SHARED-FUNCTION-POLICY-001、D系統）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

from pathlib import Path


def within(path, root):
    """pathがrootと同一またはroot配下にあるかを返す。"""
    target = Path(path).resolve()
    boundary = Path(root).resolve()
    return target == boundary or boundary in target.parents
