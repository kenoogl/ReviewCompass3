"""正式再利用検索の計画JSON writer（finalize・verify）。

計画草稿へのcontent_digest埋め込みを手書きscriptから専用入口へ移す。
検証は検索側の`_validate_plan`をそのまま再利用し（複製しない）、
**検索と同一の検証に合格した計画だけ**がfileへ書かれる。

- finalize：digest無しの草稿→digest機械埋め込み→検証→合格時のみ書換え。
  不合格時はfileへ一切書かない。digest既存はalready_finalizedで停止。
- verify：完成計画の構造とdigestを照合。証明書（attestation）が既に存在する
  のは検索実施済みの正常状態として合格に含める（複数searchの計画では
  後続searchが未検証で終わる限界がある——単一search運用が前提）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import argparse
import json
import sys
from pathlib import Path

from tools.common import digests
from tools.development import formal_code_reuse_search as formal


def _emit(document):
    print(json.dumps(document, ensure_ascii=False, sort_keys=True))


def _stop(mode, plan_path, reason):
    _emit({
        "schema_version": 1,
        "status": "stopped",
        "mode": mode,
        "plan": str(plan_path),
        "reason": reason,
    })
    return 2


def _load(plan_path):
    return json.loads(Path(plan_path).read_text(encoding="utf-8"))


def _finalize(plan_path, project_root):
    try:
        document = _load(plan_path)
    except (OSError, ValueError):
        return _stop("finalize", plan_path, "plan_unreadable")
    if not isinstance(document, dict):
        return _stop("finalize", plan_path, "invalid_search_plan")
    if "content_digest" in document:
        return _stop("finalize", plan_path, "already_finalized")
    document["content_digest"] = digests.canonical_content_digest(document)
    try:
        formal._validate_plan(document, project_root)
    except formal.FormalCodeReuseSearchError as error:
        return _stop("finalize", plan_path, error.code)
    Path(plan_path).write_text(
        json.dumps(document, ensure_ascii=False, indent=1, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    _emit({
        "schema_version": 1,
        "status": "ok",
        "mode": "finalize",
        "plan": str(plan_path),
        "content_digest": document["content_digest"],
    })
    return 0


def _verify(plan_path, project_root):
    try:
        document = _load(plan_path)
    except (OSError, ValueError):
        return _stop("verify", plan_path, "plan_unreadable")
    try:
        formal._validate_plan(document, project_root)
    except formal.FormalCodeReuseSearchError as error:
        # attestationが既に在るのは検索実施済みの正常状態（構造・digest・
        # capability検証はこの停止に至る前に全て合格している）。
        if error.code != "output_already_exists":
            return _stop("verify", plan_path, error.code)
    _emit({
        "schema_version": 1,
        "status": "ok",
        "mode": "verify",
        "plan": str(plan_path),
        "content_digest": document.get("content_digest"),
    })
    return 0


def run(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("finalize", "verify"))
    parser.add_argument("--plan", required=True)
    parser.add_argument("--project-root", default=".")
    arguments = parser.parse_args(
        list(sys.argv[1:] if argv is None else argv)
    )
    if arguments.mode == "finalize":
        return _finalize(arguments.plan, arguments.project_root)
    return _verify(arguments.plan, arguments.project_root)


def main():
    raise SystemExit(run())


if __name__ == "__main__":
    main()
