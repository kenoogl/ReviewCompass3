"""第2段の双方向依存展開に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import importlib

import pytest


def test_expands_forward_and_reverse_closure_from_user_entry():
  dependencies = importlib.import_module(
    "tools.extraction.dependencies"
  )
  nodes = (
    "caller",
    "cli",
    "orchestrator",
    "implementation",
    "test",
    "design",
    "failure",
  )
  edges = (
    {"source": "caller", "target": "cli", "relation": "calls"},
    {"source": "cli", "target": "orchestrator", "relation": "calls"},
    {
      "source": "orchestrator",
      "target": "implementation",
      "relation": "calls",
    },
    {
      "source": "implementation",
      "target": "test",
      "relation": "verified_by",
    },
    {"source": "test", "target": "design", "relation": "derived_from"},
    {"source": "design", "target": "failure", "relation": "introduced_by"},
  )

  result = dependencies.expand_dependency_graph(
    nodes,
    edges,
    roots=("cli",),
  )

  assert result.status == "complete"
  assert result.forward_nodes == (
    "cli",
    "design",
    "failure",
    "implementation",
    "orchestrator",
    "test",
  )
  assert result.reverse_nodes == ("caller", "cli")
  assert len(result.traversed_edges) == 6
  assert result.unexpanded_edges == ()
  assert len(result.digest) == 64


def test_blocks_when_an_edge_is_dangling_or_disconnected_from_roots():
  dependencies = importlib.import_module(
    "tools.extraction.dependencies"
  )

  result = dependencies.expand_dependency_graph(
    ("cli", "implementation", "orphan-a", "orphan-b"),
    (
      {"source": "cli", "target": "implementation", "relation": "calls"},
      {"source": "orphan-a", "target": "orphan-b", "relation": "calls"},
      {"source": "implementation", "target": "missing", "relation": "tests"},
    ),
    roots=("cli",),
  )

  assert result.status == "blocked"
  assert tuple(
    (edge.source, edge.target)
    for edge in result.unexpanded_edges
  ) == (
    ("implementation", "missing"),
    ("orphan-a", "orphan-b"),
  )


@pytest.mark.parametrize(
  ("nodes", "edges", "roots"),
  (
    (("a", "a"), (), ("a",)),
    (("a",), (), ("missing",)),
    (
      ("a", "b"),
      (
        {"source": "a", "target": "b", "relation": "calls"},
        {"source": "a", "target": "b", "relation": "calls"},
      ),
      ("a",),
    ),
    (
      ("a", "b"),
      ({"source": "a", "target": "b", "relation": "unknown"},),
      ("a",),
    ),
  ),
)
def test_rejects_ambiguous_graph_inputs(nodes, edges, roots):
  dependencies = importlib.import_module(
    "tools.extraction.dependencies"
  )

  with pytest.raises(dependencies.DependencyExpansionError):
    dependencies.expand_dependency_graph(
      nodes,
      edges,
      roots=roots,
    )
