> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 契約候補（抜粋）：前置recordの正準列の定義

## 7. 中心的な取り決め

### 7.1 正準列の定義（論点1）

先頭から連続する**既知前置record**だけを読み飛ばし、最初の判定可能recordで従来判定
（Claude本文形式・Codex 2形式）を行う。既知前置の必須欄（実物基準・事前走査record §1）：

| 種別 | 必須欄 |
| --- | --- |
| `queue-operation` | `operation`∈{enqueue, dequeue}・`sessionId`（str非空）・`content`存在 |
| `mode` | `mode`（str）・`sessionId`（str非空） |
| `custom-title` | `customTitle`（str）・`sessionId`（str非空） |
| `started` | `agentId`（str非空）・`key`（str非空） |

- `type`が上記4種のrecordは、他の欄（`uuid`等）を持っていても本文形式と判定しない（前置経路で
  必須欄を検査する）。
- スキップ上限は**16 record**（実測の連続数3〜4個の4倍）。超過は非対応。
- 必須欄に合致しないrecord（偽装・未知種別）が現れた時点で打ち切り、その位置で従来判定に
  合致しなければ非対応（fail-closed）。
