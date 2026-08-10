# Human裁定：本日の方針文書のうち設計正本と重複する3件を廃棄候補にする

- 裁定日：2026-08-10
- 裁定者：Human（kenoogl）
- 裁定文言（原文）：「3文書を廃棄候補として裁定recordに記し、規約Aと正本だけ生かす。」

## 1. 背景

`records/design/stage-five-design.json`（設計正本、SHA-256
`29ed55927061c9991ec7bbad3f03c929214527b653979d3453c9bbd7eb499c4f`）は、9つの設計判断の
それぞれに「機械の責務／LLMの責務／Humanの責務／失敗戦略」を4分割で持つ。本日Pilotが
作った方針文書の多くは、この正本の再発明であった。

## 2. 廃棄候補（今後の判断根拠にしない）

| # | 文書 | SHA-256 | 重複する正本 |
| --- | --- | --- | --- |
| 1 | `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`（規約A/B/C） | `bb24ab9d046dd103462f192236b2ea057f5a77f32cd1f4e04be49518d5160174` | 規約B・Cは`DES-EVIDENCE-EVALUATION`（限界を別フィールドで保持・未確定停止）の再発明 |
| 2 | `records/development/2026-08-10-review-method-consolidation-v1.md`（型1〜4） | `93d2dbb26d9c5742c2f7c1ae0dcec4d4448c1c4dddef41a40b5ee89960be6a15` | `DES-REVIEW-TRIAGE`・`DES-HARNESSED-EXECUTION`の役割4分割の劣化版 |
| 3 | `records/development/2026-08-10-trusted-core-policy-proposal-v1.md`（骨太3方針） | `f48168652d22430d80c289420e9aac4362ffc3807c386b2274fd79f863cd7947` | 方針2は共通原則の再発明。方針1・3は依存測定バグで根拠が崩れた |

「廃棄」の意味：**これらを今後の判断・レビュー・規約の根拠にしない**。過去commitとしては
残る（履歴は書き換えない）。付随する完了レビューrecord（原因分析v1/v2・規約C有効性・
レビュー方法・骨太方針の各判定record）も同じく判断根拠から外す。

## 3. 生かすもの

| 対象 | 生かす理由 |
| --- | --- |
| 設計正本 `records/design/stage-five-design.json` | 役割4分割・失敗戦略の正本。今後の判断はこれに従う |
| 規約A（巻き添え防止5手順）**のみ** | 対象fileの現在Digestで全文検索し固定record・testを洗い出す手順。正本に無く、2026-08-10にCodexが実効を機械実証（違反commit `f8c01b5`の範囲外1件を検出）した唯一の新規手順 |

規約Aは廃棄文書#1の一部だが、#1を廃棄候補とすることと矛盾しない。**規約Aだけを
別の正式な場所へ移すか否かは別裁定**とし、当面は本record §3で「生かす対象」として指す。

## 4. 本裁定が決めていないこと

- 廃棄候補3件のfile自体の削除（現時点では削除しない。参照を断つだけ）。
- 規約Aを設計正本または連携文書へ統合するか。
- codex CLI方式でAPIレビュープロトコル（閉鎖payload）の方針が実現できるか
  （§別途、Pilotが分析中）。
