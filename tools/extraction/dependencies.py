"""第2段の順方向・逆方向依存展開。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json


ALLOWED_RELATIONS = frozenset({
  "calls",
  "derived_from",
  "introduced_by",
  "produces",
  "references",
  "tests",
  "validated_by",
  "verified_by",
})


class DependencyExpansionError(Exception):
  """依存グラフを一意かつ安全に展開できない。"""


@dataclasses.dataclass(frozen=True, order=True)
class DependencyEdge:
  source: str
  target: str
  relation: str


@dataclasses.dataclass(frozen=True)
class DependencyExpansion:
  status: str
  forward_nodes: tuple
  reverse_nodes: tuple
  traversed_edges: tuple
  unexpanded_edges: tuple
  digest: str


def _valid_identifier(value):
  return (
    isinstance(value, str)
    and bool(value)
    and "\x00" not in value
    and "\n" not in value
  )


def _parse_edge(value):
  if (
    not isinstance(value, dict)
    or set(value) != {"source", "target", "relation"}
    or not _valid_identifier(value["source"])
    or not _valid_identifier(value["target"])
    or value["relation"] not in ALLOWED_RELATIONS
  ):
    raise DependencyExpansionError(
      "Dependency edges require fixed valid fields"
    )
  return DependencyEdge(
    source=value["source"],
    target=value["target"],
    relation=value["relation"],
  )


def _walk(roots, adjacency):
  visited = set(roots)
  traversed = set()
  pending = list(sorted(roots))
  while pending:
    node = pending.pop(0)
    for next_node, edge in adjacency.get(node, ()):
      traversed.add(edge)
      if next_node not in visited:
        visited.add(next_node)
        pending.append(next_node)
        pending.sort()
  return visited, traversed


def expand_dependency_graph(
  nodes,
  edges,
  *,
  roots,
) -> DependencyExpansion:
  node_values = tuple(nodes)
  root_values = tuple(roots)
  if (
    not node_values
    or len(set(node_values)) != len(node_values)
    or any(not _valid_identifier(node) for node in node_values)
    or not root_values
    or len(set(root_values)) != len(root_values)
    or not set(root_values) <= set(node_values)
  ):
    raise DependencyExpansionError(
      "Nodes and roots must be unique valid identifiers"
    )

  edge_values = tuple(_parse_edge(edge) for edge in edges)
  if len(set(edge_values)) != len(edge_values):
    raise DependencyExpansionError(
      "Dependency edges must be unique"
    )

  node_set = set(node_values)
  valid_edges = tuple(
    edge
    for edge in edge_values
    if edge.source in node_set and edge.target in node_set
  )
  dangling_edges = set(edge_values) - set(valid_edges)
  forward_adjacency = {}
  reverse_adjacency = {}
  for edge in valid_edges:
    forward_adjacency.setdefault(edge.source, []).append(
      (edge.target, edge)
    )
    reverse_adjacency.setdefault(edge.target, []).append(
      (edge.source, edge)
    )
  for adjacency in (
    forward_adjacency,
    reverse_adjacency,
  ):
    for node in adjacency:
      adjacency[node].sort(
        key=lambda item: (item[0], item[1])
      )

  forward_nodes, forward_edges = _walk(
    root_values,
    forward_adjacency,
  )
  reverse_nodes, reverse_edges = _walk(
    root_values,
    reverse_adjacency,
  )
  traversed = forward_edges | reverse_edges
  unexpanded = (
    dangling_edges
    | (set(valid_edges) - traversed)
  )
  document = {
    "forward_nodes": sorted(forward_nodes),
    "reverse_nodes": sorted(reverse_nodes),
    "roots": sorted(root_values),
    "schema_version": 1,
    "traversed_edges": [
      dataclasses.asdict(edge)
      for edge in sorted(traversed)
    ],
    "unexpanded_edges": [
      dataclasses.asdict(edge)
      for edge in sorted(unexpanded)
    ],
  }
  digest = hashlib.sha256(
    json.dumps(
      document,
      ensure_ascii=False,
      separators=(",", ":"),
      sort_keys=True,
    ).encode("utf-8")
  ).hexdigest()
  return DependencyExpansion(
    status="blocked" if unexpanded else "complete",
    forward_nodes=tuple(sorted(forward_nodes)),
    reverse_nodes=tuple(sorted(reverse_nodes)),
    traversed_edges=tuple(sorted(traversed)),
    unexpanded_edges=tuple(sorted(unexpanded)),
    digest=digest,
  )
