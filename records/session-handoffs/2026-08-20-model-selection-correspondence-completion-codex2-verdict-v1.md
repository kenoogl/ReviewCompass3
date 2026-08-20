# Reviewer起動アダプタ 判定record（機械転記） contract-016-e2e-codex-terra-3

- Reviewer：provider `openai`／model `gpt-5.6-terra`（アダプタ照合済み）
- 独立性：Tier 1（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `codex-cli`）
- 依頼record：`records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-request-v1.md`（SHA-256 `41e51d20e7c01bbb701748a22af022af1e410a85c51ed88fa80b12a33e4544fc`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `5a3244e6f3339d8ff4b2c9f2459521b858aa8d6be5b2a7134829d5657bcfd900`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`contract-016-e2e-codex-terra-3`
- 判定：**rejected**
- 判定要旨：依頼recordのSHA-256は一致した。実装には正準抽出の開始境界欠落というblocking不適合があり、手順書にも契約016と矛盾する旧記載が残るため、受入を止めるべきと判断する。
- 鮮度（Reviewer申告）：match（expected `41e51d20e7c01bbb701748a22af022af1e410a85c51ed88fa80b12a33e4544fc`／observed `41e51d20e7c01bbb701748a22af022af1e410a85c51ed88fa80b12a33e4544fc`）
- 未検査：sandboxの書込み禁止に従い、pytest、request-builder check、git履歴からのRED再生を独立実行していない。、GREEN測定ブロックおよびfull-test receiptの記録内容は読取確認したが、記録された終了コード・2668件合格をこの環境で再現していない。

## findings

- F-016-001（severity: high／blocking: true）：正準依頼先行の抽出が「先頭見出し行の直後から」という契約016 v2 §7.2の開始境界を実装していません。先頭見出しより前に置かれたfence外の偽「- 依頼先：」行を正準行として採用でき、後続の正しい行を無視します。これは正準位置限定・騙され耐性・fail-closedの要件に反します。（根拠：`tools/reviewer_launch/core.py` 374-403）
- F-016-002（severity: medium／blocking: true）：手順書のcodex-cli節に「gpt-5.6-terraは許可済みだが起動選択機構は範囲外」とする旧記載が残り、同一file後段の契約016説明（--modelで選択可能）と矛盾しています。契約016 §5.1-7・§9-5の導線手順書更新として一貫しておらず、利用者に誤った運用を案内します。（根拠：`docs/development/prompts/reviewer-launch-run.md` 84-86,95-110）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": true,
      "claim": "正準依頼先行の抽出が「先頭見出し行の直後から」という契約016 v2 §7.2の開始境界を実装していません。先頭見出しより前に置かれたfence外の偽「- 依頼先：」行を正準行として採用でき、後続の正しい行を無視します。これは正準位置限定・騙され耐性・fail-closedの要件に反します。",
      "evidence_location": "374-403",
      "evidence_path": "tools/reviewer_launch/core.py",
      "identifier": "F-016-001",
      "severity": "high"
    },
    {
      "blocking": true,
      "claim": "手順書のcodex-cli節に「gpt-5.6-terraは許可済みだが起動選択機構は範囲外」とする旧記載が残り、同一file後段の契約016説明（--modelで選択可能）と矛盾しています。契約016 §5.1-7・§9-5の導線手順書更新として一貫しておらず、利用者に誤った運用を案内します。",
      "evidence_location": "84-86,95-110",
      "evidence_path": "docs/development/prompts/reviewer-launch-run.md",
      "identifier": "F-016-002",
      "severity": "medium"
    }
  ],
  "freshness": {
    "expected": "41e51d20e7c01bbb701748a22af022af1e410a85c51ed88fa80b12a33e4544fc",
    "observed": "41e51d20e7c01bbb701748a22af022af1e410a85c51ed88fa80b12a33e4544fc",
    "result": "match"
  },
  "reviewer": {
    "model": "gpt-5.6-terra",
    "provider": "openai"
  },
  "summary": "依頼recordのSHA-256は一致した。実装には正準抽出の開始境界欠落というblocking不適合があり、手順書にも契約016と矛盾する旧記載が残るため、受入を止めるべきと判断する。",
  "target": {
    "commit": "2a4116781c35a46ad49e360474c648e98f1006e1",
    "path": "records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-request-v1.md"
  },
  "unexamined": [
    "sandboxの書込み禁止に従い、pytest、request-builder check、git履歴からのRED再生を独立実行していない。",
    "GREEN測定ブロックおよびfull-test receiptの記録内容は読取確認したが、記録された終了コード・2668件合格をこの環境で再現していない。"
  ],
  "verdict": "rejected"
}
```
