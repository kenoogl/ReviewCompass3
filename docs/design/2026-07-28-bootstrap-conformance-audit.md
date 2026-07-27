---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
---

# ブートストラップ実装の適合性監査

監査対象commit：
`a26630ac614809d2bcf43ff3b4fc2eb4d7a12452`

構造化正本：
`records/design/bootstrap-conformance-audit.json`

## 結果

| 分類 | 件数 | 意味 |
|---|---:|---|
| conformant | 5 | 実装・テスト両証拠がありgapなし |
| adapt | 23 | 類似責務はあるが正式設計の関門が不足 |
| replace | 4 | 既存責務境界が設計と異なり置換が必要 |
| defer | 5 | 初期bootstrap範囲外で後段実装 |

全37要件を一意に分類し、未分類・重複は0件である。

## そのまま昇格可能な責務

- `REQ-CONTEXT-002`：本文とDigestを持つ材料束
- `REQ-EXEC-004`：複数担当と結果の結線
- `REQ-SESSION-002`：rawから伏字化転写・要約・来歴への変換
- `REQ-SESSION-003`：追記・改変・消失・転写変異の検出
- `REQ-PORTABLE-003`：所有境界付き配置ライフサイクル

## 修正が必要な主な境界

- Contextは7入力、影響閉包Scope、Composition、完全identityを統合する。
- HarnessはWorkflow許可、承認者identity、write-ahead captureを追加する。
- TriageはTrace verdictと対象Digest付きHuman判断を追加する。
- Traceはruntime意味グラフ、影響閉包、Operational Provenanceを追加する。
- Session取込は利用者承認identityと共有保存境界へ接続する。
- Portableはsupported-platform matrixと共有機微情報vaultを追加する。

## 置換対象

既存のstage gateはセッションログまたは段監査の関門であり、
active workとRun開始・完了を扱う正式Workflow状態機械ではない。
`REQ-WORKFLOW-001`〜`004`は既存境界へ継ぎ足さず置換する。

## 後段対象

Evidence Evaluation 3要件とSelf Improvement 2要件は、初期bootstrapの
正式実装対象外である。設計と受け入れ試験は確定するが、未実装を
conformantとして扱わない。
