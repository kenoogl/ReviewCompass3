"""path境界判定の正本（DEC-SHARED-FUNCTION-POLICY-001、D系統）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import os
from pathlib import Path


def _same_entity_within(target, boundary):
    """実体（device・inode）でroot内かを判定する。

    macOS等では、大文字小文字差やUnicode正規化差だけが違うpathが同一の実体を
    指す。字句上の比較だけでは、root内のpathをroot外と誤判定する。
    """
    try:
        boundary_stat = os.stat(boundary)
    except OSError:
        return False
    for candidate in (target, *target.parents):
        try:
            candidate_stat = os.stat(candidate)
        except OSError:
            continue
        if os.path.samestat(candidate_stat, boundary_stat):
            return True
    return False


def within(path, root):
    """pathがrootと同一またはroot配下にあるかを返す。"""
    target = Path(path).resolve()
    boundary = Path(root).resolve()
    if target == boundary or boundary in target.parents:
        return True
    return _same_entity_within(target, boundary)
