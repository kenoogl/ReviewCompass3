# 範囲固定：守り役後追いレビューの対象一覧（deferred #6・第1単位）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：Humanのrisk確定・着手確認待ち

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: deferred #6 守り役後追いレビュー・第1単位（対象一覧の作成）
           （裁定record：records/development/2026-08-09-deferred-items-triage-decision-v1.md）
```

受け渡しは`docs/development/pilot-driven-record-handoff.md`による。

## 2. risk提案

- 提案：`low`
- 根拠：本単位の成果物は**調査記録（一覧record）1件だけ**で、product code・test・
  workflow台帳・既存recordへ一切触れない。誤りの影響は「一覧の不正確さ」に限られ、
  それはReviewerの完了レビュー（一覧の網羅・根拠の照合）と、後続の個別レビュー実施時に
  検出される。§3の`low`規定により、Humanのriskと着手の確認だけで実装可能。

## 3. 作業の位置づけ

`work-review-protocol.md` §3は「守り役のcode（validator・Digest照合・承認関門・改竄拒否
など、他の成果物の合否を決めるcode）」を既定`high`とする。この基準と「Pilot fixtureに
無い反証の機械実行」を含む現行レビュー体制が確立する**前**に入った守り役codeは、
現基準相当の独立レビューを受けていない。#6はその後追いであり、第1単位はまず
**何が対象で、何が済んでいるか**を機械的に固定する。

## 4. 開始状態

- branch：`main`
- base commit：`3c4738b`（#1 Closer projection）
- 開始時worktree：clean

## 5. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 共通レビュー基準（§3守り役定義・§11比例原則） | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| mode手順書 | `docs/development/role-neutral-pilot-review-collaboration.md` | `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e` |
| 受け渡し方式 | `docs/development/pilot-driven-record-handoff.md` | `93c84dd6ddd86af12175a4e844334ec9d62633f9be5ba9e97bcfbe3a435e92f0` |
| deferred仕分け裁定（#6着手承認） | `records/development/2026-08-09-deferred-items-triage-decision-v1.md` | `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `f72273ca9761d97df069851e5135a1b8bc3d5d780f7a2f34f26ae75183118a0a` |

調査対象は`tools/`配下の現行moduleと`records/development/`のレビューEvidence群
（読み取りのみ。内容は一覧recordへ要約として写し、原本は変更しない）。

## 6. 今回の作業（第1単位＝一覧のみ）

新規record `records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md`
を作成する。

1. `tools/`配下の全moduleを機械的に列挙し、§3定義に照らして**守り役に該当するmodule**を
   判定する（該当・非該当と判定理由を1行ずつ）。
2. 守り役該当の各moduleについて、次を記録する：
   - path・役割（何の合否を決めるか）
   - **現基準相当の独立レビューの有無**（反証つき独立レビューのEvidence record・
     commitへの参照。無い場合は「後追い対象」）
   - 後追い対象の**優先度提案**（誤った合格の影響の大きさ・使用頻度に基づく
     Pilot提案。確定はHuman）
3. 一覧の網羅性の根拠（列挙に使ったcommandと件数）をrecordに記す。

**本単位で行わないこと**：個別moduleの後追いレビュー実施、code・test・既存recordの
変更、優先度の確定（Human裁定）、レビュー日程の計画。

## 7. 受入条件

1. `tools/`配下の全moduleが一覧に現れ、守り役該当・非該当の判定と理由を持つ
   （網羅性はReviewerが列挙commandの再実行で照合できる）。
2. 守り役該当の各行が、レビュー有無の根拠（Evidence参照または「無し」）を持ち、
   参照はpath＋SHA-256で照合可能である。
3. 後追い対象に優先度提案（高・中・低と理由）が付く。
4. 成果はrecord 1件のみで、他のfileに変更が無い。

## 8. 変更可能path

- `records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md`（新規）
- `records/session-handoffs/2026-08-10-claude-pilot-guard-backfill-inventory-review-request-v1.md`（新規、作成後）

## 9. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §8以外のpath変更が必要。
3. 守り役該当の判定に意味的裁定が必要な境界事例が出た場合は、一覧に「要Human判定」と
   記して先へ進む（停止はせず、判定保留として可視化する）。

## 10. commit境界

1. **SCOPE**（本commit）：本文書のみ。Humanのrisk確定・着手確認待ちで停止。
2. **INVENTORY**：一覧record 1件のみ。
3. **review request**：依頼書のみ（ignore検査exit `1`確認のうえ）。完了レビューは
   `low`規定どおり（対象の再実行照合。過小分類の検査を含む）。
