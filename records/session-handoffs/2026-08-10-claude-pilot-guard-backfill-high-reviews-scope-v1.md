# 範囲固定：守り役後追いレビュー・第2単位（優先度「高」19 moduleの独立レビュー実施）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：Humanのrisk確定・着手確認待ち

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: deferred #6 守り役後追いレビュー・第2単位（高19件の実施）
           （裁定record：records/development/2026-08-10-guard-backfill-priority-decision-v1.md）
```

受け渡しは`docs/development/pilot-driven-record-handoff.md`による。

## 2. risk提案

- 提案：`low`
- 根拠：本単位の成果物は**レビュー結果record群のみ**。code・test・既存recordへ
  一切触れない（Reviewerの反証実行は読み取りと一時領域のみ）。blocking finding
  が出た場合のcode修正は本単位に含めず、都度Human承認を得た別単位
  （守り役code修正は既定`high`）で行う。

## 3. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| Human裁定（高19のみ実施・6件含める） | `records/development/2026-08-10-guard-backfill-priority-decision-v1.md` | `d73f51a17ef20fa6a5abb531c30119384582cec9c299102e518088e3bb51afa7` |
| 対象一覧（verified） | `records/development/2026-08-10-guard-code-backfill-review-inventory-v1.md` | `77b6ba9fc0bfd7ea17e071dc4e4df59e12f84f4a7d23798dedafe58b6ea6571e` |
| 共通レビュー基準（§3・§4.7・§11） | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `6de9d6d8b4f0ebc93f59e7fbe1ee6e192f5aba27e7b94e4e5dfe673e65b6205a` |

## 4. 対象19 moduleとgroup分割

一覧record §5(a)〜(e)の区分どおり、5 groupに分けて順に実施する。

| group | 対象 |
| --- | --- |
| A 共通正本（3） | `tools/common/digests.py`・`tools/common/paths.py`・`tools/task_contract/identity.py` |
| B 公式検証oracle（4） | `tools/development/policy_test_runner.py`・`tools/development/pytest_summary.py`・`tools/development/declaration_red_map_check.py`・`tools/development/work_unit_transition.py` |
| C 現在地正本（2） | `tools/development/todo_handoff.py`・`tools/development/todo_update_path.py` |
| D 実行・台帳境界（3） | `tools/development/structured_argv_executor.py`・`tools/development/issue_intake_v4.py`・`tools/layout/baseline.py` |
| E 外部送信・機微境界（7） | `tools/egress/approval.py`・`gate.py`・`payload.py`・`prefilter.py`・`sender.py`・`tools/session_logs/preservation.py`・`tools/session_logs/private_validation.py` |

## 5. 今回の作業（第2単位）

group毎に、Reviewer（Codex）が現行体制の独立レビューを実施する：

1. 対象moduleの実装・既存testを読み、**既存fixtureに無い反証**（不正入力・改竄・
   境界脱出・偽陰性を狙う入力）を機械実行する（読み取り専用・一時領域のみ。
   実台帳・実設定・利用者環境へ書かない）。
2. 結果を判定record
   `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-<a〜e>-v1.md`
   として新規作成し、単独commitする。内容：module毎の判定（§4.7）、finding
   （§11区分：blocking／non-blocking／defer）、実行した反証の一覧と結果、
   model来歴行。
3. Pilotは各group完了時に鮮度・単独commit・禁止path不変を機械照合する。

**本単位で行わないこと**：code・test・既存recordの修正（blocking findingの修正は
Human承認後の別単位）、「中」「低」moduleのレビュー、TODO反映（Closerが最後に行う）。

## 6. 受入条件

1. 19 module全てが5 recordのいずれかで判定を持ち、反証は機械実行の結果
   （command・結果・終了コード）を伴う。
2. findingは§11の閉じた区分に従い、blockingは4類型のみ。
3. 成果はレビューrecord 5件（＋Closer のTODO反映1 commit）のみ。

## 7. 変更可能path

- `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-a-v1.md` 〜 `-group-e-v1.md`（新規）
- `TODO_NEXT_SESSION.md`（Closerのみ、最後に）

## 8. 停止条件

1. 固定入力Digestの不一致。
2. §7以外のpath変更が必要になった場合。
3. blocking findingの検出は停止ではなく記録し、group完了毎にHumanへ集約報告する
   （修正着手はHuman承認待ち）。

## 9. commit境界

1. **SCOPE**（本commit）：本文書のみ。Humanのrisk確定・着手確認待ちで停止。
2. **REVIEW×5**：group毎に判定record 1件ずつ（Reviewer単独commit）。
3. **CLOSE**：CloserによるTODO反映1件。
