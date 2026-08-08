"""機械可読出力の正本（DEC-SHARED-FUNCTION-POLICY-001、E系統）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import json


def print_json(document):
    """canonical並び（sort_keys、ensure_ascii=False）でJSONを1行印字する。"""
    print(json.dumps(document, ensure_ascii=False, sort_keys=True))
