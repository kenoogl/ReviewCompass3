"""Work 1B用Session Log Bootstrapと現在位置text projection。"""

import dataclasses
import hashlib
import json
from pathlib import Path


class SessionLogBootstrapError(Exception):
    """bootstrap入力を安全かつ決定的に処理できない。"""


@dataclasses.dataclass(frozen=True)
class CapturePlan:
    session_id: str
    source_identity: str
    event_range: tuple
    raw_path: Path
    derived_paths: dict
    confidentiality: str
    access: tuple
    retention: dict
    capture_deadline: str
    completeness: str
    mutation: str
    source_availability: str


@dataclasses.dataclass(frozen=True)
class RestoreResult:
    artifacts: dict
    digests: dict
    source_digest: str
    matches_profile: bool


@dataclasses.dataclass(frozen=True)
class DurableCaptureResult:
    raw_path: Path
    derived_paths: dict
    evidence_path: Path
    evidence: dict


@dataclasses.dataclass(frozen=True)
class SessionBootstrapResult:
    capture: DurableCaptureResult
    session_lifecycle: dict
    projection: dict
    short_text: str
    detailed_text: str
    authority_status: str
    display_status: str
    display_error: str


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _mapping(value, *, field):
    if not isinstance(value, dict):
        raise SessionLogBootstrapError(f"{field} must be an object")
    return value


def _string(value, *, field):
    if not isinstance(value, str) or not value:
        raise SessionLogBootstrapError(f"{field} must be a non-empty string")
    return value


def _profile_parts(profile):
    record = _mapping(profile, field="capture profile")
    if record.get("schema_version") != 1:
        raise SessionLogBootstrapError("Unsupported capture profile version")
    session_id = _string(record.get("session_id"), field="session_id")
    if session_id in {".", ".."} or "/" in session_id or "\\" in session_id:
        raise SessionLogBootstrapError("session_id must be a safe identifier")
    source = _mapping(record.get("source"), field="source")
    source_identity = _string(
        source.get("identity"),
        field="source.identity",
    )
    _string(source.get("kind"), field="source.kind")
    _string(source.get("revision"), field="source.revision")
    capture = _mapping(record.get("capture"), field="capture")
    event_range = _mapping(capture.get("range"), field="capture.range")
    count = event_range.get("event_count")
    if not isinstance(count, int) or count < 0:
        raise SessionLogBootstrapError(
            "capture.range.event_count must be a non-negative integer"
        )
    range_tuple = (
        _string(
            event_range.get("start_event_id"),
            field="capture.range.start_event_id",
        ),
        _string(
            event_range.get("end_event_id"),
            field="capture.range.end_event_id",
        ),
        count,
    )
    for field in ("started_at", "captured_at", "capture_deadline"):
        _string(capture.get(field), field=f"capture.{field}")
    digests = _mapping(record.get("digests"), field="digests")
    for name in ("raw", "transcript", "summary", "index"):
        digest = _string(
            digests.get(f"{name}_sha256"),
            field=f"digests.{name}_sha256",
        )
        if len(digest) != 64:
            raise SessionLogBootstrapError(
                f"digests.{name}_sha256 must be SHA-256"
            )
    access = record.get("access")
    if not isinstance(access, list) or not access:
        raise SessionLogBootstrapError("access must be a non-empty list")
    access_tuple = tuple(
        _string(item, field="access item")
        for item in access
    )
    retention = _mapping(record.get("retention"), field="retention")
    if set(retention) != {"raw", "derived"}:
        raise SessionLogBootstrapError("retention boundary is incomplete")
    return (
        record,
        session_id,
        source_identity,
        capture,
        range_tuple,
        access_tuple,
    )


def plan_session_capture(profile, *, raw_bytes, layout):
    """Layout Baselineに従うraw／派生物の保存先を決定する。"""

    (
        record,
        session_id,
        source_identity,
        capture,
        event_range,
        access,
    ) = _profile_parts(profile)
    if not isinstance(raw_bytes, bytes):
        raise SessionLogBootstrapError("raw_bytes must be bytes")
    if _sha256(raw_bytes) != record["digests"]["raw_sha256"]:
        raise SessionLogBootstrapError("raw source Digest does not match")
    roots = getattr(layout, "roots", None)
    if not isinstance(roots, dict):
        raise SessionLogBootstrapError("Layout resolution is required")
    try:
        sensitive_root = Path(roots["sensitive_root"])
        data_root = Path(roots["data_root"])
    except KeyError as error:
        raise SessionLogBootstrapError(
            "Layout resolution lacks Session Evidence roots"
        ) from error
    if (
        not sensitive_root.is_absolute()
        or not data_root.is_absolute()
        or sensitive_root == data_root
    ):
        raise SessionLogBootstrapError(
            "Session Evidence roots must be distinct absolute paths"
        )
    raw_path = (
        sensitive_root
        / "sessions"
        / session_id
        / "raw"
        / "session.jsonl"
    )
    derived_root = data_root / "sessions" / session_id
    return CapturePlan(
        session_id=session_id,
        source_identity=source_identity,
        event_range=event_range,
        raw_path=raw_path,
        derived_paths={
            "index": derived_root / "index.json",
            "summary": derived_root / "summary.json",
            "transcript": derived_root / "transcript.md",
        },
        confidentiality=_string(
            record.get("confidentiality"),
            field="confidentiality",
        ),
        access=access,
        retention=dict(record["retention"]),
        capture_deadline=capture["capture_deadline"],
        completeness=_string(
            record.get("completeness"),
            field="completeness",
        ),
        mutation=_string(record.get("mutation"), field="mutation"),
        source_availability=_string(
            record.get("source_availability"),
            field="source_availability",
        ),
    )


def assess_source_availability(observation):
    """正常な空sourceと取得・復元不能を区別する。"""

    record = _mapping(observation, field="source observation")
    required = {
        "accessible",
        "complete",
        "event_count",
        "expired",
        "reconstructable",
    }
    if set(record) != required:
        raise SessionLogBootstrapError(
            "source observation has unknown or missing fields"
        )
    if record["expired"]:
        status = "source_expired"
    elif not record["accessible"]:
        status = "source_missing"
    elif not record["complete"] or not record["reconstructable"]:
        status = "non_reconstructable"
    else:
        status = "available"
    return {
        "normal_empty": status == "available" and record["event_count"] == 0,
        "status": status,
    }


def _parse_raw_events(raw_bytes):
    if not isinstance(raw_bytes, bytes):
        raise SessionLogBootstrapError("raw session must be bytes")
    try:
        text = raw_bytes.decode("utf-8")
        return tuple(
            _mapping(json.loads(line), field="raw event")
            for line in text.splitlines()
            if line
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SessionLogBootstrapError("raw session is not valid JSONL") from error


def _render_json_bytes(value):
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")


def restore_derived_artifacts(raw_bytes, *, profile):
    """合成bootstrap rawからtranscript、summary、indexを再生成する。"""

    (
        record,
        session_id,
        source_identity,
        _capture,
        event_range,
        _access,
    ) = _profile_parts(profile)
    events = _parse_raw_events(raw_bytes)
    if len(events) != event_range[2]:
        raise SessionLogBootstrapError("raw event count does not match profile")
    if not events:
        raise SessionLogBootstrapError("fixed restore range must not be empty")
    event_ids = [
        _string(event.get("event_id"), field="raw event_id")
        for event in events
    ]
    if (event_ids[0], event_ids[-1]) != event_range[:2]:
        raise SessionLogBootstrapError("raw event range does not match profile")
    if any(event.get("session_id") != session_id for event in events):
        raise SessionLogBootstrapError("raw session identity does not match")

    messages = [event for event in events if event.get("type") == "message"]
    transcript_lines = [f"# Session {session_id}", ""]
    roles = []
    for event in messages:
        role = _string(event.get("role"), field="message role")
        content = _string(event.get("content"), field="message content")
        roles.append(role)
        transcript_lines.extend((f"## {role}", "", content, ""))
    transcript = "\n".join(transcript_lines).encode("utf-8")
    summary = _render_json_bytes({
        "message_count": len(messages),
        "roles": roles,
        "session_id": session_id,
        "source_identity": source_identity,
    })
    index = _render_json_bytes({
        "events": [
            {
                "event_id": event_id,
                "line": line,
                "type": _string(event.get("type"), field="event type"),
            }
            for line, (event_id, event) in enumerate(
                zip(event_ids, events),
                start=1,
            )
        ],
        "session_id": session_id,
    })
    artifacts = {
        "index": index,
        "summary": summary,
        "transcript": transcript,
    }
    digests = {
        name: _sha256(content)
        for name, content in artifacts.items()
    }
    source_digest = _sha256(raw_bytes)
    expected_digests = record["digests"]
    matches_profile = (
        source_digest == expected_digests["raw_sha256"]
        and all(
            digest == expected_digests[f"{name}_sha256"]
            for name, digest in digests.items()
        )
    )
    return RestoreResult(
        artifacts=artifacts,
        digests=digests,
        source_digest=source_digest,
        matches_profile=matches_profile,
    )


def _session_evidence(profile, *, session_id):
    relative_root = f"sessions/{session_id}"
    return {
        "access": list(profile["access"]),
        "capture": dict(profile["capture"]),
        "completeness": profile["completeness"],
        "confidentiality": profile["confidentiality"],
        "digests": dict(profile["digests"]),
        "mutation": profile["mutation"],
        "retention": dict(profile["retention"]),
        "schema_version": 1,
        "session_id": session_id,
        "source": dict(profile["source"]),
        "source_availability": profile["source_availability"],
        "status": "captured",
        "storage": {
            "derived": {
                "index": {
                    "path": f"{relative_root}/index.json",
                    "root": "data_root",
                },
                "summary": {
                    "path": f"{relative_root}/summary.json",
                    "root": "data_root",
                },
                "transcript": {
                    "path": f"{relative_root}/transcript.md",
                    "root": "data_root",
                },
            },
            "evidence": {
                "path": f"{relative_root}/session-evidence.json",
                "root": "data_root",
            },
            "raw": {
                "path": f"{relative_root}/raw/session.jsonl",
                "root": "sensitive_root",
            },
        },
    }


def _write_new_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(content)


def _capture_directories(paths, *, stop_roots):
    stop = {Path(root) for root in stop_roots}
    directories = set()
    for path in paths:
        parent = Path(path).parent
        while parent not in stop:
            if parent == parent.parent:
                raise SessionLogBootstrapError(
                    "Capture destination escapes logical roots"
                )
            directories.add(parent)
            parent = parent.parent
    return directories


def _remove_empty_capture_directories(
    directories,
    *,
    preserve_directories,
):
    for directory in sorted(
        set(directories) - set(preserve_directories),
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        try:
            directory.rmdir()
        except FileNotFoundError:
            continue
        except OSError:
            continue


def persist_session_capture(
    profile,
    *,
    raw_bytes,
    layout,
    write_bytes=None,
):
    """検証済みSession Evidence一式をproject外rootへ保存する。"""

    plan = plan_session_capture(
        profile,
        raw_bytes=raw_bytes,
        layout=layout,
    )
    restored = restore_derived_artifacts(raw_bytes, profile=profile)
    if not restored.matches_profile:
        raise SessionLogBootstrapError(
            "Derived artifact Digest does not match capture profile"
        )
    evidence = _session_evidence(profile, session_id=plan.session_id)
    data_root = Path(layout.roots["data_root"])
    sensitive_root = Path(layout.roots["sensitive_root"])
    evidence_path = (
        data_root
        / "sessions"
        / plan.session_id
        / "session-evidence.json"
    )
    payloads = [
        (plan.raw_path, raw_bytes),
        (plan.derived_paths["index"], restored.artifacts["index"]),
        (plan.derived_paths["summary"], restored.artifacts["summary"]),
        (
            plan.derived_paths["transcript"],
            restored.artifacts["transcript"],
        ),
        (evidence_path, _render_json_bytes(evidence)),
    ]
    conflicts = [path for path, _content in payloads if path.exists()]
    if conflicts:
        raise SessionLogBootstrapError(
            "Session capture destination already exists"
        )
    writer = _write_new_file if write_bytes is None else write_bytes
    if not callable(writer):
        raise SessionLogBootstrapError("write_bytes must be callable")

    destination_paths = [path for path, _content in payloads]
    capture_directories = _capture_directories(
        destination_paths,
        stop_roots=(data_root, sensitive_root),
    )
    preexisting_directories = {
        directory
        for directory in capture_directories
        if directory.exists()
    }
    created_files = []
    try:
        for path, content in payloads:
            existed_before = path.exists()
            try:
                writer(path, content)
            except Exception:
                if not existed_before and path.is_file():
                    created_files.append(path)
                raise
            if not existed_before and path.is_file():
                created_files.append(path)
        for path, content in payloads:
            if path.read_bytes() != content:
                raise OSError("capture post-write verification failed")
    except Exception as error:
        rollback_failed = False
        for path in reversed(created_files):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                rollback_failed = True
        _remove_empty_capture_directories(
            capture_directories,
            preserve_directories=preexisting_directories,
        )
        message = (
            "partial capture rollback incomplete"
            if rollback_failed
            else "partial capture write failed and was rolled back"
        )
        raise SessionLogBootstrapError(message) from error

    return DurableCaptureResult(
        raw_path=plan.raw_path,
        derived_paths=dict(plan.derived_paths),
        evidence_path=evidence_path,
        evidence=evidence,
    )


def _projection_missing_inputs(fixed_inputs):
    plan_present = any(
        isinstance(item, dict)
        and "plan" in str(item.get("identity", "")).lower()
        and isinstance(item.get("digest"), str)
        and len(item["digest"]) == 64
        for item in fixed_inputs
    )
    event_stream_present = any(
        isinstance(item, dict)
        and (
            str(item.get("identity", "")).endswith(".jsonl")
            or "event" in str(item.get("identity", "")).lower()
        )
        and isinstance(item.get("digest"), str)
        and len(item["digest"]) == 64
        for item in fixed_inputs
    )
    missing = []
    if not plan_present:
        missing.append("fixed Plan identity and Digest")
    if not event_stream_present:
        missing.append("workflow event stream identity and Digest")
    return missing


def _work_start_conflict(events):
    starts = {}
    for event in events:
        if event.get("event_type") != "work_started":
            continue
        key = event.get("occurred_at")
        work_item_id = _mapping(
            event.get("payload"),
            field="event payload",
        ).get("work_item_id")
        starts.setdefault(key, set()).add(work_item_id)
    return any(len(work_items) > 1 for work_items in starts.values())


def project_current_work(events, *, inputs):
    """固定eventを一つのbootstrap current workへ畳み込む。"""

    input_record = _mapping(inputs, field="projection inputs")
    fixed_inputs = input_record.get("fixed_inputs")
    if not isinstance(fixed_inputs, list):
        raise SessionLogBootstrapError("fixed_inputs must be a list")
    event_records = tuple(
        _mapping(event, field="workflow event")
        for event in events
    )
    plan = {
        "stage": None,
        "state": None,
        "work_id": None,
        "work_name": None,
    }
    current_activity = {
        "contract_id": None,
        "tdd_state": None,
        "work_item_id": None,
    }
    next_action = None
    blockers = {}
    decisions = {}
    stale = {}
    deferred = []
    canceled = []
    completion_next_missing = False

    for event in event_records:
        event_type = _string(
            event.get("event_type"),
            field="event_type",
        )
        _string(event.get("event_id"), field="event_id")
        _string(event.get("occurred_at"), field="occurred_at")
        payload = _mapping(event.get("payload"), field="event payload")
        if event_type == "work_started":
            plan = {
                "stage": payload.get("stage"),
                "state": payload.get("state"),
                "work_id": payload.get("work_id"),
                "work_name": payload.get("work_name"),
            }
            current_activity = {
                "contract_id": payload.get("contract_id"),
                "tdd_state": payload.get("tdd_state"),
                "work_item_id": payload.get("work_item_id"),
            }
            next_action = payload.get("next")
        elif event_type == "work_paused":
            plan["state"] = "paused"
        elif event_type == "work_resumed":
            plan["state"] = "active"
        elif event_type == "work_completed":
            plan["state"] = "completed"
            current_activity["work_item_id"] = None
            completion_next = payload.get("next")
            if isinstance(completion_next, str) and completion_next:
                next_action = completion_next
            else:
                completion_next_missing = True
        elif event_type == "blocker_raised":
            blockers[payload.get("blocker_id")] = {
                "blocker_id": payload.get("blocker_id"),
                "summary": payload.get("summary"),
            }
        elif event_type == "blocker_cleared":
            blockers.pop(payload.get("blocker_id"), None)
        elif event_type == "human_decision_requested":
            decisions[payload.get("decision_id")] = {
                "decision_id": payload.get("decision_id"),
                "summary": payload.get("summary"),
            }
        elif event_type == "human_decision_recorded":
            decisions.pop(payload.get("decision_id"), None)
        elif event_type == "artifact_stale":
            stale[payload.get("artifact_id")] = {
                "artifact_id": payload.get("artifact_id"),
                "reason": payload.get("reason"),
            }
        elif event_type == "artifact_reverified":
            stale.pop(payload.get("artifact_id"), None)
        elif event_type == "work_deferred":
            deferred.append({
                "summary": payload.get("summary"),
                "work_id": payload.get("work_id"),
            })
        elif event_type == "work_canceled":
            canceled.append({
                "summary": payload.get("summary"),
                "work_id": payload.get("work_id"),
            })

    missing = _projection_missing_inputs(fixed_inputs)
    if completion_next_missing:
        missing.append("work_completed.payload.next")
    conflicts = []
    if _work_start_conflict(event_records):
        conflicts.append(
            "concurrent work_started events have different work_item_id"
        )
        current_activity["work_item_id"] = None
    if conflicts:
        diagnostic_status = "inconsistent"
        next_action = "Resolve conflicting active work"
    elif missing:
        diagnostic_status = "incomplete"
        if "work_completed.payload.next" in missing:
            next_action = "Repair missing work_completed next action"
        else:
            next_action = "Repair missing projection inputs"
    else:
        diagnostic_status = "complete"
    return {
        "blockers": list(blockers.values()),
        "canceled": canceled,
        "current_activity": current_activity,
        "deferred": deferred,
        "diagnostics": {
            "conflicts": conflicts,
            "missing": missing,
            "status": diagnostic_status,
        },
        "freshness": input_record.get("freshness"),
        "generated_at": input_record.get("generated_at"),
        "human_decisions": list(decisions.values()),
        "inputs": list(fixed_inputs),
        "next": next_action,
        "plan": plan,
        "project_id": input_record.get("project_id"),
        "schema_version": 1,
        "stale": list(stale.values()),
    }


def _render_diagnostic(projection):
    diagnostics = projection["diagnostics"]
    status = diagnostics["status"].upper()
    lines = [
        "ReviewCompass3 Current Work",
        f"STATUS: {status}",
    ]
    if diagnostics["missing"]:
        lines.append("missing:")
        lines.extend(f"  - {item}" for item in diagnostics["missing"])
    if diagnostics["conflicts"]:
        lines.append("conflicts:")
        lines.extend(f"  - {item}" for item in diagnostics["conflicts"])
    lines.extend(("next:", f"  - {projection['next']}"))
    return "\n".join(lines) + "\n"


def render_current_work(projection, *, mode):
    """同じstructured projectionからshort／detailed textを生成する。"""

    record = _mapping(projection, field="current work projection")
    diagnostics = _mapping(
        record.get("diagnostics"),
        field="projection diagnostics",
    )
    if diagnostics.get("status") != "complete":
        return _render_diagnostic(record)
    plan = record["plan"]
    activity = record["current_activity"]
    if mode == "short":
        return (
            f"RC3 | {plan['work_id']} | {plan['state']} | "
            f"blockers:{len(record['blockers'])} | "
            f"decisions:{len(record['human_decisions'])} | "
            f"next:{record['next']}\n"
        )
    if mode != "detailed":
        raise SessionLogBootstrapError("Unknown current work render mode")
    lines = [
        "ReviewCompass3 Current Work",
        f"generated_at: {record['generated_at']}",
        f"freshness: {record['freshness']}",
        "inputs:",
    ]
    lines.extend(
        f"  - {item['identity']} {item['digest']}"
        for item in record["inputs"]
    )
    lines.extend((
        "",
        "PLAN",
        f"  stage: {plan['stage']}",
        f"  work: {plan['work_id']} {plan['work_name']}",
        f"  state: {plan['state']}",
        "",
        "CURRENT ACTIVITY",
        f"  contract: {activity['contract_id'] or 'none'}",
        f"  work_item: {activity['work_item_id'] or 'none'}",
        f"  tdd_state: {activity['tdd_state'] or 'none'}",
        "",
        "NEXT",
        f"  {record['next']}",
        "",
        "BLOCKERS",
        "  none" if not record["blockers"] else "  present",
        "",
        "HUMAN DECISIONS",
        "  none" if not record["human_decisions"] else "  present",
        "",
        "STALE / REVERIFY",
        "  none" if not record["stale"] else "  present",
    ))
    return "\n".join(lines) + "\n"


def run_session_bootstrap(
    profile,
    *,
    raw_bytes,
    layout,
    projection_inputs,
    renderer=None,
):
    """session lifecycleを保存し、現在位置textまで一続きに生成する。"""

    capture = persist_session_capture(
        profile,
        raw_bytes=raw_bytes,
        layout=layout,
    )
    saved_events = _parse_raw_events(capture.raw_path.read_bytes())
    event_types = tuple(event.get("event_type") for event in saved_events)
    session_lifecycle = {
        "ended": "session_ended" in event_types,
        "event_count": len(saved_events),
        "started": "session_started" in event_types,
    }
    projection = project_current_work(
        saved_events,
        inputs=projection_inputs,
    )
    diagnostic_status = projection["diagnostics"]["status"]
    authority_status = (
        "valid"
        if diagnostic_status == "complete"
        else diagnostic_status
    )
    text_renderer = render_current_work if renderer is None else renderer
    if not callable(text_renderer):
        raise SessionLogBootstrapError("renderer must be callable")
    try:
        short_text = text_renderer(projection, mode="short")
        detailed_text = text_renderer(projection, mode="detailed")
    except Exception:
        short_text = None
        detailed_text = None
        display_status = "failed"
        display_error = "renderer_failed"
    else:
        display_status = "rendered"
        display_error = None
    return SessionBootstrapResult(
        capture=capture,
        session_lifecycle=session_lifecycle,
        projection=projection,
        short_text=short_text,
        detailed_text=detailed_text,
        authority_status=authority_status,
        display_status=display_status,
        display_error=display_error,
    )
