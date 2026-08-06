"""AGENTS.mdの改善候補経路が行き止まりにならないことを固定するTest。

改善候補を登録した後のHuman仕分け判断を、どこへ記録するのかがAGENTS.mdに
書かれていない状態を防ぐ。あわせて、凍結された旧置き場所を新しい記録の
保存先として名指しする退行も防ぐ。
"""

import re
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENTS = PROJECT_ROOT / "AGENTS.md"

# 凍結された旧置き場所。件数とファイル名が固定されているため、新しい記録の
# 保存先にできない。凍結は意図的な設計判断であり、根拠は次のとおり。
#   - docs/design/2026-08-05-historical-todo-issue-intake-proposal.md §1.1
#     「旧記録は旧versionの規則のまま保持し、新規則で再判定しない」
#   - tools/development/issue_intake_v4.py の「V4 Issue永続化（schema 2）」注記
#     （旧Issue directoryは「旧Pilot subjectが1件」の検査を持つ）
#   - tests/test_issue_resolution_pilot.py
#     ::test_repository_contains_only_the_single_valid_pilot_subject
#     （issues=1件、triage-decisions<=1件を固定）
#   - tests/test_issue_intake_v4.py
#     ::test_k6_legacy_v1_decision_and_pilot_validation_keep_passing
#     （triage-decisionsのファイル名一覧を固定）
FROZEN_LANES = (
    ".reviewcompass/workflow/triage-decisions",
    ".reviewcompass/workflow/issues",
)

# 凍結された置き場所の後継。件数上限を持たないため、新しい記録はこちらへ入る。
SUCCESSOR_LANES = (
    ".reviewcompass/workflow/triage-decisions-v4",
    ".reviewcompass/workflow/issues-v4",
)

# 改善候補の経路を説明している箇所を見分ける手掛かり。
LANE_MARKERS = (
    ".reviewcompass/workflow/improvement-candidates",
    "improvement_candidate",
    "改善候補",
    "IC-",
    "OBS-",
)

# 改善候補に対するHumanの仕分け判断は、先例ではDecision recordとして
# records/development/配下に残されている。
# 例: records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md
TRIAGE_DECISION_RECORD_DIRECTORY = "records/development/"


def _bullet_blocks(text):
    """Markdownの箇条書きを、継続行を含めた塊の列にして返す。"""
    blocks = []
    current = None
    for line in text.splitlines():
        if line.startswith("- "):
            if current is not None:
                blocks.append("\n".join(current))
            current = [line]
        elif current is not None and line[:1].isspace() and line.strip():
            current.append(line)
        else:
            if current is not None:
                blocks.append("\n".join(current))
            current = None
    if current is not None:
        blocks.append("\n".join(current))
    return blocks


def _lane_guidance(text):
    """改善候補の経路を説明している箇所だけを取り出して連結する。"""
    return "\n".join(
        block
        for block in _bullet_blocks(text)
        if any(marker in block for marker in LANE_MARKERS)
    )


def _names_lane_literally(text, lane):
    """後継（`-v4`など）を巻き込まずに、その置き場所を名指ししているか判定する。"""
    pattern = re.escape(lane) + r"(?![0-9A-Za-z_-])"
    return re.search(pattern, text) is not None


def test_agents_lane_guidance_names_the_triage_decision_destination():
    agents = AGENTS.read_text(encoding="utf-8")
    guidance = _lane_guidance(agents)

    if ".reviewcompass/workflow/improvement-candidates" not in guidance:
        pytest.skip("AGENTS.mdに改善候補の登録手順が無いため、この検査は適用しない。")

    assert TRIAGE_DECISION_RECORD_DIRECTORY in guidance, (
        "改善候補の経路を説明している箇所に、Humanの仕分け判断の保存先"
        f"（{TRIAGE_DECISION_RECORD_DIRECTORY}）が示されていない。"
        "検証後の行き先が無く、経路が行き止まりになっている。"
    )


def test_agents_does_not_name_frozen_lanes_as_record_destinations():
    agents = AGENTS.read_text(encoding="utf-8")

    for lane in FROZEN_LANES:
        assert not _names_lane_literally(agents, lane), (
            f"AGENTS.mdが凍結された置き場所`{lane}`を新しい記録の保存先として"
            "名指ししている。件数とファイル名が固定されているため追加できない。"
        )

    # 後継を名指ししても、この検査には引っ掛からないことを併せて固定する。
    for lane in SUCCESSOR_LANES:
        assert not _names_lane_literally(lane, lane.rsplit("-v4", 1)[0])


def test_frozen_lane_inventory_is_not_stale():
    for lane in FROZEN_LANES:
        assert (PROJECT_ROOT / lane).is_dir(), (
            f"凍結された置き場所`{lane}`が実在しない。凍結リストが古びている。"
        )

    for lane in SUCCESSOR_LANES:
        assert (PROJECT_ROOT / lane).is_dir(), (
            f"後継の置き場所`{lane}`が実在しない。凍結リストが古びている。"
        )
