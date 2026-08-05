"""Work 6A：Current Work Projectionの中核negative pathの受入テスト。

承認：`DEC-WORK5A-PROJECTION-ROUTING-001`（案A）
提案正本：`docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md`

案Aで固定するのは次の4分類である。正式projection本体はここで発明しない。

- 正式入力欠落：identityとDigestが揃わない固定入力を、無視して完全と表示しない。
- 第二正本化：手編集できる人向けhandoffを、現在位置のauthorityとして受け入れない。
- 欠測推測：freshnessが無い入力を`current`とみなさない。
- stale／競合の誤表示：staleなfreshnessと、同一identityのDigest競合を正常表示しない。

既存の被覆（欠測authority、並行work_startedの競合、表示器failureとauthority欠落の分離）は
`tests/test_session_log_bootstrap.py`と`tests/test_session_bootstrap_e2e.py`が持つ。
ここでは重複させず、未被覆の負例だけを固定する。
"""

import copy
import importlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).parents[1]
FIXTURE_ROOT = (
    PROJECT_ROOT
    / "tests"
    / "fixtures"
    / "development"
    / "session-log-bootstrap"
)


def _bootstrap():
    return importlib.import_module(
        "tools.development.session_log_bootstrap"
    )


def _json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonl(path):
    return tuple(
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    )


def _events():
    return _jsonl(FIXTURE_ROOT / "workflow-events.jsonl")


def _inputs():
    """既存fixtureの、現行実装が`complete`と判定する固定入力。"""

    return copy.deepcopy(_json(FIXTURE_ROOT / "projection-inputs.json"))


def _project(inputs):
    bootstrap = _bootstrap()
    return bootstrap.project_current_work(_events(), inputs=inputs)


def test_hand_editable_handoff_is_not_accepted_as_authority():
    """第二正本化：手編集できるTODO handoffを現在位置のauthorityにしない。"""

    inputs = _inputs()
    inputs["fixed_inputs"].append(
        {
            "digest": "0" * 64,
            "identity": "TODO_NEXT_SESSION.md",
        }
    )

    projection = _project(inputs)

    diagnostics = projection["diagnostics"]
    assert diagnostics["status"] != "complete"
    assert any(
        "TODO_NEXT_SESSION.md" in item for item in diagnostics["missing"]
    ), diagnostics


def test_stale_freshness_is_not_displayed_as_complete():
    """stale誤表示：freshnessがstaleの入力を完全な現在位置として表示しない。"""

    inputs = _inputs()
    inputs["freshness"] = "stale"

    projection = _project(inputs)

    assert projection["diagnostics"]["status"] != "complete"
    assert projection["freshness"] == "stale"


def test_missing_freshness_is_not_guessed_as_current():
    """欠測推測：freshnessが無い入力を`current`とみなさない。"""

    inputs = _inputs()
    del inputs["freshness"]

    projection = _project(inputs)

    diagnostics = projection["diagnostics"]
    assert diagnostics["status"] != "complete"
    assert any("freshness" in item for item in diagnostics["missing"]), diagnostics
    assert projection["freshness"] != "current"


def test_fixed_input_without_valid_digest_is_not_ignored():
    """正式入力欠落：Digestが64桁でない固定入力を、無視して完全と表示しない。"""

    inputs = _inputs()
    inputs["fixed_inputs"].append(
        {
            "digest": "unknown",
            "identity": "records/task-contract/first-review-task-contract.json",
        }
    )

    projection = _project(inputs)

    diagnostics = projection["diagnostics"]
    assert diagnostics["status"] != "complete"
    assert any(
        "records/task-contract/first-review-task-contract.json" in item
        for item in diagnostics["missing"]
    ), diagnostics


def test_conflicting_digests_for_one_identity_are_inconsistent():
    """競合誤表示：同一identityに異なるDigestがある入力を正常表示しない。"""

    inputs = _inputs()
    original = inputs["fixed_inputs"][0]
    inputs["fixed_inputs"].append(
        {
            "digest": "1" * 64,
            "identity": original["identity"],
        }
    )

    projection = _project(inputs)

    diagnostics = projection["diagnostics"]
    assert diagnostics["status"] == "inconsistent"
    assert any(
        original["identity"] in item for item in diagnostics["conflicts"]
    ), diagnostics


def test_stale_input_text_does_not_assert_a_normal_next_action():
    """誤表示の禁止：staleな入力で、次作業を断定した通常表示を返さない。

    現行は`freshness: stale`の一行を添えたまま、PLAN、CURRENT ACTIVITY、NEXTを
    正常な現在位置として断定表示する。stale時は診断表示へ切り替え、理由を示す。
    """

    bootstrap = _bootstrap()
    inputs = _inputs()
    inputs["freshness"] = "stale"

    projection = _project(inputs)
    detailed = bootstrap.render_current_work(projection, mode="detailed")
    short = bootstrap.render_current_work(projection, mode="short")

    assert "STATUS:" in detailed
    assert "NEXT\n  Implement Session Log Bootstrap mapping" not in detailed
    assert "Implement Session Log Bootstrap mapping" not in short
