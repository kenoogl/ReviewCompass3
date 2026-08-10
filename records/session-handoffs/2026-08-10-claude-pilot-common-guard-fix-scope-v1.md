# 範囲固定：group A（共通正本）blocking 2件の修正

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビュー待ち → Humanのrisk確定は受領済み

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: 守り役後追い修正 第2単位（group A＝共通正本のF-A1・F-A2修正）
           （裁定record：records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md）
```

## 2. riskとHuman承認

- risk：`high`（Human確定済み）
- Human承認（2026-08-10）：「組A修正 risk highを確定、着手を承認する」
- 根拠：対象はDigest計算とpath境界判定の**共通正本**であり、ほぼ全ての守り役が
  依存する。修正の誤りは全validatorの誤った合格として波及する。

## 3. 固定入力と上流authority

| role | path | SHA-256 |
| --- | --- | --- |
| 対象Finding（group A判定） | `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-a-v1.md` | `34a53581751a5b23864933b3ab23e08a875170ab5cdbe08e00e112c803da5139` |
| 修正順序の裁定 | `records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md` | `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997` |
| 上流（構造化正本はJSON互換の閉じたschema。§3.1） | `docs/design/2026-08-02-task-contract-design-amendment.md` | `55115696a3a33612fa52d7fab59dddccb2045ef6baba982a4b5fe17437b25eda` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `bcab80e9f52fcaa1a594567ca79d03be6f3777ecebb83cc8eb4ca7b987d78164` |

対象実装（修正前）：

| path | SHA-256 |
| --- | --- |
| `tools/common/digests.py` | `db6b830592f5d57ef7b42b5ec32fd398f4c36957a978604166525fc54da3396f` |
| `tools/common/paths.py` | `daa325791b5bead80c240eb298c7084f6c26ff2d96ca850cc65449686cc4826d` |
| `tools/task_contract/identity.py` | `bbbce848e3beb50301c2ef4e242a75daf64968a0d5c1f2f733751ac2a75a5c42` |

- base commit：`17c2002`、開始時worktree：clean

## 4. 対象Findingと修正方針（Pilot提案）

上流（構造化正本はJSON互換の閉じたschema）への**適合**であり、新しいschema・
新しいDigest algorithm・新しいpath規則は導入しない。

| # | 対象 | 修正方針 |
| --- | --- | --- |
| F-A1 | `tools/common/digests.py`（正本）、`tools/task_contract/identity.py`（`canonical_bytes`・`seal`・`validate_record`） | Digest計算の前に**JSON互換性をfail-closedで検査**する。非文字列key・tuple等のnon-JSON型・非有限数（NaN・±Infinity）を拒否し、`json.dumps`は`allow_nan=False`とする。これにより「異なるPython値が同一Digestになる」経路を断つ |
| F-A2 | `tools/common/paths.py`（`within`） | root内判定を、字句上の解決後path比較に加えて**実体同一性（`os.stat`のdevice・inode）** による照合へ拡張する。case差・Unicode正規化差だけが違う実在pathをroot外と誤判定しない。存在しないpathは従来どおり解決後pathで判定し、判定不能はfail-closed（False）を維持する |

**明示的に行わないこと**：Digest algorithmの変更、canonical仕様（key順・
`ensure_ascii=False`・`separators`・`content_digest`除外）の変更、既存recordの
再計算・移行、`within`の呼び出し側の変更。

## 5. 受入条件

1. **危険側（反証の不成立）**：group A判定recordの反証と同じ入力に対し、
   - `{1: "value"}`と`{"1": "value"}`、tupleとlist、NaNを含むrecordは
     **Digest計算・`seal`・`validate_record`のいずれでも拒否**される
     （同一Digestで合格しない）。
   - case差・NFC/NFD差だけが違う実在directoryについて、`within`が
     `os.path.samefile`と**同じ判定**を返す。
2. **正例（回帰の不在）**：既存の正常record（JSON互換）のDigest値が
   **修正前と一致**すること（値の変化は台帳全体の再計算を招くため許さない）。
   実台帳の代表record数件で修正前後のDigestが一致することを機械確認する。
3. 既存testが壊れない：§7の対象test fileが更新・追加後の全件で合格
   （件数はEvidenceに実測を記す）。公式全Test合格・status `passed`。
4. 上流設計・config・schema・既存recordは変更しない。

## 6. commit境界

| # | commit | 変更file（これ以外を含めない） |
| --- | --- | --- |
| 1 | **SCOPE**（本commit） | 本文書のみ |
| 2 | **RED** | `tests/test_common_digests.py`・`tests/test_common_errors_paths_output.py` |
| 3 | **GREEN** | `tools/common/digests.py`・`tools/common/paths.py`・`tools/task_contract/identity.py`、Evidence（新規、§7）、receipt（新規、§7） |
| 4 | **review request** | 依頼書のみ（ignore検査exit `1`確認のうえ） |

- REDは「実装前に新規test（および旧契約を写した既存testがあればその契約更新）だけが
  反証どおり失敗し、それ以外の既存testは合格、exit `1`」を機械確認してEvidenceへ記録する
  （scope v3 for group Eで承認されたRED定義と同一の運用）。既存testの削除・
  検査性質の緩和は禁止。
- RED以後のtest変更にはHuman承認と理由の記録を要する。

## 7. 変更可能path

実装：`tools/common/digests.py`、`tools/common/paths.py`、
`tools/task_contract/identity.py`

Test：`tests/test_common_digests.py`、`tests/test_common_errors_paths_output.py`

記録（新規）：
- `records/development/2026-08-10-common-guard-fix-evidence-v1.md`
- `records/development/2026-08-10-common-guard-fix-test-receipt-v1.json`
- `records/session-handoffs/2026-08-10-claude-pilot-common-guard-fix-review-request-v1.md`

これ以外のfile（他tool・既存record・config・schema・上流設計・TODO）は変更しない。

## 8. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §7以外のpath変更が必要になった場合。特に、JSON互換検査の導入により
   **既存の実台帳recordが拒否される**ことが判明した場合は、移行の要否がHuman裁定に
   なるため停止する。
3. 既存recordのDigest値が修正前後で変わる場合（受入条件2の違反）は停止する。
4. 修正が上流設計と矛盾する場合。

## 9. Humanへの確認事項

- risk `high`の確定と着手承認：**受領済み**（§2）。
- 追加の承認が必要になるのは、§8-2または§8-3に該当した場合のみ。
