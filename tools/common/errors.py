"""fail-closed例外の基底（DEC-SHARED-FUNCTION-POLICY-001、B系統）。

codeとdetailを保持しmessageを組み立てる基底クラスの正本。各moduleの
例外クラス名は捕捉の意味を担うため維持し、継承だけで結線する。
変更はHuman承認事項。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""


class FailClosedError(Exception):
    """fail-closed条件に触れたことをcode/detail付きで表す基底。"""

    def __init__(self, code, detail=None):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail
