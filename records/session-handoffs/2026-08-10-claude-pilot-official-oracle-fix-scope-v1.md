# 範囲固定：group B（公式検証oracle）blocking 5件の修正

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビュー待ち（risk確定・着手・RED開始は包括承認済み）

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: 守り役後追い修正 第3単位（group B＝公式検証oracleのF-B1〜F-B5修正）
```

## 2. riskとHuman承認

- risk：`high`（包括承認により確定）
- Human承認（2026-08-10）：「組BからDまで自律的に実行。停止条件に触れたときと、
  修正の承認が要るときだけ止めよ」
  （承認record：`records/development/2026-08-10-guard-backfill-autonomous-authorization-v1.md`）
- 根拠：対象は公式Testの合否を決めるoracleと完了関門であり、誤りは
  **全成果物の誤った合格**として現れる。

## 3. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 包括承認 | `records/development/2026-08-10-guard-backfill-autonomous-authorization-v1.md` | `3c0a0fb8f02ebead2694c1ae0568e536f9a8fbf99ba65c7050116744f18ab8c9` |
| 対象Finding（group B判定） | `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-b-v1.md` | `06c9722aed283224cff2347dc1e4d1c106f959103bfddee44d38e120e4628bd1` |
| 修正順序の裁定 | `records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md` | `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `8200a22cf56ad9cc3f1d5ae7281f136062c0cb70ad2d78b0cac49a6246f98b69` |

対象実装（修正前）：

| path | SHA-256 |
| --- | --- |
| `tools/development/policy_test_runner.py` | `64724e0ff1aed80953dd48054218c2765c905a1a207ed43ef9ddfe8056e2cd82` |
| `tools/development/pytest_summary.py` | `b70c4fb7cc6840509a9b16f683a3f2286396df7ebbfd9ba5daa4d1d71ecacebe` |
| `tools/development/declaration_red_map_check.py` | `fee17b2161cb07268cb05fd954cf5d57c29c9824add4d59ef05fc08def64e73d` |
| `tools/development/work_unit_transition.py` | `de131c00baef55799b6222aec578c2ad4e960b5e56df8a0b97fcdabd998d434e` |

- base commit：`271826a`、開始時worktree：clean
- 対象既存test（修正前）：6 file合計 **34 passed**

## 4. 対象Findingと修正方針（Pilot提案）

いずれも既存契約への**適合**であり、新しいreceipt schema・新しい方針・新しい
command種別は導入しない。

| # | 対象 | 修正方針 |
| --- | --- | --- |
| F-B1 | `policy_test_runner.py` | ①summary出力pathをrun開始前に**new-only**とし、現在runが書いたことを束縛する（実行前から存在する古いsummaryを現在runの集計として受理しない）。②合格側の整合条件に「**実合格件数が1件以上**」を加え、失敗0だけでは公式`passed`にしない（skip・xfailのみのsuiteを拒否） |
| F-B2 | `policy_test_runner.py` | receipt出力pathを**実行対象source外**へ制限する。sourceと同一pathを許さず、`source_state_digest`からの除外による同一性欠落を作らない |
| F-B3 | `pytest_summary.py` | ①`nodeid`と実行phaseで**重複計上を排除**する。②収集error（`pytest_collectreport`相当）を集計へ取り込み、`errors=0,total=0`で確定させない |
| F-B4 | `declaration_red_map_check.py` | ①`scope.kind=complete`では検査対象集合を**対応表以外からも**machine列挙し、宣言とfileの同時省略を検出する。②`red_now`は**bool型限定**（文字列`"false"`等を拒否）。③test fileのpathを**project root内**へ束縛する |
| F-B5 | `work_unit_transition.py` | ①porcelain出力だけでなく**HEADとのbytes差**を照合し、`skip-worktree`等でindex表示を消しても検出する。②対象repository identityを束縛し、別Git rootへの差し替えで合格させない |

**行わないこと**：receipt schemaの変更、pytest版の変更、対象moduleの公開CLI引数の
削除、既存receiptの再生成、他moduleの変更。

## 5. 受入条件

1. **危険側**：group B判定record §4の反証（P1・P2・P3・S1・S2・D1・D2・D3・W1・W2）
   と同じ入力に対し、各経路が拒否またはstatus `failed`となる。
2. **正例（回帰の不在）**：正常な公式run（本repositoryの`--suite full`）が引き続き
   `passed`となり、receiptの件数が実行実績と一致する。既存の正例testが壊れない。
3. 対象既存test（§7の6 file）が更新・追加後の全件で合格（件数はEvidenceへ実測）。
   公式全Test合格・status `passed`。
4. 上流設計・config・schema・既存recordは変更しない。

## 6. commit境界

| # | commit | 変更file |
| --- | --- | --- |
| 1 | **SCOPE**（本commit） | 本文書のみ |
| 2 | **RED** | §7のtest fileのみ |
| 3 | **GREEN** | §7の実装4 file、Evidence（新規）、receipt（新規） |
| 4 | **review request** | 依頼書のみ（ignore検査exit `1`確認のうえ） |

REDの定義は先行単位と同一（新規反証＋旧契約を写した既存testの契約更新のみ。
削除・緩和は禁止。実装前は新規・更新testだけが反証どおり失敗し、それ以外は合格、exit `1`）。
RED以後のtest変更にはHuman承認と理由の記録を要する。

## 7. 変更可能path

実装：`tools/development/policy_test_runner.py`、`tools/development/pytest_summary.py`、
`tools/development/declaration_red_map_check.py`、`tools/development/work_unit_transition.py`

Test：`tests/test_policy_test_runner.py`、`tests/test_policy_test_runner_summary.py`、
`tests/test_policy_test_runner_receipt_identity.py`、
`tests/test_declaration_red_map_check.py`、`tests/test_declaration_red_verification.py`、
`tests/test_work_unit_transition.py`

記録（新規）：
- `records/development/2026-08-10-official-oracle-fix-evidence-v1.md`
- `records/development/2026-08-10-official-oracle-fix-test-receipt-v1.json`
- `records/session-handoffs/2026-08-10-claude-pilot-official-oracle-fix-review-request-v1.md`

これ以外（他tool・既存record・config・schema・上流設計・TODO）は変更しない。

## 8. 停止条件（該当時はHumanへ）

1. base・worktree・固定入力Digestの不一致。
2. §7以外のpath変更が必要になった場合。
3. **既存receiptの再生成や既存recordの移行**が必要と判明した場合。
4. 修正により本repositoryの正常な公式runが`passed`にならなくなる場合
   （受入条件2の違反）。
5. 上流設計・config・schemaの変更が必要と判明した場合。
