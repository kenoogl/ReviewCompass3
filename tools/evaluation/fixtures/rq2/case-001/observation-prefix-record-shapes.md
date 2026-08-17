> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 観測記録（抜粋）：前置recordの実物形の網羅調査

## 調査範囲

前置型recordで始まるsource file 81件の全数。各fileの先頭から連続する前置recordについて、
JSONの実キーを列挙した。

## 実際に存在した欄

| 種別 | 本調査での出現数 | 実際に存在した欄 |
| --- | --- | --- |
| `queue-operation`（`operation`＝`dequeue`） | 76 | `type`・`operation`・`sessionId`・`timestamp` |
| `custom-title` | 3 | `type`・`customTitle`・`sessionId` |
| `mode` | 2 | `type`・`mode`・`sessionId` |
| 合計 | 81 | |

- `operation`が`enqueue`のrecordは本調査の対象file群には現れなかった。別系統で採取した
  enqueue形は`content`欄を持つ。
- `uuid`等の付随欄を持つrecordが混在するが、上表は全件に共通して存在した欄のみを挙げている。
