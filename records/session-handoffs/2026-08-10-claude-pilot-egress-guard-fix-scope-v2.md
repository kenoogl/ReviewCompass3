# 範囲固定 v2：group E（外部送信・機微境界）blocking 7件の修正

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビューv2待ち → Humanのrisk確定・着手確認待ち
- 先行：scope v1（`2c970d9`）は範囲レビューv1（`928997f`、要修正・blocking 4件）により
  RED開始の根拠にできない。v1は変更せず保持し、本v2が有効な範囲固定となる。

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
  改竄拒否である。修正の誤りは情報漏えいまたは保全の破れとして現れ、守り役codeの
  修正であるため開発方針上も既定`high`。

## 3. 固定入力と上流authority

**SR-EG-SCOPE-001対応**：sliceごとに上流authorityを分けて固定する。

| role | path | SHA-256 |
| --- | --- | --- |
| 修正順序の裁定 | `records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md` | `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997` |
| 対象Finding（group E判定） | `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-e-v1.md` | `a4bc656cdfe73188b1def7bc107a98a1027daf289dc3b6ab254b9808d3c86a33` |
| 範囲レビューv1 | `records/session-handoffs/2026-08-10-codex-scope-review-egress-guard-fix-v1.md` | `bbb45c0222f14d98eafaf73514dd4ccf1fbff6d931bb8c08d39e8206c9b1e928` |
| **slice 1の上流**（F-E1〜F-E5） | `docs/design/2026-08-07-external-egress-gate-proposal-v4.md` | `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd` |
| **slice 2の上流**（F-E6・F-E7＝§5.3 Raw Archive：追記専用・prefix検査・atomic replace・lock・integrity ledger） | `docs/design/2026-08-03-session-transcript-eventual-preservation-design.md` | `b387b9cf913b11a0d39e13cbd5aa6222527fdb4f801e478f1110683c3dd8d1fe` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `ce66c9f374319105f3c86558d910054151b79d1671a6352b80a9b661c827b137` |

- base commit：`928997f`、開始時worktree：clean
- 出口設計v4はslice 1のみのauthorityであり、slice 2へは及ばない（v1の誤りを訂正）。

## 4. 対象Findingと修正方針（Pilot提案）

いずれも各sliceの上流が既に要求している事項への**適合**であり、新しい設計・新しい送信段階・
新しいpayload種別・新しい保存schemaは導入しない。

### slice 1（出口設計v4適合）

| # | 対象 | 修正方針 |
| --- | --- | --- |
| F-E1 | `approval.py`・`gate.py`・`sender.py` | 承認をHuman作成のrecord fileへ束縛（path＋SHA-256の実在一致、厳密形schema、`consumed`は存在と型の厳密検査、有効期限はcaller提供`now`ではなく実時刻で判定）。gateとstage-one runnerは検証済み承認のみを受け取る |
| F-E2 | `payload.py`・`gate.py` | code断片の由来検証を現在sourceからの再切出し結果との一致へ変更。gateは送信JSONの入れ子schemaと`EgressPayload` fieldを相互照合し、許可field名の値の型まで固定 |
| F-E3 | `approval.py`・`gate.py` | 秘密値走査に資格情報3形式を追加し、Digest由来数字列の誤検出を除外（§9でHuman承認、**RED-1開始前に確定**） |
| F-E4 | `prefilter.py` | 閾値・重みの有限性・範囲・大小関係を検証し、非有限値・範囲外はfail-closedで拒否（固定値自体は不変） |
| F-E5 | `gate.py`・`sender.py` | 段階1ではcaller注入callbackを**実行前に**拒否する（許可実装の同一性検査、または段階1では呼び出さない構成） |

### slice 2（Raw Archive §5.3適合）

| # | 対象 | 修正方針 |
| --- | --- | --- |
| F-E6 | `preservation.py` | 既存backupを台帳へ照合してから台帳を更新する順序へ変更し、不一致は改竄として拒否 |
| F-E7 | `preservation.py` | raw・backup両rootについて解決後pathと全祖先componentのsymlink・root内束縛を検査（読取り側・書込み側の両方） |

## 5. 受入条件

**SR-EG-SCOPE-003対応**：拒否だけでなく「拒否のしかた」と正例の両方向を機械判定する。

1. **危険側（反証11件の不成立）**：group E判定recordの反証と同じ入力に対し、
   各経路が拒否すること。
2. **副作用の不在**：拒否時に**外部から観測可能な副作用が一切残らない**こと
   （S1系の反証では、callbackが作る痕跡fileが存在しないことをTestで固定する。
   拒否前実行の合格を防ぐ）。
3. **正例（偽陽性の不在）**：Digest（64桁hex）由来の数字列を含む正常payloadが
   個人識別子誤検出で拒否されないこと、および既存の正常送信経路が引き続き通ること。
4. 既存testが壊れない：対象既存test **69 passed**（§7の6 file合計。measured 2026-08-10）
   と公式全Test 1381 passed・status `passed`。
5. 実際の外部送信は行わない。段階1の「送信不可」性質は維持される。
6. 上流設計・config・schemaは変更しない。

## 6. slice分割とcommit境界

**SR-EG-SCOPE-004対応**：各commitのpathを一意に固定する。ワイルドカードは用いない。

| # | commit | 変更file（これ以外を含めない） |
| --- | --- | --- |
| 1 | **SCOPE v2**（本commit） | 本文書のみ |
| 2 | **RED-1** | `tests/test_egress_approval.py`・`tests/test_egress_gate.py`・`tests/test_egress_payload.py`・`tests/test_egress_prefilter.py`・`tests/test_egress_adversarial.py` |
| 3 | **GREEN-1** | `tools/egress/approval.py`・`gate.py`・`payload.py`・`prefilter.py`・`sender.py`、Evidence（新規、§7）、receipt（新規、§7） |
| 4 | **RED-2** | `tests/test_session_log_preservation.py` |
| 5 | **GREEN-2** | `tools/session_logs/preservation.py`、Evidence（**同一fileへslice 2節を追記**）、receipt（**新規file、§7の2件目**） |
| 6 | **review request** | 依頼書のみ（ignore検査exit `1`確認のうえ） |

- REDは各sliceとも「実装前に新規testだけが反証どおり失敗、既存testは合格、exit `1`」を
  Evidenceへ記録する。RED以後のtest変更にはHuman承認と理由の記録を要する。
- GREEN-1完了時点でslice 1のみで公式全Testを実行し、GREEN-2で再実行する（receipt 2件）。
- `tests/test_egress_dry_run.py`は変更しないが、回帰確認の実行対象には含める。

## 7. 変更可能path（一意列挙）

実装：`tools/egress/approval.py`、`tools/egress/gate.py`、`tools/egress/payload.py`、
`tools/egress/prefilter.py`、`tools/egress/sender.py`、`tools/session_logs/preservation.py`

Test：`tests/test_egress_approval.py`、`tests/test_egress_gate.py`、
`tests/test_egress_payload.py`、`tests/test_egress_prefilter.py`、
`tests/test_egress_adversarial.py`、`tests/test_session_log_preservation.py`

記録（新規）：
- `records/development/2026-08-10-egress-guard-fix-evidence-v1.md`（slice 1で作成、slice 2で追記）
- `records/development/2026-08-10-egress-guard-fix-slice1-test-receipt-v1.json`
- `records/development/2026-08-10-egress-guard-fix-slice2-test-receipt-v1.json`
- `records/session-handoffs/2026-08-10-claude-pilot-egress-guard-fix-review-request-v1.md`

これ以外のfile（config・schema・上流設計・他tool・TODO・checklist）は変更しない。

## 8. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §7以外のpath変更が必要になった場合。
3. **§9の承認を得ないままRED-1へ着手すること**（F-E3の方針をtestへ固定できないため）。
4. 修正が各sliceの上流と矛盾する場合（設計変更が必要と判明した時点で停止しHumanへ）。

## 9. Humanへの確認事項（RED-1開始前に必要）

**SR-EG-SCOPE-002対応**：F-E3の承認はGREEN前ではなく**RED-1開始前**に置く。

1. risk `high`の確定と着手承認。
2. F-E3で追加する資格情報形式（**AWS access key形式／GitHub token形式／PEM秘密鍵header**）の承認。
3. F-E3の誤検出除外規則（**64桁hex文字列に含まれる数字列を個人識別子判定の対象外とする**）の承認。

2・3が未承認の間はRED-1に着手しない（§8-3）。
