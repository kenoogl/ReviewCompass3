# 機械操作routing v2 最小縦切り 承認Decision v1

- decision ID：`DEC-MACHINE-OPERATION-ROUTING-001`
- decision maker：Human
- decided at：2026-08-05
- 対象Issue：`ISSUE-HTC-C9F6C917`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-machine-operation-routing-v2-slice.md`

## 1. Humanが承認したこと

Humanは次の3点をすべて承認した。

1. **最小縦切りの内容**：versioned operation inventory、permission preflight、execution receiptの3部。
2. **runnerの分離**：project内のrunnerを、既存のpolicy runnerから分離した別moduleとする。
3. **権限の責任分担**：project内は必要な権限種別を計算して出すだけとし、**承認と取得済みの確認は
   host側に置く**。

承認対象は、v2提案`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`の
**§3だけ**である。

## 2. 承認対象と実Digest

| 種別 | path | SHA-256 |
| --- | --- | --- |
| v2提案（承認は§3のみ） | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md` | `7c812b68b4b4b0cd282af29b44ff117e78aa172b6f2b830f6d684856f9bf7a31` |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |
| 主triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-c9f6c917--v1.json` | `5b698bd0e9069128710bef161e3d60475002c89c4a4b70cce015a39c31bbf444` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-477ea1a4--v1.json` | `9e4d76f2e791deaa8c8bfd5fbb97e2ff01aff4449828a01d439e29cac3498d78` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-186e9b83--v1.json` | `94c102c1313f21e799df8e4bca992663238b605c561c75869a55a3024d0aff62` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-9dce8503--v1.json` | `8088e41b42a2e59b78bcb5717c9328c6e0a0eb0f50914efb518097c65844c606` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-a5d1bcca--v1.json` | `5f8c771d6bf70b834e759b4c960debee7279906f2673090d16534e75f218628f` |
| 意味単位commit Decision | `records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md` | `07eb9cbcd1e4e1b33aff787f597a45db1be6913a0685d76f8db1169adf965d23` |

## 3. runnerの位置づけとhost境界

- 実装moduleは`tools/development/operation_routing.py`であり、**既存のpolicy runnerとは別module**である。
  policy runnerへのimport依存を持たない。既存のpolicy runner、Git helper、TODO helper、
  Task Contract resolverは変更しない。
- このmoduleはshellも外部processも起動しない。commandを実行するのはcallerのcallbackであり、
  moduleはその呼出しの可否と記録だけを扱う。
- **権限を承認・確認するのはhost側である。** project内は、inventoryの分類から必要な権限種別を
  計算して出すだけである。moduleが受け取る`host attestation`はcallerの申告であり、
  project内がOS、sandbox、hostの権限を検査・付与・迂回したことにはならない。
- 必要な権限が未取得なら、書込みを一度も試さず停止し、必要権限を一回の集合で返す。
  失敗してから権限を切り替える経路は持たない。

## 4. §3以外は承認していない

次はこの決定に含まれない。着手しない。

- shellを実行する汎用argv executor、`shell=True`相当、既存の直接shell操作の置換
- cache rootの固定
- Gitへの実書込み、push、tag、外部送信、host／sandbox権限の取得・迂回・自動承認
- Codex hostのJavaScript tool構文、外部toolのAPI schemaへの対応
- `ISSUE-HTC-66C3E6CA`が扱うEvidence／TODOの定型欄生成
- V4 Issue recordのstate変更、正式製品schema／UI／automation、Task Contractの新規作成

`ISSUE-HTC-C9F6C917`はV4の限定scope内で正式なimplementation lifecycleをまだ持たないため、
Issue recordは`registered`のままとする。今回の実装許可はこのHuman Decisionにだけ記録する。
v2提案は正式なIssue Resolution PlanまたはTask Contractへ昇格していない。

## 5. 実装物

| 種別 | path | SHA-256 |
| --- | --- | --- |
| module | `tools/development/operation_routing.py` | `f735299433b49b868b713dfcc4ed1973c7d4771f906242e3e3932e39bf269049` |
| 受入test | `tests/test_operation_routing_v2.py` | `6da141f20f7b8a31e270c6a2dc2195cbce20c908633d81e0e939e51b703d6fc4` |

GREEN Evidenceは
`records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md`である。
