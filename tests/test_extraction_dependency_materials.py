"""固定材料集合からの内部依存閉包に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib


def test_expands_internal_materials_forward_and_reverse():
  expansion = importlib.import_module(
    "tools.extraction.dependency_materials"
  )
  documents = {
    "ReviewCompass:tools/api/entry.py": (
      "from tools.api.helper import run\n"
      "import requests\n"
    ),
    "ReviewCompass:tools/api/helper.py": (
      "from tools.shared import value\n"
    ),
    "ReviewCompass:tools/shared.py": "value = 1\n",
    "ReviewCompass:tests/test_entry.py": (
      "from tools.api.entry import main\n"
    ),
    "ReviewCompass:tools/orphan.py": (
      "from tools.absent import value\n"
    ),
  }

  result = expansion.expand_dependency_materials(
    documents,
    roots=("ReviewCompass:tools/api/entry.py",),
  )

  assert result.status == "complete"
  assert result.forward_materials == (
    "ReviewCompass:tools/api/entry.py",
    "ReviewCompass:tools/api/helper.py",
    "ReviewCompass:tools/shared.py",
  )
  assert result.reverse_materials == (
    "ReviewCompass:tests/test_entry.py",
    "ReviewCompass:tools/api/entry.py",
  )
  assert result.added_materials == (
    "ReviewCompass:tests/test_entry.py",
    "ReviewCompass:tools/api/helper.py",
    "ReviewCompass:tools/shared.py",
  )
  assert tuple(
    (edge.source, edge.target)
    for edge in result.edges
  ) == (
    (
      "ReviewCompass:tests/test_entry.py",
      "ReviewCompass:tools/api/entry.py",
    ),
    (
      "ReviewCompass:tools/api/entry.py",
      "ReviewCompass:tools/api/helper.py",
    ),
    (
      "ReviewCompass:tools/api/helper.py",
      "ReviewCompass:tools/shared.py",
    ),
  )
  assert result.external_modules == ("requests",)
  assert result.unresolved == ()
  assert len(result.digest) == 64


def test_keeps_dynamic_and_missing_internal_dependencies_distinct():
  expansion = importlib.import_module(
    "tools.extraction.dependency_materials"
  )
  documents = {
    "ReviewCompass:tools/entry.py": (
      "import importlib\n"
      "from tools.missing import value\n"
      "importlib.import_module(module_name)\n"
    ),
  }

  result = expansion.expand_dependency_materials(
    documents,
    roots=("ReviewCompass:tools/entry.py",),
  )

  assert result.status == "blocked"
  assert tuple(
    (item.kind, item.source, item.reference)
    for item in result.unresolved
  ) == (
    (
      "dynamic_import",
      "ReviewCompass:tools/entry.py",
      "importlib.import_module",
    ),
    (
      "missing_internal_import",
      "ReviewCompass:tools/entry.py",
      "tools.missing.value",
    ),
  )
  assert result.external_modules == ("importlib",)


def test_dependency_material_expansion_is_deterministic():
  expansion = importlib.import_module(
    "tools.extraction.dependency_materials"
  )
  documents = {
    "ReviewCompass:tools/a.py": "from tools.b import value\n",
    "ReviewCompass:tools/b.py": "value = 1\n",
  }

  first = expansion.expand_dependency_materials(
    documents,
    roots=("ReviewCompass:tools/a.py",),
  )
  second = expansion.expand_dependency_materials(
    dict(reversed(tuple(documents.items()))),
    roots=("ReviewCompass:tools/a.py",),
  )

  assert first == second
