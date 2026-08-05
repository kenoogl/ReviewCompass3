"""TODOの機械管理部分を、公式Test receiptと参照fileから決定的に作る。

正本設計：docs/design/2026-08-05-record-generation-issue-plan-proposal.md
承認：`DEC-RECORD-GENERATION-PLAN-001`（TODO最小縦切りだけ）

## 何を機械が決めるか

このmoduleが更新するのは、次の2箇所だけである。

1. `## Git・Test`節の「直近の全Test」行。件数、Python版、pytest版、fallbackを公式receiptの
   構造化`test_summary`とfieldから作る。
2. `## 最新のauthority／Evidence`節にあるMarkdown linkのSHA-256値。参照fileのbytesから
   計算し直した値を書く。

## 何を機械が決めないか

- 人が書いた全体説明、判断理由、次の一作業などの自由文。既存bytesをそのまま保つ。
- 関連Testの意味的な選定、link label、link path、行の並び。
- 見出しの位置。見出しと対象行は完全一致でちょうど1回でなければならず、近傍探索や行番号で
  書き込まない。

## 参照Digestの扱い

参照のSHA-256は、人が手入力するのではなく、必ずfileのbytesから計算した値を書く。
計算した値がTODOに記録済みの値と食い違う場合は、参照対象の内容が変わったことを意味するため、
`reference_digest_mismatch`で停止し、TODOを一切変更しない。参照の追加・変更は人の判断を要する。

## 停止する条件

入力の欠落、receiptの不整合、見出しや対象行の欠落・重複、path異常、Digest不一致では、
候補を作らず停止する。停止したときはTODOのbytesを変更しない。
"""

import hashlib
import re
from pathlib import Path

from tools.development import pytest_summary


#: 機械が更新する行の先頭。完全一致でちょうど1回だけ現れなければならない。
FULL_TEST_PREFIX = "- 直近の全Test："

#: 対象節の見出し。完全一致でちょうど1回だけ現れなければならない。
EVIDENCE_HEADING = "## 最新のauthority／Evidence"
GIT_TEST_HEADING = "## Git・Test"

#: 参照linkの形。label、path、順序は保ち、Digestだけを機械が書く。
_REFERENCE = re.compile(
    r"^- \[(?P<label>[^\]\n]+)\]\((?P<path>[^)\n]+)\) — SHA-256 `(?P<sha256>[0-9a-f]{64})`$"
)

#: 公式receiptが持つfield。これ以外があれば受理しない。構造化集計の無い旧receiptも受理しない。
RECEIPT_FIELDS = (
    "receipt_kind",
    "runner_id",
    "runner_version",
    "recorded_at",
    "suite",
    "command",
    "configured_python",
    "resolved_python",
    "python_version",
    "pytest_version",
    "fallback_used",
    "config_digest",
    "source_state_digest",
    "status",
    "exit_code",
    "test_summary",
    "stdout",
    "stderr",
)

#: 全Test行へ出す内訳の並び。0の内訳は出さない。
_COUNT_ORDER = ("passed", "failed", "errors", "skipped", "xfailed", "xpassed")

STOP_CODES = (
    "todo_unavailable",
    "todo_heading_invalid",
    "todo_line_invalid",
    "receipt_unavailable",
    "receipt_invalid",
    "receipt_field_unknown",
    "receipt_not_passed",
    "receipt_fallback_used",
    "test_summary_invalid",
    "reference_path_invalid",
    "reference_digest_mismatch",
)


class TodoRecordGenerationError(Exception):
    """TODOの機械管理部分を安全に作れない。"""

    def __init__(self, code, detail=None):
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def _require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise TodoRecordGenerationError("receipt_invalid", label)
    return value.strip()


def validate_official_receipt(receipt):
    """公式receiptが、TODO自動更新の入力として使えるかを検査する。"""

    if not isinstance(receipt, dict):
        raise TodoRecordGenerationError("receipt_invalid", str(type(receipt)))
    expected = set(RECEIPT_FIELDS)
    unknown = sorted(set(receipt) - expected)
    if unknown:
        raise TodoRecordGenerationError("receipt_field_unknown", ",".join(unknown))
    missing = sorted(expected - set(receipt))
    if missing:
        raise TodoRecordGenerationError("receipt_field_unknown", ",".join(missing))
    if receipt["receipt_kind"] != "policy_test_verification_run":
        raise TodoRecordGenerationError("receipt_invalid", str(receipt["receipt_kind"]))

    try:
        pytest_summary.validate_summary(receipt["test_summary"])
    except pytest_summary.TestSummaryError as error:
        raise TodoRecordGenerationError("test_summary_invalid", str(error)) from error

    summary = receipt["test_summary"]
    if receipt["status"] != "passed" or summary["failed"] or summary["errors"]:
        raise TodoRecordGenerationError("receipt_not_passed", str(receipt["status"]))
    if receipt["fallback_used"] is not False:
        raise TodoRecordGenerationError(
            "receipt_fallback_used", str(receipt["fallback_used"])
        )
    _require_text(receipt["python_version"], "python_version")
    _require_text(receipt["pytest_version"], "pytest_version")
    _require_text(receipt["suite"], "suite")
    return True


def build_full_test_line(receipt):
    """receiptの構造化集計から「直近の全Test」行を作る。"""

    validate_official_receipt(receipt)
    summary = receipt["test_summary"]
    counts = ", ".join(
        f"{summary[field]} {field}" for field in _COUNT_ORDER if summary[field]
    ) or "0 passed"
    return (
        f"{FULL_TEST_PREFIX}venv公式runner `{counts}`、"
        f"Python {receipt['python_version'].strip()}、"
        f"pytest {receipt['pytest_version'].strip()}、"
        f"fallback {'true' if receipt['fallback_used'] else 'false'}"
    )


def _reference_target(project_root, relative_path):
    root = Path(project_root).resolve()
    path = Path(relative_path)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != relative_path:
        raise TodoRecordGenerationError("reference_path_invalid", relative_path)
    target = root / path
    if target.is_symlink():
        raise TodoRecordGenerationError("reference_path_invalid", relative_path)
    try:
        resolved = target.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError) as error:
        raise TodoRecordGenerationError(
            "reference_path_invalid", relative_path
        ) from error
    if not target.is_file():
        raise TodoRecordGenerationError("reference_path_invalid", relative_path)
    return target


def evidence_section_bounds(lines):
    """Evidence節の範囲を返す。見出しの次行から、次の`## `見出しの直前までである。

    節外のlinkは、この更新経路では収集も更新もDigest検証もしない。
    """

    starts = [index for index, line in enumerate(lines) if line == EVIDENCE_HEADING]
    if len(starts) != 1:
        raise TodoRecordGenerationError("todo_heading_invalid", EVIDENCE_HEADING)
    start = starts[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return start, end


def collect_reference_digests(document, *, project_root):
    """Evidence節**の中だけ**のlinkを読み、参照fileのbytesからDigestを計算し直す。"""

    lines = document.splitlines()
    start, end = evidence_section_bounds(lines)
    collected = []
    for line in lines[start:end]:
        matched = _REFERENCE.match(line)
        if matched is None:
            continue
        relative_path = matched.group("path")
        target = _reference_target(project_root, relative_path)
        collected.append(
            {
                "label": matched.group("label"),
                "path": relative_path,
                "recorded_sha256": matched.group("sha256"),
                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            }
        )
    if not collected:
        raise TodoRecordGenerationError("todo_heading_invalid", "no reference link")
    return tuple(collected)


def verify_reference_digests(document, *, project_root):
    """Evidence節に限定して、参照Digestが実bytesと一致することを確かめる。

    歴史的なglobal validatorとは別経路である。節外のlinkは対象にしない。
    """

    for reference in collect_reference_digests(document, project_root=project_root):
        if reference["sha256"] != reference["recorded_sha256"]:
            raise TodoRecordGenerationError(
                "reference_digest_mismatch", reference["path"]
            )
    return True


def build_todo_candidate(*, todo_path, receipt, project_root):
    """TODOの機械管理部分だけを差し替えた候補bytesを返す。fileへは書かない。"""

    path = Path(todo_path)
    try:
        document = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise TodoRecordGenerationError("todo_unavailable", str(path)) from error

    lines = document.splitlines(keepends=True)
    plain = document.splitlines()
    if plain.count(GIT_TEST_HEADING) != 1:
        raise TodoRecordGenerationError("todo_heading_invalid", GIT_TEST_HEADING)
    targets = [
        index for index, line in enumerate(plain) if line.startswith(FULL_TEST_PREFIX)
    ]
    if len(targets) != 1:
        raise TodoRecordGenerationError("todo_line_invalid", str(len(targets)))

    full_test_line = build_full_test_line(receipt)
    evidence_start, evidence_end = evidence_section_bounds(plain)
    references = collect_reference_digests(document, project_root=project_root)
    for reference in references:
        if reference["sha256"] != reference["recorded_sha256"]:
            raise TodoRecordGenerationError(
                "reference_digest_mismatch", reference["path"]
            )

    digests = {reference["path"]: reference["sha256"] for reference in references}
    updated = []
    for index, raw in enumerate(lines):
        stripped = raw.rstrip("\n")
        ending = raw[len(stripped):]
        if index == targets[0]:
            updated.append(full_test_line + ending)
            continue
        # Evidence節の外にある同形式のlinkは、Digestを含めてbytesを保つ。
        if evidence_start <= index < evidence_end:
            matched = _REFERENCE.match(stripped)
            if matched is not None:
                updated.append(
                    f"- [{matched.group('label')}]({matched.group('path')}) — "
                    f"SHA-256 `{digests[matched.group('path')]}`" + ending
                )
                continue
        updated.append(raw)
    return "".join(updated).encode("utf-8")
