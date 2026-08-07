"""反証I-4の処置：Issue本文が引用元候補の本文と一致することを固定する。

承認：DEC-ADVERSARIAL-REMEDY-I4-001
所見：records/development/2026-08-07-adversarial-review-batch1-legacy-systems-v1.md
"""

import hashlib
import json
from pathlib import Path

import pytest

from tools.development import issue_intake_v4 as intake

CONFIG = "config/development-issue-resolution-pilot-v4.json"
ISSUE_PATH = ".reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json"
PROJECT_ROOT = Path(".")


def _config():
    return intake.load_config(CONFIG)


def _issue():
    return json.loads(Path(ISSUE_PATH).read_text(encoding="utf-8"))


def _digest(document):
    payload = {key: value for key, value in document.items() if key != "content_digest"}
    return hashlib.sha256(
        json.dumps(
            payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")
    ).hexdigest()


def test_i4_issue_body_must_match_the_cited_candidate():
    """健全なrecordは、本文一致の検査を加えても通り続ける。"""

    assert intake.validate_v4_issue_record(
        _issue(), path=ISSUE_PATH, project_root=PROJECT_ROOT, config=_config()
    ) is True


def test_i4_rewritten_issue_body_is_rejected():
    """本文だけを差し替え、自己digestを合わせ直したrecordを拒否する。"""

    tampered = _issue()
    tampered["problem"] = "全く別の問題（差し替え）"
    tampered["content_digest"] = _digest(tampered)
    with pytest.raises(intake.IntakeError):
        intake.validate_v4_issue_record(
            tampered, path=ISSUE_PATH, project_root=PROJECT_ROOT, config=_config()
        )


def test_i4_truncated_issue_body_is_rejected():
    """本文の一部だけを削ったrecordも拒否する（部分的な書き換えを見逃さない）。"""

    tampered = _issue()
    tampered["problem"] = tampered["problem"][: len(tampered["problem"]) // 2]
    tampered["content_digest"] = _digest(tampered)
    with pytest.raises(intake.IntakeError):
        intake.validate_v4_issue_record(
            tampered, path=ISSUE_PATH, project_root=PROJECT_ROOT, config=_config()
        )
