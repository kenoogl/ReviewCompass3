"""無工具Claude疎通結果をCLI終了codeへ変換する薄い層。"""

from tools.development import claude_bootstrap


def _run(manifest_digest, approval_id):
    result = claude_bootstrap.run_approved_no_tool_bootstrap(
        manifest_digest,
        approval_id,
    )
    if result.get("result") == "succeeded":
        return result, 0
    if result.get("result") == "stopped":
        return result, 2
    return result, 1
