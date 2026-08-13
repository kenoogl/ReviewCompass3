# 第3段 最初の試験整理 実施Evidence v1

- 実施日：2026-08-13
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 実施計画：`docs/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2.md`
- 実施計画SHA-256：`c470da1e4ed3b19c548b64db0d817bdec2d1236b747d3388f50eeccf8c6d1147`
- 利用者承認：`records/development/2026-08-13-stage3-first-test-cleanup-implementation-approval-decision-v1.md`
- 利用者承認SHA-256：`de6e39ebad70ae55dd0693251c57df153226e81cd2dfee7009e24a3c65be8ccd`
- 実施前commit：`9ddf8da1788707cdb4137f172e78eb69ca14969b`
- 実施前対象file Git物体識別値：`8323f09c731d6b3f7d3e13e2559d19f8cdc236df`
- 実施前対象file SHA-256：`fefe377808e47d3dae1330bf708fba951522a8a6010411af97756b5842b1a2a5`

## 1. 実施

【実測】変更した試験fileは`tests/test_claude_bootstrap_entrypoints.py`一件だけである。次の二試験を
削除した。

1. `test_declaration_map_keys_equal_scope_requirement_ids`
2. `test_red_evidence_keeps_green_fields_explicitly_unimplemented`

【実測】一番目の試験だけが使っていた`MAP_PATH`と`REQUIREMENT_IDS`も同時に削除した。差分は28行の
削除だけで、追加行は0行だった。

## 2. 変更範囲の機械照合

【実測】実施前commitの対象fileと現在fileをPython構文木で比較した結果は次のとおりだった。

- 削除された試験：指定二件だけ
- 追加された試験：0件
- 残る試験：六件
- 残る六試験の構文木差分：0件
- 削除されたmodule名：`MAP_PATH`と`REQUIREMENT_IDS`だけ
- 照合command終了コード：0

【実測】`git diff --check -- tests/test_claude_bootstrap_entrypoints.py`は終了コード0だった。

## 3. 対象試験

次を単独commandとして実行した。

```text
.venv/bin/python3 -B -m pytest -q tests/test_claude_bootstrap_entrypoints.py
```

【実測】六件成功、失敗0件、終了コード0、所要時間1.54秒だった。

## 4. 正規全試験

次を単独commandとして実行した。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage3-first-test-cleanup-full-receipt-v1.json
```

【実測】結果は次のとおりだった。

- 成功：1,737件
- 失敗：0件
- エラー：0件
- 除外：0件
- 終了コード：0
- Python：3.13.14
- pytest：8.4.2
- 代替実行：なし
- 結果記録SHA-256：`fb3aaf9498053a6b39fa880b67682e778707e4c3c60bcf3a5665fa508a00bf0f`
- 状態識別値：`bfeb3a3ef222c87907505091575c60ada2be0a3e58d07e6d707bb84a92b9cce9`

【実測】計画の期待値である1,739件から指定二件だけ減った1,737件と一致した。

## 5. 変更しなかったもの

【実測】G11三試験、G11専用補助処理、`tests/test_pilot_collaboration.py`の現行`TRACEABILITY`、製品コード、
設定、正規入口、RED／GREEN証跡、宣言対応表、履歴資料は変更していない。

## 6. 判断

【判断】利用者が承認した案Bの変更範囲どおりに実施できた。現在保証を維持しながら、G04の履歴時点固定
二試験と専用定数二件を現役試験集合から除いた。第3段全体の完了条件はまだ満たしたと判断しない。

## 7. 未実施

他の意味群の削除・統合、G11要求証拠の廃止・置換、製品コード整理、設定変更、外部送信、push、履歴書換え、
第3段完了判断は行っていない。本実施の独立完了レビューは本記録の固定後に新規サブエージェントが行う。
