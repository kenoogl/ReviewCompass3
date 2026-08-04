"""WI-003 rendererとrepository templateの結合Acceptance Test。"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = PROJECT_ROOT / "docs/development/templates/TODO_NEXT_SESSION.template.md"

REQUIRED_PROJECTION_HEADINGS = (
    "## 現在作業に影響する改善候補／Issue",
    "## 最新のauthority／Evidence",
)


def test_repository_template_declares_compact_projection_sections():
    content = TEMPLATE.read_text(encoding="utf-8")

    for heading in REQUIRED_PROJECTION_HEADINGS:
        assert content.count(heading) == 1
