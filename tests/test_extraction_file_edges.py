"""固定blob間の実在依存辺抽出に関する暫定テスト。"""

import importlib


def test_extracts_import_test_and_document_reference_edges():
  edges = importlib.import_module(
    "tools.extraction.file_edges"
  )
  result = edges.extract_file_edges({
    "source:tools/app.py": "from tools import lib\n",
    "source:tools/lib.py": "VALUE = 1\n",
    "source:tests/test_app.py": "import tools.app\n",
    "source:docs/design.md": "実装は `tools/app.py` を参照する。\n",
  })

  assert result.status == "complete"
  assert tuple(
    (edge.source, edge.target, edge.relation)
    for edge in result.edges
  ) == (
    ("source:docs/design.md", "source:tools/app.py", "references"),
    ("source:tests/test_app.py", "source:tools/app.py", "tests"),
    ("source:tools/app.py", "source:tools/lib.py", "imports"),
  )
  assert result.unresolved == ()


def test_preserves_unresolved_internal_and_dynamic_imports():
  edges = importlib.import_module(
    "tools.extraction.file_edges"
  )
  result = edges.extract_file_edges({
    "source:tools/app.py": (
      "import tools.missing\n"
      "import importlib\n"
      "name = input()\n"
      "importlib.import_module(name)\n"
    ),
  })

  assert result.status == "blocked"
  assert tuple(item.kind for item in result.unresolved) == (
    "dynamic_import",
    "missing_internal_import",
  )
