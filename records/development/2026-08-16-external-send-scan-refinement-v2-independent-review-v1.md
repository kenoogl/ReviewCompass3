# 機微検査精密化・改名 契約候補v2 独立確認 v1（Gemini・Human中継）

- Reviewer：Gemini 3.1 Pro (High)（利用者がディレクトリ共有のGeminiへ依頼recordのpathを伝達。
  判定文は利用者がchatへ貼り付け、Claudeが本recordへ転記した）
- 中継：Human中継（暫定体制`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`による）
- 実施日：2026-08-16
- 依頼record：`records/session-handoffs/2026-08-16-g20-scan-refinement-v2-review-gemini-request-v1.md`
- 対象契約候補：`records/task-contract/2026-08-16-external-send-scan-refinement-candidate-v2.md`
  - SHA-256：`58e5f9165e2201892377744377a9758f79be7559fe26f82ed114ec246968e6da`
- 判定：`開始可`

## 1. 判定の転記（要旨）

【記録】

- **鮮度検査：合格**。3 file（契約候補v2・自己レビュー・観測record）のSHA-256がrecord記載値と完全一致。
- **反証1 機械層の一意性：担保**。`find_high_entropy`は`allow_patterns`を引数に取り`re.fullmatch`で評価する
  設計であり、`_scan_order`のJSON走査で`path == ("order_identifier",)`のときだけ`allow_patterns`を渡さない
  分岐（出し分け）は「実装上極めて明瞭かつ一意に実現可能。実装者が後決めする余地や曖昧さは存在しない」。
- **反証2 X2の通り抜け耐性：優秀（敵対集合への追加は不要）**。断片20文字以下の要求により、JWT署名部
  （43文字）・Stripe鍵（24文字超の無区切り断片）・GitHub token（36文字断片）は確実に停止する。
  hexのみの連結（UUID形を含む）は`(?=.*[G-Zg-z_])`で弾かれる。「hex外文字を1字だけ混ぜた乱雑hexを
  20文字ずつに区切る」偽装はX2を通り得るが、操縦LLMの意図的な難読化行為が必要であり、偶発漏えいを防ぐ
  機械層の範囲を越える（意図的なら自然言語にも偽装できる）ため、敵対集合へ追加して正規表現を複雑化する
  必要はないと判断する。
- **反証3 残余riskの受容妥当性：妥当**。40／64桁hexはgit運用の必須データであり、これを止めると送信機能が
  実用に耐えない。主要な鍵は不変の既定5 patternで保護され、commit済み限定・台帳記録の多重緩和がある。
  実運用との均衡として非常に妥当な水準。
- **反証4 縮小境界と上位整合：問題なし**。改名は実体と名称を一致させる健全な整理で、保護の境界を
  広げない。契約008の保護基準は§6で継承され矛盾なし。「受入だけでは後続を完了にしない」ことも§12で固定。
- 結論：「安全境界を損なう退行はなく、実装を開始して問題ありません。」

## 2. Claudeによる機械照合

【実測】判定文が参照する根拠と実物の一致を確認した。

| 判定文の根拠 | 実物 | 一致 |
| --- | --- | --- |
| `find_high_entropy`が`allow_patterns`引数を持つ | `tools/session_logs/redaction.py` 204〜210行 | 一致 |
| `allow_patterns`は`re.fullmatch`で評価 | 同 216行（起草時実測でも確認済み） | 一致 |
| `_scan_order`がJSON走査でpathを持ち出し分け可能 | `tools/external_review/gemini_send.py` 260〜265行 | 一致 |
| 契約v2の§7.1／§7.2／§6／§8／§9／§12の構成 | 契約候補v2の節構成 | 一致 |

## 3. 未実施・次

- 契約採用・実装は未開始。次は利用者へ縮小境界の採用・契約v2採用・実装開始を一判断として求める
  （依頼record§6手順4）。
