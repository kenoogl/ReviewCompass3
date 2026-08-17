# セッションログ前置record解釈（契約014） 作業契約候補 v3

- 作成日：2026-08-17
- 起草者：Claude
- v3改定：利用者「修正案を承認。候補v3固定→RED追加→GREEN→再実測まで一気に進めて」
  （2026-08-17 chat）。改定理由＝遡及実測（v2 §7.5-2）が不合格となり、機械特定した原因が
  「`queue-operation`の`dequeue`操作recordは`content`キーを持たない実物形」だったため。
  §7.1の必須欄を操作別分岐へ修正する（全81 fileの網羅調査で、判定に落ちる前置型recordは
  この1形のみ・76件。`mode`・`custom-title`・`started`に変形なし）。
  v2＝`…-candidate-v2.md`（commit `ed20d6a`・本v3で置換）
- 採用：v1採用済み（採用判断record・残余risk4点受容）・§7.4改定はv2で承認済み・§7.1の
  本修正はv3冒頭の指示文言で承認済み
- 種別：Task Contract（契約014）。RED追加着手可
- 主題：v2に同じ（前置recordの正準列スキップ・補助分類の本文基準化・自然遡及）

## 1〜6・8・10（v2から変更なし）

`records/task-contract/2026-08-17-session-log-prefix-interpretation-candidate-v2.md`の
§1（位置と縮小境界）・§2（Human承認境界）・§3（権威、証拠）・§4（実装方法）・§5（範囲）・
§6（固定再利用部品と保護基準）・§8（変更上限）・§10（停止条件）を変更なしで引き継ぐ。

## 7. 中心的な取り決め（§7.1のみ改定・他はv2から変更なし）

### 7.1 正準列の定義（v3改定）

先頭から連続する**既知前置record**だけを読み飛ばし、最初の判定可能recordで従来判定
（Claude本文形式・Codex 2形式）を行う。既知前置の必須欄（実物基準・**遡及実測での実file網羅
調査を反映**）：

| 種別 | 必須欄 |
| --- | --- |
| `queue-operation`（`operation`＝`enqueue`） | `sessionId`（str非空）・`content`存在 |
| `queue-operation`（`operation`＝`dequeue`） | `sessionId`（str非空）。**`content`不要**（実物76件の形） |
| `mode` | `mode`（str）・`sessionId`（str非空） |
| `custom-title` | `customTitle`（str）・`sessionId`（str非空） |
| `started` | `agentId`（str非空）・`key`（str非空） |

- `operation`が`enqueue`・`dequeue`以外の`queue-operation`は非対応（打ち切り）。
- `type`が前置4種のrecordは、他の欄（`uuid`等）を持っていても本文形式と判定しない。
- スキップ上限は**16 record**。超過は非対応。
- 必須欄に合致しないrecord（偽装・未知種別）が現れた時点で打ち切り、その位置で従来判定に
  合致しなければ非対応（fail-closed）。

### 7.2〜7.6（v2から変更なし）

§7.2（判定の互換）・§7.3（issue計上＝前置の無issueスキップ）・§7.4（補助分類＝本文record
へ到達できるfileは補助でない）・§7.5（敵対fixtureと遡及の受入）・§7.6（残余risk4点・
受容済み）はv2を変更なしで引き継ぐ。§7.5-1の敵対fixtureに次を追加する：
(f) `content`なし`enqueue`（引き続き打ち切り＝enqueueの`content`必須は維持）。

## 9. 受入条件（v2から追記のみ）

v2 §9の6条件を引き継ぎ、条件1のRED対象へ「`dequeue`形（`content`なし）のスキップ」と
「(f) `content`なし`enqueue`の打ち切り」の試験を追加する。

## 11. 影響、未実施、次作業

- 影響：v2に同じ。本修正により実fileの前置列（`enqueue`→`dequeue`→本文）が正しくスキップ
  され、遡及（非対応→解釈済み）が成立する見込み。
- 未実施：RED追加、GREEN（`is_known_prefix_record`の操作別分岐）、再実測。
- 次作業：RED追加→GREEN→再実測（v3冒頭の指示文言により一括承認済み）。

## 12. 注記（2026-08-18追記・原文は無変更）

§7.1の正準列定義に書かれていない2つの場合について、実挙動を機械確認した（確認record＝
`records/development/2026-08-18-contract-014-canonical-sequence-gaps-observation-v1.md`・
全10 probe）。**いずれもfail-closedで安全側であり、実装変更は不要**。挙動は敵対試験2本で
固定した（`tests/test_session_log_prefix_interpretation.py`）。

1. **入力終端**：前置recordだけで入力の終端に達した場合（判定可能recordが存在しない場合）、
   判定は非対応（`None`）である。§7.4の「到達できないfile」の語が実質これを覆う。
2. **Codex 2形式との関係**：前置スキップ後の最初の判定可能recordは、Claude本文形式と
   Codex 2形式の**両方**で従来判定される（前置1件→Codex 2形式は`codex_exec_json`と判定）。
   前置record自体・必須欄不足の偽装前置がCodex 2形式として誤判定されることはない（打ち切り後の
   従来判定にも合致せず非対応）。

出所：RQ2 paired trialの独立レビュー（case-001条件D）が欠落を指摘した。改善候補
`IC-CONTRACT-014-CANONICAL-SEQUENCE-GAPS-001`・仕分けrecord
`records/development/2026-08-18-rq2-byproduct-candidates-triage-decision-v1.md`。
