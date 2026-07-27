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

固定commitの実体Digest、要件別Evidence role、固定時点テスト結果、
要件別gap、依存gapおよび設計対応は
`records/design/bootstrap-conformance-integrity.json`に固定する。

## 結果

| 分類 | 件数 | 意味 |
|---|---:|---|
| conformant | 0 | 全義務を固定commitの証拠で証明できる要件なし |
| adapt | 28 | 類似責務はあるが正式設計の義務、関門または依存境界が不足 |
| replace | 4 | 既存責務境界が設計と異なり置換が必要 |
| defer | 5 | 初期bootstrap範囲外で後段実装 |

全37要件を一意に分類し、未分類・重複は0件である。

## そのまま昇格可能な責務

現時点では0件である。既存実装は捨てず、Evidenceとgapを保持して正式実装で
適応する。

`REQ-CONTEXT-002`はprior identityと宣言Digestの反証試験、
`REQ-EXEC-004`はround・Target・topology identity、
`REQ-PORTABLE-003`は途中cleanup失敗時の逆順補償が不足するため、
いずれもconformantからadaptへ戻した。

`REQ-SESSION-003`も、消失と非追記変更の別分類および変更前後identity・
変異診断の耐久保存を全義務で反証できないためadaptへ戻した。

## 修正が必要な主な境界

- Contextは7入力、影響閉包Scope、Composition、完全identityを統合する。
- HarnessはWorkflow許可、承認者identity、write-ahead captureを追加する。
- TriageはTrace verdictと対象Digest付きHuman判断を追加する。
- Traceはruntime意味グラフ、影響閉包、Operational Provenanceを追加する。
- Session取込は利用者承認identityと共有保存境界へ接続する。
- Portableはsupported-platform matrixと共有機微情報vaultを追加する。

`REQ-SESSION-002`の変換処理自体は実装・試験済みだが、依存する
`REQ-PORTABLE-004`の共有隔離保存境界が未適合である。このため単独の
conformantとはせず、依存gapを明示したadaptとして扱う。

## 証拠の固定方法

61件の実装・テストEvidenceは、パスだけでなく監査対象commitから読み出した
blob内容のSHA-256へ結び付けた。監査対象commitのarchiveに対する全試験は
361件通過した。全37件の非適合要件は、承認済み464原子的義務IDから
該当statement・受け入れ条件を参照し、正しい対象component、受け入れ試験、
停止条件および直接依存gapへ結び付けた。validatorは監査対象commitから
各blobを直接読み出し、宣言SHA-256と照合する。

## 置換対象

既存のstage gateはセッションログまたは段監査の関門であり、
active workとRun開始・完了を扱う正式Workflow状態機械ではない。
`REQ-WORKFLOW-001`〜`004`は既存境界へ継ぎ足さず置換する。

## 後段対象

Evidence Evaluation 3要件とSelf Improvement 2要件は、初期bootstrapの
正式実装対象外である。設計と受け入れ試験は確定するが、未実装を
conformantとして扱わない。
