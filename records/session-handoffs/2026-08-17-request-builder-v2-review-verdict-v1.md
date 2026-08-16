# Reviewer起動アダプタ 判定record（機械転記） cr-011-001

- Reviewer：provider `google`／model `gemini-3.1-pro-high`（アダプタ照合済み）
- 独立性：Tier 1（アダプタ判定。契約010 §5.1-4）
- 起動方式：headless機械起動（backend `antigravity-cli`）
- 依頼record：`records/session-handoffs/2026-08-17-request-builder-v2-review-request-v1.md`（SHA-256 `04b404d209c7fa45506869884e3eed5ebdf8683b9d02888d4fc140a1200c4816`）
- 未加工出力：保存先種別 `private_root_immutable_store`、SHA-256 `d7f240b00528dfb3aa75366977e8e7888b39c980515cc64427069a34caf3cad8`、参照権限：repo外私有領域（利用者とClaude）
- 実行識別子：`cr-011-001`
- 判定：**verified_with_findings**
- 判定要旨：契約候補v2をレビューしました。機械層の一意性、縮小境界と流用の妥当性、受入条件の充足性について概ね妥当であると判断します。検査の抜け・騙され方に関して、機微検査の除外形式を装った鍵のすり抜け、placeholderマーカーの破損による迂回、およびdigest表が空の場合の挙動について、敵対試験（RED）で確認すべき3点の非ブロッキングな所見を抽出しました。
- 鮮度（Reviewer申告）：not_computable（expected `04b404d209c7fa45506869884e3eed5ebdf8683b9d02888d4fc140a1200c4816`／observed `not_computable`）。理由：この実行環境ではコマンド実行が制限されており、ファイルのSHA-256ダイジェストを機械的に計算できないため
- 未検査：（申告なし＝空配列）

## findings

- evasion-secret-matching-exclusion（severity: warning／blocking: false）：機微検査の除外3形式（40/64桁hex・可読連結名）と同一の形式を持つ実在の鍵や機密情報が、高乱雑性検知をすり抜ける可能性がある。受入条件の敵対試験（RED）に、除外形式に合致してしまうダミー鍵のすり抜け確認（または許容の明示）を追加することを提案する。（根拠：`records/task-contract/2026-08-17-request-builder-candidate-v2.md` §7.3）
- evasion-placeholder-modification（severity: warning／blocking: false）：placeholder検査が `<<記入:` の完全一致残存のみを検知条件とする場合、LLMが `<記入:` のように一部だけ書き換えたり、マーカーだけを消して実内容を埋めない場合に検査をすり抜ける。敵対試験においてマーカー破損時の検知を確認することが望ましい。（根拠：`records/task-contract/2026-08-17-request-builder-candidate-v2.md` §7.1）
- evasion-empty-digest-table（severity: warning／blocking: false）：digest表検査において、表自体が空（0件）の場合の合格/不合格の挙動が暗黙的である。対象ファイルが1件も存在しない依頼recordを不正とする場合、空表の拒否を明示的に試験に追加することを提案する。（根拠：`records/task-contract/2026-08-17-request-builder-candidate-v2.md` §5.1-3-3）

## 判定JSON（verbatim）

```json
{
  "findings": [
    {
      "blocking": false,
      "claim": "機微検査の除外3形式（40/64桁hex・可読連結名）と同一の形式を持つ実在の鍵や機密情報が、高乱雑性検知をすり抜ける可能性がある。受入条件の敵対試験（RED）に、除外形式に合致してしまうダミー鍵のすり抜け確認（または許容の明示）を追加することを提案する。",
      "evidence_location": "§7.3",
      "evidence_path": "records/task-contract/2026-08-17-request-builder-candidate-v2.md",
      "identifier": "evasion-secret-matching-exclusion",
      "severity": "warning"
    },
    {
      "blocking": false,
      "claim": "placeholder検査が `<<記入:` の完全一致残存のみを検知条件とする場合、LLMが `<記入:` のように一部だけ書き換えたり、マーカーだけを消して実内容を埋めない場合に検査をすり抜ける。敵対試験においてマーカー破損時の検知を確認することが望ましい。",
      "evidence_location": "§7.1",
      "evidence_path": "records/task-contract/2026-08-17-request-builder-candidate-v2.md",
      "identifier": "evasion-placeholder-modification",
      "severity": "warning"
    },
    {
      "blocking": false,
      "claim": "digest表検査において、表自体が空（0件）の場合の合格/不合格の挙動が暗黙的である。対象ファイルが1件も存在しない依頼recordを不正とする場合、空表の拒否を明示的に試験に追加することを提案する。",
      "evidence_location": "§5.1-3-3",
      "evidence_path": "records/task-contract/2026-08-17-request-builder-candidate-v2.md",
      "identifier": "evasion-empty-digest-table",
      "severity": "warning"
    }
  ],
  "freshness": {
    "expected": "04b404d209c7fa45506869884e3eed5ebdf8683b9d02888d4fc140a1200c4816",
    "observed": "not_computable",
    "reason": "この実行環境ではコマンド実行が制限されており、ファイルのSHA-256ダイジェストを機械的に計算できないため",
    "result": "not_computable"
  },
  "reviewer": {
    "model": "Gemini 3.1 Pro (High)",
    "provider": "google"
  },
  "summary": "契約候補v2をレビューしました。機械層の一意性、縮小境界と流用の妥当性、受入条件の充足性について概ね妥当であると判断します。検査の抜け・騙され方に関して、機微検査の除外形式を装った鍵のすり抜け、placeholderマーカーの破損による迂回、およびdigest表が空の場合の挙動について、敵対試験（RED）で確認すべき3点の非ブロッキングな所見を抽出しました。",
  "target": {
    "commit": "unknown",
    "path": "records/session-handoffs/2026-08-17-request-builder-v2-review-request-v1.md"
  },
  "unexamined": [],
  "verdict": "verified_with_findings"
}
```
