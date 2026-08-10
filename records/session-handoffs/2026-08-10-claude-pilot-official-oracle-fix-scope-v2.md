# 範囲固定 v2：group B — conftest結線と既存test 1件の契約更新

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：**Humanの承認待ち**（包括承認 §2 の停止条件・修正承認に該当）
- 先行：scope v1（`c5cd440`、範囲レビューv1 `verified`：`134fed4`）。v1は変更せず保持し、
  本v2が**§7 変更可能pathの追加**と**既存test 1件の契約更新の許可**のみを差し替える。

## 1. 停止した理由

GREEN実装中に、v1の範囲では完了できない2点が判明した。いずれも包括承認
（`records/development/2026-08-10-guard-backfill-autonomous-authorization-v1.md`）
§2で**Humanに留保された**事項である。

### 1.1 F-B3の実運用結線に`conftest.py`が要る（停止条件§8-2）

`pytest_summary.record_collect_report`（収集errorの算入）を新設したが、pytestのhookを
登録しているのは`conftest.py`であり、そこへ`pytest_collectreport`を結線しないと
**実運用では従来どおり収集errorが0のまま**になる。`conftest.py`はv1 §7に無い。

- 提案：`conftest.py`を変更可能pathへ加える。変更は**hook 1個の追加のみ**
  （`pytest_collectreport`で`record_collect_report`を呼ぶ4行）。既存hookは変更しない。

### 1.2 F-B5の修正で既存test 1件が旧契約を写している（修正承認§2-2）

`tests/test_work_unit_transition.py::test_preflight_reads_git_state_mechanically`は、
`preflight_next_work`が**`git status`だけを1回呼ぶ**ことをcall列で固定している。
F-B5の修正は、`skip-worktree`等でindex表示が消えても検出するために
`git rev-parse --show-toplevel`（対象repositoryの同一性束縛）と
`git diff --name-only HEAD`（HEADとのbytes差）を加えるため、この既存testは失敗する。

- 提案：当該既存test 1件の**呼び出し形（期待するcall列）のみ**を新契約へ更新する。
  検査している性質（機械的にGit状態を読み、blockedを返すこと）は保持し、
  削除・緩和はしない。REDの原則どおり、更新後のtestが修正前実装で失敗することを
  機械確認してEvidenceへ記録する。
- これはRED以後のtest変更にあたるため、Human承認と理由の記録を要する。

## 2. 実装済み（v1範囲内・未commit）

| finding | 状態 |
| --- | --- |
| F-B1 | 実装済み。実行前から在るsummaryを拒否（`test_summary_stale`）、実合格0件の公式合格を拒否 |
| F-B2 | 実装済み。receipt pathを`records/`配下へ限定し、既存`.py`への上書きを拒否 |
| F-B3 | **module側は実装済み**（nodeid＋段階での重複排除、`record_collect_report`新設）。§1.1の結線が未了 |
| F-B4 | 実装済み。completeの空対応表を拒否、`red_now`のbool型限定、root外file参照の拒否 |
| F-B5 | 実装済み。HEADとのbytes差の照合とrepository identity束縛。§1.2の既存test更新が未了 |

現時点の測定：group B対象6 test fileで **47 passed / 1 failed**（失敗は§1.2の1件のみ）。

## 3. 差し替え後の §7 変更可能path

実装：`tools/development/policy_test_runner.py`、`tools/development/pytest_summary.py`、
`tools/development/declaration_red_map_check.py`、`tools/development/work_unit_transition.py`、
**`conftest.py`（hook 1個の追加のみ）**

Test：v1 §7の6 file（うち`tests/test_work_unit_transition.py`は§1.2の既存test 1件の
契約更新を含む）

記録（新規）：v1 §7のとおり。

## 4. 差し替え後のcommit境界

| # | commit | 変更file |
| --- | --- | --- |
| 2' | **修正RED** | `tests/test_work_unit_transition.py`（既存test 1件の契約更新のみ） |
| 3' | **GREEN** | 実装4 file＋`conftest.py`、Evidence（新規）、receipt（新規） |
| 4 | **review request** | 依頼書のみ |

## 5. Humanへの確認事項

1. `conftest.py`を変更可能pathへ加えること（hook 1個の追加に限る）。
2. `test_preflight_reads_git_state_mechanically`の呼び出し形の更新（性質は保持）。

いずれも承認が得られない場合、F-B3は実運用で未修正のまま、F-B5は修正不能となるため、
その旨をEvidenceへ記し、当該findingを未解消として残す。
