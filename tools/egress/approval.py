"""承認recordの機械検証（出口設計v4 §4）。

送信物一覧への承認をHumanが与え、機械が7項目を照合する。
一覧に無いpayloadは送れない。一覧への承認は一度きり（排他claim）で、
送信自体は一覧の範囲内で小分けに行える。
構造は開発元ReviewCompassのexternal-api-approval-v1を参考に、
RC3の文脈で新しく書き直した（codeのコピーはしていない）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import json
import os
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


class ApprovalError(Exception):
  """承認recordの検証または消費に失敗した。"""


APPROVAL_SCHEMA_VERSION = "egress-approval-v1"
APPROVED_PURPOSES = frozenset({"implementation_sameness_judgment"})

_SECRET_PATTERNS = (
  re.compile(r"\bapi[_-]?key\s*[:=]\s*\S+", re.I),
  re.compile(r"\b(?:token|password|passwd|secret)\s*[:=]\s*\S+", re.I),
  re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}", re.I),
  re.compile(r"\bsk-[A-Za-z0-9_-]{8,}"),
  # Human承認（2026-08-10）：資格情報3形式を走査対象へ追加する。
  re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
  re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"),
  re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
)
_EMAIL_PATTERN = re.compile(
  r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)
_PHONE_PATTERN = re.compile(r"\+?\d[\d ()-]{8,}\d")
# Human承認（2026-08-10）：64桁hex（Digest表現）は個人識別子判定の対象外。
# Digestは全payloadへ構造上必ず現れるため、除外しないと正常な送信が止まる。
_DIGEST_HEX_PATTERN = re.compile(r"\b[0-9a-fA-F]{64}\b")


def payload_list_digest(digests):
  """送信物一覧のdigest。順序に依らず決定的である。"""
  canonical = json.dumps(sorted(str(d) for d in digests))
  return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def scan_outbound_text(text):
  """送信直前文面の秘密値・個人識別子の走査。検出は送信拒否の理由になる。"""
  findings = []
  if any(pattern.search(text) for pattern in _SECRET_PATTERNS):
    findings.append("credential-like material detected in outbound text")
  if _EMAIL_PATTERN.search(text):
    findings.append("personal identifier (email) detected in outbound text")
  else:
    without_digests = _DIGEST_HEX_PATTERN.sub(" ", text)
    for match in _PHONE_PATTERN.finditer(without_digests):
      if len(re.sub(r"\D", "", match.group(0))) >= 10:
        findings.append(
          "personal identifier (phone) detected in outbound text"
        )
        break
  return findings


def _parse_expiry(value):
  if not isinstance(value, str) or not value.strip():
    return None
  try:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
  except ValueError:
    return None
  if parsed.tzinfo is None:
    return None
  return parsed


def validate_approval_record(
  record,
  *,
  payload_list_digest,
  provider,
  model,
  purpose,
):
  """承認recordの7項目を照合する。一つでも合わなければApprovalError。

  有効期限はcallerが渡す時刻ではなく実時刻で判定する（過去時刻の注入で
  期限切れrecordを合格させられないため）。
  """
  if not isinstance(record, dict):
    raise ApprovalError("approval record must be a mapping")
  errors = []
  if record.get("schema_version") != APPROVAL_SCHEMA_VERSION:
    errors.append("schema_version must be egress-approval-v1")
  if record.get("approved_by") != "user":
    errors.append("approved_by must be user")
  if record.get("payload_list_digest") != payload_list_digest:
    errors.append("payload list digest mismatch")
  if record.get("provider") != provider:
    errors.append("provider mismatch")
  if record.get("model") != model:
    errors.append("model mismatch")
  expires_at = _parse_expiry(record.get("expires_at"))
  if expires_at is None:
    errors.append("expires_at must be a timezone-aware ISO datetime")
  elif expires_at <= datetime.now(timezone.utc):
    errors.append("approval record is expired")
  if (
    record.get("purpose") not in APPROVED_PURPOSES
    or record.get("purpose") != purpose
  ):
    errors.append("purpose is not approved")
  policy = record.get("material_policy")
  if not isinstance(policy, dict) or not all(
    policy.get(flag) is True
    for flag in (
      "require_secret_scan",
      "forbid_credentials",
      "forbid_personal_identifiers",
    )
  ):
    errors.append("material_policy must enable all three protections")
  consumed = record.get("consumed")
  if not isinstance(consumed, bool):
    errors.append("consumed must be present and boolean")
  elif consumed:
    errors.append("approval record is already consumed")
  if errors:
    raise ApprovalError(
      "approval validation failed: " + "; ".join(errors)
    )


def load_approval_file(
  record_path,
  *,
  sha256,
  payload_list_digest,
  provider,
  model,
  purpose,
):
  """Human作成の承認record fileを読み、path＋SHA-256で束縛して検証する。

  一時辞書やcaller生成の値は承認として通らない。
  """
  path = Path(record_path)
  try:
    raw = path.read_bytes()
  except OSError as error:
    raise ApprovalError(
      f"approval record file is unreadable: {path}"
    ) from error
  if not isinstance(sha256, str) or hashlib.sha256(
    raw
  ).hexdigest() != sha256:
    raise ApprovalError(
      f"approval record file does not match its declared digest: {path}"
    )
  try:
    record = json.loads(raw.decode("utf-8"))
  except (UnicodeDecodeError, ValueError) as error:
    raise ApprovalError(
      f"approval record file is not valid JSON: {path}"
    ) from error
  validate_approval_record(
    record,
    payload_list_digest=payload_list_digest,
    provider=provider,
    model=model,
    purpose=purpose,
  )
  return record


def _claim_path(record_path):
  path = Path(record_path)
  return path.parent / f".{path.name}.consume-claim"


@contextmanager
def approval_claim(record_path):
  """承認recordの消費を直列化する排他claim。二重取得はApprovalError。"""
  claim = _claim_path(record_path)
  try:
    descriptor = os.open(
      claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600
    )
  except FileExistsError as error:
    raise ApprovalError(
      "approval record is already being consumed"
    ) from error
  try:
    os.close(descriptor)
    yield claim
  finally:
    try:
      claim.unlink()
    except FileNotFoundError:
      pass


def mark_consumed(record_path):
  """承認recordを消費済みにする。一覧への承認は一度きりである。"""
  path = Path(record_path)
  with approval_claim(path):
    try:
      record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
      raise ApprovalError(f"approval record is unreadable: {path}") from error
    if not isinstance(record, dict):
      raise ApprovalError("approval record must be a mapping")
    record["consumed"] = True
    path.write_text(
      json.dumps(record, ensure_ascii=False, sort_keys=True, indent=1)
      + "\n",
      encoding="utf-8",
    )
