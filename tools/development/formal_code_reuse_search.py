"""確定commitから既存コード再利用検索を一回で実行する開発支援入口。"""

import argparse
import json
from datetime import datetime
from pathlib import Path

from tools.development import reuse_search_record as reuse
from tools.development import work4a_rebuild_v3 as work4a


_PLAN_FIELDS = {
    "record_kind",
    "schema_version",
    "plan_id",
    "searches",
    "content_digest",
}
_SEARCH_FIELDS = {
    "subject",
    "target_paths",
    "target_symbols",
    "attestation_path",
}


class FormalCodeReuseSearchError(Exception):
    """正式検索を一つの確定状態から安全に完了できない。"""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _read_json(path, failure):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise FormalCodeReuseSearchError(failure) from error


def _project_path(project_root, relative_path):
    if not isinstance(relative_path, str):
        raise FormalCodeReuseSearchError("invalid_search_plan")
    relative = Path(relative_path)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise FormalCodeReuseSearchError("invalid_search_plan")
    root = Path(project_root).resolve()
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise FormalCodeReuseSearchError("invalid_search_plan") from error
    return resolved


def _validate_plan(document, project_root):
    if not isinstance(document, dict) or set(document) != _PLAN_FIELDS:
        raise FormalCodeReuseSearchError("invalid_search_plan")
    if (
        document.get("record_kind") != "formal_code_reuse_search_plan"
        or document.get("schema_version") != 1
        or not isinstance(document.get("plan_id"), str)
        or not document["plan_id"]
        or document.get("content_digest") != work4a._content_digest(document)
    ):
        raise FormalCodeReuseSearchError("invalid_search_plan")
    searches = document.get("searches")
    if not isinstance(searches, list) or not searches:
        raise FormalCodeReuseSearchError("invalid_search_plan")

    subjects = set()
    outputs = set()
    validated = []
    for search in searches:
        if not isinstance(search, dict) or set(search) != _SEARCH_FIELDS:
            raise FormalCodeReuseSearchError("invalid_search_plan")
        subject = search.get("subject")
        target_paths = search.get("target_paths")
        target_symbols = search.get("target_symbols")
        if (
            not isinstance(subject, str)
            or not subject
            or subject in subjects
            or not isinstance(target_paths, list)
            or not target_paths
            or any(not isinstance(item, str) or not item for item in target_paths)
            or not isinstance(target_symbols, list)
            or any(not isinstance(item, str) or not item for item in target_symbols)
        ):
            raise FormalCodeReuseSearchError("invalid_search_plan")
        if any(Path(item).is_absolute() or ".." in Path(item).parts for item in target_paths):
            raise FormalCodeReuseSearchError("invalid_search_plan")
        output = _project_path(project_root, search.get("attestation_path"))
        if output in outputs:
            raise FormalCodeReuseSearchError("invalid_search_plan")
        if output.exists():
            raise FormalCodeReuseSearchError("output_already_exists")
        subjects.add(subject)
        outputs.add(output)
        validated.append((search, output))
    return tuple(validated)


def _load_universe(project_root, path):
    target = _project_path(project_root, Path(path).resolve().relative_to(Path(project_root).resolve()).as_posix())
    document = _read_json(target, "source_universe_unavailable")
    try:
        work4a.validate_record_schema(document, record_kind="work4a_source_universe")
        work4a.verify_project_ref(
            project_root=project_root,
            reference=document["development_policy_ref"],
        )
    except work4a.V3ValidationError as error:
        raise FormalCodeReuseSearchError(error.code) from error
    return work4a.Universe(
        document["source_universe_id"],
        document["source_universe_version"],
        target,
        document["content_digest"],
    )


def _load_policy(project_root, path):
    target = _project_path(project_root, Path(path).resolve().relative_to(Path(project_root).resolve()).as_posix())
    document = _read_json(target, "freshness_policy_unavailable")
    try:
        work4a.validate_record_schema(document, record_kind="work4a_freshness_policy")
        work4a.verify_project_ref(
            project_root=project_root,
            reference=document["development_policy_ref"],
        )
    except work4a.V3ValidationError as error:
        raise FormalCodeReuseSearchError(error.code) from error
    return work4a.Policy(
        document["policy_id"],
        document["policy_version"],
        target,
        document["content_digest"],
    )


def _target_paths_exist(search, observed_paths):
    for prefix in search["target_paths"]:
        if not any(path == prefix or path.startswith(f"{prefix}/") for path in observed_paths):
            return False
    return True


def execute_formal_search(
    *,
    project_root,
    runtime_root,
    profile,
    universe_path,
    policy_path,
    plan_path,
    captured_at,
):
    """一つの確定commitから計画内の全検索と証明書を生成する。"""

    root = Path(project_root).resolve()
    try:
        plan_relative = Path(plan_path).resolve().relative_to(root).as_posix()
    except ValueError as error:
        raise FormalCodeReuseSearchError("invalid_search_plan") from error
    plan_target = _project_path(root, plan_relative)
    plan_document = _read_json(plan_target, "invalid_search_plan")
    searches = _validate_plan(plan_document, root)
    universe = _load_universe(root, universe_path)
    policy = _load_policy(root, policy_path)

    try:
        observation = work4a.capture_committed_observation(
            project_root=root,
            runtime_root=runtime_root,
            profile=profile,
            universe=universe,
            policy=policy,
            tool_version="formal-code-reuse-search-v1",
            captured_at=captured_at,
        )
        routine_profile = work4a.build_routine_profile_v3(
            observation=observation,
            policy=policy,
        )
        discovery = work4a.build_comparison_discovery(
            observation=observation,
            routine_profile=routine_profile,
            policy=policy,
        )
    except work4a.V3ValidationError as error:
        raise FormalCodeReuseSearchError(error.code) from error

    observation_document = _read_json(
        observation.path,
        "observation_unavailable",
    )
    profile_document = _read_json(
        routine_profile.path,
        "routine_profile_unavailable",
    )
    discovery_document = _read_json(
        discovery.path,
        "comparison_discovery_unavailable",
    )
    observed_paths = {item["path"] for item in observation_document["files"]}
    results = []
    for search, attestation_path in searches:
        if not _target_paths_exist(search, observed_paths):
            raise FormalCodeReuseSearchError("invalid_search_plan")
        declaration = {
            "subject": search["subject"],
            "target_paths": list(search["target_paths"]),
            "target_symbols": list(search["target_symbols"]),
        }
        try:
            record = reuse.search_existing_routines(
                profile_document=profile_document,
                discovery_document=discovery_document,
                declaration=declaration,
                observation_document=observation_document,
                project_root=root,
            )
            reuse.externalize_reuse_search_record(
                record=record,
                data_root=observation.data_root,
                attestation_path=attestation_path,
            )
            verdict = reuse.gate_check_attested(
                attestation_path=attestation_path,
                data_root=observation.data_root,
                expected_identity={
                    field: record["source_identity"][field]
                    for field in (
                        "profile_run_id",
                        "discovery_run_id",
                        "source_content_id",
                    )
                },
                project_root=root,
            )
        except reuse.ReuseSearchError as error:
            raise FormalCodeReuseSearchError("reuse_search_failed") from error
        results.append(
            {
                "subject": search["subject"],
                "search_content_digest": record["content_digest"],
                "hit_count": len(record["hits"]),
                "group_count": len(record["groups"]),
                "attestation_path": str(attestation_path),
                "attestation_sha256": reuse.file_sha256(attestation_path),
                "start_allowed": verdict["start_allowed"],
                "reason": verdict["reason"],
            }
        )

    return {
        "status": "completed" if all(item["start_allowed"] for item in results) else "stopped",
        "plan_id": plan_document["plan_id"],
        "plan_sha256": work4a._file_sha256(plan_target),
        "head": observation_document["head"],
        "source_content_id": observation.source_content_id,
        "source_file_count": len(observation.files),
        "observation_snapshot_id": observation.snapshot_id,
        "routine_profile_run_id": routine_profile.profile_run_id,
        "routine_count": routine_profile.routine_count,
        "comparison_discovery_run_id": discovery.discovery_run_id,
        "comparison_group_count": discovery.group_count,
        "searches": results,
        "lifecycle_adjudication_required": True,
        "reuse_disposition_adjudication_required": True,
    }


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--profile", default="development")
    parser.add_argument("--universe", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--captured-at")
    args = parser.parse_args(argv)
    captured_at = args.captured_at or datetime.now().astimezone().isoformat(timespec="seconds")
    try:
        result = execute_formal_search(
            project_root=args.project_root,
            runtime_root=args.runtime_root,
            profile=args.profile,
            universe_path=args.universe,
            policy_path=args.policy,
            plan_path=args.plan,
            captured_at=captured_at,
        )
    except FormalCodeReuseSearchError as error:
        result = {"status": "stopped", "reason": error.code}
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
