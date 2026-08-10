# 範囲固定 v3：group C — 受入条件と変更可能pathの統合（不整合の解消）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビューv3待ち（risk確定・着手・RED開始は包括承認済み）
- 先行：scope v1（`1831450`）、v2（`72b8389`）。範囲レビューv2（`f943251`、
  要修正・blocking 1件 SR-C-SCOPE-003）により、v2をRED開始の根拠にできない。
  v1・v2は変更せず保持する。

## 1. 指摘（SR-C-SCOPE-003）と是正方針

v2は§7（変更可能test）だけを5 file→2 fileへ差し替えたが、v1 §5.3の受入条件は
「§7の5 file」と書かれたまま残り、**同じ集合を指す2つの数が併存**した。
v1 §6のRED定義も「§7のtest fileのみ」と参照するため、REDで変更できるtestが
2 fileとも5 fileとも読めた。

**是正**：本v3で、**受入条件・変更可能path・RED定義の3か所を一つの文書にまとめて
再掲**する。以後、group Cの範囲は**本v3だけ**を読めば一意に定まる。
v1・v2の当該節（v1 §5・§6・§7、v2 §2・§3）は本v3が置き換える。
v1 §1〜§4（mode・risk・固定入力・修正方針）と§8（停止条件）はそのまま有効。

## 2. 受入条件（確定版）

1. **危険側**：group C判定record §4の反証**10件**と同じ入力に対し、各経路が拒否する。

   | ID | 反証の要旨 |
   | --- | --- |
   | H1 | 現HEADへ解決する4文字SHAの自己snapshot |
   | H2 | 同じくHEADへ解決する40文字大文字SHA |
   | H3 | 実Gitの現在branchと異なるbranch記載 |
   | H4 | 末尾空白付きの別名Git見出しへ禁止snapshotを置く |
   | H5 | 別のGit状態節へ同じ内容を置いて検査範囲外へ逃がす |
   | H6 | Unicode空白を用いた非正規行による行構造逃れ |
   | U1 | 第2receiptの未知kind・偽runner・exit code 9・浮動小数件数・整数0のfallback |
   | U2 | 第1receiptの再利用（要求pathと実pathの非束縛） |
   | U3 | 候補read-back後、第2公式Test callback内でのTODO差替え |
   | U4 | CRLF改行22個のTODOが正常二段更新でLFへ書き換わる |

   H6のうちBOM・CRLF読取り・必須3行の順序入替えは上流Findingではないため、
   拒否対象へ広げない。

2. **正例**：本repositoryの実`TODO_NEXT_SESSION.md`に対する
   `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`が引き続き合格する。
3. **変更するtest**：§3の**2 file**が、更新・追加後の全件で合格する
   （件数はEvidenceへ実測を記す）。
4. **変更しないtest**：§3の回帰確認対象が、変更なしで合格し続ける。
5. 公式全Test合格・status `passed`。
6. 上流設計・config・schema・既存recordは変更しない。

## 3. 変更可能path（確定版）

実装（2 file）：
- `tools/development/todo_handoff.py`
- `tools/development/todo_update_path.py`

Test（**2 fileのみ**）：
- `tests/test_todo_handoff_git_state.py`
- `tests/test_todo_update_path.py`

記録（新規3件）：
- `records/development/2026-08-10-current-position-fix-evidence-v1.md`
- `records/development/2026-08-10-current-position-fix-test-receipt-v1.json`
- `records/session-handoffs/2026-08-10-claude-pilot-current-position-fix-review-request-v1.md`

**回帰確認のみ（変更しない）**：
`tests/test_todo_handoff_projection.py`、
`tests/test_todo_handoff_projection_repository.py`、
`tests/test_todo_handoff_prompt_entrypoints.py`、および範囲レビューv1が挙げた
§3外の関連回帰4 fileと直接呼出元1 module。これらの変更が必要になった場合は、
v1 §8-2の停止条件に従いHumanへ諮る。

上記以外（他tool・既存record・config・schema・上流設計・TODO本体）は変更しない。

## 4. commit境界とRED定義（確定版）

| # | commit | 変更file |
| --- | --- | --- |
| 1 | **SCOPE v3**（本commit） | 本文書のみ |
| 2 | **RED** | §3のtest **2 fileのみ** |
| 3 | **GREEN** | §3の実装2 file、Evidence（新規）、receipt（新規） |
| 4 | **review request** | 依頼書のみ（ignore検査exit `1`確認のうえ） |

- REDは、新規反証と、旧契約を写した既存testの契約更新だけを含む。
  削除・検査性質の緩和は禁止。実装前は新規・更新testだけが反証どおり失敗し、
  それ以外は合格、exit `1`であることを機械確認してEvidenceへ記録する。
- RED以後のtest変更にはHuman承認と理由の記録を要する。
- **反証は使い捨ての一時領域だけで行い、実`TODO_NEXT_SESSION.md`と実Git索引には
  触れない。**
