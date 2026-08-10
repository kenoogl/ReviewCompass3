# 範囲固定 v2：group C — 受入条件の補完と変更可能pathの絞り込み

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビューv2待ち（risk確定・着手・RED開始は包括承認済み）
- 先行：scope v1（`1831450`）。範囲レビューv1（`994c072`、要修正・blocking 2件）により
  v1をRED開始の根拠にできない。v1は変更せず保持し、本v2が
  **§5受入条件1**と**§7変更可能path**のみを差し替える。

## 1. 指摘の反映

### SR-C-SCOPE-001（受入条件の漏れ）

v1 §5.1の危険側はH1・H2・H4・H5・U1〜U4の8件で、上流group C判定の
**H3（実branch差替え）**と**H6のUnicode空白による行構造逃れ**を列挙していなかった。
方針（§4）には含めていたが、受入条件に無いため「8件だけ拒否する実装」でも
合格できてしまう。

### SR-C-SCOPE-002（変更可能pathの過剰）

v1 §7のtest 5 fileのうち3件——`tests/test_todo_handoff_projection.py`、
`tests/test_todo_handoff_projection_repository.py`、
`tests/test_todo_handoff_prompt_entrypoints.py`——は対象実装をimportせず、
別契約（projectionのrenderer、repository template、prompt入口）を検査している。
今回のFinding修正はこれらの変更を要求しないため、変更可能pathから外す。

## 2. 差し替え後の §5 受入条件1（危険側）

group C判定record §4の反証**10件**と同じ入力に対し、各経路が拒否すること。

| ID | 反証の要旨 |
| --- | --- |
| H1 | 現HEADへ解決する4文字SHAの自己snapshot |
| H2 | 同じくHEADへ解決する40文字**大文字**SHA |
| **H3** | **実Gitの現在branchと異なるbranch記載** |
| H4 | **末尾空白付きの別名Git見出し**へ禁止snapshotを置く |
| H5 | **別のGit状態節**へ同じ内容を置いて検査範囲外へ逃がす |
| **H6** | **Unicode空白**を用いた非正規行による行構造逃れ |
| U1 | 第2receiptの未知kind・偽runner・exit code 9・浮動小数件数・整数0のfallback |
| U2 | 第1receiptの再利用（要求pathと実pathの非束縛） |
| U3 | 候補read-back後、第2公式Test callback内でのTODO差替え |
| U4 | CRLF改行22個のTODOが正常二段更新でLFへ書き換わる |

H6のうちBOM・CRLF読取り・必須3行の順序入替えは**上流Findingではない**ため、
拒否対象へ広げない（範囲レビューv1の指摘どおり）。

v1 §5の2〜4（正例＝実TODO検査の維持、既存test全件合格と公式全Test、
上流・config・schema・既存record不変）は不変。

## 3. 差し替え後の §7 変更可能path

実装：`tools/development/todo_handoff.py`、`tools/development/todo_update_path.py`

Test：`tests/test_todo_handoff_git_state.py`、`tests/test_todo_update_path.py`
（**v1から3 fileを削除**）

記録（新規）：v1 §7のとおり3件。

**回帰確認のみの対象**（変更しない）：
`tests/test_todo_handoff_projection.py`、
`tests/test_todo_handoff_projection_repository.py`、
`tests/test_todo_handoff_prompt_entrypoints.py`、および範囲レビューv1が挙げた
§7外の関連回帰4 fileと直接呼出元1 module。これらが失敗して変更が必要になった場合は、
v1 §8-2の停止条件に従いHumanへ諮る。

## 4. 不変の節

v1 §1〜§4、§6 commit境界、§8 停止条件はそのまま有効。特に、
反証は使い捨ての一時領域だけで行い、実`TODO_NEXT_SESSION.md`と実Git索引には
触れない規定を維持する。
