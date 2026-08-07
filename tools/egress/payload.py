"""送信payloadの構成と由来の解決（出口設計v4 §3・§5条件1〜2）。

外部へ送れるものは3種のみ：code断片（行範囲からの機械切り出し）、
数値・列挙値の機械特徴量（allowlist）、承認済みtemplateの定型文。
自由文fieldは型として通らない。payloadの内容は正準JSONとして固定し、
SHA-256で結線する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json
from pathlib import Path


class PayloadError(Exception):
  """payloadを安全に構成できない。"""


PAYLOAD_SCHEMA_VERSION = 1

MACHINE_FEATURE_ALLOWLIST = frozenset({
  "parameter_count",
  "line_count",
  "branch_count",
  "return_count",
  "raise_count",
  "max_nesting_depth",
  "complexity_signal",
  "public_api_signal",
})

_ENUM_FEATURE_VALUES = {
  "complexity_signal": frozenset({"low", "medium", "high"}),
  "public_api_signal": frozenset({"low", "medium", "high"}),
}

QUESTION_TEMPLATES = {
  "impl-sameness-v1": (
    "この2つの断片は同じ処理を実装しているか。相違点はどこか。"
  ),
}


@dataclasses.dataclass(frozen=True)
class CodeFragment:
  relative_path: str
  start_line: int
  end_line: int
  content: str
  content_sha256: str


@dataclasses.dataclass(frozen=True)
class EgressPayload:
  fragment_a: CodeFragment
  fragment_b: CodeFragment
  machine_features_a: dict
  machine_features_b: dict
  question_id: str
  question_text: str
  content: str
  digest: str


def _resolve_within(repository_root, relative_path):
  root = Path(repository_root).resolve()
  candidate = Path(relative_path)
  if candidate.is_absolute() or ".." in candidate.parts:
    raise PayloadError(f"path escapes the repository: {relative_path}")
  resolved = (root / candidate).resolve()
  if root != resolved and root not in resolved.parents:
    raise PayloadError(f"path escapes the repository: {relative_path}")
  return resolved


def cut_code_fragment(repository_root, code_reference):
  """code_referenceの行範囲をfileから機械的に切り出す。手書き文字列は通らない。"""
  if not isinstance(code_reference, dict):
    raise PayloadError("code_reference must be a mapping")
  relative_path = code_reference.get("relative_path")
  start_line = code_reference.get("start_line")
  end_line = code_reference.get("end_line")
  if not isinstance(relative_path, str) or not relative_path:
    raise PayloadError("code_reference requires relative_path")
  if not isinstance(start_line, int) or not isinstance(end_line, int):
    raise PayloadError("code_reference requires integer line bounds")
  resolved = _resolve_within(repository_root, relative_path)
  if not resolved.is_file():
    raise PayloadError(f"source file is missing: {relative_path}")
  lines = resolved.read_text(encoding="utf-8").splitlines()
  if start_line < 1 or end_line > len(lines) or start_line > end_line:
    raise PayloadError(
      f"line range is out of bounds: {relative_path}"
      f" {start_line}-{end_line} (file has {len(lines)} lines)"
    )
  content = "\n".join(lines[start_line - 1:end_line])
  return CodeFragment(
    relative_path=relative_path,
    start_line=start_line,
    end_line=end_line,
    content=content,
    content_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
  )


def verify_fragment_provenance(repository_root, fragment):
  """断片が現在のfile内容から機械切り出しされたものと一致するかを照合する。"""
  recut = cut_code_fragment(
    repository_root,
    {
      "relative_path": fragment.relative_path,
      "start_line": fragment.start_line,
      "end_line": fragment.end_line,
    },
  )
  if recut.content_sha256 != fragment.content_sha256:
    raise PayloadError(
      "fragment no longer matches its source: "
      f"{fragment.relative_path} {fragment.start_line}-{fragment.end_line}"
    )


def build_machine_features(routine):
  """allowlistの数値・列挙値だけを通す。自由文fieldは型として通らない。"""
  if not isinstance(routine, dict):
    raise PayloadError("routine must be a mapping")
  signature = routine.get("signature")
  if not isinstance(signature, dict) or not isinstance(
    signature.get("parameters"), list
  ):
    raise PayloadError("routine signature must carry parameters")
  features = {"parameter_count": len(signature["parameters"])}
  for field in MACHINE_FEATURE_ALLOWLIST:
    if field == "parameter_count" or field not in routine:
      continue
    value = routine[field]
    allowed_enum = _ENUM_FEATURE_VALUES.get(field)
    if allowed_enum is not None:
      if value not in allowed_enum:
        raise PayloadError(f"feature {field} has a non-enumerated value")
      features[field] = value
      continue
    if isinstance(value, bool) or not isinstance(value, int):
      raise PayloadError(f"feature {field} must be an integer")
    features[field] = value
  return features


def resolve_question(question_id):
  """承認済みtemplateの定型文を返す。未承認の問いは通らない。"""
  if question_id not in QUESTION_TEMPLATES:
    raise PayloadError(f"question template is not approved: {question_id}")
  return QUESTION_TEMPLATES[question_id]


def _fragment_document(fragment):
  return {
    "relative_path": fragment.relative_path,
    "start_line": fragment.start_line,
    "end_line": fragment.end_line,
    "content": fragment.content,
    "content_sha256": fragment.content_sha256,
  }


def build_pair_payload(
  *,
  repository_root,
  routine_a,
  routine_b,
  question_id,
):
  """1組の比較payloadを3種の構成要素だけから機械的に組み立てる。"""
  question_text = resolve_question(question_id)
  fragment_a = cut_code_fragment(
    repository_root, routine_a.get("code_reference")
  )
  fragment_b = cut_code_fragment(
    repository_root, routine_b.get("code_reference")
  )
  features_a = build_machine_features(routine_a)
  features_b = build_machine_features(routine_b)
  document = {
    "schema_version": PAYLOAD_SCHEMA_VERSION,
    "question_id": question_id,
    "question_text": question_text,
    "fragment_a": _fragment_document(fragment_a),
    "fragment_b": _fragment_document(fragment_b),
    "machine_features_a": features_a,
    "machine_features_b": features_b,
  }
  content = json.dumps(
    document, ensure_ascii=False, separators=(",", ":"), sort_keys=True
  )
  return EgressPayload(
    fragment_a=fragment_a,
    fragment_b=fragment_b,
    machine_features_a=features_a,
    machine_features_b=features_b,
    question_id=question_id,
    question_text=question_text,
    content=content,
    digest=hashlib.sha256(content.encode("utf-8")).hexdigest(),
  )
