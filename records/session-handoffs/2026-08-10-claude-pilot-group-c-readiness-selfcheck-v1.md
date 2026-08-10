# 自己点検：group C実装着手前の準備状況（Pilot自己申告）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 契機：Humanの問い「組Cに適用する手法には抜け漏れはないのか」
  「本当に、推奨案でよいか？　多視点でみて、抜け・漏れはないか？」
  および指示「信用度が低い。codexへレビューを回せ。」
- 位置づけ：**Pilotの自己申告**であり、Codexの独立点検の対象。
  Pilotの点検は信用しない前提で、Reviewerが**独自に**過不足を判定すること。

## 0. 現状（機械出力の転記）

```text
$ .venv/bin/python3 -m pytest tests/ -q | tail -1
12 failed, 1470 passed in 12.89s
```

失敗12件はgroup CのRED commit `431dd7b`が追加したtestであり、実装が未着手のため。
**mainは現在「赤い」状態**である。

## 1. 固定対象

| role | path | SHA-256 |
| --- | --- | --- |
| 上流Finding（group C判定） | `records/session-handoffs/2026-08-10-codex-guard-backfill-review-group-c-v1.md` | `d7b52bd131cbae3e559643c66e229c52084710586171cd3b4644e61bb5540b0d` |
| 現行の範囲固定 | `records/session-handoffs/2026-08-10-claude-pilot-current-position-fix-scope-v3.md` | `44f46ae89a98d234aedffc45ffa44b5d30fdc040eaa8d864b45b80d607baf683` |
| RED test 1 | `tests/test_todo_handoff_git_state.py` | `66fa2dd016e8316c00d6fd4efd508da6536c469eda37f8372b3b940390fd520b` |
| RED test 2 | `tests/test_todo_update_path.py` | `322f1629bfd2b308193ea6465e48e4534d273fb3388b6a8938d4243688f2a79a` |

Human指示（2026-08-10）：「`todo_record_generation.py`を変更可能に加える。範囲固定v4を
作って再レビューへ」。**v4は未作成**である。

## 2. Pilotが自己申告する抜け（5件）

Reviewerはこの申告を正しいと仮定せず、独自に過不足を判定すること。

### 2.1 巻き添えで壊れうるtestが範囲外（規約Aの実行結果）

変更予定の3 fileを取り込むtestは**9 file**。範囲固定v3が変更可能とするのは**2 file**。

| 変更予定 | 取り込んでいるtest |
| --- | --- |
| `todo_handoff.py` | `test_todo_handoff_projection`／`test_todo_handoff_git_state`／`test_todo_handoff_prompt_entrypoints`／`test_common_digests` |
| `todo_update_path.py` | `test_issue_resolution_pilot_wi_005`／`test_common_errors_paths_output`／`test_todo_update_path`／`test_shared_function_sweep` |
| `todo_record_generation.py` | `test_todo_record_generation`／`test_common_errors_paths_output`／`test_todo_update_path` |

Digestを実行時に再計算して照合するtestは**無い**（記録内の記述のみ）。
したがってgroup Aの指紋pin、group Bの契約recordのような巻き添えは**起きない**見込み。

### 2.2 `todo_record_generation.py`が範囲固定v3に未反映

Human指示で変更可能に加えるが、v3には無い。

### 2.3 本日確定した記録義務が未反映

材料の出自（機械導出か判断選定か）の1行、判定recordのモードと抽出件数。
裁定record：`records/development/2026-08-10-review-material-mode-decision-v1.md`。

### 2.4 反証U2（第1receiptの再利用）のtestが存在しない

上流の`F-C3`は「要求pathとexecutorが返した実pathを束縛しないため、第1receiptの再利用を
『二度目の公式実行』として合格させられる」を含む。`tests/test_todo_update_path.py`を
検索したが該当testは見つからなかった。

### 2.5 反証U4（CRLF破壊）のtestを削除したまま

Pilotが「実処理が範囲外の`todo_record_generation.py`にある」と判明した時点で削除した。
その後Humanが同fileを変更可能に加えたため、**復活させる必要がある**。

## 3. 反証とtestの対応（Pilotの申告）

| 反証 | 対応するtest | Pilot申告 |
| --- | --- | --- |
| H1 短縮SHA | `test_short_lowercase_sha_snapshot_is_rejected` | あり |
| H2 大文字SHA | `test_uppercase_forty_character_sha_snapshot_is_rejected` | あり |
| H3 branch不一致 | `test_branch_mismatch_is_rejected` | あり |
| H4 末尾空白見出し | `test_trailing_space_heading_variant_is_counted` | あり |
| H5 別のGit状態節 | `test_alternative_git_section_heading_is_counted` | あり |
| H6 Unicode空白 | `test_unicode_space_line_is_normalised` | あり |
| U1 receipt偽造 | `test_unknown_receipt_kind_is_rejected`／`test_nonzero_exit_code_is_rejected`／`test_boolean_and_integer_are_not_equal` | あり |
| U2 receipt再利用 | — | **無い** |
| U3 確認後の差替え | `test_todo_swapped_after_verification_is_detected` | あり |
| U4 CRLF破壊 | — | **削除したまま** |

範囲固定v3 §2の受入条件1は**10件すべて**の拒否を要求している。
現状のままGREENへ進むと、**受入条件を満たさないのに全testが通る**状態になりうる。

## 4. Reviewerへの確認観点

**Pilotの§2・§3の申告を正しいと仮定しないこと。** 独自に次を判定せよ。

1. 上流group C判定record §4の反証を**あなた自身で列挙**し、
   現RED test（2 file）との対応を独立に作れ。Pilotが挙げた「U2・U4が無い」以外に
   **不足・過剰・誤対応**が無いか。
2. 各REDテストが**狙った反証そのものを理由に失敗しているか**を機械確認せよ
   （別理由での失敗＝偽陰性でないか）。group Aで`F-CG-COMP-001`、group Cで
   Pilot自身が2件の偽陰性を出した前例がある。
3. §2.1の巻き添え調査（9 file、Digest実行時照合なし）が正しいか。
   **Pilotが見落とした巻き添え経路**が無いか独自に探せ。
4. 範囲固定v3の受入条件・変更可能path・commit境界と、Human指示
   （`todo_record_generation.py`の追加）の間に**矛盾または未反映**が無いか。
5. 実装着手前に**他に満たすべき前提**が無いか（Pilotが列挙していない観点を含む）。

材料モード：発見力（repository全体を参照してよい）。
本レビューは実装着手の可否を判定するものであり、周回数の上限は設けない。
