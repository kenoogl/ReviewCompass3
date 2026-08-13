# Claude向け 第3段 最初の試験整理 実施計画v2 変更点レビュー指示 v1

次の実施計画v2を独立レビューしてください。レビュー対象は、先行指摘に対するv1からv2への変更点だけです。
fileの作成・変更、試験削除、試験実行、commit、外部送信はしないでください。

## 固定対象

- v1観測commit：`1dac94d`
- v1計画：`docs/development/2026-08-13-stage3-first-multi-group-test-cleanup-implementation-plan-v1.md`
  - SHA-256：`aa64f44c8795b61d1a76cad4374d6463e9bd061ab14ab87cdd739850fb63bc07`
- v1独立レビュー：
  `records/development/2026-08-13-stage3-first-multi-group-test-cleanup-implementation-plan-independent-review-v1.md`
  - SHA-256：`f9966ff0135be6cd01c128d60ffec96218000d0ede4722a838b79f2690115f51`
- v2観測commit：`29bcd0e`
- v2計画：`docs/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2.md`
  - SHA-256：`c470da1e4ed3b19c548b64db0d817bdec2d1236b747d3388f50eeccf8c6d1147`
- v2一回限り修正後確認：
  `records/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2-one-time-correction-review-v1.md`
  - SHA-256：`0afc66a36878dc431d7a3e9105b82b2e49c7c0886b8129211460d4c73cf09c45`

## 先行指摘と修正意図

v1はG04二試験とG11三試験を削除候補にした。しかしG11三試験は現行
`tests/test_pilot_collaboration.py`の`TRACEABILITY`から、`NG-PC-007`、`ST-PC-001`、`OUT-PC-004`の
証拠として計七回参照されていた。二つの試験fileだけを削除すると現役の参照実在検査が失敗するため、v1は
`correction_required`になった。

v2はG11三試験、専用補助処理、`TRACEABILITY`をすべて変更対象外へ戻した。実施候補は
`tests/test_claude_bootstrap_entrypoints.py`のG04二試験と、一試験だけが使う専用定数二件に縮小した。

## 変更点だけの確認事項

次を実file、構文木、参照検索、Git objectの読み取りで確認してください。

1. G11三試験、専用補助処理、`TRACEABILITY`がv2の変更範囲から完全に外れ、現役要求の保証が維持される。
2. G04の次の二試験が、固定済み役割分類どおり現在の製品処理や現役正本を保証せず、履歴時点の成果物を固定する役割である。
   - `test_declaration_map_keys_equal_scope_requirement_ids`
   - `test_red_evidence_keeps_green_fields_explicitly_unimplemented`
3. `MAP_PATH`と`REQUIREMENT_IDS`は一番目の削除対象試験だけが使い、同時削除して残る利用者がない。
4. 対象fileは現在八試験で、指定二試験の削除後は六試験になる。全体基準1,739件からは1,737件になる。
5. 残る六試験、製品コード、設定、履歴資料、対応表を変更しない境界が意味的に完結している。
6. 新たなHuman承認対象が未承認の一試験と専用定数に限定され、承認済み一試験と混同されていない。

中心判断を崩す反証を最低一件だけ機械で試してください。例えば、削除対象二試験または専用定数が現在の
製品安全、現役正本、正規入口、別の現役検査から実際に利用されていることを示せるか確認します。

## 範囲制限

- 401件全体、別群、G11の要求証拠の廃止・置換、製品コード整理を再調査しない。
- 新しい台帳、検査器、試験、強制関門、履歴専用入口を提案しない。
- G04の履歴対応表を現在の合否判定器へ戻さない。履歴資料自体も書き換えない。
- 実行時間や削減件数を採否の中心根拠にしない。
- 文体、好み、より完全な一般解を理由に修正要としない。
- 本質から外れた過剰な修正案を出さない。止める指摘は、v2の変更点が現在保証を失う、範囲が不完結、計数や参照が誤る場合だけにする。
- 実装の最終承認、第3段完了の判断はしない。利用者が判断する点として返す。

## 出力形式

1. 判定：`verified`または`修正要`
2. 先行指摘が解消したか
3. 止める指摘
4. 報告不一致
5. 変更範囲と現在保証の確認
6. 試した反証と結果
7. 利用者が判断する点
8. 未実施
