"""依頼recordの雛形生成（assemble）と機械検査（check）。

契約011 §5.1・§7の実装。外部送信・外部起動を行わない完全local処理。
核（redaction・digests・縦Bの命名導出・許可model定数）は共有部品を
読取り流用し、薄い包みだけを持つ（利用者裁定2026-08-17）。
"""

import hashlib
import re
import subprocess as _subprocess
from pathlib import Path

from tools.common.digests import file_sha256
from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
from tools.reviewer_launch.record import verdict_record_relative_path
from tools.session_logs.redaction import (
    default_pattern_rules,
    find_high_entropy,
)


REQUEST_TYPES = ("contract_review", "completion_review")
_TYPE_LABELS = {
    "contract_review": "実装開始前の契約定義反証",
    "completion_review": "実装完了レビュー",
}
OUTPUT_DIRECTORY = "records/session-handoffs"
PLACEHOLDER_PREFIX = "<<記入:"
# 破損placeholderの断片検知（cr-011-001所見の反映）
PLACEHOLDER_FRAGMENTS = ("<<記入", "記入:")

# 契約§7.3：契約009 v2 §7と同値の除外3形式。本契約の直書き定数であり、
# 設定・環境・引数から変更できない。同値性は試験で固定する。
HIGH_ENTROPY_ALLOW_PATTERNS = (
    r"[0-9a-f]{40}",
    r"[0-9a-f]{64}",
    r"(?=.*[G-Zg-z_])[A-Za-z0-9]{1,20}(?:[-_]+[A-Za-z0-9]{1,20})+",
)

REQUIRED_SECTIONS = (
    "対象と固定",
    "開始時の鮮度検査",
    "反証点",
    "判定の形式",
    "判断済み・範囲外",
    "手順",
)

_SLUG_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
_DATE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
_DIGEST_ROW_PATTERN = re.compile(r"^([0-9a-f]{64})  (\S+)$", re.MULTILINE)
_MODEL_PATTERN = re.compile(r"許可model `([^`]+)`")
_POINT_PATTERN = re.compile(r"^(\d+)\.\s", re.MULTILINE)


class BuilderStop(Exception):
    """依頼recordを安全に組み立てまたは検査できないため停止した。"""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def _run_git(repository, *arguments):
    completed = _subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise BuilderStop("git_command_failed")
    return completed.stdout


def _git_succeeds(repository, *arguments):
    completed = _subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def _scan_sensitive(text):
    for rule in default_pattern_rules():
        if re.search(rule.pattern, text):
            raise BuilderStop("sensitive_data_remaining")
    if find_high_entropy(
        text, allow_patterns=HIGH_ENTROPY_ALLOW_PATTERNS
    ):
        raise BuilderStop("sensitive_data_remaining")


def _render(
    *,
    title,
    kind_label,
    record_date,
    base_commit_line,
    digest_table,
    repository_absolute,
    record_relative,
    verdict_relative,
    model,
):
    return (
        "# %s 独立確認依頼record（headless起動対象・Claude→Reviewer）\n"
        "\n"
        "- 作成日：%s\n"
        "- 依頼元：Claude（操縦）\n"
        "- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、"
        "許可model `%s`）\n"
        "- 起動方式：`reviewcompass3-reviewer-launch launch`による"
        "headless機械起動（利用者の明示指示後）。fallbackは暫定手動体制\n"
        "- レビュー種別：%s（読み取り専用・repositoryへの書込みなし）\n"
        "%s"
        "\n"
        "## 1. 対象と固定（SHA-256）\n"
        "\n"
        "```text\n"
        "%s\n"
        "```\n"
        "\n"
        "## 2. 開始時の鮮度検査\n"
        "\n"
        "起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で"
        "本recordを開き、対象であることを確認する。digestの機械計算が"
        "この実行環境で行えない場合は、freshnessへ`not_computable`と"
        "理由を記載する（内容が明らかに別物ならmismatchとして判定せず"
        "停止）。§1のdigest表は本record作成時点の固定値である。\n"
        "\n"
        "## 3. Reviewer（あなた）への依頼：反証点\n"
        "\n"
        "あなたは独立したReviewerです。次の反証点をそれぞれ反証的に"
        "検査し、各findingへ根拠（節番号・file・行）を付けてください。\n"
        "\n"
        "<<記入:反証点を「1.」「2.」の番号つき一覧でここへ列挙する>>\n"
        "\n"
        "## 4. 判定の形式\n"
        "\n"
        "- headless起動時は、起動promptが指定するJSON schemaに完全に"
        "従う構造化出力だけで返す。`verdict`は5語彙（`verified`／"
        "`verified_with_findings`／`rejected`／`stale_target`／"
        "`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、"
        "実施できなかった検査は`unexamined`配列へ明示、`summary`は"
        "日本語で書く。\n"
        "- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を"
        "日本語の文章で返し、冒頭にmodel名を記載する。\n"
        "\n"
        "## 5. 判断済み・範囲外（蒸し返し不要）\n"
        "\n"
        "<<記入:判断済み事項・範囲外・事実の明示をここへ列挙する>>\n"
        "\n"
        "## 6. 手順（Human・Claude向け）\n"
        "\n"
        "1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に"
        "従う）。\n"
        "2. Claudeが単体入口を実行する：\n"
        "\n"
        "```text\n"
        "reviewcompass3-reviewer-launch launch \\\n"
        "  --repository %s \\\n"
        "  --request %s \\\n"
        "  --expected-sha256 <本record commit後のSHA-256> \\\n"
        "  --private-root <repo外私有領域の絶対パス> \\\n"
        "  --run-id <実行識別子>\n"
        "```\n"
        "\n"
        "3. アダプタが判定recordを`%s`へ機械転記して単独commitし、"
        "事後照合4点を実行する。\n"
        "4. `verified`系（blocking 0件）なら次のHuman判断へ進み、"
        "blocking所見があれば停止して利用者へ諮る。\n"
        % (
            title,
            record_date,
            model,
            kind_label,
            base_commit_line,
            digest_table,
            repository_absolute,
            record_relative,
            verdict_relative,
        )
    )


def assemble(
    *,
    repository,
    request_type,
    record_date,
    slug,
    title,
    target_paths,
):
    """類型の雛形から依頼record草稿を生成する（new-only書込み）。"""

    if request_type not in REQUEST_TYPES:
        raise BuilderStop("request_type_unknown")
    if (
        not isinstance(record_date, str)
        or _DATE_PATTERN.fullmatch(record_date) is None
    ):
        raise BuilderStop("invalid_record_date")
    if not isinstance(slug, str) or _SLUG_PATTERN.fullmatch(slug) is None:
        raise BuilderStop("invalid_slug")
    if not isinstance(title, str) or not title.strip():
        raise BuilderStop("invalid_title")
    targets = [str(value) for value in (target_paths or ())]
    if not targets:
        raise BuilderStop("digest_table_empty")

    root = Path(repository)
    rows = []
    for relative in targets:
        try:
            digest = file_sha256(root / relative)
        except OSError as error:
            raise BuilderStop("request_target_unreadable") from error
        rows.append("%s  %s" % (digest, relative))

    record_name = "%s-%s-request-v1.md" % (record_date, slug)
    record_relative = "%s/%s" % (OUTPUT_DIRECTORY, record_name)
    output = root / record_relative
    if output.exists():
        raise BuilderStop("output_already_exists")

    base_commit_line = ""
    if request_type == "completion_review":
        head = _run_git(root, "rev-parse", "HEAD").strip()
        base_commit_line = "- 実装基準commit：`%s`\n" % head

    if not ALLOWED_RESPONSE_MODELS:
        raise BuilderStop("allowed_models_unfixed")
    body = _render(
        title=title.strip(),
        kind_label=_TYPE_LABELS[request_type],
        record_date=record_date,
        base_commit_line=base_commit_line,
        digest_table="\n".join(rows),
        repository_absolute=str(root.resolve()),
        record_relative=record_relative,
        verdict_relative=verdict_record_relative_path(record_relative),
        model=ALLOWED_RESPONSE_MODELS[0],
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(body, encoding="utf-8")
    return {
        "status": "ok",
        "record_relative_path": record_relative,
        "request_type": request_type,
        "digest_rows": len(rows),
    }


def _section_text(text, key):
    lines = text.splitlines()
    collected = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = key in line
            continue
        if inside:
            collected.append(line)
    return "\n".join(collected)


def check(*, repository, request_relative_path):
    """完成した依頼recordを7項目＋check-ignore＋機微検査で検査する。

    contentの検査を先に行い、Git状態の検査（commit済み等）を最後に行う
    （契約§7.2：commit前の実行でrequest_record_uncommittedだけが不合格に
    なる状態は正常な途中経過。最終合格はcommit済み状態での全項目合格）。
    """

    root = Path(repository)
    name = str(request_relative_path).rsplit("/", 1)[-1]
    if "-request-" not in name:
        raise BuilderStop("request_name_invalid")
    verdict_relative = verdict_record_relative_path(
        str(request_relative_path)
    )

    path = root / request_relative_path
    try:
        data = path.read_bytes()
    except OSError as error:
        raise BuilderStop("request_record_unreadable") from error
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise BuilderStop("invalid_utf8") from error

    for section in REQUIRED_SECTIONS:
        if not any(
            line.startswith("## ") and section in line
            for line in text.splitlines()
        ):
            raise BuilderStop("required_section_missing")

    for fragment in (PLACEHOLDER_PREFIX, *PLACEHOLDER_FRAGMENTS):
        if fragment in text:
            raise BuilderStop("placeholder_remaining")

    points_section = _section_text(text, "反証点")
    numbers = _POINT_PATTERN.findall(points_section)
    if not numbers:
        raise BuilderStop("fill_in_missing")
    if len(set(numbers)) != len(numbers):
        raise BuilderStop("request_point_identifiers_invalid")
    decided_section = _section_text(text, "判断済み・範囲外")
    if not any(line.strip() for line in decided_section.splitlines()):
        raise BuilderStop("fill_in_missing")

    table_section = _section_text(text, "対象と固定")
    rows = _DIGEST_ROW_PATTERN.findall(table_section)
    if not rows:
        raise BuilderStop("digest_table_empty")
    for digest, relative in rows:
        target = root / relative
        try:
            payload = target.read_bytes()
        except OSError as error:
            raise BuilderStop("digest_reference_missing") from error
        if hashlib.sha256(payload).hexdigest() != digest:
            raise BuilderStop("digest_mismatch")

    for required in ("依頼元：", "依頼先：", "読み取り専用"):
        if required not in text:
            raise BuilderStop("required_statement_missing")
    model_match = _MODEL_PATTERN.search(text)
    if model_match is None:
        raise BuilderStop("required_statement_missing")
    if model_match.group(1) not in ALLOWED_RESPONSE_MODELS:
        raise BuilderStop("model_not_allowed")

    if text.count("```") % 2 != 0:
        raise BuilderStop("fence_unbalanced")

    _scan_sensitive(text)

    for _, relative in rows:
        if not _run_git(root, "ls-files", "--", relative).strip():
            raise BuilderStop("digest_reference_uncommitted")
    if _git_succeeds(
        root, "check-ignore", "-q", str(request_relative_path)
    ):
        raise BuilderStop("request_record_ignored")
    if not _run_git(
        root, "ls-files", "--", str(request_relative_path)
    ).strip():
        raise BuilderStop("request_record_uncommitted")
    if _run_git(
        root, "status", "--porcelain", "--", str(request_relative_path)
    ).strip():
        raise BuilderStop("request_record_uncommitted")

    request_type = (
        "completion_review"
        if _TYPE_LABELS["completion_review"] in text
        else "contract_review"
    )
    return {
        "status": "ok",
        "operation": "request_builder_check",
        "request": {
            "path": str(request_relative_path),
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        "request_type": request_type,
        "digest_rows": len(rows),
        "verdict_record_relative_path": verdict_relative,
    }
