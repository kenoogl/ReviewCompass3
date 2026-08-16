"""判定schemaの検証・判定recordの機械転記・事後照合。

契約010 §7.2（判定schema）・§7.3（事後照合4点）・§9-5〜6の実装。
判定の正本はcommitted recordであり、転記と単独commitは機械処理が行う。
"""

import hashlib
import json
import re
import subprocess as _subprocess
from pathlib import Path


VERDICT_VOCABULARY = (
    "verified",
    "verified_with_findings",
    "rejected",
    "stale_target",
    "unable",
)
FRESHNESS_RESULTS = ("match", "mismatch", "not_computable")
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
_REQUIRED_KEYS = (
    "reviewer",
    "freshness",
    "target",
    "findings",
    "unexamined",
    "verdict",
    "summary",
)
_FINDING_KEYS = (
    "identifier",
    "severity",
    "blocking",
    "claim",
    "evidence_path",
    "evidence_location",
)
_JSON_BLOCK_PATTERN = re.compile(
    r"```json\n(.*?)\n```",
    re.DOTALL,
)


class VerdictInvalid(Exception):
    """判定JSONが契約§7.2のschemaへ適合しない。"""


class TranscriptionStop(Exception):
    """判定recordの転記または事後照合を安全に完了できない。"""

    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


def _require(condition, message):
    if not condition:
        raise VerdictInvalid(message)


def _require_text(value, message):
    _require(isinstance(value, str) and bool(value), message)


def validate_verdict(value):
    """契約§7.2の必須項目・語彙・一意性を検査し、valueを返す。"""

    _require(isinstance(value, dict), "verdict document must be an object")
    for key in _REQUIRED_KEYS:
        _require(key in value, "missing required key: %s" % key)

    reviewer = value["reviewer"]
    _require(isinstance(reviewer, dict), "reviewer must be an object")
    _require_text(reviewer.get("provider"), "reviewer.provider required")
    _require_text(reviewer.get("model"), "reviewer.model required")

    freshness = value["freshness"]
    _require(isinstance(freshness, dict), "freshness must be an object")
    _require(
        _SHA256_PATTERN.fullmatch(freshness.get("expected") or "")
        is not None,
        "freshness.expected must be sha256",
    )
    result = freshness.get("result")
    _require(
        result in FRESHNESS_RESULTS,
        "freshness.result outside fixed vocabulary",
    )
    if result == "mismatch":
        raise VerdictInvalid("freshness mismatch reported by reviewer")
    if result == "not_computable":
        _require_text(
            freshness.get("reason"),
            "freshness.result not_computable requires reason",
        )
    if result == "match":
        _require(
            freshness.get("observed") == freshness.get("expected"),
            "freshness.observed must equal expected on match",
        )

    target = value["target"]
    _require(isinstance(target, dict), "target must be an object")
    _require_text(target.get("path"), "target.path required")
    _require_text(target.get("commit"), "target.commit required")

    findings = value["findings"]
    _require(isinstance(findings, list), "findings must be an array")
    identifiers = []
    for finding in findings:
        _require(isinstance(finding, dict), "finding must be an object")
        for key in _FINDING_KEYS:
            _require(key in finding, "finding missing key: %s" % key)
        _require_text(finding["identifier"], "finding.identifier required")
        _require_text(finding["severity"], "finding.severity required")
        _require(
            isinstance(finding["blocking"], bool),
            "finding.blocking must be boolean",
        )
        _require_text(finding["claim"], "finding.claim required")
        _require_text(finding["evidence_path"], "finding.evidence_path required")
        _require_text(
            finding["evidence_location"],
            "finding.evidence_location required",
        )
        identifiers.append(finding["identifier"])
    _require(
        len(set(identifiers)) == len(identifiers),
        "finding identifiers must be unique",
    )

    unexamined = value["unexamined"]
    _require(isinstance(unexamined, list), "unexamined must be an array")
    for entry in unexamined:
        _require_text(entry, "unexamined entries must be text")

    _require(
        value["verdict"] in VERDICT_VOCABULARY,
        "verdict outside fixed vocabulary",
    )
    _require_text(value["summary"], "summary required")
    return value


def _run_git(repository, *arguments):
    completed = _subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise TranscriptionStop("git_command_failed")
    return completed.stdout


def _git_succeeds(repository, *arguments):
    completed = _subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def current_commit(repository):
    return _run_git(repository, "rev-parse", "HEAD").strip()


def verdict_record_relative_path(request_relative_path):
    """依頼record名から判定record名を決定的に導出する。"""

    parts = request_relative_path.rsplit("/", 1)
    directory = parts[0] if len(parts) == 2 else ""
    name = parts[-1]
    if "-request-" in name:
        head, _, tail = name.rpartition("-request-")
        new_name = head + "-verdict-" + tail
    elif name.endswith(".md"):
        new_name = name[:-3] + "-verdict-v1.md"
    else:
        new_name = name + "-verdict-v1.md"
    if directory:
        return directory + "/" + new_name
    return new_name


def _backend_provider(backend_name):
    from tools.reviewer_launch.core import BACKENDS

    backend = BACKENDS.get(backend_name)
    if backend is None:
        raise TranscriptionStop("backend_unknown")
    return backend["provider"]


def _render_findings(findings):
    if not findings:
        return "なし（0件）"
    lines = []
    for finding in findings:
        lines.append(
            "- %s（severity: %s／blocking: %s）：%s（根拠：`%s` %s）"
            % (
                finding["identifier"],
                finding["severity"],
                "true" if finding["blocking"] else "false",
                finding["claim"],
                finding["evidence_path"],
                finding["evidence_location"],
            )
        )
    return "\n".join(lines)


def _render_record(
    *,
    request_relative_path,
    request_sha256,
    verdict,
    tier,
    backend_name,
    provider,
    model,
    raw_digest,
    raw_store_kind,
    run_id,
):
    freshness = verdict["freshness"]
    freshness_line = "%s（expected `%s`／observed `%s`）" % (
        freshness["result"],
        freshness["expected"],
        freshness["observed"],
    )
    if freshness["result"] == "not_computable":
        freshness_line += "。理由：%s" % freshness.get("reason", "")
    unexamined = verdict["unexamined"]
    unexamined_line = (
        "、".join(unexamined) if unexamined else "（申告なし＝空配列）"
    )
    return (
        "# Reviewer起動アダプタ 判定record（機械転記） %s\n"
        "\n"
        "- Reviewer：provider `%s`／model `%s`（アダプタ照合済み）\n"
        "- 独立性：Tier %d（アダプタ判定。契約010 §5.1-4）\n"
        "- 起動方式：headless機械起動（backend `%s`）\n"
        "- 依頼record：`%s`（SHA-256 `%s`）\n"
        "- 未加工出力：保存先種別 `%s`、SHA-256 `%s`、参照権限：repo外私有領域（利用者とClaude）\n"
        "- 実行識別子：`%s`\n"
        "- 判定：**%s**\n"
        "- 判定要旨：%s\n"
        "- 鮮度（Reviewer申告）：%s\n"
        "- 未検査：%s\n"
        "\n"
        "## findings\n"
        "\n"
        "%s\n"
        "\n"
        "## 判定JSON（verbatim）\n"
        "\n"
        "```json\n"
        "%s\n"
        "```\n"
        % (
            run_id,
            provider,
            model,
            tier,
            backend_name,
            request_relative_path,
            request_sha256,
            raw_store_kind,
            raw_digest,
            run_id,
            verdict["verdict"],
            verdict["summary"],
            freshness_line,
            unexamined_line,
            _render_findings(verdict["findings"]),
            json.dumps(verdict, ensure_ascii=False, indent=2, sort_keys=True),
        )
    )


def transcribe_verdict_record(
    *,
    repository,
    request_relative_path,
    request_sha256,
    verdict,
    tier,
    backend_name,
    model,
    raw_digest,
    raw_store_kind,
    run_id,
):
    """schema適合の判定JSONを判定recordへ転記し、単独commitする。"""

    validate_verdict(verdict)
    if _SHA256_PATTERN.fullmatch(raw_digest or "") is None:
        raise TranscriptionStop("raw_digest_invalid")
    status = _run_git(repository, "status", "--porcelain")
    if status.strip():
        raise TranscriptionStop("worktree_not_clean")
    request_path = Path(repository) / request_relative_path
    try:
        data = request_path.read_bytes()
    except OSError as error:
        raise TranscriptionStop("request_record_unreadable") from error
    if hashlib.sha256(data).hexdigest() != request_sha256:
        raise TranscriptionStop("request_record_stale")
    provider = _backend_provider(backend_name)
    record_relative = verdict_record_relative_path(request_relative_path)
    record_path = Path(repository) / record_relative
    if record_path.exists():
        raise TranscriptionStop("verdict_record_exists")
    body = _render_record(
        request_relative_path=request_relative_path,
        request_sha256=request_sha256,
        verdict=verdict,
        tier=tier,
        backend_name=backend_name,
        provider=provider,
        model=model,
        raw_digest=raw_digest,
        raw_store_kind=raw_store_kind,
        run_id=run_id,
    )
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(body, encoding="utf-8")
    _run_git(repository, "add", "--", record_relative)
    _run_git(
        repository,
        "commit",
        "-q",
        "-m",
        "Add reviewer launch verdict record %s" % run_id,
    )
    shown = _run_git(
        repository, "show", "--name-only", "--format=%H", "HEAD"
    ).splitlines()
    commit = shown[0].strip() if shown else ""
    changed = [line for line in shown[1:] if line.strip()]
    if changed != [record_relative]:
        raise TranscriptionStop("verdict_commit_not_single")
    return {"record_relative_path": record_relative, "commit": commit}


def _extract_embedded_verdict(body):
    matches = _JSON_BLOCK_PATTERN.findall(body)
    if not matches:
        raise TranscriptionStop("verdict_json_unparseable")
    try:
        return json.loads(matches[-1])
    except (json.JSONDecodeError, ValueError) as error:
        raise TranscriptionStop("verdict_json_unparseable") from error


def post_verify(
    *,
    repository,
    request_relative_path,
    request_sha256,
    record_relative_path,
    target_commit,
    raw_digest,
):
    """契約§7.3の事後照合4点を機械実行する。不備は停止。"""

    checks = []

    request_path = Path(repository) / request_relative_path
    try:
        data = request_path.read_bytes()
    except OSError as error:
        raise TranscriptionStop("request_record_unreadable") from error
    if hashlib.sha256(data).hexdigest() != request_sha256:
        raise TranscriptionStop("request_record_stale")
    checks.append("freshness")

    commit = _run_git(
        repository,
        "log",
        "-n",
        "1",
        "--format=%H",
        "--",
        record_relative_path,
    ).strip()
    if not commit:
        raise TranscriptionStop("verdict_commit_missing")
    shown = _run_git(
        repository, "show", "--name-only", "--format=%H", commit
    ).splitlines()
    changed = [line for line in shown[1:] if line.strip()]
    if changed != [record_relative_path]:
        raise TranscriptionStop("verdict_commit_not_single")
    if commit == target_commit or not _git_succeeds(
        repository,
        "merge-base",
        "--is-ancestor",
        target_commit,
        commit,
    ):
        raise TranscriptionStop("verdict_commit_not_after_target")
    checks.append("single_record_commit")

    record_path = Path(repository) / record_relative_path
    try:
        body = record_path.read_text(encoding="utf-8")
    except OSError as error:
        raise TranscriptionStop("verdict_record_unreadable") from error
    if raw_digest not in body:
        raise TranscriptionStop("raw_digest_mismatch")
    parsed = _extract_embedded_verdict(body)
    for finding in parsed.get("findings", ()):
        evidence = finding.get("evidence_path")
        if not isinstance(evidence, str) or not (
            Path(repository) / evidence
        ).exists():
            raise TranscriptionStop("evidence_path_missing")
    checks.append("evidence")

    try:
        validate_verdict(parsed)
    except VerdictInvalid as error:
        raise TranscriptionStop("verdict_schema_nonconforming") from error
    checks.append("schema_form")

    return {"status": "passed", "checks": checks}
