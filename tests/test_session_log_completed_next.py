"""Work完了eventのNEXT遷移に関する回帰テスト。"""

import importlib


def _bootstrap():
    return importlib.import_module(
        "tools.development.session_log_bootstrap"
    )


def _inputs():
    return {
        "fixed_inputs": [
            {
                "digest": "a" * 64,
                "identity": "docs/current/reviewcompass3-plan-current.md",
            },
            {
                "digest": "b" * 64,
                "identity": "session:test-completed-next/events",
            },
        ],
        "freshness": "current",
        "generated_at": "2026-08-03T14:00:01+09:00",
        "project_id": "reviewcompass3",
    }


def _events(*, completion_payload):
    return (
        {
            "event_id": "evt-001",
            "event_type": "work_started",
            "occurred_at": "2026-08-03T13:00:00+09:00",
            "payload": {
                "contract_id": "TC-WORK1B",
                "next": "Complete repaired operational verification",
                "stage": "initial-development",
                "state": "active",
                "tdd_state": "green",
                "work_id": "Work 1B",
                "work_item_id": "RC3-WORK1B-OPERATIONAL-USE",
                "work_name": "Session Log Bootstrap",
            },
        },
        {
            "event_id": "evt-002",
            "event_type": "work_completed",
            "occurred_at": "2026-08-03T14:00:00+09:00",
            "payload": completion_payload,
        },
    )


def test_work_completed_replaces_started_next_with_completion_next():
    bootstrap = _bootstrap()
    projection = bootstrap.project_current_work(
        _events(
            completion_payload={
                "next": "Request Human approval for Work 1B completion",
            }
        ),
        inputs=_inputs(),
    )

    assert projection["plan"]["state"] == "completed"
    assert projection["current_activity"]["work_item_id"] is None
    assert projection["next"] == (
        "Request Human approval for Work 1B completion"
    )
    assert projection["diagnostics"] == {
        "conflicts": [],
        "missing": [],
        "status": "complete",
    }
    detailed = bootstrap.render_current_work(
        projection,
        mode="detailed",
    )
    assert "Request Human approval for Work 1B completion" in detailed
    assert "Complete repaired operational verification" not in detailed


def test_work_completed_without_next_is_incomplete():
    bootstrap = _bootstrap()
    projection = bootstrap.project_current_work(
        _events(completion_payload={}),
        inputs=_inputs(),
    )

    assert projection["diagnostics"] == {
        "conflicts": [],
        "missing": ["work_completed.payload.next"],
        "status": "incomplete",
    }
    assert projection["next"] == (
        "Repair missing work_completed next action"
    )
    detailed = bootstrap.render_current_work(
        projection,
        mode="detailed",
    )
    assert "STATUS: INCOMPLETE" in detailed
    assert "work_completed.payload.next" in detailed
