# 範囲固定：group C（現在地正本）blocking 5件の修正

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビュー待ち（risk確定・着手・RED開始は包括承認済み）

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: 守り役後追い修正 第4単位（group C＝現在地正本のF-C1〜F-C5修正）
```

## 2. riskとHuman承認

- risk：`high`（包括承認により確定）
- Human承認（2026-08-10）：「組BからDまで自律的に実行。停止条件に触れたときと、
  修正の承認が要るときだけ止めよ」
  （承認record `271826a`。risk確定・着手・RED開始・GREEN着手を事前承認）
- 根拠：対象はTODO（現在地の正本）の検査と更新経路であり、誤りは
  **作業の現在地の偽装**として現れる。

## 3. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 包括承認 | `records/development/2026-08-10-guard-backfill-autonomous-authorization-v1.md` | `3c0a0fb8f02ebead2694c1ae0568e536f9a8fbf99ba65c7050116744f18ab8c9` |
| 対象Finding（group C判定） | `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-c-v1.md` | `d7b52bd131cbae3e559643c66e229c52084710586171cd3b4644e61bb5540b0d` |
| 修正順序の裁定 | `records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md` | `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `3e944791e21da372e9723257c72881d8332f605bcec37c8364926c98b8e7be14` |

対象実装（修正前）：

| path | SHA-256 |
| --- | --- |
| `tools/development/todo_handoff.py` | `fbc6279b6471913f490b604940c14ef792b139e35819c951a0e4406ce5994d61` |
| `tools/development/todo_update_path.py` | `3396e9d8131c8059661a7a264503faafe7ad1d5b8af96b09d9483385e873bd31` |

- base commit：`cbc8709`、開始時worktree：clean
- 対象既存test（修正前）：5 file合計 **42 passed**

## 4. 対象Findingと修正方針（Pilot提案）

| # | 対象 | 修正方針 |
| --- | --- | --- |
| F-C1 | `todo_handoff.py` | SHA検出を7〜40文字の小文字に限定せず、**4文字以上・大文字を含む形も対象**とし、実Gitへ解決したうえで自己SHA snapshotを拒否する。branch記載も実Gitの現在branchと照合する |
| F-C2 | `todo_handoff.py` | 対象節の判定を完全一致見出しだけに頼らず、**末尾空白・別見出し・Unicode空白の別表現**を正規化して数える。必須文は部分文字列ではなく**行構造**で検査し、欄外へ逃がした可変Git状態を検査範囲外にできないようにする |
| F-C3 | `todo_update_path.py` | 第2receiptの**構造・実行結果・identity**を検証する（kind・runner・exit code・件数の型・fallbackを含む）。`False == 0`や整数同値の浮動小数を一致としない。要求pathとexecutorが返した実pathを束縛し、第1receiptの再利用を拒否する |
| F-C4 | `todo_update_path.py` | 第2実行の**後に**TODOをread-backし、候補bytesとの同一性を再確認してから確定する（確認途中の差替え・並行更新を未検証のまま通さない） |
| F-C5 | `todo_update_path.py` | 読み取りを`read_text()`（改行変換あり）から**bytes単位**へ変え、機械管理外bytes（CRLF等）を書き換えない |

**行わないこと**：TODOの書式変更、新しい検査項目の追加、receipt schemaの変更、
`todo_handoff_projection.py`等の他moduleの変更。

## 5. 受入条件

1. **危険側**：group C判定record §4の反証（H1・H2・H4・H5・U1・U2・U3・U4）と同じ入力に
   対し、各経路が拒否する。
2. **正例（回帰の不在）**：本repositoryの実`TODO_NEXT_SESSION.md`に対する
   `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`が
   引き続き合格すること（現在地の検査が通らなくなると全作業が止まるため）。
3. 対象既存test（§7の5 file）が更新・追加後の全件で合格（件数はEvidenceへ実測）。
   公式全Test合格・status `passed`。
4. 上流設計・config・schema・既存recordは変更しない。

## 6. commit境界

| # | commit | 変更file |
| --- | --- | --- |
| 1 | **SCOPE**（本commit） | 本文書のみ |
| 2 | **RED** | §7のtest fileのみ |
| 3 | **GREEN** | §7の実装2 file、Evidence（新規）、receipt（新規） |
| 4 | **review request** | 依頼書のみ（ignore検査exit `1`確認のうえ） |

REDの定義は先行単位と同一（新規反証＋旧契約を写した既存testの契約更新のみ。
削除・緩和は禁止。実装前は新規・更新testだけが反証どおり失敗し、それ以外は合格、exit `1`）。
RED以後のtest変更にはHuman承認と理由の記録を要する。
**反証は使い捨ての一時領域だけで行い、実`TODO_NEXT_SESSION.md`と実Git索引には触れない。**

## 7. 変更可能path

実装：`tools/development/todo_handoff.py`、`tools/development/todo_update_path.py`

Test：`tests/test_todo_handoff_git_state.py`、`tests/test_todo_handoff_projection.py`、
`tests/test_todo_handoff_projection_repository.py`、
`tests/test_todo_handoff_prompt_entrypoints.py`、`tests/test_todo_update_path.py`

記録（新規）：
- `records/development/2026-08-10-current-position-fix-evidence-v1.md`
- `records/development/2026-08-10-current-position-fix-test-receipt-v1.json`
- `records/session-handoffs/2026-08-10-claude-pilot-current-position-fix-review-request-v1.md`

これ以外（他tool・既存record・config・schema・上流設計・TODO本体）は変更しない。

## 8. 停止条件（該当時はHumanへ）

1. base・worktree・固定入力Digestの不一致。
2. §7以外のpath変更が必要になった場合（**指紋pin・契約recordなど巻き添えの
   追随変更を含む**。group Bの経験から明示する）。
3. 修正により実`TODO_NEXT_SESSION.md`の検査が通らなくなる場合（受入条件2の違反）。
4. TODOの書式変更や既存recordの移行が必要と判明した場合。
5. 上流設計・config・schemaの変更が必要と判明した場合。
