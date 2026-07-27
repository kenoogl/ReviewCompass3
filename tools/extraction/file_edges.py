"""固定blob本文からの実在依存辺抽出。"""

import ast
import dataclasses
import hashlib
import json
import re


@dataclasses.dataclass(frozen=True, order=True)
class FileEdge:
  source: str
  target: str
  relation: str


@dataclasses.dataclass(frozen=True, order=True)
class UnresolvedFileReference:
  kind: str
  source: str
  reference: str


@dataclasses.dataclass(frozen=True)
class FileEdgeExtraction:
  status: str
  edges: tuple
  unresolved: tuple
  digest: str


def _split(identifier):
  if not isinstance(identifier, str) or identifier.count(":") != 1:
    raise ValueError("file identifier must use source:path")
  return identifier.split(":", 1)


def _module_name(path):
  if not path.endswith(".py"):
    return None
  value = path[:-3].replace("/", ".")
  if value.endswith(".__init__"):
    value = value[:-9]
  return value


def extract_file_edges(documents):
  if not isinstance(documents, dict) or not documents:
    raise ValueError("documents must be a non-empty mapping")
  parsed = {identifier: _split(identifier) for identifier in documents}
  module_maps = {}
  path_maps = {}
  for identifier, (source, path) in parsed.items():
    path_maps.setdefault(source, {})[path] = identifier
    module = _module_name(path)
    if module:
      module_maps.setdefault(source, {})[module] = identifier
  edges = set()
  unresolved = set()
  for identifier in sorted(documents):
    source_name, path = parsed[identifier]
    content = documents[identifier]
    if not isinstance(content, str):
      raise ValueError("document content must be text")
    if path.endswith(".py"):
      try:
        tree = ast.parse(content)
      except SyntaxError:
        unresolved.add(UnresolvedFileReference(
          "syntax_error", identifier, path,
        ))
        continue
      names = []
      for node in ast.walk(tree):
        if isinstance(node, ast.Import):
          names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
          if node.module:
            for alias in node.names:
              names.append(node.module + "." + alias.name)
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
            names.append(node.args[0].value)
          else:
            unresolved.add(UnresolvedFileReference(
              "dynamic_import", identifier, "importlib.import_module",
            ))
      for name in names:
        target = module_maps.get(source_name, {}).get(name)
        if target is None and "." in name:
          target = module_maps.get(source_name, {}).get(
            name.rsplit(".", 1)[0]
          )
        if target:
          relation = "tests" if "/test" in path else "imports"
          edges.add(FileEdge(identifier, target, relation))
        elif name.startswith("tools."):
          unresolved.add(UnresolvedFileReference(
            "missing_internal_import", identifier, name,
          ))
    else:
      for reference in re.findall(r"`([^`]+)`", content):
        target = path_maps.get(source_name, {}).get(reference)
        if target:
          edges.add(FileEdge(identifier, target, "references"))
  ordered_edges = tuple(sorted(edges))
  ordered_unresolved = tuple(sorted(unresolved))
  document = {
    "edges": [dataclasses.asdict(edge) for edge in ordered_edges],
    "schema_version": 1,
    "unresolved": [
      dataclasses.asdict(item) for item in ordered_unresolved
    ],
  }
  digest = hashlib.sha256(json.dumps(
    document,
    separators=(",", ":"),
    sort_keys=True,
  ).encode()).hexdigest()
  return FileEdgeExtraction(
    status="blocked" if ordered_unresolved else "complete",
    edges=ordered_edges,
    unresolved=ordered_unresolved,
    digest=digest,
  )
