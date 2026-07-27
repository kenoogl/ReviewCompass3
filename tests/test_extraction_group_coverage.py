"""既知正例群の抽出被覆に関する暫定テスト。"""

import importlib

import pytest


def test_requires_resolution_for_every_candidate_and_every_group():
  coverage = importlib.import_module(
    "tools.extraction.group_coverage"
  )
  result = coverage.cover_known_positive_groups(
    {
      "group-a": ("source:a.py", "source:test_a.py"),
      "group-b": ("source:b.md",),
    },
    (
      {
        "candidate": "source:a.py",
        "action": "extract",
        "essence_id": "ESS-0001",
        "rationale": "実装契約",
      },
      {
        "candidate": "source:test_a.py",
        "action": "not_selected",
        "essence_id": None,
        "rationale": "ESS-0001の関連テストとして保持",
      },
      {
        "candidate": "source:b.md",
        "action": "extract",
        "essence_id": "ESS-0002",
        "rationale": "判断根拠",
      },
    ),
  )

  assert result.status == "complete"
  assert result.extracted == (
    ("source:a.py", "ESS-0001"),
    ("source:b.md", "ESS-0002"),
  )
  assert result.not_selected == ("source:test_a.py",)
  assert result.covered_groups == ("group-a", "group-b")


@pytest.mark.parametrize(
  "resolutions",
  (
    (),
    ({
      "candidate": "source:a.py",
      "action": "not_selected",
      "essence_id": None,
      "rationale": "",
    },),
    ({
      "candidate": "outside.py",
      "action": "extract",
      "essence_id": "ESS-0001",
      "rationale": "範囲外",
    },),
  ),
)
def test_rejects_missing_unreasoned_or_outside_resolutions(resolutions):
  coverage = importlib.import_module(
    "tools.extraction.group_coverage"
  )

  with pytest.raises(coverage.GroupCoverageError):
    coverage.cover_known_positive_groups(
      {"group-a": ("source:a.py",)},
      resolutions,
    )
