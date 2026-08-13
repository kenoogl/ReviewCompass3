# 第3段 最初の試験整理 実施計画 v2

- 作成日：2026-08-13
- 状態：`proposed_pending_correction_review_and_human_review`
- 基準commit：`b15be8a63acab71378263fdda1600f35c3839aa0`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 危険度案：`medium`
- 実施前Human承認：必要
- 他社モデル確認：第3段で予定する一回目。本v2の変更点確認に限定する

## 1. v1からの限定修正

v1の独立レビューで、G11の削除予定三試験が現行`tests/test_pilot_collaboration.py`の
`TRACEABILITY`から`NG-PC-007`、`ST-PC-001`、`OUT-PC-004`の証拠として計七回参照されていることが
判明した。三試験は以前の補正で恒久的な変更範囲試験として明示的に残されたものであり、現役要求との接続を
廃止または置換するHuman判断なしに役割終了とは扱えない。

本v2はG11の三試験と専用補助処理を変更範囲から外し、G04で役割終了と確認済みの二試験だけを最初の
整理単位とする。G11の分類は先行抽出Evidence v2の`役割終了`を採用せず、今回の整理では`現在保証`として
維持する。

限定修正の根拠：

- v1：`docs/development/2026-08-13-stage3-first-multi-group-test-cleanup-implementation-plan-v1.md`
  - SHA-256：`aa64f44c8795b61d1a76cad4374d6463e9bd061ab14ab87cdd739850fb63bc07`
- v1独立レビュー：
  `records/development/2026-08-13-stage3-first-multi-group-test-cleanup-implementation-plan-independent-review-v1.md`
  - SHA-256：`f9966ff0135be6cd01c128d60ffec96218000d0ede4722a838b79f2690115f51`
- G04役割分類v2：`records/development/2026-08-13-stage3-g04-role-classification-evidence-v2.md`
  - SHA-256：`db16c07912ed13250f17faa017c71538bc277b79b133c3cf6874cd6ae789a834`
- G04限定修正後確認：
  `records/development/2026-08-13-stage3-g04-role-classification-evidence-v2-one-time-correction-review-v1.md`
  - SHA-256：`e61b337012f4771405c5e127235d559c8801d6c54099bfd8fb1b8e7ab3a84681`
- 手動確認回数Decision：
  `records/development/2026-08-13-stage3-manual-external-review-limit-decision-v1.md`
  - SHA-256：`9c0bd9d371b1f6b59be49818b759d17e3877d645f42ff6dc4a4c0eacbeb05136`

## 2. 三案比較

| 案 | 内容 | 単純さ | 処理時間・記憶量 | 頑健さ | 変更範囲 | 保守負担・戻しやすさ | 判断 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A 承認済み一件だけ | RED証跡三文言試験だけを削除 | 最も小さい | 差は最小 | 製品保証は維持するが、同じ履歴固定の一件を残す | 1 file、1試験 | 戻しやすいが同じ責務を分割する | 不採用候補 |
| B G04の役割終了二件 | 履歴対応表とRED証跡を固定する二試験と専用定数を削除 | 小さい意味単位 | 追加処理・記憶なし | 現在安全、現役正本、互換性試験を残し、役割終了だけを除く | 1 test file、2試験 | 同じ履歴固定を一度に整理し、1 commitで戻せる | 採用候補 |
| C G11も同時整理 | Bに加えてG11三試験と専用補助処理を削除 | 広い | 確認と裁定が増える | 現役要求三件の証拠を失い、別の意味的裁定が必要 | 3 test file以上 | 要求廃止・置換まで連鎖する | 不採用 |

【判断】案Bを推奨する。案Aは既存機能だけで済む最小案だが、同じG04履歴固定の責務を分割する。案Bは
製品コードと現役要求へ触れず、同じfileにある二つの役割終了試験だけを整理できる。案Cはv1レビューで
現在保証を失うことが判明したため採用しない。

実行時間や試験件数の減少は採否の中心根拠にしない。

## 3. 案Bの変更範囲

変更する試験fileは`tests/test_claude_bootstrap_entrypoints.py`一件だけとし、次の二試験を削除する。

1. `test_declaration_map_keys_equal_scope_requirement_ids`
2. `test_red_evidence_keeps_green_fields_explicitly_unimplemented`

二番目は利用者が削除承認済みである。一番目は本計画で新たにHuman承認を求める。

一番目だけが使う次の試験専用定数も同じfileから削除する。

- `MAP_PATH`
- `REQUIREMENT_IDS`

`MANIFEST_ROOT`は残る試験が使うため維持する。他のimport、定数、補助関数、残る六試験の本文は変更しない。

実施Evidence一件は`records/development/`へ追加する。コード変更pathは上記試験fileだけとする。

## 4. 変更しないもの

- 製品コード、設定、正規入口、案内文書
- RED／GREEN証跡、宣言対応表、範囲レビュー、範囲固定v3、処理目録
- G04の現在安全一件、混在二件、現役正本と結ぶ一件、未使用処理と結合する一件
- G11三試験、`tests/test_pilot_collaboration.py`の`TRACEABILITY`、G11専用補助処理
- G06、G07、その他のG11試験
- 401件一覧、過去のEvidence・Decision・レビュー記録

【判断】当時のG04宣言対応表は履歴資料なので、削除する二試験への参照が残っても書き換えない。現在の
宣言対応表検査を本作業の合否判定器にしない。対照的にG11の`TRACEABILITY`は現行試験が参照先の実在を
検査しているため、履歴資料とみなさず現在保証として維持する。

## 5. 実施順序

1. v1を確認した同じ独立レビュー担当が、本v2で先行指摘一件だけが解消したか確認する。
2. 利用者が本v2と修正後確認をClaudeへ手動で渡し、第3段一回目の他社モデル確認を行う。
3. 両確認の結果を固定し、利用者が案B、追加一試験、変更範囲を明示承認する。
4. 基準commitと対象fileのGit物体識別値を固定する。
5. 対象二試験と専用定数二件だけを削除する。既存の残る試験本文は変更しない。
6. 対象fileを実行し、六件成功、終了コード0を確認する。
7. 正規全試験を実行し、基準1,739件から削除二件だけ減った1,737件成功、失敗・error・除外0、終了コード0を確認する。
8. 変更path、差分、試験結果、未実施、履歴資料を変更しない判断を実施Evidenceへ固定してコミットする。
9. 新規サブエージェントが独立完了レビューを一回行う。Claude確認は追加しない。

## 6. 確認方法

- 対象fileから試験識別子を機械収集し、削除が指定二件だけで、八件から六件になることを集合差で確認する。
- Python構文木で`MAP_PATH`と`REQUIREMENT_IDS`の参照が削除対象だけであることを実施前に再確認する。
- Git差分が指定試験fileと実施Evidenceだけであることを確認する。
- 残る六試験の本文を、関数名と正規化した構文木で基準commitと比較し、意味変更0件を確認する。
- 対象fileと正規全試験を、それぞれ単独commandの終了コードで確認する。
- `git diff --check`、成果物再読込み、commit後のread-only照合を行う。

## 7. 停止条件

次の場合は実施を開始しない、または作業を停止する。

- 限定修正後確認またはClaude確認が`verified`相当でない。
- 利用者が追加一試験の保証廃止を明示承認しない。
- 指定試験file以外のコード、設定、証跡、対応表の変更が必要になる。
- 削除対象以外の試験本文変更が必要になる。
- 対象fileが六件成功にならない、または正規全試験が1,737件成功にならない。
- 現在の製品安全または現役正本に新しい利用関係が見つかる。

## 8. 完了条件とHuman判断

本計画作成の完了条件は、限定修正後確認とClaude確認の結果が揃い、利用者へ次を判断可能な形で返すことである。

1. 案Bを採用するか。
2. 未承認の`test_declaration_map_keys_equal_scope_requirement_ids`の保証廃止を承認するか。
3. 対象試験file一件、二試験、専用定数二件だけという範囲を承認するか。

本計画の承認は第3段完了の承認ではない。
