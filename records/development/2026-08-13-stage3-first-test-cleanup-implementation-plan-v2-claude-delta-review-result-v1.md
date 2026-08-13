# 第3段 最初の試験整理 実施計画v2 Claude変更点レビュー結果 v1

- 記録日：2026-08-13
- 受渡方法：利用者による手動転記
- 指示書：`records/session-handoffs/2026-08-13-claude-stage3-first-test-cleanup-implementation-plan-v2-delta-review-prompt-v1.md`
- 指示書SHA-256：`953a92312e97181d90ff150650bc0b09d0a3daf2e974f7d1ebddf8a766957f42`
- Codexによる外部送信：未実施
- 本記録による実装承認：行わない
- 本記録による第3段完了判断：行わない

## 1. 判定

`verified`

固定対象六件はすべて実在し、SHA-256は全件一致した。v2が固定するG04役割分類v2、限定修正後確認、
手動確認回数Decisionの三件も再計算で一致したとの報告を受領した。

## 2. 先行指摘

解消。v1で削除候補だったG11三試験は、現行`TRACEABILITY`から計七回参照されていた。v2はG11三試験、
専用補助処理、`tests/test_pilot_collaboration.py`を変更対象外へ戻し、G04二試験と専用定数二件だけへ
範囲を縮小した。G11の参照先三試験は現存し、現在の参照実在検査は影響を受けないとの報告を受領した。

## 3. 止める指摘と報告不一致

- 止める指摘：0件
- 報告不一致：0件

## 4. 変更範囲と現在保証

- G11三試験、専用補助処理、現行`TRACEABILITY`は変更しない。
- 削除候補は`tests/test_claude_bootstrap_entrypoints.py`の次の二試験である。
  - `test_declaration_map_keys_equal_scope_requirement_ids`
  - `test_red_evidence_keeps_green_fields_explicitly_unimplemented`
- 二試験は製品コード、設定、正規入口、現役正本を保証せず、履歴時点の成果物を固定する役割であるとの
  照合結果を受領した。
- `MAP_PATH`と`REQUIREMENT_IDS`は一番目の削除候補だけが使い、削除後の利用者は0件である。
- `MANIFEST_ROOT`は残る`BASELINE_PATH`が使うため維持する。
- 対象fileは現在八試験で、削除後は六試験になる。基準1,739件から削除後1,737件という計数が成立する。
- `RED_START_COMMIT`は削除前から未使用であり、今回の削除で新たに生じる残骸ではないため変更しない。

## 5. 試した反証

1. 二試験名の全tree検索では、製品コード、設定、現役案内、他の試験コードからの利用は0件だった。
2. v1と同じく現行`TRACEABILITY`から参照される可能性を調べたが、G04二試験名の参照はなかった。
3. `declaration-red-map-v1.json`を読む現役toolや設定を検索したが、該当はG04作業票文書だけで、
   manifest自体は削除対象外だった。

中心判断を崩す反証はいずれも成立しなかったとの報告を受領した。

## 6. 利用者が判断する点

1. G04の役割終了二試験と専用定数二件を削除する案Bを採用するか。
2. 未承認の`test_declaration_map_keys_equal_scope_requirement_ids`の保証廃止を承認するか。
3. 変更範囲を試験file一件、二試験、専用定数二件に限定することを承認するか。

`test_red_evidence_keeps_green_fields_explicitly_unimplemented`の削除は承認済みである。

## 7. 未実施

Claude側はfileの作成・変更、試験の削除・実行、stage、commit、push、履歴書換え、外部送信を行っていない
との報告だった。401件全体、別群、G11要求証拠の再調査、新機構の提案、G04履歴対応表の現在の合否判定器
への転用も行っていない。本記録の作成時点でも削除実装と第3段完了判断は未実施である。
