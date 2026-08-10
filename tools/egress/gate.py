"""出口関門（出口設計v4 §5）。送信前検査の単一実装。

送信前に全条件を満たさなければ送信しない（fail-closed）。
停止時は理由と復旧手順を返し、自動修正はしない。
どの呼び出し経路もこの1実装を通ること（二重実装禁止）。
trusted経路の目録検証と応答不全のエスカレート（条件7・9）は
送信を実装する段階4の対象であり、本moduleは送信そのものを持たない。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import dataclasses
import hashlib
import json

from tools.egress.approval import (
  ApprovalError,
  load_approval_file,
  payload_list_digest,
  scan_outbound_text,
)
from tools.egress.payload import (
  MACHINE_FEATURE_ALLOWLIST,
  EgressPayload,
  PayloadError,
  fragment_document,
  machine_feature_violations,
  resolve_question,
  verify_fragment_provenance,
)
from tools.session_logs.redaction import default_pattern_rules, redact_text

DEFAULT_SIZE_LIMIT_KB = 45


def approved_redaction_hook(text):
  """段階1で許可される唯一の伏字化実装（出口設計v4 §8）。

  caller注入の任意callbackは実行しない。合格の根拠にはせず、
  内容が変わった場合は「本来入らない物が入っていた兆候」として拒否する。
  """
  return redact_text(text, default_pattern_rules()).text


APPROVED_REDACTION_HOOK = approved_redaction_hook

_EXPECTED_CONTENT_KEYS = frozenset({
  "schema_version",
  "question_id",
  "question_text",
  "fragment_a",
  "fragment_b",
  "machine_features_a",
  "machine_features_b",
})


@dataclasses.dataclass(frozen=True)
class GateResult:
  allowed: bool
  reasons: tuple
  recovery: tuple


def run_egress_gate(
  *,
  payload,
  repository_root,
  approved_payload_digests,
  approval_record_path,
  approval_record_sha256,
  provider,
  model,
  redaction_hook,
  size_limit_kb=DEFAULT_SIZE_LIMIT_KB,
):
  """条件1〜6・8を検査する。全て合格のときだけallowed。

  承認はHuman作成record file（path＋SHA-256）で渡す。辞書は受け取らない。
  伏字化hookは許可実装だけを受け付け、それ以外は**実行せず**拒否する。
  """
  reasons = []
  recovery = []

  def block(reason, step):
    reasons.append(f"{reason}（外部送信せず停止）")
    recovery.append(step)

  if not isinstance(payload, EgressPayload):
    block(
      "payloadが3種構成の型ではない",
      "build_pair_payloadで組み立て直す",
    )
    return GateResult(False, tuple(reasons), tuple(recovery))

  if hashlib.sha256(
    payload.content.encode("utf-8")
  ).hexdigest() != payload.digest:
    block(
      "payloadのdigestが内容の指紋と一致しない（偽造の兆候）",
      "build_pair_payloadで組み立て直し、一覧承認を取り直す",
    )

  try:
    document = json.loads(payload.content)
  except ValueError:
    document = None
  if not isinstance(document, dict) or set(document) != set(
    _EXPECTED_CONTENT_KEYS
  ):
    block(
      "payload内容が3種の構成要素と一致しない",
      "build_pair_payloadで組み立て直す",
    )
  else:
    try:
      expected_question = resolve_question(document.get("question_id"))
    except PayloadError:
      expected_question = None
    if (
      expected_question is None
      or document.get("question_text") != expected_question
    ):
      block(
        "問いが承認済みtemplateの定型文と一致しない",
        "resolve_questionの定型文だけを用いて組み立て直す",
      )
    for side, expected_features in (
      ("machine_features_a", payload.machine_features_a),
      ("machine_features_b", payload.machine_features_b),
    ):
      features = document.get(side)
      if machine_feature_violations(features):
        block(
          f"{side}にallowlist外のfieldまたは型違反の値が含まれる",
          "build_machine_featuresだけを用いて組み立て直す",
        )
      elif features != expected_features:
        block(
          f"{side}が送信JSONとpayload fieldで一致しない",
          "build_pair_payloadで組み立て直す",
        )
    for side, expected_fragment in (
      ("fragment_a", payload.fragment_a),
      ("fragment_b", payload.fragment_b),
    ):
      if document.get(side) != fragment_document(expected_fragment):
        block(
          f"{side}が送信JSONとpayload fieldで一致しない（自由文混入の兆候）",
          "build_pair_payloadで組み立て直す",
        )

  for fragment in (payload.fragment_a, payload.fragment_b):
    try:
      verify_fragment_provenance(repository_root, fragment)
    except PayloadError as error:
      block(
        f"code断片の由来が現在のsourceと一致しない: {error}",
        "payloadを現在のsourceから組み立て直し、一覧承認を取り直す",
      )

  approved = set(approved_payload_digests or [])
  if payload.digest not in approved:
    block(
      "payloadが承認済み送信物一覧に無い",
      "dry-runで一覧を再生成し、Humanの一覧承認を得る",
    )
  try:
    load_approval_file(
      approval_record_path,
      sha256=approval_record_sha256,
      payload_list_digest=payload_list_digest(approved),
      provider=provider,
      model=model,
      purpose="implementation_sameness_judgment",
    )
  except ApprovalError as error:
    block(str(error), "承認recordを確認し、必要ならHumanの承認を取り直す")

  if redaction_hook is None:
    block(
      "伏字化が適用されていない",
      "伏字化hookを結線して再実行する（合格を送信根拠にはしない）",
    )
  elif redaction_hook is not APPROVED_REDACTION_HOOK:
    block(
      "伏字化hookが許可実装ではない（実行せず拒否）",
      "gate.APPROVED_REDACTION_HOOKだけを渡す。任意callbackは段階1で実行しない",
    )
  else:
    masked = redaction_hook(payload.content)
    if masked != payload.content:
      block(
        "伏字化が内容を変更した＝本来入らない物が入っていた兆候",
        "payloadの構成規則を見直す。伏字化で直して送る運用はしない",
      )

  for finding in scan_outbound_text(payload.content):
    block(finding, "payloadの構成規則を見直し、混入源を特定する")

  size_kb = len(payload.content.encode("utf-8")) / 1024
  if size_kb > size_limit_kb:
    block(
      f"入力規模が上限を超えている（{size_kb:.1f}KB > {size_limit_kb}KB）",
      "対象を分割するか、上限の変更をHumanへ提案する（自動切り詰めはしない）",
    )

  return GateResult(not reasons, tuple(reasons), tuple(recovery))
