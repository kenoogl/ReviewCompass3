"""V4 Issue state遷移の正規永続化tool（deferred #1・案B）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

正本authority：IC-V4-ISSUE-RESOLUTION-PERSISTENCE-GAP-001のscope／non_scopeと、
Human裁定（2026-08-10）：risk high・案B・遷移元は`registered`のみ。

案Bの永続化：既存Issue record fileの`state`と`content_digest`だけをin-placeで
更新し（file名・issue_version不変）、解決の根拠（Human裁定・Evidence参照）は
`records/development/`の解決record（new-only）として残す。V4 Issue schema・
config・既存toolは変更しない。

fail-closed：全検証に合格するまで書かず、事後の正規検証（record＋repository）に
失敗した場合は元bytesへ完全復元し、解決recordも残さない。
"""

import argparse
import hashlib
import json
import re
from pathlib import Path

from tools.development import issue_intake_v4 as intake


_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_RECORDS_PREFIX = "records/development/"


class ResolutionError(Exception):
    """resolve遷移を安全に実行できない。文言は安定stop codeのみ。"""

    def __init__(self, stop_code):
        self.stop_code = stop_code
        super().__init__(stop_code)


def _safe_relative(value, stop_code):
    if not isinstance(value, str) or not value:
        raise ResolutionError(stop_code)
    pure = Path(value)
    if pure.is_absolute() or ".." in pure.parts or "\\" in value:
        raise ResolutionError(stop_code)
    return value


def _resolve_inside(project_root, relative, stop_code):
    resolved = (project_root / relative).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError:
        raise ResolutionError(stop_code) from None
    return resolved


def _parse_evidence(items, project_root):
    if not items:
        raise ResolutionError("evidence_invalid")
    references = []
    for item in items:
        relative, separator, digest = item.partition("=")
        if separator != "=" or _HEX64.fullmatch(digest) is None:
            raise ResolutionError("evidence_invalid")
        _safe_relative(relative, "evidence_invalid")
        file = _resolve_inside(project_root, relative, "evidence_invalid")
        if not file.is_file():
            raise ResolutionError("evidence_invalid")
        if hashlib.sha256(file.read_bytes()).hexdigest() != digest:
            raise ResolutionError("evidence_invalid")
        references.append({"path": relative, "sha256": digest})
    return references


def _verify_ruling(project_root, relative, sha256_value, human_id, decided_at):
    if (
        not isinstance(human_id, str)
        or not human_id.strip()
        or not isinstance(decided_at, str)
        or not decided_at.strip()
    ):
        raise ResolutionError("human_ruling_invalid")
    _safe_relative(relative, "human_ruling_invalid")
    if _HEX64.fullmatch(sha256_value or "") is None:
        raise ResolutionError("human_ruling_invalid")
    file = _resolve_inside(project_root, relative, "human_ruling_invalid")
    if not file.is_file():
        raise ResolutionError("human_ruling_invalid")
    if hashlib.sha256(file.read_bytes()).hexdigest() != sha256_value:
        raise ResolutionError("human_ruling_invalid")
    return {"path": relative, "sha256": sha256_value}


def _load_issue(project_root, issue_path, config):
    _safe_relative(issue_path, "issue_record_invalid")
    file = _resolve_inside(project_root, issue_path, "issue_record_invalid")
    try:
        original_bytes = file.read_bytes()
        record = json.loads(original_bytes.decode("utf-8"))
    except (OSError, ValueError):
        raise ResolutionError("issue_record_invalid") from None
    try:
        intake.validate_v4_issue_record(
            record, path=issue_path, project_root=project_root, config=config
        )
    except intake.IntakeError:
        raise ResolutionError("issue_record_invalid") from None
    return file, original_bytes, record


def _transition(record, target_state, config):
    if record["state"] != "registered":
        raise ResolutionError("issue_state_not_registered")
    if (
        target_state not in config["issue_states"]
        or target_state not in config["terminal_issue_states"]
    ):
        raise ResolutionError("target_state_invalid")
    updated = dict(record)
    updated["state"] = target_state
    updated.pop("content_digest")
    updated["content_digest"] = intake.canonical_digest(updated)
    return updated


def _resolution_record_target(project_root, relative):
    _safe_relative(relative, "resolution_record_path_invalid")
    if not relative.startswith(_RECORDS_PREFIX):
        raise ResolutionError("resolution_record_path_invalid")
    file = _resolve_inside(project_root, relative, "resolution_record_path_invalid")
    if file.exists():
        raise ResolutionError("resolution_record_conflict")
    return file


def _write_json_bytes(document):
    return (
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def resolve_issue(
    *,
    config_path,
    project_root,
    issue_path,
    target_state,
    human_id,
    decided_at,
    ruling_path,
    ruling_sha256,
    evidence_items,
    resolution_record_path,
):
    """検証→in-place遷移→事後正規検証→解決record作成を行う。"""

    root = Path(project_root)
    if not root.is_dir():
        raise ResolutionError("project_root_invalid")
    try:
        config = intake.load_config(config_path)
    except intake.IntakeError:
        raise ResolutionError("config_invalid") from None
    issue_file, original_bytes, record = _load_issue(root, issue_path, config)
    updated = _transition(record, target_state, config)
    ruling = _verify_ruling(root, ruling_path, ruling_sha256, human_id, decided_at)
    evidence = _parse_evidence(evidence_items, root)
    record_file = _resolution_record_target(root, resolution_record_path)

    resolution_document = {
        "kind": "v4_issue_resolution",
        "issue": {
            "issue_id": record["issue_id"],
            "path": issue_path,
            "content_digest_before": record["content_digest"],
            "content_digest_after": updated["content_digest"],
        },
        "transition": {"from": "registered", "to": target_state},
        "human": {
            "human_id": human_id,
            "decided_at": decided_at,
            "ruling": ruling,
        },
        "evidence": evidence,
    }

    issue_file.write_bytes(_write_json_bytes(updated))
    try:
        intake.validate_v4_issue_record(
            updated, path=issue_path, project_root=root, config=config
        )
        intake.validate_v4_issue_repository(project_root=root, config=config)
    except intake.IntakeError:
        issue_file.write_bytes(original_bytes)
        raise ResolutionError("post_validation_failed") from None
    except Exception:
        issue_file.write_bytes(original_bytes)
        raise ResolutionError("post_validation_failed") from None

    try:
        record_file.parent.mkdir(parents=True, exist_ok=True)
        record_file.write_bytes(_write_json_bytes(resolution_document))
    except OSError:
        issue_file.write_bytes(original_bytes)
        raise ResolutionError("resolution_record_write_failed") from None

    return {
        "status": "ok",
        "issue_id": record["issue_id"],
        "issue_path": issue_path,
        "state": target_state,
        "content_digest_before": record["content_digest"],
        "content_digest_after": updated["content_digest"],
        "resolution_record": resolution_record_path,
    }


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--issue", required=True)
    parser.add_argument("--to", required=True)
    parser.add_argument("--human-id", required=True)
    parser.add_argument("--decided-at", required=True)
    parser.add_argument("--ruling", required=True)
    parser.add_argument("--ruling-sha256", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--resolution-record", required=True)
    args = parser.parse_args(argv)
    try:
        report = resolve_issue(
            config_path=args.config,
            project_root=args.project_root,
            issue_path=args.issue,
            target_state=args.to,
            human_id=args.human_id,
            decided_at=args.decided_at,
            ruling_path=args.ruling,
            ruling_sha256=args.ruling_sha256,
            evidence_items=tuple(args.evidence),
            resolution_record_path=args.resolution_record,
        )
    except ResolutionError as error:
        print(json.dumps(
            {"status": "error", "reason": error.stop_code},
            ensure_ascii=False,
            sort_keys=True,
        ))
        return 5
    print(json.dumps(report, ensure_ascii=False, sort_keys=True))
    return 0


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
