# 4件の裁定（policy v5・レビュー開始・段完了・削除）Decision v1

- decision ID：`DEC-FOUR-RULINGS-2026-08-07-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言（2026-08-07）
  「1．作成可。 2．承認、新module含む 3．承認 4．削除」

## 裁定1：freshness policy v5の作成——**可**

既存`write_freshness_policy_v4`でpolicy_version 5として機械生成する。開発方針参照の現行化のみで、
判定語彙・閾値・change_classは変更しない。作成後、`validate_current`の挙動を機械確認してから
コミットする（`DEC-UNIVERSE-RECORD-V2-TIMING-001`と同じ事前確認規則）。

## 裁定2：レビューbacklogの着手——**承認、新module含む**

`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`を`in_progress`へ進め、反証レビューの第1束を
次の構成とする。

- **新module 4件**（本日新設の守り役）：`reuse_search_record.py`（外部化含む）、
  `declaration_red_map_check.py`、`integration_exclusions.py`、`candidate_ranking.py`
- 従来優先度の上位2系統：`operation_routing.py`＋`structured_argv_executor.py`、
  `issue_intake_v4.py`＋`issue_resolution_pilot.py`

方法はwork-review-protocol §4.4（実装者のfixtureに無い反証の新作）・§5（上流からの独立oracle
導出）。レビュー結果と修正は分離する（§2-5）。

## 裁定3：Work 5Bの段完了——**承認**

checklist §10の全6項目がEvidence接続済みであることを前提に、Work 5B（内部Implementation
Task Contract Pilot）の段完了を承認する。

## 裁定4：外部化済み旧record 7件と旧書庫——**削除**

- 検索record旧位置7件：外部化のbyte一致検証と証明書作成が完了済み（`591e998`）。削除前に
  test・validator・Contractからの機械参照を走査し、**機械参照が残るfileは参照の解消まで削除を
  保留して報告する**（黙って壊さない）。
- 旧書庫：Layout v3移行のrollback保持分。削除前に移行Receiptの検証結果を再確認する。

## この決定が承認していないこと

- レビューで見つかった欠陥の修正（レビューと分離し、都度Human判断）
- backlog以外のIssueの着手
