"""テスト共通の合成fixture生成（deferred #7 テストfixture重複の共通化）。

範囲固定：records/session-handoffs/2026-08-09-claude-pilot-test-fixture-dedup-scope-v1.md

テストとして収集されない名前のhelper module。ここへ集約したfixture内容は、
各test fileの従来定義と出力が同一であることを置換時にhash照合した。
内容を変える場合は利用元テストの意味への影響をレビュー対象とする。
"""

import json


PROJECT_MANIFEST_V2_ARTIFACT_ROOTS = {
    "contracts": "artifacts/contracts",
    "design_decisions": "artifacts/design-decisions",
    "policies": "artifacts/policies",
    "requirement_maps": "artifacts/requirement-maps",
    "reuse": "artifacts/reuse",
    "verified_artifacts": "artifacts/verified",
    "workflow": "artifacts/workflow",
}

WORK4A_ARTIFACT_ROOTS = {
    "contracts": ".reviewcompass/contracts",
    "design_decisions": ".reviewcompass/design-decisions",
    "policies": ".reviewcompass/policies",
    "reuse": ".reviewcompass/reuse",
}


def project_manifest_v2(project_id):
    """Work 7A系テストが使うProject Manifest v2（7 artifact roots）。"""

    return {
        "schema_version": 2,
        "project_id": project_id,
        "artifact_roots": dict(PROJECT_MANIFEST_V2_ARTIFACT_ROOTS),
        "document_links": [],
    }


def write_project_manifest_v2(project_root, project_id):
    """project直下の.reviewcompassへProject Manifest v2を書く（末尾改行なし）。"""

    manifest_dir = project_root / ".reviewcompass"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "project-manifest.json").write_text(
        json.dumps(
            project_manifest_v2(project_id),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def work4a_manifest(project_id):
    """Work 4A系テストが使うProject Manifest（4 artifact roots）。"""

    return {
        "artifact_roots": dict(WORK4A_ARTIFACT_ROOTS),
        "document_links": [],
        "project_id": project_id,
        "schema_version": 2,
    }


def write_jsonl(path, records):
    """recordsを1行1JSONで書き、そのbytesを返す。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = b"".join(
        (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
        for record in records
    )
    path.write_bytes(encoded)
    return encoded


def claude_conversation_records(user_content, assistant_text):
    """user＋assistantの2 recordから成る合成Claude会話。"""

    return (
        {
            "uuid": "user-1",
            "type": "user",
            "sessionId": "session-1",
            "message": {
                "role": "user",
                "content": user_content,
            },
        },
        {
            "uuid": "assistant-1",
            "type": "assistant",
            "sessionId": "session-1",
            "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": assistant_text}],
            },
        },
    )
