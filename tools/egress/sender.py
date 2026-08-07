"""段階1の送信係（出口設計v4 §8）。関門は通すが、送信は型として不可能。

実行境界（tools/bootstrap/review_execution.py）へ注入するrunnerを作る。
段階1では送信機能そのものを持たず、関門合格後も必ず
EgressSendingNotApprovedで停止する。実際の送信（段階4）は別提案の
Human承認を要する。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

from tools.egress.gate import run_egress_gate


class EgressGateRefusal(Exception):
  """出口関門が送信を拒否した（fail-closed）。"""


class EgressSendingNotApproved(Exception):
  """送信の実装（段階4）は未承認である。"""


def build_stage_one_runner(
  *,
  repository_root,
  approved_payload_digests,
  approval_record,
  provider,
  model,
  redaction_hook,
  now,
  size_limit_kb=None,
):
  """関門つきrunnerを作る。段階1では関門合格でも送信しない。"""

  def runner(assignment, payload):
    arguments = {
      "payload": payload,
      "repository_root": repository_root,
      "approved_payload_digests": approved_payload_digests,
      "approval_record": approval_record,
      "provider": provider,
      "model": model,
      "redaction_hook": redaction_hook,
      "now": now,
    }
    if size_limit_kb is not None:
      arguments["size_limit_kb"] = size_limit_kb
    result = run_egress_gate(**arguments)
    if not result.allowed:
      lines = list(result.reasons)
      lines.extend(f"復旧: {step}" for step in result.recovery)
      raise EgressGateRefusal("\n".join(lines))
    raise EgressSendingNotApproved(
      "外部送信の実装は段階4であり、本提案の範囲では承認されていない"
    )

  return runner
