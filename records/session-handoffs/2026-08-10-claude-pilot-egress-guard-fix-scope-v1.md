# 範囲固定：group E（外部送信・機微境界）blocking 7件の修正

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビュー待ち → Humanのrisk確定・着手確認待ち

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: 守り役後追い修正 第1単位（group E＝外部送信・機微境界の7 finding修正）
           （裁定record：records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md）
```

## 2. risk提案

- 提案：`high`（Human確定を要する）
- 根拠：対象は外部送信の承認関門・payload制限・秘密値走査・段階境界と、生ログ保全の
  改竄拒否である。修正の誤りは**情報漏えい**または**保全の破れ**として現れ、
  かつ守り役codeの修正であるため開発方針上も既定`high`。

## 3. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 修正順序の裁定 | `records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md` | `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997` |
| 対象Finding（group E判定） | `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-e-v1.md` | `a4bc656cdfe73188b1def7bc107a98a1027daf289dc3b6ab254b9808d3c86a33` |
| 上流設計（出口設計v4） | `docs/design/2026-08-07-external-egress-gate-proposal-v4.md` | `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `ce66c9f374319105f3c86558d910054151b79d1671a6352b80a9b661c827b137` |

- base commit：`4bb1c9b`、開始時worktree：clean

## 4. 対象Findingと修正方針（Pilot提案）

いずれも**出口設計v4が既に要求している事項への適合**であり、新しい設計・新しい送信段階・
新しいpayload種別は導入しない。

| # | 対象 | 修正方針 |
| --- | --- | --- |
| F-E1 | `approval.py`・`gate.py`・`sender.py` | 承認をHuman作成のrecord fileへ束縛する（path＋SHA-256の実在一致、schema厳密形、`consumed`は「Trueでない＝未消費」ではなく**存在と型の厳密検査**、有効期限は呼び出し側の`now`ではなく**単調に取得した実時刻**で判定）。gateとstage-one runnerは辞書ではなくこの検証済み承認だけを受け取る |
| F-E2 | `payload.py`・`gate.py` | code断片の由来検証を**現在sourceからの再切出し結果との一致**へ変更。gateは送信JSONの入れ子schemaと`EgressPayload`のfieldを相互照合し、許可field名の**値の型**まで固定する |
| F-E3 | `approval.py`・`gate.py` | 秘密値走査に資格情報3形式（AWS access key形式・GitHub token形式・PEM秘密鍵header）を追加し、Digest（64桁hex）由来の数字列を個人識別子と誤検出しないよう**除外規則**を入れる。※**追加する形式一覧と除外規則はHuman承認事項**（#5の7 key allowlistと同じ扱い） |
| F-E4 | `prefilter.py` | 閾値・重みの**有限性・範囲・大小関係**を検証し、非有限値・範囲外はfail-closedで拒否する（固定値そのものは変更しない） |
| F-E5 | `gate.py`・`sender.py` | 段階1では`redaction_hook`等のcaller注入callbackを**実行前に**拒否する（許可実装の同一性検査、または段階1では呼び出さない構成へ）。「段階1は外部副作用が型として不可能」を維持する |
| F-E6 | `preservation.py` | 既存backupを**台帳へ照合してから**台帳を更新する順序へ変更し、不一致は改竄として拒否する（改竄値の正当化を断つ） |
| F-E7 | `preservation.py` | raw・backupの両rootについて、**解決後path**と全祖先componentのsymlink・root内束縛を検査する（読取り側・書込み側の両方） |

## 5. slice分割とcommit境界

独立subsystemのため2 sliceに分ける。各sliceはTDD（RED＝反証testのみ → GREEN＝実装）。

1. **SCOPE**（本commit）：本文書のみ。`high`範囲レビューとHuman裁定待ちで停止。
2. **RED-1**：`tests/test_egress_*.py`への反証test追加のみ（F-E1〜F-E5）。実装前に
   反証どおり失敗し既存testは合格、exit `1`を確認。
3. **GREEN-1**：`tools/egress/`の実装＋Evidence＋公式receiptのみ。Testは変更しない。
4. **RED-2**：`tests/test_session_log_preservation.py`への反証test追加のみ（F-E6・F-E7）。
5. **GREEN-2**：`tools/session_logs/preservation.py`の実装＋Evidence更新＋receipt更新。
6. **review request**：依頼書のみ（ignore検査exit `1`確認のうえ）。

RED以後のtest変更にはHuman承認と理由の記録を要する（既定どおり）。

## 6. 受入条件

1. group E判定recordの反証11件が**すべて不成立**になる（同じ入力で拒否される）。
2. 既存の正例が壊れない（対象既存test 73件＋公式全Test 1381件が合格、status `passed`）。
3. 実際の外部送信は行わない。段階1の「送信不可」性質は維持される。
4. 上流設計v4・config・schemaは変更しない（適合修正のみ）。

## 7. 変更可能path

- `tools/egress/approval.py`・`gate.py`・`payload.py`・`prefilter.py`・`sender.py`
- `tools/session_logs/preservation.py`
- `tests/test_egress_approval.py`・`test_egress_gate.py`・`test_egress_payload.py`・
  `test_egress_prefilter.py`・`test_egress_adversarial.py`・`tests/test_session_log_preservation.py`
- Evidence record（新規）・公式receipt（新規）・review request（新規）

## 8. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §7以外のpath変更が必要になった場合（特にconfig・schema・上流設計）。
3. **F-E3の形式一覧・除外規則**がHuman承認を得られていない状態でのGREEN着手。
4. 修正が上流設計v4と矛盾する場合（設計変更が必要と判明した時点で停止しHumanへ）。

## 9. Humanへの確認事項

1. risk `high`の確定と着手承認。
2. F-E3で追加する資格情報形式（AWS access key形式・GitHub token形式・PEM秘密鍵header）と、
   64桁hex由来の数字列を個人識別子判定から除外する規則の承認。
