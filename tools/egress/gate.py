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
import json

from tools.egress.approval import (
  ApprovalError,
  payload_list_digest,
  scan_outbound_text,
  validate_approval_record,
)
from tools.egress.payload import (
  EgressPayload,
  PayloadError,
  verify_fragment_provenance,
)

DEFAULT_SIZE_LIMIT_KB = 45

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
  approval_record,
  provider,
  model,
  redaction_hook,
  now,
  size_limit_kb=DEFAULT_SIZE_LIMIT_KB,
):
  """条件1〜6・8を検査する。全て合格のときだけallowed。"""
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
    validate_approval_record(
      approval_record,
      payload_list_digest=payload_list_digest(approved),
      provider=provider,
      model=model,
      purpose="implementation_sameness_judgment",
      now=now,
    )
  except ApprovalError as error:
    block(str(error), "承認recordを確認し、必要ならHumanの承認を取り直す")

  if redaction_hook is None:
    block(
      "伏字化が適用されていない",
      "伏字化hookを結線して再実行する（合格を送信根拠にはしない）",
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
