"""固定材料集合からの内部依存閉包。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import ast
import dataclasses
import hashlib
import json


@dataclasses.dataclass(frozen=True, order=True)
class MaterialEdge:
  source: str
  target: str
  relation: str = "imports"


@dataclasses.dataclass(frozen=True, order=True)
class UnresolvedMaterial:
  kind: str
  source: str
  reference: str


@dataclasses.dataclass(frozen=True)
class DependencyMaterialExpansion:
  status: str
  forward_materials: tuple
  reverse_materials: tuple
  added_materials: tuple
  edges: tuple
  external_modules: tuple
  unresolved: tuple
  digest: str


def _split_identifier(identifier):
  if not isinstance(identifier, str) or identifier.count(":") != 1:
    raise ValueError("material identifier must use source:path")
  return identifier.split(":", 1)


def _module_name(path):
  if not path.endswith(".py"):
    return None
  value = path[:-3].replace("/", ".")
  if value.endswith(".__init__"):
    value = value[:-9]
  return value


def _resolve_module(reference, modules):
  value = reference
  while value:
    target = modules.get(value)
    if target:
      return target
    if "." not in value:
      break
    value = value.rsplit(".", 1)[0]
  return None


def _walk(roots, adjacency):
  visited = set(roots)
  traversed = set()
  pending = list(sorted(roots))
  while pending:
    node = pending.pop(0)
    for target, edge in adjacency.get(node, ()):
      traversed.add(edge)
      if target not in visited:
        visited.add(target)
        pending.append(target)
        pending.sort()
  return visited, traversed


def _parse_imports(identifier, content, modules):
  if not isinstance(content, str):
    raise ValueError("material content must be text")
  try:
    tree = ast.parse(content)
  except SyntaxError:
    return (), (), (
      UnresolvedMaterial("syntax_error", identifier, identifier),
    )
  references = []
  dynamic = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Import):
      references.extend(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom) and node.level == 0:
      if node.module:
        references.extend(
          node.module + "." + alias.name
          for alias in node.names
        )
    elif (
      isinstance(node, ast.Call)
      and isinstance(node.func, ast.Attribute)
      and node.func.attr == "import_module"
      and isinstance(node.func.value, ast.Name)
      and node.func.value.id == "importlib"
    ):
      if (
        node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
      ):
        references.append(node.args[0].value)
      else:
        dynamic.append(UnresolvedMaterial(
          "dynamic_import",
          identifier,
          "importlib.import_module",
        ))
  edges = set()
  external = set()
  unresolved = set(dynamic)
  for reference in references:
    target = _resolve_module(reference, modules)
    if target:
      if target != identifier:
        edges.add(MaterialEdge(identifier, target))
    elif reference.startswith("tools."):
      unresolved.add(UnresolvedMaterial(
        "missing_internal_import",
        identifier,
        reference,
      ))
    else:
      external.add(reference.split(".", 1)[0])
  return tuple(sorted(edges)), tuple(sorted(external)), tuple(
    sorted(unresolved)
  )


def expand_dependency_materials(documents, *, roots):
  if not isinstance(documents, dict) or not documents:
    raise ValueError("documents must be a non-empty mapping")
  root_values = tuple(roots)
  if (
    not root_values
    or len(set(root_values)) != len(root_values)
    or not set(root_values) <= set(documents)
  ):
    raise ValueError("roots must be unique known materials")
  parsed = {
    identifier: _split_identifier(identifier)
    for identifier in documents
  }
  module_maps = {}
  for identifier, (source, path) in parsed.items():
    module = _module_name(path)
    if module:
      module_maps.setdefault(source, {})[module] = identifier
  all_edges = set()
  external_by_source = {}
  unresolved_by_source = {}
  for identifier in sorted(documents):
    source, path = parsed[identifier]
    if not path.endswith(".py"):
      continue
    edges, external, unresolved = _parse_imports(
      identifier,
      documents[identifier],
      module_maps.get(source, {}),
    )
    all_edges.update(edges)
    external_by_source[identifier] = external
    unresolved_by_source[identifier] = unresolved
  forward_adjacency = {}
  reverse_adjacency = {}
  for edge in sorted(all_edges):
    forward_adjacency.setdefault(edge.source, []).append(
      (edge.target, edge)
    )
    reverse_adjacency.setdefault(edge.target, []).append(
      (edge.source, edge)
    )
  forward, forward_edges = _walk(root_values, forward_adjacency)
  reverse, reverse_edges = _walk(root_values, reverse_adjacency)
  selected = forward | reverse
  edges = tuple(sorted(forward_edges | reverse_edges))
  external = tuple(sorted({
    module
    for identifier in selected
    for module in external_by_source.get(identifier, ())
  }))
  unresolved = tuple(sorted({
    item
    for identifier in selected
    for item in unresolved_by_source.get(identifier, ())
  }))
  document = {
    "added_materials": sorted(selected - set(root_values)),
    "edges": [dataclasses.asdict(edge) for edge in edges],
    "external_modules": list(external),
    "forward_materials": sorted(forward),
    "reverse_materials": sorted(reverse),
    "roots": sorted(root_values),
    "schema_version": 1,
    "unresolved": [
      dataclasses.asdict(item) for item in unresolved
    ],
  }
  digest = hashlib.sha256(json.dumps(
    document,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return DependencyMaterialExpansion(
    status="blocked" if unresolved else "complete",
    forward_materials=tuple(sorted(forward)),
    reverse_materials=tuple(sorted(reverse)),
    added_materials=tuple(sorted(selected - set(root_values))),
    edges=edges,
    external_modules=external,
    unresolved=unresolved,
    digest=digest,
  )
