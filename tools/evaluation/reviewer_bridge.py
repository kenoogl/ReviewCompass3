"""LLM reviewer接続adapter（データ取得順序3）。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

作業票：docs/development/2026-08-17-reviewer-bridge-work-ticket-v1.md（案A＝正式経路の機械駆動・
§4の変換表を実装する）。正式経路の部品（assemble・check）とTask Contractの封（seal）を
読み取り専用で使い、本moduleは製品本体へ手を入れない。外部起動はinjectable（launcher）であり、
実起動の結線は順序4（実験計画の承認）で行う。実起動系は`subprocess_guard`経由でのみ起動する
規約とし、試験はguardを禁止fakeへ差し替えて「起動ゼロ」を機械確認できる。
"""

import subprocess
from pathlib import Path

from tools.request_builder import core as request_builder
from tools.task_contract.identity import record_ref, seal

REVIEWER_NAME = "llm_review_via_launch"
RULE_ID = "llm_review"
UNRESOLVED = "unresolved"
_PLACEHOLDER_PREFIX = "<<記入:"


def subprocess_guard(*args, **kwargs):
    """実起動系が使う唯一のプロセス起動口（順序4で使用。試験は差し替えて禁止する）。"""

    return subprocess.run(*args, **kwargs)


def compose_request_body(contract, context_manifest):
    """Task Contract文脈からfree_text依頼の記入2欄を機械生成する。"""

    goal = contract["responsibility"]
    materials = "\n".join(
        "- `%s`（SHA-256 `%s`）" % (item["relative_path"], item["sha256"])
        for item in context_manifest["material_bundle"]
    )
    request_body = (
        "次のTask Contract実験ケースについて、対象materialの内容がContractの責務に"
        "照らして妥当かを検査してください。\n\n"
        "- 責務（goal）：%s\n"
        "- 対象material：\n%s\n\n"
        "検査の問い：対象の記述は責務・境界に整合するか。各findingへ根拠"
        "（file・行）を付けてください。" % (goal, materials)
    )
    decided_scope = (
        "1. 本依頼はTask Contract実験（paired trial）の1ケースである"
        "（評価データ取得計画v1）。\n"
        "2. 範囲外：対象materialの書き換え・Contract自体の改定提案・repo外の参照。\n"
        "3. 事実の明示：対象materialのdigestは本record §1の表に固定済み。"
    )
    return request_body, decided_scope


def build_free_text_request(
    *,
    repository,
    record_date,
    slug,
    title,
    target_paths,
    request_body,
    decided_scope,
):
    """assemble→機械記入（placeholder 2欄の置換）まで行い、record相対pathを返す。

    checkの実行とcommitは呼び出し側の責務（checkはcommit済み状態で最終合格になる）。
    """

    result = request_builder.assemble(
        repository=repository,
        request_type="free_text",
        record_date=record_date,
        slug=slug,
        title=title,
        target_paths=tuple(target_paths),
    )
    relative_path = result["record_relative_path"]
    path = Path(repository) / relative_path
    text = path.read_text(encoding="utf-8")
    replacements = [request_body, decided_scope]
    filled = []
    index = 0
    for line in text.splitlines():
        if line.startswith(_PLACEHOLDER_PREFIX):
            if index >= len(replacements):
                raise ValueError("unexpected extra placeholder")
            filled.append(replacements[index])
            index += 1
        else:
            filled.append(line)
    if index != len(replacements):
        raise ValueError("placeholder count mismatch: %d" % index)
    path.write_text("\n".join(filled) + "\n", encoding="utf-8")
    return relative_path


def convert_findings(verdict_findings, *, context_manifest):
    """判定findingsをfinding_set形式へ決定的に変換する（作業票§4の変換表）。"""

    bundle = {
        item["relative_path"]: item["sha256"]
        for item in context_manifest["material_bundle"]
    }
    findings = []
    for index, item in enumerate(verdict_findings, start=1):
        severity = item.get("severity", "info")
        if item.get("blocking"):
            severity = "error"
        relative_path = str(item.get("evidence_path", ""))
        location = str(item.get("evidence_location", ""))
        description = str(item.get("claim", ""))
        if location:
            description = "%s（%s）" % (description, location)
        findings.append(
            {
                "finding_id": "F-LLM-%03d" % index,
                "severity": severity,
                "target_ref": {
                    "relative_path": relative_path,
                    "sha256": bundle.get(relative_path, UNRESOLVED),
                },
                "requirement_ref": RULE_ID,
                "rule_id": RULE_ID,
                "description": description,
            }
        )
    return seal(
        {
            "record_kind": "finding_set",
            "record_id": "FS-%s" % context_manifest["record_id"],
            "record_version": 1,
            "reviewer": REVIEWER_NAME,
            "calls_llm": True,
            "context_ref": record_ref(context_manifest),
            "permit_ref": {"kind": "external_launch"},
            "findings": findings,
        }
    )


def launch_and_convert(
    *,
    request_relative_path,
    expected_sha256,
    context_manifest,
    launcher,
):
    """launcher（実起動または試験fake）を1回呼び、判定findingsを変換して返す。

    実起動launcherの結線は順序4（実験計画の承認）で行う。本moduleは起動方式を
    固定しない（injectable）。
    """

    verdict = launcher(
        request_relative_path=request_relative_path,
        expected_sha256=expected_sha256,
    )
    return convert_findings(
        verdict.get("findings", ()), context_manifest=context_manifest
    )
