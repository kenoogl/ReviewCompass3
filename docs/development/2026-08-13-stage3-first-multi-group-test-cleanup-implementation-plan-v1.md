# 第3段 最初の複数群試験整理 実施計画 v1

- 作成日：2026-08-13
- 状態：`proposed_pending_independent_and_human_review`
- 基準commit：`191cafe6ac60b25a38947d6140207f84b7b48f7c`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 危険度案：`medium`
- 実施前Human承認：必要
- 他社モデル確認：第3段で予定する一回目。本計画の変更点確認に限定する

## 1. 目的

G04とG11で役割終了候補と確認できた試験を、製品コードや履歴資料を変更せず、二つの試験ファイルに閉じた
最初の意味的な整理単位として実施する。試験件数の削減自体を目的にせず、現在保証と作業時点の検査を分け、
試験専用処理の残骸を同時に除く。

## 2. 入力と固定根拠

- G04役割分類v2：`records/development/2026-08-13-stage3-g04-role-classification-evidence-v2.md`
  - SHA-256：`db16c07912ed13250f17faa017c71538bc277b79b133c3cf6874cd6ae789a834`
- G04限定修正後確認：
  `records/development/2026-08-13-stage3-g04-role-classification-evidence-v2-one-time-correction-review-v1.md`
  - SHA-256：`e61b337012f4771405c5e127235d559c8801d6c54099bfd8fb1b8e7ab3a84681`
- 混在三群抽出v2：`records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-evidence-v2.md`
  - SHA-256：`d74a2a202f78273e1cfb6aabc0097098a1820c56db32b8f38060c95d4cd9ba34`
- 混在三群限定修正後確認：
  `records/development/2026-08-13-stage3-mixed-groups-history-pin-extraction-evidence-v2-one-time-correction-review-v1.md`
  - SHA-256：`63371ea2bbf9a5e70086f48dcf6de44f7e8649ce0de85fa536760228be2b537d`
- 手動確認回数Decision：
  `records/development/2026-08-13-stage3-manual-external-review-limit-decision-v1.md`
  - SHA-256：`9c0bd9d371b1f6b59be49818b759d17e3877d645f42ff6dc4a4c0eacbeb05136`

## 3. 三案比較

| 案 | 内容 | 単純さ | 処理時間・記憶量 | 頑健さ | 変更範囲 | 保守負担・戻しやすさ | 判断 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A 承認済み一件だけ | G04のRED証跡三文言試験だけを削除 | 最も小さい | 差は最小 | 製品保証は維持するが、同じ作業時点固定と試験専用残骸を残す | 1 file、1試験 | 戻しやすいが一件ずつ手続きを繰り返す | 不採用候補 |
| B 役割終了の試験だけを二群で整理 | G04二件とG11三件、G11三件専用の補助処理を削除 | 小さい意味単位 | 追加処理・記憶なし | 現在安全、現役正本、互換性試験を残し、役割終了だけを除く | 2 test file、5試験 | 補助処理残骸を残さず、1 commitで戻せる | 採用候補 |
| C 製品コードと混在試験も同時整理 | Bに加え、未使用の処理目録生成器とG04混在二件を整理 | 複雑 | 調査と確認が増える | 広い整理はできるが、製品コード削除と現役保証の分離を同時に扱う | test以外を含む複数path | 原因切分けと戻し方が複雑 | 後続へ分離 |

【判断】案Bを推奨する。案Aは利用者が承認済みで既存判断だけで実施できる最小案だが、一件ずつ同じ手続きを
繰り返す問題を残す。案Bは製品コードに触れず、G04とG11で確認済みの役割終了だけを意味単位にまとめる。
案Cは必要な保証に対して範囲が広すぎる。

## 4. 案Bの変更範囲

変更を次の二ファイルに限定する。

### `tests/test_claude_bootstrap_entrypoints.py`

次の二試験を削除する。

1. `test_declaration_map_keys_equal_scope_requirement_ids`
2. `test_red_evidence_keeps_green_fields_explicitly_unimplemented`

二番目は利用者が削除承認済みである。一番目は本計画で新たにHuman承認を求める。

### `tests/test_pilot_collaboration_entrypoints.py`

次の三試験を削除する。

1. `test_change_scope_ignores_later_record_and_todo_commits`
2. `test_change_scope_rejects_forbidden_commit_before_later_allowed_commit`
3. `test_change_scope_does_not_hide_code_inside_handoff_directory`

三件だけが使う次の試験専用要素も同じfileから削除する。

- `ALLOWED_PATHS`
- `_git`
- `_commit_changed_paths`
- `_is_followup_record`
- `_implementation_paths_since_base`
- `_initialize_test_repository`
- `_commit_test_change`
- `subprocess`の取込

三試験と専用要素の削除は本計画で新たにHuman承認を求める。

## 5. 変更しないもの

- 製品コード、設定、正規入口、案内文書
- RED／GREEN証跡、宣言対応表、範囲レビュー、範囲固定v3、処理目録
- G04の現在安全一件、混在二件、未使用処理と結合する一件
- G06 24件、G07 8件、G11の現在保証75件
- 401件一覧、過去のEvidence・Decision・レビュー記録

【判断】当時の宣言対応表は履歴資料なので、削除するG04二試験への参照が残っても書き換えない。現在の
宣言対応表検査を本作業の合否判定器にしない。履歴の試験名と現在の試験集合が異なることは、Gitの変更履歴と
本実施Evidenceから追跡できる。

## 6. 実施順序

1. 本計画を新規サブエージェントが独立レビューする。
2. 利用者が本計画をClaudeへ手動で渡し、第3段一回目の他社モデル確認を行う。
3. 両確認の結果を固定し、利用者が案B、追加承認4件、変更範囲を明示承認する。
4. 基準commitと対象二ファイルのGit物体識別値を固定する。
5. 対象5試験とG11専用要素だけを削除する。既存の残る試験本文は変更しない。
6. 対象二ファイルを実行し、9件成功、終了コード0を確認する。
7. 正規全試験を実行し、基準1,739件から削除5件だけ減った1,734件成功、失敗・error・除外0、終了コード0を確認する。
8. 変更path、差分、試験結果、未実施、履歴資料を変更しない判断を実施Evidenceへ固定してコミットする。
9. 新規サブエージェントが独立完了レビューを一回行う。Claude確認は追加しない。

## 7. 確認方法

- 変更前後の対象二ファイルから試験識別子を機械収集し、削除が指定5件だけであることを集合差で確認する。
- Python構文木で、G11専用要素の参照が0件になり、残る未使用定義がないことを確認する。
- Git差分が指定二試験ファイルと実施Evidenceだけであることを確認する。
- 残る9試験の本文を、関数名と正規化した構文木で基準commitと比較し、意味変更0件を確認する。
- 対象試験と正規全試験を、それぞれ単独commandの終了コードで確認する。
- `git diff --check`、成果物再読込み、commit後のread-only照合を行う。

## 8. 停止条件

次の場合は実施を開始しない、または作業を停止する。

- 独立レビューまたはClaude確認が`verified`相当でない。
- 利用者が追加4試験の保証廃止を明示承認しない。
- 指定二ファイル以外のコード、設定、証跡、対応表の変更が必要になる。
- 削除対象以外の試験本文変更が必要になる。
- 対象二ファイルが9件成功にならない、または正規全試験が1,734件成功にならない。
- 現在の製品安全または現役正本に新しい利用関係が見つかる。

## 9. 完了条件とHuman判断

本計画作成の完了条件は、独立レビューとClaude確認の結果が揃い、利用者へ次を判断可能な形で返すことである。

1. 案Bを採用するか。
2. 未承認のG04一件とG11三件、合計4件の保証廃止を承認するか。
3. 対象二ファイル、5試験、G11専用要素だけという範囲を承認するか。

本計画の承認は第3段完了の承認ではない。
