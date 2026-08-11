# Pilot collaboration run

実装指示の正本は
`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md`
である。LLMと機械処理の分担、`prompt_payload_bytes`、外部送信、Human承認を含む規則は正本を参照し、
この入口には複製しない。

共通コマンドの場所は次のとおり。

- `reviewcompass3-pilot prepare`
- `reviewcompass3-pilot ingest`
- `reviewcompass3-pilot status`

固定二payloadによる無工具Claude疎通は、用途を限定した
`docs/development/prompts/claude-bootstrap-run.md`を入口とする。
