# 範囲固定 v3：group B — F-C1・F-C2の修正

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：Human承認済み（2026-08-10「F-C1とF-C2の修正を承認する」）
- 先行：scope v1（`c5cd440`）・v2（`4fda1a6`）。両者は変更せず保持し、
  本v3が**変更可能pathの追加**と**F-C1修正の範囲**を差し替える。

## 1. 経緯

完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-official-oracle-fix-v1.md`、
SHA-256 `fd9023716741502332e945d25df585bf97dd009a758b8c22ceff3431bde80195`、
commit `9c9d9a7`、判定`report_execution_mismatch`）でblocking 2件。

- **F-C1**（類型3）：F-B5が未解消。`skip-worktree`／`assume-unchanged`では
  `git status --porcelain`も`git diff --name-only HEAD --`も空になり、HEAD差分照合を
  すり抜ける。別のclean repositoryを`project_root`へ渡すと、そのroot自身が
  `rev-parse --show-toplevel`の答えになるためidentity検査も通る。
- **F-C2**（類型4）：Work 5B契約recordのpin更新はHuman承認を得たが、
  **scope v2へ当該pathを追記しないままGREENへ含めた**。承認とcommit境界は別であり、
  committed scopeの変更file境界を破った。

## 2. F-C2の是正（変更可能pathの追加）

`records/development/2026-08-07-work5b-implementation-task-contract-v2.json`を
変更可能pathへ加える。変更は**`fixed_sources`内の`tests/test_declaration_red_map_check.py`の
`sha256`値1箇所のみ**（契約本文・受入条件・他fieldとv1は不変）。
Human承認：2026-08-10「契約recordの照合値更新を承認する」。

本v3の成立により、GREEN `f8c01b5`に含まれた当該変更は範囲内となる。
**過去commitの書き換えは行わない**（履歴を変えず、範囲固定側を正す）。

## 3. F-C1の修正方針（Pilot提案）

Gitの表示や索引の状態に依存しない照合へ変える。

1. **索引の隠蔽を受けない実バイト照合**：追跡fileごとに、HEADのblob内容と作業treeの
   bytesを直接比較する（`git ls-tree -r HEAD`で得た blob と作業fileの照合、
   または`git diff --no-index`相当の内容比較）。`skip-worktree`・`assume-unchanged`は
   索引の表示を抑えるだけで、HEAD blobと作業bytesの差は残るため検出できる。
2. **対象repositoryの実体束縛**：`project_root`が答えるrootを信用せず、
   **呼び出し元が意図した作業対象**——すなわちCLIでは実行時のcwd、library利用時は
   引数で渡されたroot——について、そのpathが実在しGit管理下であることに加え、
   `git rev-parse --show-toplevel`の結果が**渡されたpathの解決後実体と同一**であることを
   確認する。加えて、決め打ちのclean rootを渡す迂回を検出するため、
   **要求rootの実体（device・inode）**を照合する。

### 3.1 検出できる範囲の限界（明記）

呼び出し側が「別の正当なrepositoryを対象として指定した」場合、それが誤りかどうかを
tool単体で判定することはできない（利用者が対象を選ぶ自由と区別できない）。
本修正が保証するのは、**指定されたrootについて、索引の隠蔽指定に関わらず
未コミット変更を見逃さないこと**である。W2型の「別rootを渡す」運用上の誤りは、
Evidenceへ限界として記す。

## 4. 変更可能path（v1 §7・v2 §3の差し替え）

実装：`tools/development/work_unit_transition.py`（F-C1）
※ v1・v2で許可済みの他3 moduleと`conftest.py`は本v3で追加変更しない。

Test：`tests/test_work_unit_transition.py`（F-C1の反証追加）

記録：
- `records/development/2026-08-07-work5b-implementation-task-contract-v2.json`（§2、既に変更済み）
- `records/development/2026-08-10-official-oracle-fix-evidence-v1.md`（追記）
- `records/development/2026-08-10-official-oracle-fix-test-receipt-v2.json`（新規）
- `records/session-handoffs/2026-08-10-claude-pilot-official-oracle-fix-review-request-v2.md`（新規）

## 5. commit境界

| # | commit | 変更file |
| --- | --- | --- |
| 1 | **SCOPE v3**（本commit） | 本文書のみ |
| 2 | **修正RED** | `tests/test_work_unit_transition.py`のみ |
| 3 | **修正GREEN** | `tools/development/work_unit_transition.py`、Evidence追記、receipt v2 |
| 4 | **review request v2** | 依頼書のみ |

修正REDは、`skip-worktree`・`assume-unchanged`・別root差し替えの3反証を、
**実際のGit操作を使い捨ての一時repositoryに対して行う形**で固定する
（実repositoryの索引には触れない）。実装前に反証どおり失敗することを機械確認する。

## 6. 受入条件

1. W1（`skip-worktree`）・追加反証（`assume-unchanged`）で、完了関門が`blocked`を返す。
2. W2（別clean rootの差し替え）については§3.1の限界を明記したうえで、
   要求rootの実体照合により**要求rootとGitが答えるrootが食い違う場合**は拒否する。
3. 正常な運用（本repositoryでcleanなとき）は`passed`のままで、既存testを弱めない。
4. 公式全Test合格・status `passed`。

## 7. 停止条件

1. 実repositoryの索引・作業treeを反証で汚す必要が生じた場合。
2. §4以外のpath変更が必要になった場合。
3. `git`の追加subcommandがsandboxで使えない等、方針が成立しないと判明した場合。
